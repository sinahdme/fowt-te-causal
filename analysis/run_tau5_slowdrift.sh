#!/usr/bin/env bash
# Plan B: recompute ALL PtfmPitch + PtfmHeave edges at tau=5 so each slow-drift
# target is internally uniform in tau (drops their salvaged tau=1 rows). Every
# other target stays tau=1 from the salvage. ~14 jobs, ~45-60 min on 2 GPUs.
#
# Writes a NEW parquet (te_v08_full_uniform.parquet) so the current
# te_v08_full.parquet is preserved until you've checked the result.
#
# Usage:        nohup bash analysis/run_tau5_slowdrift.sh &
# Track with:   grep -E '\[force|\[missing|->|\[launch|\[done|TIMEOUT|CRASH|\[write' /tmp/rerun_tau5_slowdrift.log
set -euo pipefail
cd "$(dirname "$0")/.."
exec > /tmp/rerun_tau5_slowdrift.log 2>&1

python -u analysis/te_rerun_missing.py \
  --outb /home/lams/Downloads/dlca_v08ms_s00.outb \
  --log /tmp/te_v08_full.log /tmp/rerun.log \
  --out /tmp/te_v08_full_uniform.parquet \
  --gpu --gpus 0,1 \
  --tau 5 \
  --force-targets PtfmPitch,PtfmHeave \
  --max-parallel 4 \
  --timeout 5400
