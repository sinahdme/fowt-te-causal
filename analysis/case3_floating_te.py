"""
case3_floating_te.py — validation case 3:
real OpenFAST floating-platform run → end-to-end TE pipeline.

Retargeted 2026-05-14 to the IEA-15 UMaineSemi run completed in
`sims/case-iea15-real/` (TMax=300 s, ROSCO 2.10.1). Replaces the prior
r-test 5MW_ITIBarge stand-in.

Pipeline (PLAN.md Phase 3 + Phase 4):
  1. load_runs.load_outb()        → DataFrame (units-suffixed cols)
  2. detect Time / Wind1VelX / PtfmPitch
  3. drop first 60 s transient   (UMaineSemi surge natural period ~100 s)
  4. decimate to ~20 Hz                       (Phase 3)
  5. add 1e-10 Gaussian jitter (kraskov-2004) (Phase 4 prep)
  6. BivariateTE with KSG (kraskov_k=4, n_perm=200, permute_in_time=True)
  7. forward (wind → pitch) and reverse (pitch → wind, sanity)

Pass criteria (smoke test):
  - forward TE > 0 and p < 0.05 (significant)
  - reverse TE NOT significant (no back-action sanity check)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))

from load_runs import load_outb, find_time_column  # noqa: E402


OUTB_PATH = (
    PROJECT_ROOT
    / "sims" / "case-iea15-real"
    / "IEA-15-240-RWT-UMaineSemi"
    / "IEA-15-240-RWT-UMaineSemi.outb"
)

TARGET_DECIMATED_HZ = 5.0
TRANSIENT_DROP_SEC = 60.0
KSG_K = 4
N_PERM = 200
MAX_LAG = 30  # in samples = 6 s at 5 Hz; covers wind→thrust→pitch onset


def find_channel(df, basename: str) -> str:
    for col in df.columns:
        if col.split("_[")[0].lower() == basename.lower():
            return col
    raise KeyError(f"no '{basename}' channel; first 10 cols = {list(df.columns[:10])}")


def decimate(x: np.ndarray, factor: int) -> np.ndarray:
    """Cheap decimation: take every Nth sample. (No anti-alias filter — fine
    for a smoke test; Phase 3 will use scipy.signal.decimate with FIR.)"""
    return x[::factor]


def jitter(arr: np.ndarray, scale: float = 1e-10, seed: int = 42) -> np.ndarray:
    """kraskov-2004 §III.A neighbour-degeneracy fix."""
    rng = np.random.default_rng(seed)
    return arr + scale * rng.standard_normal(arr.shape)


def run_te(source: np.ndarray, target: np.ndarray, ksg_k: int = KSG_K, n_perm: int = N_PERM):
    from idtxl.bivariate_te import BivariateTE
    from idtxl.data import Data

    arr = np.vstack([source, target])
    data = Data(arr, dim_order="ps", normalise=True)
    settings = {
        "cmi_estimator": "JidtKraskovCMI",
        "kraskov_k": str(ksg_k),
        "max_lag_sources": MAX_LAG,
        "min_lag_sources": 1,
        "max_lag_target": MAX_LAG,
        "n_perm_max_stat": n_perm,
        "n_perm_min_stat": n_perm,
        "n_perm_omnibus": n_perm,
        "n_perm_max_seq": n_perm,
        "alpha_max_stat": 0.05,
        "alpha_min_stat": 0.05,
        "alpha_omnibus": 0.05,
        "permute_in_time": True,
        # Circular shift preserves the source's power spectrum + amplitude
        # distribution exactly while destroying directed coupling. Spectrum-
        # preserving null is essential for oscillatory FOWT signals; the IDTxl
        # default 'random' destroys auto-correlation too (weakest null).
        # Equivalent in effect to IAAFT for single-source-pair use. True IAAFT
        # (Schreiber-Schmitz 2000) is not in IDTxl natively — see
        # concepts/surrogate-significance.
        "perm_type": "circular",
    }
    analysis = BivariateTE()
    results = analysis.analyse_single_target(settings=settings, data=data, target=1, sources=[0])
    tr = results.get_single_target(1, fdr=False)
    te = tr.get("te")
    pval = tr.get("omnibus_pval")
    te_val = float(te[0]) if (te is not None and len(te) > 0) else 0.0
    p_val = float(pval) if pval is not None else 1.0
    return te_val, p_val


def main() -> int:
    print(f"Loading {OUTB_PATH.name}")
    df = load_outb(OUTB_PATH)
    print(f"  shape = {df.shape}")

    t_col = find_time_column(df)
    wind_col = find_channel(df, "Wind1VelX")
    pitch_col = find_channel(df, "PtfmPitch")
    print(f"  time = {t_col!r}, wind = {wind_col!r}, pitch = {pitch_col!r}")

    t = df[t_col].to_numpy()
    dt = float(np.median(np.diff(t)))
    src_hz = 1.0 / dt
    print(f"  source rate ~ {src_hz:.1f} Hz; dt = {dt:.4f} s")

    drop_idx = int(TRANSIENT_DROP_SEC / dt)
    factor = max(1, int(round(src_hz / TARGET_DECIMATED_HZ)))
    print(f"  drop first {drop_idx} samples ({TRANSIENT_DROP_SEC}s)"
          f"; decimate by {factor} -> {src_hz/factor:.1f} Hz")

    wind = df[wind_col].to_numpy()[drop_idx:]
    pitch = df[pitch_col].to_numpy()[drop_idx:]
    wind = decimate(wind, factor)
    pitch = decimate(pitch, factor)
    print(f"  post-decimation: N = {len(wind)} samples ({len(wind)/(src_hz/factor):.1f}s)")
    print(f"    Wind1VelX: mean={wind.mean():+.3f}, std={wind.std():.3f}")
    print(f"    PtfmPitch: mean={pitch.mean():+.3f}, std={pitch.std():.3f}")

    wind_j = jitter(wind, seed=1)
    pitch_j = jitter(pitch, seed=2)

    print("\nForward: TE(Wind1VelX -> PtfmPitch)")
    te_fwd, p_fwd = run_te(wind_j, pitch_j)
    print(f"  TE = {te_fwd:+.4f} nats, p = {p_fwd:.4f}")

    print("\nReverse: TE(PtfmPitch -> Wind1VelX)  [no back-action sanity check]")
    te_rev, p_rev = run_te(pitch_j, wind_j)
    print(f"  TE = {te_rev:+.4f} nats, p = {p_rev:.4f}")

    print("\n=== Validation verdict ===")
    pass_fwd = (p_fwd < 0.05) and (te_fwd > 0)
    pass_rev = (p_rev >= 0.05) or (te_rev < 0.2 * max(te_fwd, 1e-6))
    print(f"  TE(wind->pitch) significant and > 0?     {'PASS' if pass_fwd else 'FAIL'}")
    print(f"  TE(pitch->wind) NOT significant or << fwd? {'PASS' if pass_rev else 'FAIL'}")

    return 0 if (pass_fwd and pass_rev) else 1


if __name__ == "__main__":
    sys.exit(main())
