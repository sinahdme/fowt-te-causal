---
title: "Index"
type: index
created: 2026-05-12
updated: 2026-05-13
tags: [meta, index, post-ingest]
---

# Index

Catalogue of every page in the wiki. One line per page. Drill from here.

See [[overview]] for the synthesis, [[log]] for chronology, [[open-questions]]
for tracked research questions, [[wiki-improvement-plan]] for the meta-plan.

## Overview & meta

- [[overview]] — top-level synthesis of the project
- [[log]] — append-only event log (ingests, queries, lints)
- [[open-questions]] — tracked research questions, statuses
- [[wiki-improvement-plan]] — how the wiki itself should evolve

## Concepts

- [[concepts/transfer-entropy]] — directional information transfer (project core)
- [[concepts/conditional-transfer-entropy]] — TE conditioned on third variable
- [[concepts/mutual-information]] — symmetric statistical dependence
- [[concepts/ksg-estimator]] — Kraskov–Stögbauer–Grassberger MI/TE estimator
- [[concepts/surrogate-significance]] — null-distribution testing for TE
- [[concepts/sobol-sensitivity]] — variance-based parameter sensitivity
- [[concepts/jonswap-spectrum]] — irregular sea-state model *(stub)*
- [[concepts/blade-element-momentum]] — rotor aerodynamic model *(stub)*
- [[concepts/output-channels]] — OpenFAST channel reference *(stub)*

## Equations

- [[equations/eq-transfer-entropy]] — TE definition
- [[equations/eq-mutual-information]] — MI definition
- [[equations/eq-sobol-first-order]] — Sobol `S_i`
- [[equations/eq-sobol-total]] — Sobol `ST_i`

## Entities — OpenFAST modules

- [[entities/openfast-overview]] — module map and driver flow
- [[entities/openfast-aerodyn]] — rotor aerodynamics
- [[entities/openfast-inflowwind]] — wind input field
- [[entities/openfast-elastodyn]] — platform + tower + rotor structure
- [[entities/openfast-beamdyn]] — nonlinear blade beam
- [[entities/openfast-hydrodyn]] — hydrodynamics on platform
- [[entities/openfast-servodyn]] — controller / generator interface
- [[entities/openfast-moordyn]] — dynamic mooring
- [[entities/openfast-subdyn]] — substructure dynamics (inactive for floating)

## Entities — reference platforms

- [[entities/iea-15mw-volturnus-s]] — primary reference platform (IEA-15MW, locked)
- [[entities/iea-22-280-rwt-semi]] *(stub)* — second platform for Q5 multi-platform comparison (locked 2026-05-13)

## Entities — software

- [[entities/idtxl]] — Information-Dynamics Toolkit for TE/MI estimation
- [[entities/salib]] — Sensitivity Analysis Library (Sobol)
- [[entities/openfast]] — the solver itself
- [[entities/openfast-toolbox]] — `.out`/`.outb` Python reader
- [[entities/rosco]] — reference open-source wind-turbine controller
- [[entities/moorpy]] — quasi-static mooring solver
- [[entities/weis]] — wind-energy optimization framework
- [[entities/turbsim]] — turbulent inflow generator
- [[entities/raft]] — frequency-domain coupled FOWT solver (Phase 5 ensemble engine)

## Validation cases (from [[PLAN]] §Verification)

- [[validation/case-1-r-test-parse]] — confirm OpenFAST output parsing
- [[validation/case-2-ar1-te-recovery]] — synthetic TE known-answer test
- [[validation/case-3-iea15-single-case-te]] — one full-case TE end-to-end
- [[validation/case-4-sobol-3pt-mooring-ea]] — minimal Sobol smoke test

## Sources

- [[sources/schreiber-2000]] — original Transfer Entropy definition (PRL 85, 461)
- [[sources/kraskov-2004]] — KSG nearest-neighbour MI estimator (PRE 69, 066138)
- [[sources/wollstadt-2019]] — IDTxl methods paper (JOSS 4(34), 1081)
- [[sources/jeon-2025]] — predecessor RL optimisation of FOWT substructure (KSME 2025); defines this project's optimisation problem

## Papers (deep analytical companions)

- [[papers/schreiber-2000]] — derivation chain, alternatives table, FOWT-specific implications
- [[papers/kraskov-2004]] — KSG estimator derivation, comparison vs binning, 10⁻¹⁰ jitter rationale
- [[papers/wollstadt-2019]] — IDTxl integration plan, Granger-baseline-free insight, AIS denominator idea

## Analyses

*(empty — filed-back query answers go here.)*
