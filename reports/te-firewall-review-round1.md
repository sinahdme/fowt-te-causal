# Peer Review — Round 1 (Stage 3, academic-paper-reviewer full mode)

**Manuscript:** Blade-Pitch Health Monitoring of a Floating Offshore Wind Turbine via Transfer Entropy (v0.2, 8,347 words)
**Date:** 2026-07-08
**Panel:** EiC + Methodology (R1) + Domain (R2) + Perspective (R3) + Devil's Advocate

---

## Phase 0 — Field analysis & reviewer configuration

- **Primary discipline:** floating offshore wind engineering (structural dynamics / control).
- **Secondary:** information-theoretic time-series analysis / SHM.
- **Paradigm:** simulation-based quantitative; causal-inference methods.
- **Target tier:** *Wind Energy Science / Renewable Energy / Ocean Engineering* (Q1 applied-energy).
- **Maturity:** strong core result; one over-scoped contribution.

**Reviewer personas:**
- **EiC** — associate editor, *Wind Energy Science*; values novelty + rigor + honest scoping.
- **R1 (Methodology)** — information-theoretic causality specialist (TE/KSG/surrogate testing).
- **R2 (Domain)** — FOWT control & loads engineer (ROSCO, DLCs, platform dynamics).
- **R3 (Perspective)** — condition-monitoring / SHM researcher (detection-theory framing).
- **Devil's Advocate** — challenges the core claims.

---

## Phase 1 — Independent reviews

### Reviewer: Editor-in-Chief

**Summary.** The paper reframes a striking negative result — wind carries no information into FOWT platform motion — as a controller-induced "information firewall," and proposes its breach as a health-monitoring signal. The firewall result is novel, well-supported, and genuinely interesting; I have not seen directed information flow used to characterise control-loop health in a floating turbine, and the coherence-vs-TE contrast is a compelling teaching example. The writing is clear and unusually honest about its own limits.

**Concern.** The manuscript advertises three contributions of roughly equal weight, but only two are actually delivered. The third — the monitoring method — is presented as "proof of concept," yet the single fault case has no transfer entropy computed at all. A reader arriving via the title ("Health Monitoring") will expect a demonstrated diagnostic and will not find one. Either the evidence must be strengthened or the framing must be rebalanced so the title and abstract match what is shown.

**Scores (0–100):** Originality 82 · Rigor 63 · Evidence 56 · Coherence 80 · Writing 86. **Recommendation: Major Revision.**

---

### Reviewer 1 — Methodology

**Strengths.** Estimator choice and configuration are documented to an unusually reproducible standard (KSG k=4, decoupled target/source embedding windows, permutation null with max-statistic correction, AIS normalisation). The decision to report an exact zero when no source is selected is defensible and well explained. Grounding every number in named data tables is exemplary.

**Major issues.**

1. **The significance rate sits at the chance floor, and this cuts both ways (§4.1, §4.4).** With a permutation test at α = 0.05, roughly 5% of truly-null channels are expected to test "significant" by chance. The reported wind→platform-pitch significance rate is 3.7% — *at or below* the false-positive floor. This strongly corroborates the firewall (wind selection is indistinguishable from noise). But it fatally weakens §4.4: the two cases "flagged as wind reaching the platform" (0.026–0.029 nats, significant) are exactly what one expects from chance false positives at this α, not evidence of a breach. The manuscript must confront this directly — a monitoring alarm built on an effect at the noise floor has no demonstrated separation from the healthy population. Report the expected number of chance-significant cases (≈ 2–3 of 54) and compare.

2. **The open-loop attribution is itself n=1 and partly uncomputed (§4.3).** The `U:BldPitch1 → PtfmPitch` collapse (0.167 → 0) is a single simulation, and the paper concedes the twin's TE legs are pending. The attribution therefore leans on one case plus SURD redirection. SURD redirection is the stronger leg; lead with it and treat the twin as corroborating, and add at least a few more open-loop seeds if feasible.

3. **`te_frac` is defined but never used in Results (§3.4 vs §4).** Either report the normalised effect size where it matters (it would sharpen the firewall claim: wind te_frac ≈ 0) or cut the machinery.

4. **SURD robustness (§3.6).** nbins = 3 is very coarse; a sensitivity check on bin count and lag would reassure that `surd_wind_into_bldpitch ≈ 0.4` is not quantisation-dependent.

**Scores:** Originality 75 · Rigor 55 · Evidence 52 · Coherence 74 · Writing 82. **Recommendation: Major Revision.**

