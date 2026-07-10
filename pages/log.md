---
title: "Log"
type: log
created: 2026-05-12
updated: 2026-07-10
tags: [meta, log, publication]
---

# Log

Append-only chronological record. New entries at the **bottom**.
Conventions:
- `## [YYYY-MM-DD] ingest | <Title>` — adding a raw source
- `## [YYYY-MM-DD] query | <Topic>` — substantive question answered
- `## [YYYY-MM-DD] lint | <Scope>` — health-check pass
- `## [YYYY-MM-DD] structure | <Change>` — wiki structural change

---

## [2026-05-12] structure | Vault bootstrap

- Created Phase 1 scaffolding per [[PLAN]]:
  - Top-level dirs `repos/`, `vault/` (deprecated), `sims/`, `data/`,
    `analysis/`, `reports/`.
  - Shallow-cloned 7 OpenFAST-ecosystem repos into `repos/` (~1.6 GB).
- Seeded original `vault/` with 17 markdown notes (Modules, Models, Theory,
  Channels, TE-Analysis stubs).
- Wrote `requirements.txt` and copied plan to `PLAN.md`.

## [2026-05-12] structure | Migrated vault/ → wiki/ per LLM_Wiki_Pattern.md

- Reorganised into three-layer split: `wiki/raw/`, `wiki/pages/`, `wiki/SCHEMA.md`.
- Renamed notes to kebab-case, added YAML frontmatter to every page.
- Split theory notes into `pages/concepts/` (idea) +
  `pages/equations/eq-*.md` (formula).
- Moved OpenFAST modules to `pages/entities/openfast-*.md`.
- Added software entity pages for tooling (idtxl, salib, etc.).
- Added 4 validation-case stubs from [[PLAN]] §Verification.
- Created `index.md`, `overview.md`, `open-questions.md`,
  `wiki-improvement-plan.md`.
- Old `vault/` renamed to `vault-legacy/` (reversible) after verification.
- Updated [[PLAN]] directory layout section + project_layout memory.

## [2026-05-12] structure | Added publication-strategy section to PLAN

- Added §"Publication strategy" to [[PLAN]] covering target venues
  (workshop → WES / Marine Structures), strengthening moves (baselines,
  hypothesis predictions, design takeaway, reproducibility, multi-platform
  stretch).
- Phase 4 expanded with **mandatory baseline comparisons** table
  (coherence + bivariate/conditional Granger) — `analysis/baselines.py`
  added to critical-files list.
- Phase 6 expanded to require a **concrete engineering takeaway** that
  changes a design decision vs Sobol-only.
- Added Q7 (target venue), Q8 (pre-registered hypothesis predictions
  H1–H6), Q9 (design-decision case study) to [[open-questions]].
- Added `publication_strategy` memory; mirrored PLAN.md back to
  `.claude/plans/`.

## [2026-05-12] structure | User opened vault and moved PLAN + pattern inside

- User renamed `wiki/` → `wiki-transfer entropy/` and pointed Obsidian at it.
- User moved `PLAN.md` and `LLM_Wiki_Pattern.md` into the vault root alongside
  `SCHEMA.md` (the clean single-vault setup).
- Obsidian `.obsidian/` config created on first open; `Welcome.md` placed at
  vault root (Obsidian default — kept for now).
- Agent re-checked relative paths: 9 references had `../` counts that no
  longer matched the new vault root depth. Fixed across `SCHEMA.md`,
  `raw/README.md`, `log.md`, `open-questions.md`,
  `concepts/conditional-transfer-entropy.md`, `entities/openfast-hydrodyn.md`.

## [2026-05-12] structure | IEA-22-280-RWT considered and dropped (Option 3)

- User dropped the full IEA-22-280-RWT repo (475 files, 26.5 MB) into
  `raw/extracts/` mid-session.
- Agent assessed: wrong folder per SCHEMA (`raw/extracts/` is for converted
  text, not model repos) and flagged the deeper question of whether to switch
  reference platform from IEA-15MW VolturnUS-S to IEA-22-Semi.
- Recommendation: **Option 3** — keep IEA-15 as the locked reference for
  publication-comparability reasons (more validation, OC6 model-test data,
  hundreds of citing papers). IEA-22 is a strong candidate if Q5 reopens.
- User deleted the IEA-22 repo from `raw/extracts/`. Q5 in [[open-questions]]
  updated to note IEA-22 is the natural multi-platform candidate when Q5
  reopens — can be re-fetched via `git clone …/IEA-22-280-RWT`.

## [2026-05-12] structure | Alignment pass

- Cleanup: deleted stray empty `Transfer Entropy/` folder at vault root
  (Obsidian artifact), `Welcome.md` (Obsidian default greeter), 7 `.clonelog`
  files in `repos/` (leftover from the initial parallel-clone job).
- Wikilink sweep: converted in-prose references from
  `` `../PLAN.md` `` / `` `../../PLAN.md` `` / `` `../LLM_Wiki_Pattern.md` ``
  / `` `../SCHEMA.md` `` etc. into `[[PLAN]]`, `[[LLM_Wiki_Pattern]]`,
  `[[SCHEMA]]` wikilinks. Aligns with SCHEMA convention "always use
  folder-prefixed wikilinks". 22 files touched, ~23 sites changed. Code-block
  and structural-table paths kept as paths.
- Updated [[wiki-improvement-plan]] status snapshot with current 48-page count.
- Q5 status changed from 🟢 to ⚪ (deferred — properly marked now).

## [2026-05-12] ingest | Schreiber 2000 + Kraskov 2004 + Wollstadt 2019 (Tier 1 batch)

- Sources placed:
  - `raw/papers/0001042v1.pdf` — Schreiber 2000 (arXiv preprint, 4 pages)
  - `raw/papers/0305641v1.pdf` — Kraskov, Stögbauer, Grassberger 2004 (PRE preprint)
  - `raw/papers/Wollstadt-2019-IDTxl.md` + `.bib` — JOSS paper, copied from
    `repos/IDTxl/IDTxl-master/paper/paper.md`
- Source pages created (citation, TL;DR, key claims, how-it-informs):
  - [[sources/schreiber-2000]]
  - [[sources/kraskov-2004]]
  - [[sources/wollstadt-2019]]
- Deep-paper companions (derivation re-check, comparison to alternatives,
  project implications):
  - [[papers/schreiber-2000]]
  - [[papers/kraskov-2004]]
  - [[papers/wollstadt-2019]]
- Concept / equation pages updated with **verified-from-source quotes**
  (replacing earlier from-memory paraphrases):
  - [[concepts/transfer-entropy]] — Schreiber's verbatim quotes on
    non-symmetry, common-driver conditioning
  - [[concepts/ksg-estimator]] — Kraskov's `k=2..4` recommendation and
    the critical 10⁻¹⁰ jitter note for empirical data
  - [[concepts/mutual-information]] — kraskov-2004 Eq. 1 form with
    reparametrisation-invariance note
  - [[concepts/conditional-transfer-entropy]] — Schreiber's "common driving
    force Z" quote; IDTxl multivariate vs single-conditioner forms
  - [[concepts/surrogate-significance]] — added theoretical justification:
    KSG is exact-for-independence (kraskov-2004 Sec. III), so the
    surrogate shift = signal, not bias
  - [[equations/eq-transfer-entropy]] — Schreiber's verbatim Eq. 4 with
    original notation alongside modern form
  - [[equations/eq-mutual-information]] — kraskov-2004 Eq. 1 with units
    note ("we always will use natural logarithms")
  - [[entities/idtxl]] — added analyser map, fixed estimator settings
    table, surfaced the Granger-via-`JidtGaussianCMI` finding
- [[index]] sources/ and papers/ sections now populated with the 6 new pages.
- **Three implementation surprises** flagged in [[papers/wollstadt-2019]]
  that update Phase 4 of [[PLAN]]:
  1. Granger baseline is free — same library, swap `cmi_estimator`. No
     separate `statsmodels` dependency.
  2. AIS as effect-size denominator (`TE / (H(Y) − AIS(Y))`) instead of
     `TE / H(Y)` — more meaningful "fraction of externally-driven
     predictability".
  3. PID for follow-up paper — answers redundant vs synergistic
     wind+wave contributions.
- No contradictions found between the three sources or with our prior
  pages. Project understanding is consistent with primary sources.

## [2026-05-12] structure | PLAN.md Phase 4 updated per Tier-1 ingest

Three changes propagated from [[papers/wollstadt-2019]] into [[PLAN]] Phase 4:

1. **Granger baseline consolidated** into `analysis/te_pipeline.py` via
   `cmi_estimator='JidtGaussianCMI'` swap on `MultivariateTE`. Drops the
   separate `statsmodels.tsa.stattools.grangercausalitytests` call.
   `analysis/baselines.py` shrinks to a thin coherence wrapper around
   `scipy.signal.coherence`.
