#!/usr/bin/env bash
# rotoravg_wind_test.sh - THE decisive test for the firewall interpretation.
#
# Is wind->structure TE ~0 because of a physical firewall, or because the single-point hub
# anemometer (Wind1VelX) is decorrelated from the rotor-averaged inflow that actually drives
# the machine? Compare BOTH wind sources -> RootMyc1 (blade root, directly wind-loaded) and
# PtfmPitch (platform), on a healthy case, at the validated pilot settings.
#
#   RtVAvgxh FIRES (esp. -> RootMyc1) while Wind1VelX ~0
#       => point-wind OBSERVABILITY limit; the rotor spatially filters the point wind, but the
#          coupling is real and observable with the right (rotor-averaged) sensor. Potentially
#          rescues a positive monitoring result and reframes the firewall precisely.
#   RtVAvgxh ALSO ~0
#       => genuine PHYSICAL firewall: even the correct wind input carries no info into the
#          structure. Strong physical claim, defensible as-is.
set -uo pipefail
cd "$(dirname "$0")/.."
PY="${PY_TE:-/home/lams/anaconda3/envs/fowt-te-gpu/bin/python}"
DECK=IEA-15-240-RWT-UMaineSemi
CASE="${1:-dlca_v15ms_s00}"
OUTB="sims/$CASE/$DECK/$DECK.outb"

echo "### rotor-averaged (RtVAvgxh) vs point (Wind1VelX) wind -> structure : $CASE"
[ -f "$OUTB" ] || { echo "  MISSING $OUTB"; exit 1; }
$PY analysis/te_pipeline.py "$OUTB" -o "reports/te_rotoravg_${CASE}.parquet" \
    --sources Wind1VelX,RtVAvgxh --targets RootMyc1,PtfmPitch --no-conditional --no-granger \
    --no-ais --no-coherence --gpu --gpus 0,1 --workers 4 --slow-drift-tau 5 --max-lag-sources 20 \
    2>&1 | grep -E "bivariate_ksg|ERROR|Error|Traceback" \
  || echo "  (no result line - check reports/te_rotoravg_${CASE}.parquet)"
echo "### CRUX: RtVAvgxh -> RootMyc1  vs  Wind1VelX -> RootMyc1."
echo "###   rotor-avg fires, point ~0  => observability firewall (point sensor is the limit)."
echo "###   both ~0                    => physical firewall."
