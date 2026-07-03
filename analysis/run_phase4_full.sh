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

# Every case ships the SAME filename (sims/<case>/IEA-15-.../IEA-15-...outb), so
# te_pipeline's stem-based case_id would collapse all 54 cases to one id and
# merge_parquet_parts.py would drop_duplicates them down to ~2. Stage each .outb
# as a FOLDER-named symlink first (exactly like run_campaign.sh) so the stem
# becomes the real case id (dlca_v11ms_s00, ...).
STAGE="/tmp/te_full_inputs"
rm -rf "$STAGE"; mkdir -p "$STAGE"
shopt -s nullglob
for outb in sims/*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb; do
    case_name="$(basename "$(dirname "$(dirname "$outb")")")"
    ln -sf "$(realpath "$outb")" "$STAGE/$case_name.outb"
done
mapfile -t ALL_OUTB < <(ls "$STAGE"/*.outb 2>/dev/null | sort)
TOTAL=${#ALL_OUTB[@]}

if [ "$TOTAL" -lt 1 ]; then
    echo "ERROR: no .outb files found in sims/*/IEA-15-240-RWT-UMaineSemi/. Run Phase 2 first." >&2
    exit 1
fi

echo "Total cases: $TOTAL"
echo "Workers:     $N"
echo "Per worker:  ~$((TOTAL / N))-$((TOTAL / N + 1)) cases"
echo "Settings:    FULL (conditional + Granger + AIS + coherence, max_lag=150, max_lag_sources=20, 5 Hz, n_perm=200)"
echo ""

mkdir -p reports analysis

# Full settings: only override the three knobs the first pass lowered.
# Conditional + Granger + AIS + coherence stay ON (no --no-* flags).
# --slow-drift-tau 5 matches run_campaign.sh / te_rerun_missing.py: at tau=1 the
# 4 slow-drift targets go singular in the Gaussian (Granger) estimator => TE=nan
# (see TESettings docstring, te_pipeline.py:111-120), which would NaN the Granger
# baseline this rerun exists to produce (Gap 1).
# --max-lag-sources 20: symmetric max_lag=150 nulls real couplings — the greedy
# max-stat tightens with candidate-pool size and rejected Wave->PtfmHeave
# (te_pipeline.py TESettings, commit 986f867). Re-validation on dlca_v11ms_s00
# (reports/diag_revalidate.parquet, 2026-07-03): w=20 and w=45 both recover
# TE=0.067 (p=0.005, lag 6 = 1.2 s); w=30 stochastically nulled. 20 = smallest
# candidate pool => most sensitive + cheapest; target embedding stays 150.
COMMON_ARGS=( --n-perm 200 --max-lag 150 --max-lag-sources 20 --decimate-target-hz 5.0 --slow-drift-tau 5 )

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
