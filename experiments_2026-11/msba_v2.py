"""MSBA-Net v2 candidates (2026-11-18, author asked overnight for the model to be improved; design chosen on validation
data only). Motivation from the results so far: MSBA-Net keeps full-resolution detail (wins on small defects) but its
bottleneck has a limited receptive field, while the models that win on NEU-Seg (HRNet-W18, SegFormer-B1, DeepLabv3+)
aggregate wide or global context. Both candidates keep the author's MSBA-Net unchanged and add one context module on
the 1/16-resolution bottleneck feature (residual, so it starts close to the original network):
  MSBANetV2a: multi-rate dilated context (rates 1, 2, 4, 8) + image-level pooling branch (ASPP-style).
  MSBANetV2b: two transformer blocks (8-head self-attention + depthwise-conv MLP) over the bottleneck tokens.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from models import MSBANet


def cbr(i, o, k=1, d=1):
    return nn.Sequential(nn.Conv2d(i, o, k, padding=d * (k // 2), dilation=d, bias=False), nn.BatchNorm2d(o), nn.ReLU(inplace=True))


class DilatedContext(nn.Module):
    def __init__(self, ch, mid=128):
        super().__init__()
        self.br = nn.ModuleList([cbr(ch, mid, 1)] + [cbr(ch, mid, 3, d) for d in (2, 4, 8)])
        self.pool = cbr(ch, mid, 1)
        self.proj = cbr(5 * mid, ch, 1)

    def forward(self, x):
        g = F.interpolate(self.pool(F.adaptive_avg_pool2d(x, 1)), size=x.shape[-2:], mode="nearest")
        return x + self.proj(torch.cat([b(x) for b in self.br] + [g], 1))


class TBlock(nn.Module):
    def __init__(self, d, heads=8):
        super().__init__()
        self.n1, self.n2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.o, self.h = nn.Linear(d, 3 * d), nn.Linear(d, d), heads
        self.fc1, self.dw, self.fc2 = nn.Linear(d, 4 * d), nn.Conv2d(4 * d, 4 * d, 3, padding=1, groups=4 * d), nn.Linear(4 * d, d)

    def forward(self, t, H, W):
        B, N, D = t.shape
        q, k, v = self.qkv(self.n1(t)).view(B, N, 3, self.h, D // self.h).permute(2, 0, 3, 1, 4)
        t = t + self.o(F.scaled_dot_product_attention(q, k, v).transpose(1, 2).reshape(B, N, D))
        y = self.fc1(self.n2(t)).transpose(1, 2).reshape(B, -1, H, W)
        return t + self.fc2(F.gelu(self.dw(y)).flatten(2).transpose(1, 2))


class GlobalContext(nn.Module):
    def __init__(self, ch, d=256, depth=2):
        super().__init__()
        self.inp, self.blocks, self.out = nn.Conv2d(ch, d, 1), nn.ModuleList([TBlock(d) for _ in range(depth)]), cbr(d, ch, 1)

    def forward(self, x):
        B, _, H, W = x.shape
        t = self.inp(x).flatten(2).transpose(1, 2)
        for b in self.blocks:
            t = b(t, H, W)
        return x + self.out(t.transpose(1, 2).reshape(B, -1, H, W))


class _V2(MSBANet):
    ctx_cls = None

    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__(in_channels, num_classes, base_ch)
        self.context = self.ctx_cls(base_ch * 16)

    def forward(self, x):          # identical to the author's MSBANet.forward except for the context module on b
        e1 = self.msfp1(self.enc1(x))
        e2 = self.msfp2(self.enc2(F.max_pool2d(e1, 2)))
        e3 = self.msfp3(self.enc3(F.max_pool2d(e2, 2)))
        e4 = self.msfp4(self.enc4(F.max_pool2d(e3, 2)))
        b = self.context(self.bottleneck(F.max_pool2d(e4, 2)))
        b_feat2 = self.b_conv3(torch.cat([self.b_up3(e3), e2], dim=1))
        b_feat1 = self.b_conv2(torch.cat([self.b_up2(b_feat2), e1], dim=1))
        pred_boundary = self.b_head(b_feat1)
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        return self.seg_head(self.bg_fusion(d1, b_feat1)), pred_boundary


class MSBANetV2a(_V2):
    ctx_cls = DilatedContext


class MSBANetV2b(_V2):
    ctx_cls = GlobalContext


class MSBANetV2c(MSBANetV2a):
    """v2a + the same dilated-context module on the 1/8-resolution encoder feature e4 (before its skip and pooling)."""
    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__(in_channels, num_classes, base_ch)
        self.context4 = DilatedContext(base_ch * 8, mid=64)

    def forward(self, x):
        e1 = self.msfp1(self.enc1(x))
        e2 = self.msfp2(self.enc2(F.max_pool2d(e1, 2)))
        e3 = self.msfp3(self.enc3(F.max_pool2d(e2, 2)))
        e4 = self.context4(self.msfp4(self.enc4(F.max_pool2d(e3, 2))))
        b = self.context(self.bottleneck(F.max_pool2d(e4, 2)))
        b_feat2 = self.b_conv3(torch.cat([self.b_up3(e3), e2], dim=1))
        b_feat1 = self.b_conv2(torch.cat([self.b_up2(b_feat2), e1], dim=1))
        pred_boundary = self.b_head(b_feat1)
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        return self.seg_head(self.bg_fusion(d1, b_feat1)), pred_boundary


class _Stack2(nn.Module):
    def __init__(self, ch):
        super().__init__(); self.a, self.b = DilatedContext(ch), DilatedContext(ch)

    def forward(self, x):
        return self.b(self.a(x))


class MSBANetV2d(_V2):
    """v2a with two stacked dilated-context modules on the bottleneck."""
    ctx_cls = _Stack2
