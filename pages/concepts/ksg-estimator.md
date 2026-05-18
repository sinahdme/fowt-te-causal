---
title: "Kraskov–Stögbauer–Grassberger (KSG) Estimator"
type: concept
created: 2026-05-12
updated: 2026-05-12
sources: ["kraskov-2004"]
tags: [information-theory, estimator]
---

## Definition

A nearest-neighbour based estimator for differential entropy and mutual
information from continuous data, generalised to transfer entropy via the
chain rule of conditional MI. Defined in [[sources/kraskov-2004]].

The two algorithm variants (`I^(1)` and `I^(2)`, both used in
[[entities/idtxl]]) differ only in how marginal neighbour counts are
taken. See [[papers/kraskov-2004]] for the derivation re-check.

## Why KSG over alternatives

- **Asymptotically unbiased**. Per kraskov-2004: *"In all cases we found
  that both estimators become exact for independent variables"* — verified
  for Gaussian, uniform, exponential, gamma-exponential distributions
  (p. 5). This is the property that makes the surrogate test in
  [[concepts/surrogate-significance]] *theoretically sound* — under the
  independence null, the estimator returns zero in expectation, so any
  observed positive shift is signal, not bias.
- **No bin width** to tune. Histogram / binning estimators are dominated
  by binning bias; kernel methods need bandwidth tuning per channel pair.
- **Adaptive resolution**. kraskov-2004 (abstract): *"adaptive (the
  resolution is higher where data are more numerous)"*.
- **Works at moderate sample sizes** (≈10³ – 10⁵) — matches our
  per-case data after decimation to ~10 Hz.

## Hyperparameters

- **`k` neighbours**. kraskov-2004 (p. 7) explicit recommendation:
  *"We propose to use typically `k = 2` to `4`, except when testing for
  independence. In the latter case we do not have to worry about
  systematic errors, and statistical errors are minimized by taking `k`
  to be very large (up to `k ≈ N/2`, say)."*
  Defaults we adopt: `k = 4` for TE / MI estimation in Phase 4; `k = N/4`
  for the surrogate independence-test in
  [[validation/case-2-ar1-te-recovery]].

## Cost

`O(N log N)` per estimate with KD-trees or `O(N √(kN))` with box grids.
kraskov-2004 (p. 6) explicitly describes the box-grid algorithm. The
constant grows with embedding dimension, so we **decimate** OpenFAST output
to 5–10 Hz before estimation to keep `N` manageable.

## Critical implementation detail — empirical-data jitter

kraskov-2004 (Sec. III.A, p. 6):

> "Empirical data usually are obtained with few (e.g. 12 or 16) binary
> digits, which means that many points in a large set may have identical
> coordinates (the assumption of continuously distributed points is
> violated). If no precautions are taken, any code based on nearest
> neighbour counting is then bound to give wrong results. The simplest
> way out of this dilemma is to add very low amplitude noise to the data
> (≈ 10⁻¹⁰, say, when working with double precision) which breaks this
> degeneracy."

This must be applied to FOWT outputs in `analysis/load_runs.py` after
decimation. OpenFAST emits float-precision data (~7 significant digits)
so the degeneracy risk is real. Utility: `apply_neighbour_jitter(df,
scale=1e-10)`.

## Related concepts

- [[concepts/transfer-entropy]] · [[concepts/mutual-information]] ·
  [[concepts/surrogate-significance]]
- [[concepts/conditional-transfer-entropy]] — KSG generalises to higher
  dims for conditional MI; see kraskov-2004 Eq. 30.

## Sources

- [[sources/kraskov-2004]] — Phys. Rev. E 69, 066138.
- [[papers/kraskov-2004]] — deep analytical re-read with derivation chain.
