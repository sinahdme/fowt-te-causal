---
title: "IEA-15MW UMaine VolturnUS-S"
type: entity
created: 2026-05-12
updated: 2026-05-13
sources: []
tags: [platform, reference-model, floating, semisubmersible]
---

## What it is

Primary (locked) reference floating offshore wind turbine for this project.
The 15 MW IEA reference wind turbine sited on the UMaine VolturnUS-S
4-column semisubmersible platform, with three catenary chain mooring lines.

- Repo: `../../../repos/IEA-15-240-RWT/`
- OpenFAST input deck: `../../../repos/IEA-15-240-RWT/OpenFAST/IEA-15-240-RWT-UMaineSemi/`
- HAWC2 input deck: `../../../repos/IEA-15-240-RWT/HAWC2/IEA-15-240-RWT-UMaineSemi/`
- WT_Ontology YAML: `../../../repos/IEA-15-240-RWT/WT_Ontology/IEA-15-240-RWT_VolturnUS-S.yaml`

## Properties / parameters

| Property | Value |
|---|---|
| Rated power | 15 MW |
| Rotor diameter | 240 m |
| Hub height | 150 m |
| Platform type | 4-column semisubmersible (1 central + 3 outer) |
| Mooring | 3 chain catenary lines, 120° apart |
| Water depth | 200 m |
| Cut-in / rated / cut-out wind | 3 / 10.59 / 25 m/s |

## Substructure geometry (recovered from `WT_Ontology/IEA-15-240-RWT_VolturnUS-S.yaml`, 2026-05-13)

These are the **IEA-15 baselines for the 7 [[sources/jeon-2025]] design
variables** — the locked Phase 5 Sobol/MI sweep parameters.

| # | Variable | Symbol | Baseline (IEA-15) | Source line in YAML |
|---|----------|--------|-------------------|---------------------|
| 1 | Main column diameter | `D_MCol` | **10.0 m** | L748 `outer_diameter: [10.0, 10.0]` |
| 2 | Offset column diameter | `D_OCol` | **12.5 m** | L775 `outer_diameter: [12.5, 12.5]` |
| 3 | Offset column radius (spacing) | `R_MO` | **51.75 m** | L712 `location: [51.75, 180.0, -20.0]` |
| 4 | Pontoon diameter (equiv. circular) | `D_Pt` | **9.6148 m** | L877 — equates displacement to original rectangular [12.5, 7.0] |
| 5 | Pontoon height | `H_Pt` | **7.0 m** | L872 (commented original rect side_length_b) |
| 6 | Freeboard | `H_FB` | **15.0 m** | L709 `main_freeboard: z = +15.0` |
| 7 | Draft | `H_Draft` | **20.0 m** | L707 `main_keel: z = -20.0` |

**Note on D_Pt / H_Pt**: the original Allen 2020 design uses a rectangular
pontoon cross-section 12.5 m (width) × 7.0 m (height). The WT_Ontology
YAML and the WAMIT body in this OpenFAST deck use an equivalent circular
pontoon of diameter 9.6148 m (matched displacement). When sweeping `D_Pt`
in Sobol/MI we sweep the **equivalent circular diameter**, since that is
what OpenFAST/WAMIT actually sees.

## Mooring properties (recovered from `*_MoorDyn.dat`, 2026-05-13)

The Phase 5 sweep additionally includes mooring `EA` and unstretched
length as variables 8–9 (project additions on top of the
[[sources/jeon-2025]] geometry-only list):

| # | Variable | Symbol | Baseline (IEA-15) | Source |
|---|----------|--------|-------------------|--------|
| 8 | Mooring axial stiffness | `EA` | **3.27 × 10⁹ N** | LINE TYPES, line `main` |
| 9 | Mooring unstretched length | `L_u` | **850 m** | LINES, all 3 lines |

Other anchor-system context (not in the sweep but useful for templating):

