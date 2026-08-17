#!/usr/bin/env python3
"""collect_wind_struct.py - the CORRECTED wind->structure table for the paper.

Merges the RtVAvgxh full campaign (reports/te_wsrc_*.parquet, rotor-averaged wind) with the
existing te_table_full (Wind1VelX point wind + Wave1Elev) at the same settings, into one
source x target summary over the healthy population. Also reports the firewall under fault
(RtVAvgxh -> PtfmPitch, from the reanalysis reports/te_rtvavg_<fault>.parquet).

Works on partial results (run anytime during the campaign).
"""
import argparse
import glob
import re
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
TARGETS = ("PtfmPitch", "PtfmSurge", "PtfmHeave", "RootMyc1", "RootMxc1", "TwrBsMyt",
           "FAIRTEN1", "FAIRTEN2", "FAIRTEN3")
FAULT = re.compile(r"_(pitchlock|gain\d+|stuckb\d)$")


def summarize(df: pd.DataFrame, title: str) -> None:
    if df.empty:
        return
    k = df[(df.method == "bivariate_te_ksg") & (df.target.isin(TARGETS))]
    if k.empty:
        return
    g = k.groupby(["source", "target"]).agg(
        mean_te=("te_nats", "mean"), max_te=("te_nats", "max"),
        pct_sig=("significant", lambda s: 100.0 * s.mean()), n=("te_nats", "size"))
    print(f"\n=== {title} ===")
    print(g.round(4).to_string())


def load_glob(pattern: str) -> pd.DataFrame:
    frames = []
    for p in sorted(glob.glob(str(REPO / "reports" / pattern))):
        df = pd.read_parquet(p)
        # te_pipeline stamps `case` as the .outb stem (IEA-15-240-RWT-UMaineSemi,
        # identical for every case); the real campaign id lives in the filename
        # te_wsrc_<caseid>.parquet. Recover it so per-case joins (analyze_phase2
        # Section 4) line up with the SURD table's case ids.
        m = re.match(r"te_wsrc_(.+)\.parquet$", Path(p).name)
        if m:
            df["case"] = m.group(1)
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=None,
                    help="write the merged per-case healthy table (RtVAvgxh + "
                         "Wind1VelX/Wave1Elev) to this parquet, for the SURD "
                         "join in analyze_phase2.py --te-table")
    args = ap.parse_args()

    rt = load_glob("te_wsrc_dlc*.parquet")       # RtVAvgxh full campaign (new); dlc* so a
                                                 # merged/derived te_wsrc_*.parquet is never re-ingested
    full = REPO / "reports" / "te_table_full.parquet"
    ft = pd.read_parquet(full) if full.exists() else pd.DataFrame()
    if not ft.empty:
        ft = ft[ft.source.isin(["Wind1VelX", "Wave1Elev"])]

    n_rt = rt.case.nunique() if not rt.empty else 0
    healthy = pd.concat([x for x in (rt, ft) if not x.empty], ignore_index=True)
    if healthy.empty:
        print("no data yet - run sims/rtvavg_full_campaign.sh (and/or check te_table_full.parquet)")
        return 1
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        healthy.to_parquet(args.out, compression="zstd")
        print(f"wrote merged healthy table -> {args.out} "
              f"({healthy['case'].nunique()} cases, {len(healthy)} rows)")
    summarize(healthy, f"HEALTHY corrected wind->structure  "
                       f"(RtVAvgxh: {n_rt} cases done; Wind1VelX/Wave1Elev from te_table_full)")

    # firewall under fault (RtVAvgxh -> PtfmPitch) from the reanalysis fault parquets
    frows = [pd.read_parquet(p) for p in sorted(glob.glob(str(REPO / "reports" / "te_rtvavg_*.parquet")))
             if FAULT.search(Path(p).stem.replace("te_rtvavg_", ""))]
    if frows:
        summarize(pd.concat(frows, ignore_index=True),
                  "FAULT cases: does the firewall hold with the correct (rotor-averaged) wind?")

    print("\nRead:")
    print("  RtVAvgxh -> platform ~0            => physical firewall (correct wind, healthy AND fault)")
    print("  RtVAvgxh -> blade/tower non-zero   => positive control (wind reaches the rotor)")
    print("  Wind1VelX -> everything ~0         => point-sensor observability limit")
    print("  Wave1Elev -> platform strong       => the platform IS a detectable target (it's wind that's blocked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
