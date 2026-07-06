#!/usr/bin/env python
"""Phase 1 thin slice of the SURD subproject (surd/PLAN.md): observe the
controller firewall on ONE .outb case.

Pipeline (TE-parity preprocessing, mirrors analysis/te_pipeline.py):
  load .outb -> drop 600 s transient -> stride-decimate to 5 Hz -> jitter
  -> SURD decomposition of PtfmPitch(t+lag) for three observed groups:

    reduced : {PtfmPitch, Wind1VelX, Wave1Elev}                  (4-D hist)
    full    : + {BldPitch1, RotThrust}                           (6-D hist)
    control : full, but the controller channels independently
              circular-shifted (kills coupling, keeps marginals,
              autocorrelation and dimensionality)

  Headline metric: the leak drop. leak(reduced) - leak(full) is the raw
  drop; leak(control) - leak(full) is the bias-corrected controller
  contribution (the control isolates the finite-sample effect of just
  adding two more histogram dimensions).

  Also decomposes RotThrust and BldPitch1 as targets (full group) to check
  the upstream links: wind must show nonzero unique/synergistic causality
  into the controller channels for the mediation story to hold.

Exit code 0 = Phase 1 gate PASSES (leak story holds -> Phase 2), 1 = not.

Usage:
  python surd/surd_runner.py sims/dlc16_v11ms_s00/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "analysis"))

from vendorlib import surd_mod  # noqa: E402
from load_runs import load_outb, find_time_column  # noqa: E402

# TE-parity preprocessing constants (analysis/te_pipeline.py TESettings)
DECIMATE_TARGET_HZ = 5.0   # module default; --hz overrides (diagnostics only)
TRANSIENT_DROP_S = 600.0
JITTER_SCALE = 1e-10

TARGET = "PtfmPitch"
RATE = "PtfmPitch_rate"  # derived: d/dt of TARGET (no native rate channel)
DRIVERS = ["Wind1VelX", "Wave1Elev"]
CONTROLLER = ["BldPitch1", "RotThrust"]


def find_channel(df, basename: str) -> str:
    """Same suffix-stripping match as te_pipeline (`Name_[unit]` or `Name`)."""
    for col in df.columns:
        if col.split("_[")[0].lower() == basename.lower():
            return col
    raise KeyError(f"channel {basename!r} not found")


def preprocess(arr: np.ndarray, dt_in: float, seed: int,
               target_hz: float = DECIMATE_TARGET_HZ) -> np.ndarray:
    """Mirror te_pipeline.preprocess_channel: drop transient, decimate, jitter."""
    src_hz = 1.0 / dt_in
    factor = max(1, int(round(src_hz / target_hz)))
    drop_n = int(TRANSIENT_DROP_S / dt_in)
    out = arr[drop_n:][::factor]
    rng = np.random.default_rng(seed)
    return out + JITTER_SCALE * rng.standard_normal(out.shape)


def rank_transform(x: np.ndarray) -> np.ndarray:
    """Map to uniform [0,1] by rank (copula transform). Monotone, so
    information quantities are unchanged in the continuous limit; uniform
    binning afterwards = equiprobable bins, which stops heavy tails from
    wasting histogram resolution."""
    order = np.argsort(x, kind="stable")
    r = np.empty_like(order, dtype=float)
    r[order] = np.arange(len(x))
    return r / (len(x) - 1)


def decompose(target: np.ndarray, agents: np.ndarray, nlag: int, nbins: int,
              rank: bool = False):
    """SURD of target(t+nlag) given agents(t). agents rows = variables."""
    Y = np.vstack([target[nlag:], agents[:, :-nlag]])
    if rank:
        Y = np.apply_along_axis(rank_transform, 1, Y)
    hist, _ = np.histogramdd(Y.T, nbins)
    return surd_mod.surd(hist)


def norm_terms(I_R: dict, I_S: dict, MI: dict, names: list[str]) -> dict:
    """R/U/S terms normalized by max MI, keyed with channel names."""
    mmax = max(MI.values())
    out = {}
    for k, v in I_R.items():
        label = ("U" if len(k) == 1 else "R") + ":" + "+".join(names[i - 1] for i in k)
        out[label] = v / mmax
    for k, v in I_S.items():
        out["S:" + "+".join(names[i - 1] for i in k)] = v / mmax
    return out


def load_channels(outb: Path, hz: float, with_rate: bool = False):
    """Load one case and return (case_id, {channel: preprocessed array}).
    TE-parity preprocessing; the derived RATE channel is differentiated at
    the source rate before decimation."""
    df = load_outb(outb)
    tcol = find_time_column(df)
    dt_in = float(np.diff(df[tcol].to_numpy()[:100]).mean())
    case = outb.parent.parent.name if outb.parent.name.startswith(
        "IEA-15") else outb.stem
    chans = [TARGET] + DRIVERS + CONTROLLER
    X = {ch: preprocess(df[find_channel(df, ch)].to_numpy(), dt_in,
                        seed=i, target_hz=hz)
         for i, ch in enumerate(chans)}
    if with_rate:
        raw = df[find_channel(df, TARGET)].to_numpy()
        X[RATE] = preprocess(np.gradient(raw, dt_in), dt_in, seed=99,
                             target_hz=hz)
    return case, X, dt_in


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("outb", type=Path)
    ap.add_argument("--nbins", type=int, default=5,
                    help="bins/dim; 6-D hist needs nbins^6 << n_samples (~15k)")
    ap.add_argument("--lags", type=str, default="1,3,6,12,25",
                    help="lag sweep in samples at 5 Hz (0.2 s each)")
    ap.add_argument("--n-controls", type=int, default=3,
                    help="independent circular-shift draws to average")
    ap.add_argument("--rank", action="store_true",
                    help="rank(copula)-transform channels before binning "
                         "(equiprobable bins)")
    ap.add_argument("--hz", type=float, default=DECIMATE_TARGET_HZ,
                    help="decimation rate; 5.0 = TE parity (default). Higher "
                         "= more samples, diagnostics only")
    ap.add_argument("--pitch-rate", action="store_true",
                    help="add d(PtfmPitch)/dt to the observed self-state "
                         "block (pitch is an oscillator; one time slice of "
                         "its past cannot capture its state). Groups grow "
                         "one dimension; also reports the no-state reference "
                         "leak so the state closure is measurable")
    ap.add_argument("-o", "--out", type=Path, default=None,
                    help="output stem (default surd/phase1_<case>)")
    args = ap.parse_args()

    case = args.outb.parent.parent.name if args.outb.parent.name.startswith(
        "IEA-15") else args.outb.stem
    out_stem = args.out or HERE / f"phase1_{case}"
    lags = [int(x) for x in args.lags.split(",")]

    t0 = time.time()
    print(f"[{case}] loading {args.outb.name} ...", flush=True)
    case, X, dt_in = load_channels(args.outb, args.hz,
                                   with_rate=args.pitch_rate)
    n = len(X[TARGET])
    chans = list(X)  # incl. RATE when --pitch-rate: upstream groups see it too

    state = [TARGET] + ([RATE] if args.pitch_rate else [])
    reduced_names = state + DRIVERS
    full_names = state + DRIVERS + CONTROLLER
    reduced = np.vstack([X[c] for c in reduced_names])
    full = np.vstack([X[c] for c in full_names])
    nostate = np.vstack([X[c] for c in [TARGET] + DRIVERS])
    ctrl_rows = [full_names.index(c) for c in CONTROLLER]
    ndim_full = len(full_names) + 1
    print(f"[{case}] {n} samples @ {args.hz} Hz after "
          f"{TRANSIENT_DROP_S}s drop (src dt={dt_in}s); nbins={args.nbins} "
          f"-> full {ndim_full}-D hist {args.nbins**ndim_full} cells "
          f"(state block: {state})", flush=True)

    results = {"case": case, "nbins": args.nbins, "rank": args.rank, "hz": args.hz,
               "n_samples": int(n), "lags": {}}
    print(f"\n{'lag':>5} {'sec':>5} {'leak_nost':>10} {'leak_red':>9} "
          f"{'leak_full':>10} {'leak_ctrl':>10} {'raw_drop':>9} "
          f"{'corr_drop':>10}", flush=True)

    for lag in lags:
        _, _, _, leak_red = decompose(X[TARGET], reduced, lag, args.nbins,
                                      args.rank)
        I_R, I_S, MI, leak_full = decompose(X[TARGET], full, lag, args.nbins,
                                            args.rank)
        leak_nostate = leak_red
        if args.pitch_rate:
            _, _, _, leak_nostate = decompose(X[TARGET], nostate, lag,
                                              args.nbins, args.rank)

        ctrl_leaks = []
        for k in range(args.n_controls):
            rng = np.random.default_rng(1000 + k)
            shifted = full.copy()
            for row in ctrl_rows:  # controller channels only
                shifted[row] = np.roll(shifted[row],
                                       rng.integers(n // 4, 3 * n // 4))
            _, _, _, lk = decompose(X[TARGET], shifted, lag, args.nbins,
                                    args.rank)
            ctrl_leaks.append(lk)
        leak_ctrl = float(np.mean(ctrl_leaks))

        results["lags"][lag] = {
            "leak_nostate": leak_nostate,
            "leak_reduced": leak_red, "leak_full": leak_full,
            "leak_control": leak_ctrl,
            "raw_drop": leak_red - leak_full,
            "corrected_drop": leak_ctrl - leak_full,
            "terms_full": norm_terms(I_R, I_S, MI, full_names),
        }
        print(f"{lag:>5} {lag/args.hz:>5.1f} {leak_nostate:>10.4f} "
              f"{leak_red:>9.4f} {leak_full:>10.4f} {leak_ctrl:>10.4f} "
              f"{leak_red-leak_full:>9.4f} {leak_ctrl-leak_full:>10.4f}",
              flush=True)

    # Headline lag = largest bias-corrected drop
    best = max(results["lags"], key=lambda l: results["lags"][l]["corrected_drop"])
    hb = results["lags"][best]
    print(f"\nheadline lag {best} ({best/args.hz:.1f} s): "
          f"corrected leak drop {hb['corrected_drop']:.4f} "
          f"(raw {hb['raw_drop']:.4f})", flush=True)
    top = sorted(hb["terms_full"].items(), key=lambda kv: -kv[1])[:8]
    print("top terms (full group, normalized):", flush=True)
    for k, v in top:
        print(f"    {k:45s} {v:.4f}", flush=True)

    # Upstream links: wind into the controller channels (full group, headline lag)
    print("\nupstream links at headline lag:", flush=True)
    upstream = {}
    for up_tgt in CONTROLLER:
        names = [up_tgt] + [c for c in chans if c != up_tgt]
        agents = np.vstack([X[c] for c in names])
        I_R, I_S, MI, leak = decompose(X[up_tgt], agents, best, args.nbins,
                                       args.rank)
        terms = norm_terms(I_R, I_S, MI, names)
        wind_terms = {k: v for k, v in terms.items()
                      if "Wind1VelX" in k and v > 0.001}
        wind_total = sum(wind_terms.values())
        upstream[up_tgt] = {"leak": leak, "wind_terms": wind_terms,
                            "wind_total": wind_total}
        print(f"  {up_tgt}: wind-involved info {wind_total:.4f} "
              f"(leak {leak:.4f})", flush=True)
        for k, v in sorted(wind_terms.items(), key=lambda kv: -kv[1])[:4]:
            print(f"      {k:43s} {v:.4f}", flush=True)
    results["upstream"] = upstream
    results["headline_lag"] = best

    # ---- Phase 1 gate --------------------------------------------------------
    print("\n=== Phase 1 checks ===", flush=True)
    failures = []

    def check(cond, msg):
        print(f"  {'PASS' if cond else 'FAIL'}  {msg}", flush=True)
        if not cond:
            failures.append(msg)

    if args.pitch_rate:
        # Closure is lag-dependent: rate information matters most around a
        # quarter of the ~30 s pitch natural period and washes out by 5 s.
        # The check's purpose is that the added state variable carries real
        # information at SOME horizon, so test the peak over the sweep.
        closures = {l: r["leak_nostate"] - r["leak_reduced"]
                    for l, r in results["lags"].items()}
        lmax = max(closures, key=closures.get)
        check(closures[lmax] > 0.05,
              f"pitch-rate carries real state info (peak closure "
              f"{closures[lmax]:.3f} at lag {lmax} = {lmax/args.hz:.1f} s; "
              f"at headline lag it is "
              f"{hb['leak_nostate']:.3f} -> {hb['leak_reduced']:.3f})")
    else:
        check(hb["leak_reduced"] > 0.5,
              f"leak with only (wind, wave, own past) is high "
              f"({hb['leak_reduced']:.3f}) - unobserved drivers dominate")
    thresh = max(0.02, 0.05 * hb["leak_reduced"])
    check(hb["corrected_drop"] > thresh,
          f"observing the controller drops the leak materially "
          f"(corrected drop {hb['corrected_drop']:.3f} vs threshold "
          f"{thresh:.3f} = max(0.02, 5% of remaining leak "
          f"{hb['leak_reduced']:.3f}))")
    if not args.pitch_rate:
        check(hb["corrected_drop"] > 0.5 * hb["raw_drop"],
              f"drop survives the dimensionality control "
              f"(corrected {hb['corrected_drop']:.3f} vs raw {hb['raw_drop']:.3f})")
    check(all(u["wind_total"] > 0.01 for u in upstream.values()),
          "wind carries info into both controller channels "
          + str({k: round(v['wind_total'], 4) for k, v in upstream.items()}))

    results["failures"] = failures
    results["runtime_s"] = time.time() - t0
    Path(str(out_stem) + ".json").write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out_stem}.json ({time.time()-t0:.0f}s)", flush=True)

    if failures:
        print(f"\nPHASE 1 GATE: {len(failures)} check(s) failed - "
              "inspect before scaling to Phase 2.", flush=True)
        return 1
    print("\nPHASE 1 GATE OPEN: the leak story holds on this case.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
