# Plan — Causal Effect on FOWT via Transfer Entropy

## Context

You want to quantify, on a floating offshore wind turbine (FOWT), how much of
the structural response is *causally* driven by:

1. **Environmental excitation** (wind, wave time histories) — natural fit for
   Transfer Entropy (TE), since both inputs and outputs are time series.
2. **Structural design parameters** (mooring stiffness, platform inertia,
   tower stiffness, controller gains, …) — these are *constants per simulation*,
   so classical TE does not apply directly. We will combine TE with a
   sensitivity / surrogate approach (see Phase 5) to handle them.

The project is greenfield: working directory is empty. We will build (a) a
local OpenFAST knowledge base navigable in Obsidian, (b) a simulation campaign,
(c) a Python + IDTxl analysis pipeline.

## Big-picture phases

```
Phase 1  Knowledge base   →  OpenFAST repo + docs in an Obsidian vault
Phase 2  Simulation       →  OpenFAST DLC matrix (wind/wave/param sweeps)
Phase 3  Data pipeline    →  Parse .out/.outb, align, preprocess
Phase 4  TE: env → resp   →  IDTxl bivariate + conditional TE on time series
Phase 5  Param causality  →  Sensitivity (Sobol/Morris) + ensemble-TE for params
Phase 6  Reporting        →  Causal graph, ranked drivers per response
```

---

## Compute target

**Production runs do not happen on this Windows box.** They target a 65-core
Linux server. The local 8-core machine is used only for development, smoke
tests, and one-off cases (e.g. `case-iea15-real`, the H1 DLC-1.6 smoke batch).

Wall-time ratio (full pipeline): **~4 h on the server vs ~3 days locally.**
Everything in §Phase 2 (DLC-A/B 24-case matrices), §Phase 5 at production N
(≥ 256), and §Phase 4 across the full campaign is server-only.

Server setup, sync paths (Git via GitHub Desktop or one-shot scp), env vars,
and the `python pipeline.py all` launch line all live in
[[SERVER_DEPLOYMENT]]. Phase-level launch syntax in §Phase 2 / §Phase 5 below
is reference only — the real entry point is `pipeline.py`, not the per-phase
drivers.

---

## Phase 1 — OpenFAST knowledge base in Obsidian

Goal: a navigable, backlinked vault that lets you (and the analysis) understand
which OpenFAST module produces which channel and which input file controls
which physical parameter.

Repos to clone locally (keep as plain git clones, do **not** convert source
code to markdown — only wrap with notes):

| Repo | Why we need it |
|---|---|
| `OpenFAST/openfast` | Aero-hydro-servo-elastic solver (source + docs) |
| `OpenFAST/r-test` | Regression test cases — reusable input templates |
| `IEAWindTask37/IEA-15-240-RWT` | Reference FOWT model (UMaine VolturnUS-S) |
| `NREL/ROSCO` | Reference open-source controller |
| `NREL/WEIS` | Optimization framework — useful for parameter sweeps |
| `NREL/openfast_toolbox` (a.k.a. pyFAST) | Python parser for `.out` / `.outb` |
| `NREL/MoorPy` | Quasi-static mooring (sanity checks, fast sweeps) |

Directory layout (single-vault flat structure — **everything lives inside
the Obsidian vault** as of 2026-05-15 consolidation):

```
D:\Causal Effect with transfer entropy\
└── wiki-transfer entropy\       # Obsidian vault root = project root
    ├── LLM_Wiki_Pattern.md      # wiki methodology (Part 1–4)
    ├── PLAN.md                  # this plan (mirror of .claude/plans/...)
    ├── SCHEMA.md                # domain-specific schema delta
    ├── requirements.txt
    ├── .obsidian\               # Obsidian config (graph, workspace)
    ├── raw\                     # user-owned immutable source
    │   ├── papers\
    │   ├── manuscripts\
    │   ├── extracts\
    │   ├── data\
    │   ├── figures\
    │   └── notes\
    ├── pages\                   # LLM-owned, evolving
    │   ├── index.md
    │   ├── log.md
    │   ├── overview.md
    │   ├── open-questions.md
    │   ├── wiki-improvement-plan.md
    │   ├── sources\             # one page per ingested source
    │   ├── papers\              # deep analytical pages for key refs
    │   ├── concepts\            # TE, KSG, MI, Sobol, surrogates, …
    │   ├── entities\            # OpenFAST modules, platforms, software, channels
    │   ├── equations\           # eq-transfer-entropy, eq-sobol-*, …
    │   ├── validation\          # 4 verification cases from §Verification
    │   └── analyses\            # filed-back query answers
    ├── analysis\                # Python scripts, notebooks
    ├── sims\                    # OpenFAST run outputs (.out, .outb)
    ├── data\                    # cleaned Parquet time series
    ├── reports\                 # figures, write-ups
    ├── repos\                   # vendored git clones (~2.5 GB)
    │   ├── openfast\
    │   ├── r-test\
    │   ├── IEA-15-240-RWT\
    │   ├── ROSCO\
    │   ├── WEIS\
    │   ├── openfast_toolbox\
    │   └── MoorPy\
    └── vault-legacy\            # deprecated pre-three-layer vault (delete-when-comfortable)
```

