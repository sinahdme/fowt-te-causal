#!/usr/bin/env python
"""Assemble the pitch-control fault-detection signature table (paper Phase 1).

The two-sided signature, per case:

    SILENCE     TE(Wind1VelX -> PtfmPitch) insignificant / ~0
    ABSORPTION  wind information demonstrably entering the actuator:
                TE(Wind1VelX -> BldPitch1) significant (preferred leg), and/or
                SURD wind-involved info into BldPitch1 - WITH degeneracy guard.

    healthy = silence AND absorption       (controller absorbing the wind)
    idle    = silence AND weak absorption  (below rated: nothing to absorb)
    broken  = silence AND NO absorption    (pitch frozen: emulated lock fault)
    leak    = NO silence                   (wind reaching the platform)

Degeneracy guard (found 2026-07-06, worth a methods paragraph): for the
open-loop twin, BldPitch1 is constant + estimator jitter, so the SURD
histogram runs on noise - leak(BldPitch1)=0.97 and the normalized shares
are spurious high-order synergy (wind_total 0.851, the HIGHEST of all
cases). Normalized information shares cannot be trusted when the target
channel is (near-)degenerate: gate on leak(full) > LEAK_DEGENERATE before
reading them. The TE leg is immune (surrogate test on a constant channel
-> insignificant), which is why the TE leg is the arbiter.

Inputs:  reports/surd_table.parquet          (SURD Phase 2, committed)
         reports/te_table.parquet            (first-pass TE, committed)
         reports/te_signature_edges.parquet  (analysis/te_signature_edges.py;
                                              optional - columns filled NaN
                                              until computed)
Output:  reports/monitor_signature.parquet + Gate-1 report on stdout.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

HEADLINE_LAG = 25          # 5 s at 5 Hz (SURD table convention)
LEAK_DEGENERATE = 0.90     # leak(full) above this => target ~degenerate
ABSORB_SURD_MIN = 0.15     # wind_total into BldPitch1, guarded
DROP_MIN = 0.02            # corrected controller leak drop materiality


def regime_of(case: str) -> str:
    m = re.search(r"_v(\d+)ms", case)
    return f"{int(m.group(1))} m/s" if m else "other"


def population_of(case: str) -> str:
    if "openloop" in case:
        return "broken (pitch lock)"
    if regime_of(case) == "8 m/s":
        return "idle (below rated)"
    return "healthy (control active)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surd", type=Path, default=Path("reports/surd_table.parquet"))
    ap.add_argument("--te", type=Path, default=Path("reports/te_table.parquet"))
    ap.add_argument("--edges", type=Path,
                    default=Path("reports/te_signature_edges.parquet"))
    ap.add_argument("-o", "--output", type=Path,
                    default=Path("reports/monitor_signature.parquet"))
    args = ap.parse_args()

    surd = pd.read_parquet(args.surd)
    te = pd.read_parquet(args.te)

    cases = sorted(surd.case.unique())
    rows = []

    # --- silence leg: TE(wind -> PtfmPitch), first-pass table -----------------
    sil = te[(te.source == "Wind1VelX") & (te.target == "PtfmPitch")
             & (te.method == "bivariate_te_ksg")].set_index("case")

    # --- absorption leg (TE): wind -> BldPitch1, from the edges run -----------
    ab_te = pd.DataFrame()
    if args.edges.exists():
        edges = pd.read_parquet(args.edges)
        ab_te = edges[(edges.source == "Wind1VelX")
                      & (edges.target == "BldPitch1")
                      & (edges.method == "bivariate_te_ksg")].set_index("case")
        # silence leg for cases absent from te_table (the open-loop twin)
        sil_extra = edges[(edges.source == "Wind1VelX")
                          & (edges.target == "PtfmPitch")
                          & (edges.method == "bivariate_te_ksg")].set_index("case")
        sil = pd.concat([sil, sil_extra[~sil_extra.index.isin(sil.index)]])

    # --- SURD legs -------------------------------------------------------------
    wt = surd[(surd.metric == "drop") & (surd.term == "wind_total")
              & (surd.target == "BldPitch1")
              & (surd.lag == HEADLINE_LAG)].set_index("case")["value"]
    leak_bp = surd[(surd.metric == "leak") & (surd.target == "BldPitch1")
                   & (surd.term == "full")
                   & (surd.lag == HEADLINE_LAG)].set_index("case")["value"]
    drop = surd[(surd.metric == "drop") & (surd.term == "corrected")
                & (surd.lag == HEADLINE_LAG)].set_index("case")["value"]
    ubp = surd[(surd.metric == "rus") & (surd.term == "U:BldPitch1")
               & (surd.target == "PtfmPitch")
               & (surd.lag == HEADLINE_LAG)].set_index("case")["value"]

    for case in cases:
        te_sil = sil["te_nats"].get(case, np.nan)
        te_sil_sig = bool(sil["significant"].get(case, False)) \
            if case in sil.index else None
        te_ab = ab_te["te_nats"].get(case, np.nan) if len(ab_te) else np.nan
        te_ab_sig = bool(ab_te["significant"].get(case, False)) \
            if len(ab_te) and case in ab_te.index else None

        degenerate = bool(leak_bp.get(case, np.nan) > LEAK_DEGENERATE)
        wt_val = wt.get(case, np.nan)
        surd_absorb = (not degenerate) and (wt_val > ABSORB_SURD_MIN)

        # classification: TE absorption leg is the arbiter when available;
        # SURD leg (guarded) is the fallback so the table works pre-edges-run.
        silence = (te_sil_sig is False) or (te_sil == 0)
        if te_ab_sig is not None:
            absorption = te_ab_sig
        else:
            absorption = surd_absorb
        # graded absorption strength separates idle from healthy
        strong_absorb = absorption and (drop.get(case, 0) > DROP_MIN)

        if te_sil_sig is None and np.isnan(te_sil):
            label = "pending TE legs"
        elif not silence:
            label = "flag: wind reaching platform"
        elif strong_absorb:
            label = "healthy"
        elif absorption:
            label = "idle-or-weak"
        else:
            label = "no absorption (fault)"

        rows.append({
            "case": case,
            "regime": regime_of(case),
            "population": population_of(case),
            "te_wind_pitch": te_sil, "te_wind_pitch_sig": te_sil_sig,
            "te_wind_bldpitch": te_ab, "te_wind_bldpitch_sig": te_ab_sig,
            "surd_wind_into_bldpitch": wt_val,
            "bldpitch_leak_full": leak_bp.get(case, np.nan),
            "bldpitch_degenerate": degenerate,
            "surd_corrected_drop": drop.get(case, np.nan),
            "surd_u_bldpitch": ubp.get(case, np.nan),
            "label": label,
        })

    out = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(args.output, index=False)

    print("=" * 78)
    print("Signature table:", args.output, f"({len(out)} cases)")
    print("TE absorption leg computed:" ,
          "YES" if len(ab_te) else "NO - SURD fallback in use "
          "(run analysis/te_signature_edges.py)")
    print("=" * 78)
    print(pd.crosstab(out.population, out.label).to_string())
    print()
    med = out.groupby("population")[
        ["te_wind_pitch", "te_wind_bldpitch", "surd_wind_into_bldpitch",
         "surd_corrected_drop", "surd_u_bldpitch"]].median()
    print(med.round(4).to_string())

    # ---- Gate 1 ---------------------------------------------------------------
    print()
    misfits = []
    for _, r in out.iterrows():
        pop, lab = r.population, r.label
        if lab == "pending TE legs":
            continue  # not evaluable until the edges run lands
        ok = (pop.startswith("healthy") and lab in ("healthy",
                                                    "flag: wind reaching platform")) \
            or (pop.startswith("idle") and lab in ("idle-or-weak", "healthy")) \
            or (pop.startswith("broken") and lab in ("no absorption (fault)",
                                                     "flag: wind reaching platform"))
        if not ok:
            misfits.append((r.case, pop, lab))
    if misfits:
        print(f"GATE 1: {len(misfits)} misclassification(s):")
        for c, p, l in misfits:
            print(f"  {c}: population={p} label={l}")
    else:
        print("GATE 1 PASS: all populations classified consistently "
              "(leak cases flagged by design).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
