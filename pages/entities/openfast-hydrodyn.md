---
title: "OpenFAST HydroDyn"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, hydrodynamics]
---

## What it is

Hydrodynamics on the floating platform. Combines potential-flow loading (from
WAMIT-precomputed coefficients) with strip-theory Morison terms. Produces the
wave-induced excitation that drives [[entities/openfast-elastodyn]]'s
platform DOFs.

- Source: `../../../repos/openfast/modules/hydrodyn/`
- Input file: `HydroDyn.dat`

See [[concepts/jonswap-spectrum]] for the wave-spectrum model and
[[equations/eq-morison]] *(stub)* for the strip-theory term.

## Properties / parameters

| Parameter | Role |
|---|---|
| `WaveMod` | 0 still, 2 JONSWAP, 5 user-defined, … |
| `WaveHs`, `WaveTp`, `WaveDir`, `WavePkShp` | JONSWAP parameters |
| `WaveSeed(1)`, `WaveSeed(2)` | Random seeds for the irregular sea |
| `PtfmRefxt`, `PtfmRefyt`, `PtfmRefzt` | Hydro reference point |

## TE source candidates

- `Wave1Elev` — wave elevation at reference point [m]
- `WavesF1xi`, `WavesF1zi` — wave-induced force components

## Phase 2 sweep

`Hs` ∈ {1.5, 3.0, 5.0} m, `Tp` correlated to wind speed; 6 wave seeds per
case. Coupled with wind seeds for DLC set A, decoupled for DLC set B
(see [[PLAN]]).

## Appears in

- [[entities/openfast-overview]] · [[entities/openfast-elastodyn]] ·
  [[entities/openfast-moordyn]]
- [[entities/iea-15mw-volturnus-s]] — VolturnUS-S WAMIT files

## Sources

- *(to ingest)* OpenFAST HydroDyn manual
