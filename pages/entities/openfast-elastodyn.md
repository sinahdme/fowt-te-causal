---
title: "OpenFAST ElastoDyn"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, structure]
---

## What it is

Structural dynamics: integrates rigid-body platform DOFs (surge / sway /
heave / roll / pitch / yaw), tower fore-aft / side-to-side modes, drivetrain,
and rotor. Receives forces from [[entities/openfast-aerodyn]],
[[entities/openfast-hydrodyn]], and [[entities/openfast-moordyn]].

- Source: `../../../repos/openfast/modules/elastodyn/`
- Input file: `ElastoDyn.dat`

## Properties / parameters

| Parameter | Role |
|---|---|
| `PtfmSgDOF` … `PtfmYDOF` (6 flags) | Enable each platform DOF |
| `TwFADOF1/2`, `TwSSDOF1/2` | Tower fore-aft / side-side modes |
| `PtfmMass`, `PtfmRIner`, `PtfmCMzt` | Platform inertia properties |
| Tower file (`*_ElastoDyn_tower.dat`) | Tower modal stiffness / mass distribution |

## TE target candidates (likely response channels)

| Channel | Meaning | Units |
|---|---|---|
| `PtfmSurge`, `PtfmSway`, `PtfmHeave` | Platform translation | m |
| `PtfmRoll`, `PtfmPitch`, `PtfmYaw`   | Platform rotation     | deg |
| `TwrBsMyt`, `TwrBsMxt`               | Tower base bending moment | kN·m |
| `TTDspFA`, `TTDspSS`                 | Tower-top deflection | m |
| `RootMyc1`                           | Blade 1 root flapwise moment | kN·m |

These are the strongest candidates for the user's Q1 lock
(see [[open-questions]]).

## Sweepable parameters (Phase 5)

- Platform mass `PtfmMass`, vertical COG `PtfmCMzt` (±10 %, ±5 %)
- Tower modal stiffness scale (±20 % via tower file)

## Appears in

- [[entities/openfast-overview]] · [[entities/openfast-hydrodyn]] ·
  [[entities/openfast-aerodyn]] · [[entities/openfast-servodyn]]
- [[entities/iea-15mw-volturnus-s]]

## Sources

- *(to ingest)* OpenFAST ElastoDyn manual
