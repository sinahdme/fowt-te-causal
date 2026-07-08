#!/usr/bin/env python3
"""Delay-resolved transfer entropy: how the source lag affects the TE estimate.

WHY
---
Stage-3 review + author question: the manuscript describes the lag *search
window* (max_lag_sources) but never reports the *selected coupling delay* as a
result, nor shows how the delay affects the TE calculation. This module does
both, on the real OpenFAST signals, without needing IDTxl/GPU (which is not
installed on the Windows box). It uses a compact, transparent KSG conditional
mutual-information estimator (Kraskov k=4, Chebyshev metric) — the same
estimator FAMILY as the pipeline, but a single-lag delay profile rather than
IDTxl's greedy multi-lag embedding. State that distinction where it is used.

DELAY-RESOLVED TE
-----------------
For a source X and target Y we compute, at each candidate delay d (samples):

    TE_d(X -> Y) = I( Y_t ; X_{t-d} | Y_{t-1} )     [nats]

estimated with the KSG conditional-MI estimator. Sweeping d gives the delay
profile; its argmax is the selected coupling delay. A circular-shift null
gives a chance band. Preprocessing exactly mirrors te_pipeline.preprocess_channel
(drop 600 s transient, stride-decimate 40 -> 5 Hz, z-normalise).

OUTPUTS
-------
  reports/delay_profiles.parquet         profiles for the reported edges
  reports/figs/fig6-delay-analysis.png   worked-example figure (2 panels)
  stdout                                  selected-delay table for the paper

USAGE
-----
    python analysis/delay_analysis.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.special import digamma

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import load_runs  # noqa: E402

FS_TARGET = 5.0          # Hz, after decimation (te_pipeline decimate_target_hz)
TRANSIENT_S = 600.0      # te_pipeline transient_drop_s
K = 4                    # te_pipeline kraskov_k
MAX_DELAY = 30           # samples => 6.0 s at 5 Hz (covers max_lag_sources window)
JITTER = 1e-10

HEALTHY_11MS = [f"sims/dlc16_v11ms_s{ i:02d}/IEA-15-240-RWT-UMaineSemi/"
                "IEA-15-240-RWT-UMaineSemi.outb" for i in range(6)]


# ---------------------------------------------------------------------------
# preprocessing (mirror te_pipeline.preprocess_channel) + KSG conditional MI
# ---------------------------------------------------------------------------
def load_channel(df, tcol, name):
    col = next(c for c in df.columns if c.split("_[")[0].lower() == name.lower())
    return df[col].to_numpy(float)


def preprocess(arr, dt_in, seed=0):
    factor = max(1, int(round((1.0 / dt_in) / FS_TARGET)))
    drop_n = int(TRANSIENT_S / dt_in)
    out = arr[drop_n:][::factor]
    out = out + JITTER * np.random.default_rng(seed).standard_normal(out.shape)
    return (out - out.mean()) / out.std()          # z-normalise (IDTxl normalise=True)


def ksg_cmi(X, Y, Z, k=K):
    """KSG estimator of I(X;Y|Z) in nats (Frenzel & Pombe 2007). X,Y,Z: (N,d)."""
    X, Y, Z = np.atleast_2d(X.T).T, np.atleast_2d(Y.T).T, np.atleast_2d(Z.T).T
    W = np.hstack([X, Y, Z])
    eps = cKDTree(W).query(W, k=k + 1, p=np.inf)[0][:, k]      # k-th nbr dist (excl self)
    r = np.nextafter(eps, 0)                                   # strict "<" convention
    def cnt(A):
        return np.array(cKDTree(A).query_ball_point(A, r, p=np.inf, return_length=True)) - 1
    n_xz = cnt(np.hstack([X, Z])); n_yz = cnt(np.hstack([Y, Z])); n_z = cnt(Z)
    val = digamma(k) + np.mean(digamma(n_z + 1) - digamma(n_xz + 1) - digamma(n_yz + 1))
    return float(val)


def te_delay_profile(x, y, delays):
    """TE_d(x->y) = I(y_t ; x_{t-d} | y_{t-1}) for each d in delays."""
    out = []
    for d in delays:
        t0 = max(d, 1)
        yt, ytm1, xd = y[t0:], y[t0 - 1:-1], x[t0 - d: len(x) - d]
        n = min(len(yt), len(ytm1), len(xd))
        out.append(ksg_cmi(yt[:n], xd[:n], ytm1[:n]))
    return np.array(out)


def null_threshold(x, y, delays, n_shuffle=40, pct=95, seed=1):
    """95th-percentile chance TE from circularly shifted source (coupling destroyed)."""
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_shuffle):
        xs = np.roll(x, int(rng.integers(len(x) // 8, 7 * len(x) // 8)))
        d = int(rng.choice(delays))
        t0 = max(d, 1)
        yt, ytm1, xd = y[t0:], y[t0 - 1:-1], xs[t0 - d: len(xs) - d]
        n = min(len(yt), len(ytm1), len(xd))
        vals.append(ksg_cmi(yt[:n], xd[:n], ytm1[:n]))
    return float(np.percentile(vals, pct))


# ---------------------------------------------------------------------------
def main():
    delays = np.arange(1, MAX_DELAY + 1)
    delays_s = delays / FS_TARGET

    # ----- Part A: selected delays for the significant wave edges -----
    edges = [("Wave1Elev", "PtfmHeave"), ("Wave1Elev", "PtfmPitch"),
             ("Wave1Elev", "PtfmSurge"), ("Wave1Elev", "FAIRTEN2")]
    cases = HEALTHY_11MS[:3]                    # 3 seeds for the reported average
    rows, prof_rows = [], []
    print("Loading + preprocessing (3 healthy 11 m/s seeds)...", flush=True)
    sig = {}
    for cpath in cases:
        df = load_runs.load_outb(cpath)
        tcol = load_runs.find_time_column(df)
        dt = float(np.median(np.diff(df[tcol].to_numpy(float))))
        case = cpath.split("/")[1]
        chans = {n: preprocess(load_channel(df, tcol, n), dt)
                 for n in ["Wave1Elev", "Wind1VelX", "PtfmHeave", "PtfmPitch",
                           "PtfmSurge", "FAIRTEN2"]}
        sig.setdefault(case, chans)
        for src, tgt in edges:
            p = te_delay_profile(chans[src], chans[tgt], delays)
            j = int(np.argmax(p))
            rows.append(dict(case=case, source=src, target=tgt,
                             sel_delay_s=round(delays_s[j], 2), peak_te=round(p[j], 4)))
            for d, s, v in zip(delays, delays_s, p):
                prof_rows.append(dict(case=case, source=src, target=tgt,
                                      delay_s=s, te_nats=v))
        print(f"  {case} done", flush=True)

    prof = pd.DataFrame(prof_rows)
    prof.to_parquet("reports/delay_profiles.parquet")
    summ = (pd.DataFrame(rows).groupby(["source", "target"])
            .agg(sel_delay_s=("sel_delay_s", "mean"), peak_te=("peak_te", "mean"))
            .round(3).reset_index())
    print("\n=== SELECTED COUPLING DELAYS (mean over 3 healthy 11 m/s seeds) ===")
    print(summ.to_string(index=False))

    # ----- Part B: worked-example figure on one case -----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    case0 = list(sig)[0]
    ch = sig[case0]
    wave, heave, wind = ch["Wave1Elev"], ch["PtfmHeave"], ch["Wind1VelX"]
    te_wave = te_delay_profile(wave, heave, delays)
    te_wind = te_delay_profile(wind, heave, delays)
    thr = null_threshold(wave, heave, delays)
    d_sel = delays_s[int(np.argmax(te_wave))]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))

    # panel (a): a 100 s span; wave leads platform heave by ~d_sel (visible lag)
    span = slice(500, 500 + int(100 * FS_TARGET))
    t = np.arange(len(wave))[span] / FS_TARGET
    ax1.plot(t, wave[span], lw=1.2, label="Wave elevation", color="#1f77b4")
    ax1.plot(t, heave[span], lw=1.2, label="Platform heave", color="#d62728")
    ax1.set_xlabel("time (s)"); ax1.set_ylabel("z-scored signal")
    ax1.set_title(f"(a) 100 s span — platform heave lags the wave by ~{d_sel:.1f} s")
    ax1.legend(loc="upper right", fontsize=8, framealpha=0.9)

    # panel (b): delay-resolved TE, wave (coupled) vs wind (firewalled)
    ax2.plot(delays_s, te_wave, "-o", ms=3, color="#1f77b4", label="Wave -> PtfmHeave")
    ax2.plot(delays_s, te_wind, "-s", ms=3, color="#7f7f7f", label="Wind -> PtfmHeave (firewalled)")
    ax2.axhline(thr, ls="--", lw=1, color="k", label="95% chance level")
    ax2.axvline(d_sel, ls=":", lw=1, color="#1f77b4")
    ax2.set_xlabel("assumed source delay d (s)")
    ax2.set_ylabel("delay-resolved TE (nats)")
    ax2.set_title("(b) TE peaks at the coupling delay; wind flat at every lag")
    ax2.legend(loc="upper right", fontsize=8, framealpha=0.9)
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig("reports/figs/fig6-delay-analysis.png", dpi=150, bbox_inches="tight")
    print(f"\nFigure: reports/figs/fig6-delay-analysis.png "
          f"(wave peak delay ~{d_sel:.1f}s, peak TE {te_wave.max():.3f}, "
          f"wind max {te_wind.max():.3f}, null {thr:.3f})")


if __name__ == "__main__":
    main()
