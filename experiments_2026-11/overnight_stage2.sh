#!/usr/bin/env bash
# Stage 2 (2026-11-18): MSBA-Net v2a (selected on seed-42 validation: NEU-Seg +1.01, KolektorSDD2 +5.39 over MSBA-Net)
# under the full protocols, then the remaining KolektorSDD2 seeds for all models incl. v2a.
cd "$(dirname "$0")"
export EPOCH_LOG=ksdd2_epochs.log PYTHONDONTWRITEBYTECODE=1
until grep -q "queue: STAGE 1 DONE" ksdd2.log; do sleep 30; done
echo "$(date +%H:%M:%S) queue: stage 2 started" >> ksdd2.log
python -B dev_v2.py syn MSBANetV2a 42,100,2026,7,123 >> dev_v2.stdout 2>&1
python -B dev_v2.py neu MSBANetV2a 100,2026 >> dev_v2.stdout 2>&1
echo "$(date +%H:%M:%S) queue: v2a synthetic + NEU done" >> ksdd2.log
M8=MSBANetV2a,MSBANet,UNet,HRNetW18,DeepLabV3Plus,SegFormerB1,AttUNet,UNetPlusPlus
for s in 100 2026 7 123; do
  python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds $s --models $M8 >> ksdd2.stdout 2>&1
  python -B ksdd2_postproc.py >> ksdd2_postproc.log 2>&1
  echo "$(date +%H:%M:%S) queue: KolektorSDD2 seed $s done" >> ksdd2.log
done
echo "$(date +%H:%M:%S) queue: STAGE 2 DONE" >> ksdd2.log
