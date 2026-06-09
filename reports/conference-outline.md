# Conference talk outline — TE causal discovery on a FOWT
*Draft 2026-06-09. Numbers from the validated controller-on run + the open-loop ablation. Single condition (11 m/s, DLC-A seed s00). Frame everything as preliminary.*

---

### 1. Title
Transfer-entropy causal discovery of environment→structure coupling in a floating offshore wind turbine (IEA-15MW on UMaine VolturnUS-S).

### 2. Motivation
- FOWT load/response analysis leans on coherence/correlation (association, symmetric) — not **directed causality**.
- Question: can information-theoretic **directed transfer** reveal which environmental driver causes which structural response, and pathways linear methods miss?

### 3. System & data
- IEA-15-240-RWT on UMaineSemi, OpenFAST (aero-hydro-servo-elastic), 3600 s, drop 600 s, decimate to 5 Hz.
- 2 sources (Wind1VelX, Wave1Elev) → 9 responses (RootMyc1, RootMxc1, TwrBsMyt, PtfmHeave/Surge/Pitch, FAIRTEN1/2/3).

### 4. Method
- **KSG transfer entropy** (Kraskov k=4), non-uniform embedding, max_lag=150 (30 s, covers slow-drift).
- **Circular-shift surrogates** ×200, p<0.05, max-stat correction.
- **AIS-normalised effect size** te_frac = TE/(H(Y)−AIS(Y)).
- **Two linear baselines, same pipeline**: Gaussian/Granger (estimator swap) + coherence (scipy).
- Compute: OpenCL on 2× A100; GPU validated vs CPU (AIS RootMyc1 = 1.50 GPU vs 1.49 CPU).

### 5. Result — the causal graph  *(figure: fig3-te-network)*
Wave-dominated directed structure.

### 6. Result — significant edges (controller-on, 6/18)
| Edge | TE (nats) |
|---|---|
| Wave → PtfmPitch | **0.211** (dominant) |
| Wave → FAIRTEN2  | 0.118 |
| Wave → PtfmSurge | 0.065 |
| **Wind → FAIRTEN2** | 0.042 (only wind edge) |
| Wave → TwrBsMyt  | 0.031 |
| Wave → RootMxc1  | 0.002 |

Headline: **wave drives platform motion + mooring; wind shows almost no directed transfer.**

### 7. Triangulation — TE vs coherence vs Granger
Where TE is significant and the linear baselines are not = nonlinear directed coupling TE uniquely catches (e.g. wave 2nd-order difference-frequency → pitch). Where they agree = validates the embedding.

### 8. The wind paradox (open question)
- Wind→structure ≈ 0 at rated — counter to intuition (wind drives the turbine).
- **Not an artifact**: pick_tau shows wind decorrelates at ~11.6 s, well inside the 30 s window → wind is sampled, just not transferring.
- Hypothesis: the blade-pitch controller regulates rotor thrust, decoupling wind fluctuations from the structure — a causal "firewall."

### 9. Testing the firewall — controller-off ablation (preliminary)
- Re-ran the same case with pitch control frozen (open-loop).
- **Result: suggestive but inconclusive.** `Wind→PtfmHeave` appeared (0→0.017, sig), consistent with wind→thrust→heave once pitch is frozen — but the strong thrust loads (blade, tower) stayed ~0, and the controller-on wind edge (FAIRTEN2) vanished.
- **Confound (be upfront):** open-loop overspeeds → rotor self-dynamics inflate AIS (RootMyc1 1.50→2.05), which masks wind in *bivariate* TE. So this is not a surgical test.
- Next: conditional TE `TE(wind→Y|wave)` + a non-overspeeding ablation (or a controller-on below-vs-above-rated sweep).

### 10. Methods notes (a good "lessons" slide)
- GPU made the sweep tractable; one case 35 h on a single A100-batched run.
- **Caution result**: data-driven embedding-delay (tau) from self-MI preserved AIS but **collapsed the TE edges** (tau=10: dominant Wave→PtfmPitch 0.21→0) — directed couplings live at specific lags; AIS embedding heuristics don't transfer to TE.

### 11. Limitations / future
- Single condition (11 m/s), single platform, sim-only.
- max_lag=150 may be short for PtfmSurge (decorrelates ~24.6 s).
- Next: multi-condition operating-point sweep, conditional/multivariate TE, ensemble TE across seeds, the Sobol parameter-causality graph (fig4/fig5).

### 12. Conclusion
- TE reveals a **wave-dominated causal structure** in FOWT response that linear methods only partially capture.
- The wind→structure decoupling is a robust, non-obvious finding; whether the controller causes it is an open, testable question.

---
*Build order for slides: 1–7 are solid/validated. 8–9 are the interesting open thread (frame as preliminary). 10 is the methods/compute story. Figures already in reports/figs/: fig3-te-network, fig4-sobol, fig5-combined-graph.*