`PROJECT_ROOT = Path(__file__).resolve().parents[1]` in all analysis/sims
scripts now resolves to the vault root, so paths like
`PROJECT_ROOT / "repos" / ...` and `PROJECT_ROOT / "sims" / ...` continue
to work without code edits (they did before too — the move preserved the
relative relationship between scripts and project subdirs).

Note: `PLAN.md` and `LLM_Wiki_Pattern.md` live **inside the vault root** so
they appear in Obsidian's Quick Switcher and can be linked via plain
wikilinks (`[[PLAN]]`, `[[LLM_Wiki_Pattern]]`). The canonical plan still
lives at `C:\Users\kunsanuni3\.claude\plans\in-this-project-i-steady-church.md`;
this file is a working mirror.

Wiki construction approach:

- **Three-layer split** per `LLM_Wiki_Pattern.md`:
  user owns `wiki/raw/` (immutable); LLM owns `wiki/pages/`;
  `wiki/SCHEMA.md` is co-evolved. Large `repos/` stay outside the vault for
  portability — referenced by relative path from pages.
- **Kebab-case filenames**, YAML frontmatter on every page (`title`, `type`,
  `created`, `updated`, `sources`, `tags`).
- **Folder-prefixed wikilinks** only: `[[entities/openfast-aerodyn]]`, never
  bare `[[X]]`.
- Equations live as standalone `eq-*.md` pages; concept pages link out.
- Use Obsidian Graph View to inspect dependency structure.
- Optional plugins: **Dataview** (frontmatter queries), **Excalidraw** (causal
  sketches).

We will write a one-shot Python script `analysis/build_vault.py` that:
1. Walks `repos/openfast/docs/source/`, runs pandoc per file.
2. Writes converted MD under `wiki/raw/extracts/openfast-docs/`.
3. Updates (does not overwrite) `wiki/pages/entities/openfast-*.md`
   incrementally.

---

## Phase 2 — Simulation campaign

Reference model:

- **Primary (locked)**: **IEA-15MW UMaine VolturnUS-S** semisubmersible
  from the `IEA-15-240-RWT` repo.
- **Second platform for Q5 multi-platform comparison (locked)**:
  **IEA-22MW-RWT-Semi** — gives direct continuity with [[sources/jeon-2025]]
  predecessor work. Adds the cross-platform "does causal structure scale?"
  figure for the publication.

**Response channels** ([[open-questions]] Q1 — **locked 2026-05-13**
via [[sources/jeon-2025]]): the 9 channels logged in the predecessor
validation campaign:

| Group | Channels |
|---|---|
| Structural loads | `RootMyc1`, `RootMxc1`, `TwrBsMyt` |
| Platform motions | `PtfmHeave`, `PtfmSurge`, `PtfmPitch` |
| Mooring | `FAIRTEN1`, `FAIRTEN2`, `FAIRTEN3` |

Design Load Cases (DLC) — start narrow, expand later:

| Set | Wind | Wave | Purpose |
|---|---|---|---|
| A | NTM @ 8, 11, 15, 20 m/s; 6 seeds each | JONSWAP correlated | Baseline TE(wind→resp), TE(wave→resp) |
| B | Same | Decoupled wave (independent seeds) | Disentangle wind vs wave contribution |
| C | LHS over structural params (Phase 5) | Fixed env seed | Param sensitivity ensemble |

### Hydro-evaluation pipeline (locked 2026-05-13)

The IEA-15 OpenFAST deck uses pure potential-flow (WAMIT) for the platform
— all geometry of the 7 substructure variables is baked into the WAMIT
`.hst/.1/.3` files. Geometry sweeps therefore cannot be done by editing
OpenFAST inputs alone. Pipeline chosen: **RAFT + OpenFAST hybrid**
(mirrors [[sources/jeon-2025]] split):

```
LHS / Saltelli on 9 vars
        │
        ▼
   ┌────────┐   fast frequency-domain coupled aero-hydro-servo-elastic
   │  RAFT  │   surrogate. Sweeps all 9 vars per design point.
   └───┬────┘   Stats produced: max, std, DEL, mean per response channel.
       │
       ▼
   Sobol-S1/ST + KSG-MI on the RAFT ensemble (Phase 5 first cut)
       │
       ▼
   Pick ≤ ~20 winners (top-Sobol / top-MI designs + the
   predecessor's Case_03 equivalent) for OpenFAST validation
       │
       ▼
   ┌──────────┐   OpenFAST time-domain DLC matrix (DLC sets A + B).
   │ OpenFAST │   For env-→response TE (Phase 4) — RAFT cannot do TE,
   └──────────┘   only OpenFAST gives the time series.
       │
       ▼
   Phase 4 TE + AIS + Granger baseline on the validation runs.
   Final causal graph combines RAFT-Sobol/MI edges + OpenFAST-TE edges.
```

