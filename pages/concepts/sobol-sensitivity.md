---
title: "Sobol Sensitivity Indices"
type: concept
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [sensitivity, statistics, variance-decomposition]
---

## Definition

Variance-based global sensitivity measures for parameter → output
relationships. For output `Y` and inputs `X = (X_1, ..., X_d)`:

- First-order index `S_i` — see [[equations/eq-sobol-first-order]].
- Total index `ST_i` — see [[equations/eq-sobol-total]].

`S_i` is the fraction of `Var(Y)` explained by `X_i` alone; `ST_i` includes
all interactions involving `X_i`.

## Why it matters here

This is the **core method for Phase 5** of this project — quantifying the
causal effect of structural design parameters on FOWT response. We use
Sobol instead of [[concepts/transfer-entropy]] because design parameters
are constants per OpenFAST run; no source time series exists for TE to
operate on (decision recorded in `phase5_param_method` memory).

## Sampling

Saltelli's extended sample of size `N (2d + 2)` enables both `S_i` and
`ST_i` from the same simulation set. Implemented in [[entities/salib]].

## Outputs `Y` we apply this to

Per response channel, summary statistics over the 3000 s analysis window
of each OpenFAST run:

- `std(response)` — fluctuation magnitude
- damage equivalent load (DEL) — fatigue proxy via rainflow counting
- `max|response|` — extreme proxy
- `mean(response)` — bias / trim

See [[concepts/damage-equivalent-load]] *(stub)*.

## Companion ranking

[[concepts/mutual-information]] across the same Saltelli ensemble gives a
nonlinear, information-theoretic ranking that complements Sobol.

## Related concepts

- [[concepts/mutual-information]] · [[concepts/transfer-entropy]] ·
  [[concepts/saltelli-sampling]] *(stub)*

## Sources

- *(to ingest)* Sobol 2001 — original variance-decomposition paper.
- *(to ingest)* Saltelli 2010 — sampling design.
