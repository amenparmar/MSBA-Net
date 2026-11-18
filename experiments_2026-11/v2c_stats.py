"""Statistics for the paper with MSBA-Net v2c as the proposed model ("MSBA-Net" with Context Aggregation).
Reads runs/*.json only; writes v2c_stats.json. Holm correction over the six baselines per condition (synthetic, NEU-Seg)
and over the four augmented baselines, exactly as in final_tests.py; efficiency (params, GMACs) on CPU."""
import os, sys, json, glob
sys.dont_write_bytecode = True
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
R = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(os.path.join(HERE, "runs", "*.json"))}
S5, S3 = [42, 100, 2026, 7, 123], [42, 100, 2026]
COND = ["normal", "tiny_defects", "low_contrast", "blur", "noise"]
BASE = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "HRNetW18", "SegFormerB1"]
V = "MSBANetV2c"
ms = lambda x: {"mean": float(np.mean(x)), "sd": float(np.std(x, ddof=1))}


def paired(a, b):
    return {"diff": float(np.mean(np.array(a) - np.array(b))), "p": float(stats.ttest_rel(a, b).pvalue)}


def holm(d):
    items = sorted(d.items(), key=lambda kv: kv[1]["p"]); k = len(items); run = 0.0
    for j, (m, v) in enumerate(items):
        run = max(run, min(1.0, (k - j) * v["p"])); v["p_holm"] = run
    return d


syn = lambda m, c, k="iou", pre="syn": [R[f"{pre}_{m}_s{s}"]["test"][c][k] for s in S5]
neu = lambda m, k="miou_defects": [R[f"neu_{m}_s{s}"]["test"]["test"][k] for s in S3]
out = {"syn_full": {c: {k: ms(syn(V, c, k)) for k in ("iou", "dice")} for c in COND},
       "per_class": {}, "syn_sig": {}, "syn_vs_v1": {}, "neu": {}, "neu_sig": None, "neu_vs_v1": None}
pcs = [R[f"syn_{V}_s{s}"]["test"]["normal_per_class"] for s in S5]
out["per_class"] = {c: ms([pc[c]["iou"] for pc in pcs]) for c in pcs[0]}
for c in COND:
    out["syn_sig"][c] = holm({b: paired(syn(V, c), syn(b, c)) for b in BASE})
    out["syn_vs_v1"][c] = paired(syn(V, c), syn("MSBANet", c))
rs = [R[f"neu_{V}_s{s}"]["test"]["test"] for s in S3]
out["neu"] = {"miou": ms([r["miou_defects"] for r in rs]), "mdice": ms([r["mdice_defects"] for r in rs]),
              "iou_cls": [ms([r["iou_per_class"][k] for r in rs]) for k in range(4)],
              "best_epoch": [R[f"neu_{V}_s{s}"]["best_epoch"] for s in S3]}
out["neu_sig"] = holm({b: paired(neu(V), neu(b)) for b in BASE})
out["neu_vs_v1"] = paired(neu(V), neu("MSBANet"))
out["neu_vs_v1"]["inclusion"] = paired([r["iou_per_class"][1] for r in rs], [R[f"neu_MSBANet_s{s}"]["test"]["test"]["iou_per_class"][1] for s in S3])
# ablation step Arch-4 (MSBA-Net without CA) -> Arch-5 (with CA)
out["arch5"] = {c: ms(syn(V, c)) for c in ("normal", "tiny_defects", "low_contrast")}
out["arch5_vs_arch4"] = {c: paired(syn(V, c), syn("MSBANet", c)) for c in ("normal", "tiny_defects", "low_contrast")}
out["arch5_vs_arch1"] = {c: paired(syn(V, c), syn("UNet", c)) for c in ("normal", "tiny_defects", "low_contrast")}
# augmentation (only if all five v2c runs exist)
if all(f"syn_aug_{V}_s{s}" in R for s in S5):
    out["aug"] = {c: ms(syn(V, c, pre="syn_aug")) for c in COND}
    out["aug_sig"] = {c: holm({b: paired(syn(V, c, pre="syn_aug"), syn(b, c, pre="syn_aug")) for b in BASE[:4]}) for c in COND}
    out["aug_vs_plain"] = {c: paired(syn(V, c, pre="syn_aug"), syn(V, c)) for c in COND}
    out["aug_vs_v1"] = {c: paired(syn(V, c, pre="syn_aug"), syn("MSBANet", c, pre="syn_aug")) for c in COND}
# efficiency: parameters and GMACs (CPU, same counting as final_tests.py); latency measured separately on an idle GPU
if "--eff" in sys.argv:
    import torch
    from torch.utils.flop_counter import FlopCounterMode
    import common as C
    net = C.MODELS[V](1).eval(); x = torch.randn(1, 1, 256, 256)
    with FlopCounterMode(display=False) as fc, torch.no_grad():
        net(x)
    out["efficiency"] = {"params_M": sum(p.numel() for p in net.parameters()) / 1e6, "gmacs": fc.get_total_flops() / 2e9}
elif os.path.exists(os.path.join(HERE, "v2c_stats.json")):
    old = json.load(open(os.path.join(HERE, "v2c_stats.json")))
    for k in ("efficiency", "latency", "latency_meta"):
        if k in old:
            out[k] = old[k]
json.dump(out, open(os.path.join(HERE, "v2c_stats.json"), "w"), indent=1)
f = lambda d: f"{d['mean']:.2f}±{d['sd']:.2f}"
print("SYN", {c: f(out["syn_full"][c]["iou"]) for c in COND})
for c in COND:
    print("SIG", c, {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["syn_sig"][c].items()}, "| vs v1", round(out["syn_vs_v1"][c]["diff"], 2), round(out["syn_vs_v1"][c]["p"], 3))
print("NEU", f(out["neu"]["miou"]), f(out["neu"]["mdice"]), [f(x) for x in out["neu"]["iou_cls"]], out["neu"]["best_epoch"])
print("NEU SIG", {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["neu_sig"].items()}, "| vs v1", out["neu_vs_v1"])
print("PERCLASS", {c: round(v["mean"], 2) for c, v in out["per_class"].items()})
print("ARCH5", {c: f(v) for c, v in out["arch5"].items()}, {c: (round(v["diff"], 2), round(v["p"], 3)) for c, v in out["arch5_vs_arch4"].items()})
print("ARCH5 vs U-Net", {c: (round(v["diff"], 2), round(v["p"], 3)) for c, v in out["arch5_vs_arch1"].items()})
if "aug" in out:
    print("AUG", {c: f(v) for c, v in out["aug"].items()})
    for c in COND:
        print("AUG SIG", c, {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["aug_sig"][c].items()})
if "efficiency" in out:
    print("EFF", out["efficiency"])
