"""Final paper statistics after round 2: MSBA-Net vs all six baselines (Holm over six per condition), synthetic and
NEU-Seg; augmentation comparisons (Holm over four per condition); efficiency of all seven models measured in one
session (FP32, batch 1, 50 warm-up + 300 timed runs, median). Writes final_tests.json."""
import os, sys, json, glob, time
sys.dont_write_bytecode = True
import numpy as np, torch
from scipy import stats
from torch.utils.flop_counter import FlopCounterMode
import common as C
sys.stdout.reconfigure(encoding="utf-8")
R = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(os.path.join(C.RUNS, "*.json"))}
BASE = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "HRNetW18", "SegFormerB1"]
COND = C.CONDITIONS
S5, S3 = C.SEEDS, C.SEEDS[:3]


def holm(d):
    items = sorted(d.items(), key=lambda kv: kv[1]["p"]); k = len(items); run = 0.0
    for j, (m, v) in enumerate(items):
        run = max(run, min(1.0, (k - j) * v["p"])); v["p_holm"] = run
    return d


def paired(a, b):
    return {"diff": float(np.mean(np.array(a) - np.array(b))), "p": float(stats.ttest_rel(a, b).pvalue)}


syn = lambda pre, seeds, c: [R[f"{pre}_s{s}"]["test"][c]["iou"] for s in seeds]
neu = lambda m: [R[f"neu_{m}_s{s}"]["test"]["test"]["miou_defects"] for s in S3]
out = {"syn": {c: holm({b: paired(syn("syn_MSBANet", S5, c), syn(f"syn_{b}", S5, c)) for b in BASE}) for c in COND},
       "neu": holm({b: paired(neu("MSBANet"), neu(b)) for b in BASE}),
       "aug": {c: holm({b: paired(syn("syn_aug_MSBANet", S5, c), syn(f"syn_aug_{b}", S5, c)) for b in BASE[:4]}) for c in COND},
       "aug_vs_plain": {m: {c: paired(syn(f"syn_aug_{m}", S5, c), syn(f"syn_{m}", S5, c)) for c in COND}
                        for m in BASE[:4] + ["MSBANet"]}}
eff = {}
for m in BASE + ["MSBANet"]:
    net = C.MODELS[m](1).eval(); x = torch.randn(1, 1, 256, 256)
    with FlopCounterMode(display=False) as fc, torch.no_grad():
        net(x)
    net = net.to(C.DEV); xg = x.to(C.DEV); ts = []
    with torch.no_grad():
        for _ in range(50): net(xg)
        for _ in range(300):
            torch.cuda.synchronize(); t = time.perf_counter(); net(xg); torch.cuda.synchronize()
            ts.append((time.perf_counter() - t) * 1000)
    eff[m] = {"params_M": sum(p.numel() for p in net.parameters()) / 1e6, "gmacs": fc.get_total_flops() / 2e9,
              "latency_ms": float(np.median(ts))}
    del net; torch.cuda.empty_cache()
out["efficiency"] = eff
json.dump(out, open(os.path.join(C.HERE, "final_tests.json"), "w"), indent=1)
for c in COND:
    print("SYN", c, {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["syn"][c].items()})
print("NEU", {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["neu"].items()})
for c in COND:
    print("AUG", c, {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["aug"][c].items()})
for m, d in out["aug_vs_plain"].items():
    print("AUG-PLAIN", m, {c: f"{v['diff']:+.2f} ({v['p']:.3f})" for c, v in d.items()})
for m, e in eff.items():
    print("EFF", m, f"{e['params_M']:.2f}M {e['gmacs']:.2f} GMACs {e['latency_ms']:.2f} ms {1000 / e['latency_ms']:.0f}/s")
