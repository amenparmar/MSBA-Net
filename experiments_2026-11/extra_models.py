"""Two further baselines, written from the published designs (no pretrained weights, no external packages):
HRNetV2-W18 (Wang et al., TPAMI 2021) and SegFormer MiT-B1 with the all-MLP decoder (Xie et al., NeurIPS 2021).
Both take a 1-channel input and return (logits at input resolution, None) like the other models."""
import torch
import torch.nn as nn
import torch.nn.functional as F


# ------------------------------------------------------------------------------------------------ HRNetV2-W18
def cbr(i, o, k=3, s=1, relu=True):
    layers = [nn.Conv2d(i, o, k, s, k // 2, bias=False), nn.BatchNorm2d(o)]
    if relu:
        layers.append(nn.ReLU(inplace=True))
    return nn.Sequential(*layers)


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, i, o, s=1, down=None):
        super().__init__()
        self.c1 = cbr(i, o, 3, s); self.c2 = cbr(o, o, 3, 1, relu=False); self.down = down

    def forward(self, x):
        r = x if self.down is None else self.down(x)
        return F.relu(self.c2(self.c1(x)) + r)


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, i, p, s=1, down=None):
        super().__init__()
        self.c1 = cbr(i, p, 1); self.c2 = cbr(p, p, 3, s); self.c3 = cbr(p, p * 4, 1, relu=False); self.down = down

    def forward(self, x):
        r = x if self.down is None else self.down(x)
        return F.relu(self.c3(self.c2(self.c1(x))) + r)


class HRModule(nn.Module):
    def __init__(self, ch, blocks=4):
        super().__init__()
        n = len(ch)
        self.branches = nn.ModuleList([nn.Sequential(*[BasicBlock(c, c) for _ in range(blocks)]) for c in ch])
        self.fuse = nn.ModuleList()
        for i in range(n):
            row = nn.ModuleList()
            for j in range(n):
                if j > i:
                    row.append(cbr(ch[j], ch[i], 1, relu=False))
                elif j == i:
                    row.append(nn.Identity())
                else:
                    steps = [cbr(ch[j], ch[j], 3, 2) for _ in range(i - j - 1)] + [cbr(ch[j], ch[i], 3, 2, relu=False)]
                    row.append(nn.Sequential(*steps))
            self.fuse.append(row)

    def forward(self, xs):
        xs = [b(x) for b, x in zip(self.branches, xs)]
        out = []
        for i, row in enumerate(self.fuse):
            y = 0
            for j, f in enumerate(row):
                z = f(xs[j])
                if j > i:
                    z = F.interpolate(z, size=xs[i].shape[-2:], mode="bilinear", align_corners=False)
                y = y + z
            out.append(F.relu(y))
        return out


class HRNetW18(nn.Module):
    """HRNetV2-W18: stem to 1/4, stage 1 (4 bottlenecks), stages 2-4 with 1/4/3 modules and 2/3/4 branches
    (widths 18/36/72/144), HRNetV2 head (all branches upsampled and concatenated)."""
    def __init__(self, in_channels=1, num_classes=1):
        super().__init__()
        self.stem = nn.Sequential(cbr(in_channels, 64, 3, 2), cbr(64, 64, 3, 2))
        down = nn.Sequential(nn.Conv2d(64, 256, 1, bias=False), nn.BatchNorm2d(256))
        self.layer1 = nn.Sequential(Bottleneck(64, 64, down=down), *[Bottleneck(256, 64) for _ in range(3)])
        w = [18, 36, 72, 144]
        self.t1 = nn.ModuleList([cbr(256, w[0]), cbr(256, w[1], 3, 2)])
        self.s2 = nn.Sequential(HRModule(w[:2]))
        self.t2 = cbr(w[1], w[2], 3, 2)
        self.s3 = nn.Sequential(*[HRModule(w[:3]) for _ in range(4)])
        self.t3 = cbr(w[2], w[3], 3, 2)
        self.s4 = nn.Sequential(*[HRModule(w) for _ in range(3)])
        self.head = nn.Sequential(cbr(sum(w), sum(w), 1), nn.Conv2d(sum(w), num_classes, 1))

    def forward(self, x):
        h, wd = x.shape[-2:]
        y = self.layer1(self.stem(x))
        xs = [t(y) for t in self.t1]
        xs = self.s2(xs)
        xs = self.s3(xs + [self.t2(xs[-1])])
        xs = self.s4(xs + [self.t3(xs[-1])])
        s = xs[0].shape[-2:]
        y = torch.cat([xs[0]] + [F.interpolate(z, size=s, mode="bilinear", align_corners=False) for z in xs[1:]], 1)
        return F.interpolate(self.head(y), size=(h, wd), mode="bilinear", align_corners=False), None