**Why this split**:
- A 1000-point Sobol ensemble on the full IEA-15 OpenFAST deck would
  require re-meshing + re-running WAMIT per design point — infeasible.
- RAFT is the predecessor's chosen surrogate; preserving it gives
  direct continuity and a cross-check (RAFT-RL Case_03 vs RAFT-Sobol).
- OpenFAST is reserved for TE (which needs time-series) and validation
  of RAFT-screened winners, exactly as [[sources/jeon-2025]] does.

[[entities/raft]] *(stub — to expand)* is in `repos/WEIS/` already.

### DLC matrix (OpenFAST validation half only)

Design Load Cases (DLC) — start narrow, expand later:

| Set | Wind | Wave | Purpose |
|---|---|---|---|
| A | NTM @ 8, 11, 15, 20 m/s; 6 seeds each | JONSWAP correlated | Baseline TE(wind→resp), TE(wave→resp) |
| B | Same | Decoupled wave (independent seeds) | Disentangle wind vs wave contribution |
| Predecessor-DLC1.6 | NTM V=11 m/s, 6 seeds | SSS Hₛ=8.3, Tₚ=12.95 | Continuity with [[sources/jeon-2025]] validation |

DLC set C from the earlier plan version (LHS over structural params) is
absorbed into the RAFT half above.

### Tooling

> ⚠️ Production runs go on the 65-core Linux server, **not** locally —
> see §Compute target and [[SERVER_DEPLOYMENT]]. The driver flags below
> are reference; the canonical entry point is `python pipeline.py`.

- **RAFT** (frequency-domain coupled solver) for Phase 5 ensemble —
  available via `repos/WEIS/` install. Driver: `sims/run_raft_lhs.py`.
- **TurbSim** (bundled with OpenFAST) for wind fields (validation half).
- **HydroDyn** native JONSWAP for irregular waves (validation half).
- Driver: `sims/run_campaign.py` templates `.fst` / `HydroDyn.dat` /
  `ElastoDyn.dat`, launches OpenFAST in parallel via
  `concurrent.futures`, stores outputs under `sims/<case_id>/`.
- Reuse WEIS' `weis.aeroelasticse` driver (preferred; gives RAFT + OpenFAST
  in one framework, mirrors predecessor).
- **Templating gotchas for r-test-derived `.fst` decks** (discovered
  2026-05-14, validated end-to-end on `sims/case-iea15-real/`):
  (a) ServoDyn `DLL_FileName` ships as the Linux CI path
  `/home/runner/miniconda3/envs/test/lib/libdiscon.so` — templater must
  rewrite to the local Windows ROSCO DLL absolute path
  (`anaconda3/envs/te-fowt/Lib/site-packages/rosco/lib/libdiscon.dll`).
  (b) Paired `wind.inp` ships with `GridHeight = 260` → grid bottom at
  z = 20 m, which sits 5 m above the UMaineSemi tower base at z = 15 m;
  AeroDyn aborts in `IfW_FlowField_GetVelAcc`. Templater must set
  `GridHeight ≥ 270` (use 280 for margin) before TurbSim.

Simulation length: 3600 s per run, drop first 600 s as transient
(OpenFAST DLC sets A/B). Predecessor-DLC1.6 runs: 730 s with first 100 s
discarded for cross-compatibility with [[sources/jeon-2025]].
Sample rate: 0.0125 s (80 Hz, OpenFAST default DT_Out 0.05 s — TBD).

---

## Phase 3 — Data extraction & preprocessing

Script: `analysis/load_runs.py`.

- Parse `.outb` via `openfast_toolbox.io.FASTOutputFile` → pandas.
- Time-align all channels to a common grid; store as **Parquet** in `data/`.
- Per channel: detrend, optional band-pass (e.g., 0.01–0.5 Hz to focus on
  wave/low-freq platform dynamics), z-score normalize.
- Stationarity check: ADF test; if non-stationary, work with first
  differences.
- Decimate to ~5–10 Hz before TE (KSG cost scales badly with N; TE is rate-
  invariant for properly chosen embedding).

---

## Phase 4 — TE on environment → response (the core "causal" step)

Library: **[[entities/idtxl]]** (`pip install idtxl`, JDK 11 backend).
KSG estimator ([[concepts/ksg-estimator]]) per
[[sources/kraskov-2004]]; multivariate inference + automatic embedding
per [[sources/wollstadt-2019]]. Methodology grounded in
[[sources/schreiber-2000]] (see [[papers/schreiber-2000]] for the
derivation re-check).

For each (source, target) pair (e.g., `Wind1VelX → PtfmPitch`):

1. **Pre-processing**: decimate to ~10 Hz; **add 10⁻¹⁰ Gaussian noise**
   to break finite-precision neighbour degeneracy
   (kraskov-2004 §III.A — see [[concepts/ksg-estimator]]).
2. **Embedding**: IDTxl's automatic max-stat / min-stat selection of
   history lengths `k_target`, `l_source`, source-target lag `u`.
   Default `kraskov_k = 4` (kraskov-2004 recommendation `k ∈ [2,4]`).
