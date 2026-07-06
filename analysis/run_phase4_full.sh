#!/usr/bin/env bash
# run_phase4_full.sh — full-settings Phase 4 rerun for the journal-tier paper.
#
# Difference from run_phase4_parallel.sh (the scope-reduced first pass):
#   first pass : --no-conditional --no-granger --max-lag 60 --decimate 2.0 --n-perm 50
#   this run   : conditional + Granger + AIS + coherence ON,
#                --max-lag 150 (= 30 s slow-drift window at 5 Hz),
#                --max-lag-sources 20 (asymmetric fix, commit 986f867),
#                --decimate-target-hz 5.0, --n-perm 200
#
# Closes: Gap 1 (Granger baseline), Gap 2 (conditional TE → H3, rigorous H5b),
# and re-tests the H1 / H6 nulls at the physics-correct max_lag=150.
#
# This is LAMS (GPU) work. A previous revision sharded 36 CPU-only python
# processes (written for the 65-core box, no --gpu). That run wedged for 2 days
# with zero rows: each JIDT-CPU job child hosts a JVM whose signal handlers can
# swallow the watchdog's SIGTERM, so p.join() in _execute_watchdog blocked
# forever and every worker went silent. It also ran a DIFFERENT KSG estimator
# (JidtKraskovCMI) from the one the max_lag_sources=20 re-validation was done
# on (OpenCLKraskovCMI) — an estimator inconsistency the paper can't carry.
#
# This revision follows run_campaign.sh (the launcher that completed the
# first-pass + tau5 runs): ONE te_pipeline process, OpenCL KSG on both A100s,
# a live watchdog, and a checkpoint parquet rewritten after EVERY case — a
# crash/hang loses at most the case in flight, and there is no merge step.
#
# Usage (on lams):
#   nohup ./analysis/run_phase4_full.sh > analysis/run-full-gpu.log 2>&1 &
#   # optional arg = intra-case worker count (default 4; KSG jobs are
#   # GPU-latency-bound, more workers buys little):
#   nohup ./analysis/run_phase4_full.sh 4 > analysis/run-full-gpu.log 2>&1 &
#
# Track progress:
#   grep -E 'OK \(|=== \[|case done|TIMEOUT|checkpoint' analysis/run-full-gpu.log | tail
#
# Output: reports/te_table_full.parquet (checkpointed per case, final on exit).
# The first-pass reports/te_table.parquet is left untouched for reproducibility.

set -euo pipefail

WORKERS="${1:-4}"

cd "$(dirname "$0")/.."

# Every case ships the SAME filename (sims/<case>/IEA-15-.../IEA-15-...outb), so
# te_pipeline's stem-based case_id would collapse all 54 cases to one id. Stage
# each .outb as a FOLDER-named symlink first (exactly like run_campaign.sh) so
# the stem becomes the real case id (dlca_v11ms_s00, ...).
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
echo "Workers:     $WORKERS (intra-case, GPU round-robin over 0,1)"
echo "Settings:    FULL (conditional + Granger + AIS + coherence, max_lag=150, max_lag_sources=20, 5 Hz, n_perm=200, slow_drift_tau=5)"
echo ""

mkdir -p reports analysis

# --slow-drift-tau 5: at tau=1 the 4 slow-drift targets go singular in the
#   Gaussian (Granger) estimator => TE=nan (TESettings docstring).
# --max-lag-sources 20: symmetric max_lag=150 nulls real couplings — the greedy
#   max-stat tightens with candidate-pool size and rejected Wave->PtfmHeave
#   (commit 986f867). Re-validation on dlca_v11ms_s00
#   (reports/diag_revalidate.parquet, 2026-07-03, OpenCL estimator): w=20 and
#   w=45 both recover TE=0.067 (p=0.005, lag 6 = 1.2 s); w=30 stochastically
#   nulled. 20 = smallest pool => most sensitive + cheapest; target stays 150.
# --job-timeout 9000: watchdog terminates a hung OpenCL kernel instead of
#   deadlocking the sweep (same setting run_campaign.sh completed with).
python -u analysis/te_pipeline.py "${ALL_OUTB[@]}" \
    -o reports/te_table_full.parquet \
    --graph-out reports/te_full_graph.pkl \
    --gpu --gpus 0,1 --workers "$WORKERS" \
    --n-perm 200 --max-lag 150 --max-lag-sources 20 \
    --decimate-target-hz 5.0 --slow-drift-tau 5 \
    --job-timeout 9000

echo ""
echo "DONE: reports/te_table_full.parquet"
