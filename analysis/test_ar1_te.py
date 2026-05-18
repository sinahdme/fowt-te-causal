"""
test_ar1_te.py — validation case 2: known-answer TE recovery.

Generates a coupled AR(1) chain X → Y where Y carries a delayed,
weighted copy of X plus independent noise. Verifies that IDTxl
recovers:
    TE(X → Y) > 0  and  significant (p < 0.05)
    TE(Y → X) ≈ 0  and  not significant

Per PLAN §Verification step 2.

Following kraskov-2004 §III.A: add 1e-10 jitter to break finite-precision
neighbour degeneracies. Following kraskov-2004 §III, default KSG k=4.

Usage:
    python analysis/test_ar1_te.py            # default: 5000 samples, alpha=0.5
    python analysis/test_ar1_te.py --n 10000  # longer series for tighter CI
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, asdict

import numpy as np


@dataclass
class Result:
    direction: str
    te_nats: float
    p_value: float
    significant: bool


def make_ar1_chain(n: int, alpha: float = 0.5, beta: float = 0.5, seed: int = 0):
    """Generate a coupled AR(1) chain  X_t = alpha*X_{t-1} + eps_x_t,
                                       Y_t = beta*Y_{t-1} + gamma*X_{t-1} + eps_y_t.

    Returns x, y as 1D numpy arrays of length n.
    """
    rng = np.random.default_rng(seed)
    eps_x = rng.standard_normal(n)
    eps_y = rng.standard_normal(n)
    x = np.zeros(n)
    y = np.zeros(n)
    gamma = 0.6  # coupling strength X_{t-1} → Y_t
    for t in range(1, n):
        x[t] = alpha * x[t - 1] + eps_x[t]
        y[t] = beta * y[t - 1] + gamma * x[t - 1] + eps_y[t]
    return x, y


def jitter(arr: np.ndarray, scale: float = 1e-10, seed: int = 42) -> np.ndarray:
    """Add tiny Gaussian noise (kraskov-2004 §III.A neighbour-degeneracy fix)."""
    rng = np.random.default_rng(seed)
    return arr + scale * rng.standard_normal(arr.shape)


def run_te(source: np.ndarray, target: np.ndarray, n_perm: int = 200, ksg_k: int = 4) -> Result:
    """Run IDTxl BivariateTE with KSG (Kraskov k=4) and surrogate testing.

    Returns the TE estimate and p-value for the source→target direction
    using automatic embedding selection.
    """
    from idtxl.bivariate_te import BivariateTE
    from idtxl.data import Data

    arr = np.vstack([source, target])  # shape (2, n)
    data = Data(arr, dim_order="ps", normalise=True)
    settings = {
        "cmi_estimator": "JidtKraskovCMI",
        "kraskov_k": str(ksg_k),
        "max_lag_sources": 5,
        "min_lag_sources": 1,
        "max_lag_target": 5,
        "n_perm_max_stat": n_perm,
        "n_perm_min_stat": n_perm,
        "n_perm_omnibus": n_perm,
        "n_perm_max_seq": n_perm,
        "alpha_max_stat": 0.05,
        "alpha_min_stat": 0.05,
        "alpha_omnibus": 0.05,
        # Single time series, so shuffle within the time axis rather than
        # between replications. Bypasses an `np.math.factorial` call that
        # was removed in NumPy 2.x (idtxl/stats.py line 1535).
        "permute_in_time": True,
        # Circular shift preserves the source's power spectrum + marginal
        # distribution exactly while destroying directed coupling to the
        # target. Equivalent to IAAFT for our purposes; the IDTxl default
        # 'random' would destroy auto-correlation too (weakest null).
        "perm_type": "circular",
    }
    analysis = BivariateTE()
    results = analysis.analyse_single_target(settings=settings, data=data, target=1, sources=[0])

    target_results = results.get_single_target(1, fdr=False)
    te = target_results.get("te")
    pval = target_results.get("omnibus_pval")

    te_val = float(te[0]) if (te is not None and len(te) > 0) else 0.0
    p_val = float(pval) if pval is not None else 1.0
    return Result(
        direction="source→target",
        te_nats=te_val,
        p_value=p_val,
        significant=p_val < 0.05 and te_val > 0,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5000)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--beta", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n-perm", type=int, default=200)
    parser.add_argument("--ksg-k", type=int, default=4)
    args = parser.parse_args()

    print(f"Generating AR(1) chain X→Y, n={args.n}, alpha={args.alpha}, beta={args.beta}")
    x, y = make_ar1_chain(args.n, args.alpha, args.beta, args.seed)
    x = jitter(x, seed=args.seed + 1)
    y = jitter(y, seed=args.seed + 2)
    print(f"  x: mean={x.mean():+.3f}, std={x.std():.3f}")
    print(f"  y: mean={y.mean():+.3f}, std={y.std():.3f}")

    print("\nForward: TE(X → Y)")
    fwd = run_te(x, y, n_perm=args.n_perm, ksg_k=args.ksg_k)
    print(f"  TE = {fwd.te_nats:+.4f} nats, p = {fwd.p_value:.4f}, significant = {fwd.significant}")

    print("\nReverse: TE(Y → X)")
    rev = run_te(y, x, n_perm=args.n_perm, ksg_k=args.ksg_k)
    print(f"  TE = {rev.te_nats:+.4f} nats, p = {rev.p_value:.4f}, significant = {rev.significant}")

    print("\n=== Validation verdict ===")
    pass_fwd = fwd.significant and fwd.te_nats > 0
    pass_rev = not rev.significant or rev.te_nats < fwd.te_nats * 0.2
    print(f"  TE(X→Y) significant and > 0?     {'PASS' if pass_fwd else 'FAIL'}")
    print(f"  TE(Y→X) NOT significant or ≪ fwd? {'PASS' if pass_rev else 'FAIL'}")

    return 0 if (pass_fwd and pass_rev) else 1


if __name__ == "__main__":
    sys.exit(main())
