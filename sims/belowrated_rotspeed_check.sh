#!/usr/bin/env bash
# belowrated_rotspeed_check.sh - the load-bearing sensitivity control.
#
# Above rated (and under fault) wind->RotSpeed TE came back 0. Is that physics (a point-wind
# hub measurement can't predict the rotor-averaged response) or an insensitive estimator?
# Below rated (region 2, ~8 m/s) the controller tracks optimal TSR, so rotor speed DOES follow
# the wind -> wind->RotSpeed MUST be non-zero + significant if the estimator can see it.
#
#   Non-zero here  -> estimator is sensitive; the above-rated/fault zeros are REAL (point-wind
#                     spatial decorrelation) -> the negative monitoring result is defensible.
#   Zero here too  -> a sensitivity problem to fix before concluding anything.
#
# Same validated settings as the pilot (tau=1, slow-drift-tau 5, max-lag-sources 20, GPU).
set -uo pipefail
cd "$(dirname "$0")/.."
PY="${PY_TE:-/home/lams/anaconda3/envs/fowt-te-gpu/bin/python}"
DECK=IEA-15-240-RWT-UMaineSemi
CASE="${1:-dlca_v08ms_s00}"
OUTB="sims/$CASE/$DECK/$DECK.outb"

echo "### below-rated control: $CASE  (rotor should track wind here)"
[ -f "$OUTB" ] || { echo "  MISSING $OUTB - pick a staged below-rated case (ls sims/ | grep v08ms)"; exit 1; }
$PY analysis/te_pipeline.py "$OUTB" -o "reports/te_rotspeed_${CASE}.parquet" \
    --sources Wind1VelX --targets RotSpeed,PtfmPitch --no-conditional --no-granger \
    --no-ais --no-coherence --gpu --gpus 0,1 --workers 4 --slow-drift-tau 5 --max-lag-sources 20 \
    2>&1 | grep -E "bivariate_ksg|ERROR|Error|Traceback" \
  || echo "  (no result line - check reports/te_rotspeed_${CASE}.parquet)"
echo "### EXPECT: Wind1VelX -> RotSpeed NON-ZERO + significant (validates sensitivity)."
echo "###         Wind1VelX -> PtfmPitch ~0 even below rated (firewall / point-wind decorrelation)."
