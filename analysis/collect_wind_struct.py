#!/usr/bin/env python3
"""collect_wind_struct.py - the CORRECTED wind->structure table for the paper.

Merges the RtVAvgxh full campaign (reports/te_wsrc_*.parquet, rotor-averaged wind) with the
existing te_table_full (Wind1VelX point wind + Wave1Elev) at the same settings, into one
source x target summary over the healthy population. Also reports the firewall under fault
(RtVAvgxh -> PtfmPitch, from the reanalysis reports/te_rtvavg_<fault>.parquet).

Works on partial results (run anytime during the campaign).
"""
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
    frames = [pd.read_parquet(p) for p in sorted(glob.glob(str(REPO / "reports" / pattern)))]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def main() -> int:
    rt = load_glob("te_wsrc_*.parquet")          # RtVAvgxh full campaign (new)
    full = REPO / "reports" / "te_table_full.parquet"
    ft = pd.read_parquet(full) if full.exists() else pd.DataFrame()
    if not ft.empty:
        ft = ft[ft.source.isin(["Wind1VelX", "Wave1Elev"])]

    n_rt = rt.case.nunique() if not rt.empty else 0
    healthy = pd.concat([x for x in (rt, ft) if not x.empty], ignore_index=True)
    if healthy.empty:
        print("no data yet - run sims/rtvavg_full_campaign.sh (and/or check te_table_full.parquet)")
        return 1
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
