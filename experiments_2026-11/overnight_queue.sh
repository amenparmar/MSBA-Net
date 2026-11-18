#!/usr/bin/env bash
# Overnight queue 2026-11-18 (author: "go whatever you think is right and improve my model"). Stage 1 = development
# runs on seed 42 (selection by validation only); the queue then stops so the next stage can be chosen from the
# validation results.
cd "$(dirname "$0")"
export EPOCH_LOG=ksdd2_epochs.log PYTHONDONTWRITEBYTECODE=1
until grep -q "\] ksdd2_UNetPlusPlus_s42" ksdd2.log; do sleep 30; done
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'ksdd2.py' -and \$_.CommandLine -match 'UNetPlusPlus' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }"
sleep 5
echo "$(date +%H:%M:%S) queue: seed-42 main runs done; main process stopped; v2 development next" >> ksdd2.log
python -B dev_v2.py neu MSBANetV2a,MSBANetV2b 42 >> dev_v2.stdout 2>&1
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 42 --models MSBANetV2a,MSBANetV2b >> ksdd2.stdout 2>&1
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 42 --models Arch3_MSFP_BAS,MSBANet_noBL >> ksdd2.stdout 2>&1
python -B ksdd2_postproc.py >> ksdd2_postproc.log 2>&1
echo "$(date +%H:%M:%S) queue: STAGE 1 DONE" >> ksdd2.log
