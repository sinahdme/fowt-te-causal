---
title: "MoorPy"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [software, python, mooring]
---

## What it is

NREL's lightweight Python quasi-static mooring solver. Computes mooring
restoring forces and the static-equilibrium position of a floating platform
given line geometry and material properties.

- Repo: `../../../repos/MoorPy/`
- pip: `pip install moorpy`

## Role in this project

**Sanity-check tool** for the dynamic [[entities/openfast-moordyn]] runs.
Useful for:

- Generating restoring-curve plots before launching a 3600 s OpenFAST run.
- Quickly screening proposed Phase 5 sweep ranges for mooring
  parameters (catches geometry-breaking values cheaply).
- Verifying that a swept `EA` change actually shifts the surge restoring
  curve in the expected direction.

## Appears in

- [[entities/openfast-moordyn]]
- Phase 5 pre-screening (planned)

## Sources

- *(no separate paper — repo docs)*
