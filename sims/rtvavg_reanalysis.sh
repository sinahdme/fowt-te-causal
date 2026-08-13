#!/usr/bin/env bash
# rtvavg_reanalysis.sh - re-establish the firewall with the CORRECT wind source.
#
# Wind1VelX (single-point hub) reads ~0 into EVERY structural channel (observability limit).
# RtVAvgxh (rotor-averaged inflow) is the physically-correct source. This campaign recomputes
# wind->structure TE with BOTH sources so the firewall rests on a positive control:
#
#   HEALTHY cases: RtVAvgxh + Wind1VelX -> {PtfmPitch,PtfmSurge,PtfmHeave,RootMyc1}
#     expect  RtVAvgxh->platform ~0            (physical firewall)
#             RtVAvgxh->RootMyc1 non-zero/sig  (positive control: wind reaches the blades)
#             Wind1VelX ~0 everywhere          (point-sensor observability limit)
#   FAULT cases:   RtVAvgxh + Wind1VelX -> PtfmPitch
#     does the firewall hold under fault with the correct wind source?
#
# Validated pilot settings (tau=1, slow-drift-tau 5, max-lag-sources 20, GPU). Resumable
# (skips cases whose parquet already exists). Blade (RootMyc1) jobs are slow (deep embedding);
# expect a few hours total. Run under nohup.
set -uo pipefail
cd "$(dirname "$0")/.."
PY="${PY_TE:-/home/lams/anaconda3/envs/fowt-te-gpu/bin/python}"
DECK=IEA-15-240-RWT-UMaineSemi
COMMON="--no-conditional --no-granger --no-ais --no-coherence --gpu --gpus 0,1 \
        --workers 4 --slow-drift-tau 5 --max-lag-sources 20"

run() {  # <label> <outb> <targets>
  local label="$1" outb="$2" targets="$3"
  local parq="reports/te_rtvavg_${label}.parquet"
  [ -f "$outb" ] || { echo "  SKIP $label: missing $outb"; return; }
  [ -e "$parq" ] && { echo "  SKIP $label: $parq exists"; return; }
  echo "### $label  (targets: $targets)"
  $PY analysis/te_pipeline.py "$outb" -o "$parq" \
      --sources Wind1VelX,RtVAvgxh --targets "$targets" $COMMON \
      2>&1 | grep -E "bivariate_ksg|ERROR|Error|Traceback" || echo "  (no result line)"
}

echo "=== HEALTHY: firewall + positive control (rotor-averaged vs point wind) ==="
for c in dlca_v08ms_s00 dlca_v15ms_s00 dlca_v15ms_s01 dlca_v15ms_s02; do
  run "$c" "sims/$c/$DECK/$DECK.outb" "PtfmPitch,PtfmSurge,PtfmHeave,RootMyc1"
done

echo; echo "=== FAULT: does the firewall hold under fault with the correct wind source? ==="
for f in sims/faults/dlca_v*ms_s*_*.outb; do
  [ -e "$f" ] || continue
  run "$(basename "$f" .outb)" "$f" "PtfmPitch"
done

echo; echo "=== done. Aggregate: $PY analysis/collect_rtvavg.py ==="
