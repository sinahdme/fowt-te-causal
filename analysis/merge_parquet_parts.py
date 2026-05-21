"""Merge per-worker Phase 4 parquet shards into a single te_table.parquet.

The parallel launcher (analysis/run_phase4_parallel.sh) spawns N
te_pipeline.py workers, each writing to reports/te_table_p<W>.parquet.
This script concatenates those into reports/te_table.parquet, the
canonical aggregate the rest of the pipeline (Phase 6 graph build,
publication figures) expects.

Usage:
    python analysis/merge_parquet_parts.py
"""

from __future__ import annotations

import glob
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
parts_dir = ROOT / "reports"
parts = sorted(parts_dir.glob("te_table_p*.parquet"))

if not parts:
    raise SystemExit(
        f"No te_table_p*.parquet files found under {parts_dir}. "
        f"Run analysis/run_phase4_parallel.sh first."
    )

print(f"Merging {len(parts)} parts:")
dfs: list[pd.DataFrame] = []
total_rows = 0
for p in parts:
    df = pd.read_parquet(p)
    print(f"  {p.name:32s}  {len(df):6d} rows")
    dfs.append(df)
    total_rows += len(df)

combined = pd.concat(dfs, ignore_index=True)

# Drop duplicates that can arise if a worker re-runs the same case
# (defensive — shouldn't happen with the round-robin allocation).
before = len(combined)
combined = combined.drop_duplicates(
    subset=["case", "source", "target", "method"], keep="last"
).reset_index(drop=True)
dedup_dropped = before - len(combined)
if dedup_dropped:
    print(f"  (dropped {dedup_dropped} duplicate (case, source, target, method) rows)")

out = parts_dir / "te_table.parquet"
combined.to_parquet(out, compression="zstd")
print(f"\nWrote {out}  ({len(combined)} rows total)")

# Quick sanity summary
n_cases = combined["case"].nunique()
n_methods = combined["method"].nunique()
n_pairs = combined.groupby(["source", "target"]).ngroups
print(f"  Cases:   {n_cases}")
print(f"  Methods: {n_methods}  ({sorted(combined['method'].unique())})")
print(f"  Pairs:   {n_pairs}")
