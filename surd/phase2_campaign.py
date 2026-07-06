#!/usr/bin/env python
"""Phase 2 of the SURD subproject (surd/PLAN.md), firewall-focused width.

Runs the validated Phase 1 firewall analysis (surd_runner.py, --pitch-rate
mode) across every case given, and writes one long-form parquet mirroring
te_table's join keys (case, target), so SURD vs TE is a direct join.

Frozen configuration (the config that passed the Phase 1 gate):
  TE-parity preprocessing (600 s drop, 5 Hz, jitter), nbins=3 (7-D hist =
  2187 cells vs ~15k samples), uniform bins, lags {1,3,6,12,25} = 0.2-5 s,
  pitch-rate in the observed self-state block, 3 circular-shift controls.

Schema (one row per case x target x lag x metric x term):
  case, target, lag, lag_s, metric, term, value, nbins, hz, n_samples
  - metric='leak'  term in {nostate, reduced, full, control}
  - metric='drop'  term in {raw, corrected}
  - metric='rus'   term like 'U:BldPitch1' (normalized by max MI; the full
                   observed group for PtfmPitch, upstream groups for the
                   controller targets)
  - metric='gate'  term = check name, value 1.0/0.0 (per-case Phase 1 gate)

Output checkpoints after EVERY case (crash loses at most the case in
flight). Runtime ~5 s/case on one CPU core; safe to run on lams alongside
the GPU TE campaign.

Usage:
  python surd/phase2_campaign.py sims/*/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb \
      -o reports/surd_table.parquet
"""
from __future__ import annotations

import argparse
import glob as globmod
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from surd_runner import (CONTROLLER, DRIVERS, RATE, TARGET,  # noqa: E402
                         decompose, load_channels, norm_terms)

NBINS = 3
HZ = 5.0
LAGS = [1, 3, 6, 12, 25]
N_CONTROLS = 3
HEADLINE_LAG = 25  # 5 s: where the corrected drop peaked in Phase 1


