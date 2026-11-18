#!/usr/bin/env bash
# KolektorSDD2 queue (author approved the ablation 2026-11-18): after the seed-42 run of all 7 models, stop the main
# process, run the three MSBA-Net ablation variants (seed 42), then continue seed by seed.
cd "$(dirname "$0")"
export EPOCH_LOG=ksdd2_epochs.log PYTHONDONTWRITEBYTECODE=1
M7=MSBANet,UNet,HRNetW18,DeepLabV3Plus,SegFormerB1,AttUNet,UNetPlusPlus
V3=Arch3_MSFP_BAS,MSBANet_noBL,Arch2_MSFP
until grep -q "\] ksdd2_UNetPlusPlus_s42" ksdd2.log; do sleep 30; done
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'ksdd2.py' -and \$_.CommandLine -match 'UNetPlusPlus' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }"
sleep 5
echo "$(date +%H:%M:%S) queue: seed-42 main runs done; main process stopped; ablation variants next" >> ksdd2.log
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 42 --models $V3 >> ksdd2.stdout 2>&1
python -B ksdd2_postproc.py >> ksdd2_postproc.log 2>&1
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 100 --models $M7,$V3 >> ksdd2.stdout 2>&1
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 2026 --models $M7,$V3 >> ksdd2.stdout 2>&1
python -B ksdd2_postproc.py >> ksdd2_postproc.log 2>&1
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 7,123 --models $M7 >> ksdd2.stdout 2>&1
python -B ksdd2_postproc.py >> ksdd2_postproc.log 2>&1
echo "$(date +%H:%M:%S) queue: ALL QUEUE DONE" >> ksdd2.log
