"""Extra statistics for the paper (reads runs/*.json only): ablation/loss/lambda paired tests, full metric means,
synthetic per-class means for MSBA-Net and U-Net, NEU per-class. Writes extra_stats.json and prints a summary."""
import json, os, glob, sys
import numpy as np
from scipy import stats
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
R = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(os.path.join(HERE, "runs", "*.json"))}
SEEDS = [42, 100, 2026, 7, 123]


def vals(prefix, seeds, cond, metric="iou"):
    return [R[f"{prefix}_s{s}"]["test"][cond][metric] for s in seeds]


def paired(a, b):
    d = np.array(a) - np.array(b)
    t, p = stats.ttest_rel(a, b)
    return {"diff": float(d.mean()), "p": float(p), "n": len(d)}


def ms(x):
    return {"mean": float(np.mean(x)), "sd": float(np.std(x, ddof=1))}


out = {}
# full metric table (synthetic, all 5 conditions) for the 5 main models
main = {"UNet": "syn_UNet", "UNetPlusPlus": "syn_UNetPlusPlus", "AttUNet": "syn_AttUNet",
        "DeepLabV3Plus": "syn_DeepLabV3Plus", "MSBANet": "syn_MSBANet"}
out["syn_full"] = {m: {c: {k: ms(vals(p, SEEDS, c, k)) for k in ("iou", "dice", "precision", "recall", "iou_per_image")}
                       for c in ("normal", "tiny_defects", "low_contrast", "blur", "noise")} for m, p in main.items()}
# architecture ablation steps (5 seeds)
arch = {"A1": "syn_UNet", "A2": "syn_Arch2_MSFP", "A3": "syn_Arch3_MSFP_BAS", "A4": "syn_MSBANet"}
out["arch"] = {}
for c in ("normal", "tiny_defects", "low_contrast"):
    v = {k: vals(p, SEEDS, c) for k, p in arch.items()}
    out["arch"][c] = {"means": {k: ms(x) for k, x in v.items()},
                      "A2-A1": paired(v["A2"], v["A1"]), "A3-A2": paired(v["A3"], v["A2"]),
                      "A4-A3": paired(v["A4"], v["A3"]), "A4-A1": paired(v["A4"], v["A1"])}
    out["arch"][c]["dice_means"] = {k: ms(vals(p, SEEDS, c, "dice")) for k, p in arch.items()}
# loss ablation (3 seeds) ; Loss-4 = MSBANet default
S3 = SEEDS[:3]
loss = {"L1": "syn_MSBANet_Loss1_BCE", "L2": "syn_MSBANet_Loss2_BCE_Dice", "L3": "syn_MSBANet_Loss3_BCE_Dice_Focal",
        "L4": "syn_MSBANet"}
out["loss"] = {}
for c in ("normal", "tiny_defects", "low_contrast"):
    v = {k: vals(p, S3, c) for k, p in loss.items()}
    out["loss"][c] = {"means": {k: ms(x) for k, x in v.items()},
                      "dice_means": {k: ms(vals(p, S3, c, "dice")) for k, p in loss.items()},
                      "L2-L1": paired(v["L2"], v["L1"]), "L3-L2": paired(v["L3"], v["L2"]),
                      "L4-L3": paired(v["L4"], v["L3"]), "L4-L2": paired(v["L4"], v["L2"])}
lam = {"0.2": "syn_MSBANet_Lb0.2", "0.4": "syn_MSBANet", "0.8": "syn_MSBANet_Lb0.8"}
out["lambda"] = {}
for c in ("normal", "tiny_defects", "low_contrast"):
    v = {k: vals(p, S3, c) for k, p in lam.items()}
    out["lambda"][c] = {"means": {k: ms(x) for k, x in v.items()},
                        "0.2-0.4": paired(v["0.2"], v["0.4"]), "0.8-0.4": paired(v["0.8"], v["0.4"])}
# synthetic per-class (nominal test, pooled per class, mean over 5 seeds)
out["per_class"] = {}
for m in ("MSBANet", "UNet", "UNetPlusPlus", "AttUNet"):
    pcs = [R[f"syn_{m}_s{s}"]["test"]["normal_per_class"] for s in SEEDS]
    out["per_class"][m] = {c: {k: ms([pc[c][k] for pc in pcs]) for k in ("iou", "dice", "precision", "recall")}
                           for c in pcs[0]}
# NEU
out["neu"] = {}
for m in main:
    rs = [R[f"neu_{m}_s{s}"]["test"]["test"] for s in S3]
    out["neu"][m] = {"miou": ms([r["miou_defects"] for r in rs]), "mdice": ms([r["mdice_defects"] for r in rs]),
                     "iou_cls": [ms([r["iou_per_class"][k] for r in rs]) for k in range(4)],
                     "best_epoch": [R[f"neu_{m}_s{s}"]["best_epoch"] for s in S3]}
