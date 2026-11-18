"""Runs synthetic / NEU-Seg trainings for any registered model under the round-1 protocol (same as run_all.py):
synthetic 40 epochs (train/val per seed, five held-out test conditions); NEU-Seg 30 epochs, flips, 4 classes.
Model selection uses validation only (best_val); test metrics are stored by train_run as for every other run.
Usage: python dev_v2.py <syn|neu> <model[,model]> <seed[,seed]>"""
import sys, time, traceback
sys.dont_write_bytecode = True
import common as C

ds, models, seeds = sys.argv[1], sys.argv[2].split(","), [int(s) for s in sys.argv[3].split(",")]
LOG = "dev_v2.log"


def log(m):
    line = time.strftime("%H:%M:%S ") + m; print(line, flush=True); open(LOG, "a", encoding="utf-8").write(line + "\n")


data = None
for s in seeds:
    for m in models:
        rid = f"{ds}_{m}_s{s}"; t0 = time.time()
        try:
            if ds in ("syn", "syn_aug"):     # syn_aug = degradation augmentation, as in run_round2.py
                syn_test = {c: C.synth_split("test", cond=c) for c in C.CONDITIONS}
                r = C.train_run(rid, m, {"train": C.synth_split("train", s), "val": C.synth_split("val", s)}, 40, s, nc=1,
                                test_sets=syn_test, aug=(ds == "syn_aug"))
            else:
                if data is None:
                    data = {k: C.neu_split(k) for k in ("train", "val", "test")}
                r = C.train_run(rid, m, {"train": data["train"], "val": data["val"]}, 30, s, nc=4, flips=True, test_sets={"test": data["test"]})
            log(f"{rid}: best ep {r['best_epoch']} VAL {r['best_val']:.2f} ({(time.time() - t0) / 60:.1f} min)")
        except Exception:
            log(f"{rid}: FAILED\n" + traceback.format_exc())
