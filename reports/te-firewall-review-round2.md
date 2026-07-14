# Simulated Peer-Review Panel — Round 2

- **Manuscript**: "An Information Firewall in Floating Offshore Wind Turbines: Blade-Pitch Control Decouples Wind from Platform Motion, with Implications for Health Monitoring" (`reports/te-firewall-paper-final.md`, as of 2026-07-14)
- **Review round**: 2 (Round 1: 2026-07-13, `reports/te-firewall-review-panel.docx` → Major Revision; immediately-actionable roadmap items were applied before this round)
- **Mode**: `academic-paper-reviewer` full (5-reviewer panel)
- **Review date**: 2026-07-14
- **Method note**: every quantitative claim checked in this round was verified against the repository (`sims/run_campaign.py`, `analysis/te_pipeline.py`, `analysis/delay_analysis.py`, `surd/phase2_campaign.py`, `reports/delay_profiles.parquet`, `reports/surd_table.parquet`) rather than taken from the manuscript.

---

## Phase 0 — Field Analysis & Reviewer Configuration

- **Primary field**: Ocean/offshore wind engineering (FOWT dynamics and control)
- **Secondary fields**: Information theory / causal inference on time series; structural health monitoring
- **Paradigm**: Quantitative simulation study (54-run OpenFAST campaign), empirical-mechanistic
- **Target tier**: Wind Energy Science / Ocean Engineering / Mechanical Systems and Signal Processing
- **Maturity**: Post-first-revision draft; pre-submission (placeholders in Data Availability / CRediT / Funding)