# ---------------- round 2: augmentation and further baselines (only if all runs are present) ----------------
COND = ("normal", "tiny_defects", "low_contrast", "blur", "noise")
if all(f"syn_aug_{m}_s{s}" in R for m in main for s in SEEDS):
    out["aug"] = {m: {c: ms(vals(f"syn_aug_{m}", SEEDS, c)) for c in COND} for m in main}
    out["aug_vs_plain"] = {m: {c: paired(vals(f"syn_aug_{m}", SEEDS, c), vals(f"syn_{m}", SEEDS, c)) for c in COND} for m in main}
    raw = {}
    for c in COND:
        b = {m: vals(f"syn_aug_{m}", SEEDS, c) for m in main if m != "MSBANet"}
        tests = {m: paired(vals("syn_aug_MSBANet", SEEDS, c), v) for m, v in b.items()}
        ps = sorted(tests.items(), key=lambda kv: kv[1]["p"])
        k = len(ps); run = 0.0
        for j, (m, d) in enumerate(ps):                  # Holm step-down, monotone
            run = max(run, min(1.0, (k - j) * d["p"])); d["p_holm"] = run
        raw[c] = tests
    out["aug_msba_vs"] = raw
NEW = ["HRNetW18", "SegFormerB1"]
if all(f"syn_{m}_s{s}" in R for m in NEW for s in SEEDS):
    for m in NEW:
        out["syn_full"][m] = {c: {k: ms(vals(f"syn_{m}", SEEDS, c, k)) for k in ("iou", "dice", "precision", "recall", "iou_per_image")} for c in COND}
        pcs = [R[f"syn_{m}_s{s}"]["test"]["normal_per_class"] for s in SEEDS]
        out["per_class"][m] = {c: {k: ms([pc[c][k] for pc in pcs]) for k in ("iou", "dice", "precision", "recall")} for c in pcs[0]}
    out["msba_vs_new_syn"] = {m: {c: paired(vals("syn_MSBANet", SEEDS, c), vals(f"syn_{m}", SEEDS, c)) for c in COND} for m in NEW}
if all(f"neu_{m}_s{s}" in R for m in NEW for s in S3):
    for m in NEW:
        rs = [R[f"neu_{m}_s{s}"]["test"]["test"] for s in S3]
        out["neu"][m] = {"miou": ms([r["miou_defects"] for r in rs]), "mdice": ms([r["mdice_defects"] for r in rs]),
                         "iou_cls": [ms([r["iou_per_class"][k] for r in rs]) for k in range(4)],
                         "best_epoch": [R[f"neu_{m}_s{s}"]["best_epoch"] for s in S3]}
    msba = [R[f"neu_MSBANet_s{s}"]["test"]["test"]["miou_defects"] for s in S3]
    out["msba_vs_new_neu"] = {m: paired(msba, [R[f"neu_{m}_s{s}"]["test"]["test"]["miou_defects"] for s in S3]) for m in NEW}
json.dump(out, open(os.path.join(HERE, "extra_stats.json"), "w"), indent=1)
f = lambda d: f"{d['mean']:.2f}±{d['sd']:.2f}"
if "aug" in out:
    for m, d in out["aug"].items():
        print("AUG", m, {c: f(v) for c, v in d.items()})
    for m, d in out["aug_vs_plain"].items():
        print("AUG-PLAIN", m, {c: (round(v["diff"], 2), round(v["p"], 3)) for c, v in d.items()})
    for c, d in out["aug_msba_vs"].items():
        print("AUG MSBA vs", c, {m: (round(v["diff"], 2), round(v["p_holm"], 3)) for m, v in d.items()})
for key in ("msba_vs_new_syn",):
    if key in out:
        for m, d in out[key].items():
            print("MSBA vs", m, {c: (round(v["diff"], 2), round(v["p"], 3)) for c, v in d.items()})
if "msba_vs_new_neu" in out:
    print("NEU MSBA vs new", {m: (round(v["diff"], 2), round(v["p"], 3)) for m, v in out["msba_vs_new_neu"].items()})

f = lambda d: f"{d['mean']:.2f}±{d['sd']:.2f}"
for c in ("normal", "tiny_defects", "low_contrast"):
    a = out["arch"][c]
    print("ARCH", c, {k: f(v) for k, v in a["means"].items()},
          {k: (round(a[k]["diff"], 2), round(a[k]["p"], 3)) for k in ("A2-A1", "A3-A2", "A4-A3", "A4-A1")})
    print("  dice", {k: f(v) for k, v in a["dice_means"].items()})
for c in ("normal", "tiny_defects", "low_contrast"):
    a = out["loss"][c]
    print("LOSS", c, {k: f(v) for k, v in a["means"].items()},
          {k: (round(a[k]["diff"], 2), round(a[k]["p"], 3)) for k in ("L2-L1", "L3-L2", "L4-L3", "L4-L2")})
    print("  dice", {k: f(v) for k, v in a["dice_means"].items()})
for c in ("normal", "tiny_defects", "low_contrast"):
    a = out["lambda"][c]
    print("LAMBDA", c, {k: f(v) for k, v in a["means"].items()},
          {k: (round(a[k]["diff"], 2), round(a[k]["p"], 3)) for k in ("0.2-0.4", "0.8-0.4")})
for m, d in out["syn_full"].items():
    for c in ("normal", "tiny_defects"):
        print("FULL", m, c, {k: f(v) for k, v in d[c].items()})
for m, d in out["per_class"].items():
    print("PERCLASS", m, {c: f(v["iou"]) for c, v in d.items()})
for m, d in out["neu"].items():
    print("NEU", m, f(d["miou"]), f(d["mdice"]), [f(x) for x in d["iou_cls"]], d["best_epoch"])
