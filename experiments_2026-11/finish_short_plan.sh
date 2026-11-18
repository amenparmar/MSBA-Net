#!/usr/bin/env bash
# Author 2026-11-18: short plan. KolektorSDD2 stops after seed 2026 (3 seeds, as NEU-Seg); seeds 7 and 123 are not run.
# One check run: DeepLabv3+ seed 100 retrained in a fresh process (prefix ksdd2rerun), because the original run
# collapsed temporarily right after the 3-minute suspend used for latency timing.
cd "$(dirname "$0")"
export EPOCH_LOG=ksdd2_epochs.log PYTHONDONTWRITEBYTECODE=1
until grep -q "queue: KolektorSDD2 seed 2026 done" ksdd2.log; do sleep 15; done
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { (\$_.Name -eq 'bash.exe' -and \$_.CommandLine -match 'overnight_stage3') -or (\$_.Name -eq 'python.exe' -and \$_.CommandLine -match 'ksdd2.py' -and \$_.CommandLine -match '--seeds 7') } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }"
sleep 5
echo "$(date +%H:%M:%S) queue: short plan - stopped after seed 2026 (seeds 7, 123 not run); DLV3+ s100 check rerun next" >> ksdd2.log
python -B ksdd2.py "D:/scratch/kolektorsdd2" --seeds 100 --models DeepLabV3Plus --prefix ksdd2rerun >> ksdd2.stdout 2>&1
echo "$(date +%H:%M:%S) queue: SHORT PLAN DONE" >> ksdd2.log
