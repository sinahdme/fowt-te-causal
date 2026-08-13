#!/usr/bin/env python3
"""collect_rtvavg.py - aggregate the RtVAvgxh re-analysis (reports/te_rtvavg_*.parquet) into a
source x target summary: Wind1VelX (point) vs RtVAvgxh (rotor-averaged) -> structure, split by
healthy vs fault. Shows the physical firewall (RtVAvgxh->platform ~0), the positive control
(RtVAvgxh->RootMyc1 fires), and the point-sensor observability limit (Wind1VelX ~0 everywhere).
"""
import glob
import re
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
FAULT = re.compile(r"_(pitchlock|gain\d+|stuckb\d)$")


def main() -> int:
    rows = []
    for p in sorted(glob.glob(str(REPO / "reports" / "te_rtvavg_*.parquet"))):
        label = Path(p).stem.replace("te_rtvavg_", "")
        grp = "fault" if FAULT.search(label) else "healthy"
        k = pd.read_parquet(p)
        k = k[k.method == "bivariate_te_ksg"]
        for _, r in k.iterrows():
            rows.append({"label": label, "grp": grp, "source": r.source,
                         "target": r.target, "te_nats": float(r.te_nats),
                         "significant": bool(r.significant)})
    if not rows:
        print("no reports/te_rtvavg_*.parquet found - run sims/rtvavg_reanalysis.sh first")
        return 1
    df = pd.DataFrame(rows)
    df.to_csv(REPO / "reports" / "rtvavg_summary.csv", index=False)

    for grp in ("healthy", "fault"):
        sub = df[df.grp == grp]
        if sub.empty:
            continue
        print(f"\n=== {grp}  ({sub.label.nunique()} cases) ===")
        g = sub.groupby(["source", "target"]).agg(
            mean_te=("te_nats", "mean"), max_te=("te_nats", "max"),
            pct_sig=("significant", lambda s: 100.0 * s.mean()),
            n=("te_nats", "size"))
        print(g.round(4).to_string())

    print("\nRead:")
    print("  RtVAvgxh -> platform (PtfmPitch/Surge/Heave) ~0  => PHYSICAL firewall (holds with the")
    print("    correct rotor-averaged wind; and under fault if the fault rows are ~0 too).")
    print("  RtVAvgxh -> RootMyc1 non-zero + significant       => POSITIVE CONTROL (wind reaches the")
    print("    blades; the estimator sees wind->structure where it is real).")
    print("  Wind1VelX ~0 on EVERYTHING                        => point-sensor observability limit")
    print("    (a hub anemometer is decorrelated from the rotor-averaged inflow).")
    print(f"\nWrote reports/rtvavg_summary.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
