---
title: "OpenFAST Overview"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, simulator, overview]
---

## What it is

OpenFAST is NREL's aero-hydro-servo-elastic multi-physics solver for wind
turbines, including floating platforms. The "glue code" couples
discipline-specific modules through a common driver and time-step manager.

- Source: `../../../repos/openfast/`
- Docs: `../../../repos/openfast/docs/source/` (RST — to be converted to MD
  under `../../raw/extracts/openfast-docs/` by `analysis/build_vault.py`).
- Solver tool entity: [[entities/openfast]]

## Module map

| Module | Discipline | Key inputs | Key outputs |
|---|---|---|---|
| [[entities/openfast-aerodyn]]    | Rotor aerodynamics       | Inflow field, blade geom | Blade loads, rotor thrust/torque |
| [[entities/openfast-inflowwind]] | Inflow turbulence        | TurbSim `.bts` file      | Wind velocity at points |
| [[entities/openfast-elastodyn]]  | Rigid + flexible bodies  | Tower / blade modal data | Platform DOFs, tower base loads |
| [[entities/openfast-beamdyn]]    | Nonlinear blade beam     | Blade BD inputs          | Blade root moments |
| [[entities/openfast-hydrodyn]]   | Hydrodynamics            | Wave spectrum, body geom | Hydro forces on platform |
| [[entities/openfast-servodyn]]   | Controller / generator   | Bladed-style DLL         | Blade pitch, generator torque |
| [[entities/openfast-moordyn]]    | Dynamic mooring          | Line geometry, EA, EI    | Fairlead tensions |
| [[entities/openfast-subdyn]]     | Substructure dynamics    | FE model of substructure | Member loads |

## Driver flow (per time step)

```
InflowWind  →  AeroDyn ──┐
                          ├──► ElastoDyn ──► ServoDyn ──► (next step)
HydroDyn  ──► MoorDyn ────┘
```

ElastoDyn integrates platform + tower + rotor structural DOFs given the
forces from the discipline modules.

## Inputs we will template (Phase 2)

- `<case>.fst` — master driver
- `ElastoDyn.dat` — initial conditions, structural DOF flags
- `HydroDyn.dat` — wave spectrum, JONSWAP `Hs`/`Tp`
- `InflowWind.dat` — wind type, TurbSim `.bts` path
- `MoorDyn.dat` — line `EA`, length, fairlead positions

## Appears in

- [[entities/iea-15mw-volturnus-s]] — reference floating platform configuration
- [[validation/case-1-r-test-parse]] — first parsing smoke test

## Sources

- *(to ingest)* OpenFAST documentation — `repos/openfast/docs/`
