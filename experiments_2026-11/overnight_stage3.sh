#!/usr/bin/env bash
# Stage 3 (2026-11-18): MSBA-Net v2c selected on NEU-Seg validation (mean of seeds 42/100: v2c 78.58, v2d 78.51,
# v2a 78.31, MSBA-Net 77.31). Full protocols for v2c, then the remaining KolektorSDD2 seeds.
cd "$(dirname "$0")"
export EPOCH_LOG=ksdd2_epochs.log PYTHONDONTWRITEBYTECODE=1
echo "$(date +%H:%M:%S) queue: stage 3 started (v2c selected)" >> ksdd2.log
python -B dev_v2.py neu MSBANetV2c 2026 >> dev_v2.stdout 2>&1
python -B dev_v2.py syn MSBANetV2c 42,100,2026,7,123 >> dev_v2.stdout 2>&1
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 42 --models MSBANetV2c >> ksdd2.stdout 2>&1
python -B ksdd2_postproc.py >> ksdd2_postproc.log 2>&1
echo "$(date +%H:%M:%S) queue: v2c NEU + synthetic + KolektorSDD2 s42 done" >> ksdd2.log
M8=MSBANetV2c,MSBANet,UNet,HRNetW18,DeepLabV3Plus,SegFormerB1,AttUNet,UNetPlusPlus
for s in 100 2026 7 123; do
  python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds $s --models $M8 >> ksdd2.stdout 2>&1
  python -B ksdd2_postproc.py >> ksdd2_postproc.log 2>&1
  echo "$(date +%H:%M:%S) queue: KolektorSDD2 seed $s done" >> ksdd2.log
done
echo "$(date +%H:%M:%S) queue: STAGE 3 DONE" >> ksdd2.log