2. **Effect-size denominator changed** from `TE / H(Y)` to
   `TE / (H(Y) − AIS(Y))` — "fraction of externally-driven predictability."
   AIS comes from IDTxl's `ActiveInformationStorage` analyser using the
   same `k_target` embedding selected for TE.
3. **Methodology references grounded** — Phase 4 prose now cites
   [[sources/schreiber-2000]], [[sources/kraskov-2004]],
   [[sources/wollstadt-2019]] inline where decisions are anchored
   (jitter, `k=4`, IAAFT surrogates, family-wise correction).

`analysis/te_pipeline.py` block-diagram added to PLAN critical-files
section. Mirrored to `.claude/plans/`. Memory updated:
[[tooling-stack]] revised; new [[tier1-sources]] reference memory written.

## [2026-05-13] ingest | Jeon 2025 (KSME) — RL optimisation predecessor work

- Source: `raw/papers/reference_papers/대한기계학회_강화학습기반부유식해상풍력하부구조물설계변수최적화_전해명.pptx`
  (15 slides; PPTX text was image-only, slides rendered via PowerPoint COM
  automation to `%TEMP%/pptx_render/Slide*.JPG` and read visually).
- New page: [[sources/jeon-2025]] — captures 7 design variables, 9 response
  channels, 3 constraint groups (geometric / dynamic / resonance),
  validation DLC (DLC 1.6, NTM 11 m/s, SSS Hₛ=8.3 Tₚ=12.95, 6 seeds),
  and the Case_03 trade-off table (mass −21.5 %, FAIRTEN +19/+59/+57 %).
- **Decisions cascaded**:
  - Q1 closed (🔵): 9 response channels locked = `RootMyc1`, `RootMxc1`,
    `TwrBsMyt`, `PtfmHeave/Surge/Pitch`, `FAIRTEN1/2/3`.
  - Q2 partially closed (🟡): 7 substructure-geometry variables locked;
    project adds mooring `EA` and unstretched length as variables 8–9 so
    causal graph can answer the Case_03 fairlead-tension trade-off (Q9
    lead candidate). LHS ranges and IEA-15 baselines still open.
  - Q3 partially closed (🟡): `max` (predecessor) + `std`, DEL, `mean`
    (project additions for fatigue-relevant TE/MI).
  - Q5 partially closed (🟡): IEA-15MW VolturnUS-S = primary (locked);
    IEA-22MW-RWT-Semi = second platform for multi-platform comparison
    (locked — direct continuity with predecessor work).
  - Q9 lead candidate set: explain the Case_03 trade-off via conditional
    TE(wave / wind → FAIRTEN) + Sobol-`ST` on (geometry, mooring).
- **PLAN.md updated**: Phase 2 §"Response channels" added, Phase 5
  §"Parameter sweep list" added (9 variables), Phase 6 §engineering
  takeaway pointed at the Case_03 trade-off, §"Execution order on plan
  approval" updated to reflect closed gates.
- **[[index]]**: added [[sources/jeon-2025]], added IEA-22-280-RWT-Semi
  to reference platforms.
- Memory updates: `project_goal`, `phase5_param_method`, new
  `jeon-2025-predecessor` project memory.

## [2026-05-13] structure | IEA-15 baselines recovered for the 9 sweep variables

Extracted from the cloned IEA-15-240-RWT repo without user input:

- **Substructure geometry (vars 1–7)** from
  `repos/IEA-15-240-RWT/WT_Ontology/IEA-15-240-RWT_VolturnUS-S.yaml`:
  D_MCol=10.0 m, D_OCol=12.5 m, R_MO=51.75 m, D_Pt=9.6148 m (equiv.
  circular; rect 12.5 × 7.0 in original Allen 2020), H_Pt=7.0 m,
  H_FB=15.0 m, H_Draft=20.0 m.
- **Mooring (vars 8–9)** from `*_MoorDyn.dat`: EA=3.27e9 N, L_u=850 m.
- **WAMIT vs strip-theory caveat** flagged: the IEA-15 OpenFAST deck
  uses pure potential-flow (PotMod=1, NJoints=0, NMembers=0). All
  platform geometry is baked into the WAMIT `HydroData/*.hst/.1/.3`
  files — geometric sweeps (vars 1–7) require either RAFT (predecessor's
  approach), a HydroDyn member-mode switch (PotMod=0 + strip theory),
  or restricting OpenFAST runs to mooring-only sweeps.
- [[entities/iea-15mw-volturnus-s]] rewritten with the locked geometry +
  mooring tables, anchor system context (fairlead r=58 m z=-14 m,
  anchor r=837.6 m z=-200 m), and the templating-decision options.
- [[PLAN]] Phase 5 §"Parameter sweep list" — Baseline (IEA-15) column
  filled in. Q2 in [[open-questions]] downgraded from "parameter names
  locked; baselines open" to "parameter names + baselines locked; ranges
  + hydro-method open".
- PLAN.md mirrored to `.claude/plans/`.

## [2026-05-13] structure | Phase 2/5 fully unblocked — final two gates closed

User locked the last two decisions:
- **Hydro-evaluation method**: RAFT + OpenFAST hybrid. RAFT runs the
  9-variable Saltelli ensemble; OpenFAST validates top winners and
  supplies Phase 4 TE time-series. Direct mirror of [[sources/jeon-2025]]'s
  RAFT→OpenFAST split.
- **LHS ranges**: ±20 % per variable around IEA-15 baseline. Concrete
  bounds table now in [[PLAN]] Phase 5.

Cascaded changes:
- [[PLAN]] Phase 2 §"Hydro-evaluation pipeline" added with ASCII
  pipeline diagram; DLC matrix expanded with Predecessor-DLC1.6 row
  for [[sources/jeon-2025]] cross-comparability; old "Open inputs
  from you" placeholder removed.
- [[PLAN]] Phase 5 §"LHS / Saltelli sample range" added with per-variable
  −20 % / baseline / +20 % table and constraint-handling policy
  (mark `D_OCol < D_Pt` etc. as infeasible, mirror predecessor's
  reward=−100, Sobol/MI on feasible subset only).
- Q2 in [[open-questions]] downgraded from 🟡 to 🔵 (resolved).
- New [[entities/raft]] entity page created — covers the RAFT inputs
  the 9 design vars map to and the Phase 2 driver `sims/run_raft_lhs.py`.
- [[entities/iea-15mw-volturnus-s]] §"Phase 2 templating note" rewritten
  to lock the hybrid pipeline (was 3-option decision).
- [[index]] updated with the RAFT entity.
- PLAN.md mirrored to `.claude/plans/`.
- Memory updates: `phase5_param_method` (ranges + hybrid pipeline),
  `tooling_stack` (RAFT added).

## [2026-05-13] structure | Toolchain installed + validation cases 1 & 2 PASS

Parallel work across three tracks. All pass.

### Track 1 — Pandoc (157 OpenFAST RST → MD)
- `analysis/build_vault.py` walks `repos/openfast/docs/source/**/*.rst`
  via 8-worker ThreadPoolExecutor, writes GFM markdown under
  `wiki-transfer entropy/raw/extracts/openfast-docs/`. 157/157 succeeded.

### Track 2 — Toolchain
- **Discovered**: `openfast_env` (miniconda3) already has OpenFAST 4.2.0
  binary at `C:\Users\kunsanuni3\miniconda3\envs\openfast_env\Library\bin\openfast.exe`.
  Won't reinstall — call from te-fowt env via full path.
- **Discovered**: `raft-env` (anaconda3) at Python 3.14 — too new for
  IDTxl. Kept separate.
- **Created `te-fowt` conda env** (Python 3.11.15 + OpenJDK 11.0.30 +
  numpy/scipy/pandas/pyarrow/networkx/matplotlib/statsmodels/SALib/jpype1/h5py
  from conda-forge).
- **IDTxl install pattern**: upstream `setup.py` requires a C compiler
  for the HDE Cython extension which we don't use. Bypassed with a
  `.pth` file in te-fowt's site-packages pointing at the local
  `repos/IDTxl/IDTxl-master/` clone. Verified import, JIDT JAR present,
  JVM starts (Java 11.0.30 reported).
- **openfast-toolbox**: not on PyPI; `pip install -e repos/openfast_toolbox`
  works. Version 3.5.1 installed.
- **setuptools<81 pinned** because IDTxl uses `pkg_resources` which was
  removed in setuptools 81+.

### Track 3 — Validation cases
- **Case 1 (r-test parse) PASS**: `analysis/load_runs.py` parses the
  pre-computed `5MW_Land_BD_DLL_WTurb.outb` shipped with r-test — 2001
  rows × 67 channels, dt=0.01 s uniform, Parquet round-trip exact (max
  abs diff = 0). Patched two openfast_toolbox / NumPy-2 issues:
  `use_buffer=True` to bypass the broadcast bug at line 617 of
  `fast_output_file.py`, and a `find_time_column` helper to handle the
  `Time_[s]` column-name convention.
