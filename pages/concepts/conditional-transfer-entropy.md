---
title: "Conditional Transfer Entropy"
type: concept
created: 2026-05-12
updated: 2026-05-12
sources: ["schreiber-2000", "wollstadt-2019"]
tags: [information-theory, causality]
---

## Definition

Conditional Transfer Entropy `TE(X → Y | Z)` measures the information `X`'s
past contributes to `Y`'s present **beyond** what `Y`'s past *and* `Z`'s
past already provide. It strips the part of the apparent `X → Y` relation
that is attributable to a common driver `Z`.

The conditional form is mentioned by Schreiber in the original TE paper:

> "If computationally feasible, the influence of a known common driving
> force Z may be excluded by conditioning the probabilities under the
> logarithm to z_n as well." (schreiber-2000, p. 462)

Schreiber explicitly flagged the "computational feasibility" caveat —
which [[entities/idtxl]]'s greedy parent-set construction mitigates 18+
years later (per [[sources/wollstadt-2019]]).

Formal statement: extend [[equations/eq-transfer-entropy]] by adding `Z`'s
embedded past as an extra conditioning variable in the conditional mutual
information.

## Why it matters here

In real ocean conditions, wind and wave are correlated (wind sea couples
the two). A naïve `TE(wind → PtfmPitch)` could double-count what is really
`wave → PtfmPitch`. We compute:

- `TE(wind → PtfmPitch | wave)` — the genuine wind contribution
- `TE(wave → PtfmPitch | wind)` — the genuine wave contribution

DLC set B (decoupled wave seeds — see [[PLAN]]) provides a check:
in set B the marginal and conditional TEs should agree, while in set A
(coupled seeds) they may differ. This is hypothesis H3 in
[[open-questions]] Q8 — the cleanest pre-registered prediction in the
project.

## Multivariate vs simple conditioning

wollstadt-2019 distinguishes two forms:

1. **Single conditioning variable** — `TE(X → Y | Z)` as defined above.
   Removes confounding from one known common driver.
2. **Greedy multivariate parent-set search** — for each target `Y`,
   iteratively add the candidate source-history that maximises
   `I(Y_t ; X_{t-u}^{(l)} | Y_{t-1}^{(k)}, S)` where `S` is the current
   parent set. Removes redundant *and* captures synergistic contributions
   across many candidate sources simultaneously.

For Phase 4, our wind-vs-wave story uses form (1) explicitly (both are
known drivers). When we extend to more channels later (e.g., does rotor
speed mediate any of the wind → tower-base bending coupling?), form (2)
takes over.

## Estimator

[[entities/idtxl]] supports both forms directly:
- `BivariateTE` with `conditional = ProcessAnalysisData(...)` for explicit
  single-conditioner Form 1.
- `MultivariateTE` for greedy Form 2.

Both use the same KSG conditional-MI estimator under the hood (see
[[concepts/ksg-estimator]], generalised via kraskov-2004 Eq. 30).

## Related concepts

- [[concepts/transfer-entropy]] — bivariate version
- [[concepts/ksg-estimator]] — same estimator, higher-dim CMI
- [[concepts/mutual-information]] — symmetric analogue

## Sources

- [[sources/schreiber-2000]] — original mention of conditional form.
- [[sources/wollstadt-2019]] — multivariate / conditional implementation.
- `bossomaier-2016` *(to ingest)* — textbook treatment.
