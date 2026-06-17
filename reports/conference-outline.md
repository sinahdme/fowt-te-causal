# Conference talk outline — TE causal discovery on a FOWT
*Draft 2026-06-09; numbers corrected 2026-06-17 to the full 54-case campaign in reports/te_table.parquet (DLC-A/B at 8/11/15/20 m/s + DLC-1.6 at 11 m/s, 6 seeds each). The earlier draft quoted single-seed preliminary values (incl. Wave→PtfmPitch 0.211 nats and a Wind→FAIRTEN2 edge) that do not survive the campaign-wide significance test — do not reuse them.*

---

### 1. Title
Transfer-entropy causal discovery of environment→structure coupling in a floating offshore wind turbine (IEA-15MW on UMaine VolturnUS-S).

### 2. Motivation
- FOWT load/response analysis leans on coherence/correlation (association, symmetric) — not **directed causality**.
- Question: can information-theoretic **directed transfer** reveal which environmental driver causes which structural response, and pathways linear methods miss?

### 3. System & data
- IEA-15-240-RWT on UMaineSemi, OpenFAST (aero-hydro-servo-elastic), 3600 s, drop 600 s, decimate to 5 Hz.
- 2 sources (Wind1VelX, Wave1Elev) → 9 responses (RootMyc1, RootMxc1, TwrBsMyt, PtfmHeave/Surge/Pitch, FAIRTEN1/2/3).
- Full campaign: DLC-A / DLC-B / DLC-1.6, 8/11/15/20 m/s, 6 seeds — 54 cases.

### 4. Method
- **KSG transfer entropy** (Kraskov k=4), non-uniform embedding, max_lag=150 (30 s, covers slow-drift).
- **Circular-shift surrogates** ×200, p<0.05, max-stat correction.
- **AIS-normalised effect size** te_frac = TE/(H(Y)−AIS(Y)).
- **Two linear baselines, same pipeline**: Gaussian/Granger (estimator swap) + coherence (scipy).
- Compute: OpenCL on 2× A100; GPU validated vs CPU (AIS RootMyc1 = 1.50 GPU vs 1.49 CPU).
- Graph rule: keep edges significant in >50% of the 54 cases; edge weight = mean across cases.

### 5. Result — the causal graph  *(figure: fig3-te-network)*
Wave-dominated directed structure: 7 significant edges, every one from Wave1Elev, none from wind.

### 6. Result — significant edges (7 of 18, mean across 54 cases)
| Edge | TE (nats) | te_frac | sig |
|---|---|---|---|
| Wave → PtfmPitch | **0.121** | 4.29% | 100% |
| Wave → PtfmHeave | 0.114 | 4.29% | 87% |
| Wave → FAIRTEN2  | 0.111 | 7.50% | 100% |
| Wave → FAIRTEN3  | 0.110 | 8.63% | 100% |
| Wave → PtfmSurge | 0.107 | 3.84% | 100% |
| Wave → TwrBsMyt  | 0.023 | 1.86% | 61% |
| Wave → FAIRTEN1  | 0.020 | 1.42% | 54% |

The five strongest edges cluster at 0.11–0.12 nats (no single dominant edge). By the normalised te_frac the mooring lines (FAIRTEN3 8.6%, FAIRTEN2 7.5%) rank highest.

Headline: **wave drives platform motion + mooring; no wind→structure edge is significant anywhere in the campaign.**

### 7. Triangulation — TE vs coherence vs Granger
Where TE is significant and the linear baselines are not = nonlinear directed coupling TE uniquely catches (e.g. wave 2nd-order difference-frequency → pitch). Where they agree = validates the embedding.

### 8. The wind paradox (open question)
- Wind→structure ≈ 0 **across 8–20 m/s** — counter to intuition (wind drives the turbine), and it holds at every operating point.
- **Not an artifact**: pick_tau shows wind decorrelates at ~11.6 s, well inside the 30 s window → wind is sampled, just not transferring.
- Hypothesis: the blade-pitch controller regulates rotor thrust, decoupling wind fluctuations from the structure — a causal "firewall."

### 9. Testing the firewall — controller-off ablation (preliminary, single case)
- Re-ran one case with pitch control frozen (open-loop).
- **Result: suggestive but inconclusive.** `Wind→PtfmHeave` appeared (0→0.017, sig), consistent with wind→thrust→heave once pitch is frozen — but the strong thrust loads (blade, tower) stayed ~0, and a controller-on wind→FAIRTEN2 edge (0.042 in *this single case only*) vanished.
- **Caveat:** that single-case Wind→FAIRTEN2 = 0.042 does **not** survive the campaign-wide >50% significance rule — it is a per-case artifact, not a campaign result. Keep it inside the ablation framing.
- **Confound (be upfront):** open-loop overspeeds → rotor self-dynamics inflate AIS (RootMyc1 1.50→2.05), which masks wind in *bivariate* TE. So this is not a surgical test.
- Next: conditional TE `TE(wind→Y|wave)` + a non-overspeeding ablation (or a controller-on below-vs-above-rated sweep).

### 10. Methods notes (a good "lessons" slide)
- GPU made the sweep tractable; one case ~35 h on a single A100-batched run.
- **Caution result**: data-driven embedding-delay (tau) from self-MI preserved AIS but **collapsed the TE edges** (tau=10: strongest Wave→PtfmPitch 0.12→0) — directed couplings live at specific lags; AIS embedding heuristics don't transfer to TE.

### 11. Limitations / future
- Single platform (UMaineSemi), sim-only — no field validation.
- max_lag=150 may be short for PtfmSurge (decorrelates ~24.6 s).
- Firewall mechanism (controller) is preliminary and confounded — the wind decoupling is shown, its cause is not.
- Next: conditional/multivariate TE, a non-overspeeding ablation, the Sobol parameter-causality graph (fig4/fig5), and feeding the ranked driver→load pathways into design-optimization weights.

### 12. Conclusion
- TE reveals a **wave-dominated causal structure** in FOWT response that linear methods only partially capture.
- The wind→structure decoupling is a robust, non-obvious finding holding across 8–20 m/s; whether the controller causes it is an open, testable question.

---
*Build order for slides: 1–7 are solid/validated. 8–9 are the interesting open thread (frame as preliminary). 10 is the methods/compute story. Figures already in reports/figs/: fig3-te-network, fig4-sobol, fig5-combined-graph.*
