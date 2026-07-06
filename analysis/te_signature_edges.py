#!/usr/bin/env python
"""Compute the TE edges the signature table needs but the campaign tables lack.

The fault-detection signature (surd/monitor_signature.py) is two-sided:

    healthy pitch control  <=>  TE(wind -> structure) ~ 0
                                AND TE(wind -> BldPitch1) >> 0

The first-pass reports/te_table.parquet has the structure legs (9 responses)
but BldPitch1 was never a TE target, and the open-loop twin
(dlca_v11ms_s00_openloop) was never TE'd at all (SURD only). This script
computes exactly those missing edges on existing .outb files - no new
simulations.

Settings intentionally mirror the FIRST PASS (2 Hz, max_lag 60, n_perm 50,
tau 1, symmetric source window) so the new legs are comparable with the
te_table.parquet numbers they sit next to. Estimator caveat: the first pass
ran OpenCLKraskovCMI on the GPUs (busy with the Phase 4 full campaign);
this runs JidtKraskovCMI on CPU. Fine for the >>0-vs-0 contrast the
signature needs; the estimator is recorded per row.

Usage (CPU server, env fowt-te):
  python analysis/te_signature_edges.py \
      sims/*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb \
      -o reports/te_signature_edges.parquet --workers 16
  # open-loop twin (server-only case) is picked up by the same glob there.

Per-case checkpointing: the output parquet is rewritten after every case, so
an interruption loses at most the case in flight.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from te_pipeline import TESettings, per_case_pipeline  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("-o", "--output", type=Path,
                    default=Path("reports/te_signature_edges.parquet"))
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--sources", type=str, default="Wind1VelX")
    ap.add_argument("--responses", type=str, default="BldPitch1,PtfmPitch")
    args = ap.parse_args()

    settings = TESettings(
        decimate_target_hz=2.0,     # first-pass parity
        max_lag=60,                 # first-pass parity
        n_perm=50,                  # first-pass parity
        tau=1,
        max_lag_sources=0,          # symmetric window, first-pass behaviour
        ksg_estimator="JidtKraskovCMI",   # CPU (GPUs busy; recorded per row)
        n_workers=args.workers,
        env_sources=tuple(s.strip() for s in args.sources.split(",")),
        responses=tuple(r.strip() for r in args.responses.split(",")),
    )

    dfs: list[pd.DataFrame] = []
    t0 = time.time()
    for i, inp in enumerate(sorted(args.inputs), 1):
        # folder-named case id (every campaign .outb shares the same filename)
        case_id = inp.parent.parent.name if inp.parent.name.startswith("IEA-15") \
            else inp.stem
        print(f"\n=== [{i}/{len(args.inputs)}] {case_id} ===", flush=True)
        try:
            df = per_case_pipeline(
                inp, settings, case_id=case_id,
                do_conditional=False, do_granger=False,
                do_coherence=False, do_ais=True,   # AIS needed for te_frac
            )
        except Exception as e:
            print(f"!! {case_id} raised {type(e).__name__}: {e}",
                  file=sys.stderr, flush=True)
            continue
        df["estimator"] = settings.ksg_estimator
        dfs.append(df)
        full = pd.concat(dfs, ignore_index=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        full.to_parquet(args.output, index=False)
        print(f"  [checkpoint] {args.output.name}: {len(full)} rows "
              f"({time.time()-t0:.0f}s elapsed)", flush=True)

    if not dfs:
        print("No cases produced results.")
        return 1
    print(f"\nWrote {args.output} ({sum(len(d) for d in dfs)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
