---
title: "Peer-Review Package — Simulated Panel Review"
subtitle: "An Information Firewall in Floating Offshore Wind Turbines"
author: "ARS academic-paper-reviewer (full mode) · 5-reviewer ocean/wind-engineering panel"
date: 2026-07-13
lang: en
geometry: margin=1in
fontsize: 11pt
---

# Peer-Review Package

**Manuscript:** *An Information Firewall in Floating Offshore Wind Turbines: Blade-Pitch Control Decouples Wind from Platform Motion, with Implications for Health Monitoring*

**Author:** S. Hadadi  ·  **Target tier:** Wind Energy Science / Ocean Engineering / Renewable Energy

**Review mode:** Full panel — Editor-in-Chief + 3 peer reviewers + Devil's Advocate, followed by editorial synthesis.

> This is a *simulated* peer-review report produced by the ARS `academic-paper-reviewer` skill (read-only; the manuscript was not modified). Reviewer personas are adjustable.

---

## Phase 0 — Field analysis & reviewer configuration

| Field attribute | Determination |
|---|---|
| Primary discipline | Offshore / ocean engineering — FOWT aero-hydro-servo-elastic dynamics |
| Secondary discipline | Information-theoretic causal inference (transfer entropy / SURD) + structural health monitoring |
| Research paradigm | Simulation-based, quantitative; mechanism identification + attribution |
| Paper maturity | Complete mechanism study; monitoring application explicitly deferred |
| Suggested venue | *Wind Energy Science* (best fit); *Ocean Engineering* / *Renewable Energy*; *MSSP* if reframed SHM-first |

**Panel (adjustable):**

- **EIC** — Wind Energy Science associate editor; floating wind + methods novelty.
- **R1 — Methodology** — information-theoretic estimation (KSG / JIDT / IDTxl), significance testing, reproducibility.
- **R2 — Domain** — OpenFAST FOWT hydro-servo-elastic modelling and ROSCO control.
- **R3 — Perspective** — operational SHM / condition monitoring and deployment.
- **Devil's Advocate** — challenges the "firewall" as novelty and the monitoring framing.

---

## Phase 1 — Independent reviews

### R0 · Editor-in-Chief

**Summary.** A genuinely fresh idea: read a floating-wind controller's disturbance rejection as a *directed-information* signature and propose its failure as a health signal. The writing is unusually honest — the paper repeatedly draws the line between what it demonstrates (a firewall and its attribution to control) and what it does not (a validated monitor). That candor is a strength and rare.

**Fit & significance.** Strong fit for WES / Ocean Eng. The mechanism-and-attribution result is publishable on its own. My one editorial reservation is structural: **the title and abstract foreground "health monitoring," but the monitoring method is undelivered** (§4.4, §5.3). A reader arriving via the title will feel the paper stops one computation short of its headline. Either deliver the fault-case TE, or rebalance the title/abstract toward the demonstrated contribution.

**Recommendation: Major Revision.**  Scores — Originality 82 · Significance 66 · Clarity 88.

---

### R1 · Methodology Reviewer (information-theoretic estimation)

Rigorous and well-documented overall; the significance-gating logic and the chance-floor argument (2 of 54 significant = 0.05 × 54 expected) are handled better than most TE papers. Specific issues:

1. **[MAJOR] Internal contradiction on the k-sweep.** §3.3 reports *"Sweeping k ∈ {3,4,6,8} … the wind ceiling stays ≤ 0.03 nats … 39–48× at every k."* But §5.3 states *"we did not sweep them … A systematic sensitivity study over k … is future work."* These cannot both stand. Reconcile — presumably k was swept on the delay profiles but not systematically across all channels/cases. Fix the §5.3 wording; a referee who spots this will distrust the rest.
2. **[MAJOR] No uncertainty on headline numbers.** TE means (0.0009, 0.121 nats) and the SURD atoms (≈ 0.4, 0.167) are reported as point values. For a null-centred claim ("essentially zero") the reader needs a **confidence interval or the surrogate null band** on the key channels (at minimum Wind→ and Wave→PtfmPitch). Bootstrap over seeds or report the permutation-null quantiles.
3. **[MINOR, partly addressed] Signed KSG estimates.** Good that channel means are significance-gated (§3.4) — the right convention, and it removes the impossible negatives. State once that individual non-significant KSG estimates are signed, so a reader recomputing from `te_table.parquet` is not surprised.
4. **[MINOR] SURD reproducibility.** The 3-bin marginal quantisation is coarse; §5.3 flags this. Report the SURD atoms to a stated precision and show they survive a finer binning on at least one case — otherwise "≈ 0.4" reads as fragile.
5. **[MINOR] Percentages → counts.** "3.7% of cases" etc.: give n/N (2/54) alongside, as you do in places; be consistent across Tables 1–4.

