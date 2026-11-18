"""Aggregates runs/*.json -> results_summary.json, RESULTS.md, LaTeX snippets (tables/*.tex), figures (fig_*.png).
Statistics: mean +- sample std over seeds; paired two-sided t-test per seed (same seed = same data and init seed),
Holm-Bonferroni correction across the baseline comparisons of each condition."""
import os, sys, json, glob, time
sys.dont_write_bytecode = True
import numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, "runs")
OUTT = os.path.join(HERE, "tables"); os.makedirs(OUTT, exist_ok=True)
R = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(RUNS, "*.json"))}
SEEDS = [42, 100, 2026, 7, 123]
MAIN = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "MSBANet"]
NAMES = {"UNet": "U-Net", "UNetPlusPlus": "U-Net++", "AttUNet": "Attention U-Net", "DeepLabV3Plus": "DeepLabv3+", "MSBANet": "MSBA-Net",
         "Arch2_MSFP": "U-Net + MSFP", "Arch3_MSFP_BAS": "U-Net + MSFP + BAS"}
CONDS = ["normal", "tiny_defects", "low_contrast", "blur", "noise"]
CN = {"normal": "Nominal", "tiny_defects": "Tiny defects", "low_contrast": "Low contrast", "blur": "Gaussian blur", "noise": "Sensor noise"}


def vals(prefix, getter, seeds=SEEDS):
    out = {}
    for s in seeds:
        r = R.get(f"{prefix}_s{s}")
        if r: out[s] = getter(r)
    return out


def ms(d):
    v = np.array(list(d.values()), float)
    return (v.mean(), v.std(ddof=1) if len(v) > 1 else float("nan"), len(v))


def paired(a, b):
    ks = sorted(set(a) & set(b))
    if len(ks) < 3: return float("nan"), float("nan"), len(ks)
    x = np.array([a[k] for k in ks]); y = np.array([b[k] for k in ks])
    t = stats.ttest_rel(x, y)
    return float((x - y).mean()), float(t.pvalue), len(ks)


def holm(ps):
    idx = sorted(range(len(ps)), key=lambda i: ps[i] if ps[i] == ps[i] else 9)
    adj = [float("nan")] * len(ps); run = 0
    m = sum(1 for p in ps if p == p)
    for r, i in enumerate(idx):
        if ps[i] != ps[i]: continue
        run = max(run, min(1.0, (m - r) * ps[i])); adj[i] = run
    return adj


S = {"synthetic": {}, "neu": {}, "ablation": {}, "loss": {}, "lambda": {}, "stats": {}}
# ---- synthetic main comparison ----
for m in MAIN:
    for c in CONDS:
        for met in ("iou", "dice", "precision", "recall", "iou_per_image"):
            d = vals(f"syn_{m}", lambda r: r["test"][c][met])
            if d: S["synthetic"].setdefault(m, {}).setdefault(c, {})[met] = {"mean": ms(d)[0], "std": ms(d)[1], "n": ms(d)[2], "per_seed": d}
for c in CONDS:
    a = vals("syn_MSBANet", lambda r: r["test"][c]["iou"])
    rows = [(b, *paired(a, vals(f"syn_{b}", lambda r: r["test"][c]["iou"]))) for b in MAIN if b != "MSBANet"]
    adj = holm([p for _, _, p, _ in rows])
    S["stats"][f"synthetic_{c}"] = [{"vs": b, "mean_diff_pp": d, "p": p, "p_holm": q, "n": n} for (b, d, p, n), q in zip(rows, adj)]
# ---- NEU-Seg ----
for m in MAIN:
    d = vals(f"neu_{m}", lambda r: r["test"]["test"]["miou_defects"], SEEDS[:3])
    if d:
        pc = vals(f"neu_{m}", lambda r: r["test"]["test"]["iou_per_class"], SEEDS[:3])
        dd = vals(f"neu_{m}", lambda r: r["test"]["test"]["mdice_defects"], SEEDS[:3])
        S["neu"][m] = {"miou_defects": {"mean": ms(d)[0], "std": ms(d)[1], "n": ms(d)[2], "per_seed": d},
                       "mdice_defects": {"mean": ms(dd)[0], "std": ms(dd)[1]},
                       "iou_per_class_mean": np.mean(np.array(list(pc.values())), 0).tolist()}
