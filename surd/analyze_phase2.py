#!/usr/bin/env python
"""Cross-case analysis of the SURD Phase 2 firewall campaign.

Consumes reports/surd_table.parquet (surd/phase2_campaign.py) and, when
present, the first-pass reports/te_table.parquet for the SURD-vs-TE join.

Sections:
  1. Corrected controller leak drop @5 s by operating regime (wind speed),
     with per-regime gate pass rates.
  2. Closed-loop vs open-loop contrast (dlca_v11ms_s00_openloop natural
     experiment).
  3. R/U/S relocation statistics: U:BldPitch1 rank/share for future pitch,
     wind-involved information into the controller channels.
  4. Join with TE: cases where bivariate TE(Wind->PtfmPitch)=0 while the
     SURD corrected drop is positive (the firewall, seen by both methods).

Usage: python surd/analyze_phase2.py [--table reports/surd_table.parquet]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

HEADLINE_LAG = 25


def regime_of(case: str) -> str:
    m = re.search(r"_v(\d+)ms", case)
    return f"{int(m.group(1))} m/s" if m else "other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", type=Path,
                    default=Path("reports/surd_table.parquet"))
    ap.add_argument("--te-table", type=Path,
                    default=Path("reports/te_table.parquet"))
    args = ap.parse_args()

    df = pd.read_parquet(args.table)
    corr = df[(df.metric == "drop") & (df.term == "corrected")
              & (df.lag == HEADLINE_LAG)].copy()
    corr["regime"] = corr["case"].map(regime_of)
    corr["openloop"] = corr["case"].str.contains("openloop")
    gates = df[df.metric == "gate"].copy()
    gates["regime"] = gates["case"].map(regime_of)

    print("=" * 72)
    print("1. Corrected controller leak drop @5 s by operating regime")
    print("=" * 72)
    cl = corr[~corr.openloop]
    by = cl.groupby("regime")["value"]
    gate_by = (gates[~gates.case.str.contains("openloop")]
               .pivot_table(index="regime", columns="term", values="value",
                            aggfunc="mean"))
    tab = pd.DataFrame({
        "n": by.count(), "median": by.median(),
        "min": by.min(), "max": by.max(),
        "all_gates_pass_%": (gates[~gates.case.str.contains("openloop")]
                             .groupby(["regime", "case"])["value"].min()
                             .groupby("regime").mean() * 100),
    })
    print(tab.round(4).to_string())
    print("\nper-gate pass rates by regime (%):")
    print((gate_by * 100).round(0).to_string())
    rated = cl[cl.regime.isin(["11 m/s", "15 m/s", "20 m/s"])]["value"]
    below = cl[cl.regime == "8 m/s"]["value"]
    print(f"\nat/above rated vs below rated: median {rated.median():.4f} vs "
          f"{below.median():.4f} ({rated.median()/below.median():.1f}x); "
          f"positive in {(cl['value'] > 0).mean()*100:.0f}% of all "
          f"closed-loop cases")

    print()
    print("=" * 72)
    print("2. Natural experiment: controller ON vs OFF (dlca_v11ms_s00)")
    print("=" * 72)
    ol = corr[corr.openloop]
    if len(ol):
        sib = corr[corr.case.str.match(r"dlca_v11ms_s\d+$")]["value"]
        print(f"closed-loop dlca_v11ms_s00..05: "
              f"median {sib.median():.4f} (range {sib.min():.4f}"
              f"-{sib.max():.4f})")
        print(f"OPEN-LOOP dlca_v11ms_s00     : {ol['value'].iloc[0]:.4f}")
        print(f"-> switching the controller off removes "
              f"{(1 - ol['value'].iloc[0]/sib.median())*100:.0f}% of the "
              f"controller channels' corrected leak contribution")
        # U:BldPitch1 in the open-loop case (pitch frozen -> should die)
        u_bp = df[(df.metric == "rus") & (df.term == "U:BldPitch1")
                  & (df.lag == HEADLINE_LAG) & (df.target == "PtfmPitch")]
        u_ol = u_bp[u_bp.case.str.contains("openloop")]["value"]
        u_cl = u_bp[u_bp.case.str.match(r"dlca_v11ms_s\d+$")]["value"]
        print(f"U:BldPitch1 for future pitch: closed-loop median "
              f"{u_cl.median():.4f} vs open-loop {u_ol.iloc[0]:.4f}")

    print()
    print("=" * 72)
    print("3. R/U/S relocation statistics (closed-loop cases, @5 s)")
    print("=" * 72)
    rus = df[(df.metric == "rus") & (df.lag == HEADLINE_LAG)
             & (df.target == "PtfmPitch")
             & ~df.case.str.contains("openloop")]
    # Rank of U:BldPitch1 among all terms, per case
    ranks, shares = [], []
    for case, g in rus.groupby("case"):
        g = g.sort_values("value", ascending=False).reset_index()
        idx = g.index[g.term == "U:BldPitch1"]
        if len(idx):
            ranks.append(idx[0] + 1)
            shares.append(g.loc[idx[0], "value"])
    print(f"U:BldPitch1 rank among ~{rus.groupby('case').size().median():.0f}"
          f" terms: median #{np.median(ranks):.0f} "
          f"(top-1 in {(np.array(ranks) == 1).mean()*100:.0f}% of cases, "
          f"top-3 in {(np.array(ranks) <= 3).mean()*100:.0f}%)")
    print(f"U:BldPitch1 normalized value: median {np.median(shares):.4f}")
    wt = df[(df.metric == "drop") & (df.term == "wind_total")
            & ~df.case.str.contains("openloop")]
    for tgt, g in wt.groupby("target"):
        print(f"wind-involved info into {tgt}: median {g['value'].median():.4f}"
              f" (IQR {g['value'].quantile(.25):.4f}-"
              f"{g['value'].quantile(.75):.4f})")

    if args.te_table.exists():
        print()
        print("=" * 72)
        print("4. SURD vs TE join (first-pass bivariate KSG)")
        print("=" * 72)
        te = pd.read_parquet(args.te_table)
        wp = te[(te.source == "Wind1VelX") & (te.target == "PtfmPitch")
                & (te.method == "bivariate_te_ksg")][
                    ["case", "te_nats", "significant"]]
        j = corr.merge(wp, on="case", how="inner",
                       suffixes=("_surd", "_te"))
        n_null = (j.te_nats == 0).sum()
        n_fw = ((j.te_nats == 0) & (j.value > 0.02)).sum()
        print(f"{len(j)} joined cases: TE(Wind->PtfmPitch)=0 in {n_null}; "
              f"of those, SURD corrected drop >0.02 in {n_fw} "
              f"({n_fw/max(n_null,1)*100:.0f}%)")
        print("-> the TE null coexists with a measured controller-mediated "
              "path in the same cases: firewall, not absence of coupling.")
        nz = j[j.te_nats > 0]
        if len(nz):
            print(f"cases with nonzero TE(Wind->PtfmPitch): "
                  f"{nz['case'].tolist()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
