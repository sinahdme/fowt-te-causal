---
title: "OpenFAST MoorDyn"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, mooring]
---

## What it is

Lumped-mass dynamic mooring solver. Computes fairlead reaction forces on the
floating platform given each line's geometry, axial stiffness `EA`, mass per
unit length, and seabed contact. Replaces the older quasi-static MAP++.

- Source: `../../../repos/openfast/modules/moordyn/`
- Input file: `MoorDyn.dat`
- Standalone Python (quasi-static) equivalent: [[entities/moorpy]]

See [[concepts/catenary-mooring]] *(stub)* for the underlying physics.

## Properties / parameters

| Parameter | Role |
|---|---|
| `LineType` block (`Diam`, `MassDen`, `EA`, …) | Per line-type material props |
| `Line` block (`UnstrLen`, `NumSegs`, end nodes) | Per-line geometry |
| `Point` block (anchor / fairlead positions) | Boundary conditions |

## TE target candidates

- `FAIRTEN1`, `FAIRTEN2`, `FAIRTEN3` — fairlead tensions [N]
- `ANCHTEN*` — anchor tensions
- `Con<n>FX/FY/FZ` — connection-node forces

## Sweepable parameters (Phase 5)

- `EA` per line type (±20 %)
- `UnstrLen` per line (±5 %)
- Fairlead radius / position (via `Point` z- and r-coords)
- Anchor radius

## Appears in

- [[entities/openfast-overview]] · [[entities/openfast-hydrodyn]] ·
  [[entities/openfast-elastodyn]]
- [[entities/iea-15mw-volturnus-s]] — VolturnUS-S 3-line catenary
- [[entities/moorpy]] — quasi-static sanity-check tool

## Sources

- *(to ingest)* OpenFAST MoorDyn manual
