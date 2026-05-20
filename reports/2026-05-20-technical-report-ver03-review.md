# Review — `2026-05-20-technical-report-ver03.docx`

**Reviewer:** Claude (Opus 4.7)
**Date:** 2026-05-20
**Source:** 458 paragraphs extracted from `_unpacked_ver03/word/document.xml`. Paragraph/line numbers below refer to `reports/_ver03_extracted.md`.

---

## Substantive issues (worth fixing before circulating)

### 1. §6.3 — the wave-spectrum-peak claim is physically wrong (line 303)
You say the platform-pitch eigenfrequency "~0.034 Hz … sits well within the spectral peak of the SSS wave forcing." Tp = 12.95 s ⇒ fp ≈ 0.077 Hz. 0.034 Hz is in the **low-frequency tail** of the first-order spectrum, not at its peak. Low-frequency pitch excitation at 0.034 Hz under SSS is driven by **second-order (difference-frequency / slow-drift) wave forcing**, not by the JONSWAP peak. This is the right physics for the null and arguably *strengthens* the wave-dominance interpretation — but the current sentence will be flagged in review.

### 2. §3.2 vs §4.4 — output-rate contradiction (lines 82 vs 184)
§3.2 says "3600 s … at **80 Hz** output"; Table 4 says "**40 Hz** (OpenFAST DT_Out = 0.025 s)". DT_Out = 0.025 s ⇒ 40 Hz. Fix §3.2.

### 3. §5.3 over-claim about pre-registration thresholds (line 293)
"Each H1–H6 prediction … is paired with an explicit numeric threshold." Only H4 (and H5 partially) actually have explicit numeric thresholds. H1/H2 reduce to "p < 0.05 + significant"; H3 has the 80 % criterion but the "≈" is undefined; H6 ("PSD peak at ~0.0345 Hz") doesn't define a tolerance. Either tighten the predictions or weaken the claim ("each is paired with an evaluation criterion, numeric where applicable").

### 4. §6.4 Sobol — median imputation deserves a caveat, not just a footnote (lines 307–310)
With 44 % feasible and ST > 1.0 you've already noted instability, but median-imputing Y for infeasible X then running Sobol is biased — the surrogate variance gets compressed and the indices distort unpredictably. At minimum, say so explicitly; ideally note that the N = 256 production run will use the constrained-sampling alternative (or whatever your plan is). Right now §6.4 reads as if N = 256 alone will fix it.

### 5. §6.2 — `p = 1.0000` with 50 surrogates needs a sentence of interpretation (line 300)
Strictly, p = 1.0 means the observed TE was ≤ every surrogate. With circular-shift surrogates and a controller actively rejecting the wind→pitch path, this is plausible but unusual; readers will read it as "broken code". One sentence — *"observed TE fell below all 50 surrogate values, consistent with active disturbance rejection"* — defuses it.

### 6. Abstract framing of H4 (line 5)
You report "Lu dominant … counter to the pre-registered prediction that EA would dominate." That's true for the **EA** part of H4, but H4 also predicted ST(Lu) > 0.2 and you got 0.82 ± 0.44 — i.e., the **Lu** half of H4 was confirmed. The abstract should call this **partial-confirmation**, not full disconfirmation. Same point in §8.2 line 382.

---

## Internal-consistency / cross-reference issues

### 7. §1.3 line 34 — figure cross-ref wrong
"the two analytical arms shown in **Figure 1**" should be **Figure 2** (Figure 1 is the OpenFAST module architecture).

### 8. Eigenfrequency notation drift
0.0345 Hz (Table 1, H6) vs 0.034 Hz (§6.3). Pick one.

### 9. `Lu` vs `L_u`
Table 1 H4 writes `L_u`; §6.4 writes `Lu`; Table 5 writes `L_u`. Pick one convention and apply globally (same for D_*, H_*).

### 10. `N = 15001` vs `N = 15 001`
§4.3 vs Table 4. Trivial but inconsistent.

### 11. Phase numbering in §4.1 vs §1.3
§1.3 lists Phase 3 as "Data extraction" (parquet/preprocess); §4.1 also lists it; §6.5 Table 6 labels it "Embedded" with the note that preprocessing is the front-end of `te_pipeline.py`. If Phase 3 is no longer a standalone phase, say so once explicitly rather than letting the reader infer it from the status table.

### 12. §7.1 Table 7 wall-time arithmetic
Baseline = 27 days. Option A claims 4× → ~7 days (27/4 = 6.75 ✓). Option B claims 3× → ~9 days (27/3 = 9 ✓). Option C claims 6× → ~5 days (27/6 = 4.5, rounds to 5 — fine). Consistent, but flag that **A+C combine multiplicatively only if conditional/Granger are also dropped under C**; if C keeps them, the 6× already includes them and A+C ≠ 24×. Worth a half-sentence.

---

## Editorial / presentation

### 13. §1.1 line 9 is a ~600-word single paragraph
Lists every OpenFAST module + every analysis library. Split into (a) coupled-physics modules, (b) post-processing/analysis stack. Currently it reads as a methods-section dump landed in the introduction.

### 14. §2 has three empty paragraphs (lines 63, 67, 69)
Presumably equation images. Verify they render in the actual DOCX; the XML extraction saw no text. If they're MathType/equation objects they'll be fine, but worth opening the DOCX once to confirm none came across blank.

### 15. Figures 1–4
The figure-paragraphs themselves (lines 10, 24, 85, 174) extract as empty — same caveat as #14, almost certainly images, but worth a visual check.

### 16. §5.2 line 291 (BLAS thread oversubscription)
Operational deployment detail. Either move to an implementation appendix or keep but trim to one sentence — it currently sits in the experimental-setup section where readers expect the *what*, not the *how it almost broke*.

### 17. §7.3 line 373 ends mid-thought
*"the share of (X → Y) causality the controller absorbs via disturbance rejection."* The formula referenced is the empty paragraph above (line 372) — same image-equation question as #14.

### 18. §8.4 Q4 status (line 391)
"Resolved during the first DLC-A post-mortem." That post-mortem hasn't happened yet (Phase 4 isn't launched). Either drop Q4 from this list or rephrase as "to be resolved during…".

---

## Strengths worth keeping

- The pre-registration table + H1–H6 numeric criteria is the strongest part of the report — keep it prominent.
- The controller-mediated TE discussion (§2.3, §7.3, §7.4) is technically sharp and pre-empts the obvious reviewer objection about closed-loop systems.
- Appendix A repo-index strategy is good — keeps the report tight without losing traceability.
- DLC-A vs DLC-B XOR-seed construction for H3 is clean and clearly motivated.

---

## Suggested fix order

Tackle in this order:

1. **#1 (physics)** → factually wrong, single-sentence fix.
2. **#2, #6 (factual)** → numbers / framing.
3. **#3, #4, #5 (overclaim/caveat)** → adds a sentence each.
4. **#7–#11 (cross-refs / notation)** → mechanical pass.
5. **#12–#18 (editorial)** → polish.

Items #1–#6 are review-grade defects; the rest are polish.
