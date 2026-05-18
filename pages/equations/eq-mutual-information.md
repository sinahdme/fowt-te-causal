---
title: "Equation — Mutual Information"
type: equation
created: 2026-05-12
updated: 2026-05-12
sources: ["kraskov-2004"]
tags: [equation, information-theory]
---

## Statement

For continuous random variables `X` and `Y` with joint density `μ(x, y)`
and marginals `μ_x(x)`, `μ_y(y)`, MI is defined in kraskov-2004 (Eq. 1):

$$
I(X;Y) \;=\; \int\!\!\int dx\,dy\; \mu(x,y)\,
  \log\!\frac{\mu(x,y)}{\mu_x(x)\,\mu_y(y)}
$$

Equivalently `I(X;Y) = H(X) + H(Y) − H(X, Y)` where `H` is differential
entropy (kraskov-2004 Eq. 5).

## Symbols

| Symbol | Meaning | Units |
|---|---|---|
| `μ(x,y)` | Joint density | – |
| `μ_x(x), μ_y(y)` | Marginal densities | – |
| `I(X;Y)` | Mutual information | nats (bits if log base 2) |

> "The base of the logarithm determines the units in which information is
> measured. In particular, taking base two leads to information measured
> in bits. In the following, we always will use natural logarithms."
> (kraskov-2004, p. 1)

## Properties

- **Symmetric**: `I(X;Y) = I(Y;X)`.
- **Non-negative**: `I(X;Y) ≥ 0`, equality iff `X ⊥ Y`.
- **Higher-dim form** (kraskov-2004 Eq. 30) for joint MI of `m` variables:

  $$
  I(X_1, …, X_m) = H(X_1) + … + H(X_m) - H(X_1, …, X_m)
  $$

  This underwrites conditional MI / TE estimation in
  [[concepts/conditional-transfer-entropy]] — the same KSG bias-cancellation
  argument extends cleanly.
- **Invariant under reparametrisation** of marginals (kraskov-2004 Sec.
  III.A): if `X' = F(X)` and `Y' = G(Y)` are homeomorphisms, then
  `I(X,Y) = I(X',Y')`. This is why rank-ordering (a monotone transform)
  is a valid pre-processing step for static MI estimation; we use it for
  Phase 5 parameter→stat ranking.

## Estimator

KSG MI (kraskov-2004 Eqs. 8-9). See [[concepts/ksg-estimator]] for
hyperparameters, [[papers/kraskov-2004]] for the derivation chain.

## Used in

- [[concepts/mutual-information]] — concept page
- [[equations/eq-transfer-entropy]] — TE = conditional MI
- [[concepts/sobol-sensitivity]] §"Companion ranking" — Phase 5 nonlinear
  parameter ranking
- [[concepts/conditional-transfer-entropy]] — generalised to higher dim

## Sources

- [[sources/kraskov-2004]] — defines MI and the KSG estimator.
- [[papers/kraskov-2004]] — deep analytical companion.
- `cover-thomas` *(to ingest if needed)* — *Elements of Information Theory* textbook.
