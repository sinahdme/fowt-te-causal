# Verification Review Report — Round 3 (Stage 3′ Re-Review)

- **Manuscript**: "An Information Firewall in Floating Offshore Wind Turbines…" (`reports/te-firewall-paper-final.md`, as of 2026-07-29)
- **Mode**: `academic-paper-reviewer` re-review (verification) — field_analyst + EIC + editorial_synthesizer
- **Verifies against**: Round-2 panel (`reports/te-firewall-review-round2.md`, Major Revision, 10 required + 4 suggested)
- **Review date**: 2026-07-29
- **Note**: No Response-to-Reviewers letter was supplied; every roadmap item was verified **directly against the manuscript** (Traceability Rule → author-claim column marked *n/a; verified in text*). Two pieces of evidence computed **after** round 2 were weighed: the completed fault-case (open-loop twin) TE run, and the full-settings GPU campaign (`te_table_full`).

---

## Decision: **MINOR REVISION**

The entire round-2 roadmap (10 required + 4 suggested) is **fully addressed** — a clean sweep, verified in text. The decision is not Accept because two new issues emerged from results computed since round 2, one of which touches a headline demonstrated-result claim (attribution) and must be reported honestly. Both fixes use results already in hand; neither needs new computation.

Round-2 IRON RULE (DA-1 CRITICAL, draft↔final divergence) is **resolved**: the draft is archived, `final.md` is the single source of truth, and the delay/sea-state/SURD-unit defects are corrected. No new CRITICAL issues.

---

## Priority 1 — Required Revisions (all verified in text)

| # | Round-2 item | Status | Location verified | Assessment |
|---|---|---|---|---|
| RR1 | Port v0.6 delay corrections (abstract lags, §3.8 half-period rule, §4.5 antiphase reading, Table 5 surge 6.3 s ≈ Tp/2 + 1.1 s, Fig 7, §4.1 "two orders") | ✅ FULLY_ADDRESSED | Abstract; §3.8 (l.176); §4.1 (l.199 "two orders"); §4.5 + Table 5 (l.290–299); Fig 7 (l.309–311) | Table 5 surge = 6.3 (≈Tp/2; secondary 1.1); abstract "0.3–3.9 s … near-antiphase at ~half wave period for surge" matches Table 5. Reproducible from `delay_profiles.parquet` per §3.8 rule. |
| RR2 | Sea-state: wind-speed-matched (Hs,Tp); spectral peaks 0.077–0.111 Hz; fix §3.2 | ✅ FULLY_ADDRESSED | §3.1 (l.116); §3.2 (l.124) | Full (Hs,Tp) list present; peak range 0.077–0.111 Hz in both §3.1 and §3.2. |
| RR3 | Fix Intro scope (campaign ≠ "DLC 1.6 at four wind speeds") | ✅ FULLY_ADDRESSED | §1 (l.38) | Now "four wind speeds … with wind-speed-matched sea states, plus a severe-sea-state DLC 1.6 set near rated." |
| RR4 | Identify §4.5 seeds as DLC 1.6 severe-sea set; scope delays to that sea state | ✅ FULLY_ADDRESSED | §4.5 (l.290); Table 5 caption (l.292) | "three analysed severe-sea 11 m/s seeds (the DLC 1.6 set …, Tp = 12.95 s; the delays scale with the sea state)." |
| RR5 | SURD units: normalisation in §3.6; strip "nats" (§4.3 ×2, Fig 4c, §5.3) | ✅ FULLY_ADDRESSED | §3.6 (l.162); §4.3 (l.256, l.266); Fig 4c (l.272); §5.3 (l.347) | "normalised, dimensionless units … not in nats"; all SURD figures now say "normalised units." |
| RR6 | Coherence: report K≈6 Welch averages + ≈0.45 zero-coherence 95% level; note peaks clear it | ✅ FULLY_ADDRESSED | §3.5 (l.152) | "six 50%-overlapping … K = 6 … γ² ≈ 0.45, and every peak … exceeds it." |
| RR7 | Open-loop twin: state n=1; add seed replication to validation list | ✅ FULLY_ADDRESSED | §4.3 (l.266); §5.3 (l.341) | "single near-rated realisation (one 11 m/s seed)"; §5.3 "rests on a single realisation … replicating … across seeds … queued campaign." |
| RR8 | Rotor-effective-vs-point-wind limitation with blade-channel counter-argument + its weakness; queue robustness check | ✅ FULLY_ADDRESSED | §5.3 (l.345) | Both sides stated ("blade loads respond to locally sampled wind, which is itself point-like, so those edges do not by themselves exclude the spatial-filtering account"); rotor-averaged check queued. |
| RR9 | Bind abstract "total" to the chance-floor clause | ✅ FULLY_ADDRESSED | Abstract (l.14) | "selected … in fewer cases than expected by chance at the 5% level — within the resolution of the significance test, the firewall is total." |
| RR10 | Reconcile draft↔final; single source of truth; end-to-end numeric re-verification | ✅ FULLY_ADDRESSED (process) | SYNTHESIS/log; commit ddc45fe | Draft archived; final is sole source; body internally consistent. See Residual note on final numeric re-check vs deposited `te_table.parquet`. |