---

### Reviewer 2 — Domain (FOWT control & loads)

**Strengths.** The physical mechanism is correct and well told: thrust regulation converts broadband wind into pitch actuation, smoothing platform forcing, while the unregulated wave channel dominates rigid-body motion. The target-specificity result (wind reaches blades/tower but not the platform, RootMxc1 39% vs PtfmPitch 3.7%) is a genuinely nice internal consistency check and should be foregrounded — it is strong evidence the mechanism is real and not an artefact.

**Major issues.**

1. **Below-rated logic needs the honesty it already shows, applied to the abstract too.** The manuscript correctly notes (§4.3, §5.1) that the 8 m/s zero is confounded by weak forcing. Good — but the abstract and intro should not imply the regime behaviour supports attribution; only SURD and the twin do. (Partly addressed already; verify consistency throughout.)

2. **Controller specificity (§2.2, §5.2).** Results are for ROSCO with floating-feedback terms. The firewall's strength depends on control tuning; a detuned or differently-architected controller could leak more. State that the baseline is controller-specific and that the monitor would need re-baselining per control configuration, not only per turbine.

3. **Missing loads context.** For a loads/SHM audience, connect the firewall to fatigue: does the wave-dominated platform response imply the pitch fault's danger is via re-admitting wind-driven low-frequency thrust into an already lightly damped platform? One paragraph on the consequence of a breach for platform/mooring fatigue would raise domain impact.

**Missing references (domain):** a floating-control negative-damping reference (e.g., Larsen & Hanson, or Fleming et al. on platform-motion-aware control) to support the §5.2 claim that floating controllers deliberately suppress the wind→platform path.

**Scores:** Originality 80 · Rigor 66 · Evidence 60 · Coherence 82 · Writing 84. **Recommendation: Major Revision (borderline Minor if monitoring is rescoped).**

---

### Reviewer 3 — Perspective (condition monitoring / detection theory)

**Strengths.** The idea of monitoring a *controller-created absence* rather than a component signature is fresh and, if validated, valuable — it is model-free, label-free, and sensitive to any fault degrading thrust regulation. The operational discussion (§5.2: region-conditioned threshold, source-selection rate as the alarm statistic) is thoughtful.

**Major issue — no detection performance exists.** The paper is titled for monitoring but reports no ROC, no detection rate, no false-alarm rate, no separation statistic. §4.4 is a hypothesis, not a result. This is acceptable *only* if the paper is reframed as "discovery + proposed diagnostic," with monitoring explicitly demoted from a contribution to an outlook. As written, the gap between title and evidence is the paper's biggest exposure at review.

**Constructive path.** Computing TE for the one existing pitch-lock/open-loop case is the minimum. Even a single fault case with TE clearly above the healthy ceiling (and above the chance floor R1 raises) would convert §4.4 from hypothesis to genuine proof of concept. Better: 3–5 graded severities at one wind speed.

**Scores:** Originality 84 · Rigor 62 · Evidence 54 · Coherence 79 · Writing 83. **Recommendation: Major Revision.**

---

### Devil's Advocate Report

**Strongest counter-argument (≈250 words).** The paper's headline is a near-zero measurement, and near-zero measurements are the easiest thing in the world to produce for the wrong reason. The authors argue the wind→platform zero is a controller firewall. But their own data offer a mundane alternative they do not fully exclude: at the two regimes where the zero is *exact and universal* (8 and 20 m/s), the explanation is plausibly trivial — at 8 m/s the wind forcing is weak and the platform is wave-dominated; at 20 m/s the analysis simply may lack the resolution or the fluctuation amplitude to detect a small residual. The only regime with any wind leakage at all (11–15 m/s) is also the only regime where a genuine effect could be resolved. In other words, the "firewall" could be partly a detectability artefact of where wind fluctuations are large enough to measure against a wave-saturated platform. The SURD redirection result is the paper's real defence — but SURD runs at nbins=3 and the decisive open-loop twin is a single, TE-uncomputed case. Strip those away and the causal claim rests on one coarse decomposition and a plausible story.

**Then the monitoring claim.** It is not merely thin — it is currently *unsupported by any computed fault TE*. The two "breach" cases live inside the healthy band and, per Reviewer 1, at the chance-significance floor. The paper's third of three contributions has zero affirmative evidence.

