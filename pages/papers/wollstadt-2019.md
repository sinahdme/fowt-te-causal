---
title: "Paper — Wollstadt 2019 (IDTxl) deep read"
type: paper
created: 2026-05-12
updated: 2026-05-12
sources: ["wollstadt-2019"]
tags: [paper, software, idtxl, methods, deep-read]
---

Companion to [[sources/wollstadt-2019]]. Deeper analytical read of the
JOSS methods paper — comparison to other TE libraries, integration plan
for this project, and three implementation surprises worth recording.

## What's actually new in IDTxl

The paper positions IDTxl as the **next-generation combination of TRENTOOL
and JIDT**. The non-trivial novelty is:

1. **Greedy multivariate-TE inference** (extends TRENTOOL's pairwise-only
   limitation). For each target `Y`, build a parent set `S = {X_1, X_2, …}`
   by iteratively maximising
   `I(Y_t ; X_{t-u}^{(l)} | Y_{t-1}^{(k)}, S)`,
   stopping when the next candidate is not significant under surrogate
   testing. Citations: Lizier 2012, Faes 2011.
2. **Automatic non-uniform embedding selection** (Faes 2011 approach).
   Embedding lags `(k, l, u)` are searched per source-target pair rather
   than fixed globally. Saves the user from per-pair hyperparameter tuning.
3. **Family-wise error correction** over candidate sources via max-statistic
   testing. Critical when scanning many channel pairs (we expect ~10
   sources × ~8 targets in Phase 4).
4. **Both linear-Gaussian and KSG estimators** under the same API. Linear-
   Gaussian is mathematically equivalent to Granger causality
   ([[concepts/granger-causality]] *(stub)*) — the same library covers our
   publication-required baseline.

## Comparison to other TE libraries

| Library | Language | Multivariate TE? | Surrogate sig? | Granger baseline? | GPU? |
|---|---|---|---|---|---|
| **IDTxl** | Python 3 | yes (greedy) | yes (auto) | yes (linear-Gaussian estimator) | yes (CUDA) |
| TRENTOOL | MATLAB | bivariate only | yes | no | no |
| JIDT | Java | yes | yes | yes | no |
| PyInform | Python | bivariate, fewer estimators | manual | no | no |
| PyIF | Python | bivariate | manual | no | no |
| `transfer_entropy` (R) | R | bivariate | manual | no | no |

IDTxl is the clear choice for our pipeline. PyInform was an early
contender but lacks multivariate inference.

## Three implementation surprises (relative to PLAN)

### Surprise 1: Granger baseline is free

PLAN.md Phase 4 currently lists `analysis/baselines.py` as a separate
script using `statsmodels.tsa.stattools.grangercausalitytests`. But IDTxl
exposes the **same multivariate inference engine** with the linear-Gaussian
estimator, which is exact Granger causality. Two implications:

- One fewer dependency.
- Granger vs KSG comparison is **apples-to-apples** — same parent-set
  search, same surrogate test, only the estimator differs. This is
  *stronger* than a separate `statsmodels` Granger because there's no
  confound from a different significance-testing method.

**Action**: update Phase 4 to obtain the Granger baseline from
`MultivariateTE` with `cmi_estimator='OpenCLKraskovCMI'` replaced by
`cmi_estimator='JidtGaussianCMI'`. Document in
`analysis/baselines.py` (which becomes a thin wrapper, not a separate
implementation).

### Surprise 2: Active Information Storage as effect-size denominator

The paper mentions AIS as a separate measure. Looking at the definition,
AIS is exactly the "self-information of `Y`'s past about `Y_t`" — i.e.,
how much of `Y_t` is internally predictable. The natural normalisation for
TE is then

$$
\text{TE}_\text{normalised} = \frac{\text{TE}(X \to Y)}{H(Y_t) - \text{AIS}(Y)}
$$

= fraction of *externally-driven* predictability that comes from `X`. This
is a more meaningful effect size than dividing by `H(Y_t)` alone (which
PLAN currently proposes). Worth adding to Phase 4.

> **Update (2026-07-06):** the pipeline ultimately implements `TE/AIS(Y)`,
> not `TE/(H(Y)−AIS(Y))` as proposed above — for continuous channels under
> KSG, `H(Y)` is a differential entropy (can be ≤ 0), so the "fraction"
> interpretation is not well-defined. All reported `te_frac` values are
> TE/AIS: source information relative to the target's self-predictability,
> not bounded by 1. See `_te_frac` in `analysis/te_pipeline.py`.

### Surprise 3: PID for the follow-up paper

Partial Information Decomposition (Williams 2010, Bertschinger 2014,
Makkeh 2018) is available in IDTxl for discrete data. The reason this is
interesting:

- Conditional TE answers "does wind drive pitch *beyond* what wave already
  explains?"
- PID answers "of the joint information `(wind, wave)` contributes to
  pitch, how much is **redundant** (either alone would suffice), how
  much is **synergistic** (only the combination works), and how much is
  **unique** to each source?"

The synergistic component is interesting for FOWT because nonlinear
interactions between wind and wave (e.g., wind-induced wave-following on
the platform) plausibly contribute. PID would surface this directly.

**But**: PID requires discretisation, the continuous PID is still an open
research problem in 2025/2026. Defer to follow-up paper unless we adopt a
specific discretisation scheme.

## Integration plan with this project

```
analysis/te_pipeline.py
├── load_runs() ........... pull Parquet from data/
├── jitter() .............. add 1e-10 noise per Kraskov-2004 §III.A
├── decimate_to(rate=10) .. anti-alias + downsample
├── run_bivariate_te() .... IDTxl BivariateTE, KSG, surrogate test
├── run_mvte() ............ IDTxl MultivariateTE, KSG, surrogate test
├── run_granger() ......... IDTxl MultivariateTE with JidtGaussianCMI
│                                                  (= Granger baseline)
├── run_ais() ............. IDTxl ActiveInformationStorage (denominator)
└── build_graph() ......... NetworkX, edges = TE or Granger weights
```

This is much tighter than the original PLAN — `te_pipeline.py` becomes
the entire Phase 4 analysis script. `baselines.py` shrinks to a configuration
wrapper.

## Lingering questions

- IDTxl's **JIDT backend requires JDK 11**. Confirmed in
  [[entities/idtxl]]; verified install instructions before Phase 4
  begins.
- **CUDA GPU acceleration** is mentioned but is optional. On the
  user's Windows machine without CUDA, we fall back to CPU — fine for
  our N ≈ 10⁴–10⁵ post-decimation data sizes.
- The paper does not benchmark **maximum tractable problem size**.
  Empirical scaling test (variants of [[validation/case-2-ar1-te-recovery]]
  with N = 10³, 10⁴, 10⁵) should run before committing to the full
  Phase 4 channel matrix.

## Related

- [[sources/wollstadt-2019]] · [[entities/idtxl]]
- [[papers/schreiber-2000]] — the TE definition IDTxl implements
- [[papers/kraskov-2004]] — the estimator IDTxl wraps
- [[concepts/conditional-transfer-entropy]] · [[concepts/surrogate-significance]]