| Quantity | Value |
|---|---|
| Line count | 3 |
| Line spread angles | 0°, 120°, 240° (col1 at 180°) |
| Chain diameter | 0.333 m |
| Chain linear mass | 685 kg/m |
| Fairlead radial position | 58.0 m (on a bracket 6.25 m beyond column centerline) |
| Fairlead depth | -14.0 m |
| Anchor radial position | 837.6 m |
| Anchor depth | -200 m |

## OpenFAST module activation

| Module | Active? | Notes |
|---|---|---|
| [[entities/openfast-aerodyn]]    | yes | BEM mode |
| [[entities/openfast-inflowwind]] | yes | TurbSim `.bts` |
| [[entities/openfast-elastodyn]]  | yes | All 6 platform DOFs enabled |
| [[entities/openfast-beamdyn]]    | yes | Used for blades |
| [[entities/openfast-hydrodyn]]   | yes | WAMIT potential flow (`HydroData/IEA-15-240-RWT-UMaineSemi.*`) — no strip-theory members in deck; **all platform geometry is baked into the WAMIT files**, so sweeping `D_MCol`/`D_OCol`/etc. requires re-running WAMIT (or a re-meshed body) per design point |
| [[entities/openfast-servodyn]]   | yes | [[entities/rosco]] DLL |
| [[entities/openfast-moordyn]]    | yes | 3-line catenary; `FairTen1/2/3` already in output list |
| [[entities/openfast-subdyn]]     | no  | Floating, not needed |

**Phase 2 templating — RAFT + OpenFAST hybrid pipeline (locked 2026-05-13)**.
Because the IEA-15 OpenFAST deck uses pure potential-flow (WAMIT) for
the platform, *geometric* sweeps (vars 1–7) cannot be done by editing
OpenFAST inputs alone. Decision: mirror the [[sources/jeon-2025]] split:

- **RAFT** ([[entities/raft]] *(stub)*) runs the 9-variable LHS / Saltelli
  ensemble. Frequency-domain coupled aero-hydro-servo-elastic; handles
  geometry changes via its built-in panel mesher; fast enough for a
  1000-point ensemble. Produces RAFT summary stats per channel → Sobol +
  KSG-MI ranking (Phase 5).
- **OpenFAST** validates the top-Sobol / top-MI winners (≤ ~20 designs +
  the predecessor's Case_03 equivalent), and supplies the time-series
  needed for Phase 4 TE (RAFT cannot do TE).

Full pipeline diagram in [[PLAN]] Phase 2 §"Hydro-evaluation pipeline".

## OpenFAST module activation

| Module | Active? | Notes |
|---|---|---|
| [[entities/openfast-aerodyn]]    | yes | BEM mode |
| [[entities/openfast-inflowwind]] | yes | TurbSim `.bts` |
| [[entities/openfast-elastodyn]]  | yes | All 6 platform DOFs enabled |
| [[entities/openfast-beamdyn]]    | yes | Used for blades |
| [[entities/openfast-hydrodyn]]   | yes | WAMIT + Morison |
| [[entities/openfast-servodyn]]   | yes | [[entities/rosco]] DLL |
| [[entities/openfast-moordyn]]    | yes | 3-line catenary |
| [[entities/openfast-subdyn]]     | no  | Floating, not needed |

## Sweepable parameters (Phase 5 — locked list)

The 9 variables are locked via [[sources/jeon-2025]] + project additions
— see the "Substructure geometry" and "Mooring properties" tables above
for IEA-15 baselines. Default LHS range is **±20 % per variable** unless
the predecessor's original bounds are recovered (see [[open-questions]]
Q2 — still open).

## Appears in

- [[overview]] — project context
- [[entities/openfast-overview]] — module map
- All validation cases ([[validation/case-1-r-test-parse]] through
  [[validation/case-4-sobol-3pt-mooring-ea]])

## Sources

- *(to ingest)* `allen-2020` — UMaine VolturnUS-S Definition of the
  UMaine Floating Offshore Wind System.
- *(to ingest)* `iea-task37-2020` — IEA Wind Task 37 reference wind turbine.