3. **Bivariate TE**: `TE(source → target)` via `BivariateTE` analyser.
4. **Conditional / multivariate TE**: `TE(wind → resp | wave)` and
   `TE(wave → resp | wind)` via `MultivariateTE` greedy parent-set search.
5. **Significance**: 200+ surrogates via IDTxl `perm_type='circular'`
   (preserves source power spectrum + amplitude distribution exactly,
   destroys directed coupling); `p < 0.05` threshold. Family-wise
   max-statistic correction over candidate sources (per
   [[sources/wollstadt-2019]]). True IAAFT ([[sources/schreiber-2000]]
   §IV) is the publication-baseline upgrade path — equivalent spectrum
   preservation but requires an external surrogate generator and a
   manual hook into IDTxl. Decision rationale + IDTxl native options
   in [[concepts/surrogate-significance]].
6. **Effect-size normalisation**:

   $$
   \text{TE}_\text{frac} = \frac{\text{TE}(X \to Y)}{H(Y_t) - \text{AIS}(Y)}
   $$

   where `AIS(Y) = I(Y_t ; Y_{t-1}^{(k)})` is the **Active Information
   Storage** (Lizier 2012). Interpretation: *fraction of externally-driven
   predictability of `Y_t` that comes from `X`*. Computed from
   [[entities/idtxl]] `ActiveInformationStorage` analyser using the same
   `k_target` embedding. Sharper than dividing by `H(Y_t)` alone because
   it removes the part `Y` predicts about itself — see
   [[papers/wollstadt-2019]] §"Surprise 2".

Outputs per case:
- A directed weighted graph (NetworkX) of significant TE links, edge
  weight = `TE_frac`.
- Tables ranking which env channel drives which response, with CIs.

### Mandatory baseline comparisons (publication requirement)

Every TE result is reported alongside two linear-method baselines so that
the value of nonlinear / directional TE is **demonstrated**, not asserted.

Per [[papers/wollstadt-2019]] §"Surprise 1", both baselines come from the
**same IDTxl pipeline** with different estimators — an apples-to-apples
comparison where the only thing changing is the CMI estimator, not the
parent-set search or surrogate test:

