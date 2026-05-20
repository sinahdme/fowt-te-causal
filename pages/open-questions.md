---
title: "Open Questions"
type: open-questions
created: 2026-05-12
updated: 2026-05-13
tags: [meta, planning, publication, multi-platform]
---

# Open Questions

Tracked research / decision questions. Status legend:
🟢 open · 🟡 under investigation · 🔵 resolved · ⚪ deferred

---

## 🔵 Q1 — Which OpenFAST output channels are the TE targets?

**Resolved 2026-05-13** via [[sources/jeon-2025]] ingest. The 9 channels
logged in the predecessor RL-optimisation validation campaign are now
the locked TE-target / Sobol-response list:

| Group | Channels |
|---|---|
| Structural loads | `RootMyc1`, `RootMxc1`, `TwrBsMyt` |
| Platform motions | `PtfmHeave`, `PtfmSurge`, `PtfmPitch` |
| Mooring | `FAIRTEN1`, `FAIRTEN2`, `FAIRTEN3` |

These go into the OpenFAST `OutList` block of the `.fst` master deck and
into `analysis/load_runs.py` channel list. **Action**: create
`pages/entities/channel-<name>.md` stubs per [[SCHEMA]] §"Channel-naming
convention" (deferred until Phase 2 templating starts).

---

## 🔵 Q2 — Which structural parameters do we sweep, with what ranges?

**Parameter list locked 2026-05-13** via [[sources/jeon-2025]]. The 7
substructure geometry variables from the predecessor optimisation are
the Sobol/MI sweep parameters:

| # | Variable | Symbol | Baseline (22 MW) |
|---|----------|--------|------------------|
| 1 | Main column diameter | `D_MCol` | 12.0 m |
| 2 | Offset column diameter | `D_OCol` | 12.5 m |
| 3 | Offset column radius (spacing) | `R_MO` | 65.0 m |
| 4 | Pontoon diameter | `D_Pt` | 10.0 m |
| 5 | Pontoon height | `H_Pt` | 8.0 m |
| 6 | Freeboard | `H_FB` | 15.0 m |
| 7 | Draft | `H_Draft` | 25.0 m |

**IEA-15 baselines recovered 2026-05-13** from
`repos/IEA-15-240-RWT/WT_Ontology/IEA-15-240-RWT_VolturnUS-S.yaml` +
`*_MoorDyn.dat` — see [[entities/iea-15mw-volturnus-s]] §"Substructure
geometry" and §"Mooring properties":

| # | Symbol | IEA-15 baseline |
|---|--------|------------------|
| 1 | `D_MCol` | 10.0 m |
| 2 | `D_OCol` | 12.5 m |
| 3 | `R_MO` | 51.75 m |
| 4 | `D_Pt` | 9.6148 m (equiv. circular; rect 12.5 × 7.0 in original Allen 2020) |
| 5 | `H_Pt` | 7.0 m |
| 6 | `H_FB` | 15.0 m |
| 7 | `H_Draft` | 20.0 m |
| 8 | `EA` | 3.27 × 10⁹ N |
| 9 | `L_u` | 850 m |

**Mooring parameters** (vars 8–9) added by project on top of the
predecessor's geometry-only list, so the causal graph can answer:
*is the fairlead-tension penalty in [[sources/jeon-2025]] Case_03
caused by geometry or by under-sized mooring?* — Q9 lead candidate.

**LHS ranges locked 2026-05-13**: **±20 % per variable around baseline**.
Concrete bounds in [[PLAN]] Phase 5 §"LHS / Saltelli sample range".
Constraint-violating samples (e.g. `D_OCol < D_Pt`) are flagged as
infeasible, mirroring the predecessor's reward = −100 treatment;
Sobol/MI indices computed on the feasible subset.

**Hydro-evaluation method locked 2026-05-13**: **RAFT + OpenFAST hybrid**
— RAFT for the 9-variable Saltelli ensemble; OpenFAST for top-winner
validation + Phase 4 TE time series. Direct continuity with
[[sources/jeon-2025]]'s RAFT→OpenFAST split. See [[entities/raft]] *(stub)*
and [[entities/iea-15mw-volturnus-s]].

**Status**: 🔵 fully resolved — parameter names, IEA-15 baselines, LHS
ranges, and hydro-evaluation method all locked. Phase 5 can be templated.

