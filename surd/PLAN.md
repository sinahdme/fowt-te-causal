---
title: "SURD subproject — plan"
type: plan
created: 2026-06-29
status: approved
tags: [surd, causality, controller-firewall, phase-7]
---

# SURD subproject — plan

A new analysis track (`surd/`) inside the FOWT TE project. It applies the SURD
causal decomposition to the **same `.outb` data** the TE pipeline uses, to turn
the H1 "controller firewall" null into a *measured* result and to re-answer the
TE hypotheses with a cleaner decomposition. It **complements**, not replaces, the
TE pipeline.

## Context

The Phase-4 TE campaign found `TE(Wind1VelX → PtfmPitch) ≈ 0` across all DLCs
(H1 null). The leading explanation is the **controller firewall**: ROSCO senses
wind and adjusts blade pitch / generator torque to reject the thrust disturbance
*before* it reaches the platform, so wind's influence on pitch disappears into an
intermediary (the controller) the TE channel set never observes. Bivariate and
conditional TE cannot resolve this — they conflate unique vs. synergistic
causality and give no measure of how much of a response is driven by *unobserved*
variables.

**SURD** (Martínez-Sánchez, Arranz & Lozano-Durán, *Nat. Commun.* 15, 9296,
2024; DOI [10.1038/s41467-024-53373-4](https://doi.org/10.1038/s41467-024-53373-4))
decomposes causality into **Redundant / Unique / Synergistic** components **plus a
causality leak** that quantifies unobserved drivers, and handles mediator /
confounder / collider structures explicitly.

- Code: <https://github.com/Computational-Turbulence-Group/SURD>
- Data: Zenodo [10.5281/zenodo.13750918](https://doi.org/10.5281/zenodo.13750918)
- Foundational TE formulation: Lozano-Durán & Arranz, *Phys. Rev. Research* 4,
  023195 (2022).

## Scope and intent

- Subproject **inside the existing repo**, in `surd/` alongside `analysis/`.
  Reuses the same `.outb` loader, same 54 cases, same preprocessing, same channel
  conventions → SURD and TE run on **identical inputs** for a fair head-to-head.
- Primary target: **observe the controller firewall** rather than infer around
  it — add the controller/drivetrain channels (already exported) to the variable
  set and let SURD decompose the mediator chain.
- Out of scope (for now): OpenFAST re-runs. The controller-off (Q11)
  interventional run is a *confirmatory backstop*, not part of this plan.

## The core idea — observe the firewall

The firewall exists only because the controller is unobserved. Physical chain:

```
Wind → BldPitch             (controller senses wind, commands blade pitch)
Wind, BldPitch → RotThrust  (net rotor thrust after control action)
RotThrust → PtfmPitch       (thrust × hub height = platform pitching moment)
```

All required channels confirmed present in `dlca_v08ms_s00.outb` (930 channels):
`Wind1VelX`, `Wave1Elev`, `BldPitch1/2/3`, `RotThrust`, `RotTorq`, `GenTq`,
`GenPwr`, `GenSpeed`, `RotSpeed`, all 6 `Ptfm*` DOF, `FAIRTEN1/2/3`, `RootMxc1`,
`TwrBsMyt`.

**Headline metric — the leak drop.** Compare `leak(PtfmPitch)` with only
`{Wind, Wave}` observed vs. with `{Wind, Wave, BldPitch1, RotThrust}` added. A
collapse in the leak *is* the controller's mediating contribution — a direct
observational test of H1's mechanism #1 with **no new OpenFAST runs**.

**Honest caveat (state in any write-up).** A disturbance-rejection controller
produces near-perfect cancellation, so the *net* wind→pitch information genuinely
is small. SURD will not conjure causality that isn't in the net signal; it
**relocates** wind's information into the controller channels (unique causality
wind→BldPitch/RotThrust; redundant/synergistic wind+RotThrust→pitch). Framed as
**total effect** (controller unobserved, ≈ 0 — the firewall) vs.
**decomposed/direct effect** (controller observed — where it went). The report
asks both questions explicitly.

## Phases

### Phase 0 — validation gate (correctness insurance)
- Vendor the SURD reference implementation under `surd/vendor/` (or pip/submodule
  per its packaging). Confirm the transport-map dependency stack installs on this
  box.
- Reproduce **one synthetic case from the paper** with a known answer (the
  mediator system Q3→Q2→Q1, Fig. 2) and confirm our wiring returns the expected
  R/U/S signature and leak. Gates trust before touching FOWT data.

### Phase 1 — thin vertical slice
- Group: **`{Wind1VelX, Wave1Elev, BldPitch1, RotThrust, PtfmPitch}`**, target
  `PtfmPitch`, on **one** `.outb` case.
- Preprocessing **identical to TE** (drop 600 s transient, decimate to 5 Hz, tiny
  jitter) — reuse `analysis/load_runs.py` and mirror
  `te_pipeline.preprocess_channel` so inputs match the TE table exactly.
- Compute SURD R/U/S + leak for the full group and the reduced
  `{Wind, Wave, PtfmPitch}` group; report the **leak drop**.
- **Decision point:** if the leak story holds → Phase 2; if not → stop (a day
  spent, not a campaign).

### Phase 2 — scale (width TBD, see Open decisions)
- Run SURD across all 54 cases → `reports/surd_table.parquet`, long-form schema
  mirroring `te_table.parquet` (one row per case × group × target × component) so
  SURD vs. TE is a direct join.
- Comparison figures/notes: TE(wind→pitch)≈0 alongside SURD's leak-drop /
  relocated-causality decomposition.

## Structure

```
surd/
  PLAN.md                  # this file
  vendor/                  # SURD reference code (gitignored if large)
  surd_runner.py           # load .outb → preprocess (TE-parity) → SURD decompose
  groups.py                # named variable groups (pitch/firewall, fairlead, ...)
  validate_synthetic.py    # Phase 0 gate: paper's mediator case
  compare_te.py            # join surd_table.parquet vs te_table.parquet
reports/surd_table.parquet # Phase 2 output (gitignored like other parquets)
```

Reuse, don't duplicate: `analysis/load_runs.py` (`load_outb`,
`find_time_column`) and the TE preprocessing constants.

## Open decisions (do not block Phases 0–1)

- **Phase 2 width** — (a) *firewall-focused*: just the pitch/thrust story (sharpest
  single result); or (b) *full sweep*: add fairlead-tension groups
  (`{Wind, Wave, RotThrust, FAIRTEN1/2/3}` for H5b) and heave, re-answering
  H1/H3/H5b head-to-head with TE. **Recommend start (a)**; schema + runner make
  (b) an extension, not a rewrite.
- Add `GenTq`/`RotSpeed` to the pitch group, or keep it minimal at 5 vars —
  decide empirically in Phase 1 (cost grows as 2^N; keep groups ≤ ~5–6 vars).

## Risks / considerations

- **Combinatorics**: SURD decomposes over all subsets (2^N). Keep groups small —
  per-target small-group analysis, not a 972-row sweep.
- **New toolchain**: transport-map density estimation, different stack than
  IDTxl. Confirm install in Phase 0; production scale-out may move to the server
  like the TE campaign.
- **Stationarity**: same assumption (and slow-drift caveat) as the TE pipeline;
  carry over unchanged.
- **ΔT choice**: SURD picks the prediction horizon as the time of maximum unique
  causality; document the chosen ΔT per group.
- **Provenance**: write `surd_table.parquet` to the gitignored `reports/` path;
  never overwrite `te_table.parquet`.

## Verification

- **Phase 0**: synthetic mediator case reproduces the paper's R/U/S + leak
  signature (qualitative match to Fig. 2) → wiring correct.
- **Phase 1**: `leak(PtfmPitch | {Wind,Wave})` is high and drops materially when
  `{BldPitch1, RotThrust}` are added; wind shows nonzero unique causality to
  `RotThrust`/`BldPitch`. Numbers sane (R/U/S ≥ 0, normalized sum to 1; leak ∈
  [0,1]).
- **Phase 2**: `surd_table.parquet` has 54 distinct cases, joins cleanly to
  `te_table.parquet`, reproduces the H1 null, and adds the leak-drop
  decomposition.

## Out of scope / explicitly not doing

- No OpenFAST re-runs (controller-off Q11 is a later, separate confirmatory step).
- No changes to the TE pipeline or `te_table.parquet`.
- Not reimplementing SURD's estimator — vendor and call the reference code.
