#!/usr/bin/env bash
# Unattended multi-case TE run: process every .outb in $CASE_DIR through the
# hardened pipeline in one checkpointed invocation. Safe to set-and-forget —
# the per-job watchdog drops a hung kernel instead of deadlocking, te_pipeline
# catches per-case errors and continues, and it writes the combined parquet
# after EVERY case (so a crash/hang loses at most the case in flight).
#
# Edit CASE_DIR / GLOB below to point at your .outb files, then:
#     nohup bash analysis/run_campaign.sh &
# Track:    grep -E '=== \[|\[done|TIMEOUT|checkpoint|Wrote' /tmp/campaign.log
# Progress: grep -c 'case done' /tmp/campaign.log
set -euo pipefail
cd "$(dirname "$0")/.."
exec > /tmp/campaign.log 2>&1

CASE_DIR="/home/lams/Downloads"      # <-- where your .outb files live
GLOB="dlc16_v11ms_s*.outb"           # <-- pattern to run (e.g. dlc16 6-seed set)
OUT="reports/te_campaign.parquet"

mapfile -t FILES < <(ls -1 "$CASE_DIR"/$GLOB 2>/dev/null | sort)
echo "[campaign] $(date) — found ${#FILES[@]} case(s) under $CASE_DIR/$GLOB:"
printf '   %s\n' "${FILES[@]}"
if [ "${#FILES[@]}" -eq 0 ]; then echo "[campaign] nothing to run — fix CASE_DIR/GLOB"; exit 1; fi

python -u analysis/te_pipeline.py "${FILES[@]}" \
  -o "$OUT" \
  --graph-out reports/te_campaign_graph.pkl \
  --gpu --gpus 0,1 --workers 4 \
  --slow-drift-tau 5 \
  --job-timeout 9000

echo "[campaign] $(date) — DONE"
