"""NEU-Seg test-time augmentation (same rule for every model): softmax averaged over the identity, horizontal,
vertical and both flips (training used random flips). Evaluates the saved best-validation checkpoints of every
model on validation and test; writes neu_tta.json. Inference only."""
import os, sys, json, time
sys.dont_write_bytecode = True
import numpy as np, torch
import common as C

MODELS = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "HRNetW18", "SegFormerB1", "MSBANet", "MSBANetV2c"]
SEEDS = [42, 100, 2026]


@torch.no_grad()
def predict_tta(model, images, bs=16):
    model.eval(); out = []
    for i in range(0, len(images), bs):
        x = images[i:i + bs].to(C.DEV); p = 0
        for f in ((), (-1,), (-2,), (-1, -2)):
            xi = x.flip(f) if f else x
            with torch.autocast("cuda", dtype=torch.bfloat16):
                lg, _ = model(xi)
            s = lg.float().softmax(1)
            p = p + (s.flip(f) if f else s)
        out.append(p.argmax(1).cpu())
    return torch.cat(out)


if __name__ == "__main__":
    data = {k: C.neu_split(k) for k in ("val", "test")}
    out_p = os.path.join(C.HERE, "neu_tta.json")
    res = json.load(open(out_p)) if os.path.exists(out_p) else {}
    for m in MODELS:
        for s in SEEDS:
            rid = f"neu_{m}_s{s}"
            if rid in res:
                continue
            net = C.MODELS[m](4).to(C.DEV); net.load_state_dict(torch.load(os.path.join(C.RUNS, rid + ".pth"), map_location=C.DEV))
            r = {k: {"plain": C.multiclass_metrics(C.predict(net, data[k]["image"], 4), data[k]["mask"], 4)["miou_defects"],
                     "tta": C.multiclass_metrics(predict_tta(net, data[k]["image"]), data[k]["mask"], 4)["miou_defects"]}
                 for k in ("val", "test")}
            res[rid] = r; json.dump(res, open(out_p, "w"), indent=1); del net; torch.cuda.empty_cache()
            print(f"{time.strftime('%H:%M:%S')} {rid}: val {r['val']['plain']:.2f}->{r['val']['tta']:.2f} | test {r['test']['plain']:.2f}->{r['test']['tta']:.2f}", flush=True)
