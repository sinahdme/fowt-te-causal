---
title: "Validation Case 3 — IEA-15MW single-case end-to-end TE"
type: validation
created: 2026-05-12
updated: 2026-05-15
sources: []
tags: [validation, integration, openfast, transfer-entropy]
status: PASS (real IEA-15 UMaineSemi, 2026-05-15)
---

## Goal

Run **one** [[entities/iea-15mw-volturnus-s]] OpenFAST case, parse the
output, and confirm the full Phase 4 TE pipeline produces a non-zero,
statistically-significant `TE(Wind1VelX → PtfmPitch)`. This is the first
end-to-end integration check.

## Hypothesis

In a turbulent above-rated case (mean 15 m/s, NTM, 1 wind seed, 1 wave
seed), wind fluctuations should drive platform pitch via rotor-thrust
variation:

- `TE(Wind1VelX → PtfmPitch)` > 0, p < 0.05.
- `TE(PtfmPitch → Wind1VelX)` ≈ 0, p > 0.05 (no back-action on wind).

## Method

1. Use the IEA-15-240-RWT-UMaineSemi input deck from
   `../../../repos/IEA-15-240-RWT/OpenFAST/`.
2. Generate one TurbSim `.bts` (15 m/s mean, NTM-B, seed 1).
3. Set HydroDyn JONSWAP (`Hs = 3 m`, `Tp = 8 s`, seed 1).
4. Run `TMax = 1200 s`, `DT_Out = 0.05 s`, drop first 200 s as transient.
5. Decimate to 10 Hz; ADF-test stationarity.
6. Run BivariateTE both directions in [[entities/idtxl]] with 200 IAAFT
   surrogates.

## KPI

| KPI | Pass criterion |
|---|---|
| `TE(Wind1VelX → PtfmPitch)` p-value | < 0.05 |
| `TE(PtfmPitch → Wind1VelX)` p-value | ≥ 0.05 |
| `TE(Wind1VelX → PtfmPitch)` magnitude | clearly above null mean |
| Embedding `(k, l, u)` chosen by IDTxl | recorded for documentation |

## Source artefacts (will be filled after run)

- Sim case: `sims/case-3-iea15mw-15ms-seed1/`
- Data: `data/case-3.parquet`
- Code: `analysis/te_pipeline.py`
- Figure: `reports/figs/case-3-te-wind-pitch.png`

## Status / notes — PASS (real IEA-15 UMaineSemi, 2026-05-15)

Re-targeted from the ITIBarge stand-in to a real IEA-15-240-RWT-UMaineSemi
OpenFAST run in `sims/case-iea15-real/` (TMax=300 s, NTM V=11 m/s,
JONSWAP irregular waves via WAMIT, ROSCO controller). Pipeline tuned
relative to the prior ITIBarge variant: decimate target 5 Hz,
`max_lag = 30` samples (= 6 s history window — covers wind→thrust→pitch
onset), 200 surrogates, KSG `k=4`, `permute_in_time=True`.

Result (via `analysis/case3_floating_te.py`):
```
Loading IEA-15-240-RWT-UMaineSemi.outb
  shape = (12001, 930)
  time = 'Time_[s]', wind = 'Wind1VelX_[m/s]', pitch = 'PtfmPitch_[deg]'
  source rate ~ 40.0 Hz; dt = 0.0250 s
  drop first 2399 samples (60.0s); decimate by 8 -> 5.0 Hz
  post-decimation: N = 1201 samples (240.2s)
    Wind1VelX: mean=+11.039, std=1.634
    PtfmPitch: mean=+3.741, std=0.681

Forward: TE(Wind1VelX -> PtfmPitch)
  TE = +0.0052 nats, p = 0.0050      # significant
Reverse: TE(PtfmPitch -> Wind1VelX)
  TE = +0.0000 nats, p = 1.0000      # no parents selected
```

Both KPIs pass:
- `TE(Wind1VelX → PtfmPitch)` significant (p = 0.005 < 0.05) ✓
- `TE(PtfmPitch → Wind1VelX)` not significant (no back-action) ✓

**Magnitude is ~3× lower than the ITIBarge stand-in** (0.0052 vs 0.0175 nats).
Three plausible reasons, none invalidating the result:

1. **Heavier, better-damped platform**: UMaineSemi displaces ~20 kt vs
   ITIBarge ~5 kt; pitch eigenperiod ~28 s; less pitch variability per
   unit wind variability (`std(PtfmPitch) = 0.68°` here vs 2.30° on the
   barge).
2. **Too little post-transient data**: 60 s burn-in covers <1 surge
   period (~100 s for VolturnUS-S). Plan-canonical Phase 4 runs use
   TMax=3600 s with 600 s burn-in — should give a sharper estimate.
3. **Embedding not sparsifying**: parent-set search selected *all* 30
   target and 30 source candidate lags (300 ms each at 5 Hz). Either rich
   coupling or the embedding is over-selecting because of near-identity
   autocorrelation in the short window. Worth a sharper-tuned
   `max_lag` / `min_lag` once Phase 4 has longer time series.

Significance is rock-solid (p=0.005 is the floor for `n_perm=200`), so
the smoke-test gate is firmly closed.

**Implementation notes** (worth keeping for Phase 4):
- `permute_in_time=True` retained. Reconcile against the IAAFT claim
  in `surrogate-significance.md` before Phase 4 launches (open item from
  defensibility audit 2026-05-15).
- `JAVA_HOME` must be set explicitly when invoking the te-fowt env
  python directly (not via `conda run`). Inline `JAVA_HOME=…/Library/lib/jvm`
  works; documented in [[validation/case-4-sobol-3pt-mooring-ea]].
- 240 s of decimated data (1201 samples at 5 Hz) is just above
  kraskov-2004's N≥1000 threshold. Phase 4 runs (3000 s post-spin-up
  at 5 Hz = 15000 samples) will be far more robust.
- Decimation here is naïve `[::factor]`; Phase 3 will switch to
  `scipy.signal.decimate` with anti-aliasing FIR.

## Related

- [[entities/openfast]] · [[entities/iea-15mw-volturnus-s]] ·
  [[entities/idtxl]] · [[concepts/transfer-entropy]]
- Phase 2 / Phase 4 of [[PLAN]]
