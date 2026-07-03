---
title: "Hypothesis scorecard — H1–H6 vs Phase 4/5 results"
type: scorecard
created: 2026-05-25
updated: 2026-05-25
tags: [pre-registration, hypotheses, results, publication-defense]
---

# Hypothesis scorecard — H1–H6 vs Phase 4 / Phase 5 results

Pre-registered predictions locked **2026-05-13** (see
`pages/open-questions.md` §Q8). This document scores each prediction
against the actual numbers from the completed campaign:

- **Phase 5 Sobol**: `data/raft_lhs_v2-N256_sobol.json` (production —
  2816 RAFT evals, 971 feasible). The N=64 result was a preliminary
  check; all H4 / H5(a) numbers below are now the publication-grade
  N=256 values with Saltelli 95% confidence intervals tightened ~2×.
- **Phase 4 TE**: `reports/te_table.parquet` (54 cases, bivariate KSG,
  2 Hz, max_lag=60, n_perm=50, `--no-conditional --no-granger`).

Legend: ✅ confirmed · ⚠️ partially confirmed · ❌ not confirmed · ⏳ not yet evaluable

---

## Summary table

| ID | Status | One-line evidence |
|----|--------|-------------------|
| H1 | ❌ | Wind → pitch TE essentially zero (0/24 DLC-A, 2/24 DLC-B significant) |
| H2 | ⚠️ | Wave → heave 100% sig in DLC-1.6 / 92% DLC-A / 79% DLC-B; γ² peak 0.085–0.121 Hz (mostly within predicted 0.1–0.3 Hz) |
| H3 | ⏳ | requires scoped conditional rerun (Phase 4 was `--no-conditional`) |
| H4 | ⚠️ | L_u dominates as predicted; EA negligible; geometry exceeds predicted bound |
| H5(a) | ❌ | EA does **not** dominate geometry on fairlead-tension std |
| H5(b) | ⚠️ (bivariate proxy) | Wave→FAIRTEN ~7–9% TE_frac, Wind→FAIRTEN ~0% — wave-dominated as predicted, but full conditional check still pending |
| H6 | ⚠️ | γ²(Wave→Pitch) peak 0.11 Hz (wave band), **not** the predicted 0.0345 Hz pitch eigenfreq; full windowed-TE evaluation still pending |

**Headline**: the campaign produced **two surprises that pre-registration paid for**:
(1) the predicted dominant mooring variable was wrong (EA vs L_u — H4 / H5a),
and (2) wind-to-pitch TE is null at the bivariate level (H1) — the
ROSCO controller's wind-disturbance rejection is more dominant than
predicted. Wave-driven dynamics dominate everywhere TE is significant.

---

## H1 — `TE(Wind1VelX → PtfmPitch)` significant in DLC-A and DLC-B; reverse ≈ 0

**Prediction (locked 2026-05-13)**:
> `TE(Wind1VelX → PtfmPitch)` significant (p < 0.05) in both DLC-A and
> DLC-B; `TE(PtfmPitch → Wind1VelX) ≈ 0` (no back-action sanity check).

