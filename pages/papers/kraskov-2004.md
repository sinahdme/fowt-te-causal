---
title: "Paper — Kraskov 2004 deep read"
type: paper
created: 2026-05-12
updated: 2026-05-12
sources: ["kraskov-2004"]
tags: [paper, mutual-information, ksg, estimator, deep-read]
---

Companion to [[sources/kraskov-2004]]. Deeper analytical read of the KSG
estimator paper — derivation re-check, comparison to alternatives,
project-specific implications.

## Derivation chain (re-checked)

The KSG estimator generalises the **Kozachenko-Leonenko** k-NN entropy
estimator to mutual information by exploiting the identity
`I(X;Y) = H(X) + H(Y) − H(X,Y)` (Eq. 5 of the paper).

The naïve approach of estimating each of the three entropies independently
with a fixed `k` would give cancelling biases only if the biases are
identical — which they aren't, because the distance scales differ between
the joint and marginal spaces. KSG's trick is:

1. Use a **single distance scale `ε(i)`** (the k-th-NN distance in the
   joint space) for all three estimates.
2. Count marginal neighbours `n_x(i)`, `n_y(i)` *within* that scale, rather
   than running a separate k-NN search in each marginal.
3. Plug the counts into modified Kozachenko-Leonenko formulae that account
   for the use of a shared scale.

The result (Eq. 8 of the paper):

$$
I^{(1)}(X,Y) = \psi(k) - \langle \psi(n_x+1) + \psi(n_y+1) \rangle + \psi(N)
$$

where ψ is the digamma function. Biases in the entropy estimates cancel by
construction because the same `ε(i)` is used for all of them.

The second estimator (Eq. 9) is the same idea with rectangular rather than
square ε-balls in the marginal-counting step:

$$
I^{(2)}(X,Y) = \psi(k) - 1/k - \langle \psi(n_x) + \psi(n_y) \rangle + \psi(N)
$$

I⁽²⁾ has slightly smaller statistical errors but slightly larger systematic
errors — this is the trade-off documented in Figs. 4-5.

## The "exact for independence" property (and why it matters)

The conjecture established in the paper (Sec. III, p. 5): both estimators
return **identically zero (within statistical fluctuations) for
independent variables**. This is verified across Gaussian, uniform,
exponential, gamma-exponential distributions.

Why this matters for TE / surrogate testing:
- The null hypothesis in [[concepts/surrogate-significance]] is
  independence between source and target.
- If the estimator returned a positive bias under the null, surrogate
  testing would have to subtract that bias — adding noise and complicating
  the analysis.
- Because KSG returns 0 in expectation under the null, the entire shift
  is signal: `TE_observed − TE_surrogate ≈ TE_true` cleanly.

This is the *theoretical justification* for why we can use IDTxl + KSG +
surrogate tests as a sound hypothesis-test pipeline, and not just as a
"compare with whatever the estimator outputs for shuffled data" hack.

## Comparison to alternatives

| Method | Bias for independence | Smoothness assumption | Cost | Notes |
|---|---|---|---|---|
| Histogram / binning | depends on bins | none | O(N) | Bias dominated by bin choice; struggles in higher dims |
| Adaptive binning (Darbellay-Vajda) | small | none | O(N log N) | Fig. 8: roughly 10× larger errors than KSG |
| Kernel density (Schreiber 2000 style) | bias depends on bandwidth | smooth densities | O(N²) naive | Hard to tune; bandwidth bias is real |
| **KSG-1, KSG-2** | **exact in expectation** | smooth marginals | O(N log N) with kd-tree | Adaptive, no bandwidth |

For our FOWT pipeline, KSG is the unambiguous choice. Binning would
struggle in the (k+l+1)-dim joint space for conditional TE; kernel methods
require bandwidth tuning per channel pair.

## Practical recommendations (verbatim quotes)

- **Choice of `k`**: "We propose to use typically `k = 2` to `4`, except
  when testing for independence. In the latter case we do not have to
  worry about systematic errors, and statistical errors are minimized by
  taking `k` to be very large (up to `k ≈ N/2`, say)."
- **Discrete-data trap**: "Empirical data usually are obtained with few
  (e.g. 12 or 16) binary digits, which means that many points in a large
  set may have identical coordinates. … **The simplest way out of this
  dilemma is to add very low amplitude noise to the data (≈ 10⁻¹⁰, say,
  when working with double precision) which breaks this degeneracy.**"
- **Rank ordering**: "Often, MI is estimated after rank ordering the data,
  i.e. after replacing the coordinate `x_i` by the rank of the `i`-th
  point when sorted by magnitude." Invariant under monotone transforms.
  We will *not* rank-order for TE (would destroy temporal embedding) but
  may use it for the static Phase 5 parameter→stat MI ranking.
- **Fast neighbour search**: "An algorithm with complexity `O(N√(kN))`
  is then obtained by first ranking the `x_i` by magnitude … Most results
  in this paper were obtained by this method which is suitable for `N`
  up to a few thousands. The fastest (but also most complex) algorithm
  is obtained by using grids ('boxes')."

## Project-specific implications

1. **Add 10⁻¹⁰ Gaussian noise to FOWT decimated data in
   `analysis/load_runs.py`** before passing to IDTxl. Implement as a
   utility `apply_neighbour_jitter(df, scale=1e-10)`. This avoids the
   "many identical neighbours" trap mentioned in the paper.
2. **Default `k=4` for TE estimation, `k=N/4` for surrogate
   independence-tests** — calibrate in
   [[validation/case-2-ar1-te-recovery]].
3. **Use rank-ordering for Phase 5 parameter→statistic MI** — invariant
   under monotone transforms of the parameter, so we don't have to worry
   about whether `EA` or `log(EA)` is the "right" parameterisation.
4. **Higher-dim MI / conditional MI** (Eq. 30 of the paper) is what
   IDTxl's `JidtKraskovCMI` estimator uses under the hood. Same KSG idea,
   same independence property, same bias-cancellation argument — extends
   cleanly to the dimensions we need for conditional TE.

## Lingering questions

- The paper's error scaling is for Gaussian and a few other smooth
  distributions. FOWT signals are *not* Gaussian (heavy-tailed extremes,
  multi-modal under bifurcations). Should monitor estimate stability vs
  `k` and vs `N` empirically in
  [[validation/case-3-iea15-single-case-te]].
- The "exact for independence" conjecture is verified numerically but
  not proven. For our purposes the numerical evidence is sufficient.

## Related

- [[sources/kraskov-2004]] · [[concepts/ksg-estimator]] ·
  [[concepts/mutual-information]] · [[equations/eq-mutual-information]]
- [[papers/schreiber-2000]] — the TE definition this estimator implements
- [[papers/wollstadt-2019]] — the toolbox that wraps this estimator