- **Case 2 (AR(1) TE recovery) PASS**: `analysis/test_ar1_te.py` runs
  IDTxl BivariateTE + KSG on a coupled AR(1) chain. Forward
  `TE(X→Y) = 0.1892` nats, p = 0.005 (significant ✓). Reverse
  `TE(Y→X) = 0` nats, p = 1.0 (no parents selected, as expected ✓).
  Fixed an `np.math.factorial` IDTxl bug by setting `permute_in_time=True`
  in the settings dict — also the correct choice for single-replication
  time series.
- Both case pages updated: status → PASS with execution logs and
  implementation notes for Phase 3 / Phase 4 to inherit.

Outputs:
- `data/case-1-5MW_Land_BD_DLL_WTurb.parquet`
- 157 markdown files under `wiki-transfer entropy/raw/extracts/openfast-docs/`
- Three analysis scripts: `analysis/build_vault.py`,
  `analysis/load_runs.py`, `analysis/test_ar1_te.py`.

**Remaining toolchain item**: WEIS / RAFT (`pip install -e repos/WEIS`)
deferred — not needed for cases 1–2, will install just before Phase 5
RAFT-driver work.

## [2026-05-13] structure | Phase 1 close-out — Q8 locked, cases 3+4 PASS, WEIS/RAFT installed

Final three independent tracks complete; all validation gates closed.

### Q8 — Pre-registered hypotheses locked (🔵)
Six predictions H1–H6 written into [[open-questions]] §Q8 with explicit
numeric pass criteria. Original H5 (controller gains) replaced — the
locked Phase 5 sweep doesn't include controller gains, so H5 is now
re-targeted at the [[sources/jeon-2025]] Case_03 fairlead-tension
trade-off (matches Q9 lead candidate). H4 expanded to include mooring
`L_u` and bound the geometry-variable contribution. **No edits after
campaign launches** — this is the publication's pre-registration record.

### WEIS / RAFT install (task #4) — done
`pip install -e repos/WEIS` succeeded; pulled rosco, moorpy, wisdem,
RAFT, openfast_io, openmdao, etc. Note: top-level `import weis` fails
because `pyOpenFAST` isn't installed, but `import raft` works
standalone — and RAFT is what we actually need for Phase 5.
Documented in [[entities/raft]].

### Case 3 — `TE(Wind1VelX → PtfmPitch)` on real floating-platform output (🟢 PASS)
Used pre-computed `5MW_ITIBarge_DLL_WTurb_WavesIrr.outb` from r-test
as IEA-15 stand-in (same channel structure, turbulent wind + irregular
JONSWAP waves; avoids a >10-minute OpenFAST run for a smoke test).
Result: `TE(wind→pitch) = 0.0175 nats, p=0.005` (significant) ✓;
`TE(pitch→wind) = 0` (no parents selected, expected) ✓. Both KPIs
pass. Real IEA-15 single-case run is the first Phase 2 launch anyway.
Script: `analysis/case3_floating_te.py`.

### Case 4 — 3-point RAFT mooring-EA sweep (🟢 PASS)
Loaded `IEA-15-240-RWT_VolturnUS-S_raft.yaml` (from WEIS examples),
perturbed `mooring.line_types[main].stiffness` by ×0.8, ×1.0, ×1.2,
ran RAFT `analyzeCases` over the YAML's 26 load cases per design,
extracted per-DOF stats. `|surge_avg|` decreases monotonically with
EA (8.041 → 7.939 → 7.871 m; 2.14% range) — correct physics ✓.
`surge_std` barely moves because RAFT default `min_freq=0.0159 Hz` is
above the surge eigenfrequency (~0.008 Hz); Phase 5 should widen the
freq range or use `surge_avg`/`FAIRTEN` as EA-sensitive responses.

**Three Windows/version gotchas captured for Phase 5**:
1. WEIS-bundled IEA-15 YAML uses integer `member.type`; standalone
   RAFT 2.0.4 wants `'rigid'`/`'beam'` — added recursive coercion shim
   in `analysis/case4_sobol_ea.py`.
2. MoorPy reads its bundled UTF-8 YAML via default `open()`, which
   uses cp949 on Korean Windows. Workaround: `PYTHONUTF8=1`.
3. `JAVA_HOME` needs to be set when invoking the env python directly
   (not via `conda run`). Documented in the case-3 page.

Script: `analysis/case4_sobol_ea.py`.

### Project status snapshot

All four validation cases now PASS:
- Case 1 — r-test parse (openfast_toolbox) ✓
- Case 2 — AR(1) TE recovery (IDTxl + KSG + JIDT) ✓
- Case 3 — real floating-platform end-to-end TE ✓
- Case 4 — RAFT mooring sweep (Phase 5 pipeline validated) ✓

Pre-registered hypotheses (Q8) locked. All Q1–Q9 in
[[open-questions]] are either 🔵 resolved or 🟡 partially-resolved
with execution deferred to natural-phase points. Phase 1 close-out
achieved; Phase 2 sim campaign is now unblocked.

## [2026-05-15] query | Real IEA-15 case-3 TE — H1 first-cut PASS

Re-ran `analysis/case3_floating_te.py` on the actual
`IEA-15-240-RWT-UMaineSemi.outb` (300 s, NTM 11 m/s, JONSWAP), replacing
the prior 5MW_ITIBarge stand-in. Tuned settings: decimate to 5 Hz,
`max_lag=30` (= 6 s history window), 200 surrogates, KSG `k=4`,
`permute_in_time=True`. Pipeline: drop first 60 s transient → 1201
samples at 5 Hz.

**Result**:
- Forward `TE(Wind1VelX → PtfmPitch) = +0.0052 nats, p = 0.0050` ✓
- Reverse `TE(PtfmPitch → Wind1VelX) = 0`, no parents selected ✓

Both KPIs pass → **H1 forward direction confirmed on real IEA-15 data**.
Magnitude is ~3× lower than the ITIBarge stand-in (0.0175 nats) for
three plausible reasons documented in
[[validation/case-3-iea15-single-case-te]]: heavier/better-damped
platform (`std(PtfmPitch) = 0.68°` vs 2.30° on the barge), only 240 s
of post-transient data (UMaineSemi surge period ~100 s — need longer
TMax for Phase 4), and parent-set search not sparsifying (all 30 source
lags + 30 target lags selected). Significance is rock-solid (p=0.005
floor for n_perm=200).

Validation page [[validation/case-3-iea15-single-case-te]] updated to
PASS (real IEA-15 UMaineSemi, 2026-05-15) — replaces the
PASS (smoke-test variant on ITIBarge) status.

**Three Windows-env gotchas captured**:
1. `JAVA_HOME` must be set inline when invoking the te-fowt python
   directly (`JAVA_HOME=…/Library/lib/jvm python script.py`). Same as
   case-4. Documented in case-3 validation page.
2. PowerShell `set X=Y` does NOT work in the Bash tool; use bash
   inline-env syntax `VAR=value command`.
3. JVM lives at `anaconda3/envs/te-fowt/Library/lib/jvm/bin/server/jvm.dll`.

## [2026-05-15] structure | Vault consolidation — everything moved into wiki-transfer entropy/

