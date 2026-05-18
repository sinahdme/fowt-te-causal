---
title: "Wollstadt et al. 2019 — IDTxl: The Information Dynamics Toolkit xl"
type: source
created: 2026-05-12
updated: 2026-05-12
source_path: "raw/papers/Wollstadt-2019-IDTxl.md"
authors: ["Wollstadt, P.", "Lizier, J. T.", "Vicente, R.", "Finn, C.", "Martinez-Zarzuela, M.", "Mediano, P.", "Novelli, L.", "Wibral, M."]
year: 2019
venue: "Journal of Open Source Software"
doi: "10.21105/joss.01081"
citation_key: "wollstadt-2019"
tags: [source, software, methods, idtxl]
sources: []
---

## Citation

Wollstadt, P., Lizier, J. T., Vicente, R., Finn, C., Martinez-Zarzuela, M.,
Mediano, P., Novelli, L., & Wibral, M. (2019). "IDTxl: The Information
Dynamics Toolkit xl: a Python package for the efficient analysis of
multivariate information dynamics in networks." *Journal of Open Source
Software* **4**(34), 1081.

Source repo also cloned to `repos/IDTxl/`; the JOSS manuscript itself is
the canonical source artefact (mirrored to `raw/papers/Wollstadt-2019-IDTxl.md`).

## TL;DR

- IDTxl is the **next-generation successor of TRENTOOL + JIDT**, written
  in pure Python 3 with no proprietary dependencies. Extends TRENTOOL's
  pairwise TE to **multivariate** TE.
- Solves four practical problems that hand-rolled TE pipelines face:
  1. Spurious / redundant interactions in multivariate settings.
  2. Missed synergistic interactions.
  3. Multiple-comparison statistical control over many candidate sources.
  4. Hyperparameter (embedding, lag) optimisation.
- **Greedy iterative parent-set construction**: for each target, sources
  are added one at a time by maximising conditional MI, with surrogate-
  based stopping. Automatically yields a non-uniform multivariate
  embedding (cites Faes 2011) and optimised source-target delays (Wibral 2013).
- Estimators include **linear-Gaussian (= Granger)** and **nonlinear KSG**,
  with both CPU and GPU implementations.
- Measures provided: bivariate TE, multivariate TE, bivariate MI,
  multivariate MI, **active information storage (AIS)**, **partial
  information decomposition (PID)** — plus local variants.

## Key claims

- "An exhaustive multivariate approach is computationally intractable,
  even for a small number of potential sources" — the greedy approach is
  the practical fix.
- "Rigorous statistical controls (based on comparison to null
  distributions from time-series surrogates) are used to gate parent
  selection and to provide automatic stopping conditions for the
  inference, requiring only a minimum of user-specified settings."
- "Linear Gaussian estimators (i.e. Granger causality, Granger 1969)
  for speed versus nonlinear estimators (e.g. Kraskov 2004) for accuracy"
  — same library covers both ends.

## Methods

- **Conditional MI greedy search**: builds a parent set `S` for target `Y`
  by repeatedly adding the candidate source-history that maximises
  `I(Y_t ; X_{t-u}^{(l)} | Y_{t-1}^{(k)}, S)`, stopping when the next
  addition is not significant under surrogate testing.
- **Surrogate generation**: time-shift and trial-shuffle surrogates,
  configurable per analyser.
- **Family-wise error correction**: max-statistic correction over
  candidate sources (controls type-I error at the network level).

## Data / cases

The JOSS paper is a methods description; no datasets reported. Validation
cases live in the [IDTxl docs](https://github.com/pwollstadt/IDTxl) and
the cited methods papers (Lizier 2012, Faes 2011, Wibral 2013).

## How it informs this project

- **Multivariate TE for free.** Our Phase 4 conditional-TE plan
  (`TE(wind → pitch | wave)`) maps directly onto IDTxl's `MultivariateTE`
  analyser — we get greedy parent-set construction, automatic embedding
  selection, and surrogate-based significance testing in one call.
- **Built-in Granger baseline.** A major surprise relative to our PLAN:
  the publication-required Granger baseline (Phase 4 baselines) can come
  from the same library via the linear-Gaussian estimator option, not a
  separate `statsmodels` call. Reduces the dependency footprint and gives
  apples-to-apples Granger vs KSG comparisons. Update
  `analysis/baselines.py` accordingly.
- **AIS as a bonus diagnostic.** Active Information Storage quantifies
  how much of `Y_t` is predicted by `Y`'s own past — useful as a denominator
  for "fraction of predictability transferred." Worth adding to the Phase
  4 effect-size normalisation.
- **PID for future paper.** Partial Information Decomposition would let us
  cleanly answer "how much of the wind+wave joint information about pitch
  is redundant vs synergistic?" — a stronger version of the
  conditional-TE story. Defer to follow-up paper.

## Open questions / contradictions

- The JOSS paper omits performance benchmarks. We should run our own scaling
  test (synthetic data, varying N) before committing to multivariate TE
  for large channel sets — see [[validation/case-2-ar1-te-recovery]] and
  Q4 in [[open-questions]].
- The greedy approach is approximation, not optimal — there are pathological
  cases where it misses parents. We will document the embedding `(k, l, u)`
  found per (source, target) pair and check for stability.
