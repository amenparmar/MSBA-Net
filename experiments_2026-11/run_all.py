"""Runs the whole programme in priority order; resumable (finished runs are skipped). Log: run_all.log"""
import sys, time, json, traceback
sys.dont_write_bytecode = True
import common as C

SYN_EPOCHS, NEU_EPOCHS = 40, 30
MAIN = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "MSBANet"]
LOSSES = {"Loss1_BCE": {"lambda_dice": 0.0, "lambda_focal": 0.0, "lambda_boundary": 0.0},
          "Loss2_BCE_Dice": {"lambda_dice": 1.0, "lambda_focal": 0.0, "lambda_boundary": 0.0},
          "Loss3_BCE_Dice_Focal": {"lambda_dice": 1.0, "lambda_focal": 0.5, "lambda_boundary": 0.0}}
LAMBDAS = {"Lb0.2": 0.2, "Lb0.8": 0.8}


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True); open("run_all.log", "a", encoding="utf-8").write(line + "\n")


syn_test = {c: C.synth_split("test", cond=c) for c in C.CONDITIONS}
plan = []
for s in C.SEEDS:                                   # 1. main synthetic comparison, 5 seeds
    for m in MAIN:
        plan.append(("syn", f"syn_{m}_s{s}", m, s, None))
for s in C.SEEDS[:3]:                               # 2. NEU-Seg (real), 3 seeds
    for m in MAIN:
        plan.append(("neu", f"neu_{m}_s{s}", m, s, None))
for s in C.SEEDS:                                   # 3. architecture ablation, 5 seeds (Arch-1 = UNet, Arch-4 = MSBANet)
    for m in ("Arch2_MSFP", "Arch3_MSFP_BAS"):
        plan.append(("syn", f"syn_{m}_s{s}", m, s, None))
for s in C.SEEDS[:3]:                               # 4. loss ablation (Loss-4 = MSBANet), 3 seeds
    for k, cfg in LOSSES.items():
        plan.append(("syn", f"syn_MSBANet_{k}_s{s}", "MSBANet", s, cfg))
for s in C.SEEDS[:3]:                               # 5. lambda_bound sensitivity (0.4 = MSBANet), 3 seeds
    for k, lb in LAMBDAS.items():
        plan.append(("syn", f"syn_MSBANet_{k}_s{s}", "MSBANet", s, {"lambda_boundary": lb}))

neu = None
log(f"plan: {len(plan)} runs")
for i, (ds, rid, m, s, cfg) in enumerate(plan, 1):
    if (C.os.path.exists(C.os.path.join(C.RUNS, rid + ".json"))):
        continue
    t0 = time.time()
    try:
        if ds == "syn":
            data = {"train": C.synth_split("train", s), "val": C.synth_split("val", s)}
            r = C.train_run(rid, m, data, SYN_EPOCHS, s, nc=1, loss_cfg=cfg, test_sets=syn_test)
            log(f"[{i}/{len(plan)}] {rid}: best ep {r['best_epoch']} val {r['best_val']:.2f} | test normal {r['test']['normal']['iou']:.2f} "
                f"tiny {r['test']['tiny_defects']['iou']:.2f} lowc {r['test']['low_contrast']['iou']:.2f} ({(time.time()-t0)/60:.1f} min)")
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
