---
title: "Mutual Information"
type: concept
created: 2026-05-12
updated: 2026-05-12
sources: ["kraskov-2004"]
tags: [information-theory]
---

## Definition

Mutual information `I(X ; Y)` is the symmetric, non-directional measure of
statistical dependence between two random variables. Zero iff `X` and `Y`
are independent; captures arbitrary nonlinear dependence.

Formal statement: see [[equations/eq-mutual-information]]. The continuous-
density form is given in kraskov-2004 (Eq. 1, p. 1).

## Why it matters here

Two distinct uses in this project:

1. **Phase 5 companion to [[concepts/sobol-sensitivity]]**: compute
   `I(parameter ; response_summary_statistic)` across the Saltelli ensemble
   to give a nonlinear, information-theoretic ranking of structural
   parameters. Recommended in `phase5_param_method` memory.
2. **Building block for [[concepts/transfer-entropy]]**: TE is a conditional
   mutual information; the estimator
   ([[concepts/ksg-estimator]]) is the same MI estimator generalised.

## Estimator

KSG MI from [[entities/idtxl]] (`JidtKraskovMI`). The estimator is exact
for independent variables — verified across multiple distribution families
in kraskov-2004 (Sec. III). This is the property that makes the surrogate
test in [[concepts/surrogate-significance]] sound.

## Related concepts

- [[concepts/transfer-entropy]] · [[concepts/ksg-estimator]] ·
  [[concepts/sobol-sensitivity]]

## Sources

- [[sources/kraskov-2004]] — Phys. Rev. E 69, 066138.
- [[papers/kraskov-2004]] — deep analytical re-read.
