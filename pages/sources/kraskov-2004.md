---
title: "Kraskov, Stögbauer, Grassberger 2004 — Estimating Mutual Information"
type: source
created: 2026-05-12
updated: 2026-05-12
source_path: "raw/papers/0305641v1.pdf"
authors: ["Kraskov, A.", "Stögbauer, H.", "Grassberger, P."]
year: 2004
venue: "Physical Review E"
doi: "10.1103/PhysRevE.69.066138"
citation_key: "kraskov-2004"
tags: [source, mutual-information, estimator, foundational]
sources: []
---

## Citation

Kraskov, A., Stögbauer, H., & Grassberger, P. (2004). "Estimating Mutual
Information." *Physical Review E* **69**, 066138. arXiv:cond-mat/0305641.

## TL;DR

- Introduces **two classes of MI estimators** based on **k-nearest-neighbour
  distances** in the joint space, derived from Kozachenko-Leonenko entropy
  estimators. The "KSG" name in the literature refers to these.
- **Two algorithm variants** differ in how marginal counts are taken:
  - I⁽¹⁾: count points strictly within ε(i)/2 in each marginal subspace
  - I⁽²⁾: use a rectangle whose edges are ε_x(i)/2 and ε_y(i)/2 (often
    different lengths)
- **Both estimators are exact for independent variables** — `Î(X,Y) → 0`
  identically (up to statistical fluctuations) when `μ(x,y) = μ_x(x)μ_y(y)`.
  This is a strong, "surprising" property the authors emphasise.
- Data-efficient: with k=1, the estimator "resolves structures down to the
  smallest possible scales." Adaptive: resolution is higher where data is
  denser. Minimal bias.
- Higher-dim generalisation given (Eq. 30) — essential because TE is a
  conditional MI in a (k_target + l_source + 1)-dimensional space.

## Key claims

- "I⁽¹⁾ and I⁽²⁾ vanish (up to statistical fluctuations) for independent
  distributions" — verified numerically for Gaussian, uniform, exponential,
  and gamma-exponential cases.
- Statistical errors scale as ~1/√N.
- **Practical k recommendation**: "We propose to use typically `k = 2` to
  `4`, except when testing for independence. In the latter case … taking
  `k` to be very large (up to `k ≈ N/2`, say)" minimises statistical errors.
- **Empirical-data caveat**: "Empirical data usually are obtained with few
  (e.g. 12 or 16) binary digits, which means that many points in a large
  set may have identical coordinates. … **The simplest way out of this
  dilemma is to add very low amplitude noise to the data (≈ 10⁻¹⁰, say,
  when working with double precision) which breaks this degeneracy.**"
  Critical for FOWT data after decimation.
- Estimators outperform Darbellay-Vajda (binning) over a wide range of
  cases (Figs. 8, 11, 12).

## Equations introduced

- [[equations/eq-mutual-information]] — the continuous-density definition
  (Eq. 1 of the paper).
- The two KSG estimators (Eqs. 8, 9 of the paper) — formalised in the
  [[concepts/ksg-estimator]] concept page.

## Methods

Kozachenko-Leonenko k-NN entropy estimate (Eq. 4) plus a clever bias
cancellation by using **different k values per marginal** (the `n_x`, `n_y`
neighbour counts). Uses **maximum norm** in joint space to make the marginal
estimates coherent. Fast neighbour search via box-grids / kd-trees gives
O(N√(kN)) complexity in 2-d.

## Data / cases

- Correlated Gaussians (exact `I = -½ log(1-r²)`) — Figs. 2, 4, 5
- Gamma-exponential distribution — Figs. 10, 11
- Ordered Weinman distribution — Fig. 12
- "Circle" distribution — Fig. 13

## How it informs this project

- This is **the estimator we will use** in [[entities/idtxl]] for both TE
  and MI. The 10⁻¹⁰ noise trick will be applied in `analysis/te_pipeline.py`
  after decimation of OpenFAST outputs to 5–10 Hz, to avoid neighbour
  degeneracies from finite-precision data.
- The k recommendation (k=2-4 for normal use) calibrates our hyperparameter
  choices in [[validation/case-2-ar1-te-recovery]] and Phase 4.
- The "exact for independence" property is the *theoretical basis* for the
  surrogate-significance test ([[concepts/surrogate-significance]]) being
  meaningful: under the true null (independence), KSG returns 0 in
  expectation, so any positive shift is signal + bias, not pure bias.
- The higher-dim formula (Eq. 30) underwrites our conditional TE: it's a
  conditional MI in (k+l+1)-dim space, estimated coherently with the same
  k value.

## Open questions / contradictions

- Statistical errors scale ~1/√N (Sec. III) but systematic errors decrease
  much faster (∼1/N for large N) — for our typical post-decimation N ≈
  10⁴–10⁵, statistical errors are likely to dominate. Need to size our
  surrogate count `n_perm` to control type-I error against this scale.
- The paper does not directly address the bias of TE (it's an MI paper) —
  TE adds a target self-history conditioning that the bias analysis here
  does not cover. We rely on surrogates for TE-specific bias correction.
