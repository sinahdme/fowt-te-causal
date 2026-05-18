---
title: "Equation — Sobol Total-Order Index"
type: equation
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [equation, sensitivity, variance-decomposition]
---

## Statement

For scalar output `Y = f(X_1, ..., X_d)`:

$$
ST_i \;=\;
\frac{\mathbb{E}_{X_{\sim i}}\!\bigl[\,\operatorname{Var}_{X_i}(Y \mid X_{\sim i})\,\bigr]}{\operatorname{Var}(Y)}
\;=\;
1 \;-\; \frac{\operatorname{Var}_{X_{\sim i}}\!\bigl(\,\mathbb{E}_{X_i}[Y \mid X_{\sim i}]\,\bigr)}{\operatorname{Var}(Y)}
$$

The fraction of `Var(Y)` attributable to `X_i` **including** all
interactions involving `X_i`. `ST_i ≥ S_i`; `ST_i ≥ 0` and `Σ_i ST_i ≥ 1`
in general.

## Symbols

See [[equations/eq-sobol-first-order]].

## Estimator (Saltelli)

$$
\hat{ST}_i \;=\;
\frac{\frac{1}{2N}\sum_{j=1}^{N} \bigl[ f(A_j) - f(A_B^{(i)}_j) \bigr]^2}
     {\hat{\operatorname{Var}}(Y)}
$$

Implemented in [[entities/salib]].

## Used in

- [[concepts/sobol-sensitivity]] — concept page
- Phase 5 of [[PLAN]] — structural-parameter ranking; `ST_i` is the
  edge weight in the Phase 6 combined causal graph.

## Related

- [[equations/eq-sobol-first-order]] — first-order index `S_i`

## Sources

- *(to ingest)* Saltelli 2010 / Homma & Saltelli 1996.
