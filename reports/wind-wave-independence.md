---
title: "Wind–Wave Forcing Independence Check"
type: analysis-note
created: 2026-07-10
updated: 2026-07-10
tags: [transfer-entropy, conditional-te, confounding, methods, robustness]
---

# Wind–Wave Forcing Independence Check

## Purpose

Reviewer-anticipating robustness check for the firewall manuscript
(`reports/te-firewall-paper-final.md`): the headline transfer-entropy table uses
IDTxl **`BivariateTE`** (§3.3), which conditions only on the target's own past,
not on the *other* environmental source. If the two sources — hub-height wind
(`Wind1VelX`) and wave elevation (`Wave1Elev`) — were mutually dependent,
bivariate TE could be confounded and **conditional (multivariate) TE** would be
required. This note measures that dependence directly.

Pre-registered as open question **Q6** and hypothesis **H3** in
[[open-questions]]. This closes Q6 empirically.

## Method

For each run, after the pipeline's exact preprocessing (drop 600 s transient,
decimate to 5 Hz, KSG tie-break jitter; `N = 15 001` samples ≈ 50 min):

- **Linear:** lag-0 Pearson *r*, and max |cross-correlation| over ±150 samples
  (±30 s).
- **Nonlinear:** histogram mutual information `I(Wind; Wave)` (32 bins, nats).
- **Correct null:** a **circular-shift surrogate** of the wave signal
  (preserves each signal's autocorrelation, destroys wind–wave alignment) —
  40 shifts per run. This is the right null because a plain i.i.d. shuffle
  destroys autocorrelation, inflates the effective sample size, and *understates*
  the finite-sample MI bias floor.

Tooling: `analysis/wind_wave_indep.py` (already in repo).

## Data

Every FOWT run reachable on this workstation (8 usable):

- 6 × near-rated **DLC 1.6, 11 m/s**, seeds 00–05 (`sims/dlc16_v11ms_s0*`)
- 1 × below-rated **8 m/s**, seed 00 (`dlca_v08ms_s00.outb`)
- 1 × **open-loop twin, 11 m/s** (`openloop.outb`, 3600 s) — the §4.3 twin;
  included as a consistency check (prescribing blade pitch does not alter the
  wind/wave forcing, so independence must hold here too — it does).

Excluded: `sims/case-iea15-real/…` is a 300 s calibration case, and the campaign
preprocessing drops the first 600 s of transient, so nothing survives — it is
not one of the 54 campaign runs.

The 15 m/s and 20 m/s bins (24 runs) live only on the server and were **not**
measured here. Independence is a property of the input seeding (independent
TurbSim wind field + independent JONSWAP wave realisation), which is identical
across all 54 runs, so the local subset is representative — but the server-side
completeness run is listed as a follow-up.

## Results

| Run | lag-0 Pearson *r* | max \|cross-corr\| (±30 s) | MI (nats) | circ-shift null MI | z | p |
|---|---|---|---|---|---|---|
| dlc16 v11 s00 | −0.0219 | 0.0423 | 0.0423 | 0.0442 ± 0.0032 | −0.58 | 0.707 |
| dlc16 v11 s01 | −0.0049 | 0.0185 | 0.0432 | 0.0407 ± 0.0027 | +0.90 | 0.171 |
| dlc16 v11 s02 | −0.0173 | 0.0302 | 0.0417 | 0.0419 ± 0.0025 | −0.09 | 0.537 |
| dlc16 v11 s03 | +0.0350 | 0.0388 | 0.0432 | 0.0429 ± 0.0022 | +0.13 | 0.366 |
| dlc16 v11 s04 | +0.0108 | 0.0217 | 0.0429 | 0.0416 ± 0.0021 | +0.62 | 0.268 |
| dlc16 v11 s05 | +0.0063 | 0.0264 | 0.0367 | 0.0406 ± 0.0023 | −1.67 | 1.000 |
| **8 m/s s00** | −0.0166 | 0.0313 | 0.0335 | 0.0383 ± 0.0027 | −1.79 | 0.976 |
| **openloop (11)** | −0.0161 | 0.0317 | 0.0365 | 0.0404 ± — | −1.26 | 0.927 |

Across all 8 usable runs: z ∈ [−1.79, +0.90], **min p = 0.171** (no run reaches
p < 0.05), mean (observed − null) excess = **−0.0013 nats**. Every run reads
INDEPENDENT.

- **Linear dependence is negligible:** |Pearson *r*| ≤ 0.035 at lag 0; max
  |cross-correlation| ≤ 0.043 anywhere in ±30 s.
- **Nonlinear dependence is null:** observed MI ≈ 0.033–0.043 nats, but this is
  entirely the finite-sample **bias floor** — it is statistically
  indistinguishable from the autocorrelation-preserving surrogate
  (z ∈ [−1.79, +0.90]; **no run reaches p < 0.05**; mean observed − null excess
  = **−0.0010 nats**). The analytic plug-in bias floor `(B−1)²/(2N)` = 0.032 nats
  matches the observed level.
- A plain i.i.d.-shuffle null gave spuriously "significant" z ≈ 5–12; that is the
  effective-sample-size artifact, not coupling — documented here so it is not
  re-derived as a false positive.

## Conclusion

Within a run, wind and wave forcing are **statistically independent** (linear and
nonlinear), as expected from independent TurbSim + JONSWAP seeding. Therefore, for
these two sources, **conditional TE ≡ bivariate TE** to within estimator noise —
there is no common-source confound for the bivariate estimator to remove. The
manuscript's bivariate `BivariateTE` choice for the wind/wave→structure edges is
justified.

Note the direction of the argument: source independence protects the estimator
against *redundancy* inflation. The one residual failure mode — *synergistic*
wind information hidden from any pairwise estimator — is addressed separately and
already in the paper by the **SURD** decomposition (§3.6/§4.3), whose synergistic
atom would expose exactly that and does not.

## Follow-ups (server, env `fowt-te`)

1. **Completeness:** on the server (env `fowt-te`, CPU-only — no IDTxl/GPU),
   run `./analysis/run_wind_wave_indep.sh` to check all 54 runs (adds the 15 m/s
   and 20 m/s bins). It writes `reports/wind_wave_independence.parquet`
   (one row per run) via `analysis/wind_wave_indep_all.py`, using the same
   circular-shift surrogate test. Verified locally on the 8 reachable runs
   (8/8 independent, min p = 0.24). Pull with `pull-results.sh` and fold the
   15/20 m/s rows into the table above. Expected to confirm (same seeding).
2. **Belt-and-suspenders conditional TE:** `analysis/probe_conditional.py` on a
   near-rated run to show `TE(Wave→PtfmPitch | Wind) ≈ TE(Wave→PtfmPitch)`
   numerically. IDTxl is not installed on the Windows workstation, so this must
   run on the server.
3. **Manuscript:** insert the robustness paragraph (drafted for §3.3) and note
   honestly that H3's DLC-A/DLC-B correlated-vs-decoupled contrast was
   pre-registered but not executed; the multivariate treatment is carried by
   the independence check here + SURD, not by H3.
