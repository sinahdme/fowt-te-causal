#!/usr/bin/env bash
# run_fault_pilot.sh - graded pitch-fault PILOT on the GPU server (lams, env fowt-te-gpu).
#
# Tests the paper's 3.4 monitoring hypothesis: does a pitch fault lift wind->platform
# transfer entropy above the healthy firewall ceiling (~0.029 nats)?  See the approved plan
# (~/.claude/plans/fluffy-forging-trinket.md) and sims/run_fault.py.
#
# PILOT (9 runs): above-rated pitch-lock + one graded gain-reduction arm.
#   pitchlock @15 m/s  x {s00,s01,s02}
#   pitchlock @20 m/s  x {s00,s01,s02}
#   gain x0.10 @15 m/s x {s00,s01,s02}
#
# PREREQUISITES on lams:
#   - Healthy base cases staged with wind.bts:  sims/dlca_v15ms_s0{0,1,2}  sims/dlca_v20ms_s0{0,1,2}
#     (each with its own IEA-15-240-RWT-UMaineSemi/*.outb from the healthy campaign - run_fault.py
#      reads the healthy operating pitch from it for the lock angle).
#   - conda env fowt-te-gpu active (idtxl + OpenCL KSG), and `openfast` on PATH (or set OPENFAST_EXE).
#   - Provenance: this uses --gpu for the fault TE. If the authoritative healthy te_table.parquet
#     was CPU-built, drop --gpu below to match its estimator backend (KSG results are close either
#     way; the significance-gated breach test is robust, but keep them consistent).
#
# OpenFAST is CPU-bound (one thread/run); the A100s only accelerate the TE step.
set -uo pipefail
cd "$(dirname "$0")/.."                          # repo root

# lams has TWO envs: fowt-openfast runs OpenFAST + reads .outb (openfast_toolbox);
# fowt-te-gpu runs the TE pipeline (idtxl + OpenCL). Override PY_SIM/PY_TE if paths differ.
PY_SIM="${PY_SIM:-/home/lams/anaconda3/envs/fowt-openfast/bin/python}"   # Phase 1: inject + OpenFAST
PY_TE="${PY_TE:-/home/lams/anaconda3/envs/fowt-te-gpu/bin/python}"       # Phase 2: TE (GPU)
OPENFAST_EXE="${OPENFAST_EXE:-openfast}"          # set if `openfast` is not on PATH in fowt-openfast
GPUS="${GPUS:-0,1}"
WORKERS="${WORKERS:-4}"
MAXJOBS="${MAXJOBS:-6}"                           # concurrent OpenFAST runs (CPU)
FAULTS_DIR="sims/faults"
REPORTS="reports"

# arm: "<base_case>  <run_fault.py extra args>  <tag>"
ARMS=(
  "dlca_v15ms_s00|--fault pitchlock|pitchlock"
  "dlca_v15ms_s01|--fault pitchlock|pitchlock"
  "dlca_v15ms_s02|--fault pitchlock|pitchlock"
  "dlca_v20ms_s00|--fault pitchlock|pitchlock"
  "dlca_v20ms_s01|--fault pitchlock|pitchlock"
  "dlca_v20ms_s02|--fault pitchlock|pitchlock"
  "dlca_v15ms_s00|--fault gain --severity 0.10|gain010"
  "dlca_v15ms_s01|--fault gain --severity 0.10|gain010"
  "dlca_v15ms_s02|--fault gain --severity 0.10|gain010"
)

echo "==================================================================="
echo " Pitch-fault PILOT : ${#ARMS[@]} runs   GPUS=$GPUS  MAXJOBS=$MAXJOBS"
echo " PY_SIM=$PY_SIM"
echo " PY_TE =$PY_TE"
echo "==================================================================="