User requested the project layout flatten so everything lives inside
the Obsidian vault. Six sibling directories moved from
`D:\Causal Effect with transfer entropy\` into
`D:\Causal Effect with transfer entropy\wiki-transfer entropy\`:

| Dir | Size | Move duration |
|---|---|---|
| `analysis/` | <1 MB | instantaneous (NTFS rename) |
| `data/` | 1 MB | instantaneous |
| `reports/` | 0 MB | instantaneous |
| `vault-legacy/` | 0 MB | instantaneous |
| `sims/` | 124 MB | instantaneous |
| `repos/` | 2,479 MB | 32.2 s (copy-then-delete; .git internals refused atomic rename) |

`requirements.txt` also moved into the vault root. Project root now
contains only `.claude/` (agent state) and the vault.

**Verified post-move**: all 5 analysis/sims scripts'
`PROJECT_ROOT = Path(__file__).resolve().parents[1]` resolves to the
vault root; 6 critical paths (the IEA-15 .outb, both Parquet outputs,
RAFT yaml, r-test land case, IDTxl JIDT module) all exist at their new
locations; `load_runs` import from the moved `analysis/` directory
succeeds. **No script edits needed** — the move preserved the relative
relationship between scripts and the dirs they reference.

**PLAN.md** §"Directory layout" rewritten with the new flat structure;
**SCHEMA.md** three-layer table updated to remove the "external" tier
and add the Obsidian-indexing trade-off note.

**Trade-off accepted**: Obsidian now indexes 2.5 GB of vendored OpenFAST
clones in `repos/`. If graph view / file search become painful, exclude
`repos/` (and possibly `sims/`, `data/`) via Settings → Files & Links
→ Excluded files.

## [2026-05-15] lint | Two audit agents reviewed Phase 1 close-out

Two parallel general-purpose agents audited the project state.

**Agent 1 (broad sanity)**: ✅ CLEAN. All 6 PLAN/log claims verified
on disk — 4 validation cases, Tier-1 papers + Jeon-2025 ingest, toolchain
probe, RAFT smoke, IEA-15 OpenFAST run + "terminated normally" log.

**Agent 2 (defensibility, 4 axes)**:
- Methodology grounding: **DEFENSIBLE**. Formulas + IDTxl settings match
  Schreiber 2000 / Kraskov 2004 / Wollstadt 2019. One drift:
  [[concepts/surrogate-significance]] promises IAAFT but scripts use
  `permute_in_time=True` (time-shuffled). **Reconcile before Phase 4.**
- Plan vs reality: **WEAK** at audit time. Case-4 numerically consistent.
  Case-3 validation page was stale (still reported ITIBarge stand-in)
  — fixed in today's TE re-run (above).
- Wiki health: **DEFENSIBLE**. 48 pages, ~15 orphan wikilinks but all
  marked `*(stub)*` in index. 41/48 pages have `sources:` frontmatter;
  the 7 missing are README scaffolding.
- Phase 2 scale risks: **BLOCKER**. Three concrete issues to fix before
  launching the campaign:
    1. `sims/run_raft_lhs.py:151` hardcodes `N=8` (smoke-test size); no
       CLI flag to scale to Saltelli N=64.
    2. No checkpointing / no parallelism in either driver. At OpenFAST
       scale a single crash wipes everything.
    3. `sims/run_iea15_single.py:120-122` wipes `RUN_DIR` every call —
       DLC matrix would overwrite itself. No per-(wind, seed, wave-mode)
       case ID. Also hardcoded absolute paths to conda envs.

Three items now blocking Phase 2 launch (all closed today):
- [x] Reconcile IAAFT promise vs `permute_in_time` reality
- [x] Refactor `run_raft_lhs.py` v2
- [x] Refactor `run_iea15_single.py` → `run_campaign.py`

## [2026-05-15] structure | Two cookbook pages seeded under pages/cookbook/

Added a task-oriented cookbook layer to the wiki, cross-cutting the
topic-oriented concept/entity/equation taxonomy. Two pages:

- [[cookbook/run-one-openfast-case]] — ~180 lines. Prereqs, deck staging,
  ServoDyn DLL gotcha, TurbSim GridHeight ≥ 270 fix, InflowWind/.fst
  patching, invocation cwd, parsing the .outb, 7-row failure-mode table,
  7 Phase-2 hooks for `run_campaign.py`. Feeds task #9.
- [[cookbook/build-saltelli-ensemble]] — ~210 lines. 9-variable
  bounds table, constraint-flag policy, `coerce_to_rigid` shim,
  `PYTHONUTF8=1`, `JAVA_HOME` for direct env-python, SALib order-of-operations,
  parquet schema, 6-row failure-mode table. Feeds task #8.

Rationale: the gotchas were scattered across log entries and validation
pages — every Phase 2 development session was re-deriving them. One
file per task should replace ~5 grep'd entries.

## [2026-05-15] structure | run_raft_lhs.py v2 — 9 vars, CLI N, checkpoint, parallel

Production driver for Phase 5 Saltelli ensemble. Lifted from v1
(4 vars, N=8 hardcoded, serial, no resume).

**New capabilities**:
- All 9 locked design variables, parameterised as multiplicative factors
  in [0.8, 1.2] (Sobol indices are scale-invariant; factor form is simpler
  to apply across the YAML structure).
- `--N` CLI flag (default 8 = smoke). `--workers` for parallelism.
  `--skip-existing` for resume after crash. `--out-suffix` for run naming.
- Per-eval checkpoint to partial parquet — every result appended +
  deduplicated by `sample_id` so a kill/resume picks up cleanly.
- `ProcessPoolExecutor` with worker-init that sets `PYTHONUTF8` and
  `JAVA_HOME` (cookbook gotchas 2, 3).
- 3 jeon-2025 geometric constraints checked in dimensional units before
  RAFT is called; infeasible designs short-circuit to `feasible=False`.
- Sobol analysis with median-imputation for infeasible Y values; reports
  `n_feasible/n_total` per response.

**Smoke test (N=4 = 44 evals serial)** found three failure modes:

| Mode | Count | Cause |
|---|---|---|
| Geometrically infeasible | 32 | Mostly `D_OCol ≤ D_Pt` (both have baseline 12.5 m; ±20% box spans the constraint cliff) |
| `raft_failure` | 8 | RAFT raised "NaN in response vector" — clustered around `H_Draft=0.8125 + R_MO=1.1875 + D_Pt=0.8625` (wide-and-shallow regime) |
| `raft_diverged` (silent) | 1 | RAFT's static-equilibrium solver converged to surge_avg=9700 m, heave_avg=387000 m at sample 16. Driver now flags this via a post-eval sanity guard (unphysical if `\|surge/sway/heave_avg\|` > 1000 m or non-finite). |
| Truly feasible | 3 | Sane physics: surge ~0.4 m, heave ~-25 to -37 m, pitch_std ~0.1-0.4° |

**Production sizing**: feasibility envelope ≈ 7% at N=4. At production
N=64 (704 evals): ~50 feasible designs. Borderline for stable Sobol —
recommend N≥128 if narrow CIs needed for the publication baseline.

Reproduces with: `python sims/run_raft_lhs.py --N 64 --workers 7 --skip-existing`
(env vars: `JAVA_HOME` + `PYTHONUTF8=1`).

## [2026-05-15] structure | sims/run_campaign.py — Phase 2 DLC matrix runner

Production OpenFAST driver. Replaces `run_iea15_single.py` (smoke).

**Capabilities**:
- Per-case ID `<dlc>_v<wind>ms_s<seed>` (e.g. `dlca_v11ms_s00`); each case
  in its own `sims/<case_id>/` directory.
- Three DLC sets: `dlca` (24 cases, NTM × 4 winds × 6 seeds, correlated
  wave), `dlcb` (24 cases, decoupled wave seed via XOR mask), `dlc16`
  (6 cases at V=11 m/s, SSS Hs=8.3 Tp=12.95 — predecessor cross-comparability).
- Wind seeds: 6 deterministic 7-digit primes. Wave seed = wind seed for
  DLC-A/16 (correlated); `(wind_seed ^ 0x5A5A5A5A) & 0x7FFFFFFF` for
  DLC-B (decoupled but reproducible).
- HydroDyn / SeaState patcher writes `WaveHs`, `WaveTp`, `WaveSeed(1)` per
  case. Hs/Tp table approximates joint Hs|V for North-Atlantic wind sea
  at the 4 wind speeds (replace with site-specific lookup for publication).
- Resume support: skips any case whose final `.outb` already exists.
- Env-var overrides: `OPENFAST_EXE`, `TURBSIM_EXE`, `ROSCO_DLL`.
- `--dry-run` prints the case list + per-case wave/wind seeds without
  running anything.
- Parallelism via `ProcessPoolExecutor` (default `cpu_count - 1`).

**Two bugs caught during patch-only smoke** (not in the cookbook — added
later):
1. `re.sub` interprets `\U` in Windows replacement paths as a regex
   escape — `bad escape \U` error. Fix: pass the replacement as a lambda
   so backslashes aren't re-parsed.
2. `\b` between `)` and whitespace does NOT match (no word/non-word
   transition since both are non-word). The WaveSeed(1) patch was
   silently a no-op. Fix: remove the `\b`; assert the substitution fired.

**Verification done**: patch-only smoke on 3 cases (one per DLC) — confirmed
WaveHs, WaveTp, WaveSeed(1), ServoDyn DLL path, TMax, and OutFileFmt all
applied correctly per case. Did NOT run an end-to-end OpenFAST execution
through the new driver — the patching helpers are lifted from the
known-working `run_iea15_single.py` (which produced the May-14 IEA-15
case-iea15-real.outb), so risk is low; first real campaign launch will
be the production end-to-end check.

**Launch syntax** (when ready):
```
# Dry-run first to see the case list
python sims/run_campaign.py --dlc dlc16 --dry-run

# Real launch (predecessor-DLC1.6, 6 cases at V=11, fastest scope)
python sims/run_campaign.py --dlc dlc16 --tmax 3600 --workers 6

