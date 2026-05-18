---
title: "Paper — Schreiber 2000 deep read"
type: paper
created: 2026-05-12
updated: 2026-05-12
sources: ["schreiber-2000"]
tags: [paper, transfer-entropy, foundational, deep-read]
---

Companion to [[sources/schreiber-2000]]. Deeper analytical read of the
original TE paper — derivation re-check, comparison to alternatives,
project-specific implications.

## Derivation chain (re-checked)

Starting from the Shannon entropy `H_I = -Σ p(i) log p(i)` and the
Kullback-Leibler divergence `K_I = Σ p(i) log p(i)/q(i)`, Schreiber arrives
at TE in four steps:

1. **MI as KL deviation from independence**: setting `q_IJ(i,j) = p_I(i)
   p_J(j)` in the KL definition gives the standard MI formula (Eq. 2).
   This is symmetric and static.
2. **Time delay**: introducing a lag `τ` in one variable gives
   `M_IJ(τ)` — directional but "somewhat ad-hoc" (Schreiber's own
   characterisation).
3. **Markov property as the right null**: instead of measuring deviation
   from independence (which gives MI), measure deviation from the
   *generalised Markov property*
   `p(i_{n+1} | i_n^{(k)}) = p(i_{n+1} | i_n^{(k)}, j_n^{(l)})`. If `J`
   doesn't drive `I`, this equality holds.
4. **TE = KL between the conditional distributions** (Eq. 4 of the paper;
   see [[equations/eq-transfer-entropy]]).

The key insight is the choice of null: TE asks "what does `J`'s past tell
us about `I`'s next step *beyond* what `I`'s own past already tells us?"
Whereas MI asks "what does `J` tell us about `I` at all?" The conditioning
on `I`'s past is what removes shared-history bias.

## Comparison to alternatives Schreiber considered

| Measure | Symmetric? | Removes shared history? | Handles common driver? |
|---|---|---|---|
| Mutual information `M_IJ` | yes | no | no |
| Time-delayed MI `M_IJ(τ)` | partially | no | no |
| Conditional entropy `H_{I|J}` | "non-symmetric only due to different individual entropies, not due to information flow" | no | no |
| Transinformation (MI rate) | yes | yes | no |
| **Transfer entropy `T_{J→I}`** | **no** | **yes** | **only with conditioning on Z** |

Conditional TE (the `TE(X→Y|Z)` form we use for wind/wave disentanglement)
is mentioned in passing on p. 462: "If computationally feasible, the
influence of a known common driving force Z may be excluded by conditioning
the probabilities under the logarithm to z_n as well." Schreiber explicitly
flagged the computational difficulty — exactly what [[entities/idtxl]]'s
greedy approach mitigates 18 years later.

## Embedding choices

Schreiber's recommendations:
- "The most natural choices for `l` are `l = k` or `l = 1`. Usually, the
  latter is preferable for computational reasons" (p. 462).
- For the tent-map / Ulam examples, `k = l = 1` is used.

For our FOWT data:
- Target `Y` (e.g. `PtfmPitch`) is a continuous, autocorrelated
  oscillation with multiple eigenfrequencies — `k = 1` would be far too
  short. We rely on IDTxl's max-stat embedding-length search ([[entities/idtxl]]).
- Source `X` (wind / wave) is also autocorrelated; `l = 1` may capture
  the immediate excitation but miss accumulated forcing. Again, defer
  to IDTxl.

## Project-specific implications

1. **TE definition is unchanged from 2000.** Our [[equations/eq-transfer-entropy]]
   directly transcribes Eq. 4. The estimator has evolved (Schreiber used
   kernel; we use [[concepts/ksg-estimator]]); the *measure* is the same.
2. **The sleep-apnea analogy is useful as a sanity check on plot
   interpretation.** Schreiber's Fig. 4 shows TE deflecting to zero at
   small `r` (length scale) due to finite-sample artefacts. For our
   decimated FOWT data we should expect the same shape — TE plotted
   vs. embedding parameter or noise level should plateau in the middle
   and collapse at the extremes. Track this in
   [[validation/case-3-iea15-single-case-te]].
3. **Schreiber's caveat on common drivers**: "Certainly, both signals
   could instead be responding to a common external trigger." This is
   *our* situation with wind and wave under correlated DLC-A conditions.
   The conditional TE is the answer; DLC-B (decoupled seeds) is the
   control. See Q6 in [[open-questions]].
4. **Validation against the closed-form scaling.** The tent-map example
   gives `T_{I^{m-1}→I^m} ≈ α²ε²/ln(2)` for small `ε`. This is a clean
   benchmark — replicating it would be a stronger validation than the
   AR(1) case in [[validation/case-2-ar1-te-recovery]]. Worth adding
   as `case-2b` after the AR(1) basic test passes.

## Lingering questions

- Schreiber's kernel estimator is positivity-preserving by construction.
  KSG is **not** strictly positive (it can return small negative values
  for genuinely independent processes due to finite-sample fluctuations).
  Need to check how IDTxl handles negative-but-near-zero estimates in
  the surrogate test (clip vs preserve).
- The paper does not discuss bias correction. With KSG we get
  asymptotic unbiasedness; the surrogate test handles finite-`N` bias
  for free.

## Related

- [[sources/schreiber-2000]] · [[concepts/transfer-entropy]] ·
  [[concepts/conditional-transfer-entropy]] · [[equations/eq-transfer-entropy]]
- [[papers/kraskov-2004]] — the estimator we substitute for Schreiber's kernel
- [[papers/wollstadt-2019]] — the modern multivariate generalisation