# ------------------------------------------------------------------------------------------------ SegFormer MiT-B1
class OverlapPatchEmbed(nn.Module):
    def __init__(self, i, o, k, s):
        super().__init__()
        self.proj = nn.Conv2d(i, o, k, s, k // 2); self.norm = nn.LayerNorm(o)

    def forward(self, x):
        x = self.proj(x); h, w = x.shape[-2:]
        return self.norm(x.flatten(2).transpose(1, 2)), h, w


class EfficientAttention(nn.Module):
    def __init__(self, dim, heads, sr):
        super().__init__()
        self.h = heads; self.q = nn.Linear(dim, dim); self.kv = nn.Linear(dim, 2 * dim); self.proj = nn.Linear(dim, dim)
        self.sr = sr
        if sr > 1:
            self.sr_conv = nn.Conv2d(dim, dim, sr, sr); self.sr_norm = nn.LayerNorm(dim)

    def forward(self, x, h, w):
        b, n, c = x.shape
        q = self.q(x).reshape(b, n, self.h, c // self.h).transpose(1, 2)
        if self.sr > 1:
            y = self.sr_conv(x.transpose(1, 2).reshape(b, c, h, w)).flatten(2).transpose(1, 2)
            y = self.sr_norm(y)
        else:
            y = x
        k, v = self.kv(y).reshape(b, -1, 2, self.h, c // self.h).permute(2, 0, 3, 1, 4)
        o = F.scaled_dot_product_attention(q, k, v)
        return self.proj(o.transpose(1, 2).reshape(b, n, c))


class MixFFN(nn.Module):
    def __init__(self, dim, ratio=4):
        super().__init__()
        hid = dim * ratio
        self.fc1 = nn.Linear(dim, hid); self.dw = nn.Conv2d(hid, hid, 3, 1, 1, groups=hid); self.fc2 = nn.Linear(hid, dim)

    def forward(self, x, h, w):
        b, n, _ = x.shape
        y = self.fc1(x)
        y = self.dw(y.transpose(1, 2).reshape(b, -1, h, w)).flatten(2).transpose(1, 2)
        return self.fc2(F.gelu(y))


class MiTBlock(nn.Module):
    def __init__(self, dim, heads, sr):
        super().__init__()
        self.n1 = nn.LayerNorm(dim); self.attn = EfficientAttention(dim, heads, sr)
        self.n2 = nn.LayerNorm(dim); self.ffn = MixFFN(dim)

    def forward(self, x, h, w):
        x = x + self.attn(self.n1(x), h, w)
        return x + self.ffn(self.n2(x), h, w)


class SegFormerB1(nn.Module):
    """MiT-B1 encoder (widths 64/128/320/512, depths 2/2/2/2, heads 1/2/5/8, reduction 8/4/2/1) and the
    all-MLP decoder (256 channels); prediction at 1/4 resolution, bilinearly upsampled."""
    def __init__(self, in_channels=1, num_classes=1, dims=(64, 128, 320, 512), depths=(2, 2, 2, 2),
                 heads=(1, 2, 5, 8), srs=(8, 4, 2, 1), dec=256):
        super().__init__()
        self.embeds = nn.ModuleList([OverlapPatchEmbed(in_channels if i == 0 else dims[i - 1], dims[i],
                                                       7 if i == 0 else 3, 4 if i == 0 else 2) for i in range(4)])
        self.blocks = nn.ModuleList([nn.ModuleList([MiTBlock(dims[i], heads[i], srs[i]) for _ in range(depths[i])])
                                     for i in range(4)])
        self.norms = nn.ModuleList([nn.LayerNorm(d) for d in dims])
        self.lin = nn.ModuleList([nn.Linear(d, dec) for d in dims])
        self.fuse = nn.Sequential(nn.Conv2d(4 * dec, dec, 1, bias=False), nn.BatchNorm2d(dec), nn.ReLU(inplace=True))
        self.drop = nn.Dropout2d(0.1); self.cls = nn.Conv2d(dec, num_classes, 1)

    def forward(self, x):
        H, W = x.shape[-2:]; feats = []
        for emb, blks, norm in zip(self.embeds, self.blocks, self.norms):
            t, h, w = emb(x)
            for blk in blks:
                t = blk(t, h, w)
            x = norm(t).transpose(1, 2).reshape(t.shape[0], -1, h, w); feats.append(x)
        s = feats[0].shape[-2:]; outs = []
        for f, lin in zip(feats, self.lin):
            y = lin(f.flatten(2).transpose(1, 2)).transpose(1, 2).reshape(f.shape[0], -1, *f.shape[-2:])
            outs.append(F.interpolate(y, size=s, mode="bilinear", align_corners=False))
        y = self.cls(self.drop(self.fuse(torch.cat(outs[::-1], 1))))
        return F.interpolate(y, size=(H, W), mode="bilinear", align_corners=False), None