# Full DLC-A (24 cases, ~12 h on 6 cores at TMax=3600)
python sims/run_campaign.py --dlc dlca --tmax 3600 --workers 6
```

**All three Phase-2 prep blockers from 2026-05-15 audit now closed.**
Phase 2 sim campaign can launch when the user is ready.

## [2026-05-15] lint | Vault-move broke two editable installs (caught + fixed)

When the morning's vault consolidation moved `repos/` from the project
root into the vault, **two path-pinned package installs broke silently**:

| Package | Install type | What broke |
|---|---|---|
| `openfast_toolbox` | pip-editable (`pip install -e repos/openfast_toolbox`) | Editable wheel pointed at the OLD `D:\…\repos\openfast_toolbox\` path |
| `idtxl` | `.pth` file bypass at `site-packages/idtxl.pth` | Pointed at the OLD `D:\…\repos\IDTxl\IDTxl-master` path |
| `raft` | regular non-editable install | ✓ unaffected (files in site-packages, no path reference) |
| WEIS finder (`__editable___weis_2_1_2_finder.py`) | finder-based editable | Has stale paths in `MAPPING`/`NAMESPACES` but only used for `examples/`/`docs/`/etc. — `raft` import path bypasses it |

**Discovery**: `te_pipeline.py` smoke test failed with
`ImportError: No module named 'openfast_toolbox'`. Editable-install metadata
in site-packages stored the absolute path it was installed from; that path
no longer existed.

**Fix**:
- `pip uninstall openfast_toolbox` then
  `pip install -e wiki-transfer entropy/repos/openfast_toolbox`
- Rewrote `site-packages/idtxl.pth` with the new path

**Why this didn't catch Phase 5 N=64** (which used `raft` via 5
worker processes): `raft` was installed as a regular package — files
copied into site-packages, no path reference. Phase 5 ran fine; the
break only surfaced for the path-pinned pair.

**Cookbook addendum candidate**: add a "Recovering from a project-root
move" page covering the editable-install + .pth re-registration pattern.
Deferred.

Also fixed minor str-vs-Path bug in `analysis/load_runs.py::load_outb` —
function now does `path = Path(path)` at entry so callers can pass either.

## [2026-05-15] structure | analysis/te_pipeline.py + Phase 5 N=64 production run

Two pieces of work landed.

### te_pipeline.py — Phase 4 production TE pipeline

End-to-end per PLAN.md Phase 4 + Wollstadt 2019:

```
load .outb -> drop transient -> decimate to 5 Hz -> jitter (1e-10)
  -> per (env_source, response_channel) pair:
       BivariateTE (KSG, IDTxl)
       Conditional MultivariateTE (KSG, IDTxl)  [if both env sources present]
       Gaussian-Granger baseline (same IDTxl, estimator='JidtGaussianCMI')
       AIS per response (KSG, IDTxl)   [effect-size denominator]
       Coherence baseline (scipy.signal.coherence)  [linear ceiling]
  -> long-form parquet (case, source, target, method, te_nats, p, ...)
  -> NetworkX DiGraph (edge weight = mean TE_frac across cases)
