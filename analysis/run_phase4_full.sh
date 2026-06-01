#!/usr/bin/env bash
# run_phase4_full.sh — full-settings Phase 4 rerun for the journal-tier paper.
#
# Difference from run_phase4_parallel.sh (the scope-reduced first pass):
#   first pass : --no-conditional --no-granger --max-lag 60 --decimate 2.0 --n-perm 50
#   this run   : conditional + Granger + AIS + coherence ON,
#                --max-lag 150 (= 30 s slow-drift window at 5 Hz),
#                --decimate-target-hz 5.0, --n-perm 200
#
# These are the te_pipeline.py canonical defaults (see TESettings), so we pass
# only the ones we want to be explicit about. Conditional/Granger are ON simply
# by NOT passing --no-conditional / --no-granger.
#
# Closes: Gap 1 (Granger baseline), Gap 2 (conditional TE → H3, rigorous H5b),
# and re-tests the H1 / H6 nulls at the physics-correct max_lag=150.
#
# Output: per-worker reports/te_table_full_p<W>.parquet, merged by
# merge_parquet_parts.py --prefix te_table_full_p --out te_table_full.parquet.
# The first-pass reports/te_table.parquet is left untouched for reproducibility.
#
# This is SERVER work (65-core box). The cost is ~20-50x the first pass per
# case; expect hours. Run the timing probe below on ONE case first.
#
# Usage:
#   # 0. timing probe — one case, full settings, foreground, time it:
#   time python analysis/te_pipeline.py \
#       sims/dlca_v11ms_s00/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb \
#       -o /tmp/te_probe.parquet --max-lag 150 --decimate-target-hz 5.0 --n-perm 200
#
#   # 1. full sharded run (default 36 workers; tune to free cores):
#   ./analysis/run_phase4_full.sh 36
#
#   # 2. when all 54 done, merge:
#   python analysis/merge_parquet_parts.py --prefix te_table_full_p --out te_table_full.parquet

set -euo pipefail

N="${1:-36}"

cd "$(dirname "$0")/.."

mapfile -t ALL_OUTB < <(ls sims/*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb 2>/dev/null | sort)
TOTAL=${#ALL_OUTB[@]}

if [ "$TOTAL" -lt 1 ]; then
    echo "ERROR: no .outb files found in sims/*/IEA-15-240-RWT-UMaineSemi/. Run Phase 2 first." >&2
    exit 1
fi

echo "Total cases: $TOTAL"
echo "Workers:     $N"
echo "Per worker:  ~$((TOTAL / N))-$((TOTAL / N + 1)) cases"
echo "Settings:    FULL (conditional + Granger + AIS + coherence, max_lag=150, 5 Hz, n_perm=200)"
echo ""

mkdir -p reports analysis

# Full settings: only override the three knobs the first pass lowered.
# Conditional + Granger + AIS + coherence stay ON (no --no-* flags).
COMMON_ARGS=( --n-perm 200 --max-lag 150 --decimate-target-hz 5.0 )

PIDS=()
for w in $(seq 0 $((N - 1))); do
    # Round-robin: worker w gets indices w, w+N, w+2N, ... (DLCs stay mixed).
    FILES=()
    i=$w
    while [ $i -lt $TOTAL ]; do
        FILES+=("${ALL_OUTB[$i]}")
        i=$((i + N))
    done

    if [ ${#FILES[@]} -eq 0 ]; then
        continue
    fi

    OUT="reports/te_table_full_p${w}.parquet"
    LOG="analysis/run-full-p${w}.log"

    nohup python analysis/te_pipeline.py "${FILES[@]}" -o "$OUT" "${COMMON_ARGS[@]}" \
        > "$LOG" 2>&1 &
    PID=$!
    disown $PID || true
    PIDS+=("$PID")
    printf "Worker %2d: %d cases  →  %s  (PID %d)\n" "$w" "${#FILES[@]}" "$OUT" "$PID"
done

echo ""
echo "Launched $N workers."
echo ""
echo "── Total completed cases across all workers:"
echo "  grep -h 'OK (' analysis/run-full-p*.log | wc -l"
echo ""
echo "── When all $TOTAL cases done, merge the parts:"
echo "  python analysis/merge_parquet_parts.py --prefix te_table_full_p --out te_table_full.parquet"