**All 10 Priority-1 items FULLY_ADDRESSED.**

## Priority 2/3 — Suggested Revisions

| # | Item | Status | Location |
|---|---|---|---|
| S1 | Window-length ↔ detection-latency sentence (§5.2) | ✅ FULLY_ADDRESSED | §5.2 (l.335) — "≈ 50-minute windows … detection latency of that order; shortening the window … inflates the variance …" |
| S2 | FAIRTEN1 mooring-orientation explanation | ✅ FULLY_ADDRESSED | §4.1 (l.201) — up-wave single line vs symmetric down-wave pair |
| S3 | Bridge to control-performance monitoring + operator action on alarm | ✅ FULLY_ADDRESSED | §5.2 (l.331) — "structural-monitoring analogue of control-loop performance monitoring … targeted pitch-system inspection" |
| S4 | dlca/dlcb seed-pairing detail | ✅ FULLY_ADDRESSED | §3.1 (l.116) — paired vs bit-mask-decoupled wave seeds |

---

## New Issues (from evidence computed after Round 2)

| # | Type | Severity | Location | Description |
|---|---|---|---|---|
| NEW-1 | Consistency / selective citation | Minor | §4.1 (l.201) | The new robustness sentence cites the full-campaign GPU (OpenCL–Kraskov) re-estimation **only on the wind side** ("surge significance 11%→0%, max wind→platform TE <0.005") while Tables 1–3 retain the first-pass numbers. A methodology reviewer will ask why the same run's wave→platform magnitudes were not adopted. The (legitimate) reason — the GPU run's `--max-lag-sources 20` ≈ 4 s window is appropriate for the near-instantaneous wind channel but truncates the 6.3 s wave→surge delay, so it is a valid **wind-side** robustness check only — should be stated in one clause to pre-empt a cherry-picking reading. |
| NEW-2 | Currency of a core claim | **Major** | §4.3 (l.268), §4.6 (l.315), Abstract | §4.3 states the open-loop twin's TE legs "have not been computed … completing it would close both arguments at once." **They have now been computed, and TE(Wind→platform) does NOT rise with the loop open (null).** The manuscript must (a) update the "pending" language to report the computed null, and (b) interpret it honestly: the open-loop SURD *organisation* collapses (§4.3) yet wind→platform TE stays zero, which means the firewall is **not exclusively control-erected** — a structural / spatial-filtering component is implicated, connecting directly to the DA-2 / §5.3 rotor-effective-wind caveat. Caveat that softens severity: n = 1, and full loop-disabling is not a realistic pitch fault, so the null is inconclusive for the *monitoring* outlook; and the paper never *claimed* the TE-converse, so the attribution does not collapse — but leaving a now-answered question marked "pending," with an over-optimistic "would close both arguments," is not tenable. |

