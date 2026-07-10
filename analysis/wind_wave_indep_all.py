"""wind_wave_indep_all.py — batch wind/wave independence check over many runs.

Extends the single-run `wind_wave_indep.py` to (a) accept many `.outb` files,
(b) replace its crude `MI < 0.05` heuristic with a proper **circular-shift
surrogate** test, and (c) write a tidy parquet + print a table. It reuses
`wind_wave_indep.mutual_info` / `cross_corr` and the pipeline preprocessing, so
the estimator is identical to the main analysis.

Why the surrogate matters: the histogram MI of two *independent* finite,
autocorrelated signals is not zero — it sits at a positive bias floor
(≈ (bins-1)^2 / 2N nats). A fixed MI threshold misreads that floor as coupling.
A circular shift of the wave signal preserves each signal's autocorrelation
(hence the same bias floor) while destroying any wind-wave alignment, giving the
correct null. A plain i.i.d. shuffle does NOT (it destroys autocorrelation,
inflates effective N, understates the floor, and yields spurious significance).

CPU-only: no IDTxl / GPU needed (only numpy + the .outb reader), so this runs in
the `fowt-te` env on the server without the estimator stack.

Usage (server, all 54 runs):
    python analysis/wind_wave_indep_all.py \
        sims/*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb \
        -o reports/wind_wave_independence.parquet

    # include the root-level below-rated / open-loop runs too:
    python analysis/wind_wave_indep_all.py sims/*/*/*.outb *.outb -o reports/wind_wave_independence.parquet
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
from wind_wave_indep import mutual_info, cross_corr  # noqa: E402  (reused)


def case_id_from_path(p: Path) -> str:
    """sims/<case>/<model>/<model>.outb -> <case>; otherwise the file stem.

    The 54 campaign runs share one filename (IEA-15-240-RWT-UMaineSemi.outb)
    inside per-case folders, so the folder name is the real case id."""
    parts = p.resolve().parts
    if "sims" in parts:
        i = parts.index("sims")
        if i + 1 < len(parts):
            return parts[i + 1]
    return p.stem


def check_one(path: Path, settings: TESettings, bins: int, xcorr_lag: int,
              n_surrogate: int, min_n: int, rng: np.random.Generator) -> dict:
    """Independence metrics for one run. Returns a row dict (status='ok' or a
    skip reason in 'status')."""
    row = {"case": case_id_from_path(path), "path": str(path)}
    try:
        df = load_outb(path)
        dt_in = float(np.median(np.diff(df[find_time_column(df)].to_numpy())))
        wind, dt_out = preprocess_channel(
            df[find_channel(df, "Wind1VelX")].to_numpy(), dt_in, settings, seed=0)
        wave, _ = preprocess_channel(
            df[find_channel(df, "Wave1Elev")].to_numpy(), dt_in, settings, seed=1)
    except Exception as e:  # missing channel, unreadable file, ...
        row["status"] = f"error: {type(e).__name__}: {e}"
        return row

    n = len(wave)
    row["n"] = n
    if n < min_n:
        row["status"] = f"too_short (N={n} after {settings.transient_drop_s:.0f}s drop)"
        return row

    r0, rmax, lag = cross_corr(wind, wave, xcorr_lag)
    w = (wind - wind.mean()) / wind.std()
    v = (wave - wave.mean()) / wave.std()
    obs = mutual_info(w, v, bins)

    lo, hi = n // 10, n - n // 10
    shifts = rng.integers(lo, hi, size=n_surrogate)
    nulls = np.array([mutual_info(w, np.roll(v, int(k)), bins) for k in shifts])
    nm, ns = float(nulls.mean()), float(nulls.std())
    z = (obs - nm) / ns if ns > 0 else 0.0
    # one-sided p: fraction of surrogates with MI >= observed (coupling => obs high)
    p = (1 + int(np.sum(nulls >= obs))) / (n_surrogate + 1)

    row.update(
        status="ok", fs_hz=round(1.0 / dt_out, 3),
        pearson_r0=round(r0, 4), xcorr_absmax=round(abs(rmax), 4),
        xcorr_lag_s=round(lag * dt_out, 2),
        mi_nats=round(obs, 4), mi_null_nats=round(nm, 4),
        mi_null_sd=round(ns, 4), z=round(z, 2), p_value=round(p, 4),
        independent=bool(abs(rmax) < 0.1 and p >= 0.05),
    )
    return row


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", type=Path, nargs="+", help=".outb files (shell-globbed)")
    ap.add_argument("-o", "--out", type=Path,
                    default=PROJECT_ROOT / "reports" / "wind_wave_independence.parquet")
    ap.add_argument("--decimate-target-hz", type=float, default=5.0)
    ap.add_argument("--transient-drop-s", type=float, default=600.0)
    ap.add_argument("--max-lag", type=int, default=150,
                    help="Lag window (samples) for the cross-correlation scan.")
    ap.add_argument("--bins", type=int, default=32)
    ap.add_argument("--n-surrogate", type=int, default=200,
                    help="Circular-shift surrogates for the MI null.")
    ap.add_argument("--min-n", type=int, default=1000,
                    help="Skip runs with fewer than this many samples after the "
                         "transient drop (e.g. short calibration cases).")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    settings = TESettings(
        decimate_target_hz=args.decimate_target_hz,
        transient_drop_s=args.transient_drop_s,
        max_lag=args.max_lag,
    )
    rng = np.random.default_rng(args.seed)

    rows = []
    for path in args.inputs:
        row = check_one(path, settings, args.bins, args.max_lag,
                        args.n_surrogate, args.min_n, rng)
        rows.append(row)
        if row["status"] != "ok":
            print(f"  {row['case']:22s} SKIP -- {row['status']}", flush=True)
        else:
            v = "INDEP" if row["independent"] else "COUPLED"
            print(f"  {row['case']:22s} N={row['n']:6d} r0={row['pearson_r0']:+.4f} "
                  f"|xc|={row['xcorr_absmax']:.4f} MI={row['mi_nats']:.4f} "
                  f"null={row['mi_null_nats']:.4f} z={row['z']:+.2f} "
                  f"p={row['p_value']:.3f}  {v}", flush=True)

    import pandas as pd
    df = pd.DataFrame(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.out, index=False)

    ok = df[df["status"] == "ok"]
    n_ok = len(ok)
    n_indep = int(ok["independent"].sum()) if n_ok else 0
    n_skip = len(df) - n_ok
    print("\n" + "=" * 60)
    print(f"tested {n_ok} runs, skipped {n_skip}")
    if n_ok:
        print(f"  independent: {n_indep}/{n_ok}")
        print(f"  z range    : [{ok['z'].min():+.2f}, {ok['z'].max():+.2f}]")
        print(f"  min p      : {ok['p_value'].min():.3f}  "
              f"(any p<0.05 => {'COUPLED runs present' if (ok['p_value'] < 0.05).any() else 'none - all independent'})")
        print(f"  mean(MI-null) excess: {(ok['mi_nats'] - ok['mi_null_nats']).mean():+.4f} nats")
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