a = vals("neu_MSBANet", lambda r: r["test"]["test"]["miou_defects"], SEEDS[:3])
rows = [(b, *paired(a, vals(f"neu_{b}", lambda r: r["test"]["test"]["miou_defects"], SEEDS[:3]))) for b in MAIN if b != "MSBANet"]
adj = holm([p for _, _, p, _ in rows])
S["stats"]["neu"] = [{"vs": b, "mean_diff_pp": d, "p": p, "p_holm": q, "n": n} for (b, d, p, n), q in zip(rows, adj)]
# ---- ablations ----
for key, pref in (("Arch-1 U-Net", "syn_UNet"), ("Arch-2 +MSFP", "syn_Arch2_MSFP"), ("Arch-3 +MSFP+BAS", "syn_Arch3_MSFP_BAS"), ("Arch-4 MSBA-Net", "syn_MSBANet")):
    S["ablation"][key] = {c: {"mean": ms(d)[0], "std": ms(d)[1], "n": ms(d)[2], "per_seed": d}
                          for c in ("normal", "tiny_defects") if (d := vals(pref, lambda r: r["test"][c]["iou"]))}
for key, pref in (("Loss-1 BCE", "syn_MSBANet_Loss1_BCE"), ("Loss-2 BCE+Dice", "syn_MSBANet_Loss2_BCE_Dice"),
                  ("Loss-3 BCE+Dice+Focal", "syn_MSBANet_Loss3_BCE_Dice_Focal"), ("Loss-4 full", "syn_MSBANet")):
    S["loss"][key] = {c: {"mean": ms(d)[0], "std": ms(d)[1], "n": ms(d)[2], "per_seed": d}
                      for c in ("normal", "tiny_defects") if (d := vals(pref, lambda r: r["test"][c]["iou"], SEEDS[:3]))}
for key, pref in (("0.2", "syn_MSBANet_Lb0.2"), ("0.4", "syn_MSBANet"), ("0.8", "syn_MSBANet_Lb0.8")):
    S["lambda"][key] = {c: {"mean": ms(d)[0], "std": ms(d)[1], "n": ms(d)[2], "per_seed": d}
                        for c in ("normal", "tiny_defects", "low_contrast") if (d := vals(pref, lambda r: r["test"][c]["iou"], SEEDS[:3]))}
# ---- training budget ----
S["best_epochs"] = {m: vals(f"syn_{m}", lambda r: r["best_epoch"]) for m in MAIN}

# ---- efficiency (params, GMACs via torch FlopCounter, latency FP32 bs1) ----
import torch
from torch.utils.flop_counter import FlopCounterMode
import common as C
eff = {}
for m in MAIN:
    net = C.MODELS[m](1).eval(); x = torch.randn(1, 1, 256, 256)
    with FlopCounterMode(display=False) as fc, torch.no_grad():
        net(x)
    net = net.to(C.DEV); xg = x.to(C.DEV); ts = []
    with torch.no_grad():
        for _ in range(50): net(xg)
        for _ in range(300):
            torch.cuda.synchronize(); t = time.perf_counter(); net(xg); torch.cuda.synchronize(); ts.append((time.perf_counter() - t) * 1000)
    eff[m] = {"params_M": sum(p.numel() for p in net.parameters()) / 1e6, "gmacs": fc.get_total_flops() / 2e9, "latency_ms": float(np.median(ts))}
S["efficiency"] = eff
json.dump(S, open(os.path.join(HERE, "results_summary.json"), "w"), indent=1, default=float)

