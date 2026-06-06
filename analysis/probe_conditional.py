"""probe_conditional.py — fast isolation test for the conditional/multivariate
TE path on the GPU (OpenCL) estimator.

The bivariate GPU path is validated; the conditional path
(`run_multivariate_te` -> IDTxl MultivariateTE) runs extra machinery
(multivariate omnibus + multivariate sequential max-stat) that could hide
another numpy-2 estimate-shape bug like the ones already patched for bivariate.
This runs ONE conditional TE on a known-coupled triple at small settings so any
such bug surfaces in ~1-3 min instead of mid-sweep.

Triple: TE(Wave1Elev -> PtfmPitch | Wind1VelX) — wave->pitch is the strongest
coupling, so a source lag is selected and the final-stats path is exercised.

Usage:
    python analysis/probe_conditional.py sims/.../run.outb [--max-lag 30] [--n-perm 50] [--cpu]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
from te_pipeline import (  # noqa: E402
    TESettings, find_channel, preprocess_channel, run_multivariate_te,
)
from load_runs import load_outb, find_time_column  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("--source", default="Wave1Elev")
    ap.add_argument("--target", default="PtfmPitch")
    ap.add_argument("--conditional", default="Wind1VelX")
    ap.add_argument("--max-lag", type=int, default=30)
    ap.add_argument("--n-perm", type=int, default=50)
    ap.add_argument("--decimate-target-hz", type=float, default=5.0)
    ap.add_argument("--gpuid", type=int, default=0)
    ap.add_argument("--cpu", action="store_true",
                    help="Use JidtKraskovCMI (CPU) instead of OpenCL, e.g. to "
                         "get a reference value to compare the GPU result to.")
    args = ap.parse_args()

    settings = TESettings(
        decimate_target_hz=args.decimate_target_hz,
        max_lag=args.max_lag,
        n_perm=args.n_perm,
        ksg_estimator="JidtKraskovCMI" if args.cpu else "OpenCLKraskovCMI",
        gpuid=args.gpuid,
    )

    df = load_outb(args.input)
    dt = float(np.median(np.diff(df[find_time_column(df)].to_numpy())))
    arrs = {}
    for i, name in enumerate((args.source, args.target, args.conditional)):
        clean, _ = preprocess_channel(df[find_channel(df, name)].to_numpy(),
                                      dt, settings, seed=i)
        arrs[name] = clean

    print(f"\nTE({args.source} -> {args.target} | {args.conditional})  "
          f"[{settings.ksg_estimator}, max_lag={args.max_lag}, "
          f"n_perm={args.n_perm}, N={len(arrs[args.source])}]\n", flush=True)

    import time
    t0 = time.time()
    r = run_multivariate_te(arrs[args.source], arrs[args.target],
                            arrs[args.conditional], settings)
    dt_run = time.time() - t0

    print(f"\n=== conditional TE result ({dt_run:.0f}s) ===")
    for k, v in r.items():
        print(f"  {k:28s} {v}")
    print("\nOK — conditional/multivariate GPU path ran without error.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
