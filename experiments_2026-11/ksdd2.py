"""KolektorSDD2: second real dataset (all seven models x 5 seeds), binary defect segmentation.

Data: KolektorSDD2.zip from https://www.vicos.si/resources/kolektorsdd2/ (CC BY-NC-SA 4.0; Bozic, Tabernik, Skocaj,
Computers in Industry 2021), extracted to <root> with train/ and test/ folders holding <id>.png and <id>_GT.png.

Protocol (fixed before any KolektorSDD2 result was seen):
  * official test split for testing only; fixed 10 % validation hold-out (seed 0) from the official training split;
  * images converted to grayscale, kept at native resolution and padded (edge-replicate; mask 0) to a common size
    divisible by 32; padded pixels are excluded from every test metric;
  * same training as the synthetic benchmark (common.train_run: AdamW 1e-3/1e-4, cosine, batch 16, bf16, the paper's
    composite loss BCE + Dice + 0.5 focal [+ 0.4 boundary]), random flips, 40 epochs, best-validation checkpoint;
  * test metrics on valid pixels: pooled IoU / Dice / precision / recall; mean IoU over defective images;
    small-defect analysis: recall of ground-truth connected components (8-connectivity) in the pre-set area bins
    <=256, 257-1024, 1025-4096, >4096 px (found when >= 50 % of the component is predicted defective);
    false components (predicted components that touch no ground truth); image-level detection (an image is called
    defective when it has >= 1 predicted pixel): recall on defective, false-alarm rate on defect-free images.
Usage:  python ksdd2.py <root> [--seeds 42,100,2026,7,123] [--models ...] [--epochs 40]
"""
import os, sys, json, time, argparse, traceback, glob
sys.dont_write_bytecode = True
import numpy as np, torch
from PIL import Image
from scipy import ndimage
import common as C

BINS = [(1, 256), (257, 1024), (1025, 4096), (4097, 10 ** 9)]
BIN_NAMES = ["<=256", "257-1024", "1025-4096", ">4096"]
ALL_MODELS = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "HRNetW18", "SegFormerB1", "MSBANet"]
LOG = os.path.join(C.HERE, "ksdd2.log")
# U-Net++ needs 13 GB at batch 16 x 672 x 256 (GPU has 12 GB): its batch of 16 is processed as 2 x 8 with summed gradients
ACCUM = {"UNetPlusPlus": 2}
# ablation variants on KolektorSDD2 (added 2026-11-18 after the seed-42 results showed many false blobs for MSBA-Net):
# name -> (architecture in common.MODELS, loss_cfg). Arch2 = MSFP only; Arch3 = MSFP + BAS without BGFF;
# MSBANet_noBL = full architecture trained without the boundary loss term.
VARIANTS = {"Arch2_MSFP": ("Arch2_MSFP", None), "Arch3_MSFP_BAS": ("Arch3_MSFP_BAS", None),
            "MSBANet_noBL": ("MSBANet", {"lambda_boundary": 0.0})}


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True); open(LOG, "a", encoding="utf-8").write(line + "\n")


def _read(folder):
    ids = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(folder, "*.png")) if not p.endswith("_GT.png"))
    ims = [np.asarray(Image.open(os.path.join(folder, i + ".png")).convert("L")) for i in ids]
    gts = [(np.asarray(Image.open(os.path.join(folder, i + "_GT.png")).convert("L")) > 127).astype(np.uint8) for i in ids]
    for i, a, g in zip(ids, ims, gts):
        if a.shape != g.shape:
            sys.exit(f"STOP: {i} image {a.shape} != mask {g.shape}")
    return ids, ims, gts


def _pack(ids, ims, gts, H, W):
    n = len(ids); x = np.zeros((n, H, W), np.uint8); y = np.zeros((n, H, W), np.uint8); v = np.zeros((n, H, W), bool)
    b = np.zeros((n, H, W), np.uint8)
    for k, (a, g) in enumerate(zip(ims, gts)):
        h, w = a.shape
        x[k] = np.pad(a, ((0, H - h), (0, W - w)), mode="edge"); y[k, :h, :w] = g; v[k, :h, :w] = True
        bd = ndimage.binary_dilation(g, iterations=2).astype(np.float32) - ndimage.binary_erosion(g, iterations=1).astype(np.float32)
        b[k, :h, :w] = np.clip(bd, 0, 1) * 255                          # author's dataset.py boundary definition
    return {"image": torch.from_numpy(x).unsqueeze(1).float() / 255.0, "mask": torch.from_numpy(y).unsqueeze(1).float(),
            "boundary": torch.from_numpy(b).unsqueeze(1).float() / 255.0, "valid": torch.from_numpy(v), "ids": ids}


