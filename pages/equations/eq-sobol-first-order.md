---
title: "Equation — Sobol First-Order Index"
type: equation
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [equation, sensitivity, variance-decomposition]
---

## Statement

For scalar output `Y = f(X_1, ..., X_d)` with independent inputs:

$$
S_i \;=\; \frac{\operatorname{Var}_{X_i}\!\bigl(\, \mathbb{E}_{X_{\sim i}}[Y \mid X_i] \,\bigr)}{\operatorname{Var}(Y)}
$$

The fraction of `Var(Y)` that is removed in expectation by fixing `X_i`.
`S_i ∈ [0, 1]`; `Σ_i S_i ≤ 1`, with equality iff `Y` is purely additive.

## Symbols

| Symbol | Meaning |
|---|---|
| `X_i` | The *i*-th input parameter (scalar) |
| `X_~i` | All inputs except `X_i` |
| `Y` | Scalar output (e.g., `std(PtfmPitch)` over a 3000 s window) |
| `S_i` | First-order Sobol index for `X_i` |

## Estimator (Saltelli)

With a Saltelli sample of size `N(2d+2)` we form two base matrices `A`, `B`
and `d` mixing matrices `A_B^{(i)}`. The first-order index estimator is the
Jansen / Saltelli formula

$$
\hat S_i \;=\;
\frac{\frac{1}{N}\sum_{j=1}^{N} f(B_j)\bigl[f(A_B^{(i)}_j) - f(A_j)\bigr]}
     {\hat{\operatorname{Var}}(Y)}
$$

Implemented in [[entities/salib]] (`SALib.analyze.sobol.analyze`).

## Used in

- [[concepts/sobol-sensitivity]] — concept page
- Phase 5 of [[PLAN]] — structural-parameter ranking

## Related

- [[equations/eq-sobol-total]] — total-order index `ST_i`

## Sources

- *(to ingest)* Saltelli 2010 — sample design and Jansen estimators.
