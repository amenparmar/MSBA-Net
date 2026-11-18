"""Shared code for the 2026-11-16 experiment programme (reviewer issues C3, C4, C5, M1, M3, M5, M7, M8).
Uses the author's original model / dataset / loss code read-only from D:/scratch/3rs sem (identical to
D:/scratch/industrial_defect_segmentation for models.py, dataset.py, losses.py). Adds two extra baselines
(Attention U-Net, DeepLabv3+), fixed cached splits, a held-out test set, and multi-seed training."""
import os, sys, json, time, math, random
sys.dont_write_bytecode = True
# author's original code (models.py, dataset.py, losses.py, run_ablations.py): local copy, or the repository root
# (parent of this folder) when the code is used from https://github.com/amenparmar/MSBA-Net
CODE = os.environ.get("MSBA_CODE") or ("D:/scratch/3rs sem" if os.path.isdir("D:/scratch/3rs sem")
                                       else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if CODE not in sys.path:
    sys.path.insert(0, CODE)
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from models import ConvBlock, UNet, UNetPlusPlus, MSBANet          # author's code
from run_ablations import UNet_MSFP, MSBANet_NoBGFF                 # author's ablation variants
from losses import CompositeLoss                                    # author's loss
from dataset import IndustrialDefectDataset                         # author's generator

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache"); os.makedirs(CACHE, exist_ok=True)
RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
DEV = torch.device("cuda")
torch.backends.cudnn.benchmark = False
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
SEEDS = [42, 100, 2026, 7, 123]
TEST_SEED = 5000          # synthetic test generator seed (val-mode rng = 6000); never used for training or selection
CONDITIONS = ["normal", "tiny_defects", "low_contrast", "blur", "noise"]


# ------------------------------------------------------------------------------------------------
# Extra baselines (standard designs; trained from scratch like every other model, no pretraining)
# ------------------------------------------------------------------------------------------------
class AttentionGate(nn.Module):
    """Additive attention gate of Oktay et al. (2018)."""
    def __init__(self, g_ch, x_ch, inter):
        super().__init__()
        self.wg = nn.Sequential(nn.Conv2d(g_ch, inter, 1, bias=False), nn.BatchNorm2d(inter))
        self.wx = nn.Sequential(nn.Conv2d(x_ch, inter, 1, bias=False), nn.BatchNorm2d(inter))
        self.psi = nn.Sequential(nn.Conv2d(inter, 1, 1, bias=False), nn.BatchNorm2d(1), nn.Sigmoid())

    def forward(self, g, x):
        return x * self.psi(F.relu(self.wg(g) + self.wx(x), inplace=True))


class AttentionUNet(nn.Module):
    """U-Net with attention-gated skip connections; same ConvBlock, widths and depth as the author's U-Net."""
    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__()
        c = [base_ch * m for m in (1, 2, 4, 8, 16)]
        self.enc = nn.ModuleList([ConvBlock(in_channels, c[0]), ConvBlock(c[0], c[1]), ConvBlock(c[1], c[2]), ConvBlock(c[2], c[3])])
        self.bottleneck = ConvBlock(c[3], c[4])
        self.ups = nn.ModuleList([nn.ConvTranspose2d(c[i + 1], c[i], 2, stride=2) for i in (3, 2, 1, 0)])
        self.gates = nn.ModuleList([AttentionGate(c[i], c[i], max(c[i] // 2, 8)) for i in (3, 2, 1, 0)])
        self.decs = nn.ModuleList([ConvBlock(c[i] * 2, c[i]) for i in (3, 2, 1, 0)])
        self.out_conv = nn.Conv2d(c[0], num_classes, 1)

    def forward(self, x):
        skips = []
        for i, e in enumerate(self.enc):
            x = e(x if i == 0 else F.max_pool2d(x, 2)); skips.append(x)
        x = self.bottleneck(F.max_pool2d(x, 2))
        for up, gate, dec, s in zip(self.ups, self.gates, self.decs, reversed(skips)):
            x = up(x); x = dec(torch.cat([x, gate(x, s)], 1))
        return self.out_conv(x), None


class DeepLabV3Plus(nn.Module):
    """DeepLabv3+ (Chen et al., 2018): ResNet-50 backbone (output stride 16, no pretraining), ASPP with
    rates 6/12/18, 48-channel low-level projection, two 3x3 decoder convolutions."""
    def __init__(self, in_channels=1, num_classes=1):
        super().__init__()
        r = torchvision.models.resnet50(weights=None, replace_stride_with_dilation=[False, False, True])
        r.conv1 = nn.Conv2d(in_channels, 64, 7, 2, 3, bias=False)
        self.stem = nn.Sequential(r.conv1, r.bn1, r.relu, r.maxpool)
        self.l1, self.l2, self.l3, self.l4 = r.layer1, r.layer2, r.layer3, r.layer4
        self.aspp = torchvision.models.segmentation.deeplabv3.ASPP(2048, [6, 12, 18], 256)
        self.low = nn.Sequential(nn.Conv2d(256, 48, 1, bias=False), nn.BatchNorm2d(48), nn.ReLU(inplace=True))
        self.dec = nn.Sequential(nn.Conv2d(304, 256, 3, padding=1, bias=False), nn.BatchNorm2d(256), nn.ReLU(inplace=True),
                                 nn.Conv2d(256, 256, 3, padding=1, bias=False), nn.BatchNorm2d(256), nn.ReLU(inplace=True),
                                 nn.Conv2d(256, num_classes, 1))

    def forward(self, x):
        h, w = x.shape[-2:]
        low = self.l1(self.stem(x))
        y = self.aspp(self.l4(self.l3(self.l2(low))))
        y = F.interpolate(y, size=low.shape[-2:], mode="bilinear", align_corners=False)
        y = self.dec(torch.cat([y, self.low(low)], 1))
        return F.interpolate(y, size=(h, w), mode="bilinear", align_corners=False), None


MODELS = {
    "UNet": lambda nc: UNet(1, nc, 32),
    "UNetPlusPlus": lambda nc: UNetPlusPlus(1, nc, 32),
    "AttUNet": lambda nc: AttentionUNet(1, nc, 32),
    "DeepLabV3Plus": lambda nc: DeepLabV3Plus(1, nc),
    "MSBANet": lambda nc: MSBANet(1, nc, 32),
    "Arch2_MSFP": lambda nc: UNet_MSFP(1, nc, 32),
    "Arch3_MSFP_BAS": lambda nc: MSBANet_NoBGFF(1, nc, 32),
}
HAS_BOUNDARY = {"MSBANet", "Arch3_MSFP_BAS"}
from extra_models import HRNetW18, SegFormerB1                       # further baselines (2026-11-16, round 2)
MODELS.update({"HRNetW18": lambda nc: HRNetW18(1, nc), "SegFormerB1": lambda nc: SegFormerB1(1, nc)})


def degrade_aug(x, g):
    """Training-time degradation augmentation (round 2). Each image independently gets one of: unchanged,
    contrast scaling about its mean (s ~ U(0.35, 1)), Gaussian blur (one sigma ~ U(0.5, 3) per batch), or additive
    Gaussian noise (sigma ~ U(5, 25) grey levels). The test settings (s = 0.45, radius 2.5, sigma = 18) lie inside
    these ranges."""
    b = x.shape[0]
    op = torch.randint(0, 4, (b,), generator=g, device=x.device)
    x = x.clone()
    m = op == 1
    if m.any():
        s = 0.35 + 0.65 * torch.rand(int(m.sum()), 1, 1, 1, generator=g, device=x.device)
        mu = x[m].mean((1, 2, 3), keepdim=True)
        x[m] = ((x[m] - mu) * s + mu).clamp(0, 1)
    m = op == 2
    if m.any():
        sig = 0.5 + 2.5 * torch.rand(1, generator=g, device=x.device).item()
        k = 2 * math.ceil(3 * sig) + 1
        x[m] = torchvision.transforms.functional.gaussian_blur(x[m], [k, k], [sig, sig])
    m = op == 3
    if m.any():
        sd = (5 + 20 * torch.rand(int(m.sum()), 1, 1, 1, generator=g, device=x.device)) / 255.0
        x[m] = (x[m] + sd * torch.randn(x[m].shape, generator=g, device=x.device)).clamp(0, 1)
    return x


# ------------------------------------------------------------------------------------------------
# Synthetic benchmark: fixed cached splits (train 700 / val 150 per training seed; test 150 per condition)
# ------------------------------------------------------------------------------------------------
def _gen(n, mode, cond, seed):
    d = IndustrialDefectDataset(num_samples=n, mode=mode, condition=cond, seed=seed)
    s = [d[i] for i in range(n)]
    return {"image": torch.stack([x["image"] for x in s]), "mask": torch.stack([x["mask"] for x in s]),
            "boundary": torch.stack([x["boundary"] for x in s]), "cls": [x["defect_type"] for x in s]}


def synth_split(kind, seed=None, cond="normal"):
    name = {"train": f"syn_train_s{seed}.pt", "val": f"syn_val_s{seed}.pt", "test": f"syn_test_{cond}.pt"}[kind]
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        data = {"train": lambda: _gen(700, "train", "normal", seed), "val": lambda: _gen(150, "val", "normal", seed),
                "test": lambda: _gen(150, "val", cond, TEST_SEED)}[kind]()
        torch.save(data, p)
    return torch.load(p)


# ------------------------------------------------------------------------------------------------
# NEU-Seg (real): author's pre-processed tensors (256x256, classes 0 bg / 1 inclusion / 2 patches / 3 scratches)
# fixed 10 % validation hold-out from the official training split (same for every run); official test split for test.
# ------------------------------------------------------------------------------------------------
NEU_TRAIN = os.path.join(CODE, "data", "NEU_Seg", "neu_seg_training.pt")
NEU_TEST = os.path.join(CODE, "data", "NEU_Seg", "neu_seg_test.pt")


def neu_split(kind):
    p = os.path.join(CACHE, f"neu_{kind}.pt")
    if not os.path.exists(p):
        src = torch.load(NEU_TEST if kind == "test" else NEU_TRAIN, map_location="cpu")
        n = len(src["stems"]); idx = torch.arange(n)
        if kind != "test":
            perm = torch.randperm(n, generator=torch.Generator().manual_seed(0))
            nval = n // 10
            idx = perm[:nval] if kind == "val" else perm[nval:]
        torch.save({"image": src["images"][idx].unsqueeze(1).float() / 255.0, "mask": src["masks"][idx].long(),
                    "boundary": src["boundaries"][idx].unsqueeze(1).float() / 255.0,
                    "stems": [src["stems"][i] for i in idx.tolist()]}, p)
    return torch.load(p)


# ------------------------------------------------------------------------------------------------
# Losses
# ------------------------------------------------------------------------------------------------
class MultiClassComposite(nn.Module):
    """NEU-Seg analogue of the paper's loss: CE + 1.0 mDice + 0.5 Focal(gamma 2) [+ lambda_b (BCE + Dice) on the
    binary defect boundary for boundary-supervised models]."""
    def __init__(self, nc=4, lb=0.4):
        super().__init__(); self.nc, self.lb = nc, lb

    def forward(self, logits, y, pb=None, yb=None):
        ce = F.cross_entropy(logits, y, reduction="none")
        pt = torch.exp(-ce)
        focal = ((1 - pt) ** 2 * ce).mean()
        p = logits.softmax(1); oh = F.one_hot(y, self.nc).permute(0, 3, 1, 2).float()
        inter = (p * oh).sum((0, 2, 3)); den = p.sum((0, 2, 3)) + oh.sum((0, 2, 3))
        dice = (1 - (2 * inter + 1) / (den + 1)).mean()
        loss = ce.mean() + dice + 0.5 * focal
        if pb is not None and yb is not None and self.lb > 0:
            sb = torch.sigmoid(pb)
            bd = 1 - (2 * (sb * yb).sum() + 1) / (sb.sum() + yb.sum() + 1)
            loss = loss + self.lb * (F.binary_cross_entropy_with_logits(pb, yb) + bd)
        return loss


# ------------------------------------------------------------------------------------------------
# Metrics: pooled over the whole split (dataset-level), plus per-image foreground IoU (binary only)
# ------------------------------------------------------------------------------------------------
@torch.no_grad()
def predict(model, images, nc, bs=16):
    model.eval(); out = []
    for i in range(0, len(images), bs):
        with torch.autocast("cuda", dtype=torch.bfloat16):
            lg, _ = model(images[i:i + bs].to(DEV, non_blocking=True))
        lg = lg.float()
        out.append((lg.argmax(1) if nc > 1 else (torch.sigmoid(lg[:, 0]) > 0.5).long()).cpu())
    return torch.cat(out)


def binary_metrics(pred, mask):
    y = mask[:, 0].long(); p = pred
    tp = (p & y).sum().item(); fp = (p & (1 - y)).sum().item(); fn = ((1 - p) & y).sum().item()
    e = 1e-9
    inter = (p & y).flatten(1).sum(1).float(); union = (p | y).flatten(1).sum(1).float()
    per_img = torch.where(union > 0, inter / union.clamp(min=1), torch.ones_like(union))
    return {"iou": 100 * tp / (tp + fp + fn + e), "dice": 100 * 2 * tp / (2 * tp + fp + fn + e),
            "precision": 100 * tp / (tp + fp + e), "recall": 100 * tp / (tp + fn + e),
            "iou_per_image": 100 * per_img.mean().item()}


def multiclass_metrics(pred, y, nc=4):
    cm = torch.bincount((y.flatten() * nc + pred.flatten()), minlength=nc * nc).reshape(nc, nc).double()
    tp = cm.diag(); fp = cm.sum(0) - tp; fn = cm.sum(1) - tp
    iou = (100 * tp / (tp + fp + fn).clamp(min=1)).tolist(); dice = (100 * 2 * tp / (2 * tp + fp + fn).clamp(min=1)).tolist()
    return {"iou_per_class": iou, "dice_per_class": dice, "miou_defects": float(np.mean(iou[1:])),
            "miou_all": float(np.mean(iou)), "mdice_defects": float(np.mean(dice[1:]))}


# ------------------------------------------------------------------------------------------------
# Training (AdamW 1e-3 / 1e-4, cosine, batch 16 - as in the paper; epochs configurable; best-val selection)
# ------------------------------------------------------------------------------------------------
def set_seed(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s); torch.cuda.manual_seed_all(s)


def train_run(run_id, model_name, data, epochs, seed, nc=1, loss_cfg=None, flips=False, test_sets=None, aug=False, accum=1, compact=False):
    """data: dict(train=..., val=...). test_sets: {name: split}. Saves runs/<run_id>.json (skips if present)."""
    out_p = os.path.join(RUNS, run_id + ".json")
    if os.path.exists(out_p):
        return json.load(open(out_p))
    set_seed(seed)
    model = MODELS[model_name](nc).to(DEV)
    use_b = model_name in HAS_BOUNDARY and (loss_cfg or {}).get("lambda_boundary", 0.4) > 0
    if nc == 1:
        lc = {"lambda_dice": 1.0, "lambda_focal": 0.5, "lambda_boundary": 0.4}; lc.update(loss_cfg or {})
        crit = CompositeLoss(**lc).to(DEV)
    else:
        crit = MultiClassComposite(nc, (loss_cfg or {}).get("lambda_boundary", 0.4)).to(DEV)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)
    # whole training split kept on the GPU (same batches and order as before, no per-batch host->device copies)
    X, B = data["train"]["image"].to(DEV), data["train"]["boundary"].to(DEV)
    Ym = data["train"]["mask"]
    Y = Ym.to(torch.uint8).to(DEV) if Ym.dtype == torch.long else Ym.to(DEV)   # NEU labels 0..3 stored compactly
    if compact:     # large binary sets (images k/255, boundary and mask 0/1) kept as uint8 on the GPU; exact round trip
        X = (X * 255).round().to(torch.uint8); B = (B * 255).round().to(torch.uint8); Y = Y.round().to(torch.uint8)
        torch.cuda.empty_cache()
    g = torch.Generator().manual_seed(seed)
    g_aug = torch.Generator(device=DEV).manual_seed(seed + 77) if aug else None
    hist = {"train_loss": [], "val_iou": [], "epoch_s": []}
    best, best_state = -1.0, None
    for ep in range(epochs):
        t0 = time.time(); model.train(); tl = 0.0; nb = 0
        perm = torch.randperm(len(X), generator=g)
        for i in range(0, len(X), 16):
            idx = perm[i:i + 16].to(DEV)
            x = X[idx]; b = B[idx]; y = Y[idx]
            if compact:
                x = x.float() / 255.0; b = b.float() / 255.0; y = y.float()
            if Ym.dtype == torch.long:
                y = y.long()
            if flips:
                if torch.rand(1, generator=g).item() < 0.5:
                    x, y, b = x.flip(-1), y.flip(-1), b.flip(-1)
                if torch.rand(1, generator=g).item() < 0.5:
                    x, y, b = x.flip(-2), y.flip(-2), b.flip(-2)
            if aug:
                x = degrade_aug(x, g_aug)
            opt.zero_grad(set_to_none=True)
            if accum == 1:
                with torch.autocast("cuda", dtype=torch.bfloat16):      # bf16 mixed precision; loss in FP32
                    pm, pb = model(x)
                pm = pm.float(); pb = pb.float() if pb is not None else None
                loss = crit(pm, y, pb, b) if use_b else crit(pm, y)
                loss.backward(); opt.step(); tl += loss.item(); nb += 1
            else:       # memory-limited models only: the batch of 16 in `accum` chunks, gradients summed (mean loss)
                lsum = 0.0
                for xc, yc, bc in zip(x.chunk(accum), y.chunk(accum), b.chunk(accum)):
                    with torch.autocast("cuda", dtype=torch.bfloat16):
                        pm, pb = model(xc)
                    pm = pm.float(); pb = pb.float() if pb is not None else None
                    loss = (crit(pm, yc, pb, bc) if use_b else crit(pm, yc)) * (len(xc) / len(x))
                    loss.backward(); lsum += loss.item()
                opt.step(); tl += lsum; nb += 1
        sch.step()
        vp = predict(model, data["val"]["image"], nc)
        v = binary_metrics(vp, data["val"]["mask"])["iou"] if nc == 1 else multiclass_metrics(vp, data["val"]["mask"], nc)["miou_defects"]
        hist["train_loss"].append(tl / nb); hist["val_iou"].append(v); hist["epoch_s"].append(time.time() - t0)
        if os.environ.get("EPOCH_LOG"):         # progress only; does not affect training
            open(os.environ["EPOCH_LOG"], "a").write(f"{time.strftime('%H:%M:%S')} {run_id} ep {ep + 1}/{epochs} loss {tl / nb:.4f} val {v:.2f} ({time.time() - t0:.0f}s)" + "\n")
        if v > best:
            best = v; best_state = {k: t.detach().clone() for k, t in model.state_dict().items()}
    model.load_state_dict(best_state)
    res = {"run_id": run_id, "model": model_name, "seed": seed, "epochs": epochs, "loss_cfg": loss_cfg, "aug": aug, "accum": accum,
           "best_val": best, "best_epoch": int(np.argmax(hist["val_iou"])) + 1, "history": hist, "test": {}}
    for name, split in (test_sets or {}).items():
        tp = predict(model, split["image"], nc)
        res["test"][name] = binary_metrics(tp, split["mask"]) if nc == 1 else multiclass_metrics(tp, split["mask"], nc)
        if nc == 1 and name == "normal" and "cls" in split:
            per = {}
            for c in sorted(set(split["cls"])):
                ii = [i for i, k in enumerate(split["cls"]) if k == c]
                per[c] = binary_metrics(tp[ii], split["mask"][ii])
            res["test"]["normal_per_class"] = per
    torch.save(best_state, os.path.join(RUNS, run_id + ".pth"))
    json.dump(res, open(out_p, "w"), indent=1)
    return res

# MSBA-Net v2 candidates (2026-11-18; context module on the bottleneck; see msba_v2.py)
from msba_v2 import MSBANetV2a, MSBANetV2b
MODELS.update({"MSBANetV2a": lambda nc: MSBANetV2a(1, nc, 32), "MSBANetV2b": lambda nc: MSBANetV2b(1, nc, 32)})
HAS_BOUNDARY |= {"MSBANetV2a", "MSBANetV2b"}
from msba_v2 import MSBANetV2c, MSBANetV2d
MODELS.update({"MSBANetV2c": lambda nc: MSBANetV2c(1, nc, 32), "MSBANetV2d": lambda nc: MSBANetV2d(1, nc, 32)})
HAS_BOUNDARY |= {"MSBANetV2c", "MSBANetV2d"}
