---
title: "Schreiber 2000 — Measuring Information Transfer"
type: source
created: 2026-05-12
updated: 2026-05-12
source_path: "raw/papers/0001042v1.pdf"
authors: ["Schreiber, T."]
year: 2000
venue: "Physical Review Letters"
doi: "10.1103/PhysRevLett.85.461"
citation_key: "schreiber-2000"
tags: [source, transfer-entropy, foundational]
sources: []
---

## Citation

Schreiber, T. (2000). "Measuring Information Transfer." *Physical Review Letters*
**85**(2), 461–464. arXiv:nlin/0001042.

## TL;DR

- Defines **Transfer Entropy** (TE), a non-symmetric Kullback-entropy measure
  of information flow that excludes spurious contributions from shared
  history and common inputs — solving a well-known flaw of time-delayed
  mutual information.
- The TE formula: see [[equations/eq-transfer-entropy]]. The most natural
  embedding choices are `l = k` or, computationally cheaper, `l = 1`.
- "If computationally feasible, the influence of a known common driving
  force Z may be excluded by conditioning the probabilities under the
  logarithm to z_n as well" — direct justification for our conditional-TE
  wind/wave disentanglement (see [[concepts/conditional-transfer-entropy]]).
- For coarse-grained continuous systems, TE is finite and partition-
  independent in the limit ε→0, except under deterministic coupling
  (then it diverges as ε→0). MI also diverges in that case.
- Demonstrates utility on three examples: tent-map lattice (closed-form
  α²ε²/ln(2) low-coupling scaling), Ulam-map lattice (TE detects directional
  coupling that MI misses near periodic windows), and a sleep-apnea
  heart/breath dataset (TE shows heart→breath > breath→heart over a
  significant range of length scales).

## Key claims

- "Mutual information neither contains dynamical nor directional information"
  (p. 461). Introducing a time delay improves but does not solve the issue.
- TE "is now explicitly non-symmetric since it measures the degree of
  dependence of I on J and not vice versa" (p. 462).
- The Ulam-map example (Fig. 2) is the cleanest validation: "transfer
  entropy for the negative direction remains consistent with zero for all
  couplings, reflecting the causality in the system" (p. 3).
- "Dynamically correlated pairs should be excluded as usual" (p. 2) —
  embedding sanity criterion we adopt in [[concepts/transfer-entropy]].

## Equations introduced

- [[equations/eq-transfer-entropy]] — Eq. 4 in the paper.

## Methods

Kernel density estimator with step kernel (Theiler-style):

$$
\hat{p}_r(x_{n+1}, x_n, y_n) = \frac{1}{N}\sum_{n'} \Theta\!\left(\left\|
  \begin{matrix} x_{n+1} - x_{n'+1} \\ x_n - x_{n'} \\ y_n - y_{n'} \end{matrix} \right\| - r\right)
$$

with maximum-distance norm. Dynamically correlated near-time-neighbours
excluded. For our project, we replace this kernel estimator with the more
modern KSG nearest-neighbour estimator ([[concepts/ksg-estimator]]), but
the underlying TE definition is unchanged.

## Data / cases

- Tent-map lattice (closed-form check)
- Unidirectional Ulam-map lattice (Fig. 2)
- Sleep apnea heart-rate / breath-rate (Fig. 3, Santa Fe 1991 contest data set B)

## How it informs this project

- Anchors the TE definition we use in Phase 4 ([[entities/idtxl]] implements
  Eq. 4 with the KSG estimator).
- The conditional form (last paragraph of p. 462) directly motivates
  [[concepts/conditional-transfer-entropy]] for separating wind vs wave
  contributions to FOWT response — see [[open-questions]] Q6.
- The "TE goes to zero for the back direction" sanity check is our
  Phase 4 embedding diagnostic and a KPI in
  [[validation/case-3-iea15-single-case-te]].
- The sleep-apnea example sets a useful template: TE diagnostics across a
  range of length scales `r`, with curves deflecting to zero at small `r`
  due to finite sample size — we should expect the same in our FOWT
  application after decimation (see [[open-questions]] Q4).

## Open questions / contradictions

- Schreiber notes that conditioning on many variables "poses immense
  numerical problems" — relevant to our multivariate TE plans. IDTxl's
  greedy parent-set construction (see [[entities/idtxl]]) is the modern
  workaround.
