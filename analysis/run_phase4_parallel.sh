#!/usr/bin/env bash
# run_phase4_parallel.sh — launch N parallel te_pipeline.py workers, each on
# its own disjoint subset of the 54 .outb files. Bivariate-only + 2 Hz +
# n_perm=50 + max_lag=60 (the scope-reduced first-pass settings).
#
# Each worker writes to its own reports/te_table_p<W>.parquet.
# After all workers finish, run analysis/merge_parquet_parts.py to combine.
#
# Usage:
#   ./analysis/run_phase4_parallel.sh         # default 12 workers
#   ./analysis/run_phase4_parallel.sh 8       # 8 workers

set -euo pipefail

N="${1:-12}"

# cd to project root (parent of analysis/)
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
echo ""

mkdir -p reports analysis

# Common args for every worker: bivariate-only first pass at 2 Hz.
COMMON_ARGS=( --n-perm 50 --max-lag 60 --decimate-target-hz 2.0 --no-conditional --no-granger )

PIDS=()
for w in $(seq 0 $((N - 1))); do
    # Round-robin distribution: worker w gets indices w, w+N, w+2N, ...
    # Keeps each worker's case list mixed across DLCs (dlc16 / dlca / dlcb).
    FILES=()
    i=$w
    while [ $i -lt $TOTAL ]; do
        FILES+=("${ALL_OUTB[$i]}")
        i=$((i + N))
    done

    if [ ${#FILES[@]} -eq 0 ]; then
        continue
    fi

    OUT="reports/te_table_p${w}.parquet"
    LOG="analysis/run-fast-p${w}.log"

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
echo "── Check progress (count completed cases per worker):"
echo "  for f in analysis/run-fast-p*.log; do echo -n \"\$f \"; grep -c 'OK (' \$f; done"
echo ""
echo "── Total completed cases across all workers:"
echo "  grep -h 'OK (' analysis/run-fast-p*.log | wc -l"
echo ""
echo "── When all $TOTAL cases done, merge the parts into one table:"
echo "  python analysis/merge_parquet_parts.py"