---

## Decision Rationale

The round-2 panel returned Major Revision on an integrity-of-record basis (stale delay analysis, wrong sea-state description, SURD units, draft↔final divergence). **Every one of those defects is fixed and verified in text**, and the two suggested-tier gaps are closed too — the manuscript is now internally consistent and its tables are reproducible from the deposited data. That clears the bar the panel set.

It is **Minor, not Accept**, because two issues surfaced from work completed after round 2. NEW-1 is a one-clause honesty fix. NEW-2 is the substantive one: the paper's own nominated "decisive" computation (open-loop TE converse) has now been run and returned a null, which the manuscript still describes as pending. This does not sink the paper — the attribution rests on SURD, which the paper is careful never to over-claim, and the null is n = 1 on a non-fault perturbation — but a reader must be told the converse was tested and did not rise, and the honest reading (a structural/spatial-filtering share of the firewall) must be folded into §4.3/§5.3. Because both fixes are honest-reporting edits using results already in hand, the effort is small.

It is **not Major** because no roadmap item regressed, no new CRITICAL issue exists, and NEW-2 is repairable in prose without new computation.

## Residual Issues / Recommended handling

1. **NEW-2 (priority)** — Update §4.3 (and the abstract/§4.6 sentences that lean on the open-loop twin) to report the computed open-loop TE null; add ~2–3 sentences interpreting it as evidence of a partly structural firewall, cross-referencing the §5.3 rotor-effective-wind limitation. Mark full graded-fault (pitch-lock/bias) TE as the still-pending monitoring test (§4.4's pitch-lock statement remains accurate).
2. **NEW-1** — Add one clause to §4.1 noting the GPU re-estimation is cited as a wind-side robustness check and why its wave magnitudes are not directly comparable (short source-lag window).
3. **RR10 final check (advisory)** — Confirm Table 1/2/3 numbers still reproduce from the deposited first-pass `reports/te_table.parquet` (the paper's stated data source), independent of the `te_table_full` campaign.

**Recommended next step after these edits:** proceed to final integrity check → finalize (Stage 4.5 → Stage 5). No further full panel needed unless NEW-2's discussion materially changes contribution #2's framing.

---

## Resolution addendum (2026-07-31)

NEW-1 and NEW-2 were applied to `te-firewall-paper-final.md` and the docx regenerated.

- **NEW-2 (Major) — RESOLVED.** §4.3's stale paragraph was rewritten: it now reports the computed open-loop TE null (wind→platform pitch/surge/heave all remain at zero, below the ≈0.03-nats ceiling), notes the estimator still finds a significant control-channel edge in the same run (conditional Wave1Elev→FAIRTEN3, TE ≈ 0.055 nats, *p* = 0.005) so the null is not an artefact, untangles the open-loop-twin converse from the §4.4 pitch-fault test (which remains genuinely uncomputed), reads the null conservatively (n=1; loop-disabling ≠ a fault), and folds in the "partly structural firewall" reading cross-referenced to §5.1. The attribution is explicitly rested on the two SURD-based lines and NOT on the TE-converse. The stale phrases ("would close both arguments at once", "have not been computed in the present dataset") are gone. Abstract and §4.6 needed no change — they lean on the SURD organisation-collapse leg, which stands.
- **NEW-1 (Minor) — RESOLVED.** §4.1 robustness sentence now carries the wind-side-only clause and the reason the full-campaign wave magnitudes are not adopted (~4 s source-lag window truncates the 6.3 s wave→surge delay).

Verified in both the markdown and the regenerated docx (`word/document.xml` text scan, 7/7 checks PASS). Recommendation stands: proceed to final numeric table re-check (RR10 advisory) + front/back matter, then finalize.
