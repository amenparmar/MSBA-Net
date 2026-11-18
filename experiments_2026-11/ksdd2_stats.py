"""KolektorSDD2 statistics for the paper (seeds 42, 100, 2026; author's short plan 2026-11-18). Reads runs/ksdd2_*.json
and ksdd2_postproc.json; paired t-tests of MSBA-Net (v2c) against each baseline, Holm-corrected over the six baselines
(as for NEU-Seg). Writes ksdd2_stats.json."""
import os, sys, json
sys.dont_write_bytecode = True
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
S3 = [42, 100, 2026]
MODELS = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "HRNetW18", "SegFormerB1", "MSBANet", "MSBANetV2c"]
BASE = MODELS[:6]
V = "MSBANetV2c"
run = lambda m, s: json.load(open(os.path.join(HERE, "runs", f"ksdd2_{m}_s{s}.json")))
PP = json.load(open(os.path.join(HERE, "ksdd2_postproc.json")))
ms = lambda x: {"mean": float(np.mean(x)), "sd": float(np.std(x, ddof=1)), "values": [float(v) for v in x]}


def metrics(m):
    out = {}
    for key, get in (("iou", lambda t: t["iou"]), ("dice", lambda t: t["dice"]),
                     ("small_recall", lambda t: 100 * t["components"]["small_le1024_found"] / t["components"]["small_le1024_total"]),
                     ("img_recall", lambda t: t["image_detection_recall"]), ("false_alarm", lambda t: t["image_false_alarm_rate"]),
                     ("false_blobs", lambda t: t["false_components"])):
        out[key] = ms([get(run(m, s)["test"]["test"]) for s in S3])
    out["iou_filtered"] = ms([PP[f"ksdd2_{m}_s{s}"]["test_filtered"]["iou"] for s in S3])
    out["false_blobs_filtered"] = ms([PP[f"ksdd2_{m}_s{s}"]["test_filtered"]["false_components"] for s in S3])
    out["best_epoch"] = [run(m, s)["best_epoch"] for s in S3]
    return out


def holm(d):
    items = sorted(d.items(), key=lambda kv: kv[1]["p"]); k = len(items); r = 0.0
    for j, (b, v) in enumerate(items):
        r = max(r, min(1.0, (k - j) * v["p"])); v["p_holm"] = r
    return d


paired = lambda a, b: {"diff": float(np.mean(np.array(a) - np.array(b))), "p": float(stats.ttest_rel(a, b).pvalue)}
R = {m: metrics(m) for m in MODELS}
out = {"models": R, "seeds": S3,
       "sig_iou": holm({b: paired(R[V]["iou"]["values"], R[b]["iou"]["values"]) for b in BASE}),
       "sig_small": holm({b: paired(R[V]["small_recall"]["values"], R[b]["small_recall"]["values"]) for b in BASE}),
       "vs_v1_iou": paired(R[V]["iou"]["values"], R["MSBANet"]["iou"]["values"]),
       "n_small": run(V, 42)["test"]["test"]["components"]["small_le1024_total"]}
rr = os.path.join(HERE, "runs", "ksdd2rerun_DeepLabV3Plus_s100.json")
if os.path.exists(rr):
    a, b = json.load(open(rr))["test"]["test"], run("DeepLabV3Plus", 100)["test"]["test"]
    out["rerun_check"] = {"original_iou": b["iou"], "rerun_iou": a["iou"]}
json.dump(out, open(os.path.join(HERE, "ksdd2_stats.json"), "w"), indent=1)
f = lambda d: f"{d['mean']:.2f}±{d['sd']:.2f}"
for m in MODELS:
    r = R[m]
    print(f"{m:14s} IoU {f(r['iou'])} Dice {f(r['dice'])} small {f(r['small_recall'])} imgrec {f(r['img_recall'])} FA {f(r['false_alarm'])} | filt IoU {f(r['iou_filtered'])}")
print("SIG IoU", {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["sig_iou"].items()})
print("SIG small", {b: f"{v['diff']:+.2f} ({v['p_holm']:.3f})" for b, v in out["sig_small"].items()})
print("vs v1", out["vs_v1_iou"], "| rerun", out.get("rerun_check"))
