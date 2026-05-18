"""
load_runs.py — OpenFAST .out / .outb → cleaned Parquet (Phase 3 + validation case 1).

Reads OpenFAST output files via openfast_toolbox.io.FASTOutputFile, returns
a pandas DataFrame with a Time column and one column per channel, and
optionally writes Parquet to data/.

Per PLAN.md Phase 3:
- Time-align all channels to a common grid (OpenFAST writes a regular grid
  already, so this is a sanity check, not a resample).
- Per-channel detrending / band-pass / z-scoring is done by the TE pipeline
  (analysis/te_pipeline.py), not here. This script is pure I/O.
- 1e-10 Gaussian jitter (kraskov-2004 §III.A) is also a TE-pipeline concern,
  not here.

Usage:
    python analysis/load_runs.py path/to/run.outb -o data/run.parquet
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def load_outb(path) -> pd.DataFrame:
    """Parse an OpenFAST .out / .outb file into a pandas DataFrame.

    Falls back from openfast_toolbox to a minimal text parser for plain
    .out files when openfast_toolbox isn't available, so the parsing
    smoke test (validation case 1) doesn't depend on the full env.
    """
    path = Path(path)
    try:
        from openfast_toolbox.io import FASTOutputFile
        # use_buffer=True forces per-column scaling, avoiding the
        # NumPy 2.x broadcast bug at line 617 of fast_output_file.py
        # (ColOff/ColScl shape (Nch,1) doesn't broadcast against (Nt,Nch)).
        df = FASTOutputFile(str(path), use_buffer=True).toDataFrame()
        return df
    except ImportError:
        pass

    if path.suffix.lower() == ".outb":
        raise RuntimeError(
            "openfast_toolbox is not installed; .outb (binary) needs it. "
            "Install via: pip install openfast-toolbox"
        )

    # Plain-text .out fallback parser (used in validation case 1 if needed).
    return _parse_text_out(path)


def _parse_text_out(path: Path) -> pd.DataFrame:
    """Minimal parser for OpenFAST text .out files.

    Format: header lines, then a column-name line, then a units line,
    then the data block (whitespace-separated floats).
    """
    with path.open("r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    # Find the start of the data block: the line after the units line.
    # OpenFAST writes headers ending with two lines: column names, then
    # parenthesised units. We find the units line by its '(' density.
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("(") and s.endswith(")") and i + 1 < len(lines):
            header_line = i - 1
            units_line = i
            data_start = i + 1
            break
    else:
        raise RuntimeError(f"could not locate column/units lines in {path}")
    cols = lines[header_line].split()
    data_rows = [ln.split() for ln in lines[data_start:] if ln.strip()]
    arr = np.array(data_rows, dtype=float)
    return pd.DataFrame(arr, columns=cols)


def find_time_column(df: pd.DataFrame) -> str:
    """Return the name of the time column.

    openfast_toolbox names columns `<Name>_[<units>]` (e.g., `Time_[s]`),
    whereas plain text .out files use bare names (`Time`). Accept either.
    """
    for col in df.columns:
        base = col.split("_[")[0] if "_[" in col else col
        if base.lower() == "time":
            return col
    raise KeyError(f"no 'Time' column found in {list(df.columns[:5])}...")


def validate_time_grid(df: pd.DataFrame) -> dict:
    """Return time-grid sanity-check stats. Used by validation case 1."""
    time_col = find_time_column(df)
    t = df[time_col].to_numpy()
    dt = np.diff(t)
    return {
        "n_samples": len(df),
        "n_channels": df.shape[1],
        "time_column": time_col,
        "t_start": float(t[0]),
        "t_end": float(t[-1]),
        "dt_mean": float(dt.mean()),
        "dt_std": float(dt.std()),
        "monotonic": bool(np.all(dt > 0)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to OpenFAST .out / .outb")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Parquet output path")
    parser.add_argument("--summary", action="store_true", help="Print time-grid summary")
    args = parser.parse_args()

    df = load_outb(args.input)
    print(f"Loaded {len(df)} rows × {df.shape[1]} channels from {args.input.name}")

    if args.summary:
        stats = validate_time_grid(df)
        for k, v in stats.items():
            print(f"  {k}: {v}")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(args.output, compression="zstd")
        # Round-trip sanity check
        df2 = pd.read_parquet(args.output)
        max_diff = float((df.values - df2.values).__abs__().max())
        print(f"Wrote {args.output}; round-trip max abs diff = {max_diff:.3e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