---

## 🟡 Q3 — What summary statistics of each response feed the Sobol/MI analysis?

**Predecessor used `max`** ([[sources/jeon-2025]] slide 13 comparison
table). For continuity with the Case_03 validation we retain `max`.

**Project addition**: also compute `std`, damage-equivalent load (DEL),
and `mean`. Rationale: TE/MI on `std` and DEL is more meaningful for
fatigue drivers — and this is exactly the analytical gap our work fills
on top of the predecessor's `max`-only optimisation.

**Still open**:
- **Frequency-band powers** (low-freq vs wave-freq vs 1P/3P)? Multiplies
  Sobol/MI cells but is more informative for fatigue. Lean **yes** for
  mooring tensions and tower base moment, **no** for max-load channels.

**Status**: 4-stat set (`max`, `std`, `DEL`, `mean`) locked; band-power
extension pending.

---

## 🟢 Q4 — Embedding & decimation strategy for IDTxl

OpenFAST default `DT_Out` is 0.05 s (20 Hz). KSG cost scales badly with N.
We will decimate to 5–10 Hz pre-TE.

**Open**: should embedding lengths be set per channel-pair (IDTxl
auto-selection) or fixed globally for cross-case comparability?

Trade-off: per-pair gives best estimates but TE values aren't directly
comparable across pairs; fixed gives comparability but may underfit some
pairs.

**Status**: open — revisit during Phase 4 calibration on [[validation/case-3-iea15-single-case-te]].

---

## 🟡 Q5 — Single-platform vs multi-platform comparison

**Partially resolved 2026-05-13** via [[sources/jeon-2025]]:

- **Primary platform**: [[entities/iea-15mw-volturnus-s]] (locked) —
  more validation literature, OC6 anchor.
- **Second platform**: **IEA-22MW-RWT-Semi** (locked-in) — gives direct
  continuity with the project owner's predecessor RL-optimisation work
  (Jeon 2025). Same UMaine-semi family scaled up to 22 MW; multi-tool
  reference (HAWC2 / QBlade / WISDEM cross-checks).
  [[entities/iea-22-280-rwt-semi]] *(stub)* — `git clone https://github.com/IEAWindTask37/IEA-22-280-RWT`
  when Phase 2 sims start.

**Status**: deferred *execution* to after IEA-15 end-to-end success
(scope discipline per [[PLAN]] §"Publication strategy" — first paper on
IEA-15, IEA-22 results as the multi-platform extension figure).

**Still alternative second platforms** (would replace IEA-22 only if Q9
reframes the publication around platform-archetype contrast rather than
scale-up):
- Spar — OC3-Hywind ([[entities/oc3-hywind]] *(stub)*). Starkest TE
  contrast vs semisub.
- Other semisub — OC4 DeepCwind ([[entities/oc4-deepcwind]] *(stub)*).
  Older, heavily cited.

---

## 🟢 Q6 — Are wind and wave correlated in the chosen DLCs?

DLC set A uses correlated wave seeds; set B uses decoupled. Real ocean
conditions exhibit wind-wave correlation (wind sea). For the TE
analysis, this matters because correlated env channels need *conditional*
TE to disentangle.

**Status**: covered by DLC set design (A vs B); flagged here so it isn't
forgotten when interpreting results.

---

## 🟢 Q7 — Target publication venue

**Why it matters**: scoping decisions (multi-platform? experimental anchor?
how much baseline detail?) flow from the venue. See [[PLAN]]
§"Publication strategy" for the assessment.

**Candidates**, ordered by reach:
1. **Workshop / conference** — TORQUE 2026, EERA DeepWind 2027, ASME
   OMAE 2027. Lowest bar; current scope already qualifies.
2. **Wind Energy Science** (open-access, methodology-friendly) — reachable
   with the strengthening moves below (Q8 + baselines + a design takeaway
   per Q9). Best fit.
3. **Marine Structures / Ocean Engineering** — viable if framed around
   mooring / platform causal analysis.
4. **(Stretch) Renewable Energy / Applied Energy** — needs experimental
   anchor or multi-platform.

**Status**: open. Pick venue early — affects DLC matrix size and figure
budget.

---

## 🔵 Q8 — Hypothesis predictions (pre-registered list)

