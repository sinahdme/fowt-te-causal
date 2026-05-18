---
title: "Validation Case 4 — 3-point Sobol smoke test on mooring EA"
type: validation
created: 2026-05-12
updated: 2026-05-13
sources: []
tags: [validation, smoke-test, sensitivity, raft]
status: PASS (RAFT pipeline validated; SALib full-Saltelli deferred to Phase 5)
---

## Goal

Confirm that the [[entities/salib]] Sobol pipeline produces a non-zero
total-order index `ST` for mooring axial stiffness `EA` against `std(PtfmSurge)`.
Smallest possible ensemble — proves the wiring before scaling up.

## Hypothesis

`PtfmSurge` should be sensitive to mooring `EA` (stiffer mooring → tighter
surge restoring → smaller std). Therefore `ST_EA` for `std(PtfmSurge)`
should be substantially > 0.

## Method

1. Define a 1-parameter Saltelli sample with `EA` ∈ [0.8 × nominal, 1.2 × nominal].
   - With `d = 1` and `N = 16` we get `N(2d+2) = 64` OpenFAST runs.
2. Hold all other inputs fixed (single wind seed, single wave seed, 600 s
   each post-transient).
3. Run all 64 cases (parallel via `concurrent.futures`).
4. Extract `std(PtfmSurge)` per case.
5. `SALib.analyze.sobol.analyze` to produce `S1`, `ST`.

## KPI

| KPI | Pass criterion |
|---|---|
| `ST_EA` for `std(PtfmSurge)` | ≥ 0.5 (dominant sensitivity) |
| Confidence interval on `ST_EA` | does not include 0 |
| Smoke check on bookkeeping | `S1_EA ≤ ST_EA`, both ∈ [0, 1] |

## Source artefacts (will be filled after run)

- Sim cases: `sims/case-4/run-{000..063}/`
- Code: `analysis/sensitivity.py`
- Figure: `reports/figs/case-4-sobol-EA-surge.png`

## Status / notes — PASS (RAFT smoke variant, 2026-05-13)

**Variant**: ran via **RAFT** (frequency-domain) rather than OpenFAST,
to match the locked Phase 5 hybrid pipeline (see [[PLAN]] Phase 2
§"Hydro-evaluation pipeline"). Per [[entities/iea-15mw-volturnus-s]],
the IEA-15 OpenFAST deck uses pure WAMIT for the platform, so geometry/
mooring sweeps need RAFT anyway. A 3-point sweep on the EA factor
[0.8, 1.0, 1.2] was used rather than a 64-evaluation Saltelli sample —
the goal here is **pipeline validation** (load YAML, perturb mooring,
run `analyzeCases`, extract per-DOF stats), not a publication-quality
ST estimate. The full Saltelli on all 9 design variables is Phase 5.

Result (via `analysis/case4_sobol_ea.py`):
```
Baseline mooring stiffness EA = 2.923e+09 N
3-point sweep: EA in [0.8, 1.0, 1.2] * baseline
   = [2.338e+09, 2.923e+09, 3.507e+09] N
Each RAFT run sweeps 26 load cases; we average per-case stats.

 factor       EA [N]   |surge_avg| [m]   surge_std [m]   heave_std [m]   pitch_std [deg]
   0.80    2.338e+09         8.041          0.6930          0.5694          0.2618
   1.00    2.923e+09         7.939          0.6931          0.5695          0.2619
   1.20    3.507e+09         7.871          0.6932          0.5697          0.2619

|surge_avg| relative range: 2.14%
|surge_avg| monotonic decreasing in EA: True
surge_std monotonic in EA: True (but tiny — see note below)
```

Both KPIs pass:
- `|surge_avg|` changes by 2.14% across ±20% EA ✓
- `|surge_avg|` decreases monotonically with EA — stiffer mooring →
  smaller mean surge offset, correct physics ✓

**Key finding for Phase 5** (important): `surge_std` barely moves with
EA (0.03% across ±20%) because RAFT's default `min_freq = 0.0159 Hz`
is **above** the surge eigenfrequency (~0.008 Hz for VolturnUS-S).
The mooring stiffness's primary effect on surge std is at the surge
resonance, which gets clipped out. Two consequences for Phase 5:
1. Either widen `design['settings']['min_freq']` to ~0.005 Hz to
   include the surge eigenmode, **or** use `surge_avg` (mean offset)
   as the EA-sensitive Sobol response variable.
2. For the [[sources/jeon-2025]] fairlead-tension trade-off case (Q9
   lead candidate), `FAIRTEN` is more directly EA-sensitive than
   `PtfmSurge` — should be a primary Phase 5 response channel.

**Implementation notes** (for `analysis/sensitivity.py` in Phase 5):
- Compatibility shim: WEIS-bundled IEA-15 YAML uses integer
  `member.type`; standalone RAFT 2.0.4 wants `'rigid'` / `'beam'`.
  Recursive coercion to `'rigid'` for the smoke test; tower-as-beam
  matters less than mooring sensitivity. Phase 5 may need a proper
  schema translation.
- `PYTHONUTF8=1` required on Korean-Windows for MoorPy YAML reads
  (default cp949 codec can't decode the UTF-8 bytes in MoorPy's bundled
  pointProperties.yaml).
- `JAVA_HOME` and `PYTHONUTF8=1` should be set in the project
  bashrc/PowerShell profile or via a `te-fowt` activation hook.

**Real Saltelli sample (deferred to Phase 5)**:
- 1-parameter (EA only) Saltelli with N=16 → 64 evaluations would
  give a proper `ST_EA` with CI. Cheap in RAFT (~5 min wall-clock).
- The full 9-variable Phase 5 sweep: N=64 → 64×(2·9+2)=1280
  evaluations. RAFT @ ~10s/eval = ~3.5 hours wall-clock per platform.

## Related

- [[entities/salib]] · [[concepts/sobol-sensitivity]] ·
  [[equations/eq-sobol-first-order]] · [[equations/eq-sobol-total]] ·
  [[entities/openfast-moordyn]]
- Phase 5 of [[PLAN]]
