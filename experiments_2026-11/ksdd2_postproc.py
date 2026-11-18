"""KolektorSDD2 post-processing (same rule for every model): remove predicted connected components (8-connectivity)
smaller than a minimum area T. T is chosen per run from the fixed grid below by validation pixel IoU (ties -> smaller T);
the test set is evaluated once with that T. Reads runs/ksdd2_*.pth; writes ksdd2_postproc.json. Inference only."""
import os, sys, json, glob, time
sys.dont_write_bytecode = True
import numpy as np, torch
from scipy import ndimage
import common as C, ksdd2 as K

GRID = [0, 8, 16, 32, 64, 128, 256]
ST = np.ones((3, 3), bool)


def filt(P, T):
    if T == 0:
        return P
    out = np.zeros_like(P)
    for k, p in enumerate(P):
        if p.any():
            lab, n = ndimage.label(p, ST)
            area = np.bincount(lab.ravel(), minlength=n + 1); keep = area >= T; keep[0] = False
            out[k] = keep[lab]
    return out


def pix_iou(P, split):
    Y = split["mask"][:, 0].numpy().astype(bool); V = split["valid"].numpy(); P = P & V
    tp = (P & Y).sum(); return 100 * tp / max(tp + (P & ~Y).sum() + (~P & Y).sum(), 1)


if __name__ == "__main__":
    D = K.load(sys.argv[1] if len(sys.argv) > 1 else r"D:\scratch\kolektorsdd2")
    out_p = os.path.join(C.HERE, "ksdd2_postproc.json")
    res = json.load(open(out_p)) if os.path.exists(out_p) else {}
    for pth in sorted(glob.glob(os.path.join(C.RUNS, "ksdd2_*.pth"))):
        rid = os.path.basename(pth)[:-4]; jp = pth[:-4] + ".json"
        if rid in res or not os.path.exists(jp) or not json.load(open(jp)).get("test"):
            continue                                        # skip runs still training
        r = json.load(open(jp)); arch = K.VARIANTS.get(r.get("variant", r["model"]), (r["model"], None))[0]
        net = C.MODELS[arch](1).to(C.DEV); net.load_state_dict(torch.load(pth, map_location=C.DEV))
        Pv = C.predict(net, D["val"]["image"], 1, bs=4).numpy().astype(bool)
        Pt = C.predict(net, D["test"]["image"], 1, bs=4).numpy().astype(bool)
        del net; torch.cuda.empty_cache()
        val = {T: float(pix_iou(filt(Pv, T), D["val"])) for T in GRID}
        best = max(GRID, key=lambda T: (round(val[T], 6), -T))
        res[rid] = {"val_iou_by_T": val, "T": best, "test_raw": K.evaluate_preds(Pt, D["test"]),
                    "test_filtered": K.evaluate_preds(filt(Pt, best), D["test"])}
        json.dump(res, open(out_p, "w"), indent=1)
        a, b = res[rid]["test_raw"], res[rid]["test_filtered"]
        print(f"{time.strftime('%H:%M:%S')} {rid}: T={best} | IoU {a['iou']:.2f} -> {b['iou']:.2f} | small found "
              f"{a['components']['small_le1024_found']} -> {b['components']['small_le1024_found']}/30 | false blobs "
              f"{a['false_components']} -> {b['false_components']}", flush=True)
