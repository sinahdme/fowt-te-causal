"""compare_tau.py — diff two te_pipeline parquet tables (e.g. tau=1 vs tau=N).

Checks whether a thinned embedding (larger tau) preserves the science. Prints,
per (source, target), the bivariate KSG TE at each setting with the absolute
and % change, flags significance flips, and summarises how many of the
baseline's significant edges survive within a tolerance. Also diffs the
per-target AIS denominators.

Verdict logic: tau is "faithful" if every edge significant in the BASELINE is
still significant in the comparison and its TE magnitude moved less than --tol.

Usage:
    python analysis/compare_tau.py /tmp/te_probe_gpu.parquet /tmp/te_tau10.parquet
    python analysis/compare_tau.py base.parquet tau.parquet --method bivariate_te_ksg --tol 0.20
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def _ais(df: pd.DataFrame) -> pd.DataFrame:
    """Per-target AIS denominator (repeated across rows -> dedupe). `case` is
    intentionally dropped: the two files being compared are single-case runs
    whose case IDs differ (they come from different input paths), so we join on
    target/edge, not case."""
    return (df[["target", "ais_nats"]]
            .dropna(subset=["ais_nats"])
            .drop_duplicates())


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("baseline", type=Path, help="reference table (e.g. tau=1)")
    ap.add_argument("compare", type=Path, help="table to test (e.g. tau=10)")
    ap.add_argument("--method", default="bivariate_te_ksg")
    ap.add_argument("--tol", type=float, default=0.20,
                    help="fractional TE change above which an edge is 'shifted' "
                         "(default 0.20 = 20%%)")
    args = ap.parse_args()

    b = pd.read_parquet(args.baseline)
    c = pd.read_parquet(args.compare)
    blab, clab = args.baseline.name, args.compare.name

    # ---- AIS denominators ----
    a = (_ais(b).rename(columns={"ais_nats": "ais_base"})
         .merge(_ais(c).rename(columns={"ais_nats": "ais_cmp"}),
                on=["target"], how="outer"))
    with np.errstate(divide="ignore", invalid="ignore"):
        a["pct"] = 100 * (a["ais_cmp"] - a["ais_base"]) / a["ais_base"].abs()
    print(f"\n=== AIS denominator:  {blab}  vs  {clab} ===")
    print(f"{'target':<12}{'base':>10}{'cmp':>10}{'d%':>8}")
    print("-" * 40)
    for _, r in a.sort_values("target").iterrows():
        pct = r["pct"]
        pcts = "   -  " if not np.isfinite(pct) else f"{pct:>6.1f}"
        print(f"{r['target']:<12}{r['ais_base']:>10.4f}{r['ais_cmp']:>10.4f}{pcts:>8}")

    # ---- TE edges ----
    cols = ["source", "target", "te_nats", "p_value", "significant"]
    m = (b[b["method"] == args.method][cols]
         .merge(c[c["method"] == args.method][cols],
                on=["source", "target"],
                suffixes=("_base", "_cmp"), how="outer"))
    m["dTE"] = m["te_nats_cmp"] - m["te_nats_base"]
    with np.errstate(divide="ignore", invalid="ignore"):
        m["pct"] = 100 * m["dTE"] / m["te_nats_base"].abs()

    print(f"\n=== {args.method}:  {blab}  vs  {clab} ===")
    hdr = (f"{'source':<11}{'target':<11}{'TE_base':>9}{'TE_cmp':>9}"
           f"{'dTE':>9}{'d%':>7}  sig")
    print(hdr)
    print("-" * len(hdr))

    total_sig = preserved = flips = 0
    for _, r in m.sort_values("te_nats_base", ascending=False,
                              na_position="last").iterrows():
        sb, sc = bool(r["significant_base"]), bool(r["significant_cmp"])
        mark = ("S" if sb else ".") + "->" + ("S" if sc else ".")
        pct = r["pct"]
        pcts = "   -  " if not np.isfinite(pct) else f"{pct:>5.0f}%"
        flag = ""
        if sb:
            total_sig += 1
            moved = (not np.isfinite(pct)) or abs(pct) > args.tol * 100
            if sc and not moved:
                preserved += 1
            else:
                flag = "  <-- check"
                if not sc:
                    flips += 1
        print(f"{r['source']:<11}{str(r['target']):<11}"
              f"{r['te_nats_base']:>9.4f}{r['te_nats_cmp']:>9.4f}"
              f"{r['dTE']:>9.4f}{pcts:>7}  {mark}{flag}")

    print(f"\nBaseline-significant edges: {total_sig}  |  "
          f"preserved within {int(args.tol*100)}%: {preserved}  |  "
          f"significance flips: {flips}")
    if total_sig and preserved == total_sig:
        print(f"VERDICT: '{clab}' reproduces every baseline-significant edge "
              f"within tolerance -- tau is faithful; use it for production.")
    elif total_sig:
        print(f"VERDICT: {total_sig - preserved} of {total_sig} baseline-"
              f"significant edge(s) shifted >{int(args.tol*100)}% or flipped "
              f"between the two runs -- the edge set is NOT stable across the "
              f"change; read the per-edge rows rather than trusting either alone.")
    else:
        print("VERDICT: no significant edges in the baseline to check.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
