---
title: "KSG k-Sensitivity Robustness Check"
type: analysis-note
created: 2026-07-10
updated: 2026-07-10
tags: [transfer-entropy, ksg, estimator, robustness, methods]
---

# KSG k-Sensitivity Robustness Check

## Purpose

An IEEE fault-detection paper (quoted by the user) notes that TE estimation is
ultimately probability-distribution estimation, with two estimator families —
kernel-density and k-nearest-neighbour (kNN). The firewall manuscript uses the
kNN family (KSG, `JidtKraskovCMI`, k = 4). This note checks that the paper's
conclusions do not depend on the one free parameter of that estimator, the
neighbour count k. Motivated the §3.3 estimator-justification paragraph.

## Method

Reused the self-contained KSG conditional-MI estimator in
`analysis/delay_analysis.py` (`ksg_cmi`, scipy `cKDTree` + `digamma`; no IDTxl),
which takes k as an argument. Recomputed the two headline delay-resolved TE
profiles — `Wave1Elev → PtfmHeave` (coupled) and `Wind1VelX → PtfmHeave`
(firewalled) — for **k ∈ {3, 4, 6, 8}**, averaged over the same 3 healthy
11 m/s seeds the paper reports. Identical preprocessing (600 s transient drop,
5 Hz decimation, 1e-10 jitter, z-normalise). Selected delay = argmax over
d ≤ 6.5 s (Tp/2), per the paper's convention. Firewall ratio = wave peak TE /
wind max TE.

## Results

| k | Wave peak TE (nats) | Selected delay (s) | Wind ceiling (nats) | Gap (nats) | Wave/Wind ratio |
|---|---|---|---|---|---|
| 3 | 1.256 | 2.87 | 0.030 | 1.226 | 41.8× |
| **4** (paper) | **1.092** | **2.73** | **0.028** | **1.064** | **39.3×** |
| 6 | 0.964 | 2.73 | 0.021 | 0.942 | 44.9× |
| 8 | 0.866 | 2.73 | 0.018 | 0.848 | 47.6× |

## Conclusion

- **Coupling delay is k-invariant**: 2.73–2.87 s across all k (paper reports
  ~2.6–2.7 s).
- **Firewall is k-invariant**: the wind ceiling stays ≤ 0.03 nats (far below the
  ≈ 0.36 nats 95% chance level) and the wave-to-wind ratio stays 39–48× at every
  k. Wind never approaches significance at any k.
- **Absolute TE magnitude is mildly k-dependent** (1.256 → 0.866 as k rises 3→8),
  which is the *expected* bias–variance behaviour of a nearest-neighbour
  estimator: larger k smooths the density estimate and lowers the absolute MI.
  No conclusion in the paper rests on the absolute nats — only on the delay
  location and the wind/wave separation, both robust.

So the choice k = 4 (the Kraskov et al. 2004 recommendation) is not driving any
result. Reproduce with the scratch script logic in the log entry, or re-run the
`ksg_cmi(..., k=k)` sweep over `delay_analysis.te_delay_profile`.
