#!/usr/bin/env python
"""Phase 0 validation gate for the SURD subproject (surd/PLAN.md).

Reproduces the mediator system Q3 -> Q2 -> Q1 from the SURD paper
(Martinez-Sanchez, Arranz & Lozano-Duran, Nat. Commun. 15, 9296, 2024,
Fig. 2 / examples/E02_building_blocks.ipynb) with the vendored reference
implementation, and asserts the qualitative R/U/S + leak signature:

  target Q1 : U2 dominant, R23 present, U3 ~ 0   (Q3 reaches Q1 only through
              the mediator Q2, so its influence must show up as redundancy
              with Q2, never as unique causality)
  target Q2 : U3 dominant
  target Q3 : U3 (self) dominant, leak > leak(Q1) (Q3 is the noise-driven end
              of the chain; Q1 is nearly deterministic given Q2)

Exit code 0 = all checks pass (gate open for Phase 1), 1 = any failure.

Defaults are scaled down from the paper (Nt=5e7, nbins=50) to run on a
laptop in minutes while keeping N_samples >> nbins^4; use --nt 50000000
--nbins 50 to replicate the notebook exactly (needs ~8 GB and a while).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import types
from pathlib import Path

import numpy as np

VENDOR = Path(__file__).resolve().parent / "vendor" / "SURD" / "utils"
sys.path.insert(0, str(VENDOR))

# The vendored surd.py imports pymp (fork-based, POSIX-only) at module level
# but only uses it in run_parallel(), which we never call. Stub it so the
# module imports on Windows without touching vendor code.
if "pymp" not in sys.modules:
    _pymp = types.ModuleType("pymp")
    _pymp.shared = types.SimpleNamespace(dict=dict)
    sys.modules["pymp"] = _pymp

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import analytic_eqs as cases  # noqa: E402  (vendor, needs sys.path above)
import surd as surd_mod  # noqa: E402


def decompose(X: np.ndarray, target: int, nlag: int, nbins: int):
    """Mirror surd.run() for one target: agents = all vars at time n,
    target = var `target` at time n+nlag. Returns (I_R, I_S, MI, leak)."""
    Y = np.vstack([X[target, nlag:], X[:, :-nlag]])
    hist, _ = np.histogramdd(Y.T, nbins)
    return surd_mod.surd(hist)


def norm(d: dict, mi: dict) -> dict:
    """nice_print()'s normalization: fraction of the largest MI."""
    mmax = max(mi.values())
    return {k: v / mmax for k, v in d.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--nt", type=int, default=20_000_000,
                    help="integration steps (paper: 5e7)")
    ap.add_argument("--nbins", type=int, default=32,
                    help="histogram bins per dim (paper: 50)")
    ap.add_argument("--nlag", type=int, default=1)
    ap.add_argument("--transient", type=int, default=10_000,
                    help="leading samples dropped (paper: 10000)")
    ap.add_argument("-o", "--out", type=Path,
                    default=Path(__file__).parent / "validation_mediator")
    args = ap.parse_args()

    if args.nt - args.transient < args.nbins ** 4 * 5:
        print(f"WARNING: only {args.nt - args.transient:.2e} samples for a "
              f"{args.nbins}^4 = {args.nbins**4:.2e}-bin joint histogram; "
              "R/U/S estimates will be noisy.", file=sys.stderr)

    t0 = time.time()
    print(f"[mediator] integrating {args.nt:.1e} steps "
          f"(vendor analytic_eqs.mediator, seed 10) ...", flush=True)
    qs = cases.mediator(args.nt)
    X = np.array([q[args.transient:] for q in qs])
    print(f"[mediator] done in {time.time()-t0:.0f}s, "
          f"{X.shape[1]:.1e} samples x {X.shape[0]} vars", flush=True)

    results, failures = {}, []

    def check(cond: bool, msg: str) -> None:
        print(f"  {'PASS' if cond else 'FAIL'}  {msg}", flush=True)
        if not cond:
            failures.append(msg)

    fig, axs = plt.subplots(3, 2, figsize=(9, 7),
                            gridspec_kw={"width_ratios": [35, 1]})

    for tgt in range(3):
        I_R, I_S, MI, leak = decompose(X, tgt, args.nlag, args.nbins)
        R, S = norm(I_R, MI), norm(I_S, MI)
        results[f"Q{tgt+1}"] = {
            "R": {str(k): v for k, v in R.items()},
            "S": {str(k): v for k, v in S.items()},
            "leak": leak,
        }
        print(f"\nSURD for target Q{tgt+1} (normalized, leak={leak:.3f}):",
              flush=True)
        surd_mod.nice_print(I_R, I_S, MI, leak)
        surd_mod.plot(I_R, I_S, leak, axs[tgt, :], 3, threshold=0.01)
        axs[tgt, 0].set_ylabel(f"target $Q_{tgt+1}$")

    fig.suptitle(f"SURD mediator validation - Nt={args.nt:.0e}, "
                 f"nbins={args.nbins}, nlag={args.nlag}")
    fig.tight_layout()
    fig.savefig(args.out.with_suffix(".png"), dpi=150)

    # ---- the gate: qualitative Fig. 2 signature ---------------------------
    print("\n=== validation checks ===", flush=True)
    q1R, q1S = results["Q1"]["R"], results["Q1"]["S"]
    q2R, q3R = results["Q2"]["R"], results["Q3"]["R"]
    u = lambda d, i: d.get(f"({i},)", 0.0)

    all1 = {**q1R, **q1S}
    top1 = max(all1, key=all1.get)
    check(top1 == "(2,)", f"Q1: dominant term is U2 (got {top1})")
    check(u(q1R, 3) < 0.05,
          f"Q1: unique Q3 ~ 0, mediation not direct (U3={u(q1R,3):.4f})")
    check(q1R.get("(2, 3)", 0.0) > u(q1R, 3),
          f"Q1: R23 ({q1R.get('(2, 3)', 0):.4f}) exceeds U3 ({u(q1R,3):.4f})")
    top2 = max(q2R, key=q2R.get)
    check(top2 == "(3,)", f"Q2: dominant redundancy-family term is U3 (got {top2})")
    top3 = max(q3R, key=q3R.get)
    check(top3 == "(3,)", f"Q3: dominant term is self-unique U3 (got {top3})")
    check(results["Q3"]["leak"] > results["Q1"]["leak"],
          f"leak(Q3)={results['Q3']['leak']:.3f} > "
          f"leak(Q1)={results['Q1']['leak']:.3f} (noise-driven vs deterministic)")
    for q in ("Q1", "Q2", "Q3"):
        check(0.0 <= results[q]["leak"] <= 1.0, f"{q}: leak in [0,1]")

    results["_meta"] = {"nt": args.nt, "nbins": args.nbins, "nlag": args.nlag,
                        "transient": args.transient,
                        "failures": failures, "runtime_s": time.time() - t0}
    args.out.with_suffix(".json").write_text(json.dumps(results, indent=2))
    print(f"\nWrote {args.out.with_suffix('.png')} and .json "
          f"({time.time()-t0:.0f}s total)", flush=True)

    if failures:
        print(f"\nGATE CLOSED: {len(failures)} check(s) failed.", flush=True)
        return 1
    print("\nGATE OPEN: mediator signature reproduced - proceed to Phase 1.",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
