"""
diag_maxlag_sweep.py — why did the full-settings KSG nulls the wave coupling?

The full-settings probe (max_lag=150, 5 Hz, n_perm=200) returned
TE_ksg(Wave1Elev -> PtfmHeave) = 0 and TE_ksg(Wave -> PtfmPitch) ~ 0, even
though linear Granger still finds them loudly (0.35 / 0.12 nats). That overturns
the first-pass H2/H6 result, where those edges were 100% significant at
max_lag=60. Before committing 54 cases x ~9 h to the full settings, we need to
know WHICH of two things is happening:

  (a) greedy-selection failure — 150 fine lag candidates + the inclusion test
      reject the true coupling that max_lag=60 found (a settings artifact); or
  (b) long-embedding absorption — at max_lag=150 the target's own past is so
      informative (heave AIS ~ 2.6, resonant/self-predictable) that wave adds
      little NEW predictive info beyond the target history (a real result that
      reframes H2/H6 rather than an artifact).

This script isolates that: it reruns ONLY the wave->{heave,pitch} bivariate KSG
TE at several max_lag values on ONE case, with Granger alongside as the linear
reference, and reports te_nats / p / n_selected_sources / runtime per setting.
The discriminator is `n_src`: if KSG selects 0 source lags at max_lag=150 but >0
at max_lag=60, that points to (a); if it selects source lags yet TE stays ~0
across all max_lag, that points to (b).

It reuses te_pipeline's preprocessing + estimators verbatim, so inputs match the
production table exactly — only max_lag (and the channel subset) change.

Usage (on lams, GPU):
    python analysis/diag_maxlag_sweep.py \
        sims/dlca_v11ms_s00/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb \
        --gpu --gpuid 0 --tau 5 --max-lags 30,60,100,150 --n-perm 200 \
        -o reports/diag_maxlag_sweep.parquet

Cost: ~8-16 single bivariate jobs run serially. A max_lag=150 KSG job is
~5-8 min on an A100; lower max_lags are faster; Granger is ~1-5 min. Budget
roughly half an hour, not the 9 h of a full case.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))

from load_runs import load_outb, find_time_column  # noqa: E402
from te_pipeline import (  # noqa: E402
    TESettings,
    find_channel,
    preprocess_channel,
    run_bivariate_te,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="One OpenFAST .outb file")
    ap.add_argument("-o", "--output", type=Path,
                    default=PROJECT_ROOT / "reports" / "diag_maxlag_sweep.parquet")
    ap.add_argument("--source", default="Wave1Elev",
                    help="Env source channel (default Wave1Elev).")
    ap.add_argument("--targets", default="PtfmHeave,PtfmPitch",
                    help="Comma-separated response channels to test "
                         "(default PtfmHeave,PtfmPitch — the suppressed H2/H6 edges).")
    ap.add_argument("--max-lags", default="30,60,100,150",
                    help="Comma-separated max_lag values to sweep (default 30,60,100,150).")
    ap.add_argument("--tau", type=int, default=5,
                    help="Embedding candidate spacing (default 5 — matches the "
                         "slow-drift handling heave/pitch got in the probe). Try "
                         "--tau 1 too to separate tau from max_lag effects.")
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--decimate-target-hz", type=float, default=5.0)
    ap.add_argument("--transient-drop-s", type=float, default=600.0)
    ap.add_argument("--gpu", action="store_true",
                    help="Use OpenCLKraskovCMI (GPU) for KSG, like the probe. "
                         "Granger stays on the analytic Gaussian estimator.")
    ap.add_argument("--gpuid", type=int, default=0)
    ap.add_argument("--no-granger", action="store_true",
                    help="Skip the Granger reference column (KSG only).")
    args = ap.parse_args()

    targets = [t.strip() for t in args.targets.split(",") if t.strip()]
    max_lags = [int(x) for x in args.max_lags.split(",") if x.strip()]
    for ml in max_lags:
        if not (0 < args.tau <= ml):
            ap.error(f"tau={args.tau} must satisfy 0 < tau <= max_lag (got max_lag={ml})")

    base = TESettings(
        decimate_target_hz=args.decimate_target_hz,
        transient_drop_s=args.transient_drop_s,
        tau=args.tau,
        n_perm=args.n_perm,
        ksg_estimator="OpenCLKraskovCMI" if args.gpu else "JidtKraskovCMI",
        gpuid=args.gpuid,
        gpu_ids=(args.gpuid,),
    )

    print(f"loading {args.input.name}", flush=True)
    df = load_outb(args.input)
    t = df[find_time_column(df)].to_numpy()
    dt = float(np.median(np.diff(t)))
    print(f"  rate {1.0/dt:.1f} Hz, dropping {args.transient_drop_s}s, "
          f"decimating to ~{args.decimate_target_hz} Hz", flush=True)

    # Preprocess each channel once (TE-parity: drop transient, decimate, jitter).
    needed = [args.source, *targets]
    cached: dict[str, np.ndarray] = {}
    for seed, name in enumerate(needed):
        col = find_channel(df, name)
        clean, dt_out = preprocess_channel(df[col].to_numpy(), dt, base, seed=seed)
        cached[name] = clean
    n = len(next(iter(cached.values())))
    print(f"  cached {len(cached)} channels @ {1.0/dt_out:.2f} Hz, N={n}\n", flush=True)

    methods = [("ksg", None)]
    if not args.no_granger:
        methods.append(("granger", "JidtGaussianCMI"))

    rows: list[dict] = []
    for target in targets:
        for ml in max_lags:
            s = replace(base, max_lag=ml)
            for label, estimator in methods:
                t0 = time.time()
                try:
                    r = run_bivariate_te(cached[args.source], cached[target], s,
                                         estimator=estimator)
                    ok, err = True, None
                except Exception as e:  # keep one bad cell from sinking the sweep
                    import traceback
                    traceback.print_exc()
                    ok, err, r = False, f"{type(e).__name__}: {e}", {}
                dt_job = time.time() - t0
                row = {
                    "source": args.source, "target": target, "method": label,
                    "max_lag": ml, "tau": args.tau,
                    "te_nats": r.get("te_nats", float("nan")),
                    "p_value": r.get("p_value", float("nan")),
                    "significant": r.get("significant", False),
                    "n_selected_sources": r.get("n_selected_sources", -1),
                    "runtime_s": dt_job, "ok": ok, "err": err,
                }
                rows.append(row)
                tag = f"{label:8s} {args.source}->{target:<10} max_lag={ml:<4d}"
                if ok:
                    print(f"  [done {dt_job:5.0f}s] {tag} "
                          f"TE={row['te_nats']:+.4f} p={row['p_value']:.4f} "
                          f"n_src={row['n_selected_sources']}", flush=True)
                else:
                    print(f"  !! {tag} {err}", file=sys.stderr, flush=True)
                # Checkpoint after every cell so a crash keeps partial results.
                args.output.parent.mkdir(parents=True, exist_ok=True)
                pd.DataFrame(rows).to_parquet(args.output, compression="zstd")

    out = pd.DataFrame(rows)
    print("\n=== max_lag sweep ===")
    cols = ["target", "method", "max_lag", "tau", "te_nats", "p_value",
            "significant", "n_selected_sources", "runtime_s"]
    with pd.option_context("display.width", 120, "display.max_columns", None):
        print(out[cols].to_string(index=False))
    print(f"\nWrote {args.output}  ({len(out)} rows)")

    # Interpretation hint, per the docstring's (a) vs (b).
    ksg = out[(out["method"] == "ksg") & out["ok"]]
    if not ksg.empty:
        print("\n--- read-out ---")
        for target in targets:
            sub = ksg[ksg["target"] == target].sort_values("max_lag")
            if sub.empty:
                continue
            selected_any = (sub["n_selected_sources"] > 0).any()
            te_ever = (sub["te_nats"].abs() > 1e-6).any()
            lo = sub.iloc[0]
            hi = sub.iloc[-1]
            print(f"{target}: TE_ksg {lo['te_nats']:+.4f} @max_lag={int(lo['max_lag'])} "
                  f"-> {hi['te_nats']:+.4f} @max_lag={int(hi['max_lag'])}; "
                  f"n_src {int(lo['n_selected_sources'])}->{int(hi['n_selected_sources'])}")
            if te_ever and (sub["te_nats"].abs() > 1e-6).iloc[0] and not (sub["te_nats"].abs() > 1e-6).iloc[-1]:
                print(f"    coupling present at low max_lag, gone at high "
                      f"-> points to (a) greedy-selection / embedding-length artifact")
            elif selected_any and not te_ever:
                print(f"    source lags selected but TE stays ~0 -> points to (b) "
                      f"long-embedding absorption into self-prediction")
    return 0


if __name__ == "__main__":
    sys.exit(main())
