---
title: "OpenFAST InflowWind"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, wind]
---

## What it is

Provides the spatially and temporally varying wind field to
[[entities/openfast-aerodyn]]. For this project's campaign we will use
[[entities/turbsim]]-generated `.bts` turbulence boxes.

- Source: `../../../repos/openfast/modules/inflowwind/`
- Input file: `InflowWind.dat`

## Properties / parameters

| Parameter | Role |
|---|---|
| `WindType` | 1 = steady, 2 = uniform, 3 = `.bts` TurbSim, … |
| `FileName_BTS` | Path to TurbSim full-field file |
| `RefHt` | Reference height for the inflow |
| `NumWindPts` | Number of explicit output points |

## TE source candidates

- `Wind1VelX`, `Wind1VelY`, `Wind1VelZ` — wind at hub-height reference point

## Phase 2 sweep parameters

Mean wind speed 8 / 11 / 15 / 20 m/s, NTM class B, 6 seeds each. Generated
ahead of time with [[entities/turbsim]].

## Appears in

- [[entities/openfast-overview]] · [[entities/openfast-aerodyn]]
- [[entities/iea-15mw-volturnus-s]]

## Sources

- *(to ingest)* OpenFAST InflowWind manual
