---
title: "ROSCO"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [software, controller, fortran, dll]
---

## What it is

NREL's reference open-source controller for utility-scale wind turbines.
Implements the standard variable-speed / variable-pitch baseline plus
floating-platform-friendly extensions (peak shaving, individual pitch,
floating feedback). Loaded by [[entities/openfast-servodyn]] as a
Bladed-style DLL.

- Repo: `../../../repos/ROSCO/`
- Toolbox: `pip install rosco`
- Input file: `DISCON.IN`

## Role in this project

The **controller** for our IEA-15MW VolturnUS-S simulation campaign. Its
gain parameters are the controller-side knobs in the Phase 5 sweep
shortlist (see [[entities/iea-15mw-volturnus-s]]).

## Sweepable parameters (Phase 5 candidates)

| Parameter | Role | Sweep range |
|---|---|---|
| `PC_KP` | Blade-pitch P gain | ±50 % |
| `PC_KI` | Blade-pitch I gain | ±50 % |
| `VS_KP` | Torque P gain | ±50 % |
| `VS_KI` | Torque I gain | ±50 % |
| `F_LPFCornerFreq` | Generator-speed LP filter | tune carefully |

## Appears in

- [[entities/openfast-servodyn]] · [[entities/iea-15mw-volturnus-s]]
- Phase 5 controller-gain ensemble

## Sources

- *(to ingest)* Abbas et al., *A reference open-source controller for
  fixed and floating offshore wind turbines* (Wind Energy Sci.).