**Pre-registered 2026-05-13** — predictions locked before any campaign
simulation runs. Confirmed predictions read stronger than discovered
correlations; this list is the publication's defense against p-hacking
accusations. **No edits after the campaign launches.**

Two structural changes from the original draft:
- Original H5 referenced controller gains, but the locked Phase 5 sweep
  ([[PLAN]] §"Parameter sweep list") includes only **substructure
  geometry + mooring** (9 vars). H5 is therefore re-targeted to the
  fairlead-tension trade-off surfaced by [[sources/jeon-2025]] —
  more directly testable and aligned with the Q9 lead case study.
- H4 expanded to include mooring `L_u` (variable 9) and to bound the
  geometry-variable contribution.

| # | Pre-registered prediction | Method that confirms |
|---|---|---|
| **H1** | `TE(Wind1VelX → PtfmPitch)` significant (p < 0.05) in both DLC-A and DLC-B; `TE(PtfmPitch → Wind1VelX) ≈ 0` (no back-action sanity check) | [[validation/case-3-iea15-single-case-te]] |
| **H2** | `TE(Wave1Elev → PtfmHeave)` significant and dominant within the 0.1–0.3 Hz wave band; bivariate Granger and coherence `γ²(f)` agree at the peak | Phase 4 spectral break-down + baselines |
| **H3** | Conditional `TE(wind → PtfmPitch \| wave)` ≈ bivariate `TE(wind → PtfmPitch)` in DLC-B (decoupled wind/wave seeds), but < 80 % of bivariate in DLC-A (correlated). I.e. "conditional shrinks more when environment is correlated" — direct demonstration that conditional TE is doing real work | DLC-A vs DLC-B contrast |
| **H4** | Mooring contribution dominates platform surge variance: Sobol-`ST(EA \| std(PtfmSurge)) > 0.5` AND `ST(L_u \| std(PtfmSurge)) > 0.2`; aggregate geometry-variable contribution `ΣST(D_*, R_MO, H_*) < 0.3` | [[validation/case-4-sobol-3pt-mooring-ea]] → Phase 5 full Saltelli |
| **H5** | **Replaces controller-gain prediction**. Fairlead-tension trade-off explained by mooring sizing + wave drive: (a) `ST(EA \| std(FAIRTEN1)) > ST(geometry-combined \| std(FAIRTEN1))`; (b) conditional `TE(wave → FAIRTEN1 \| wind) > 2 × TE(wind → FAIRTEN1 \| wave)`. I.e., fairlead-tension is wave-driven, not wind-driven, and mooring sizing dominates over substructure geometry | Phase 5 (Sobol) + Phase 4 (conditional TE) — this is the Q9 lead case study |
| **H6** | `TE(wave → PtfmPitch)` local-in-time PSD peaks at the platform pitch eigenfrequency 0.03–0.04 Hz (VolturnUS-S design value ≈ 0.0345 Hz); coherence `γ²(f)` shows the same peak; Granger baseline misses the second harmonic if any | Phase 4 spectral break-down |

**Rules of pre-registration** (applied to this analysis):
- The predictions above are committed *before* the Phase 2 campaign
  launches. Any reformulation that affects what counts as "confirmed"
  invalidates pre-registration and must be flagged in the publication
  with the original text reproduced.
- Hypotheses are evaluated as `confirmed` / `partially-confirmed` /
  `not-confirmed` per the explicit numeric thresholds above.
  `not-confirmed` is reported with equal prominence — that's the
  scientific value of pre-registration.
- Anything we learn post-hoc that wasn't in this list is reported as
  **exploratory**, not confirmatory.

Methodological clarifications:
- **DLC-A vs DLC-B** is the conditional-TE-validating contrast in
  [[PLAN]] Phase 2 §"DLC matrix" — A uses correlated wind/wave seeds,
  B uses decoupled seeds.
- **Local-in-time PSD** for H6 means: estimate `TE(wave → pitch)` per
  short window (e.g., 60 s overlapping), then Fourier-transform the
  resulting TE(t) time series. Distinct from the bivariate-TE single
  number per (source, target) pair.

**Status**: 🔵 resolved — locked 2026-05-13 ahead of Phase 2 campaign.

---

## 🟡 Q9 — Concrete design-decision case study

