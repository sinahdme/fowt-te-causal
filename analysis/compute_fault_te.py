#!/usr/bin/env python3
"""Compute wind->platform transfer entropy for the ONE pending pitch-fault case
(the pitch-lock / open-loop twin) on CPU, then test it against the healthy
firewall baseline.

WHY THIS EXISTS
---------------
Stage-3 peer review (reports/te-firewall-review-round1.md) flagged that the
manuscript's monitoring claim has no computed fault-case TE: the pitch-lock /
open-loop case (`dlca_v11ms_s00_openloop`) is recorded as "pending TE legs" in
reports/monitor_signature.parquet. This script computes exactly those legs.

It closes TWO open items at once (roadmap #1 and #3):
  * monitoring hypothesis (paper 4.4): does a pitch fault lift wind->platform TE
    above the healthy ceiling (~0.029 nats) AND above the chance floor?
  * attribution converse (paper 4.3): does wind information reappear in the
    platform channel once the control loop is opened?

CPU-ONLY BY DESIGN
------------------
This wraps analysis/te_pipeline.py WITHOUT the --gpu flag, so it uses the
JidtKraskovCMI (JVM/CPU) backend. It will NOT contend for the GPUs running the
long Phase-4 campaign. It is a minutes-to-hours single-case job. Do not add
--gpu.

REPRODUCIBILITY CAVEAT
----------------------
For the fault TE to be comparable to the authoritative healthy te_table
(reports/te_table.parquet), the estimator flags below MUST match those used to
generate that table. The defaults here mirror analysis/te_pipeline.py's
documented settings (5 Hz, transient drop 600 s, max_lag 150, n_perm 200,
tau 1 with slow_drift_tau 5 on the slow platform channels). If the healthy
table was built with different flags, pass the matching ones and update the
constants below. Verify provenance before trusting the verdict.

USAGE
-----
    # dry run: print the exact pipeline command, compute nothing
    python analysis/compute_fault_te.py --dry-run

    # real run (CPU): compute and evaluate
    python analysis/compute_fault_te.py --outb openloop.outb

    # only re-evaluate an already-computed fault parquet
    python analysis/compute_fault_te.py --eval-only reports/te_fault_openloop.parquet
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd

# --- healthy firewall baseline (from reports/te_table.parquet, 42 healthy cases) ---
HEALTHY_CEILING_NATS = 0.029      # max wind->PtfmPitch TE over the healthy population
N_HEALTHY_CASES = 54              # campaign size used for the chance-floor comparison
ALPHA = 0.05                      # permutation-test significance level
PLATFORM_TARGETS = ("PtfmPitch", "PtfmSurge", "PtfmHeave")
SLOW_DRIFT_TARGETS = "PtfmPitch,PtfmHeave,PtfmSurge,RootMxc1"

REPO = Path(__file__).resolve().parents[1]
PIPELINE = REPO / "analysis" / "te_pipeline.py"


def build_pipeline_cmd(outb: Path, out_parquet: Path) -> list[str]:
    """Exact CPU invocation of te_pipeline.py for the fault case.

    NOTE: no --gpu flag => JidtKraskovCMI (CPU). Flags mirror te_pipeline.py
    documented defaults; keep in sync with the healthy-table provenance.
    """
    return [
        sys.executable, str(PIPELINE), str(outb),
        "-o", str(out_parquet),
        "--decimate-target-hz", "5.0",
        "--transient-drop-s", "600.0",
        "--max-lag", "150",
        "--n-perm", "200",
        "--tau", "1",
        "--slow-drift-tau", "5",
        "--slow-drift-targets", SLOW_DRIFT_TARGETS,
        # deliberately NO --gpu : CPU backend, will not touch the A100 campaign
    ]


def evaluate(fault_parquet: Path) -> int:
    """Compare wind->platform TE in the fault case against the healthy firewall."""
    df = pd.read_parquet(fault_parquet)
    ksg = df[df.method == "bivariate_te_ksg"]
    wind = ksg[ksg.source == "Wind1VelX"]

    expected_chance = round(ALPHA * N_HEALTHY_CASES, 1)
    print(f"\n=== Fault-case wind->platform TE vs healthy firewall ===")
    print(f"healthy ceiling         : {HEALTHY_CEILING_NATS} nats "
          f"(max wind->PtfmPitch over healthy pop.)")
    print(f"chance floor (alpha=0.05): ~{expected_chance} significant of {N_HEALTHY_CASES} by chance\n")

    breach = False
    for tgt in PLATFORM_TARGETS:
        d = wind[wind.target == tgt]
        if d.empty:
            print(f"  {tgt:10s}: (no row — check channel mapping)")
            continue
        te = float(d.te_nats.mean())
        sig = bool((d.significant == True).any())
        over = te > HEALTHY_CEILING_NATS
        breach = breach or (over and sig)
        flag = "  <-- BREACH" if (over and sig) else ""
        print(f"  Wind->{tgt:10s}: TE={te:.4f} nats  significant={sig}"
              f"  above_ceiling={over}{flag}")

    print("\nVERDICT:", "FIREWALL BREACHED -- wind reaches the platform under fault "
          "(monitoring hypothesis supported)." if breach else
          "No breach demonstrated -- fault-case wind->platform TE does not clear "
          "the healthy ceiling. Monitoring claim stays an outlook.")
    print("\nNext: if breached, upgrade paper §4.4 from outlook to proof-of-concept "
          "and re-run Stage 3' re-review.")
    return 0 if breach else 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outb", type=Path, default=REPO / "openloop.outb",
                    help="OpenFAST output for the pitch-lock/open-loop fault case")
    ap.add_argument("-o", "--out", type=Path,
                    default=REPO / "reports" / "te_fault_openloop.parquet",
                    help="Where to write the fault TE table")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the pipeline command and exit (compute nothing)")
    ap.add_argument("--eval-only", type=Path, default=None,
                    help="Skip computation; just evaluate this existing fault parquet")
    args = ap.parse_args()

    if args.eval_only:
        return evaluate(args.eval_only)

    cmd = build_pipeline_cmd(args.outb, args.out)
    print("CPU fault-TE command (no GPU -- will not touch the campaign):\n  "
          + " ".join(cmd))
    if args.dry_run:
        return 0

    if not args.outb.exists():
        print(f"\nERROR: fault .outb not found: {args.outb}\n"
              "Point --outb at the pitch-lock/open-loop OpenFAST output.",
              file=sys.stderr)
        return 1

    print("\nRunning te_pipeline.py on CPU ...")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("Pipeline failed; not evaluating.", file=sys.stderr)
        return r.returncode
    return evaluate(args.out)


if __name__ == "__main__":
    raise SystemExit(main())
