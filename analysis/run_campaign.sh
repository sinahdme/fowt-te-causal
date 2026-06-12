#!/usr/bin/env bash
# Unattended multi-case TE run over the sims/ DLC matrix.
#
# The .outb files all share the name IEA-15-240-RWT-UMaineSemi.outb inside
# per-case folders (sims/<case>/IEA-15-.../...outb), so we symlink each to its
# FOLDER name in a staging dir — that makes te_pipeline's stem-based case_id
# come out as dlc16_v11ms_s00 etc., keeping cases distinct in the parquet.
#
# Safe to set-and-forget: per-job watchdog drops a hung kernel instead of
# deadlocking, per-case errors are caught, and the combined parquet is written
# after EVERY case (crash/hang loses at most the case in flight).
#
# Pick the subset with CASES (a shell glob over sims/ folder names). Default is
# the DLC-1.6 6-seed bin (~6 cases ≈ a 2-day window). Examples:
#   CASES="dlc16_v11ms_s*"      # DLC-1.6 validation bin (default)
#   CASES="dlca_v11ms_s*"       # DLC-A 11 m/s, 6 seeds
#   CASES="dlca_v*ms_s00"       # one seed per wind speed (4 cases, a quick spread)
#
# Usage:   nohup bash analysis/run_campaign.sh &
# Track:   grep -E '=== \[|\[done|TIMEOUT|checkpoint|Wrote|case done' /tmp/campaign.log
set -euo pipefail
cd "$(dirname "$0")/.."
exec > /tmp/campaign.log 2>&1

CASES="${CASES:-dlc16_v11ms_s*}"     # <-- which sims/ cases to run (override via env)
STAGE="/tmp/te_inputs"
OUT="reports/te_campaign.parquet"

echo "[campaign] $(date) — staging cases matching sims/$CASES"
rm -rf "$STAGE"; mkdir -p "$STAGE"
shopt -s nullglob
for d in sims/$CASES/; do
  case_name="$(basename "$d")"
  outb="$(ls "$d"*/*.outb 2>/dev/null | head -1)"
  if [ -n "$outb" ]; then
    ln -sf "$(realpath "$outb")" "$STAGE/$case_name.outb"
    echo "   $case_name.outb -> $outb"
  fi
done
FILES=("$STAGE"/*.outb)
echo "[campaign] ${#FILES[@]} case(s) staged."
if [ "${#FILES[@]}" -eq 0 ]; then echo "[campaign] no matches — fix CASES"; exit 1; fi

python -u analysis/te_pipeline.py "${FILES[@]}" \
  -o "$OUT" \
  --graph-out reports/te_campaign_graph.pkl \
  --gpu --gpus 0,1 --workers 4 \
  --slow-drift-tau 5 \
  --job-timeout 9000

echo "[campaign] $(date) — DONE"
