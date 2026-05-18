---
title: "RAFT — Response Amplitudes of Floating Turbines"
type: entity
created: 2026-05-13
updated: 2026-05-13
sources: []
tags: [software, frequency-domain, surrogate, floating, hydrodynamics, phase-5-tool]
---

## What it is

**RAFT** (*Response Amplitudes of Floating Turbines*) is NREL's
frequency-domain coupled aero-hydro-servo-elastic model for floating
wind turbines. Distributed as part of [[entities/weis]].

In this project RAFT is the **Phase 5 LHS / Saltelli ensemble engine**
for the 9 substructure design variables. Chosen because:
- The IEA-15 OpenFAST deck uses pure potential-flow (WAMIT) for the
  platform — geometric sweeps cannot be done by editing OpenFAST inputs
  alone, see [[entities/iea-15mw-volturnus-s]] §"OpenFAST module activation".
- RAFT builds the hydrodynamic body from a parametric panel mesh, so
  it handles changes in column diameters, pontoon dimensions, spacing,
  draft, freeboard directly from the design-variable values.
- Fast enough for a 1000-point Saltelli sample (predecessor used it
  exactly this way — see [[sources/jeon-2025]] §"RL setup").

## Where it lives

- Installed via WEIS: `repos/WEIS/` (already cloned in Phase 1).
- WEIS bundles RAFT as `weis.raft` (Python package) and exposes it
  through the same input-deck schema as OpenFAST, so the design variables
  for the 22 MW (predecessor) and 15 MW (this project) cases plug into
  the same RAFT input template.

## What it computes

Frequency-domain coupled solution for:
- Platform RAOs (heave, surge, pitch, sway, roll, yaw) given a JONSWAP /
  PM / user-defined wave spectrum.
- Turbine thrust + aerodynamic damping at the rotor.
- Mooring catenary linearised about the operating point.
- Statistics: per-channel `std`, peak (max), and PSD — suitable for our
  Phase 5 summary stats (`max`, `std`, `mean`, DEL approximation).

What it does **not** compute (and therefore the reason OpenFAST stays in
the pipeline):
- Time-series outputs — so no TE can be done on RAFT outputs.
- True nonlinear blade dynamics or 2nd-order wave forces.
- Strict damage-equivalent loads (only approximations from PSD + Dirlik /
  Rainflow on the inverse FFT). For the final fatigue numbers we re-run
  the top winners through OpenFAST.

## Project workflow

```
LHS / Saltelli (SALib) on 9 design vars  →  RAFT  →  per-channel stats
                                                           │
                                                           ▼
                                            Sobol-S1/ST + KSG-MI ranking
                                                           │
                                                           ▼
                                      pick top winners + Case_03 equivalent
                                                           │
                                                           ▼
                                          OpenFAST (DLC matrix) — Phase 4 TE
```

See [[PLAN]] Phase 2 §"Hydro-evaluation pipeline" for the full diagram.

## Sweepable inputs (from this project's perspective)

The 9 variables locked in Phase 5 map onto RAFT inputs as:

| # | Variable | RAFT input field |
|---|----------|------------------|
| 1 | `D_MCol` | `members[main_column].d` |
| 2 | `D_OCol` | `members[col1..3].d` |
| 3 | `R_MO` | `members[col1..3].rA / rB` (offset from origin) |
| 4 | `D_Pt` | `members[pontoon_lower_*].d` |
| 5 | `H_Pt` | pontoon member length / radial extent |
| 6 | `H_FB` | `members[main_column].rB[2]` (top z) |
| 7 | `H_Draft` | `members[main_column].rA[2]` (keel z) |
| 8 | `EA` | `mooring.lines[*].type.EA` |
| 9 | `L_u` | `mooring.lines[*].length` |

*(field names approximate — to be confirmed against the `repos/WEIS/`
RAFT input schema during Phase 2 templating.)*

## Phase 2 driver

`sims/run_raft_lhs.py` — Saltelli sample over the 9-variable ±20 % box,
template a RAFT YAML per design point, run `weis.raft.run()`, collect
`{max, std, mean}` per response channel into a Parquet at
`data/raft_ensemble.parquet`. Constraint-violating samples
(`D_OCol < D_Pt`, etc.) tagged `infeasible=True` and excluded from
Sobol/MI but reported as a fraction.

## Appears in

- [[PLAN]] Phase 2, Phase 5 — hydro-evaluation pipeline
- [[sources/jeon-2025]] — predecessor's RL inner-loop solver, same role
  here
- [[entities/iea-15mw-volturnus-s]] — why RAFT is necessary (WAMIT
  baked-in platform geometry)
- [[entities/weis]] — install host

## Sources

- *(to ingest)* RAFT GitHub README: https://github.com/WISDEM/RAFT
- *(to ingest)* WEIS documentation: https://wisdem.github.io/WEIS/
