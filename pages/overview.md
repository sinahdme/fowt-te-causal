---
title: "Overview"
type: overview
created: 2026-05-12
updated: 2026-05-12
tags: [meta, synthesis]
---

# Project Overview

## What we are doing

Quantifying the causal drivers of floating offshore wind turbine (FOWT)
structural response, separating two input categories:

1. **Environmental forcing** — wind and wave time histories. These are
   stochastic time series, so [[concepts/transfer-entropy]] (TE) applies
   naturally. We use the KSG estimator ([[concepts/ksg-estimator]]) via
   [[entities/idtxl]] and significance-test against time-shift / IAAFT
   surrogates ([[concepts/surrogate-significance]]).
2. **Structural design parameters** — mooring stiffness, platform inertia,
   tower stiffness, controller gains. These are constants within a single
   OpenFAST run, so TE does not apply. We use Sobol sensitivity
   ([[concepts/sobol-sensitivity]]) via [[entities/salib]] plus mutual
   information ([[concepts/mutual-information]]) for a nonlinear companion
   ranking.

## Reference setup

- Platform: [[entities/iea-15mw-volturnus-s]] (locked).
- Solver: [[entities/openfast]] 3.5+ on Windows.
- Wind generator: [[entities/turbsim]] (bundled with OpenFAST).
- Wave model: JONSWAP via [[entities/openfast-hydrodyn]].
- Controller: [[entities/rosco]].

## Pipeline (six phases)

```
Phase 1  Knowledge base       →  Obsidian wiki + OpenFAST repos       [DONE]
Phase 2  Simulation campaign  →  DLC matrix runs via OpenFAST         [GATED]
Phase 3  Data preprocessing   →  .outb → Parquet, decimate, detrend   [pending]
Phase 4  TE: env → response   →  IDTxl bivariate + conditional TE     [pending]
Phase 5  Param causality      →  SALib Sobol + IDTxl MI ensemble      [pending]
Phase 6  Reporting            →  Combined causal graph + narrative    [pending]
```

Phase 2 onward is gated on the user providing (see [[open-questions]]):
- The list of OpenFAST output channels to record as TE targets
  (linked to the user's optimization objectives).
- The list of structural parameters to sweep, with ranges.

## How the pieces connect

Wind and wave time series enter through [[entities/openfast-inflowwind]] and
[[entities/openfast-hydrodyn]]. The platform DOFs and tower loads come out
of [[entities/openfast-elastodyn]]. Blade loads come from
[[entities/openfast-aerodyn]] / [[entities/openfast-beamdyn]]. Mooring
tensions come from [[entities/openfast-moordyn]]. Controller / generator
signals come from [[entities/openfast-servodyn]] via [[entities/rosco]].

For Phase 4 we estimate TE(wind → response) and TE(wave → response) per
candidate response channel, plus conditional TE to disentangle wind/wave
contributions when they correlate.

For Phase 5 we run a Saltelli sample over structural parameters; for each
sample point we record response-summary statistics (std, DEL, max, mean);
we then compute Sobol `S_i`/`ST_i` and MI between parameter and statistic.

Phase 6 fuses both into a single directed weighted graph with edge weight
= normalized TE (for env channels) or Sobol `ST_i` (for parameters).

## What's verified so far

Nothing yet — all four cases in [[validation/case-1-r-test-parse]] through
[[validation/case-4-sobol-3pt-mooring-ea]] are pending.

## Related

- [[PLAN]] — full project plan
- [[LLM_Wiki_Pattern]] — wiki methodology
- [[SCHEMA]] — domain-specific schema delta (note: lives one folder up, at `wiki/SCHEMA.md`)
