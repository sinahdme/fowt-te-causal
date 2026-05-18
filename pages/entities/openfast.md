---
title: "OpenFAST (solver)"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [software, solver, simulator]
---

## What it is

NREL's open-source aero-hydro-servo-elastic solver for wind turbines and
floating offshore wind turbines. The "glue code" couples discipline modules
([[entities/openfast-aerodyn]], [[entities/openfast-hydrodyn]], …) through
a common driver and time-step manager.

- Repo: `../../../repos/openfast/`
- Required version: 3.5+
- Distribution: Windows binary from openfast/openfast Releases.

## Properties

| Property | Value |
|---|---|
| Language | Fortran (modules) + C (DLL bridges) |
| Time integration | Predictor-corrector across modules |
| Default `DT_Out` | 0.05 s (20 Hz) |

## Role in this project

Generates every time-series we feed into Phase 4 TE estimation. Driven by
templated input decks via `sims/run_campaign.py` (planned).

## Appears in

- All Phase 2 / Phase 5 simulation work
- [[entities/openfast-overview]] — module index
- [[entities/iea-15mw-volturnus-s]] — input deck

## Sources

- *(to ingest)* Jonkman et al., FAST documentation series.
