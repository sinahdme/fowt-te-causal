---
title: "SALib"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [software, python, sensitivity]
---

## What it is

Sensitivity Analysis Library (Python). Provides Sobol, Morris, FAST, DGSM
sampling and analysis. We use the Saltelli sample + `analyze.sobol` for
[[concepts/sobol-sensitivity]].

- Repo: https://github.com/SALib/SALib
- pip: `pip install SALib` (declared in `../../../requirements.txt`)

## Role in this project

The **Sobol estimator** for Phase 5 — runs the Saltelli sample over the
locked structural parameters (see [[open-questions]] Q2), consumes the
ensemble of OpenFAST response statistics, and returns `S_i` and `ST_i` per
(parameter, response) pair.

## API hooks we will use

- `SALib.sample.saltelli.sample(problem, N)` — generate the parameter sample
- `SALib.analyze.sobol.analyze(problem, Y)` — compute `S1`, `ST`, `S2`
- `problem` dict: `{'num_vars': d, 'names': [...], 'bounds': [[lo, hi], ...]}`

## Appears in

- [[concepts/sobol-sensitivity]] · [[equations/eq-sobol-first-order]] ·
  [[equations/eq-sobol-total]]
- [[validation/case-4-sobol-3pt-mooring-ea]] — smoke test
- Phase 5 of [[PLAN]]

## Sources

- *(to ingest)* Herman & Usher 2017 — *SALib: An open-source Python library
  for sensitivity analysis*, J. Open Source Softw.
