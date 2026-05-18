---
title: "Equation — Transfer Entropy"
type: equation
created: 2026-05-12
updated: 2026-05-12
sources: ["schreiber-2000"]
tags: [equation, information-theory]
---

## Statement (modern notation)

For two stationary stochastic processes `X` (source) and `Y` (target) with
source–target lag `u`, source embedding length `l`, and target embedding
length `k`:

$$
T_{X \to Y}(u, k, l)
\;=\;
I\!\left(\, Y_{t}\;;\; X^{(l)}_{t-u} \,\big|\, Y^{(k)}_{t-1} \right)
\;=\;
\sum p\!\left(y_t,\, y^{(k)}_{t-1},\, x^{(l)}_{t-u}\right)
  \log
  \frac{p\!\left(y_t \mid y^{(k)}_{t-1},\, x^{(l)}_{t-u}\right)}
       {p\!\left(y_t \mid y^{(k)}_{t-1}\right)}
$$

i.e., the conditional mutual information between `Y_t` and the embedded
past of `X`, given the embedded past of `Y`.

## Source form (schreiber-2000, Eq. 4)

The form as originally given in [[sources/schreiber-2000]] (p. 462,
Schreiber's notation):

$$
T_{J \to I}
\;=\;
\sum p\!\left(i_{n+1},\, i_n^{(k)},\, j_n^{(l)}\right)\,
  \log
  \frac{p\!\left(i_{n+1} \mid i_n^{(k)},\, j_n^{(l)}\right)}
       {p\!\left(i_{n+1} \mid i_n^{(k)}\right)}
$$

with shorthand `i_n^{(k)} = (i_n, …, i_{n-k+1})` — the `k`-dimensional
delay embedding vector. The two forms are identical up to renaming
(`I → Y` target, `J → X` source).

Schreiber's recommended embeddings (p. 462):

> "The most natural choices for `l` are `l = k` or `l = 1`. Usually, the
> latter is preferable for computational reasons."

For our project we let [[entities/idtxl]] search `(k, l, u)` automatically
per pair via max-stat / min-stat (per [[sources/wollstadt-2019]]).

## Symbols

| Symbol | Meaning | Units |
|---|---|---|
| `Y_t` | Target sample at time `t` | (signal units) |
| `Y^{(k)}_{t-1}` | Target embedding vector — `k` past samples | – |
| `X^{(l)}_{t-u}` | Source embedding vector starting `u` steps in the past, length `l` | – |
| `u` | Source–target lag (steps) | – |
| `k` | Target history length | – |
| `l` | Source history length | – |
| `T` | Transfer entropy | nats (or bits if log base 2) |

Schreiber's paper uses natural logarithms in the closed-form tent-map
result (`α²ε²/ln(2)`, p. 3), suggesting bits for the reported numbers.
IDTxl returns nats by default; we will convert to bits in
`analysis/te_pipeline.py` for human readability.

## Properties

From [[sources/schreiber-2000]]:

- **Non-symmetric**: `T_{X→Y} ≠ T_{Y→X}` in general — directional measure.
- **`T_{X→Y} ≥ 0`** in expectation, by construction (it is a KL divergence
  of conditional distributions).
- **Finite under coarse-graining of continuous systems** in the limit
  `ε → 0`, except for deterministic coupling (where it diverges) (p. 462).
- **Zero in the back-direction** for unidirectionally coupled systems —
  the cleanest causality diagnostic, demonstrated on the Ulam-map example
  (Fig. 2, p. 3).

## Used in

- [[concepts/transfer-entropy]] — concept page
- [[concepts/conditional-transfer-entropy]] — extended with conditioning `Z`
- Phase 4 of [[PLAN]] — env→response causal estimation
- [[validation/case-2-ar1-te-recovery]] — known-answer recovery test
- [[validation/case-3-iea15-single-case-te]] — first FOWT end-to-end

## Sources

- [[sources/schreiber-2000]] — original definition.
- [[papers/schreiber-2000]] — deep analytical companion.

## Related equations

- [[equations/eq-mutual-information]] — TE = conditional MI; both reduce
  to the same KL-divergence-of-distributions form.
