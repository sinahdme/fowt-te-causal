#!/usr/bin/env bash
# Launch the tau=5 GPU rerun of the 4 stuck slow-drift jobs
# (granger Wave1Elev->PtfmHeave, bivariate Wave1Elev->PtfmPitch, and the two
# conditional ->PtfmPitch pairs). Harvests the already-good results — including
# AIS(FAIRTEN1) — from both the original log and the partial CPU rerun log, so
# only the 4 jobs are recomputed. Self-redirects to /tmp/rerun_tau5.log.
#
# Usage (from anywhere):  nohup bash analysis/run_tau5_rerun.sh &
# Track with:             grep -E '\[launch|\[done|TIMEOUT|CRASH|\[write' /tmp/rerun_tau5.log
set -euo pipefail
cd "$(dirname "$0")/.."          # repo root, regardless of where it's called from

exec > /tmp/rerun_tau5.log 2>&1  # all output to the tracking log

python -u analysis/te_rerun_missing.py \
  --outb /home/lams/Downloads/dlca_v08ms_s00.outb \
  --log /tmp/te_v08_full.log /tmp/rerun.log \
  --out /tmp/te_v08_full.parquet \
  --gpu --gpus 0,1 \
  --tau 5 \
  --max-parallel 4 \
  --timeout 5400