**Recommendation: Major Revision.**  Rigor 70 · Validity 72 · Reproducibility 72.

---

### R2 · Domain Reviewer (FOWT modelling & control)

The dynamics reasoning is sound and the delay analysis (Table 5: pitch 0.3 s → surge 4.3 s) is physically convincing. My concerns are about whether the load-bearing *wave→platform* result and the control attribution are pinned to a stated model configuration.

1. **[MAJOR] Second-order wave loading is deferred, not confirmed.** The platform-pitch resonance (0.0345 Hz) is largely driven by **second-order difference-frequency** loads. §5.3 says its robustness "should be confirmed rather than assumed." For the paper's *dominant* result this must be **confirmed in-paper**: state the HydroDyn second-order settings (`WvDiffQTF` / `WvSumQTF` / PotMod) and, ideally, one sensitivity run. As written, a domain referee cannot tell whether the wave→pitch coupling is first- or second-order mediated.
2. **[MAJOR] ROSCO configuration underspecified.** The entire firewall attribution hinges on the controller. State the ROSCO version and, critically, whether the **floating feedback (`Fl`) term and set-point smoothing** were active, with gains. The firewall is *expected* to depend on the `Fl` term; if it were off, the interpretation changes. One paragraph, large interpretive payoff.
3. **[MAJOR] Attribution leans on a single open-loop seed.** The controller attribution (§4.3) rests substantially on one 11 m/s open-loop twin, and its TE legs are uncomputed, so the converse (TE *rises* when the loop opens) is untested. At minimum add seeds; better, compute the open-loop TE — it closes the attribution and the monitoring test at once (the paper says as much).
4. **[MINOR] Campaign description** (now corrected to NTM `dlca`/`dlcb` + DLC 1.6 `dlc16`) — good. Ensure Figure 2 is regenerated to match; the caption now describes a structure the old 4×6 image does not show. Co-directional wind/waves only is acknowledged; keep that limitation explicit.
5. **[MINOR] Rated-speed context.** IEA-15 rated ≈ 10.6 m/s; note that 11 m/s is *just* above rated, which sharpens the "near-rated is where leakage appears" point.

**Recommendation: Major Revision.**  Rigor 68 · Validity 70 · Domain contribution 76.

---

### R3 · Perspective Reviewer (operational SHM / deployment)

The framing — monitor the *closed loop's function* rather than a component — is compelling and complements actuator-level pitch diagnostics well. But the path from this result to a usable monitor has two structural risks the paper should confront harder (it partly does).

1. **[MAJOR] The detection window may be vanishing.** §4.4 admits the healthy ceiling (≈ 0.03 nats) and the chance-floor false positives (up to 0.029 nats) *nearly coincide*. That is close to fatal for a threshold-based monitor: the "signal" a fault must produce to be distinguishable is barely above the healthy noise. The paper is admirably honest, but the reader is left unsure the diagnostic can ever work. The graded-fault ROC (§5.3) is not optional future work — without at least a *preliminary* fault point showing separation, the monitoring outlook is unfalsified speculation.
2. **[MAJOR] The deployment input is the weak link.** The analysis uses free-stream hub-height wind; a real monitor sees a **nacelle anemometer in the rotor wake**, a poor free-stream proxy that would inflate the baseline and blunt the source-selection alarm. §5.3 concedes this and points to lidar — but lidar is not standard fleet instrumentation, so the practical claim ("ordinary operational signals," §5.2) is in tension with the input the method actually needs. Soften §5.2 or justify the anemometer path with a wake-degradation estimate.
3. **[MINOR] Re-baselining burden.** Per-turbine, per-platform, *and* per-control-configuration re-baselining (§5.2) is a real operational cost; a sentence on how a fleet operator would manage it would strengthen impact.
4. **[MINOR] Connect to directed-information SHM.** The Bauer et al. process-control analogy is apt; briefly situating against directed-information / Granger SHM would preempt "why TE over Granger" beyond the one Barnett citation.

**Recommendation: Major Revision.**  Significance 64 · External validity 60 · Clarity 86.

---

### Devil's Advocate

**Strongest counter-argument.** The paper's demonstrated result may be a well-known control fact re-expressed in nats. "A healthy above-rated collective-pitch controller regulates thrust, so the platform sees smoothed forcing and wind fluctuations do not propagate into platform motion" is textbook floating-wind control (indeed the paper cites Larsen & Hanson, Bossanyi for exactly this). Transfer entropy quantifies it elegantly and directionally — real value — but the *novel, high-impact* claim is the monitoring application, which is precisely the part not delivered. Strip the outlook and the contribution risks reducing to "we confirmed, information-theoretically, that the controller works." The paper's own honesty invites this reading.