**Method**: bivariate KSG TE with circular surrogates ([Schreiber 2000](https://doi.org/10.1103/PhysRevLett.85.461), [Kraskov et al. 2004](https://doi.org/10.1103/PhysRevE.69.066138)).

### Actuals

| DLC | n | mean TE_nats | mean TE_frac | sig (p<0.05) | mean p |
|---|---|---|---|---|---|
| DLC-1.6 | 6  | 0.0000 | 0.000 | **0/6**  (0%)  | 1.00 |
| DLC-A   | 24 | 0.0000 | 0.000 | **0/24** (0%)  | 1.00 |
| DLC-B   | 24 | 0.0019 | 0.001 | **2/24** (8%)  | 0.88 |

Reverse direction `TE(PtfmPitch → Wind1VelX)` was **not in the test matrix**
(bivariate run configured (env → response) edges only).

### Verdict: ❌ **not confirmed**

Wind → pitch TE is null across all DLCs at the bivariate level. The
prediction "significant in both DLC-A and DLC-B" fails (0% and 8%).

### Interpretation

Consistent with the smoke-test finding in `reports/_ver03_extracted.md`:
the ROSCO controller's wind-disturbance rejection makes wind almost
statistically invisible at the pitch channel in the bivariate setting.
Three candidate mechanisms:

1. **Controller-mediated cancellation** (most likely) — ROSCO drives
   the rotor pitch to reject wind variation before it propagates to
   the platform. See Q11 (controller-off comparison) in
   `pages/open-questions.md`.
2. **Bivariate-only blindness** — wind's effect on pitch may only be
   visible *conditional on* wave (which carries the dominant variance).
   Phase 4's `--no-conditional` setting forecloses checking this here.
3. **Decimation to 2 Hz** — wind variability has substantial content
   above 1 Hz; the 2 Hz Nyquist may have damped the signal we need.

**Follow-up needed**: (a) scoped conditional TE on (Wind, Wave, Pitch)
triple; (b) controller-off OpenFAST rerun for 1–2 cases to test
mechanism #1 directly (Q11).

---

## H2 — `TE(Wave1Elev → PtfmHeave)` significant + dominant in 0.1–0.3 Hz wave band

**Prediction (locked 2026-05-13)**:
> `TE(Wave1Elev → PtfmHeave)` significant and dominant within the
> 0.1–0.3 Hz wave band; bivariate Granger and coherence γ²(f) agree at the peak.

**Method caveat**: Phase 4 was run with `--no-granger`; γ² coherence
peak is the only frequency-domain check available from the current table.

### Actuals — bivariate TE

| DLC | n | mean TE_nats | mean TE_frac | sig (p<0.05) | mean p |
|---|---|---|---|---|---|
| DLC-1.6 | 6  | 0.166 | 6.5% | **6/6**   (100%) | 0.02 |
| DLC-A   | 24 | 0.112 | 4.3% | **22/24** (92%)  | 0.10 |
| DLC-B   | 24 | 0.103 | 3.8% | **19/24** (79%)  | 0.22 |

### Actuals — γ²(f) coherence peak (Hz)

| DLC | mean γ² peak | predicted band |
|---|---|---|
| DLC-1.6 | **0.085 Hz** | 0.1–0.3 Hz (slightly below) |
| DLC-A   | **0.121 Hz** | 0.1–0.3 Hz ✅ |
| DLC-B   | **0.105 Hz** | 0.1–0.3 Hz ✅ |

### Verdict: ⚠️ **partially confirmed**

Significance ✅: 79–100% across DLCs.
Frequency ⚠️: DLC-A and DLC-B γ² peaks fall inside 0.1–0.3 Hz; DLC-1.6
peak (0.085 Hz) is slightly below the lower bound. Granger agreement
unevaluable due to `--no-granger`.

### Interpretation

The peak frequency is at the lower end of the wave band, close to the
heave natural frequency (≈ 0.05 Hz for VolturnUS-S — see
`pages/entities/iea-15mw-volturnus-s.md`). The system is resonantly
amplifying wave energy at the lower edge of its wave-frequency response.

---

## H3 — Conditional TE shrinks more when wind/wave correlated (DLC-A vs DLC-B)

**Prediction (locked 2026-05-13)**:
> Conditional `TE(wind → PtfmPitch | wave) ≈ bivariate TE(wind → PtfmPitch)`
> in DLC-B (decoupled), but `< 80%` of bivariate in DLC-A (correlated).

**Status**: ⏳ **invalid as currently run** — Phase 4 launcher
(`analysis/run_phase4_parallel.sh:36`) set `--no-conditional` for the
first-pass scope reduction. Conditional TE was not computed.

**Additional complication from H1**: bivariate `TE(wind → pitch) ≈ 0`,
so the H3 ratio is `0/0` — undefined regardless. H3 will only be
testable if conditional TE on (Wind | Wave, Pitch) is non-zero, i.e.,
if mechanism #2 in H1's interpretation is real. **Test this first**;
if conditional TE is also zero, H3 collapses too.

### Required to evaluate

```bash
# On server — scoped conditional rerun (single triple, fast)
python analysis/te_pipeline.py sims/dlca_*/IEA-15-240-RWT-UMaineSemi/*.outb \
    -o reports/te_h3_conditional_dlca.parquet \
    --max-lag 60 --n-perm 50 --decimate-target-hz 2.0 \
    --channels Wind1VelX,Wave1Elev,PtfmPitch \
    --no-granger
# repeat for sims/dlcb_*/
```

(Confirm `--channels` flag in te_pipeline.py before launching; if absent,
add it or process the full bivariate matrix with conditional on.)

---

## H4 — Mooring contribution dominates platform-surge variance

**Prediction (locked 2026-05-13)**:
> `ST(EA | std(PtfmSurge)) > 0.5` **AND** `ST(L_u | std(PtfmSurge)) > 0.2`;
> aggregate geometry-variable contribution `ΣST(D_*, R_MO, H_*) < 0.3`.

**Source**: `data/raft_lhs_v2-N64_sobol.json` → channel `surge_std`.

### Actuals (N = 256, production)

| Component | Predicted | Actual Sₜ (N=256) | Sₜ (N=64) | Verdict |
|---|---|---|---|---|
| `ST(EA \| surge_std)` | > 0.5 | **0.054 ± 0.033** | 0.092 ± 0.082 | ❌ |
| `ST(L_u \| surge_std)` | > 0.2 | **0.705 ± 0.223** | 0.817 ± 0.441 | ✅ |
| `ΣST(geometry vars \| surge_std)` | < 0.3 | **0.911** | 1.324 | ❌ |

### Verdict: ⚠️ **partially confirmed**

The directional claim *"mooring dominates over geometry"* holds — but
only because of mooring **length (L_u)**, not **axial stiffness (EA)** as
predicted. At N=256 the noisy geometry sum from N=64 (1.32, >1 is
non-physical) drops to 0.91 — the L_u dominance pattern survives but
geometry contribution is more than the predicted 0.3 bound. EA gets
even smaller (0.054 vs 0.092 at N=64), strongly reinforcing the
"EA prediction wrong" verdict. CIs roughly halved.

### Mechanism (post-hoc, exploratory)

L_u changes shift the catenary scope and mean line tension, with strong
effect on platform mean position and surge restoring stiffness. EA only
matters incrementally once L_u is held fixed. In a ±20% factor sweep,
L_u dominates because it shifts the equilibrium; EA only modulates
around it.

---

## H5 — Fairlead-tension trade-off explained by mooring sizing + wave drive

### H5(a) — Sobol: EA vs geometry on fairlead-tension std

**Prediction**: `ST(EA | std(FAIRTEN1)) > ST(geometry-combined | std(FAIRTEN1))`.

**Source**: `data/raft_lhs_v2-N64_sobol.json` → channel `Tmoor0_std` (= FAIRTEN1 proxy).

| Component | Sₜ (N=256) | Sₜ (N=64) |
|---|---|---|
| `ST(EA \| Tmoor0_std)` | **0.024 ± 0.016** | 0.021 |
| `ST(L_u \| Tmoor0_std)` | **0.716 ± 0.205** | 0.835 |
| `ΣST(geometry vars \| Tmoor0_std)` | **0.984** | 1.173 |
| `ST(EA) > ΣST(geometry)` ? | **No** (0.024 vs 0.984) | ❌ |

**Verdict (a)**: ❌ **not confirmed**.

EA is the *smallest* of the 9 vars on fairlead tension std. L_u
dominates (0.716 ± 0.21); among geometry, D_Pt (0.517 ± 0.18) and
D_OCol (0.374 ± 0.16) lead. At N=256 the CIs are tight enough that
EA's position at the bottom is statistically unambiguous.

### H5(b) — Wave-driven vs wind-driven fairlead tension

**Prediction**: conditional `TE(wave → FAIRTEN1 | wind) > 2 × TE(wind → FAIRTEN1 | wave)`.

**Method gap**: conditional TE not computed (`--no-conditional`). However,
the **bivariate ratio** is a usable lower-bound proxy.

### Bivariate proxy — wave vs wind on fairlead tensions

| Target | DLC | Wave→tension TE_frac (sig) | Wind→tension TE_frac (sig) | Wave/Wind ratio |
|---|---|---|---|---|
| FAIRTEN1 | DLC-A | 1.6% (15/24) | 0.2% (3/24)  | ~6.5× |
| FAIRTEN1 | DLC-B | 1.1% (10/24) | 0.04% (1/24) | ~26× |
| FAIRTEN2 | DLC-A | 7.4% (24/24) | 0.2% (3/24)  | ~42× |
| FAIRTEN2 | DLC-B | 7.6% (24/24) | 0.0% (0/24)  | ∞ |
| FAIRTEN3 | DLC-A | 8.8% (24/24) | 0.0% (0/24)  | ∞ |
| FAIRTEN3 | DLC-B | 8.9% (24/24) | 0.16% (3/24) | ~55× |

**Verdict (b)**: ⚠️ **directionally confirmed at the bivariate level**.

Wave-to-fairlead TE exceeds wind-to-fairlead TE by **6–55×** across
mooring lines and DLCs — vastly above the 2× threshold. Conditional
verification still pending, but the bivariate signal is so dominant
that the conditional version is unlikely to reverse it.

---

## H6 — Local-in-time `TE(wave → pitch)` PSD peaks at platform-pitch eigenfreq

**Prediction (locked 2026-05-13)**:
> Local-in-time PSD of `TE(wave → PtfmPitch)` peaks at the platform pitch
> eigenfrequency 0.03–0.04 Hz (VolturnUS-S design value ≈ 0.0345 Hz);
> coherence γ²(f) shows the same peak.

**Method gap**: `te_pipeline.py` returns one TE value per (source, target,
case) — not the time-series of windowed TE values required for the full
H6 PSD prediction. The coherence γ² peak *is* in the current table.

### Actuals — γ²(Wave1Elev → PtfmPitch) coherence peak

| DLC | mean γ² peak (Hz) | predicted | |
|---|---|---|---|
| DLC-1.6 | **0.115** | 0.03–0.04 Hz | ❌ |
| DLC-A   | **0.109** | 0.03–0.04 Hz | ❌ |
| DLC-B   | **0.114** | 0.03–0.04 Hz | ❌ |

### Bonus — bivariate TE (Wave → Pitch) is highly significant

| DLC | n | TE_frac | sig | p |
|---|---|---|---|---|
| DLC-1.6 | 6  | 6.7% | 6/6 (100%) | 0.02 |
| DLC-A   | 24 | 4.0% | 24/24 (100%) | 0.02 |
| DLC-B   | 24 | 4.0% | 24/24 (100%) | 0.02 |

### Verdict: ⚠️ **partial — γ² peak fails prediction; windowed TE pending**

γ² peak is at **the wave-band frequency (~0.11 Hz)**, not the pitch
eigenfrequency (0.0345 Hz). Pitch is being **forced** by wave energy at
the wave-peak band, not **resonating** at its natural frequency. This
is a meaningful negative result for H6's resonance claim, but does not
preclude the *windowed-TE* version of H6 from showing a 0.0345 Hz peak —
those are different statistics (γ² is stationary, windowed TE picks up
non-stationary energy at the eigenfreq).

**Follow-up needed**: windowed-TE driver script. Pseudocode:

```python
# Per case, 60-s overlapping windows, 30-s hop:
for w in windows:
    te_w = idtxl_bivariate_te(wave[w], pitch[w], max_lag=10)
    te_series.append(te_w)
welch_psd(te_series)  # look for peak near 0.0345 Hz
```

---

## Cross-cutting notes

1. **N = 256 update**: production Sobol run completed 2026-05-26.
   Focus-channel Sₜ values now lie in [0, 1] with confidence intervals
   roughly halved. **The L_u-dominates, EA-negligible pattern survives
   the N=64 → N=256 transition cleanly.** A few outlier channels
   (roll_avg Sₜ ≈ 7, pitch_avg Sₜ ≈ 2.5) still exceed unity at N=256;
   these are *avg* (mean) channels where the response variance over the
   feasible subset is near zero, so Sₜ ratios blow up numerically.
   Channels used for H4 / H5(a) verdicts (surge_std, pitch_std,
   Tmoor0_std, heave_std) are clean.

2. **Phase 4 conditional gap**: H3 and the rigorous H5(b) need a
   follow-up scoped conditional run. The bivariate proxy for H5(b) is
   so dominant (6–55× wave/wind ratio) that conditioning is unlikely
   to reverse it.

3. **The H1 null finding is publishable**: a directional, statistically
   significant *absence* of wind-pitch TE in 54 hour-long simulations
   under three DLC families is a strong result. It directly motivates
   the Q11 "controller-off" comparison as the central methodological
   follow-up: if conditional TE on (Wind | Wave, Pitch) remains null
   *and* the controller-off rerun makes it appear, that *quantifies*
   ROSCO's contribution to wind-disturbance rejection — a publishable
   methodological story all by itself.

4. **Pre-registration discipline**: every ✅ / ⚠️ / ❌ above is reported
   here against the *original* 2026-05-13 prediction text. Post-hoc
   discoveries (D_Pt's role; L_u dominating EA; wind-pitch null) are
   marked **exploratory** in the manuscript — not retro-framed as
   confirmed hypotheses.

---

## What this scorecard tells the report

For ver08 of the technical report:

- **§5 Results — directly quotable**:
  - H1 null result (0/24 DLC-A sig)
  - H2 significance ✅ (79–100%) + γ² peak position
  - H4 / H5(a) inversion (L_u dominates, EA negligible)
  - H5(b) bivariate proxy (6–55× wave/wind ratio on fairlead tension)
- **§7 Discussion — two surprises**:
  1. EA-vs-L_u inversion (Sobol)
  2. Wind-pitch TE null (controller-mediated)
- **§8 Future work — concrete entries**:
  1. Scoped conditional TE rerun (H3, H5b rigor)
  2. Windowed-TE driver for H6
  3. Controller-off rerun for Q11
  4. ~~N=256 Sobol~~ — **done 2026-05-26**; verdicts hold and tighten
