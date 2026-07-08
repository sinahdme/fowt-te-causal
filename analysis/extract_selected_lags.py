#!/usr/bin/env python3
"""Extract the SELECTED source lags (coupling delays) from IDTxl's greedy
embedding — the pipeline-consistent delay numbers for the paper.

WHY THIS AND NOT THE GRAPH PICKLE
---------------------------------
te_pipeline.run_bivariate_te computes IDTxl's `selected_vars_sources` (the
(process, lag) tuples the greedy search kept) but only stores their COUNT
(`n_selected_sources`) in te_table*.parquet. build_graph() then makes a
networkx graph from that flat table, so te_full_graph.pkl carries NO lags
either. The lags are therefore not persisted anywhere and must be recomputed by
re-running IDTxl BivariateTE. This script does exactly that — bivariate only
(the leg that carries the reportable delay), with the SAME settings as the full
run — and reads `selected_vars_sources` off the results object.

Unlike analysis/delay_analysis.py (a standalone single-lag KSG profile whose
absolute magnitudes are not comparable to the pipeline TE), the lags here come
from the IDTxl greedy embedding actually used for the paper's TE, so they are
the authoritative coupling delays and can replace / corroborate Table 5.

WHEN TO RUN
-----------
On lams, AFTER the 12-day full campaign finishes (GPU free), OR any time on CPU.
Do NOT run with --gpu while the campaign is using the A100s. Bivariate-only over
a case subset is a fraction of the full-sweep cost.

USAGE (on lams, after the campaign)
-----------------------------------
    # representative healthy subset (what Table 5 reports), GPU:
    python analysis/extract_selected_lags.py \
        sims/dlc16_v11ms_s0*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb \
        --gpu --gpuid 0 -o reports/selected_lags.parquet

    # only the edges significant in the full table, all cases, CPU:
    python analysis/extract_selected_lags.py sims/*/IEA-15-*/*.outb \
        --filter-significant reports/te_table_full.parquet
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import te_pipeline as tp   # noqa: E402  (brings in load_outb/find_time_column via load_runs)


def bivariate_te_lags(source: np.ndarray, target: np.ndarray, settings) -> dict:
    """Mirror te_pipeline.run_bivariate_te, but also return the selected source
    lags (samples). Uses the pipeline's estimator/settings path verbatim."""
    from idtxl.bivariate_te import BivariateTE
    from idtxl.data import Data

    data = Data(np.vstack([source, target]), dim_order="ps", normalise=True)
    s = tp._apply_estimator(
        {**tp._idtxl_base_settings(settings), "max_shift": max(1, len(target) // 4)},
        settings.ksg_estimator, settings)
    results = BivariateTE().analyse_single_target(settings=s, data=data, target=1, sources=[0])
    tr = results.get_single_target(1, fdr=False)
    te_val, p_val, selected = tp._extract_te_pval(tr)
    src_lags = sorted(int(lag) for (proc, lag) in selected if proc == 0)
    return {"te_nats": te_val, "p_value": p_val,
            "significant": bool(p_val < settings.alpha and te_val > 0),
            "source_lags_samples": src_lags}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", type=Path, help="OpenFAST .outb files")
    ap.add_argument("-o", "--output", type=Path, default=Path("reports/selected_lags.parquet"))
    ap.add_argument("--gpu", action="store_true",
                    help="OpenCLKraskovCMI (GPU). DO NOT use while the campaign runs.")
    ap.add_argument("--gpuid", type=int, default=0)
    ap.add_argument("--decimate-target-hz", type=float, default=5.0)
    ap.add_argument("--transient-drop-s", type=float, default=600.0)
    ap.add_argument("--max-lag", type=int, default=150)
    ap.add_argument("--max-lag-sources", type=int, default=20)   # full-run value
    ap.add_argument("--tau", type=int, default=1)
    ap.add_argument("--slow-drift-tau", type=int, default=5)     # full-run value
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--sources", default="Wind1VelX,Wave1Elev")
    ap.add_argument("--filter-significant", type=Path, default=None,
                    help="Only run (source,target) edges significant in this te_table "
                         "(bivariate_te_ksg, >50%% of cases). Cheapest, most relevant.")
    args = ap.parse_args()

    settings = replace(
        tp.TESettings(),
        decimate_target_hz=args.decimate_target_hz, transient_drop_s=args.transient_drop_s,
        max_lag=args.max_lag, max_lag_sources=args.max_lag_sources, tau=args.tau,
        slow_drift_tau=args.slow_drift_tau, n_perm=args.n_perm, gpuid=args.gpuid,
        ksg_estimator="OpenCLKraskovCMI" if args.gpu else "JidtKraskovCMI",
    )
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    targets = list(settings.responses)

    # optional: restrict to edges that survived in the flat full table
    keep = None
    if args.filter_significant and args.filter_significant.exists():
        ft = pd.read_parquet(args.filter_significant)
        ft = ft[ft.method == "bivariate_te_ksg"]
        sig = (ft.groupby(["source", "target"])["significant"]
               .apply(lambda s: (s == True).mean() > 0.5))
        keep = {edge for edge, ok in sig.items() if ok}
        print(f"filter: {len(keep)} significant edges from {args.filter_significant.name}")

    dt_out = 1.0 / settings.decimate_target_hz
    rows = []
    for path in args.inputs:
        df = tp.load_outb(path)
        tcol = tp.find_time_column(df)
        dt = float(np.median(np.diff(df[tcol].to_numpy(float))))
        case = Path(path).stem if Path(path).stem != "IEA-15-240-RWT-UMaineSemi" \
            else Path(path).parents[1].name
        cache = {}
        for name in sources + targets:
            try:
                cache[name] = tp.preprocess_channel(
                    df[tp.find_channel(df, name)].to_numpy(float), dt, settings, seed=0)[0]
            except KeyError:
                pass
        for src in sources:
            if src not in cache:
                continue
            for tgt in targets:
                if tgt not in cache or (keep is not None and (src, tgt) not in keep):
                    continue
                s = replace(settings, tau=settings.slow_drift_tau) \
                    if settings.slow_drift_tau and tgt in settings.slow_drift_targets \
                    else settings
                r = bivariate_te_lags(cache[src], cache[tgt], s)
                lags_s = [L * dt_out for L in r["source_lags_samples"]]
                rows.append(dict(case=case, source=src, target=tgt,
                                 te_nats=round(r["te_nats"], 5), significant=r["significant"],
                                 n_source_lags=len(lags_s),
                                 min_lag_s=min(lags_s) if lags_s else np.nan,
                                 lags_s=lags_s, tau_used=s.tau))
                print(f"  {case} {src}->{tgt}: TE={r['te_nats']:+.4f} "
                      f"lags(s)={[round(x,2) for x in lags_s]}", flush=True)

    out = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(args.output)
    print(f"\nwrote {args.output} ({len(out)} rows)")

    sig = out[out.significant]
    if len(sig):
        agg = (sig.groupby(["source", "target"])
               .agg(sel_delay_s=("min_lag_s", "mean"),
                    te_nats=("te_nats", "mean"), n=("case", "size"))
               .round(3).reset_index())
        print("\n=== SELECTED COUPLING DELAYS (min selected source lag, mean over cases) ===")
        print(agg.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
