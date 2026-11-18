"""Black-and-white figures for the paper, from the saved runs only.
fig2_qualitative.png : held-out synthetic test samples (one per row), seed-42 checkpoints of all five models.
fig3_val_curves.png  : mean validation IoU per epoch, (a) synthetic (5 seeds), (b) NEU-Seg (3 seeds)."""
import os, sys, json, glob
sys.dont_write_bytecode = True
import numpy as np, torch
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import common as C

HERE = os.path.dirname(os.path.abspath(__file__)); FIG = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
NAMES = [("UNet", "U-Net"), ("UNetPlusPlus", "U-Net++"), ("AttUNet", "Att. U-Net"), ("DeepLabV3Plus", "DeepLabv3+"),
         ("HRNetW18", "HRNet-W18"), ("SegFormerB1", "SegFormer-B1"), ("MSBANet", "MSBA-Net")]
STY = {"UNet": ("--", "s"), "UNetPlusPlus": ("-.", "^"), "AttUNet": (":", "D"), "DeepLabV3Plus": ((0, (6, 2)), "v"),
       "HRNetW18": ((0, (1, 1)), "x"), "SegFormerB1": ((0, (4, 1, 1, 1, 1, 1)), "+"), "MSBANet": ("-", "o")}
plt.rcParams.update({"font.family": "serif", "font.size": 8})

# ---------------- Fig. 3: validation curves ----------------
fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.4))
for k, (prefix, seeds, title) in enumerate([("syn", C.SEEDS, "(a) Synthetic, validation IoU (5 seeds)"),
                                            ("neu", C.SEEDS[:3], "(b) NEU-Seg, validation mIoU (3 seeds)")]):
    for m, lab in NAMES:
        h = np.array([json.load(open(os.path.join(C.RUNS, f"{prefix}_{m}_s{s}.json")))["history"]["val_iou"] for s in seeds])
        ls, mk = STY[m]; x = np.arange(1, h.shape[1] + 1)
        ax[k].plot(x, h.mean(0), color="black", ls=ls, marker=mk, markevery=5, ms=3.2, lw=1.0, label=lab)
    ax[k].set_title(title, fontsize=8); ax[k].set_xlabel("Epoch"); ax[k].grid(ls=":", lw=0.5, color="0.75")
    if k == 0:
        ax[k].set_ylim(0, 100); ax[k].set_ylabel("IoU / mIoU (%)")
    else:
        ax[k].set_ylim(40, 80)
h, l = ax[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=4, fontsize=6.5, frameon=False, handlelength=3.0)
fig.tight_layout(rect=(0, 0.13, 1, 1)); fig.savefig(os.path.join(FIG, "fig3_val_curves.png"), dpi=300); plt.close(fig)

# ---------------- Fig. 2: qualitative ----------------
tests = {c: C.synth_split("test", cond=c) for c in ("normal", "tiny_defects", "low_contrast")}
rows = []
for cls in ("crazing", "patches", "rolled_in_scale", "scratches"):
    i = tests["normal"]["cls"].index(cls); rows.append(("normal", i, cls.replace("_", "-").capitalize()))
rows = [(c, i, {"Rolled-in-scale": "Rolled-in sc."}.get(l, l)) for c, i, l in rows]
rows.append(("tiny_defects", 0, "Tiny"))
rows.append(("low_contrast", 0, "Low contrast"))
preds = {}
for m, _ in NAMES:
    net = C.MODELS[m](1).to(C.DEV); net.load_state_dict(torch.load(os.path.join(C.RUNS, f"syn_{m}_s42.pth"), map_location=C.DEV))
    for cond, i, _ in rows:
        preds[(m, cond, i)] = C.predict(net, tests[cond]["image"][i:i + 1], 1)[0].numpy()
    del net; torch.cuda.empty_cache()
cols = ["Input", "Ground truth"] + [lab for _, lab in NAMES]
fig, ax = plt.subplots(len(rows), len(cols), figsize=(7.0, 5.1))
for r, (cond, i, lab) in enumerate(rows):
    img = tests[cond]["image"][i, 0].numpy(); gt = tests[cond]["mask"][i, 0].numpy()
    panels = [img, gt] + [preds[(m, cond, i)] for m, _ in NAMES]
    for c, p in enumerate(panels):
        a = ax[r, c]; a.imshow(p, cmap="gray", vmin=0, vmax=1 if c else None, interpolation="nearest")
        a.set_xticks([]); a.set_yticks([])
        if c >= 2:
            g = gt.astype(bool); q = p.astype(bool); u = (g | q).sum()
            a.set_xlabel(f"IoU {100 * (g & q).sum() / u:.1f}" if u else "IoU --", fontsize=6.5, labelpad=1.5)
        if r == 0: a.set_title(cols[c], fontsize=7.5)
        if c == 0: a.set_ylabel(lab, fontsize=7)
fig.tight_layout(pad=0.3, h_pad=0.5, w_pad=0.2); fig.savefig(os.path.join(FIG, "fig2_qualitative.png"), dpi=300); plt.close(fig)
print("rows:", [(c, i, l) for c, i, l in rows])