def load(root):
    p = os.path.join(C.CACHE, "ksdd2_splits.pt")
    if not os.path.exists(p):
        tr = _read(os.path.join(root, "train")); te = _read(os.path.join(root, "test"))
        shapes = [a.shape for a in tr[1] + te[1]]
        H = int(np.ceil(max(s[0] for s in shapes) / 32) * 32); W = int(np.ceil(max(s[1] for s in shapes) / 32) * 32)
        n = len(tr[0]); perm = np.random.default_rng(0).permutation(n); nval = n // 10
        vi, ti = sorted(perm[:nval].tolist()), sorted(perm[nval:].tolist())
        sub = lambda d, idx: tuple([d[k][i] for i in idx] for k in range(3))
        out = {"train": _pack(*sub(tr, ti), H, W), "val": _pack(*sub(tr, vi), H, W), "test": _pack(*te, H, W),
               "info": {"H": H, "W": W, "native_shapes": sorted(set(shapes)), "n_train_official": n,
                        "n_test": len(te[0]), "pos_train": int(sum(g.any() for g in tr[2])), "pos_test": int(sum(g.any() for g in te[2]))}}
        torch.save(out, p)
    return torch.load(p)


def evaluate(model, split):
    return evaluate_preds(C.predict(model, split["image"], 1, bs=8).numpy().astype(bool), split)


def evaluate_preds(P, split):
    Y = split["mask"][:, 0].numpy().astype(bool); V = split["valid"].numpy()
    P &= V
    tp = int((P & Y).sum()); fp = int((P & ~Y).sum()); fn = int((~P & Y).sum()); e = 1e-9
    st = np.ones((3, 3), bool); total = np.zeros(len(BINS), int); found = np.zeros(len(BINS), int); false_c = 0
    pos_iou, det_pos, det_neg, npos, nneg = [], 0, 0, 0, 0
    for p, y in zip(P, Y):
        if y.any():
            npos += 1; det_pos += int(p.any()); pos_iou.append((p & y).sum() / (p | y).sum())
            lab, n = ndimage.label(y, st)
            area = np.bincount(lab.ravel(), minlength=n + 1)[1:]; hit = np.bincount(lab.ravel(), weights=p.ravel(), minlength=n + 1)[1:]
            for b, (lo, hi) in enumerate(BINS):
                sel = (area >= lo) & (area <= hi); total[b] += sel.sum(); found[b] += (sel & (hit >= 0.5 * area)).sum()
        else:
            nneg += 1; det_neg += int(p.any())
        if p.any():
            lab, n = ndimage.label(p, st)
            ov = np.bincount(lab.ravel(), weights=y.ravel(), minlength=n + 1)[1:]; false_c += int((ov == 0).sum())
    return {"iou": 100 * tp / (tp + fp + fn + e), "dice": 100 * 2 * tp / (2 * tp + fp + fn + e),
            "precision": 100 * tp / (tp + fp + e), "recall": 100 * tp / (tp + fn + e),
            "mean_iou_defective_images": float(100 * np.mean(pos_iou)),
            "components": {"bins": BIN_NAMES, "total": total.tolist(), "found": found.tolist(),
                           "recall": [float(100 * f / t) if t else None for f, t in zip(found, total)],
                           "small_le1024_total": int(total[:2].sum()), "small_le1024_found": int(found[:2].sum())},
            "false_components": false_c,
            "image_detection_recall": 100 * det_pos / max(npos, 1), "image_false_alarm_rate": 100 * det_neg / max(nneg, 1)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--seeds", default=",".join(map(str, C.SEEDS)))
    ap.add_argument("--models", default=",".join(ALL_MODELS)); ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--prefix", default="ksdd2")
    a = ap.parse_args()
    D = load(a.root)
    log(f"KolektorSDD2: {json.dumps(D['info'])}; train {len(D['train']['ids'])} / val {len(D['val']['ids'])} / test {len(D['test']['ids'])}")
    plan = [(s, m) for s in map(int, a.seeds.split(",")) for m in a.models.split(",")]
    for i, (s, m) in enumerate(plan, 1):
        rid = f"{a.prefix}_{m}_s{s}"; jp = os.path.join(C.RUNS, rid + ".json")
        if os.path.exists(jp) and json.load(open(jp)).get("test"):
            continue
        t0 = time.time()
        try:
            arch, cfg = VARIANTS.get(m, (m, None))
            r = C.train_run(rid, arch, {"train": D["train"], "val": D["val"]}, a.epochs, s, nc=1, flips=True, test_sets={},
                            accum=ACCUM.get(arch, 1), compact=True, loss_cfg=cfg)
            r["variant"] = m
            net = C.MODELS[arch](1).to(C.DEV); net.load_state_dict(torch.load(os.path.join(C.RUNS, rid + ".pth"), map_location=C.DEV))
            r["dataset"] = "kolektorsdd2"; r["test"] = {"test": evaluate(net, D["test"])}
            json.dump(r, open(jp, "w"), indent=1); del net; torch.cuda.empty_cache()
            t = r["test"]["test"]
            log(f"[{i}/{len(plan)}] {rid}: best ep {r['best_epoch']} val {r['best_val']:.2f} | test IoU {t['iou']:.2f} Dice {t['dice']:.2f} "
                f"comp-recall {t['components']['recall']} n={t['components']['total']} ({(time.time() - t0) / 60:.1f} min)")
        except Exception:
            log(f"[{i}/{len(plan)}] {rid}: FAILED\n" + traceback.format_exc())
    log("ALL DONE")
