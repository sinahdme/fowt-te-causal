---
title: "TurbSim"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [software, wind, openfast]
---

## What it is

NREL's stochastic full-field turbulent inflow generator. Bundled with
OpenFAST. Produces `.bts` binary files with three-component wind velocity on
a regular `(y, z, t)` grid, consumed by [[entities/openfast-inflowwind]].

- Source: `../../../repos/openfast/modules/turbsim/`
- Input file: `*.inp` per case

## Role in this project

Generates the **wind input** for every Phase 2 simulation case.

## Properties / parameters

| Parameter | Role |
|---|---|
| `URef` | Reference mean wind speed at hub height |
| `IECturbc` | Turbulence class (NTM A/B/C, ETM, …) |
| `IEC_WindType` | Wind condition (NTM, EWM, EOG, …) |
| `RandSeed1`, `RandSeed2` | Realisation seeds |
| `GridHeight`, `GridWidth`, `NumGrid_Z`, `NumGrid_Y` | Grid spec |

## Phase 2 plan

Pre-generate one `.bts` per (mean wind speed, seed) combo: 8/11/15/20 m/s ×
6 seeds = 24 boxes. Reused across DLC sets A, B, C.

## Appears in

- [[entities/openfast-inflowwind]] · [[entities/openfast-aerodyn]]
- Phase 2 of [[PLAN]]

## Sources

- *(to ingest)* Jonkman & Buhl, *TurbSim User's Guide*, NREL/EL-500-46198.