| Role | Persona |
|---|---|
| EIC | Associate editor, *Wind Energy Science*; background in FOWT control co-design; values reproducibility and bounded claims |
| R1 (Methodology) | Statistician specialising in information-theoretic estimators for dynamical systems (KSG/IDTxl user); focuses on estimator validity, significance testing, reproducibility |
| R2 (Domain) | Offshore-wind loads engineer (OpenFAST/ROSCO, IEC design load cases, met-ocean characterisation) |
| R3 (Perspective) | Process-control performance-monitoring researcher (control-loop diagnostics, plant-wide disturbance analysis) |
| DA (Devil's Advocate) | Sceptical reviewer tasked with the strongest counter-argument and internal-consistency audit |

(Same panel composition as Round 1 for continuity.)

---

## Phase 1 — Reviewer Reports

### Report 1 — EIC

**Role**: EIC · **Confidence**: 4

**Recommendation**: **Major Revision**

**Summary assessment.** The paper measures directed information flow (KSG transfer entropy) in 54 OpenFAST simulations of the IEA-15MW/VolturnUS-S and finds a controller-induced "information firewall": near-zero wind→platform TE against dominant wave→platform TE, attributed to blade-pitch control via SURD and an open-loop twin. The concept is original, the honesty about the untested monitoring claim is exemplary, and the round-1 revisions (ROSCO/hydro configuration, bootstrap CIs, positive controls) have materially strengthened the manuscript. However, this round finds that the submission copy has *regressed* relative to the authors' own working draft on the delay-resolved analysis (§4.5/Table 5/abstract) — it reports a surge delay of 4.3 s that the underlying data do not support — and the met-ocean description in §3.1 is factually wrong for 48 of 54 runs. These are integrity-of-record defects, not judgement calls, and they must be fixed and re-verified before the paper can proceed.

**Strengths.**
- **S1 — Original, well-bounded thesis.** The firewall-as-observable idea is genuinely new for FOWT monitoring; the paper repeatedly and correctly separates demonstrated results (firewall, attribution) from outlook (monitoring), e.g. §1 contributions, §4.4, §5.3.
- **S2 — Unusually strong statistical hygiene.** Chance-floor reasoning (§4.1), bootstrap CIs, exact-zero convention (§3.4), and the honest near-coincidence of healthy ceiling and false-positive floor (§4.4).
- **S3 — Reproducibility posture.** Hyperparameters traced to `analysis/te_pipeline.py`; Data Availability names the exact estimator stack and versions.

**Weaknesses.** (deferring detail to R1/R2)
- **W1 (Critical)** — Submission copy carries stale §3.8/§4.5/abstract content superseded in the working draft; Table 5's surge entry is not reproducible from `delay_profiles.parquet`. See R1-W1.
- **W2 (Major)** — §3.1 sea-state description contradicts the campaign generator. See R2-W1.
- **W3 (Major)** — Two-copy manuscript maintenance (draft/final) has produced divergent "fixed" states in both directions (final has the gated-mean §3.4, draft has the corrected delay analysis). The journal will see one document; the authors need a single source of truth and a final end-to-end numeric re-verification pass.

**Questions for authors.**
1. Which manuscript copy is authoritative, and what process will prevent future divergence?
2. Will the full-campaign re-verification (te_table_full) happen before submission, as your own records require?

**Dimension scores**: Originality 88 (Strong) · Rigor 62 (Adequate, capped by W1) · Evidence 70 · Coherence 80 · Writing 85 · **Weighted → Major Revision**

---

### Report 2 — Reviewer 1 (Methodology)

**Role**: Peer Reviewer 1 (Methodology) · **Confidence**: 5

**Recommendation**: **Major Revision**

**Summary assessment.** The TE estimation stack (IDTxl BivariateTE, KSG k=4, 200 permutations, max-statistic + omnibus corrections), the AIS normalisation, the wind–wave independence check, and the k-sweep are well above the field's usual standard. The k-sweep reconciliation with §3.3 and the bootstrap CIs added after round 1 are verified as present. Three problems remain, one of them disqualifying in its current state: the delay-resolved results in the submission copy disagree with the data files, the coherence baseline lacks any statistical benchmark, and the SURD quantities are reported with wrong units.

**Weaknesses.**

- **W1 — Table 5 / §4.5 / abstract are stale and contradict the data. Severity: Critical.**
  **Problem**: Table 5 reports Wave→PtfmSurge selected delay = 4.3 s and the abstract says "physical lags of 0.3–4.3 s". Recomputing the selected delay (argmax of the delay profile, per §3.8) from `reports/delay_profiles.parquet` gives 6.4/6.2/6.2 s across the three seeds — mean 6.3 s — with the profile globally peaked near half the wave period in *every* seed. The §4.5 prose reading ("surge (≈ 4.3 s) lag progressively, tracking the slower … mooring-mediated response") is therefore a physical misreading: the surge peak at ≈ Tp/2 is a near-antiphase *phase* signature of an inertia-dominated response, not a transport delay. The authors' own working draft (v0.6, 2026-07-09) already contains the correct values (6.3 s ≈ Tp/2, secondary peak 1.1 s), the half-period selection rule in §3.8, a "two orders of magnitude" correction in §4.1 (the submission copy still says "three"), and a Figure 7 with all-edge, all-seed profiles — none of which made it into the submission copy.
  **Why it matters**: A reviewer replicating Table 5 from the deposited parquet will get different numbers; that alone justifies rejection at most venues.
  **Suggestion**: Port the v0.6 delay block (abstract sentence, §3.8 half-period selection, §4.5 prose, Table 5 with the antiphase reading, Figure 7, "two orders") into the submission copy verbatim, then re-verify every §4.5 number against the parquet.

- **W2 — Coherence baseline has no significance benchmark. Severity: Major.**
  **Problem**: §3.5 reports Welch settings (nperseg = 4096 at 5 Hz) but not the number of averages. With 15,001-sample records this is ~6 half-overlapping segments, so the γ² estimates carry substantial bias and variance, and the zero-coherence 95% significance level (≈ 1 − α^{1/(K−1)} ≈ 0.45 for K = 6 independent averages) is nowhere stated.
  **Why it matters**: The coherence contrast is the paper's foil result (Table 4, §4.2). Without the no-coherence floor, a sceptic can attribute γ² ≈ 0.63–0.72 partly to low-average bias. (The values do clear the floor — which is why reporting it *strengthens* the paper.)
  **Suggestion**: State K and the zero-coherence significance level in §3.5 and note that all Table 4 peaks exceed it.

- **W3 — SURD quantities carry wrong units. Severity: Major.**
  **Problem**: §4.3 reports "`U:BldPitch1 → PtfmPitch` = 0.167 **nats** summed over lags" and "the control-attributable information drop falls from 0.0612 to 0.0265 **nats**". Per `surd/phase2_campaign.py`, the `rus` atoms are *normalised by the maximum mutual information* and the `drop` terms are differences of SURD leak fractions — all dimensionless. "`surd_wind_into_bldpitch` ≈ 0.4" (§4.3, §5.3) is likewise a normalised fraction.
  **Why it matters**: Nats-vs-normalised changes how readers compare SURD values to the TE results (which *are* in nats) — the current text invites an apples-to-oranges comparison.
  **Suggestion**: State the normalisation convention once in §3.6 and strip "nats" from all SURD numbers (§4.3 twice, Fig 4c caption, §5.3).

- **W4 — Open-loop twin is n = 1 and not labelled as such. Severity: Major.**
  **Problem**: §4.3's open-loop evidence ("collapses to exactly zero", "−57%") derives from a single 11 m/s realisation; the text says "an open-loop twin of a near-rated case" without stating n = 1 or any variability.
  **Why it matters**: One of the two attribution legs rests on one run; the reader must be able to weight it accordingly.
  **Suggestion**: Say "a single realisation (one seed)" explicitly and add seed replication to the §5.3 validation list (the round-1 roadmap already defers the extra seeds to the server campaign — fine, but the manuscript must say so).

- **W5 — Table 5 reports means without spread. Severity: Minor.**
  **Suggestion**: The draft's Figure 7 (three seeds overlaid, visibly indistinguishable) resolves this; porting it in (W1) suffices.

**Questions for authors.**
1. Which delay table is authoritative — and can you attach the exact script + parquet commit that reproduces it?
2. What is the effective number of independent Welch averages after 50% overlap, and does the Table 4 ranking survive a longer-segment/lower-Δf compromise?
3. Is the SURD leak normalised by the target-future entropy (as in Martínez-Sánchez et al.) or by max MI? State the exact convention.

**Dimension scores**: Rigor 58 → post-fix trajectory Strong · Evidence 68 · **→ Major Revision**

---

### Report 3 — Reviewer 2 (Domain)

**Role**: Peer Reviewer 2 (Domain — offshore wind loads/met-ocean) · **Confidence**: 5

**Recommendation**: **Major Revision**

**Summary assessment.** The plant, controller, and hydrodynamic configuration reporting added in round 1 (ROSCO 2.10.1, Fl_Mode = 2, SS_Mode = 1; PotMod = 1, DiffQTF = 12) is exactly what this reviewer asked for and is verified against the repo. The remaining domain problems are met-ocean description errors: the manuscript describes a single sea state where the campaign actually varies (Hs, Tp) with wind speed, and the Introduction still claims the whole campaign is DLC 1.6.

**Weaknesses.**

- **W1 — §3.1 sea-state description is wrong for 48/54 runs. Severity: Critical (factual).**
  **Problem**: §3.1 states "irregular waves use a JONSWAP spectrum with a peak period near 12.95 s (spectral peak ≈ 0.077 Hz)". Per `sims/run_campaign.py` (`DLC_WAVES`), the NTM runs use wind-speed-matched sea states: (Hs, Tp) = (3.5 m, 9.0 s), (4.5 m, 10.0 s), (6.0 m, 11.0 s), (8.0 m, 13.0 s) at 8/11/15/20 m/s; only the 6-run DLC 1.6 set uses (8.3 m, 12.95 s). §3.2's "wave-energy peak sits near 0.077 Hz" propagates the error (the true peaks span 0.077–0.111 Hz).
  **Why it matters**: The wave→platform coupling is the paper's load-bearing baseline; misstating the forcing spectrum for 89% of the campaign is not survivable in review. (The separation argument itself survives: even Tp = 9 s → 0.111 Hz is far from the 0.0345 Hz platform-pitch mode.)
  **Suggestion**: Report the (Hs, Tp) table (or inline list) and correct the spectral-peak range in §3.1/§3.2. The wind-speed-matched sea states are actually a *strength* — say so.

- **W2 — Introduction still calls the campaign "DLC 1.6 at four wind speeds". Severity: Major.**
  **Problem**: §1 scope paragraph: "simulated in OpenFAST under design load case (DLC) 1.6 at four wind speeds". §3.1 (corrected in round 1) says DLC 1.6 is 6/54 runs at 11 m/s only.
  **Suggestion**: Rewrite the scope sentence to match §3.1.

- **W3 — The "three healthy 11 m/s seeds" of §4.5 are the DLC 1.6 severe-sea seeds. Severity: Major.**
  **Problem**: `analysis/delay_analysis.py` draws its three cases from `dlc16_v11ms_s00..02` (Hs = 8.3 m, Tp = 12.95 s). The §4.5/Table 5 text calls them "healthy 11 m/s seeds" without disclosing the severe sea state — and the half-period cap (6.5 s) is Tp/2 *for that sea state specifically*.
  **Why it matters**: Delay values are sea-state-dependent (they scale with Tp); a reader would wrongly generalise them to the NTM cases.
  **Suggestion**: Identify the seeds as the DLC 1.6 set and scope the delays to that sea state.

- **W4 — FAIRTEN1's anomalous wave significance (53.7% vs 100% for lines 2–3) is unexplained. Severity: Minor.**
  **Suggestion**: One sentence on mooring-layout orientation relative to the co-directional forcing would pre-empt the question (verify against the MoorDyn layout before asserting).

**Questions for authors.**
1. Were TurbSim wind seeds and HydroDyn wave seeds paired or independent between dlca and dlcb variants, and does the wave-realisation variant matter for any Table 1–3 statistic?
2. Which mooring line is up-wave in the model layout?

**Dimension scores**: Rigor 60 · Evidence 72 · Literature 78 · **→ Major Revision**

---

### Report 4 — Reviewer 3 (Perspective — control-performance monitoring)

**Role**: Peer Reviewer 3 (Perspective) · **Confidence**: 4

**Recommendation**: **Minor Revision**

**Summary assessment.** As a cross-disciplinary contribution this is strong: it imports the process-control idea of loop-performance diagnosis from routine operating data (Bauer et al. is exactly the right anchor) into FOWT structural monitoring, and the "watch the loop's *effect*, not the actuator" framing is genuinely useful. The deployment discussion (§5.2) improved markedly in round 1 (regime-conditioned threshold, source-selection alarm statistic, nacelle-anemometer wake caveat). Two practical gaps remain.

**Weaknesses.**

- **W1 — Detection latency vs window length is never quantified. Severity: Major (for the outlook section).**
  **Problem**: The healthy baseline is estimated on ≈ 50-minute windows (§3.1); §5.2's "rolling windows" proposal never says what latency that implies, nor that shortening the window inflates KSG variance and the false-selection rate.
  **Suggestion**: One honest sentence: the present baseline implies hour-scale detection latency; the window/latency/false-alarm trade-off is part of the validation campaign.

- **W2 — No bridge to the control-performance-monitoring literature. Severity: Minor.**
  **Suggestion**: A sentence noting that this proposal is the structural-monitoring analogue of control-loop performance monitoring would help both readerships; optional.

- **W3 — Actionability of an alarm. Severity: Minor.**
  What does an operator *do* on a firewall-breach alarm (inspect pitch actuators? derate?)? One sentence in §5.2 would close the loop. Optional.

**Dimension scores**: Significance 85 (Strong) · Coherence 82 · **→ Minor Revision**

---

### Report 5 — Devil's Advocate

**Role**: Devil's Advocate · **Confidence**: 4

**Strongest counter-argument (the case against the paper).**
The firewall may be partly an artefact of *which wind signal was interrogated*. The analysis uses the hub-height *point* wind (`Wind1VelX`), but a 240-m rotor responds to the rotor-effective wind — the disc average — which strongly attenuates the small-scale turbulence that dominates a point measurement's fluctuating content. If much of the point signal's information is in eddies the rotor spatially filters out, then TE(point wind → platform) can sit at zero *even without any controller*, because the platform never saw that information in the first place. The paper's positive control (wind→blade-root edges) blunts but does not defeat this: blade-root moments respond to *local* blade-sampled wind, which is precisely the point-like quantity, so those edges being significant while platform edges are null is *also* what the spatial-filtering story predicts. The open-loop twin is the right rebuttal instrument — but its TE legs are exactly the computation the paper concedes is pending. Until TE(wind → platform) is shown to *rise* with the loop open (or the analysis is repeated with a rotor-averaged wind source), the controller attribution rests on SURD alone, computed with a coarse 3-bin quantisation, with both attribution lines sharing that estimator — a dependency the paper itself flags in §4.3.

**Issue list.**

- **DA-1 (CRITICAL, internal consistency)**: The submission copy demonstrably diverged from the authors' own corrected working draft (§4.5/Table 5/abstract/§3.8/"three orders"), and Table 5 cannot be regenerated from the deposited data. Until the copies are reconciled and every number re-verified, *no* quantitative claim in the manuscript can be trusted at face value. (Same finding as R1-W1, raised here as a trust/process failure rather than a statistics one.)
- **DA-2 (MAJOR)**: Rotor-effective vs point wind, as above. Dimension: construct validity. Location: §3.1 (source definition), §5.3. Demand: rotor-averaged-wind robustness check, or at minimum an explicit limitation with the blade-channel counter-argument stated *and* its weakness acknowledged.
- **DA-3 (MAJOR)**: Abstract rhetoric — "the firewall is, if anything, total" — sits uneasily beside Table 3's near-rated leakage (max 0.029 nats, 5.6–8.3% significant) and §4.4's admission that the healthy ceiling and the chance floor "nearly coincide". The abstract's strongest sentence and the results' most honest sentence should not read as if from different papers. Soften "total" or bind it explicitly to the chance-floor argument.
- **DA-4 (MINOR)**: §4.4's monitoring hypothesis presumes a usable detection window exists between the healthy ceiling (~0.03 nats) and a fault signature of unknown size; the paper says this honestly, but the abstract's "should re-admit wind information" does not carry the caveat.

**Ignored alternative explanations**: spatial filtering (DA-2); wave-dominance is addressed adequately (SURD redirection + 20 m/s argument, §5.1).
**Missing stakeholder perspectives**: operators (what action does an alarm trigger — see R3-W3).
**Observations (non-defects)**: The 20 m/s detectability rebuttal in §5.1 is genuinely strong; the chance-floor framing in §4.1 is the most statistically literate treatment of "we found nothing" this reviewer has seen in the FOWT literature.

---

## Phase 2 — Editorial Decision

### Decision: **MAJOR REVISION**

(IRON RULE check: DA raised a CRITICAL issue → Accept is unavailable; the issue is however fully repairable from existing local data.)

### Reviewer summary

| Reviewer | Recommendation | Confidence |
|---|---|---|
| EIC | Major Revision | 4 |
| R1 (Methodology) | Major Revision | 5 |
| R2 (Domain) | Major Revision | 5 |
| R3 (Perspective) | Minor Revision | 4 |
| DA | Major Revision (1 CRITICAL) | 4 |

### Consensus analysis

**[CONSENSUS-5]** The delay-analysis regression (stale Table 5/abstract/§3.8/§4.5) must be repaired and all numbers re-verified against the parquet (EIC-W1, R1-W1, DA-1; R2 and R3 silent on delays but endorse re-verification).
**[CONSENSUS-3]** Sea-state misdescription (R2-W1, endorsed EIC, R1; others silent).
**[CONSENSUS-3]** SURD unit correction (R1-W3; EIC, DA endorse).

**Disagreement 1 — how damaging is the rotor-effective-wind challenge (DA-2)?**
- **DA**: construct-validity threat; demands recomputation.
- **R1**: legitimate but second-order — the near-rated leakage (Table 3) and tower-base edges show the point signal *does* carry platform-relevant low-frequency content; recomputation is a server task, a limitation suffices now.
- **Resolution**: Adopt R1's position for this round — add the limitation with both sides stated, queue the rotor-averaged robustness check with the fault-TE campaign. Rationale: conservative claim-scoping is available without new computation; the challenge attacks attribution *completeness*, not the measured firewall itself.

**Disagreement 2 — severity of the abstract's "total" rhetoric (DA-3).**
- **DA**: Major. **R3**: cosmetic given §4.4's honesty.
- **Resolution**: treat as Required-but-small: bind "total" to the chance-floor clause in the abstract. Rationale: abstracts travel alone.

### Decision rationale

The panel is unanimous that the science, framing, and statistical hygiene are strong and improved by the round-1 revision, and equally unanimous that the submission copy currently fails an integrity-of-record test: its delay-resolved results contradict both the deposited data and the authors' own corrected working draft, and its met-ocean description is wrong for 48 of 54 runs. These are Critical not because the underlying work is unsound — the corrected results already exist in the draft and reproduce from the parquet — but because a manuscript whose tables cannot be regenerated from its data is unreviewable. Major Revision (not Minor) because the fixes touch the abstract, methods, results, and a figure, and because the panel requires a documented end-to-end numeric re-verification after the two manuscript copies are reconciled. Rejection was not considered: every Critical item is repairable from existing local artefacts.

### Required revisions (Must fix)

| # | Item | Source | Severity | Section | Local? |
|---|---|---|---|---|---|
| RR1 | Port the v0.6 delay corrections into the submission copy: abstract delay sentence; §3.8 half-period selection rule; §4.5 prose (antiphase reading), Table 5 (surge 6.3 s ≈ Tp/2, secondary 1.1 s), Figure 7; §4.1 "three→two orders of magnitude". Re-verify against `delay_profiles.parquet`. | R1-W1/EIC-W1/DA-1 | Critical | Abstract, §3.8, §4.1, §4.5 | Yes |
| RR2 | Correct sea-state description: wind-speed-matched (Hs, Tp) per `DLC_WAVES`; spectral-peak range 0.077–0.111 Hz; fix §3.2. | R2-W1 | Critical | §3.1, §3.2 | Yes |
| RR3 | Fix Introduction scope sentence (campaign ≠ DLC 1.6 at four wind speeds). | R2-W2 | Major | §1 | Yes |
| RR4 | Identify the §4.5 delay seeds as the DLC 1.6 severe-sea set and scope the delays to that sea state. | R2-W3 | Major | §4.5, Table 5 | Yes |
| RR5 | SURD units: state normalisation in §3.6; remove "nats" from all SURD figures (§4.3 ×2, Fig 4c caption, §5.3). | R1-W3 | Major | §3.6, §4.3, §5.3 | Yes |
| RR6 | Coherence: report ~6 Welch averages and the ≈0.45 zero-coherence 95% level; note all Table 4 peaks clear it. | R1-W2 | Major | §3.5 | Yes |
| RR7 | Open-loop twin: state n = 1 explicitly; add seed replication to the validation list. | R1-W4 | Major | §4.3, §5.3 | Yes |
| RR8 | Rotor-effective-wind limitation with the blade-channel counter-argument and its acknowledged weakness; queue the rotor-averaged robustness check. | DA-2 | Major | §5.3 | Yes (text) |
| RR9 | Bind the abstract's "total" to the chance-floor clause. | DA-3 | Major | Abstract | Yes |
| RR10 | Reconcile draft↔final (draft §3.4 still carries the pre-gating prose); declare one source of truth; run one end-to-end numeric re-verification. | EIC-W3 | Major | — | Yes |

### Suggested revisions (Should fix)

| # | Item | Source | Priority |
|---|---|---|---|
| S1 | Window-length ↔ detection-latency sentence in §5.2. | R3-W1 | P2 |
| S2 | FAIRTEN1 mooring-orientation explanation (verify layout first). | R2-W4 | P2 |
| S3 | One-sentence bridge to control-performance monitoring; operator action on alarm. | R3-W2/W3 | P3 |
| S4 | dlca/dlcb seed-pairing detail (R2-Q1). | R2 | P3 |

### Deferred (require server / new simulations — carried over from Round 1)

- Fault-case TE (`compute_fault_te.py`), open-loop TE legs, open-loop seed replication, rotor-averaged-wind TE, tau=1 control on slow-drift channels, full-campaign (`te_table_full.parquet`) re-verification.

### Revision roadmap

- **P1 (blocking, all local)**: RR1 → RR2 → RR3 → RR10 (reconcile + re-verify), then RR4–RR9.
- **P2**: S1, S2.
- **P3**: S3, S4.
- **Estimated effort**: P1+P2 ≈ 1 working session (all artefacts exist locally); deferred items ride the queued server campaign.
