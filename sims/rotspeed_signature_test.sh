#!/usr/bin/env bash
# rotspeed_signature_test.sh - does the pitch-fault signature relocate to the rotor?
#
# The pilot showed wind->platform TE stays 0 under fault (structural firewall), while the
# mechanism check showed rotor-speed variance jumps 1.6-3.5x. This tests whether that shows
# up as DIRECTED information: compute wind->RotSpeed TE (and wind->PtfmPitch as the firewall
# reference) for a healthy arm and its faulted twin, at the same validated settings as the
# pilot (tau=1, --slow-drift-tau 5, --max-lag-sources 20, GPU).
#
# Prediction: wind->PtfmPitch ~0 in BOTH (firewall). wind->RotSpeed low healthy (controller
# regulates rotor speed against wind above rated), RISES under fault (unregulated rotor tracks
# the wind) -> the fault signature lives in the rotor-speed channel.
set -uo pipefail
cd "$(dirname "$0")/.."
PY="${PY_TE:-/home/lams/anaconda3/envs/fowt-te-gpu/bin/python}"
DECK=IEA-15-240-RWT-UMaineSemi
COMMON="--sources Wind1VelX --targets RotSpeed,PtfmPitch --no-conditional --no-granger \
        --no-ais --no-coherence --gpu --gpus 0,1 --workers 4 --slow-drift-tau 5 --max-lag-sources 20"

echo "==================================================================="
echo " wind->RotSpeed signature test (healthy vs faulted twin)"
echo "==================================================================="
echo; echo "### HEALTHY: dlca_v15ms_s00"
$PY analysis/te_pipeline.py "sims/dlca_v15ms_s00/$DECK/$DECK.outb" \
    -o reports/te_rotspeed_healthy.parquet $COMMON 2>&1 \
    | grep -E "bivariate_ksg|ERROR|Error|Traceback" || echo "  (no result line - check reports/te_rotspeed_healthy.parquet)"

echo; echo "### FAULT: dlca_v15ms_s00_pitchlock"
$PY analysis/te_pipeline.py sims/faults/dlca_v15ms_s00_pitchlock.outb \
    -o reports/te_rotspeed_fault.parquet $COMMON 2>&1 \
    | grep -E "bivariate_ksg|ERROR|Error|Traceback" || echo "  (no result line - check reports/te_rotspeed_fault.parquet)"

echo; echo "==================================================================="
echo " Read: wind->PtfmPitch should be ~0 in both (firewall holds)."
echo " wind->RotSpeed low/healthy but HIGHER + significant under fault => the pitch-fault"
echo " signature relocates to rotor speed (a viable monitor), while the platform stays shielded."
echo "==================================================================="
