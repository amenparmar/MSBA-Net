"""Round 2 (author 2026-11-16: 'run the augmentation experiments and the remaining baselines too').
1. Degradation-augmented training (C6): the five main models x 5 seeds, synthetic, same protocol plus degrade_aug.
2. Further baselines (M1): HRNetV2-W18 and SegFormer-B1, synthetic x 5 seeds and NEU-Seg x 3 seeds.
Resumable; log run_round2.log."""
import sys, time, traceback
sys.dont_write_bytecode = True
import common as C

SYN_EPOCHS, NEU_EPOCHS = 40, 30
MAIN = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "MSBANet"]
NEW = ["HRNetW18", "SegFormerB1"]


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True); open("run_round2.log", "a", encoding="utf-8").write(line + "\n")


syn_test = {c: C.synth_split("test", cond=c) for c in C.CONDITIONS}
plan = [("syn", f"syn_aug_{m}_s{s}", m, s, True) for s in C.SEEDS for m in MAIN]
plan += [("syn", f"syn_{m}_s{s}", m, s, False) for s in C.SEEDS for m in NEW]
plan += [("neu", f"neu_{m}_s{s}", m, s, False) for s in C.SEEDS[:3] for m in NEW]
neu = None
log(f"plan: {len(plan)} runs")
for i, (ds, rid, m, s, aug) in enumerate(plan, 1):
    if C.os.path.exists(C.os.path.join(C.RUNS, rid + ".json")):
        continue
    t0 = time.time()
    try:
        if ds == "syn":
            data = {"train": C.synth_split("train", s), "val": C.synth_split("val", s)}
            r = C.train_run(rid, m, data, SYN_EPOCHS, s, nc=1, test_sets=syn_test, aug=aug)
            T = r["test"]
            log(f"[{i}/{len(plan)}] {rid}: best ep {r['best_epoch']} val {r['best_val']:.2f} | normal {T['normal']['iou']:.2f} "
                f"tiny {T['tiny_defects']['iou']:.2f} lowc {T['low_contrast']['iou']:.2f} blur {T['blur']['iou']:.2f} "
                f"noise {T['noise']['iou']:.2f} ({(time.time()-t0)/60:.1f} min)")
        else:
            if neu is None:
                neu = {"train": C.neu_split("train"), "val": C.neu_split("val"), "test": C.neu_split("test")}
            r = C.train_run(rid, m, {"train": neu["train"], "val": neu["val"]}, NEU_EPOCHS, s, nc=4, flips=True,
                            test_sets={"test": neu["test"]})
            log(f"[{i}/{len(plan)}] {rid}: best ep {r['best_epoch']} val {r['best_val']:.2f} | test mIoU(defects) "
                f"{r['test']['test']['miou_defects']:.2f} ({(time.time()-t0)/60:.1f} min)")
    except Exception:
        log(f"[{i}/{len(plan)}] {rid}: FAILED\n" + traceback.format_exc())
log("ALL DONE")
