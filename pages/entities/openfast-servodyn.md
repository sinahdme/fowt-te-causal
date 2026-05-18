---
title: "OpenFAST ServoDyn"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, controller]
---

## What it is

Generator + controller interface. Loads a Bladed-style DLL (typically
[[entities/rosco]]) and exchanges blade-pitch and generator-torque commands
with [[entities/openfast-elastodyn]] each time step.

- Source: `../../../repos/openfast/modules/servodyn/`
- Input file: `ServoDyn.dat`

## Properties / parameters

| Parameter | Role |
|---|---|
| `DLL_FileName` | Path to the controller DLL |
| `DLL_InFile` | Controller input file (e.g., `DISCON.IN` for ROSCO) |
| `PCMode`, `VSContrl`, `YCMode` | Pitch / torque / yaw control modes |

## Output channels

- `BldPitch1`, `BldPitch2`, `BldPitch3` — blade pitch commands
- `GenTq`, `GenPwr`, `GenSpeed` — generator state
- `RotSpeed`, `RotPwr` — rotor state

`GenPwr` is a strong TE target candidate (objective for power-quality
analyses).

## Sweepable parameters (Phase 5)

Controller gains exposed through `DISCON.IN` (ROSCO):
- `PC_KP`, `PC_KI` — blade-pitch PI gains
- `VS_KP`, `VS_KI` — torque PI gains
- `F_LPFCornerFreq` — generator-speed LP filter cut-off

See [[entities/rosco]].

## Appears in

- [[entities/openfast-overview]] · [[entities/openfast-elastodyn]] ·
  [[entities/openfast-aerodyn]] · [[entities/rosco]]

## Sources

- *(to ingest)* OpenFAST ServoDyn manual