1. **Magnitude-squared coherence** `γ²(f)` — frequency-domain linear
   dependence, symmetric, via `scipy.signal.coherence`. Establishes the
   linear ceiling. (Different framework; can't unify with IDTxl.)
2. **Conditional Granger causality** — directional but linear, via
   IDTxl `MultivariateTE` analyser with `cmi_estimator='JidtGaussianCMI'`.
   Equivalent to classical Granger (Geweke 1982) by virtue of the
   Gaussian estimator's closed-form CMI; same parent-set search and
   surrogate test as the KSG version.

Per (source, target) pair we emit:

| Method | Direction | Significant? | Magnitude |
|---|---|---|---|
| Coherence (peak in 0.01–0.5 Hz band) | sym | y/n | γ²_max |
| Bivariate Granger (IDTxl + Gaussian) | X→Y | y/n | I_Gauss (nats) |
| Conditional Granger | X→Y \| Z | y/n | I_Gauss (nats) |
| Bivariate TE (IDTxl + KSG) | X→Y | y/n | TE_frac |
| Conditional TE (IDTxl + KSG) | X→Y \| Z | y/n | TE_frac |

The "TE catches what linear misses" story lives in the cells where TE
returns significant and Granger does not. The "TE confirms linear" story
lives in cells where both agree — also publication-relevant, since it
validates the embedding.

Sanity checks:
- TE(resp → wind) should be ~0 (no back-action on environment) — if not,
  embedding is wrong. The same IDTxl-Granger pipeline should also show
  ~0 in this direction (cross-check on embedding).

### Methodological extension — ensemble TE across seeds (Wollstadt 2014)

Our DLC sets are by construction multi-realisation ensembles: 6 seeds
per (DLC, wind-speed) bin, each a draw from the same NTM + JONSWAP / SSS
generative process. Wollstadt et al. 2014 (*"Efficient transfer entropy
analysis of non-stationary neural time series,"* PLOS ONE 9(7) e102833)
introduced **ensemble TE** specifically for repeated-trial designs of
this shape: pool the realisations as one estimator instead of averaging
per-trial TE estimates.

For us this gives:
- **Higher effective sample size**: N_eff scales with `seeds × samples`,
  not `samples` — sharper significance against the surrogate null.
- **Robust to within-run non-stationarity**: assumes stationarity *across*
  realisations rather than *within* a single 1-hr run, which is a much
  weaker requirement.
- **Cleaner per-DLC TE matrix**: one value per (source, target, DLC bin)
  instead of one per (source, target, DLC bin, seed), simplifying the
  conditional-TE contrast figure for DLC-A vs DLC-B (H3 in
  [[open-questions]] Q8) and the publication-baseline comparison table.

Implementation route: IDTxl natively supports replicated data via the
`replications` axis on `Data`. The refactor is to stack the 6 seeds'
decimated time series along the replication axis in `te_pipeline.py`,
then call `BivariateTE` / `MultivariateTE` once per (source, target,
DLC) cell instead of per (source, target, DLC, seed). No new dependencies.

**Decision rule** ([[open-questions]] Q10): adopt ensemble TE if the
per-seed Phase 4 results show seed-to-seed TE variance large enough that
the per-seed approach is statistically weak (e.g., one seed significant,
five not). Otherwise keep per-seed-then-aggregate and treat ensemble TE
as a robustness check.

**Publication framing upgrade**: ensemble adoption shifts the
methodological narrative from "TE *applied to* FOWT" to "TE *methodology
extended to* FOWT seed ensembles" — same Wollstadt-group lineage as our
existing IDTxl base, direct citation chain to Wollstadt 2014. This is a
genuine methodological contribution (FOWT TE papers to date treat seeds
independently) and is a Wind Energy Science strengthening move beyond
the three listed in §"Publication strategy".

---

## Phase 5 — Causal effect of structural parameters

**Decision:** TE does not directly apply to constants-per-run, so we use
**Sobol + MI** (option 5a + 5c):

- **5a — Sobol sensitivity:** `SALib` Saltelli sample on parameters →
  response summary statistics (std, DEL, max, mean). Reports first-order
  `S1` and total `ST` indices per (parameter, response) pair. This is the
  engineering-standard answer.
- **5c — Information-theoretic ranking:** Mutual information `I(param ;
  response_stat)` across the same LHS / Saltelli ensemble. Provides a
  TE-spirit nonlinear companion ranking. Estimator: KSG MI from IDTxl.

Both methods consume the **same parameter sweep ensemble**, so we only run
the simulation campaign once. Results merged into a per-parameter table:
`{param, response, S1, ST, MI, p_value}`.

**Parameter sweep list** ([[open-questions]] Q2 — **locked 2026-05-13**
via [[sources/jeon-2025]] + IEA-15 baselines recovered from
`repos/IEA-15-240-RWT/WT_Ontology/IEA-15-240-RWT_VolturnUS-S.yaml` and
`*_MoorDyn.dat`):

| # | Variable | Symbol | Baseline (IEA-22, predecessor) | Baseline (IEA-15, primary) |
|---|----------|--------|-------------------------------|----------------------------|
| 1 | Main column diameter | `D_MCol` | 12.0 m | **10.0 m** |
| 2 | Offset column diameter | `D_OCol` | 12.5 m | **12.5 m** |
| 3 | Offset column radius (spacing) | `R_MO` | 65.0 m | **51.75 m** |
| 4 | Pontoon diameter (equiv. circular) | `D_Pt` | 10.0 m | **9.6148 m** (≡ rect 12.5 × 7.0) |
| 5 | Pontoon height | `H_Pt` | 8.0 m | **7.0 m** |
| 6 | Freeboard | `H_FB` | 15.0 m | **15.0 m** |
| 7 | Draft | `H_Draft` | 25.0 m | **20.0 m** |
| 8 | Mooring axial stiffness | `EA` | TBD | **3.27 × 10⁹ N** |
| 9 | Mooring unstretched length | `L_u` | TBD | **850 m** |

Vars 1–7 are the predecessor's substructure-geometry decision variables.
Vars 8–9 are added by this project so the causal graph can disentangle
the predecessor's Case_03 fairlead-tension trade-off into geometry-driven
vs mooring-driven components. See [[entities/iea-15mw-volturnus-s]]
§"Substructure geometry" and §"Mooring properties" for full provenance.

**LHS / Saltelli sample range** (locked 2026-05-13): **±20 % around the
IEA-15 baseline** per variable. Concrete bounds:

| # | Symbol | −20 % | Baseline (IEA-15) | +20 % |
|---|--------|-------|-------------------|-------|
| 1 | `D_MCol` | 8.00 m | 10.00 m | 12.00 m |
| 2 | `D_OCol` | 10.00 m | 12.50 m | 15.00 m |
| 3 | `R_MO` | 41.40 m | 51.75 m | 62.10 m |
| 4 | `D_Pt` | 7.692 m | 9.6148 m | 11.538 m |
| 5 | `H_Pt` | 5.60 m | 7.00 m | 8.40 m |
| 6 | `H_FB` | 12.00 m | 15.00 m | 18.00 m |
| 7 | `H_Draft` | 16.00 m | 20.00 m | 24.00 m |
| 8 | `EA` | 2.616 × 10⁹ N | 3.27 × 10⁹ N | 3.924 × 10⁹ N |
| 9 | `L_u` | 680 m | 850 m | 1020 m |

**Constraint handling**: the predecessor's geometric constraints
(`D_OCol > D_Pt`, `H_Pt > 0.5·D_Pt`, `H_Draft > 0.5·D_Pt + H_Pt`)
will be **violated by some samples in this ±20 % box** — e.g.
`D_OCol = 10` (min) and `D_Pt = 11.538` (max) violates `D_OCol > D_Pt`.
Approach: evaluate RAFT on every Saltelli sample; mark
constraint-violating points as a separate "infeasible" category in the
results table (analogous to predecessor's reward = −100). Sobol indices
are then computed on the *feasible* subset, with the fraction-infeasible
reported as a diagnostic. Resonance constraints (vars in time-domain)
get the same treatment at the OpenFAST validation step, not in RAFT.

**Hydro-evaluation method** (locked 2026-05-13): **RAFT + OpenFAST hybrid**
— RAFT runs the 9-variable Saltelli ensemble (Phase 5 Sobol/MI); OpenFAST
validates the top-Sobol/top-MI winners and supplies the time series for
Phase 4 TE. See Phase 2 §"Hydro-evaluation pipeline" for the diagram.

Variables 1–7 are the predecessor's substructure-geometry decision
variables. Variables 8–9 are added by this project so the causal graph
can answer the Q9 lead question: *is the fairlead-tension penalty in
Case_03 caused by geometry or by under-sized mooring?* — see
[[sources/jeon-2025]] §"Validation result" trade-off table.

**Open**: IEA-15 VolturnUS-S baselines for variables 1–7 to be extracted
from [[entities/iea-15mw-volturnus-s]] before Phase 2 templating.
Per-variable LHS ranges default to **±20 %** around baseline unless the
predecessor's original bounds are recovered.

**Response summary statistics** ([[open-questions]] Q3): `max`, `std`,
DEL, `mean` per channel. `max` keeps continuity with [[sources/jeon-2025]];
`std` and DEL are the fatigue-relevant additions where TE/MI on summaries
becomes informative.

---

## Phase 6 — Reporting

- Combined **causal graph**: env channels (TE edges) + parameters (Sobol/MI
  edges) → responses, with edge weights = normalized TE / Sobol total index.
- Per-response narrative: top 3 drivers, conditional TE breakdown, surrogate
  CI.
- **Concrete engineering takeaway** (publication requirement — see §Publication
  strategy below). **Lead candidate (2026-05-13)**: explain the
  [[sources/jeon-2025]] Case_03 trade-off — mass −21.5 % but FAIRTEN
  +19 / +59 / +57 %, heave +32 %. Use conditional `TE(wave → FAIRTEN | wind)`
  vs `TE(wind → FAIRTEN | wave)` plus Sobol-`ST` on (geometry, mooring `EA`,
  mooring length) to disentangle wave-driven (surge-coupled) vs wind-driven
  (controller-mediated) contributions. Recommendation pathway: should the
  next optimisation iteration expand decision variables to include mooring,
  retune controller, or change the column-spacing constraint? Sobol on
  geometry alone cannot answer; this is the analytical gap our work fills.
- Markdown reports in `reports/`, auto-rendered figures in `reports/figs/`.

---

## Publication strategy

Honest assessment: as scoped, the project is **comfortably publishable as a
methods workshop paper** (TORQUE, EERA DeepWind, ASME OMAE) and **reachable
for *Wind Energy Science* or *Marine Structures*** with the framing below.
Not yet top-tier journal as-is — needs the strengthening moves listed.

### Working in the project's favour

- **Conditional TE on coupled wind+wave for FOWT is a genuine niche**.
  Standard TE on wind-turbine SCADA exists; conditional TE that
  systematically disentangles wind from wave for floating-platform response
  is much less explored.
- **Hybrid TE + Sobol/MI causal graph framing**. Most FOWT causality papers
  do one or the other; combining both into a single weighted directed graph
  (env edges from TE, parameter edges from Sobol `ST`) is the methodological
  novelty.
- **DLC-A vs DLC-B contrast as built-in validation**. Coupled vs decoupled
  wind/wave seeds give a direct check: conditional TE should converge to
  bivariate TE in DLC-B and diverge in DLC-A. Reviewer-friendly figure.

### Working against the project

- **Sobol on FOWT is well-trodden** (NREL, WEIS, Robertson et al.). If
  Sobol is the headline, it will not publish. Keep it as the *companion* to
  the TE story, not the lead.
- **No baseline comparison kills it**. "We applied TE, found wind drives
  pitch" is not enough — every reviewer will ask why not coherence /
  Granger. Phase 4 must include both baselines.
- **Single platform, sim-only**. Limits the generalisability claim.
- **Missing a "so what"**. Engineering-journal reviewers want a *design*
  takeaway, not a ranking. Phase 6 must close with a specific design
  decision the analysis would change.

### Strengthening moves to lift workshop → journal

1. **Baselines**: every TE plot ships alongside linear coherence and
   conditional Granger causality. Show explicitly what nonlinear TE catches
   that linear methods miss (and where they agree — agreement also strengthens
   the TE result). See Phase 4 update.
2. **Hypothesis-driven setup**: predict the TE / Sobol rankings *ahead of
   time* from FOWT physics (wave→heave dominant at 0.1–0.3 Hz; wind→pitch via
   rotor thrust at low-freq; mooring `EA` → surge std monotonic; etc.), then
   verify. Confirmed predictions read stronger than discovered correlations.
3. **One concrete engineering takeaway** (Phase 6 requirement above) —
   pick a design decision where the causal-graph answer differs from a
   coherence- or Sobol-only answer.
4. **Open code + reproducible OpenFAST decks** in a public repo. Material
   for *Wind Energy Science* acceptance.
5. **(Stretch) Multi-platform**. Adding [[entities/oc4-deepcwind]] *(stub)*
   or OC3 Hywind comparison strengthens the generalisability claim — see
   Q5 in `wiki/pages/open-questions.md`.
6. **(Stretch) Experimental anchor**. Compare a TE result against
   OC6 model-test data where available.

### Tracked publication-positioning questions

In `wiki/pages/open-questions.md`:
- Q7 — target venue (workshop vs WES vs Marine Structures)
- Q8 — pre-registered hypothesis predictions
- Q9 — concrete design-decision case study

---

## Critical files / scripts to create

| Path | Purpose |
|---|---|
| `analysis/build_vault.py` | RST→MD conversion + Obsidian vault scaffolding |
| `sims/run_campaign.py` | Templating + parallel OpenFAST execution |
| `analysis/load_runs.py` | `.outb` → Parquet + preprocessing |
| `analysis/te_pipeline.py` | IDTxl bivariate / conditional TE + AIS + Granger-via-estimator-swap + surrogates |
| `analysis/baselines.py` | Coherence (scipy) wrapper; Granger comes from `te_pipeline.py` with `JidtGaussianCMI` |
| `analysis/sensitivity.py` | SALib Sobol/Morris + MI-based ranking |
| `analysis/causal_graph.py` | Build & plot combined causal graph |
| `environment.yml` / `requirements.txt` | Pinned deps (idtxl, SALib, openfast_toolbox, pandas, jpype1) |

`te_pipeline.py` structure (post-ingest, per [[papers/wollstadt-2019]]):

```python
load_runs()            # Parquet from data/
jitter(scale=1e-10)    # kraskov-2004 §III.A neighbour-degeneracy fix
decimate_to(rate=10)   # anti-alias + downsample for KSG tractability
run_bivariate_te()     # IDTxl BivariateTE, JidtKraskovCMI
run_mvte()             # IDTxl MultivariateTE, JidtKraskovCMI (conditional)
run_granger()          # IDTxl MultivariateTE, JidtGaussianCMI = baseline
run_ais()              # IDTxl ActiveInformationStorage (effect-size denominator)
build_graph()          # NetworkX, edge weight = TE / (H(Y) − AIS(Y))
```

## Tooling install list

- OpenFAST 3.5+ binary (Windows) — get from openfast/openfast Releases.
- Python 3.11 in a fresh conda env: `idtxl`, `jpype1` (IDTxl needs JDK 8+),
  `openfast_toolbox`, `SALib`, `pandas`, `pyarrow`, `networkx`,
  `matplotlib`, `scipy`, `statsmodels`, `jinja2`.
- JDK 11 for IDTxl's JIDT backend.
- Obsidian (already a desktop app on your side).
- `pandoc` for RST → MD.

## Verification

End-to-end test before scaling up:
1. Run **one** OpenFAST case from `r-test` (5MW_Land_BD_DLL_WTurb) — confirm
   `analysis/load_runs.py` parses it.
2. Run a known-answer TE test: synthetic AR(1) chain `X → Y` with known
   coupling, verify IDTxl recovers `TE(X→Y) > 0` and `TE(Y→X) ≈ 0`.
3. Run **one** IEA-15MW case (1 wind seed, 1 wave seed) — verify TE pipeline
   produces non-zero `TE(Wind1VelX → PtfmPitch)` with p<0.05 vs surrogates.
4. Run a 3-point Sobol sample on mooring stiffness — verify SALib gives a
   non-zero total-order index on `PtfmSurge` std.

Only after all four pass do we launch the full campaign.

---

## Execution order on plan approval

Step 0 (initial approval) authorised only **Phase 1 scaffolding**
(folders + read-only repo clones). All upstream gates are now closed:

1. ✅ **Response channels** — 9 channels locked 2026-05-13 via
   [[sources/jeon-2025]] (see Phase 2 §"Response channels"). Q1 in
   [[open-questions]] resolved.
2. ✅ **Structural parameters to sweep** — 9 parameters locked
   2026-05-13 via [[sources/jeon-2025]] + project additions
   (mooring `EA`, `L_u`); IEA-15 baselines and ±20 % LHS ranges
   tabulated in Phase 5 (see "Parameter sweep list" and "LHS / Saltelli
   sample range" tables). Q2 in [[open-questions]] resolved.

Validation gate (all closed by 2026-05-15):

- ✅ Toolchain install — OpenFAST v4.2.0 + TurbSim in
  `miniconda3/envs/openfast_env`; ROSCO 2.10.1, openfast_toolbox,
  pCrunch, WEIS in `anaconda3/envs/te-fowt`; JDK 11 + IDTxl bypass
  in `te-fowt`.
- ✅ Verification case 1 — `5MW_Land_BD_DLL_WTurb` parse smoke test
  (openfast_toolbox + load_runs.py); Parquet round-trip exact.
- ✅ Verification case 2 — synthetic AR(1) TE recovery (IDTxl + KSG + JIDT);
  forward TE significant, reverse `≈ 0`.
- ✅ Verification case 3 — both halves. Simulation: one
  IEA-15-UMaineSemi OpenFAST run completed 2026-05-14 (300 s,
  22 MB `.outb`). TE analysis: `TE(Wind1VelX → PtfmPitch) =
  +0.0052 nats, p=0.005` on that `.outb` (2026-05-15, with the
  tuned settings: `max_lag=30`, 5 Hz decimation, circular-shift
  surrogates × 200). H1 first-cut PASS. See
  [[validation/case-3-iea15-single-case-te]].
- ✅ Verification case 4 — 3-point RAFT mooring-EA sweep;
  `|surge_avg|` monotonic in `EA`.

Phase 2 prep — three blockers from 2026-05-15 defensibility audit
(all closed 2026-05-15, see [[log]] entries of that date):

- ✅ Methodology reconciliation — surrogate-significance.md +
  scripts updated to use `perm_type='circular'` (IDTxl native;
  spectrum-preserving null).
- ✅ `run_raft_lhs.py` v2 — 9 vars, CLI N, per-eval checkpoint,
  parallel pool. Phase 5 N=64 production run done; N≥256 deferred
  to server.
- ✅ `run_iea15_single.py` → `run_campaign.py` — per-case IDs,
  no-clobber output dirs, env-var conda paths. DLC-1.6 6-seed
  batch completed locally; DLC-A and DLC-B deferred to server.

Server deployment + production campaign — **DONE** (2026-05-18 → 05-26;
see [[log]] entries of those dates):

- ✅ Repo bootstrapped, pushed to GitHub, cloned + env-built on the
  65-core server ([[SERVER_DEPLOYMENT]]); 3 production bugs patched.
- ✅ Phase 2 — all 54 OpenFAST cases done (6 DLC-1.6 + 24 DLC-A +
  24 DLC-B, 1 h each), pulled back to `sims/`.
- ✅ Phase 5 — N=256 Sobol done (2816 evals, 971 feasible). L_u-dominates
  / EA-negligible pattern holds; CIs ~halved vs N=64.
- ✅ Phase 4 — **bivariate first pass** done (`reports/te_table.parquet`,
  54 cases) but with **scope-reduced** settings: 2 Hz, `max_lag=60`,
  `n_perm=50`, `--no-conditional --no-granger`.
- ✅ Hypotheses H1–H6 scored vs results — `reports/hypothesis-scorecard.md`.
- ✅ Reporting through ver07 + Phase 6 figures (`reports/figs/`).

Now active — **Phase 4 full-settings rerun** (journal-tier gap closure;
decided 2026-06-01). The first pass left three publication blockers, all
closed by one rerun:

- ⏳ **Granger baseline** (Gap 1) — mandatory per §Publication strategy
  ("no baseline comparison kills it"); skipped by `--no-granger`.
- ⏳ **Conditional TE** (Gap 2) — the project's headline novelty;
  skipped by `--no-conditional`. Unblocks H3 + rigorous H5b.
- ⏳ **Re-test H1 / H6 nulls at `max_lag=150`** — first pass used
  `max_lag=60` / 2 Hz, shorter than the 2026-05-20 slow-drift physics
  correction requires. The "ROSCO rejects wind" (H1-null) narrative is
  only defensible if the null survives the corrected embedding.

Launcher: `analysis/run_phase4_full.sh` (server; conditional + Granger +
AIS + coherence ON, `max_lag=150`, 5 Hz, `n_perm=200`; writes
`te_table_full.parquet`, leaves the first-pass table intact). Sequence:
timing probe on one case → sharded run + merge → pull back → re-score →
controller-off Q11 run if H1 null holds → H6 windowed-TE driver →
finalize report ver08.

### Phase 1 scaffolding actions (executed 2026-05-12)

1. Created the directory tree shown above, including `wiki/raw/*` and
   `wiki/pages/*` subfolders.
2. Shallow-cloned the 7 reference repos into `repos/` (~1.6 GB).
3. Seeded `wiki/` with 48 pages per the three-layer pattern:
   `wiki/SCHEMA.md`, the 5 special pages (index, log, overview,
   open-questions, wiki-improvement-plan), 9 OpenFAST-module entities,
   1 reference-platform entity, 7 software entities, 6 concept pages,
   4 equation pages, 4 validation-case stubs, and README placeholders
   for `sources/`, `papers/`, `analyses/`, plus each `raw/*` subfolder.
4. Wrote `requirements.txt` (not installed yet).
5. Renamed the original ad-hoc `vault/` to `vault-legacy/` after migration
   verified — kept for reversibility, can be deleted when comfortable.

**Not yet done** (deliberately): pandoc conversion, Python dep install,
OpenFAST binary install, any simulation work.
