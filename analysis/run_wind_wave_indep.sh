#!/usr/bin/env bash
# run_wind_wave_indep.sh — wind/wave forcing independence check over ALL runs.
#
# Completes the coverage started on the Windows workstation, which could only
# reach 8 of the 54 runs (the 6x 11 m/s seeds + one 8 m/s + the open-loop twin,
# all INDEPENDENT). The 15 m/s and 20 m/s bins live only here on the server;
# this closes open-question Q6 for the full campaign.
#
# What it does: for each run, after the pipeline's exact preprocessing (drop
# 600 s transient, decimate 5 Hz, jitter), it reports lag-0 Pearson r, max
# |cross-correlation| over +/-30 s, histogram mutual information, and a
# circular-shift surrogate MI null (the correct, autocorrelation-preserving
# null — see wind_wave_indep_all.py header). A run is INDEPENDENT when
# |xcorr| < 0.1 AND the MI surrogate p >= 0.05.
#
# CPU-only: needs only numpy + the .outb reader, NOT IDTxl/GPU. Runs anywhere
# the fowt-te env is active; it does not touch the running te_pipeline campaign.
#
# Usage (on the server, with the fowt-te env active):
#   conda activate fowt-te     # or: source activate fowt-te
#   ./analysis/run_wind_wave_indep.sh
#
# Override which runs via the CASES glob (default = all 54 campaign runs):
#   CASES="sims/dlc16_v15ms_s* sims/dlc16_v20ms_s*" ./analysis/run_wind_wave_indep.sh
#
# Output: reports/wind_wave_independence.parquet (one row per run) + a printed
# table. Pull it back with pull-results.sh and fold the 15/20 m/s rows into
# reports/wind-wave-independence.md.

set -euo pipefail

cd "$(dirname "$0")/.."

# Default: every campaign .outb (all share one filename inside per-case folders;
# the aggregator derives the case id from the sims/<case> path, so no staging
# symlinks are needed here). Root-level below-rated / open-loop runs are added
# if present so the parquet is a complete record.
CASES="${CASES:-sims/*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb}"

shopt -s nullglob
FILES=( $CASES )
# Also sweep in any root-level FOWT runs (dlca_*/dlcb_*/openloop) when using the
# default glob, so all locally-checked runs are re-confirmed in one table.
if [ "$CASES" = "sims/*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb" ]; then
    FILES+=( dlca_*.outb dlcb_*.outb openloop.outb )
fi

if [ "${#FILES[@]}" -lt 1 ]; then
    echo "ERROR: no .outb files matched CASES='$CASES'. Run Phase 2 first, or" >&2
    echo "       set CASES to an existing sims/ glob." >&2
    exit 1
fi

echo "[wind-wave-indep] $(date)"
echo "  runs to check: ${#FILES[@]}"
echo "  settings: decimate 5 Hz, transient drop 600 s, xcorr +/-150 samp (30 s),"
echo "            32-bin MI, 200 circular-shift surrogates"
echo ""

python -u analysis/wind_wave_indep_all.py "${FILES[@]}" \
    -o reports/wind_wave_independence.parquet \
    --decimate-target-hz 5.0 --transient-drop-s 600 \
    --max-lag 150 --bins 32 --n-surrogate 200

echo ""
echo "DONE: reports/wind_wave_independence.parquet"