# ---- figure: validation IoU per epoch (mean over seeds) ----
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=300)
styles = {"UNet": ("--", "s"), "UNetPlusPlus": ("-.", "^"), "AttUNet": (":", "D"), "DeepLabV3Plus": ((0, (5, 1)), "v"), "MSBANet": ("-", "o")}
for m in MAIN:
    H = [R[f"syn_{m}_s{s}"]["history"]["val_iou"] for s in SEEDS if f"syn_{m}_s{s}" in R]
    if not H: continue
    H = np.array(H); ep = np.arange(1, H.shape[1] + 1); mu = H.mean(0); sd = H.std(0)
    ax.plot(ep, mu, color="black", linestyle=styles[m][0], marker=styles[m][1], markersize=3, markevery=4, linewidth=1.3, label=NAMES[m])
    ax.fill_between(ep, mu - sd, mu + sd, color="black", alpha=0.06)
ax.set_xlabel("Epoch"); ax.set_ylabel("Validation IoU (%)"); ax.set_ylim(0, 100); ax.grid(True, linestyle=":", alpha=0.5)
ax.legend(fontsize=7.5, loc="lower right", frameon=False)
plt.tight_layout(); plt.savefig(os.path.join(HERE, "fig_val_iou_curves.png"), bbox_inches="tight"); plt.close()

# ---- markdown summary ----
L = ["# Experiment results (auto-generated by analyze.py)", "", f"Runs found: {len(R)}", "",
     "## Synthetic benchmark, held-out test set (pooled foreground IoU %, mean ± sample std over seeds)", "",
     "| Model | " + " | ".join(CN[c] for c in CONDS) + " | n |", "|---|" + "---|" * (len(CONDS) + 1)]
for m in MAIN:
    if m in S["synthetic"]:
        L.append(f"| {NAMES[m]} | " + " | ".join(f"{S['synthetic'][m][c]['iou']['mean']:.2f} ± {S['synthetic'][m][c]['iou']['std']:.2f}" for c in CONDS)
                 + f" | {S['synthetic'][m]['normal']['iou']['n']} |")
L += ["", "### Paired t-tests, MSBA-Net minus baseline (IoU pp; Holm-corrected p)", ""]
for c in CONDS:
    L.append(f"- **{CN[c]}**: " + "; ".join(f"vs {NAMES[x['vs']]} {x['mean_diff_pp']:+.2f} pp (p={x['p']:.3f}, Holm {x['p_holm']:.3f}, n={x['n']})" for x in S["stats"][f"synthetic_{c}"]))
L += ["", "## NEU-Seg test set (mIoU over the 3 defect classes %, mean ± std)", "", "| Model | mIoU | mDice | IoU inclusion / patches / scratches | n |", "|---|---|---|---|---|"]
for m in MAIN:
    if m in S["neu"]:
        n = S["neu"][m]; pc = n["iou_per_class_mean"]
        L.append(f"| {NAMES[m]} | {n['miou_defects']['mean']:.2f} ± {n['miou_defects']['std']:.2f} | {n['mdice_defects']['mean']:.2f} ± {n['mdice_defects']['std']:.2f} | {pc[1]:.2f} / {pc[2]:.2f} / {pc[3]:.2f} | {n['miou_defects']['n']} |")
L.append("- " + "; ".join(f"vs {NAMES[x['vs']]} {x['mean_diff_pp']:+.2f} pp (p={x['p']:.3f}, Holm {x['p_holm']:.3f})" for x in S["stats"]["neu"]))
for title, key in (("Architecture ablation", "ablation"), ("Loss ablation", "loss"), ("lambda_bound sensitivity", "lambda")):
    L += ["", f"## {title} (test IoU %)", ""]
    for k, v in S[key].items():
        L.append(f"- {k}: " + "; ".join(f"{CN[c]} {x['mean']:.2f} ± {x['std']:.2f} (n={x['n']})" for c, x in v.items()))
L += ["", "## Efficiency (256×256×1, FP32, batch 1)", "", "| Model | Params (M) | GMACs | Latency (ms) |", "|---|---|---|---|"]
L += [f"| {NAMES[m]} | {e['params_M']:.2f} | {e['gmacs']:.2f} | {e['latency_ms']:.2f} |" for m, e in eff.items()]
L += ["", "## Best epoch (synthetic)", ""] + [f"- {NAMES[m]}: {sorted(v.values())}" for m, v in S["best_epochs"].items()]
open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
