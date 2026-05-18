---
title: "Transfer Entropy"
type: concept
created: 2026-05-12
updated: 2026-05-12
sources: ["schreiber-2000", "wollstadt-2019"]
tags: [information-theory, causality, time-series]
---

## Definition

Transfer Entropy (TE) is a directional, non-parametric measure of
information flow from one stochastic process to another. Introduced by
[[sources/schreiber-2000]]. For source `X` and target `Y`:

> "In the absence of information flow from J to I, the state of J has no
> influence on the transition probabilities on system I. The incorrectness
> of this assumption can again be quantified by a Kullback entropy."
> (schreiber-2000, p. 462)

Operationally: TE quantifies how much extra predictability of `Y_t` is
gained from the past of `X` beyond the past of `Y` itself.

Formal statement: see [[equations/eq-transfer-entropy]].

## Why it matters here

TE is the **core method for Phase 4** of this project — quantifying how
much of FOWT response variance is causally attributable to wind vs wave
forcing. It is preferred over coherence because:

- **Asymmetric** — yields a directional answer ("wind drives pitch", not
  the reverse). schreiber-2000 (p. 462): *"T_{J→I} is now explicitly
  non-symmetric since it measures the degree of dependence of I on J and
  not vice versa."*
- **Nonlinear** — captures dependencies invisible to linear coherence.
- **Conditional form** — separates contributions when source signals are
  correlated (see [[concepts/conditional-transfer-entropy]]). The
  conditional form is sketched in schreiber-2000 itself: *"the influence
  of a known common driving force Z may be excluded by conditioning the
  probabilities under the logarithm to z_n as well"* (p. 462) — directly
  applicable to our wind/wave problem.

TE does **not** apply to constants-per-run such as structural design
parameters; for those see [[concepts/sobol-sensitivity]].

## Practical pipeline (per source/target pair)

1. Choose embedding `(k, l, u)`. schreiber-2000 (p. 462) notes *"The most
   natural choices for `l` are `l = k` or `l = 1`. Usually, the latter is
   preferable for computational reasons."* For us, [[entities/idtxl]] runs
   automated max-stat / min-stat embedding selection per pair (per
   wollstadt-2019).
2. Estimate TE with the [[concepts/ksg-estimator]].
3. Test significance with [[concepts/surrogate-significance]].
4. Compare to a linear baseline (coherence + Granger). Per
   [[papers/wollstadt-2019]], the Granger baseline can be obtained from
   the same IDTxl pipeline with the linear-Gaussian estimator
   (`JidtGaussianCMI`), giving apples-to-apples comparison.

## Sanity checks

- `TE(response → wind)` should be approximately zero (no back-action on
  environment). schreiber-2000 establishes this as a directional-causality
  diagnostic (Ulam-map example, Fig. 2). Non-zero values indicate an
  embedding problem.
- Reproduce a known-answer AR(1) coupling — see
  [[validation/case-2-ar1-te-recovery]].

## Quotes worth preserving

> "Most prominent applications include multivariate analysis of time series
> and the study of spatially extended systems." (schreiber-2000, p. 4)

> "Although such approaches have been proposed […] and first software
> implementations exist […], there is no current implementation that deals
> with the practical problems that arise in multivariate TE estimation.
> These problems include the control of statistical errors that arise from
> testing multiple potential sources in a data set, and the optimization
> of parameters necessary for the estimation of multivariate TE."
> (wollstadt-2019, ¶7) — motivates our reliance on [[entities/idtxl]] for
> the multi-channel Phase 4 inference.

## Related concepts

- [[concepts/conditional-transfer-entropy]] — disentangles correlated sources
- [[concepts/mutual-information]] — symmetric companion measure
- [[concepts/ksg-estimator]] — estimator
- [[concepts/surrogate-significance]] — significance testing
- [[concepts/time-delay-embedding]] *(stub)* — `(k, l, u)` selection
- [[concepts/active-information-storage]] *(stub)* — TE effect-size denominator

## Sources

- [[sources/schreiber-2000]] — original TE definition (PRL 85, 461).
- [[sources/wollstadt-2019]] — IDTxl methods (the multivariate TE
  implementation we use).
- `bossomaier-2016` *(to ingest)* — *An Introduction to Transfer Entropy*
  textbook, useful for embedding theory.
