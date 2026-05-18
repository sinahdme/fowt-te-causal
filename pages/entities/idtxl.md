---
title: "IDTxl"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: ["wollstadt-2019"]
tags: [software, python, information-theory]
---

## What it is

Information-Dynamics Toolkit Cross-Language (IDTxl) — a Python 3 toolbox
for estimating information-theoretic measures from continuous and discrete
data. Provides bivariate and multivariate Transfer Entropy, Mutual
Information, Active Information Storage, Partial Information Decomposition,
plus local variants and group-level comparisons.

- Repo (local clone): `../../../repos/IDTxl/IDTxl-master/`
- GitHub: https://github.com/pwollstadt/IDTxl
- pip: `pip install idtxl` (declared in `../../../requirements.txt`)
- Backend: JIDT (Java) bridged via JPype1 — requires JDK 11.

Per [[sources/wollstadt-2019]], IDTxl is the **next-generation combination
of TRENTOOL and JIDT**, extending TRENTOOL's pairwise TE analysis to
multivariate and adding a wider variety of estimator types.

## Role in this project

The **TE/MI estimator** for both Phase 4 (env→response TE) and Phase 5
(parameter→response MI). The greedy multivariate-TE inference solves four
practical problems we would otherwise face (per
[[papers/wollstadt-2019]]):

1. Spurious / redundant interactions in multi-channel settings.
2. Missed synergistic interactions.
3. Multiple-comparison statistical control over many candidate sources.
4. Hyperparameter (embedding, lag) optimisation.

## Analyser map

| Analyser | What it does | Where we use it |
|---|---|---|
| `BivariateTE` | `TE(X → Y)` with surrogate sig | quick channel-pair scans |
| `MultivariateTE` | Greedy parent-set inference for `TE(X → Y \| Z, …)` | the main Phase 4 engine |
| `BivariateMI`, `MultivariateMI` | Same for MI | Phase 5 parameter→stat ranking |
| `ActiveInformationStorage` | `H(Y_t) − H(Y_t \| Y^{(k)})` | Phase 4 TE effect-size denominator |
| `JidtKraskovCMI` (estimator) | KSG conditional MI | underlies all TE/MI |
| `JidtGaussianCMI` (estimator) | Linear-Gaussian CMI = exact Granger causality | **publication-required Granger baseline** |

The last row is the surprise from the deep read — see
[[papers/wollstadt-2019]] §"Surprise 1": one library covers both nonlinear
KSG and linear Granger via estimator swap, giving apples-to-apples
comparison. PLAN.md Phase 4 baselines uses this.

## Settings we will fix

| Setting | Value | Why |
|---|---|---|
| `cmi_estimator` | `'JidtKraskovCMI'` (main), `'JidtGaussianCMI'` (Granger baseline) | KSG nonlinear vs linear |
| `kraskov_k` | 4 | Per kraskov-2004 recommendation `k ∈ [2,4]` |
| `n_perm_max_stat` | 200 | Surrogates for max-statistic family-wise correction |
| `n_perm_min_stat` | 200 | Surrogates for individual-source significance |
| `alpha_max_stat` | 0.05 | Family-wise type-I error |
| `max_lag_sources` | per channel | Embedding search range |
| `max_lag_target` | per channel | Target self-history search range |
| `min_lag_sources` | 1 | Exclude instantaneous |

## Appears in

- [[concepts/transfer-entropy]] · [[concepts/mutual-information]] ·
  [[concepts/ksg-estimator]] · [[concepts/surrogate-significance]] ·
  [[concepts/conditional-transfer-entropy]]
- Phase 4 + Phase 5 of [[PLAN]]
- All four validation cases — [[validation/case-1-r-test-parse]] through
  [[validation/case-4-sobol-3pt-mooring-ea]]

## Sources

- [[sources/wollstadt-2019]] — J. Open Source Softw. 4(34), 1081.
- [[papers/wollstadt-2019]] — deep analytical companion with integration plan.