# ---------- Phase 1: inject + run OpenFAST (CPU, parallel with a cap) ----------
echo; echo "### Phase 1 - inject faults + run OpenFAST (CPU)"
pids=()
for arm in "${ARMS[@]}"; do
  IFS='|' read -r base extra tag <<< "$arm"
  bc="sims/${base}"
  if [[ ! -f "${bc}/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.fst" ]]; then
    echo "  SKIP ${base}_${tag}: base case not staged ($bc)"; continue
  fi
  if [[ -e "${FAULTS_DIR}/${base}_${tag}.outb" ]]; then
    echo "  SKIP ${base}_${tag}: already done (${FAULTS_DIR}/${base}_${tag}.outb exists)"; continue
  fi
  # throttle to MAXJOBS
  while (( $(jobs -rp | wc -l) >= MAXJOBS )); do wait -n; done
  echo "  launch ${base}_${tag}"
  ( $PY_SIM sims/run_fault.py "$bc" $extra --tag "$tag" --openfast-exe "$OPENFAST_EXE" \
        > "sims/fault_${base}_${tag}.log" 2>&1 ) &
  pids+=($!)
done
fail=0
for p in "${pids[@]}"; do wait "$p" || { echo "  !! a fault run failed (pid $p)"; fail=1; }; done
echo "### Phase 1 done (fail=$fail). Per-run logs: sims/fault_*.log"

# ---------- Phase 2: TE on GPU + breach verdict per arm ----------
echo; echo "### Phase 2 - wind->platform TE (GPU) + breach test vs 0.029-nat ceiling"
mkdir -p "$REPORTS"
for arm in "${ARMS[@]}"; do
  IFS='|' read -r base extra tag <<< "$arm"
  outb="${FAULTS_DIR}/${base}_${tag}.outb"
  parq="${REPORTS}/te_fault_${base}_${tag}.parquet"
  [[ -f "$outb" ]] || { echo "  SKIP ${base}_${tag}: no faulted .outb"; continue; }
  echo; echo "  --- ${base}_${tag} ---"
  # GPU (A100 OpenCL) + bivariate-only: the breach verdict only needs the bivariate
  # wind->platform TE. --slow-drift-tau 5 is required (default 0 hangs PtfmPitch at
  # tau=1). REQUIRES ecos+prettytable in fowt-te-gpu (undeclared IDTxl deps) -
  # without them the OpenCL import chain hangs. Install once: pip install ecos prettytable.
  $PY_TE analysis/te_pipeline.py "$outb" -o "$parq" \
      --gpu --gpus "$GPUS" --workers "$WORKERS" \
      --sources Wind1VelX --targets PtfmPitch,PtfmSurge,PtfmHeave \
      --no-conditional --no-granger --no-ais --no-coherence \
      --n-perm 200 --tau 1 --slow-drift-tau 5 \
      --slow-drift-targets PtfmPitch,PtfmHeave,PtfmSurge,RootMxc1 \
      || { echo "  !! TE pipeline failed for ${base}_${tag}"; continue; }
  $PY_TE analysis/compute_fault_te.py --eval-only "$parq"   # prints VERDICT (rc 0=breach, 2=no breach)
done

# ---------- Phase 3: aggregate summary table + plot ----------
echo; echo "### Phase 3 - aggregate summary (CSV + plot)"
$PY_TE analysis/collect_fault_pilot.py \
  || echo "  (collector skipped/failed - run: $PY_TE analysis/collect_fault_pilot.py)"

echo; echo "==================================================================="
echo " PILOT COMPLETE. Per-arm TE tables: ${REPORTS}/te_fault_dlca_v*.parquet"
echo " Summary: ${REPORTS}/fault_pilot_summary.csv  +  ${REPORTS}/figs/fault_pilot.png"
echo " A breach = mean Wind->{PtfmPitch,Surge,Heave} TE > 0.029 nats AND significant."
echo " If lock/gain @ above-rated breaches -> expand to the full 4.3 ROC campaign."
echo " If null -> the firewall is robust/structural; report the null (no paper edits till then)."
echo "==================================================================="
