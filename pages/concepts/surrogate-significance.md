---
title: "Surrogate Significance Testing"
type: concept
created: 2026-05-12
updated: 2026-05-15
sources: ["kraskov-2004", "wollstadt-2019", "schreiber-2000"]
tags: [information-theory, statistics, hypothesis-testing]
---

## Definition

Estimated [[concepts/transfer-entropy]] values are positive even for
unrelated processes due to finite-sample fluctuations. We test against a
**null distribution** built from surrogate data that destroys the directed
coupling while preserving marginals and/or spectra.

## Why it matters here

Without significance testing, every TE estimate looks "informative". The
surrogate test gives the per-pair p-value that we use to keep / drop edges
in the final causal graph (Phase 6). Per [[sources/wollstadt-2019]],
significance-testing is also the **stopping criterion** for IDTxl's greedy
multivariate-TE parent search: *"Rigorous statistical controls (based on
comparison to null distributions from time-series surrogates) are used to
gate parent selection and to provide automatic stopping conditions for the
inference."*

## Why this works in theory (KSG-specific)

The [[concepts/ksg-estimator]] is **exact for independent variables** —
kraskov-2004 (Sec. III) shows this numerically across Gaussian, uniform,
exponential, and gamma-exponential distributions: *"In all cases we found
that both estimators become exact for independent variables."*

Under the surrogate null (independence by construction), the estimator
returns zero in expectation. Therefore any observed shift `T_obs −
mean(T_null)` is true signal, not estimator bias. This is the
*theoretical* justification for the surrogate test being meaningful and
not just a "compare-with-shuffled-data" hack.

## Surrogate types — and what [[entities/idtxl]] supports natively

| Method | Preserves | Destroys | IDTxl native? |
|---|---|---|---|
| **Permute replications** | Each replication's full temporal structure | Cross-replication coupling | ✓ default (needs ≥ enough replications) |
| **Circular shift** | Auto-correlation, power spectrum, marginal distribution (exactly) | Cross-time-lag relations | ✓ `perm_type='circular'` |
| **Block / local permutation** | Short-range dependence | Long-range coupling | ✓ `perm_type='block'` / `'local'` |
| **Random permutation** | Marginal distribution | Everything else (incl. auto-correlation) | ✓ `perm_type='random'` (IDTxl default — weakest null) |
| **IAAFT** (iterative amplitude-adjusted Fourier transform, [[sources/schreiber-2000]] §IV) | Marginal distribution + power spectrum (to small numerical tolerance via iterative refinement) | Phase coupling | ✗ **not in IDTxl** — would need external generator |

### What we use in this project (locked 2026-05-15)

For **single-replication time series** (every Phase 2 / Phase 4 run is
1 replication: one OpenFAST seed → one `.outb`), `permute_replications`
is unavailable. The settings dict in `analysis/case3_floating_te.py` and
`analysis/test_ar1_te.py` therefore sets:

```python
"permute_in_time": True,
"perm_type": "circular",
```

**Why circular over IDTxl's default `'random'`**: FOWT response channels
have strong auto-correlation at the wave (~0.1 Hz) and platform-pitch
(~0.035 Hz) frequencies. `'random'` destroys this auto-correlation
along with the cross-coupling → null distribution becomes broader →
**false positives**. Circular shift preserves the source's power
spectrum exactly while destroying its temporal alignment with the
target — exactly the null we want to reject.

**Why not true IAAFT**: not natively in IDTxl, and for our use case
(single source-target pair per surrogate batch) circular shift gives
equivalent spectrum preservation with a simpler implementation. True
IAAFT (Schreiber & Schmitz 2000) is an upgrade path for the
publication baseline if a reviewer asks: generate surrogates externally,
pass via IDTxl's surrogate hook. Not on the critical path.

## Procedure

1. Estimate `T_obs = TE(X → Y)` on real data.
2. Build `N ≥ 200` surrogates of `X` via circular shift (random shift
   `k ∈ [1, n/2]`; surrogate `X*[t] = X[(t-k) mod n]`).
3. Estimate `T_null_i = TE(X*_i → Y)` for each.
4. p-value = fraction of `T_null_i ≥ T_obs`. With `n_perm=200` the
   minimum achievable p-value is `1/200 = 0.005`.

[[entities/idtxl]] handles this loop automatically when `n_perm_max_stat`
is set on the analyser. wollstadt-2019 also describes **family-wise error
correction** (max-statistic across candidate sources) — critical when
scanning the full Phase 4 channel matrix to control the network-level
type-I error rate.

## Related concepts

- [[concepts/transfer-entropy]] · [[concepts/ksg-estimator]] ·
  [[concepts/conditional-transfer-entropy]]

## Sources

- [[sources/wollstadt-2019]] — IDTxl methods paper (significance-testing
  workflow + family-wise correction).
- [[sources/kraskov-2004]] — the estimator's independence property that
  makes the test sound.