**Issue list:**
- **CRITICAL** — Contribution 3 (monitoring diagnostic) is claimed but not demonstrated; the fault case has no TE computed and the "flagged" cases are consistent with chance (§4.4, abstract, title). Under the panel's rules a claimed-but-unevidenced core contribution blocks Accept.
- **MAJOR** — Firewall attribution's decisive experiment (open-loop twin) is n=1 with pending TE; the causal claim is under-replicated (§4.3).
- **MAJOR** — Detectability confound for the exact-zero regimes not excluded (§4.1, §5.1).
- **MINOR** — "Coherence false positive" (§4.2) risks a strawman: coherence never claims direction, so calling it "false" is rhetorically loaded. Reframe as "coherence is insufficient because undirected," not "wrong."

**Ignored alternative explanation:** wind-fluctuation amplitude / detectability varying with regime as a (partial) driver of the exact zeros.

**Missing stakeholder:** an operator deploying this would need the false-alarm cost quantified; none is given.

**Observations (non-defects):** the honesty of the limitations section is above average and works in the paper's favour; the target-specificity result is a real strength the authors under-sell.

---

## Phase 2 — Editorial synthesis & decision

**Consensus across all 5 reviewers:**
1. The **firewall discovery + coherence contrast + SURD/target-specificity attribution** is novel, rigorous, and publishable (all 5 positive).
2. The **monitoring contribution is over-claimed relative to evidence** (all 5 flag it; DA rates it CRITICAL).
3. Writing quality and honesty are strong (all 5).

**Disagreement:** R2 would accept with Minor if monitoring is rescoped; R1/R3/DA require either computed fault evidence or an explicit demotion of the monitoring claim.

**Devil's Advocate CRITICAL finding is present → decision cannot be Accept (IRON rule).**

### Editorial Decision: **MAJOR REVISION**

The core science is sound and the paper is likely acceptable after revision, but the title/abstract currently promise a monitoring method the manuscript does not demonstrate. Two acceptable resolutions; the authors choose:

- **Path A (strengthen):** compute TE for the existing pitch-lock/open-loop case (and, ideally, 3–5 graded pitch-fault severities at one wind speed). If TE clearly exceeds the healthy ceiling *and* the chance floor, §4.4 becomes a real proof of concept and the monitoring contribution stands. This also upgrades the attribution (open-loop TE) from pending to computed — one computation closes two issues.
- **Path B (rescope):** demote monitoring from a claimed contribution to a proposed outlook. Retitle toward the firewall discovery (e.g., "A control-induced information firewall in floating wind turbines, with implications for health monitoring"), move §4.4 into Discussion as a hypothesis, and soften the abstract's final sentences.

### Revision Roadmap (prioritised)

| # | Priority | Issue | Location | Required action |
|---|---|---|---|---|
| 1 | **P0 (CRITICAL)** | Monitoring claimed, not demonstrated | Title, abstract, §4.4 | Path A (compute fault TE) or Path B (rescope to outlook). Must resolve title↔evidence mismatch. |
| 2 | **P0** | Chance-floor significance undercuts the two "breach" cases | §4.1, §4.4 | Report expected chance-significant count at α=0.05; show the flagged cases exceed it, or concede they don't. |
| 3 | **P1 (MAJOR)** | Attribution's open-loop twin is n=1, TE pending | §4.3 | Lead attribution with SURD redirection; add open-loop seeds and/or compute the twin's TE. |
| 4 | **P1** | Detectability confound for exact-zero regimes | §4.1, §5.1 | Add a paragraph (and if possible a check) excluding wind-amplitude/detectability as the cause of the 8/20 m/s zeros. |
| 5 | **P2 (MINOR)** | te_frac defined, unused | §3.4, §4 | Report normalised effect size in Results or remove. |
| 6 | **P2** | "Coherence false positive" framing | §4.2 | Reframe as "insufficient because undirected," not "wrong/false." |
| 7 | **P2** | SURD nbins=3 robustness | §3.6 | Add bin-count/lag sensitivity note. |
| 8 | **P2** | Controller-specificity & fatigue consequence | §5.2 | State baseline is control-config-specific; add one paragraph on breach→platform/mooring fatigue. Add floating-control negative-damping reference. |

**Overall panel score (weighted: Orig 20 / Rigor 25 / Evidence 25 / Coherence 15 / Writing 15):** ≈ **65/100** — Major Revision. The firewall paper inside this manuscript is an easy accept; the monitoring paper it is currently billed as is not yet supported.
