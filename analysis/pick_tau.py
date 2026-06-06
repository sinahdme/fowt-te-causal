"""pick_tau.py — data-driven embedding delay (tau) for the TE pipeline.

Picks the IDTxl candidate spacing (`tau` / `tau_sources` / `tau_target`) from
the data instead of guessing. For each channel, after the SAME preprocessing
te_pipeline applies (drop transient -> decimate -> jitter), it reports:

  * autocorrelation 1/e time  -- lag where the ACF first drops below 1/e
  * autocorrelation 1st zero  -- lag where the ACF first crosses 0
  * self-MI 1st minimum       -- first local minimum of I(x_t ; x_{t+tau})

The self-MI first minimum is the standard Fraser & Swinney (1986) criterion for
a time-delay embedding: it's the spacing at which successive embedding
coordinates are maximally non-redundant. Choosing the pipeline's `tau` near
that value makes the embedding both cheaper (fewer candidates) and better
conditioned (less redundant), rather than picking a round number for speed.

All lags are reported in samples at the DECIMATED rate and in seconds. Run on
the same .outb you feed te_pipeline, with the same --decimate-target-hz.

Usage:
    python analysis/pick_tau.py sims/.../run.outb
    python analysis/pick_tau.py run.outb --max-lag 150 --decimate-target-hz 5.0 --bins 32
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
from te_pipeline import (  # noqa: E402
    TESettings, find_channel, preprocess_channel,
    DEFAULT_ENV_SOURCES, DEFAULT_RESPONSES,
)
from load_runs import load_outb, find_time_column  # noqa: E402


def autocorr(x: np.ndarray, max_lag: int) -> np.ndarray:
    """Normalised autocorrelation, acf[0]=1, for lags 0..max_lag."""
    x = x - x.mean()
    denom = float(np.dot(x, x))
    if denom == 0.0:
        return np.zeros(max_lag + 1)
    n = len(x)
    return np.array([np.dot(x[: n - k], x[k:]) / denom
                     for k in range(max_lag + 1)])


def self_mi(x: np.ndarray, max_lag: int, bins: int) -> np.ndarray:
    """Self mutual information I(x_t ; x_{t+lag}) in nats, lags 1..max_lag
    (mi[0] is the lag-1 value). Histogram estimator, fixed bin count
    (Fraser & Swinney style)."""
    # Fixed bin edges over the channel's range so every lag uses the same grid.
    edges = np.histogram_bin_edges(x, bins=bins)
    mi = np.empty(max_lag)
    for i, lag in enumerate(range(1, max_lag + 1)):
        a, b = x[:-lag], x[lag:]
        c, _, _ = np.histogram2d(a, b, bins=[edges, edges])
        p = c / c.sum()
        px = p.sum(axis=1)
        py = p.sum(axis=0)
        nz = p > 0
        outer = (px[:, None] * py[None, :])
        mi[i] = float(np.sum(p[nz] * np.log(p[nz] / outer[nz])))
    return mi


def first_below(acf: np.ndarray, thresh: float) -> int | None:
    """First lag (>=1) where acf drops below thresh; None if it never does."""
    for k in range(1, len(acf)):
        if acf[k] < thresh:
            return k
    return None


def first_zero(acf: np.ndarray) -> int | None:
    for k in range(1, len(acf)):
        if acf[k] <= 0.0:
            return k
    return None


def first_local_min(mi: np.ndarray) -> int:
    """First local minimum of mi (returns the LAG, i.e. index+1). Falls back to
    the global argmin if the curve is monotone within the window."""
    for i in range(1, len(mi) - 1):
        if mi[i] <= mi[i - 1] and mi[i] < mi[i + 1]:
            return i + 1
    return int(np.argmin(mi)) + 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="OpenFAST .outb file")
    ap.add_argument("--max-lag", type=int, default=150)
    ap.add_argument("--decimate-target-hz", type=float, default=5.0)
    ap.add_argument("--transient-drop-s", type=float, default=600.0)
    ap.add_argument("--bins", type=int, default=32,
                    help="Histogram bins for the self-MI estimate (default 32).")
    args = ap.parse_args()

    settings = TESettings(
        decimate_target_hz=args.decimate_target_hz,
        transient_drop_s=args.transient_drop_s,
        max_lag=args.max_lag,
    )

    df = load_outb(args.input)
    t = df[find_time_column(df)].to_numpy()
    dt_in = float(np.median(np.diff(t)))

    # Preprocess every channel exactly as te_pipeline does, then measure.
    rows = []
    dt_out = dt_in
    seed = 0
    for name in (*settings.env_sources, *settings.responses):
        try:
            col = find_channel(df, name)
        except KeyError:
            print(f"  (skip {name}: not in file)")
            continue
        clean, dt_out = preprocess_channel(df[col].to_numpy(), dt_in, settings, seed=seed)
        seed += 1
        acf = autocorr(clean, args.max_lag)
        mi = self_mi(clean, args.max_lag, args.bins)
        rows.append((name,
                     first_below(acf, 1.0 / np.e),
                     first_zero(acf),
                     first_local_min(mi)))

    fs_out = 1.0 / dt_out
    print(f"\nDecimated rate {fs_out:.2f} Hz  ->  1 sample = {dt_out:.3f} s, "
          f"tau in samples (x{dt_out:.2f} s)\n")
    hdr = f"{'channel':<12} {'ACF<1/e':>10} {'ACF=0':>10} {'MI 1st-min':>12}"
    print(hdr)
    print("-" * len(hdr))

    def fmt(k):
        return "    --   " if k is None else f"{k:>4d} ({k * dt_out:>4.1f}s)"

    mi_mins = []
    for name, e_tau, z_tau, mi_min in rows:
        mi_mins.append(mi_min)
        print(f"{name:<12} {fmt(e_tau):>10} {fmt(z_tau):>10} {fmt(mi_min):>12}")

    if mi_mins:
        lo, med, hi = int(np.min(mi_mins)), int(np.median(mi_mins)), int(np.max(mi_mins))
        print("\nSelf-MI first-minimum across channels:"
              f"  min={lo} ({lo*dt_out:.1f}s)  median={med} ({med*dt_out:.1f}s)"
              f"  max={hi} ({hi*dt_out:.1f}s)")
        print(f"\nSuggested tau:")
        print(f"  conservative (preserve the fastest channel) : tau = {max(1, lo)}")
        print(f"  typical (median channel)                    : tau = {max(1, med)}")
        print("  -> a single pipeline tau must be <= max_lag and is shared by all "
              "channels;\n     pick the conservative value if any fast channel "
              "matters, else the median.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