```

Settings dataclass `TESettings` with PLAN-canonical defaults:
`decimate_target_hz=5.0`, `transient_drop_s=600`, `kraskov_k=4`,
`max_lag=30`, `n_perm=200`, `perm_type='circular'`, plus `alpha=0.05`.

`--smoke` flag runs 1 env × 1 response (`Wind1VelX → PtfmPitch`) with
`n_perm=50` and skips conditional + Granger — a 2-min sanity check
before committing the longer per-case batch.

Default channels match Q1 / PLAN locked list:
- env sources: `Wind1VelX`, `Wave1Elev`
- responses: `RootMyc1`, `RootMxc1`, `TwrBsMyt`, `PtfmHeave`, `PtfmSurge`,
  `PtfmPitch`, `FAIRTEN1`, `FAIRTEN2`, `FAIRTEN3`

### Phase 5 N=64 production Sobol

`run_raft_lhs.py --N 64 --workers 5 --out-suffix v2-N64` — 704 RAFT evals
in 4 min wall clock on 5 workers (~3 evals/s; far faster than projected).

**313/704 feasible (44 %)** — much better than the 9 % at N=4 smoke.
Sobol indices computed with NaN imputation for infeasible rows.

Headline finding (preliminary, smoke-quality): **mooring line length
`L_u` is the dominant driver across most responses** — `ST(L_u | surge_avg)
= 1.26 ± 0.67`, `ST(L_u | surge_std) = 0.82 ± 0.44`, `ST(L_u | heave_std)
= 1.56 ± 1.21`. Some indices > 1.0 (non-physical bound) indicates
numerical instability from the median-imputed infeasible rows + the wide
CIs say "more samples needed".

**H4 status: weak so far**. H4 predicted `ST(EA | std(PtfmSurge)) > 0.5`;
the N=64 result gives `0.09 ± 0.08` — well below threshold. But the
numerical instability + median imputation in infeasible rows make this a
preliminary indication, not a confirmation. Re-test at N=256 (~50 min)
before drawing conclusions.

Output files:
- `data/raft_lhs_v2-N64.parquet` (704 rows × 21 cols)
- `data/raft_lhs_v2-N64_sobol.json` (S1/ST + CIs per response)

## [2026-05-18] structure | Vault initialized as git repo for server deployment

Root-cause fix: in the 2026-05-18 "what's the next step?" turn I missed
that production runs target the 65-core Linux server (documented in
[[SERVER_DEPLOYMENT]] but never referenced from [[PLAN]] or the log) and
proposed local DLC-A launches that would have burned days. Three things
landed to remove the bug:

1. **PLAN.md patched** — new §"Compute target" right after the phase
   overview, callout box at the top of Phase 2 §Tooling, and the closing
   "Execution order" §"Now active" block updated to reflect the actual
   state: all three Phase-2 prep blockers closed locally; the new ⏳ items
   are server-deployment steps + the DLC-1.6 H1-null interpretation.
2. **Memory** — `project_compute_target.md` added so future sessions land
   on the server-as-production-target answer without re-reading every file.
   Indexed in `MEMORY.md`.
3. **Repo bootstrapped for sync** — `git init -b main`, `.gitignore`
   (excludes `repos/` 2.5 GB, `.outb` ~250 MB each, regenerated DLC case
   dirs, derived `.parquet/.json`, `.claude/`, Obsidian workspace state),
   `.gitattributes` (LF on Linux for `.py/.sh/.dat/.fst`), and
   `pull-results.sh` (rsync template for `sims/` outputs + `data/` +
   `analysis/*.log` + `reports/`).

**Sync model** (one author, two machines): Git is **one-way for code**
(Windows → GitHub → server, server `git pull`s, never commits); rsync is
**one-way for results** (server → Windows via `pull-results.sh`, never
through Git — results are too big for GitHub's 100 MB/file + 1 GB-soft repo
caps anyway). Server stays write-only for `.log/.outb/.parquet`; the
narrative `pages/log.md` is authored here, never on the server.

**First commit composition**: 60.4 MB across 401 files — `pages/`,
`analysis/*.py`, `sims/*.py` (drivers only, not generated cases),
`sims/case-iea15-real/` reference inputs (minus heavy outputs), `raw/`
(69 MB — papers + manuscripts), top-level `.md`s, `pipeline.py`,
`environment.yml`, `requirements.txt`, `.obsidian/` config (minus
`workspace.json`).

**Remaining manual step** (cannot be done from this Claude session): user
creates a private GitHub repo via the web UI, then in GitHub Desktop:
File → Add Local Repository → point at the vault → Publish. See
[[SERVER_DEPLOYMENT]] §1 Option A.

## [2026-05-18] structure | Server deployed, two bugs patched, production pipeline launched

End-to-end server setup completed in one session.

**Server**: `lams@<host>:/home/lams/Desktop/sina/fowt_te_causal/fowt-te-causal/`
**Python env**: existing `raft-env` (anaconda3) — already had scipy, pandas,
SALib; pip-installed the remaining 11 packages onto it. Repos cloned
under `repos/`: IDTxl, openfast_toolbox, RAFT (standalone, not WEIS),
IEA-15-240-RWT, r-test. IDTxl registered via `site-packages/idtxl.pth`
bypass. JDK 11 from system (`/usr/lib/jvm/java-11-openjdk-amd64`).
OpenFAST + TurbSim from conda-forge (env binaries).

**Env vars** added to `~/.bashrc`:
- `OPENFAST_EXE`, `TURBSIM_EXE`: `/home/lams/anaconda3/envs/raft-env/bin/{openfast,turbsim}`
- `ROSCO_DLL`: `…/site-packages/rosco/lib/libdiscon.so`
- `JAVA_HOME`: `/usr/lib/jvm/java-11-openjdk-amd64`
- `PYTHONUTF8=1`

**SSH**: ed25519 key generated on server, public key uploaded to GitHub
account `sinahdme`. Repo cloned via `git@github.com:sinahdme/fowt-te-causal.git`.

**Three production-blocking bugs found and fixed**:

1. **OpenFAST v4.1.2 vs v4.2 ElastoDyn format mismatch.** Server's
   conda-forge openfast was 4.1.2; IEA-15 deck requires v4.2.x. Fix:
   `conda install openfast=4.2 -c conda-forge -y` (bumped to 4.2.1,
   no numpy/scipy churn).

2. **`patch_hydrodyn` false-positive on re-runs.** Used `new_txt == txt`
   to detect regex miss, but a deterministic seed produces a no-op
   match (same value written), failing the check incorrectly. Fixed:
   switched to `re.subn` with explicit count check.
   Commit `2ae0df7`, `sims/run_campaign.py`.

3. **`run_turbsim` treated 0-byte wind.bts as finished.** Killed previous
   run left empty wind.bts placeholders; `bts.exists()` returned True,
   skipped TurbSim, OpenFAST then crashed seconds into the next run.
   Fixed: check `bts.stat().st_size > 0`, unlink the stub if zero.
   Commit `36fd851`, `sims/run_campaign.py`.

**Performance surprise**: TurbSim on this server is ~50× slower per
core than the Windows dev box — a single 180 s wind file took 4117 CPU
seconds (~69 min). Conda-forge binary likely unoptimized, or the
machine has slow per-core perf despite 65 cores. SERVER_DEPLOYMENT.md's
"~4 h total" estimate is unrealistic for this hardware; revised estimate
based on actual measurements: **5–8 h** for full pipeline (TurbSim parallel
across 32 workers brings the wall time down to ~70 min per Phase 2 DLC).

**Phase 5 N=256**: completed cleanly in <2 min. Output:
`data/raft_lhs_v2-N64.parquet` (existing suffix retained per pipeline
default; need to confirm whether this is the 64 or 256 file once
results are pulled back).

**Phase 2 dlc16** currently running (launched 21:08 KST):
- PID 4120121 (`pipeline.py`)
- 6 TurbSim instances active
- Log: `analysis/production-20260518-2108.log`
- No failures so far

**Pre-existing orphan processes** found on server: dozens of
`python run_pipeline.py --step openfast` and `--step raft_hf` from
March/April, all sleeping, 0% CPU. From the user's previous FOWT work.
Not affecting this run; clean up with `kill <PID>` opportunistically.

**Post-PC-restart instructions** for the user (server work survives
the restart via nohup + disown):
1. SSH back to server (same credentials as today).
2. `cd ~/Desktop/sina/fowt_te_causal/fowt-te-causal`
3. `tail -f analysis/production-20260518-2108.log` to see progress, or
   `ls sims/*/IEA-15-240-RWT-UMaineSemi/*.outb | wc -l` to count
   completed cases (max 54 = 6 dlc16 + 24 dlca + 24 dlcb).
4. When pipeline exits, from Git Bash on Windows:
   `./pull-results.sh lams@<server>:/home/lams/Desktop/sina/fowt_te_causal/fowt-te-causal`
5. Tell Claude on the Windows side: "the pipeline finished, look at
   `analysis/*.log` and `data/*.parquet`."

## [2026-05-20] structure | Slow-drift physics correction and downstream code updates

Triggered by an internal review of `2026-05-20-technical-report-ver03.docx`
(see [[../reports/2026-05-20-technical-report-ver03-review]]). The §6.3
sentence "the platform pitch eigenfrequency (~0.034 Hz) sits well within
the spectral peak of the SSS wave forcing" is physically wrong: at
Tp = 12.95 s the first-order JONSWAP peak is at fp ≈ 0.077 Hz, not
0.034 Hz. The pitch eigenfrequency is in the **low-frequency tail** of
the first-order spectrum; what excites pitch there is **second-order
difference-frequency wave forcing** (slow-drift).

Verification audit of the existing OpenFAST campaign: the IEA-15
UMaineSemi `HydroDyn.dat` has `DiffQTF = 12` enabled (using the
WAMIT `.12s` file shipped with the deck), so the simulated platform
dynamics **do** include the slow-drift forcing. The 54-case campaign
data is therefore physically valid for this mechanism — no re-run is
needed for the simulation half.

**However**, three downstream analysis settings are tuned for shorter
timescales than the slow-drift period (~29 s = 145 samples at 5 Hz)
and need to be raised before Phase 4 can detect the wave→pitch coupling
at the pitch eigenfrequency. Three commits land today:

1. `analysis/te_pipeline.py`: `TESettings.max_lag` raised from
   **30 → 150 samples** (6 s → 30 s embedding window). Filed as
   [[open-questions]] Q12. CLI default also bumped.
2. `analysis/te_pipeline.py`: `coherence_baseline()` now accepts
   `nperseg_target` (default 4096), giving Welch Δf ≈ 0.0012 Hz —
   sharp enough to resolve the pitch eigenfreq (0.0345 Hz) from the
   JONSWAP peak (0.077 Hz). Filed as [[open-questions]] Q13.
3. Phase 5 N=256 plan revised: instead of N=64's median-imputation
   for infeasible Y, the production run will use **rejection sampling
   within the feasible region**. Filed as [[open-questions]] Q14
   (under investigation; decision before launch).

**Report ver05** built with these fixes plus an interpretive sentence
in §6.4 noting that the unexpected L_u dominance over EA in the
preliminary Sobol is physically consistent with the slow-drift
mechanism: L_u sets the surge natural frequency (~0.01 Hz, in the
slow-drift band) while EA matters only at higher frequencies where the
catenary geometry is taut. The L_u finding and the §6.3 pitch null
are therefore the **same physical story** seen from two channels.

**Implication for the H1 evaluation strategy**: the DLC-1.6 batch H1
null observed on 2026-05-15 may need to be re-evaluated with the
new max_lag=150 setting before it can be properly interpreted as a
controller-rejection signature rather than an embedding-too-short
artifact. The May 14 case-iea15-real H1 first-cut PASS (`TE = +0.0052
nats, p = 0.005` at 300 s NTM, single seed) was not in the SSS regime
and is less affected — the wind-driven direct path dominates there.

## [2026-05-26] structure | Campaign completed — catch-up entry (DLC-A/B, Phase 4 bivariate, N=256 Sobol, scorecard, reports)

Consolidated catch-up: the narrative log lapsed after 2026-05-20 while
the campaign finished on the server. Reconstructed here from git history
(commits `c11bbb9`, `0dd383f`, `98f2f4d`), `reports/hypothesis-scorecard.md`,
and the report drafts. Authoritative numbers live in the scorecard.

- **Phase 2 — full DLC matrix done.** All 54 OpenFAST cases completed
  (6 DLC-1.6 + 24 DLC-A + 24 DLC-B), 1 h each. Pulled back to `sims/`.
- **Phase 4 — bivariate first pass done.** `reports/te_table.parquet`
  (54 cases) via `analysis/run_phase4_parallel.sh` with the
  **scope-reduced** settings: bivariate KSG only, 2 Hz, `max_lag=60`,
  `n_perm=50`, `--no-conditional --no-granger`. This is a first-pass
  table, **not** the publication-grade run (see 2026-06-01 below).
- **Phase 5 — N=256 production Sobol done** (commit `98f2f4d`, after a
  WEIS-clone fix). 2816 RAFT evals, 971 feasible. Focus-channel Sₜ now
  in [0,1] with CIs ~halved vs N=64. **L_u-dominates / EA-negligible
  pattern survives N=64 → N=256 cleanly.**
- **Hypothesis scorecard** (`reports/hypothesis-scorecard.md`, 2026-05-25)
  scores H1–H6 against the above. Headline: two pre-registration-paid
  surprises — (1) EA-vs-L_u inversion (H4/H5a), (2) wind→pitch TE null
  (H1). H3 / rigorous H5b / windowed-H6 left **unevaluable** by the
  `--no-conditional --no-granger` first pass.
- **Reporting** progressed to ver04–ver07 (`reports/*.docx`,
  `2026-05-21-...-ver06.pdf`) + Phase 6 figures (`reports/figs/`:
  fig3 TE network, fig4 Sobol-ST, fig5 combined causal graph).

**Known gaps carried forward** (all trace to the first-pass scope cuts):
Granger baseline missing (plan calls it mandatory), conditional TE missing
(the project's headline novelty), and the H1/H6 nulls measured at
`max_lag=60` / 2 Hz — shorter than the 2026-05-20 slow-drift physics
correction (`max_lag=150`) says is needed. Addressed next.

## [2026-06-01] structure | Phase 4 full-settings rerun launcher (journal-tier gap closure)

Decision (this session): target **journal tier** (WES / Marine
Structures) and close the first-pass gaps with one full-settings Phase 4
rerun instead of writing up bivariate-only results.

- **`analysis/run_phase4_full.sh`** added — sharded launcher mirroring
  `run_phase4_parallel.sh` but with the publication-grade settings:
  conditional + Granger + AIS + coherence **ON**, `--max-lag 150`
  (30 s slow-drift window at 5 Hz), `--decimate-target-hz 5.0`,
  `--n-perm 200`. These are the `te_pipeline.py` `TESettings` defaults;
  the first pass had overridden them down. Writes
  `reports/te_table_full_p<W>.parquet` so the bivariate
  `te_table.parquet` stays reproducible.
- **`analysis/merge_parquet_parts.py`** — added `--prefix` / `--out`
  (backward-compatible) so full-rerun shards merge into
  `te_table_full.parquet` without clobbering the first-pass table.

**Closes in one run**: Gap 1 (Granger baseline for every pair, needed for
the publication baseline-comparison table), Gap 2 (conditional TE → H3
and rigorous H5b), and re-tests the H1 / H6 nulls at the physics-correct
`max_lag=150`. Cost is ~20–50× the first pass per case — **server work**;
header documents a one-case timing probe before sharding 54.

**Sequence from here**: (1) timing probe on one DLC-A case; (2) full
sharded run (~36 workers) + merge; (3) pull back, re-score H1/H3/H5b/H6
against `te_table_full.parquet`; (4) controller-off Q11 run if the H1
null survives — quantifies ROSCO's wind-disturbance rejection; (5) H6
windowed-TE driver (lowest priority). Then finalize report ver08.

## [2026-06-01] structure | New server bootstrap + IDTxl silent-exit bug fixed

User deployed the full pipeline on a **new** Linux box
(`isaactest@oem-MD72-HB3-00`, env `fowt-te` from `environment.yml`,
conda-forge OpenFAST 4.2.1 + openjdk 11.0.30 + jpype1 1.7.1),
regenerating everything from scratch (old server's 54 `.outb` not
transferred). **TurbSim is healthy here** (~90 s/case, dlc16 in 2.8 min)
— *not* the old server's 50× slowdown — so regeneration is viable.

Three clean-env gaps surfaced and were fixed (all now in
[[SERVER_DEPLOYMENT]] §3d + §8):
1. `environment.yml` missing `mpmath` (IDTxl Rudelt import) → `pip install mpmath`.
2. `environment.yml` missing `rosco` (ServoDyn `libdiscon.so`) → `pip install rosco`.
3. **The big one** — `idtxl/estimators_opencl.py:16` has a bare `sys.exit()`
   in its `except ImportError` block. With no `pyopencl` installed and the
   `_find_estimator` module-import order reaching `estimators_opencl` before
   `estimators_jidt`, that `sys.exit()` killed the whole process: **`EXIT=0`,
   no traceback, empty TE table**. Patched to `pass` in the clone (`.bak`
   kept). This worked on local/old-server only by import-order luck (JIDT
   found first). Would have silently produced 54 empty Phase-4 cases.

Diagnostic path (recorded because the failure was maximally deceptive —
exit 0 looks like success): bisected with minimal reproductions — bare
`jpype.startJVM` OK → IDTxl's exact start args + class load OK → JVM after
numpy OK → OpenBLAS thread-pin no effect → per-module import loop pinpointed
`estimators_opencl` as the killer → read source → `sys.exit()`. The local
Windows `te-fowt` run was the known-good baseline throughout
(`te ≈ 0.45`, `DONE`). **Lesson reinforced: validate the JIDT path with
`test_ar1_te.py` (a real estimate, not just imports) before launching any
campaign** — now a required step in §3d.

Campaign launch (Phase 5 N=256 + Phase 2 dlc16/dlca/dlcb @ TMax=3600,
then `run_phase4_full.sh`) proceeds once `test_ar1_te.py` is green on the
new box.

## [2026-06-04] structure | GPU/OpenCL TE estimator + process-pool parallelism

Backfilled 2026-07-09 from git (`da8d18a`…`d1481ff`).

- Added OpenCL/GPU KSG estimator option to `te_pipeline.py`, plus a process
  pool with multi-GPU round-robin (`--gpu/--gpus/--workers`).
- Added `--tau` embedding-subsampling flag.
- Patched IDTxl's OpenCL estimator scalar-return crash on numpy 2.x; scoped
  the coercion to `_calculate_single_link` only.
- Earlier (2026-06-02, `ca99535`): closed the Phase 4 skip-trap and fixed the
  `test_ar1_te.py` max_shift crash.

## [2026-06-06] structure | Tau validation tooling + controller-off ablation driver

Backfilled from git (`993ea4f`, `57359aa`, `d1fa08a`).

- `pick_tau.py` — data-driven embedding delay selection.
- `compare_tau.py` — validate a thinned-tau run against a baseline
  (merge-key bug fixed 2026-06-09: join on (source, target), not case).
- Controller-off ablation driver + conditional-TE GPU probe.

## [2026-06-10] structure | Conference abstract + wind–wave attribution diagnostics

Backfilled from git (2026-06-09/10 commits).

- Bilingual (EN/KO) conference abstract + keywords; talk outline with real
  numbers and the honest firewall framing; paper novelty statement (strong +
  fallback, sweep-contingent).
- `wind_wave_indep.py` — wind/wave (in)dependence diagnostic.
- `load_band_attribution.py` — frequency-band variance gate for the
  wind–wave thread, with `--notch-1p` (wave-only vs rotor-line split).

## [2026-06-12] structure | Campaign hardening for unattended batch runs

Backfilled from git (`b797444`, `d3acede`…`06459d4`).

- `te_rerun_missing.py` — salvage + watchdog'd rerun for hung jobs, later
  `--force-targets` for uniform-tau slow-drift recompute.
- Per-job watchdog + **per-target tau** for slow-drift channels
  (PtfmPitch/PtfmHeave hang or NaN at tau=1; rerun at tau=5).
- Stem-based `case_id`, `run_campaign.sh` for unattended batches,
  workers pinned to 4 (proven reliable), `.outb` staging via folder-named
  symlinks.

## [2026-06-17] structure | Conference deck reconciled to full-campaign data

Backfilled from git (`1776f52`, `cc07e39`, `bcc3312`).

- Results figures reconciled to the full-campaign TE data.
- Added LAMS/KSNU lab-format build (32 slides); body text later switched
  Korean → English.

## [2026-06-29] structure | KSG max_lag=150 falsely nulls Wave→Heave — fixed

Backfilled from git + `SESSION-LOG-2026-06-29.md` (full session record there).

- The 1-case full-settings probe (max_lag=150, 5 Hz, n_perm=200, GPU, 9.1 h)
  showed `TE(Wave→PtfmHeave)=0` while Granger saw 0.35 — would have wrecked
  the H2/H6 story. Diagnostic sweep proved a **greedy-selection artifact**:
  KSG TE = 0.066 at max_lag=30, collapses to 0 at max_lag≥60.
- Fix: decoupled `max_lag_sources` (short, sensitive source search) from the
  target embedding `max_lag` (long, for slow drift) — `986f867`.
- Also fixed a `case_id` collision in `run_phase4_full.sh` and added
  `--slow-drift-tau 5`. (2026-06-24, `4984844`: conditional-TE source
  extraction fix + full-table check.)

## [2026-07-03] structure | Fix re-validated; --max-lag-sources 20 wired in

Backfilled from git (`e8d3622`, `18ed2bf`).

- Re-validation on lams passed; `--max-lag-sources 20` wired into
  `run_phase4_full.sh`.
- Repo hygiene: ignore root scratch binaries; track SURD plan, session log,
  scorecard; executable bits on the `.sh` launchers.

## [2026-07-06] structure | SURD Phases 0–2 complete + Phase 4 full campaign relaunched on GPU

Backfilled from git (`2ba1706`…`126aa5f`, `0e550e0`).

- **SURD subproject** ran Phase 0 → Phase 2 in one push:
  - Phase 0 validation gate PASSED (mediator case reproduced).
  - Phase 1 thin slice: leak-drop metric failed its bias control; refined
    with a pitch-rate state — GATE OPEN.
  - Phase 2: firewall-focused campaign runner, 55-case `surd_table.parquet`
    + cross-case analysis + comparison figures. Headline numbers:
    **2.8× firewall dose-response** at/above-rated vs below-rated;
    open-loop twin −59% with U:BldPitch1→0; **94% of TE-null cases** show
    the mediated path.
- **Phase 4 full campaign**: CPU-shard run had wedged (JVM swallowed the
  watchdog SIGTERM); relaunched with a **single-process GPU launcher** on
  lams, both A100s ~99% (`0e550e0`). Still running as of 2026-07-09.
- Hygiene (`5a80adf`): `te_frac` is TE/AIS everywhere; the coherence flag is
  a threshold, not a statistical test.

## [2026-07-08] structure | TE-firewall manuscript v0.5 via full ARS pipeline

Backfilled from git (`65486fb`, `4186414`).

- Paper Phase 1: fault-detection **signature table** scaffolding.
- `reports/te-firewall-paper-draft.md` taken to **v0.5** through the full
  ARS pipeline (write → review → revise → finalize). Thesis: wind→platform
  TE≈0 is a blade-pitch-control *firewall*; TE rising = pitch fault →
  health-monitoring signal.

## [2026-07-09] lint | Log backfill — gap 2026-06-01 → 2026-07-09 closed

- This log went unmaintained for five weeks while work continued (recorded
  only in git commits and `SESSION-LOG-2026-06-29.md`). Entries above dated
  2026-06-04 onward were reconstructed from git history today.
- Process fix: the agent now appends a log entry at the end of every
  substantive session (rule stored in agent memory) — the wiki log is the
  durable record; git log is not a substitute.
- Still uncommitted in the tree as of today: conference-talk deck builds
  (`reports/_build_te_conference.js`, `_build_te_talk_v2.py`, `_conf2/`…
  `_conf9/`), new figures (Sobol, TE network, delay profiles, pipeline
  diagram), and paper-draft edits newer than v0.5.

## [2026-07-09] structure | SYNTHESIS.md conversation record + CLAUDE.md session rules

- User reported the lams Phase 4 GPU campaign will take **~11 days**; vault
  work fills the window.
- Added **`SYNTHESIS.md`** at vault root (`5b886b8`): durable record of the
  *conversations* — dialogue Q&A both directions, plans, decisions, file
  changes with commit hashes — per session, backfilled 2026-05-12 → today.
  §0 "Current state" block at the top is rewritten each session and answers
  "what were we doing?".
- Added **`CLAUDE.md`** at vault root: standing instruction loaded every
  session — read SYNTHESIS.md §0 at start; before ending, append the session
  entry, rewrite §0, and update this log. Also carries the working
  agreements (surface assumptions, cite primary sources, no wall-clock
  phrasing, `test_ar1_te.py` gate before campaigns).
- Division of labor: this log = task-level record; SYNTHESIS.md =
  conversation/decision record.

## [2026-07-09] structure | CLAUDE.md restructured as planning-agent charter

- User dictated role/mission/workflow rules; CLAUDE.md reorganized into 8
  sections: **Role** (planning agent + coding agent, not a chatbot; Ocean
  Engineering / offshore wind / OpenFAST / information-theory specialist),
  **Mission** (vague goals → sequenced, safely executable plans),
  **Planning standards** (milestones, file-level work areas, verification,
  rollback notes, todos; push back on unclear scope/hidden coupling/risky
  rewrites/missing acceptance criteria; completed items marked with
  evidence, not optimism), **Execution workflow** (inspect → infer patterns
  → list assumptions → plan → todos; scoped changes, preserve user work,
  prefer existing helpers, regression checks; never guess — ask),
  **Output contract** (objective, assumptions, phased plan, touched areas,
  risk register, verification commands, open questions), plus the existing
  session-record, pointers, and working-agreement sections.

## [2026-07-09] lint | Manuscript v0.6 — full numeric re-verification + 4 fixes

- Re-verified every headline number in `reports/te-firewall-paper-draft.md`
  against the parquet tables — Tables 1–5, edge counts (341/486, 69/486),
  te_frac (0.0004/0.043), coherence (0.72…), SURD 0.402, open-loop
  0.167→0.000 & 0.0612→0.0265 (−57%), delay table (0.3/2.7/3.9/6.3 s),
  surge secondary peak (~1.1 s) — **all reproduced exactly**.
- Fixed 4 issues: stale abstract delay range (0.3–4.3 s → transport delays
  0.3–3.9 s + surge antiphase at ≈Tp/2); "three orders of magnitude" → two
  (§4.1); §3.4 now explains the retained non-significant (possibly negative)
  KSG estimates behind Table 2's −0.0005 heave mean; §3.8 alias-avoidance
  claim scoped to in-phase channels. Header bumped to v0.6.
- Gotcha corrected in agent memory: open-loop drop is **−57%**, not −59%.
- Standing requirement: re-verify all paper numbers against
  `te_table_full.parquet` when the lams campaign lands, before Stage 5.

## [2026-07-09] structure | CLAUDE.md rewritten by user as 13-section operating manual

- User replaced the 8-section charter with a 13-section manual (core
  principles, working modes, planning/verification/research standards,
  output contract with confidence ratings, engineering philosophy).
- Review pass applied 4 reconciliations: Mission sentence restored to §1;
  Output Contract scoped to planning/implementation deliverables (short
  answers report applicable sections, always Verification + Confidence when
  work was performed); Planning Mode's no-file-edits rule now exempts the
  mandatory §9 session records; heading levels + EOF newline normalized.

## [2026-07-10] research | Wind–wave forcing independence check (closes Q6)

- User asked whether wind↔wave correlation forces *conditional* TE in the
  firewall paper (headline table uses IDTxl `BivariateTE`). Assessed: the
  concern is real in principle but threatens the two claims asymmetrically —
  the firewall (wind→platform≈0) is protected by SURD's synergy atom, the
  wave-dominance side is the one exposed to redundancy inflation.
- Measured wind/wave dependence directly with the existing
  `analysis/wind_wave_indep.py` on all 8 locally-reachable FOWT runs (6× DLC 1.6
  11 m/s seeds + 1× 8 m/s + the open-loop twin; `case-iea15-real` excluded as a
  300 s calibration case emptied by the 600 s transient drop). Result: **every
  run independent** — |Pearson r| ≤ 0.035, max |cross-corr| ≤ 0.043 over ±30 s,
  MI ≈ 0.04 nats but == the finite-sample bias floor.
- Key methodological catch: the plain i.i.d.-shuffle null gave spurious
  z ≈ 5–12 (effective-sample-size artifact). Redid with an
  **autocorrelation-preserving circular-shift surrogate** → observed MI
  indistinguishable from null (z ∈ [−1.79, +0.90], no p < 0.05, mean excess
  −0.001 nats). So true wind↔wave MI ≈ 0.
- Conclusion: conditional TE ≡ bivariate TE for these sources; bivariate choice
  justified. Full writeup + numbers in `reports/wind-wave-independence.md`.
- IDTxl not installed on the Windows box (lazy import; lives in server env
  `fowt-te`), so the belt-and-suspenders `TE(Wave→PtfmPitch|Wind)` confirmation
  and the 15/20 m/s completeness runs are queued as server follow-ups.

## [2026-07-10] tooling | Server script to finish wind/wave indep on all 54 runs

- Wrote `analysis/wind_wave_indep_all.py` (batch aggregator; reuses
  `wind_wave_indep.py`'s `mutual_info`/`cross_corr`, adds the circular-shift
  surrogate p-value the single-run script lacks, writes
  `reports/wind_wave_independence.parquet`) + thin launcher
  `analysis/run_wind_wave_indep.sh` (matches `run_phase4_full.sh` conventions).
- CPU-only (numpy + .outb reader, no IDTxl/GPU), so it runs in `fowt-te` on the
  server without the estimator stack and doesn't disturb the running campaign.
- **Verified locally**: launcher processed the 9 matched runs → 8/8 usable
  INDEPENDENT (min p = 0.24, mean MI−null excess −0.0015 nats),
  `case-iea15-real` auto-skipped as too_short; parquet schema confirmed.
- Server next step: `conda activate fowt-te && ./analysis/run_wind_wave_indep.sh`
  → adds the 15/20 m/s bins for all-54 coverage; fold rows into
  `reports/wind-wave-independence.md`.

## [2026-07-10] research | KSG k-sensitivity robustness check + §3.3 estimator justification

- User (quoting an IEEE fault-detection paper) asked whether to "consider the
  variables' PDF" in TE estimation. Assessment: the paper already uses the kNN
  (KSG) estimator family — distribution-free, no bandwidth/PDF fitting — the
  right choice vs kernel-density for non-Gaussian, multivariate (conditional +
  SURD) signals; switching to explicit PDF estimation would be a step back.
- Ran a k-sensitivity sweep (`ksg_cmi(...,k=k)` from `delay_analysis.py`, self-
  contained scipy, 3 healthy 11 m/s seeds) over k ∈ {3,4,6,8} on
  Wave→PtfmHeave and Wind→PtfmHeave delay profiles. Result: coupling delay
  (2.73–2.87 s) and firewall (wind ceiling ≤0.03 nats; wave/wind ratio 39–48×)
  are **k-invariant**; only the absolute TE magnitude scales with k
  (1.256→0.866 as k 3→8), as expected for a kNN estimator. Table:
  `reports/ksg-k-sensitivity.md`.
- Inserted a §3.3 estimator-justification paragraph (kNN-KSG over kernel-density:
  distribution-free/adaptive, non-Gaussian, multivariate, jitter for the
  continuity assumption, k-robustness) into paper draft + final, with 3 new
  APA refs (Frenzel & Pompe 2007, Khan et al. 2007, Kozachenko & Leonenko 1987).
