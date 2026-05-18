---
title: "OpenFAST AeroDyn"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, aerodynamics]
---

## What it is

OpenFAST's rotor aerodynamics module. Computes blade aerodynamic loads via
Blade Element Momentum (BEM) theory or OLAF (free-vortex wake), given the
inflow field from [[entities/openfast-inflowwind]] and the blade geometry
from [[entities/openfast-elastodyn]] / [[entities/openfast-beamdyn]].

- Source: `../../../repos/openfast/modules/aerodyn/`
- Input file: `AeroDyn15.dat`

See also [[concepts/blade-element-momentum]] for the theory.

## Properties / parameters

| Parameter | Role |
|---|---|
| `WakeMod` | BEM vs OLAF wake model |
| `AFAeroMod` | Steady vs Beddoes–Leishman dynamic stall |
| `TwrPotent` | Tower potential-flow influence |
| `BlSpn`, `BlChord`, `BlTwist` (per blade `.dat`) | Spanwise blade geometry |

## TE source candidates

- Rotor thrust, rotor torque (these reach the platform via [[entities/openfast-elastodyn]])

## TE target candidates

- `RootMyc1`, `RootMxc1`, `RootMzc1` — blade-root moments

## Appears in

- [[entities/openfast-overview]] · [[entities/iea-15mw-volturnus-s]]

## Sources

- *(to ingest)* OpenFAST AeroDyn manual — `repos/openfast/docs/source/user/aerodyn/`
