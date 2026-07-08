# Response to Reviewers — Round 1 (Stage 4 revision)

**Manuscript:** *An Information Firewall in Floating Offshore Wind Turbines…* (v0.3)
**Decision:** Major Revision · **Resolution chosen:** Path B (rescope monitoring to an outlook), with the fault-TE computation queued as a separate CPU job for a future revision.

We thank the panel. The reviews correctly identified that the manuscript, as submitted, promised a demonstrated monitoring method it did not deliver, and that one statistical point (the chance-significance floor) materially changed the reading of the "breach" cases. We have rescoped rather than overclaim. Every point is addressed below with status and location; status is one of **Addressed**, **Partially addressed**, or **Acknowledged (deferred)**.

---

## Roadmap items

| # | Pri | Issue | Status | Response |
|---|---|---|---|---|
| 1 | P0 | Monitoring claimed, not demonstrated | **Addressed** | Retitled to lead with the firewall discovery; monitoring recast as an explicit *outlook* (§1 contribution 3, §4.4 "A monitoring hypothesis, not yet tested", §5.2, Conclusion). Title↔evidence mismatch removed. |
| 2 | P0 | Chance-floor undercuts the two "breach" cases | **Addressed** | Added the chance-floor analysis to §4.1: expected ≈ 2.7 significant of 54 at α = 0.05, observed exactly 2, so wind selection is *below* chance. §4.4 now states plainly the two flagged cases are consistent with noise and are not a breach. |
| 3 | P1 | Open-loop attribution is n=1, TE pending | **Partially addressed** | §4.3 now leads attribution with SURD redirection and labels the open-loop twin as corroborating, single-case, TE-pending. Adding open-loop seeds is deferred (compute). |
| 4 | P1 | Detectability confound for exact-zero regimes | **Addressed** | New §5.1 paragraph rebuts the detectability alternative on three grounds: the estimator does detect wind on blade/tower channels and near rated; SURD attributes the wind information across all regimes independent of TE detectability; the open-loop twin isolates control at fixed sea state. |
| 5 | P2 | `te_frac` defined but unused | **Addressed** | §4.1 now reports it: wind adds 0.04% of the platform's self-predictability vs 4.3% for wave. |
| 6 | P2 | "Coherence false positive" strawman | **Addressed** | §4.2 retitled ("Why coherence is insufficient: shared power is not directed influence"); text now states coherence is not wrong, only that shared power ≠ influence. |
| 7 | P2 | SURD nbins = 3 robustness | **Addressed** | §5.3 limitation added: the ≈ 0.4 redundancy figure should be confirmed under finer binning/lags and is treated qualitatively. |
| 8 | P2 | Controller-specificity + fatigue; missing negative-damping ref | **Addressed** | §5.2 now states baseline is control-configuration-specific and adds the fatigue consequence of a breach (re-admitting low-frequency thrust into a lightly damped platform). Added Larsen & Hanson (2007) in §2.2 and §5.2. |

## Reviewer-disagreement notes

- **On R1's chance-floor point (item 2):** we accept it fully; it strengthens the firewall (wind below chance) while removing any positive monitoring reading from the healthy data. This is now the load-bearing statistical statement of the paper.
- **We did not** add graded-fault results (R3's preferred strengthening) in this round: the GPU cluster is committed to a separate long-running campaign, and we chose not to contend for it. The one-case fault TE is a CPU-only task (JidtKraskovCMI backend) queued as `analysis/compute_fault_te.py`; a future revision can re-upgrade §4.4 from outlook to proof of concept if it clears both the healthy ceiling and the chance floor.

## Change summary

Title changed; abstract, §1(3), §4.4, §5.2, §5.3, and Conclusion rescoped; §4.1 (te_frac + chance floor), §4.2 (coherence framing), §5.1 (detectability rebuttal) revised; Larsen & Hanson (2007) added (16 references total). Length 9,104 words. No quantitative claim changed except by adding verified numbers; all additions traced to the data tables.
