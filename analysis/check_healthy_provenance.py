#!/usr/bin/env python3
"""check_healthy_provenance.py - what does the authoritative healthy te_table say for the
platform channels, and at what tau? Used to decide whether the fault pilot's --slow-drift-tau 5
is (a) consistent with the healthy ceiling's provenance and (b) not suppressing real edges.

Prints, for bivariate_te_ksg Wind1VelX/Wave1Elev -> PtfmPitch/Surge/Heave: mean/max te_nats,
%-significant, and the tau value(s) present. A strong Wave edge (~0.1) confirms the pipeline
detects platform coupling; if it's ~0 at tau=5 but non-zero at tau=1, tau=5 is over-suppressing.
"""
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
TABLE = REPO / "reports" / "te_table.parquet"
SRCS = ("Wind1VelX", "Wave1Elev")
TGTS = ("PtfmPitch", "PtfmSurge", "PtfmHeave")


def main() -> int:
    if not TABLE.exists():
        print(f"missing {TABLE}"); return 1
    d = pd.read_parquet(TABLE)
    print(f"te_table columns: {list(d.columns)}\n")
    k = d[d.method == "bivariate_te_ksg"]
    sub = k[k.source.isin(SRCS) & k.target.isin(TGTS)].copy()
    if sub.empty:
        print("no Wind/Wave -> platform bivariate_te_ksg rows found"); return 1

    has_tau = "tau" in d.columns
    aggs = {"mean_te": ("te_nats", "mean"), "max_te": ("te_nats", "max"),
            "pct_sig": ("significant", lambda s: 100.0 * s.mean()),
            "n": ("te_nats", "size")}
    g = sub.groupby(["source", "target"]).agg(**aggs)
    print(g.round(4).to_string())

    if has_tau:
        print("\nper (source,target) tau values in the healthy table:")
        for (s, t), rows in sub.groupby(["source", "target"]):
            taus = sorted(rows["tau"].dropna().unique().tolist())
            print(f"  {s:>10} -> {t:<10}: tau={taus}")
    else:
        print("\n(no 'tau' column in this table — likely the first-pass tau=1 table)")

    print("\nInterpretation: Wave->Ptfm* mean_te should be ~0.05-0.12 (strong coupling). "
          "If it's ~0 here, or only non-zero at tau=1 while the pilot used tau=5, then "
          "--slow-drift-tau 5 is suppressing edges and the fault pilot null is unreliable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
