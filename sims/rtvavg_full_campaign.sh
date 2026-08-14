#!/usr/bin/env bash
# rtvavg_full_campaign.sh - the corrected wind->structure campaign for the paper.
#
# Recompute the wind->structure edges with the physically-correct rotor-averaged wind (RtVAvgxh)
# across ALL staged healthy cases, at the SAME settings as te_table_full (tau=1, slow-drift-tau 5,
# max-lag-sources 20, GPU). Wind1VelX (point) and Wave1Elev are already in te_table_full at these
# settings, so we only add RtVAvgxh here and merge later.
#
# Expected: RtVAvgxh -> platform ~0 (firewall), RtVAvgxh -> blade/tower non-zero (wind reaches the
# rotor), surge marginal. RESUMABLE (skips cases whose parquet exists). The blade/tower jobs
# deep-embed (~30 min each), so the full 54-case run is ~1-2 DAYS of GPU time. Run under nohup.
#
# Scope knobs (env):  TARGETS=... (default all 9)   CASE_GLOB=... (default all dlc*_v*ms_s##)
set -uo pipefail
cd "$(dirname "$0")/.."
PY="${PY_TE:-/home/lams/anaconda3/envs/fowt-te-gpu/bin/python}"
DECK=IEA-15-240-RWT-UMaineSemi
TARGETS="${TARGETS:-RootMyc1,RootMxc1,TwrBsMyt,PtfmHeave,PtfmSurge,PtfmPitch,FAIRTEN1,FAIRTEN2,FAIRTEN3}"
COMMON="--no-conditional --no-granger --no-ais --no-coherence --gpu --gpus 0,1 \
        --workers 4 --slow-drift-tau 5 --max-lag-sources 20"

# staged HEALTHY cases only: dlc<x>_v<NN>ms_s<NN> with no fault/openloop suffix
mapfile -t CASES < <(cd sims && ls -d dlc*_v*ms_s[0-9][0-9] 2>/dev/null \
                     | grep -E '^dlc[a-z0-9]+_v[0-9]+ms_s[0-9]+$')
echo "=== RtVAvgxh full campaign: ${#CASES[@]} healthy cases x targets: $TARGETS ==="
done=0
for c in "${CASES[@]}"; do
  outb="sims/$c/$DECK/$DECK.outb"; parq="reports/te_wsrc_${c}.parquet"
  [ -f "$outb" ] || { echo "  SKIP $c: missing outb"; continue; }
  [ -e "$parq" ] && { echo "  SKIP $c: done"; continue; }
  echo "### $c  ($((++done)) started)"
  $PY analysis/te_pipeline.py "$outb" -o "$parq" \
      --sources RtVAvgxh --targets "$TARGETS" $COMMON \
      2>&1 | grep -E "bivariate_ksg|ERROR|Error|Traceback" | tail -12 || echo "  (no result)"
done
echo "=== done ($done newly computed). Aggregate: $PY analysis/collect_wind_struct.py ==="