**Why it matters**: the engineering "so what" required for journal
acceptance (see [[PLAN]] §"Publication strategy"). The combined
causal graph must change at least one design recommendation versus a
Sobol-only or coherence-only analysis.

**Lead candidate (2026-05-13)** — surfaced by [[sources/jeon-2025]]
slide 13:

> Mass-only optimisation produced Case_03 with mass −21.5 %, but
> fairlead tensions +19 % / +59 % / +57 %, platform heave +32 %,
> pitch +10 %. The mooring was held fixed; the trade-off concentrated
> load into mooring and motion responses.

**Project's analytical contribution**: conditional TE + Sobol on the
same parameter sweep can disentangle the trade-off's mechanism in a way
the predecessor's RAFT-RL framework cannot:

- **Sobol-`ST`(D_OCol, R_MO, H_Draft | std(FAIRTEN))** reveals which
  geometric variable drives the mooring-tension penalty.
- **Conditional `TE(wave → FAIRTEN | wind)` vs `TE(wind → FAIRTEN | wave)`**
  reveals whether the penalty is wave-driven (surge-coupled) or
  wind-driven (controller-mediated).
- **Joint analysis** answers the design question: should the next
  optimisation iteration add mooring `EA` and unstretched length to the
  decision variables (predecessor's own recommendation), or retune
  controller gains, or change the column-spacing constraint? The Sobol-only
  view ranks contributions but cannot separate wave vs controller paths.

**Remaining candidates** (defer; pick a 2nd if Q9-lead doesn't pay off):

- **Tower fatigue path**. Conditional TE may show that part of `TwrBsMyt`
  low-freq variance attributed by Sobol to platform mass is in fact
  controller-mediated. Recommendation: re-tune `PC_KP` before oversizing.
- **Heave-pitch coupling via ballast**. TE may resolve directionality;
  Sobol on a single ballast parameter cannot.

**Status**: lead candidate locked; confirm narrative after Phase 4
baselines on the IEA-15 campaign and the IEA-22 multi-platform run.

---

## 🟡 Q10 — Adopt ensemble TE (Wollstadt 2014) for the per-DLC seed ensemble

**Why it matters**: our DLC sets are *exactly* the use case Wollstadt
et al. 2014 designed ensemble TE for — multiple independent realisations
of the same generative coupling (6 wind/wave seeds per DLC bin, all
nominally drawing from the same NTM + JONSWAP / SSS process). Pooling
the seed ensemble as one estimator instead of averaging per-seed TE
gives:

- **Higher statistical power** — N_eff scales with `seeds × samples`
  instead of `samples`, sharper significance against the surrogate null.
- **Handles within-run non-stationarity** — the OpenFAST 1-hr runs have
  transient + slow drifts the ensemble approach is robust to (assumes
  inter-realisation stationarity, not within-realisation).
- **Cross-DLC comparability** — one TE value per (source, target, DLC
  bin) instead of one per (source, target, DLC bin, seed) makes the
  paper's figures simpler and the conditional-TE contrast (DLC-A vs
  DLC-B per [[PLAN]] Phase 4 H3) sharper.

**Publication angle**: re-frames the paper from "TE *applied to* FOWT"
to "TE *methodology extended to* FOWT seed ensembles." Direct citation
chain to Wollstadt et al. 2014 *"Efficient transfer entropy analysis of
non-stationary neural time series,"* PLOS ONE 9(7) e102833. Same lineage
as our existing IDTxl base ([[papers/wollstadt-2019]]), so the framing
is "we extend the Wollstadt-group ensemble approach from neuroscience
multi-trial designs to engineering DLC ensembles."

**Implementation cost**: IDTxl already supports replicated/multi-trial
data via the `replications` axis on `Data`. Mostly a `te_pipeline.py`
refactor: stack the 6 seeds' decimated time series along the replication
axis, call `BivariateTE` / `MultivariateTE` once per (source, target,
DLC) cell instead of per (source, target, DLC, seed). ~1 day of work,
no new dependencies.

**Status**: 🟡 under investigation. Defer concrete decision until the
current campaign's per-seed Phase 4 results are in — if seed-to-seed
TE variance is large enough that the per-seed approach is statistically
weak, ensemble TE becomes the obvious upgrade. Tracked here so it isn't
lost in the analysis-after-results scramble.

**Related Wibral-group refinements** considered and *not* adopted now:
- *Twin surrogates* (Thiel et al. 2006) — circular-shift surrogates
  ([[concepts/surrogate-significance]]) already preserve the spectrum
  and are sufficient for our 36000-sample runs.
- *Partial information decomposition* (Wibral 2017, unique/shared/
  synergistic) — needs more samples than we'll have per DLC bin to
  estimate stably.
- *Local TE* (Lizier 2008, time-resolved) — H6 already does this via
  "local-in-time PSD of TE(t)"; full local TE machinery is overkill.

---

## 🟡 Q11 — Controller-off comparison to quantify ROSCO's disturbance-rejection contribution

**Why it matters**: a well-tuned controller suppresses the disturbance
from X (wind) before it reaches Y (platform pitch / loads). Bivariate
TE on closed-loop FOWT therefore *underestimates* the physical
wind→response causality and risks reporting `TE → 0` for a real causal
path that the controller is doing its job hiding. Methodology references:

- **Schreiber 2000** TE was defined for open-loop X → Y.
- **Massey 1990** *directed information* extends the framework to systems
  with feedback (Y can influence X's future).
- **Lizier 2014** "Measuring the dynamics of information processing" —
  TE in closed-loop systems requires conditioning on the controller's
  internal state, otherwise spurious bidirectional TE arises from the
  hidden mediator.
- **Wibral et al. 2013** — interaction-delay reconstruction in
  controlled / feedback configurations.

**The proposed contrast**: re-run a single representative DLC bin
(`dlc16` at V=11 m/s, 6 seeds) with **ROSCO disabled** — set
ServoDyn `CompServo=0` (or pin pitch + torque at the rated-condition
fixed point). Compute the same Phase 4 TE pipeline on both versions.

The headline quantity is then:

$$
\Delta\text{TE}_\text{ctrl}(X\to Y)
  = \text{TE}_\text{ctrl-off}(X\to Y) - \text{TE}_\text{ctrl-on}(X\to Y)
$$

interpretable as the **share of (X → Y) causality the controller absorbs
via disturbance rejection**. For wind→pitch this should be substantial
(ROSCO's floating-feedback gain is specifically designed for this).
For wave→heave this should be near zero (controller doesn't act on
heave directly).

**Why this is publishable on its own**: extends TE methodology to
explicitly quantify controller contribution to FOWT response causality.
That's a real methodological contribution to the wind-energy TE
literature, separate from (and complementary to) the per-DLC results.

**Note on bivariate vs conditional**: the cleanest analysis conditions
on ROSCO's pitch-demand signal (`BlPitch1` if available in `.outb`).
That isolates the open-loop residual without re-running OpenFAST.
The controller-off campaign is the "ground truth" against which the
conditional-TE-on-pitch-demand approach can be validated.

**Decision rule**: defer concrete commitment until controller-on Phase 4
results are in. If H5 results (Q9 — fairlead-tension trade-off) show
the controller-mediated path is small / inconclusive, the controller-off
contrast becomes a stronger framing for the paper. If H5 cleanly
resolves with controller-on alone, Q11 becomes an appendix figure
rather than a primary contribution.

**Implementation cost**: 1 DLC bin × 6 seeds × ~95 min wall = ~95 min
of server compute. Trivial relative to the main campaign. Patch:
`run_campaign.py` accepts a `--controller-off` flag that sets
`CompServo=0` and skips the DLL_FileName patch.

**Direction-reversal caveat** (raised by user 2026-05-20):
TE *direction* does NOT reverse for exogenous drivers — `TE(pitch → wind)`
stays ≈ 0 because wind doesn't depend on pitch (this is H1's sanity
check). What gets distorted is the *magnitude* of `TE(wind → pitch)`
and the appearance of spurious bidirectional artifacts from hidden
controller-state mediation. Direction-reversal only appears in genuine
feedback systems where Y can influence X (e.g., wake-aware multi-turbine
control), which isn't our setup.

---

## 🔵 Q12 — Embedding window for slow-drift coupling

**Resolved 2026-05-20** during the ver03 report review (physics audit
of §6.3): the IEA-15 UMaineSemi HydroDyn deck has `DiffQTF = 12`
enabled, so platform-pitch slow-drift dynamics at the pitch eigenfrequency
(~0.0345 Hz, period ~29 s) **are** present in the `.outb` files. The
original `te_pipeline.py` setting `max_lag = 30` covers only 6 s at
the 5 Hz decimated rate — about ⅕ of one slow-drift cycle, far too
short for the KSG embedding to capture wave → pitch coupling at the
slow-drift frequency.

**Fix** (committed 2026-05-20): `TESettings.max_lag` raised to **150
samples (30 s window)**, covering one full slow-drift cycle. CLI default
also bumped. Cost: per-pair KSG estimator runtime scales roughly with
max_lag during the max-stat embedding search — expect ~3–5× slower
per-pair than at max_lag = 30, balanced by the scope-reduction options
under Q7.

**Why this matters**: H6 specifically predicts a TE(wave → pitch)
local-in-time PSD peak at the pitch natural frequency. Under the old
max_lag = 30, KSG would systematically miss this coupling because the
embedding cannot resolve the 30-s temporal structure. The May 15
case-iea15-real H1 first-cut PASS (`TE = +0.0052 nats, p = 0.005`) was
on a short 300 s NTM run where the slow-drift signature is weaker and
the wind-driven direct path dominates — that result is unaffected.
The DLC-1.6 H1 batch null may need re-running with the corrected
embedding before it can be properly interpreted as a controller-rejection
result rather than an embedding artifact.

**Status**: 🔵 resolved — fix in `analysis/te_pipeline.py`.

---

## 🔵 Q13 — Coherence Welch NPERSEG for slow-drift frequency resolution

**Resolved 2026-05-20** during the same physics audit. The previous
`coherence_baseline()` used `nperseg = min(N//4, 256)`, giving
Δf ≈ 0.02 Hz at 5 Hz sampling — too coarse to resolve the pitch
eigenfreq (0.0345 Hz) from the first-order JONSWAP peak (~0.077 Hz at
Tp = 12.95 s). For H6 the linear-baseline coherence γ²(f) needs to
show a sharp peak at the eigenfreq alongside the JONSWAP peak; at
Δf = 0.02 Hz the two would smear together.

**Fix** (committed 2026-05-20): added `TESettings.coherence_nperseg = 4096`,
plumbed through to `coherence_baseline()`. At 5 Hz × 4096 samples =
Δf ≈ 0.0012 Hz, more than sharp enough. With N = 15 001 the
Welch averaging uses ~3 overlapping segments — borderline but workable;
ensemble TE (Q10) would also enable seed-averaging the coherence which
improves SNR further.

**Status**: 🔵 resolved — fix in `analysis/te_pipeline.py`.

---

## 🟡 Q14 — Constrained Saltelli sampling for Phase 5 N = 256

**Filed 2026-05-20** from the same review. At N = 64 we computed Sobol
indices on the 44 %-feasible subset using **median imputation** for
infeasible Y values. This compresses the response variance and distorts
Sobol indices in an unpredictable direction — `ST > 1.0` is the visible
symptom; an unknown share of the magnitudes is also affected.
Increasing N alone does not fix this.

**Two options**:
1. **Rejection sampling within feasible region** — generate Saltelli
   sample, drop infeasibles, re-generate to maintain the required N.
   Bias-free but the sampling design loses its Saltelli structure.
2. **Constrained Saltelli scheme** — generate samples directly on the
   feasible region. Preserves Saltelli structure but the radial sample
   construction (`A_B` matrix from Saltelli 2010) requires the feasible
   region to be a Cartesian product, which it isn't here
   (`D_OCol > D_Pt` couples two variables).

**Recommendation**: rejection sampling for v1. The Sobol structure is
preserved on average; only the realised sample size shrinks. With
N = 256 base and ~44 % feasibility we end up with ~1100 effective
feasible points across 9 variables — adequate for stable ST estimates.

**Status**: 🟡 under investigation. Decision before Phase 5 N=256 launch.

---

## 🔵 Q0 — Whether to use TE for structural parameters (vs Sobol)

**Resolved 2026-05-12**: Use Sobol + MI, not TE, for design parameters.
Recorded in `phase5_param_method` memory and [[concepts/sobol-sensitivity]].

**Why**: TE is defined on time series; design parameters are constants
per OpenFAST run.
