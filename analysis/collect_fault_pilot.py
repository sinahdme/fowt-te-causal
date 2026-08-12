#!/usr/bin/env python3
"""collect_fault_pilot.py - aggregate the pitch-fault pilot TE tables into one summary.

Reads the per-arm fault TE parquets (reports/te_fault_*.parquet) written by the pilot
(sims/run_fault_pilot.sh -> te_pipeline.py), extracts the wind->platform bivariate TE for
each arm, tests each against the healthy firewall ceiling, and prints a tidy breach table.
Optionally writes a CSV + a dose/response-style PNG (TE vs fault, by wind speed).

Usage:
    python analysis/collect_fault_pilot.py                        # globs reports/te_fault_*.parquet
    python analysis/collect_fault_pilot.py reports/te_fault_dlca_v15ms_s00_pitchlock.parquet ...
    python analysis/collect_fault_pilot.py --csv reports/fault_pilot_summary.csv --png reports/figs/fault_pilot.png

Breach criterion (same as analysis/compute_fault_te.py): for a platform target, mean
Wind1VelX->target TE > 0.029 nats AND permutation-significant (alpha=0.05).
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
try:  # reuse the exact healthy-baseline constants
    from compute_fault_te import HEALTHY_CEILING_NATS, PLATFORM_TARGETS
except Exception:  # pragma: no cover - fallback if not importable
    HEALTHY_CEILING_NATS = 0.029
    PLATFORM_TARGETS = ("PtfmPitch", "PtfmSurge", "PtfmHeave")

WIND_SRC = "Wind1VelX"
# case stem -> (wind m/s, seed, fault tag), e.g. dlca_v15ms_s00_pitchlock / dlc16_v11ms_s00_gain010
CASE_RE = re.compile(r"_v(\d+)ms_s(\d+)_([A-Za-z0-9]+)$")


def parse_case(case: str) -> dict:
    m = CASE_RE.search(case)
    if not m:
        return {"wind": None, "seed": None, "fault": None}
    return {"wind": int(m.group(1)), "seed": int(m.group(2)), "fault": m.group(3)}


def load_one(parq: Path) -> list[dict]:
    """One row per (arm, platform target) with wind->target TE + significance + breach."""
    df = pd.read_parquet(parq)
    ksg = df[(df.method == "bivariate_te_ksg") & (df.source == WIND_SRC)]
    rows = []
    for case, g in ksg.groupby("case"):
        meta = parse_case(str(case))
        for tgt in PLATFORM_TARGETS:
            d = g[g.target == tgt]
            te = float(d.te_nats.mean()) if not d.empty else float("nan")
            sig = bool((d.significant == True).any()) if not d.empty else False
            breach = (te > HEALTHY_CEILING_NATS) and sig
            rows.append({"case": case, **meta, "target": tgt,
                         "te_nats": te, "significant": sig, "breach": breach,
                         "parquet": parq.name})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("parquets", nargs="*", help="fault TE parquets (default: reports/te_fault_*.parquet)")
    ap.add_argument("--csv", type=Path, default=REPO / "reports" / "fault_pilot_summary.csv")
    ap.add_argument("--png", type=Path, default=REPO / "reports" / "figs" / "fault_pilot.png")
    ap.add_argument("--no-plot", action="store_true")
    args = ap.parse_args()

    paths = [Path(p) for p in args.parquets] or sorted(
        Path(p) for p in glob.glob(str(REPO / "reports" / "te_fault_*.parquet")))
    if not paths:
        print("No fault parquets found (reports/te_fault_*.parquet). Run the pilot first.",
              file=sys.stderr)
        return 1

    rows = []
    for p in paths:
        if not p.exists():
            print(f"  skip (missing): {p}"); continue
        try:
            rows.extend(load_one(p))
        except Exception as e:  # keep going; report which parquet failed
            print(f"  !! failed to read {p.name}: {e}", file=sys.stderr)
    if not rows:
        print("No usable rows extracted.", file=sys.stderr); return 1

    df = pd.DataFrame(rows).sort_values(["fault", "wind", "seed", "target"])
    df.to_csv(args.csv, index=False)

    # ---- console summary: wide table keyed on PtfmPitch, plus per-arm breach ----
    print(f"\nHealthy firewall ceiling: {HEALTHY_CEILING_NATS} nats "
          f"(breach = wind->platform TE above it AND significant)\n")
    pitch = df[df.target == "PtfmPitch"].copy()
    print("Per-arm wind->PtfmPitch (the headline firewall channel):")
    print(f"  {'arm':<28} {'wind':>5} {'seed':>4} {'TE_nats':>9} {'sig':>5} {'breach':>7}")
    for _, r in pitch.iterrows():
        print(f"  {str(r.case):<28} {str(r.wind):>5} {str(r.seed):>4} "
              f"{r.te_nats:>9.4f} {str(r.significant):>5} {str(r.breach):>7}")

    arm_breach = df.groupby("case").breach.any()
    n_breach = int(arm_breach.sum())
    print(f"\nArms with ANY platform-channel breach: {n_breach}/{len(arm_breach)}")
    if n_breach:
        print("  BREACHED:", ", ".join(arm_breach[arm_breach].index))
    # per fault-type x wind-speed roll-up (version-robust: no apply/include_groups)
    print("\nBreach rate by fault x wind (fraction of seed-arms breaching):")
    per_arm = df.groupby(["fault", "wind", "seed"]).breach.any().reset_index()
    grp = per_arm.groupby(["fault", "wind"]).breach.mean()
    for (fault, wind), frac in grp.items():
        print(f"  {fault:<12} {int(wind):>2} m/s : {frac*100:4.0f}%")

    print(f"\nWrote summary CSV: {args.csv}")

    # ---- optional plot: TE(Wind->PtfmPitch) per arm vs the ceiling ----
    if not args.no_plot:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import numpy as np
            args.png.parent.mkdir(parents=True, exist_ok=True)
            faults = sorted(pitch.fault.dropna().unique())
            fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
            for i, f in enumerate(faults):
                sub = pitch[pitch.fault == f]
                x = i + (sub.wind - sub.wind.min()) * 0.0 + np.linspace(-0.15, 0.15, len(sub))
                ax.scatter(x, sub.te_nats, s=40, label=f,
                           c=["#C00000" if b else "#1F3A5F" for b in sub.breach],
                           edgecolors="white", zorder=3)
            ax.axhline(HEALTHY_CEILING_NATS, color="#5B6470", ls=(0, (5, 3)), lw=1.2,
                       label=f"healthy ceiling ({HEALTHY_CEILING_NATS})")
            ax.set_xticks(range(len(faults)), faults)
            ax.set_ylabel("TE(Wind1VelX -> PtfmPitch)  [nats]")
            ax.set_title("Pitch-fault pilot: wind->platform TE vs firewall ceiling "
                         "(red = breach)", fontsize=11)
            ax.legend(fontsize=8, frameon=False)
            fig.tight_layout()
            fig.savefig(args.png)
            print(f"Wrote plot: {args.png}")
        except Exception as e:  # plotting is optional
            print(f"(plot skipped: {e})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
