"""load_band_attribution.py — where does each FOWT load's variance live (in frequency)?

For every response channel, compute the power spectral density (Welch) on the
preprocessed time series and report the fraction of total variance in three
bands:
  - low        (< --low-hz, default 0.03 Hz): slow drift, surge/pitch resonance,
               low-frequency wind turbulence -- the design-governing band.
  - coherence  ([--coh-lo, --coh-hi], default 0.05-0.15 Hz): the band where
               realistic wind-wave coherence lives (He 2020, peak ~0.1 Hz).
  - high       (> --coh-hi): 1P/3P rotor harmonics, high-frequency content.

Purpose: a cheap, no-GPU, no-TE gate on the wind-wave-correlation thread. Wind-
wave coupling can only change a load's causal attribution at frequencies where
BOTH the coupling and the load have energy. If the design-driving loads
(esp. tower-base fore-aft) carry < ~10% of their variance in the coherence band,
the coupling cannot rewrite their attribution -> the thread is a pre-determined
null. Also a useful spectral characterization for the main paper (which loads
are slow-drift vs wave-band vs rotor-driven).

Usage:
    python analysis/load_band_attribution.py path/to/run.outb
    python analysis/load_band_attribution.py run.outb --low-hz 0.03 --coh-lo 0.05 --coh-hi 0.15
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
from te_pipeline import TESettings, find_channel, preprocess_channel, DEFAULT_RESPONSES  # noqa: E402
from load_runs import load_outb, find_time_column  # noqa: E402


def band_fractions(x: np.ndarray, fs: float, low_hz: float,
                   coh_lo: float, coh_hi: float, nperseg: int):
    """Fraction of variance in (low, coherence, high) bands via Welch PSD.
    Returns (frac_low, frac_coh, frac_high, total_var)."""
    from scipy.signal import welch
    nperseg = min(nperseg, len(x))
    f, pxx = welch(x, fs=fs, nperseg=nperseg)
    df = f[1] - f[0]
    total = float(np.sum(pxx) * df)
    if total == 0:
        return 0.0, 0.0, 0.0, 0.0
    low = float(np.sum(pxx[f < low_hz]) * df)
    coh = float(np.sum(pxx[(f >= coh_lo) & (f <= coh_hi)]) * df)
    high = float(np.sum(pxx[f > coh_hi]) * df)
    return low / total, coh / total, high / total, total


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("--decimate-target-hz", type=float, default=5.0)
    ap.add_argument("--transient-drop-s", type=float, default=600.0)
    ap.add_argument("--low-hz", type=float, default=0.03,
                    help="Upper edge of the low/slow-drift band (Hz).")
    ap.add_argument("--coh-lo", type=float, default=0.05,
                    help="Lower edge of the wind-wave coherence band (Hz).")
    ap.add_argument("--coh-hi", type=float, default=0.15,
                    help="Upper edge of the coherence band (Hz).")
    ap.add_argument("--nperseg", type=int, default=4096,
                    help="Welch segment length (capped at N).")
    ap.add_argument("--design-loads", default="TwrBsMyt,FAIRTEN1,FAIRTEN2,FAIRTEN3,PtfmSurge,PtfmPitch",
                    help="Comma list of design-driving loads for the verdict.")
    ap.add_argument("--threshold", type=float, default=0.10,
                    help="Coherence-band fraction below which a load is "
                         "'untouched' by wind-wave coupling (default 0.10).")
    args = ap.parse_args()

    settings = TESettings(decimate_target_hz=args.decimate_target_hz,
                          transient_drop_s=args.transient_drop_s)
    df = load_outb(args.input)
    dt_in = float(np.median(np.diff(df[find_time_column(df)].to_numpy())))

    rows = []
    fs_out = None
    for name in DEFAULT_RESPONSES:
        try:
            col = find_channel(df, name)
        except KeyError:
            continue
        clean, dt_out = preprocess_channel(df[col].to_numpy(), dt_in, settings, seed=0)
        fs_out = 1.0 / dt_out
        fl, fc, fh, var = band_fractions(clean, fs_out, args.low_hz,
                                         args.coh_lo, args.coh_hi, args.nperseg)
        rows.append((name, fl, fc, fh, var))

    print(f"\n{args.input.name}  @ {fs_out:.2f} Hz")
    print(f"bands: low < {args.low_hz} Hz | coherence {args.coh_lo}-{args.coh_hi} Hz | "
          f"high > {args.coh_hi} Hz\n")
    hdr = f"{'channel':<11}{'low%':>8}{'COH%':>8}{'high%':>8}"
    print(hdr)
    print("-" * len(hdr))
    for name, fl, fc, fh, _ in rows:
        print(f"{name:<11}{100*fl:>8.1f}{100*fc:>8.1f}{100*fh:>8.1f}")

    design = [d.strip() for d in args.design_loads.split(",") if d.strip()]
    flagged = [(n, fc) for (n, _, fc, _, _) in rows
               if n in design and fc >= args.threshold]
    print(f"\nDesign-driving loads with >= {int(args.threshold*100)}% variance in the "
          f"coherence band:")
    if flagged:
        for n, fc in sorted(flagged, key=lambda t: -t[1]):
            print(f"  {n:<11} {100*fc:.1f}%  <- wind-wave coupling COULD affect this")
        print("\nVERDICT: at least one design-driving load has meaningful coherence-band\n"
              "content -> the wind-wave thread is NOT a pre-determined null; a pilot is\n"
              "worth doing (focus on the flagged channel(s)).")
    else:
        print("  (none)")
        print(f"\nVERDICT: every design-driving load has < {int(args.threshold*100)}% of its\n"
              "variance in the coherence band -> wind-wave coupling cannot rewrite their\n"
              "attribution. The thread is a PRE-DETERMINED NULL -> demote/drop it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