**Issue list:**

- **[CRITICAL] Title / abstract over-claim vs delivered content.** "…with Implications for Health Monitoring," the abstract's diagnostic framing, and contribution #3 all foreground a monitor that §4.4 / §5.3 explicitly do not test (zero fault-case TE). Per the panel's iron rule, a CRITICAL over-claim blocks Accept. Resolution is cheap: **either compute one fault case, or retitle to the mechanism** (e.g., "…Blade-Pitch Control Decouples Wind from Platform Motion in Floating Wind Turbines").
- **[MAJOR] The two "independent" attribution lines both rest on SURD.** §4.3 presents SURD redirection and the open-loop collapse as independent, but the open-loop evidence is *also* a SURD unique-information atom (`U:BldPitch1 → PtfmPitch`), computed with the same coarse 3-bin quantiser. They are correlated evidence, not independent. The truly independent test — TE rising when the loop opens — is uncomputed.
- **[MINOR] "Decisive at 20 m/s" needs one number.** The detectability rebuttal (§5.1) hinges on wind fluctuation being large at 20 m/s *at platform-relevant low frequencies*. Above rated, turbulence intensity drops; show the low-frequency wind PSD is non-negligible so the "least detectability alibi" claim is quantitative, not asserted.

**Non-defects (observations):** the honesty about the untested monitor is a genuine strength, not a flaw; the coherence-vs-TE contrast (γ² ≈ 0.72 vs 3.7% significant) is a clean, publishable teaching result on its own.

---

## Phase 2 — Editorial synthesis & decision

**Consensus (≥ 3 reviewers):**

- Novel, well-written, honest; the firewall + attribution are publishable.
- **The title / abstract promise monitoring the paper does not deliver** (EIC, R3, DA — DA rates CRITICAL).
- **Compute the pending fault / open-loop TE** — it simultaneously (a) tests the monitor, (b) closes the attribution converse, (c) earns the title (R2, R3, DA, EIC).
- Missing uncertainty quantification on headline numbers (R1; implicit in R3's detection-window concern).

**Disagreement:** R1 treats the monitoring gap as a framing / rigor issue (fixable by reframing); DA treats it as CRITICAL to the paper's claimed novelty. **Arbitration:** the CRITICAL stands but is *resolvable* — it forces non-Accept, not Reject, because a single fault computation or a retitle discharges it.

### Editorial decision: **MAJOR REVISION**

A solid, novel, honestly-scoped contribution held back by an over-claiming frame and a few load-bearing items deferred rather than confirmed. Not minor (title / framing + second-order waves + ROSCO config + uncertainty are substantive); not reject (the demonstrated results are sound and original).

### Revision Roadmap (prioritized)

| # | Priority | Item | Reviewer(s) |
|---|---|---|---|
| 1 | **Critical** | Resolve the over-claim: **compute TE for the pitch-lock + open-loop cases** (closes the monitoring test *and* the attribution converse) — *or*, if infeasible now, retitle / re-abstract to the mechanism and demote monitoring fully. | DA, EIC, R2, R3 |
| 2 | **Major** | Fix the §3.3 ↔ §5.3 **k-sweep contradiction**. | R1 |
| 3 | **Major** | Add **uncertainty** (CIs / surrogate-null bands) to the key TE and SURD values. | R1, R3 |
| 4 | **Major** | Confirm **second-order wave loading** settings + a sensitivity note (the wave→platform result is load-bearing). | R2 |
| 5 | **Major** | State **ROSCO version + floating-feedback / set-point-smoothing config**; attribution depends on it. | R2 |
| 6 | **Major** | Add **≥ 1 more open-loop seed** (or the open-loop TE) so attribution is not a single case; note the two attribution lines are both SURD-based. | R2, DA |
| 7 | **Minor** | Regenerate **Figure 2** to match the corrected campaign caption; quantify the 20 m/s low-frequency wind PSD; soften the "ordinary operational signals" claim re nacelle-anemometer wake; add counts beside percentages. | R2, R3, DA |

**The decisive lever:** items 1 and 6 are the *same computation* (`analysis/compute_fault_te.py` on the pending `dlca_v11ms_s00_openloop` + a pitch-lock case). Running it likely moves this from Major Revision toward Accept, because it converts the paper's biggest weakness (undelivered monitor) into its headline result.

---

### Dimension scorecard (panel mean, 0–100)

| Dimension | Score |
|---|---|
| Originality / novelty | 80 |
| Significance / impact | 65 |
| Methodological rigor | 69 |
| Validity of claims | 71 |
| Framing / literature | 74 |
| Clarity / presentation | 87 |
| Reproducibility | 72 |

---

*End of review package. Produced read-only; the manuscript file was not modified.*
