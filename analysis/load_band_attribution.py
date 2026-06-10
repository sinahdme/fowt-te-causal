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


def coh_notched(x: np.ndarray, fs: float, coh_lo: float, coh_hi: float,
                notch_freqs, notch_bw: float, nperseg: int):
    """Within the coherence band, split variance into rotor-line content
    (within +/- notch_bw of any nP harmonic) and wave-only content (the rest).
    Returns (coh_frac, rotor_frac, wave_frac) as fractions of TOTAL variance."""
    from scipy.signal import welch
    nperseg = min(nperseg, len(x))
    f, pxx = welch(x, fs=fs, nperseg=nperseg)
    df = f[1] - f[0]
    total = float(np.sum(pxx) * df)
    if total == 0:
        return 0.0, 0.0, 0.0
    in_coh = (f >= coh_lo) & (f <= coh_hi)
    rotor_mask = np.zeros_like(f, dtype=bool)
    for nf in notch_freqs:
        rotor_mask |= np.abs(f - nf) <= notch_bw
    coh = float(np.sum(pxx[in_coh]) * df)
    rotor = float(np.sum(pxx[in_coh & rotor_mask]) * df)
    return coh / total, rotor / total, (coh - rotor) / total


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
    ap.add_argument("--notch-1p", action="store_true",
                    help="Split the coherence band into rotor-line (nP harmonics, "
                         "wind/rotor-driven) vs WAVE-ONLY content. 1P is read from "
                         "the mean RotSpeed in the file; verdict uses the wave-only %.")
    ap.add_argument("--rotor-harmonics", default="1,3,6",
                    help="nP harmonics to notch when --notch-1p (default 1,3,6).")
    ap.add_argument("--notch-bw", type=float, default=0.01,
                    help="Half-width (Hz) of each nP notch (default 0.01; widen "
                         "if rotor speed varies, e.g. below rated).")
    args = ap.parse_args()

    settings = TESettings(decimate_target_hz=args.decimate_target_hz,
                          transient_drop_s=args.transient_drop_s)
    df = load_outb(args.input)
    dt_in = float(np.median(np.diff(df[find_time_column(df)].to_numpy())))

    # 1P / nP harmonics from mean rotor speed, if notching requested.
    notch_freqs: list[float] = []
    p1 = None
    if args.notch_1p:
        try:
            rot = df[find_channel(df, "RotSpeed")].to_numpy()  # rpm
            p1 = float(np.mean(rot)) / 60.0  # Hz
            harmonics = [int(h) for h in args.rotor_harmonics.split(",") if h.strip()]
            notch_freqs = [n * p1 for n in harmonics
                           if args.coh_lo <= n * p1 <= args.coh_hi]
        except KeyError:
            print("  (no RotSpeed channel -> cannot notch 1P; running un-notched)")
            args.notch_1p = False

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
        rotor = wave = None
        if args.notch_1p:
            _, rotor, wave = coh_notched(clean, fs_out, args.coh_lo, args.coh_hi,
                                         notch_freqs, args.notch_bw, args.nperseg)
        rows.append((name, fl, fc, fh, var, rotor, wave))

    print(f"\n{args.input.name}  @ {fs_out:.2f} Hz")
    print(f"bands: low < {args.low_hz} Hz | coherence {args.coh_lo}-{args.coh_hi} Hz | "
          f"high > {args.coh_hi} Hz")
    if args.notch_1p:
        print(f"1P = {p1:.3f} Hz (mean RotSpeed); notching nP at "
              f"{[round(x, 3) for x in notch_freqs]} +/- {args.notch_bw} Hz "
              f"(COH% = rotor% + WAVE%)")
        hdr = (f"{'channel':<11}{'low%':>8}{'COH%':>8}{'rotor%':>8}"
               f"{'WAVE%':>8}{'high%':>8}")
    else:
        hdr = f"{'channel':<11}{'low%':>8}{'COH%':>8}{'high%':>8}"
    print()
    print(hdr)
    print("-" * len(hdr))
    for name, fl, fc, fh, _, rotor, wave in rows:
        if args.notch_1p:
            print(f"{name:<11}{100*fl:>8.1f}{100*fc:>8.1f}{100*rotor:>8.1f}"
                  f"{100*wave:>8.1f}{100*fh:>8.1f}")
        else:
            print(f"{name:<11}{100*fl:>8.1f}{100*fc:>8.1f}{100*fh:>8.1f}")

    # Verdict uses the WAVE-ONLY fraction when notching, else the raw coherence band.
    design = [d.strip() for d in args.design_loads.split(",") if d.strip()]
    metric_name = "wave-only" if args.notch_1p else "coherence-band"
    def metric(r):  # r = (name, fl, fc, fh, var, rotor, wave)
        return r[6] if args.notch_1p else r[2]
    flagged = [(r[0], metric(r)) for r in rows
               if r[0] in design and metric(r) >= args.threshold]
    print(f"\nDesign-driving loads with >= {int(args.threshold*100)}% {metric_name} variance:")
    if flagged:
        for n, m in sorted(flagged, key=lambda t: -t[1]):
            print(f"  {n:<11} {100*m:.1f}%  <- wind-wave coupling COULD affect this")
        print(f"\nVERDICT: at least one design-driving load has meaningful {metric_name}\n"
              "content -> the wind-wave thread is NOT a pre-determined null; a pilot is\n"
              "worth doing (focus on the flagged channel(s)).")
    else:
        print("  (none)")
        print(f"\nVERDICT: every design-driving load has < {int(args.threshold*100)}% "
              f"{metric_name}\nvariance -> wind-wave coupling cannot rewrite their "
              "attribution. The thread is a\nPRE-DETERMINED NULL -> demote/drop it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
