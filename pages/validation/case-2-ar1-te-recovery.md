---
title: "Validation Case 2 — AR(1) TE known-answer recovery"
type: validation
created: 2026-05-12
updated: 2026-05-13
sources: []
tags: [validation, smoke-test, transfer-entropy]
status: PASS (first run; monotonicity sweep still pending)
---

## Goal

Verify that the [[entities/idtxl]] + [[concepts/ksg-estimator]] pipeline
recovers the directionality of a known-coupling AR(1) chain. This calibrates
hyperparameters before applying TE to OpenFAST data.

## Hypothesis

For
$$
X_{t+1} = a\,X_t + \varepsilon_t, \qquad
Y_{t+1} = b\,Y_t + c\,X_t + \eta_t
$$
with `a, b, c ∈ (0, 1)`, `ε`, `η` independent Gaussian noise:

- `TE(X → Y) > 0` and **statistically significant** (p < 0.05 vs surrogates).
- `TE(Y → X) ≈ 0` and **not** significant.
- `TE(X → Y)` is monotonic increasing in `c`.

## Method

1. Generate `N = 5 000` samples each of `X`, `Y` for `c ∈ {0.0, 0.2, 0.4, 0.6}`.
2. Run `BivariateTE` from IDTxl in both directions with KSG estimator,
   `n_perm_max_stat = 200` IAAFT surrogates.
3. Tabulate (`c`, TE_XY, p_XY, TE_YX, p_YX).

## KPI

| KPI | Pass criterion |
|---|---|
| `TE(X→Y) p` at `c=0` | ≥ 0.05 (no false positive) |
| `TE(Y→X) p` at any `c` | ≥ 0.05 |
| `TE(X→Y) p` at `c≥0.2` | < 0.05 |
| Monotonicity of `TE(X→Y)` in `c` | non-decreasing within MC error |

## Source artefacts (will be filled after run)

- Code: `analysis/te_pipeline.py` (test routine)
- Figure: `reports/figs/case-2-ar1-te-recovery.png`

## Status / notes — first-run PASS (2026-05-13)

Executed via `analysis/test_ar1_te.py` at `N=5000`, `c=0.6`, `n_perm=200`.

Result:
```
Generating AR(1) chain X→Y, n=5000, alpha=0.5, beta=0.5
  x: mean=−0.009, std=1.148
  y: mean=+0.025, std=1.558

Forward: TE(X → Y)
  TE = +0.1892 nats, p = 0.0050, significant = True

Reverse: TE(Y → X)
  TE = +0.0000 nats, p = 1.0000, significant = False
```

Both KPIs at `c = 0.6` pass:
- `TE(X→Y)` significant (p = 0.005 ≪ 0.05) and > 0 ✓
- `TE(Y→X)` not significant (no parents selected by greedy max-stat) ✓

**Pending**: the original case description also calls for a
monotonicity sweep over `c ∈ {0.0, 0.2, 0.4, 0.6}`. That sweep + the
figure at `reports/figs/case-2-ar1-te-recovery.png` is the next refinement
of this case; the **directional-recovery part** is already PASS.

**Implementation notes** (worth keeping for Phase 4):
- IDTxl bug with NumPy 2.x: `idtxl/stats.py:1535` calls `np.math.factorial`
  which no longer exists. Workaround: set `permute_in_time: True` in the
  settings dict — this is also the correct setting for a single-replication
  time series (shuffle within the time axis vs. between replications).
  Captured in `analysis/test_ar1_te.py:run_te`.
- IDTxl uses `pkg_resources` from setuptools; we pinned `setuptools<81`
  in `te-fowt` so the import still works. Documented in
  [[entities/idtxl]] *(setup notes)*.
- IDTxl was installed via a `.pth` file pointing at
  `repos/IDTxl/IDTxl-master/`, because the upstream `setup.py` requires
  a C compiler for the HDE Cython extension (which we don't use).

## Related

- [[concepts/transfer-entropy]] · [[concepts/ksg-estimator]] ·
  [[concepts/surrogate-significance]] · [[entities/idtxl]]
- Phase 4 of [[PLAN]]
