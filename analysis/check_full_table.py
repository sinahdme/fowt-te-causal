#!/usr/bin/env python
"""Inspect the Phase 4 full-settings TE table on the compute server.

Run on lams after `git pull`:

    python analysis/check_full_table.py

Reports whether the full-settings rerun produced a usable table, its column
layout (so we can confirm conditional + Granger columns exist, not just
bivariate), case coverage, and which tau values were used for the slow-drift /
timeout-prone channels. The git HEAD line tells us whether this checkout has the
`_extract_te_pval` conditional-TE fix, so we know if any conditional rows already
in the table were produced by the corrected pipeline or the buggy `te[0]` path.
"""
import glob
import os
import subprocess
import sys

import pandas as pd


def _git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True).strip()
    except Exception as exc:  # pragma: no cover - diagnostic only
        return f"<git error: {exc}>"


def main() -> int:
    print("=== git HEAD (does this checkout have the _extract_te_pval fix?) ===")
    print(_git("log", "--oneline", "-1"))
    print(_git("status", "-s", "analysis/te_pipeline.py") or "(te_pipeline.py clean)")

    print("\n=== full-table artifacts ===")
    arts = sorted(glob.glob("reports/te_table_full*.parquet")) + \
        sorted(glob.glob("reports/te_v08_full.parquet"))
    for a in arts:
        st = os.stat(a)
        print(f"{a}\t{st.st_size:>12,} bytes\t{pd.Timestamp(st.st_mtime, unit='s')}")
    if not arts:
        print("(none found)")

    f = "reports/te_table_full.parquet"
    if not os.path.exists(f):
        parts = sorted(glob.glob("reports/te_table_full_p*.parquet"))
        print("\nno merged table; shards:", parts)
        f = parts[0] if parts else None

    print("\n=== contents ===")
    if not (f and os.path.exists(f)):
        print("NO full-settings table found at all -> launch run_phase4_full.sh")
        return 0

    df = pd.read_parquet(f)
    print("file:", f)
    print("rows:", len(df), "| cols:", list(df.columns))
    for c in ("case_id", "case", "source", "target"):
        if c in df.columns:
            print(f"{c} n_distinct: {df[c].nunique()}")
    for c in ("method", "te_type", "estimator", "direction"):
        if c in df.columns:
            print(c, "->", df[c].value_counts().to_dict())
    if "tau" in df.columns:
        print("tau values:", sorted(df["tau"].dropna().unique()))
    # Quick sanity on conditional rows, if a method/te_type column distinguishes them.
    for c in ("method", "te_type"):
        if c in df.columns and "te" in df.columns:
            cond_mask = df[c].astype(str).str.contains("cond", case=False, na=False)
            if cond_mask.any():
                print(f"conditional rows: {cond_mask.sum()} | "
                      f"te range {df.loc[cond_mask, 'te'].min():.4f}..{df.loc[cond_mask, 'te'].max():.4f}")
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
