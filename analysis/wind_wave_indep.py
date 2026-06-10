"""wind_wave_indep.py — quantify wind/wave (in)dependence for a case.

For Wind1VelX vs Wave1Elev, after the pipeline's preprocessing (drop transient,
decimate, jitter), reports:
  - lag-0 Pearson correlation
  - max |cross-correlation| across +/- lags, and the lag (in samples and s)
  - mutual information (histogram estimator, nats)
  - optionally (--te) bidirectional transfer entropy TE(Wind->Wave) and
    TE(Wave->Wind), which should BOTH be ~0 if the two forcings are causally
    independent (also a sanity check on the embedding/surrogate machinery).

Why: decides whether conditional TE is removing a CONFOUND (correlated drivers)
or boosting DETECTION POWER (independent co-drivers) -- which changes how the
conditional-TE result is framed -- and backs a "the two forcings are
statistically/causally independent" statement for the methods section.

Usage:
    python analysis/wind_wave_indep.py path/to/run.outb
    python analysis/wind_wave_indep.py run.outb --te --gpu
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
from te_pipeline import TESettings, find_channel, preprocess_channel  # noqa: E402
from load_runs import load_outb, find_time_column  # noqa: E402


def cross_corr(a: np.ndarray, b: np.ndarray, max_lag: int):
    """Pearson r at lag 0, and the max |r| over lags -max_lag..max_lag.
    Positive lag k means a(t) vs b(t+k). Returns (r0, rmax, lag_at_max)."""
    a = (a - a.mean()) / a.std()
    b = (b - b.mean()) / b.std()
    n = len(a)
    r0 = float(np.dot(a, b) / n)
    best_r, best_lag = r0, 0
    for k in range(1, max_lag + 1):
        rp = float(np.dot(a[: n - k], b[k:]) / (n - k))   # a leads b
        rm = float(np.dot(a[k:], b[: n - k]) / (n - k))   # b leads a
        for r, lag in ((rp, k), (rm, -k)):
            if abs(r) > abs(best_r):
                best_r, best_lag = r, lag
    return r0, best_r, best_lag


def mutual_info(a: np.ndarray, b: np.ndarray, bins: int) -> float:
    """Histogram mutual information I(a;b) in nats (lag 0)."""
    c, _, _ = np.histogram2d(a, b, bins=bins)
    p = c / c.sum()
    px = p.sum(axis=1)
    py = p.sum(axis=0)
    nz = p > 0
    outer = px[:, None] * py[None, :]
    return float(np.sum(p[nz] * np.log(p[nz] / outer[nz])))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("--decimate-target-hz", type=float, default=5.0)
    ap.add_argument("--transient-drop-s", type=float, default=600.0)
    ap.add_argument("--max-lag", type=int, default=150,
                    help="Lag window (samples) for the cross-correlation scan.")
    ap.add_argument("--bins", type=int, default=32)
    ap.add_argument("--te", action="store_true",
                    help="Also compute bidirectional TE(Wind<->Wave) (slower).")
    ap.add_argument("--gpu", action="store_true",
                    help="Use OpenCL estimator for the --te option.")
    ap.add_argument("--n-perm", type=int, default=200)
    args = ap.parse_args()

    settings = TESettings(
        decimate_target_hz=args.decimate_target_hz,
        transient_drop_s=args.transient_drop_s,
        max_lag=args.max_lag,
        n_perm=args.n_perm,
        ksg_estimator="OpenCLKraskovCMI" if args.gpu else "JidtKraskovCMI",
    )

    df = load_outb(args.input)
    dt_in = float(np.median(np.diff(df[find_time_column(df)].to_numpy())))
    wind, dt_out = preprocess_channel(df[find_channel(df, "Wind1VelX")].to_numpy(),
                                      dt_in, settings, seed=0)
    wave, _ = preprocess_channel(df[find_channel(df, "Wave1Elev")].to_numpy(),
                                 dt_in, settings, seed=1)

    r0, rmax, lag = cross_corr(wind, wave, args.max_lag)
    mi = mutual_info((wind - wind.mean()) / wind.std(),
                     (wave - wave.mean()) / wave.std(), args.bins)

    print(f"\n{args.input.name}  (N={len(wind)} @ {1/dt_out:.2f} Hz)\n")
    print(f"  lag-0 Pearson r          : {r0:+.4f}")
    print(f"  max |cross-corr| (+-{args.max_lag}) : {rmax:+.4f}  at lag "
          f"{lag} ({lag*dt_out:+.1f} s)")
    print(f"  mutual information       : {mi:.4f} nats")
    indep = abs(rmax) < 0.1 and mi < 0.05
    print(f"  -> wind & wave look {'INDEPENDENT' if indep else 'COUPLED'} "
          f"(|r|<0.1 & MI<0.05 nats => independent)")

    if args.te:
        from te_pipeline import run_bivariate_te
        print("\n  bidirectional TE (should be ~0 both ways if independent):")
        fwd = run_bivariate_te(wind, wave, settings)
        rev = run_bivariate_te(wave, wind, settings)
        print(f"    TE(Wind->Wave) = {fwd['te_nats']:+.4f}  p={fwd['p_value']:.4f}")
        print(f"    TE(Wave->Wind) = {rev['te_nats']:+.4f}  p={rev['p_value']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