def run_case(outb: Path) -> tuple[str, list[dict]]:
    case, X, _ = load_channels(outb, HZ, with_rate=True)
    n = len(X[TARGET])

    state = [TARGET, RATE]
    reduced_names = state + DRIVERS
    full_names = state + DRIVERS + CONTROLLER
    reduced = np.vstack([X[c] for c in reduced_names])
    full = np.vstack([X[c] for c in full_names])
    nostate = np.vstack([X[c] for c in [TARGET] + DRIVERS])
    ctrl_rows = [full_names.index(c) for c in CONTROLLER]

    rows: list[dict] = []

    def add(target, lag, metric, term, value):
        rows.append({"case": case, "target": target, "lag": int(lag),
                     "lag_s": lag / HZ, "metric": metric, "term": term,
                     "value": float(value), "nbins": NBINS, "hz": HZ,
                     "n_samples": int(n)})

    per_lag = {}
    for lag in LAGS:
        _, _, _, leak_nost = decompose(X[TARGET], nostate, lag, NBINS)
        _, _, _, leak_red = decompose(X[TARGET], reduced, lag, NBINS)
        I_R, I_S, MI, leak_full = decompose(X[TARGET], full, lag, NBINS)

        ctrl_leaks = []
        for k in range(N_CONTROLS):
            rng = np.random.default_rng(1000 + k)
            shifted = full.copy()
            for row in ctrl_rows:
                shifted[row] = np.roll(shifted[row],
                                       rng.integers(n // 4, 3 * n // 4))
            _, _, _, lk = decompose(X[TARGET], shifted, lag, NBINS)
            ctrl_leaks.append(lk)
        leak_ctrl = float(np.mean(ctrl_leaks))

        add(TARGET, lag, "leak", "nostate", leak_nost)
        add(TARGET, lag, "leak", "reduced", leak_red)
        add(TARGET, lag, "leak", "full", leak_full)
        add(TARGET, lag, "leak", "control", leak_ctrl)
        add(TARGET, lag, "drop", "raw", leak_red - leak_full)
        add(TARGET, lag, "drop", "corrected", leak_ctrl - leak_full)
        for term, v in norm_terms(I_R, I_S, MI, full_names).items():
            add(TARGET, lag, "rus", term, v)
        per_lag[lag] = {"nostate": leak_nost, "reduced": leak_red,
                        "corrected": leak_ctrl - leak_full}

    # Upstream links (wind into the controller channels) at the headline lag.
    chans = [TARGET, RATE] + DRIVERS + CONTROLLER
    wind_totals = {}
    for up_tgt in CONTROLLER:
        names = [up_tgt] + [c for c in chans if c != up_tgt]
        agents = np.vstack([X[c] for c in names])
        I_R, I_S, MI, leak = decompose(X[up_tgt], agents, HEADLINE_LAG, NBINS)
        add(up_tgt, HEADLINE_LAG, "leak", "full", leak)
        terms = norm_terms(I_R, I_S, MI, names)
        for term, v in terms.items():
            add(up_tgt, HEADLINE_LAG, "rus", term, v)
        wind_totals[up_tgt] = sum(v for k, v in terms.items()
                                  if "Wind1VelX" in k and v > 0.001)
        add(up_tgt, HEADLINE_LAG, "drop", "wind_total", wind_totals[up_tgt])

    # Per-case Phase 1 gate (same rules as surd_runner --pitch-rate mode).
    hb = per_lag[HEADLINE_LAG]
    closure_peak = max(per_lag[l]["nostate"] - per_lag[l]["reduced"]
                       for l in LAGS)
    thresh = max(0.02, 0.05 * hb["reduced"])
    gates = {
        "state_info": closure_peak > 0.05,
        "controller_drop_material": hb["corrected"] > thresh,
        "wind_into_controllers": all(v > 0.01 for v in wind_totals.values()),
    }
    for gname, ok in gates.items():
        add(TARGET, HEADLINE_LAG, "gate", gname, 1.0 if ok else 0.0)

    return case, rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs", nargs="+",
                    help=".outb paths (globs expanded internally on Windows)")
    ap.add_argument("-o", "--output", type=Path,
                    default=Path("reports/surd_table.parquet"))
    args = ap.parse_args()

    files: list[Path] = []
    for pat in args.inputs:
        hits = sorted(globmod.glob(pat))
        files.extend(Path(h) for h in hits) if hits else files.append(Path(pat))
    print(f"{len(files)} case file(s); frozen config: {HZ} Hz, nbins={NBINS}, "
          f"lags={LAGS}, {N_CONTROLS} controls, pitch-rate ON", flush=True)

    all_rows: list[dict] = []
    t0 = time.time()
    for i, f in enumerate(files, 1):
        tc = time.time()
        try:
            case, rows = run_case(f)
        except Exception as e:  # keep the campaign alive past one bad case
            print(f"[{i}/{len(files)}] !! {f}: {type(e).__name__}: {e}",
                  file=sys.stderr, flush=True)
            continue
        all_rows.extend(rows)
        gates = {r["term"]: r["value"] for r in rows if r["metric"] == "gate"}
        corr = next(r["value"] for r in rows
                    if r["metric"] == "drop" and r["term"] == "corrected"
                    and r["lag"] == HEADLINE_LAG)
        print(f"[{i}/{len(files)}] {case}: corrected drop @5s = {corr:+.4f}, "
              f"gates {int(sum(gates.values()))}/{len(gates)} "
              f"({time.time()-tc:.1f}s)", flush=True)
        # Checkpoint after every case.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(all_rows).to_parquet(args.output, compression="zstd")

    if not all_rows:
        print("No cases produced results.", file=sys.stderr)
        return 1

    df = pd.DataFrame(all_rows)
    corr = df[(df.metric == "drop") & (df.term == "corrected")
              & (df.lag == HEADLINE_LAG)]
    gates = df[df.metric == "gate"].groupby("term")["value"].mean()
    print(f"\nWrote {args.output}: {len(df)} rows, "
          f"{df['case'].nunique()} cases ({time.time()-t0:.0f}s)", flush=True)
    print(f"corrected drop @5s: median {corr['value'].median():.4f}, "
          f"IQR [{corr['value'].quantile(.25):.4f}, "
          f"{corr['value'].quantile(.75):.4f}], "
          f"positive in {(corr['value'] > 0).mean()*100:.0f}% of cases",
          flush=True)
    print("gate pass rates: "
          + ", ".join(f"{k}={v*100:.0f}%" for k, v in gates.items()),
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
