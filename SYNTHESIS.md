---
title: "Synthesis — conversation & decision record"
type: synthesis
created: 2026-07-09
updated: 2026-08-12
tags: [meta, log, sessions, decisions]
---

# SYNTHESIS.md

Durable record of **conversations** between the user and Claude: questions and
answers (both directions), plans, decisions, and every file update. Exists
because git commits and [[pages/log|log]] capture *tasks*, not *dialogue* — and
each new Claude session was forgetting what the last one discussed.

**Conventions**
- §0 is rewritten every session — it is the "what were we doing?" answer.
- Session entries below §0 are **append-only, newest at the bottom**
  (same convention as `pages/log.md`).
- Every session entry records: Dialogue (user↔Claude Q&A), Decisions,
  Files changed (with commit hashes), Open items / next steps.
- Entries before 2026-07-09 are *reconstructed* from git history,
  `pages/log.md`, `SESSION-LOG-2026-06-29.md`, and Claude's memory notes —
  summaries, not verbatim (those transcripts are gone).
- Maintenance rule lives in `CLAUDE.md` (vault root) so every session loads it.

---

## §0 Current state — read this first (rewritten 2026-08-12)

- **Latest (2026-08-12, session 36): retitled the paper (hybrid firewall + monitoring-feasibility).**
  Author proposed "feasibility of Information theory for blade pitch controller health monitoring"; flagged that a
  feasibility-led title would overclaim (monitoring is an untested outlook; the demonstrated results are the
  firewall + attribution). Author chose the hybrid — NEW title: "An Information-Theoretic Firewall in Floating
  Offshore Wind Turbines: Feasibility for Blade-Pitch Controller Health Monitoring" (was "An information-flow
  firewall … the controller as structural shield"). Updated both the Title paragraph (document.xml) and dc:title
  (core.xml); no body realignment (hybrid matches abstract/contributions). Master was open in Word (file lock) —
  staged to _title_check.docx, finalized after author closed it. validate.py PASSED, 449 paras. Backup
  `…bak-<ts>-pretitle-hybrid`.

- **Prev (2026-08-12, session 35): revised Figure 6 (combined causal graph) — reframed the firewall as a blocked edge.**
  Author: "figure 6 must be revised" and delegated the call. Numbers all verified correct (wave %s = te_frac;
  U=0.167 matches Fig 5c; SURD≈0.40 matches §4), so it was a presentation fix. The red FIREWALL *box* wrapped the
  platform nodes while grey WAVE arrows flowed into it — implying the platform is walled off, contradicting the
  thesis (waves drive the platform; only wind is blocked). Fix in `_make_fig5_firewall_graph.py` (feeds docx Fig 6
  = rId13 → image8.png): removed the box + rotated wordmark; drew the firewall as the ABSENT wind→platform edge —
  a blocked dashed-red pathway cut by a bold ✗ with a white-boxed "FIREWALL / no direct wind → platform" label;
  bowed the indigo U=0.167 edge higher for legibility. Same dims (1977×1321), validate.py PASSED, embedded
  md5-identical, caption already matches. Backup `…bak-<ts>-prefig6revise`.

- **Prev (2026-08-12, session 34): reconciled Figure 5c to the paired-seed numbers (0.167 / 0.0612).**
  Author: "reconcile the figure to 0.167 summed over lags." Corrected a mis-diagnosis — summing lags is a no-op
  (only lag=25 is non-zero, already the sum). The real gap: figure showed the 6-seed MEDIAN (0.140/0.065) while the
  text uses the single s00 seed (0.167/0.0612), s00 being the seed the open-loop twin is built from. Author chose
  same-seed paired framing in BOTH panels. Rewrote the open-loop block in `_make_surd_figs.py`: closed-loop
  reference = s00 (0.0612 leak-drop, 0.167 U:BldPitch1) matching the text; other 5 seeds as light-grey context;
  x-tick "controller ON (seed s00)"; legend updated. No text/caption edit (caption already says 0.167). Regenerated
  surd-openloop.png only, swapped into docx (rId12 → media/image7.png, 1480×720). validate.py PASSED, 449 paras,
  embedded md5-identical. Backup `…bak-<ts>-prefig5c167`. Follow-up: added a clause to the Figure 5c caption —
  "Open-loop twin (11 m/s; seed s00, five sibling seeds shown as context)." — so the grey context dots are
  explained (docx XML edit; validate.py PASSED; backup `…bak-<ts>-prefig5ccaption`).

- **Prev (2026-08-12, session 33): cleaned up Figure 5c (open-loop twin) — added legend, stripped baked-in annotations.**
  Author: add the missing legend; remove the two-sentence bottom caption; move "−59%" and "exactly 0" to the text.
  Both facts already live in §3.3 ("collapses to exactly zero"; drop "0.0612→0.0265, −57%"), so no text edit. The
  figure's −59% (median-of-seeds baseline) differed from the text's −57% (same-seed s00 baseline); author chose to
  KEEP −57% and just drop the annotation. Edited `_make_surd_figs.py` open-loop block: removed the −59% / →exactly-0
  panel annotations + `fig.text` caption, added a 3-entry legend (seeds / median / open-loop twin), kept data-value
  labels. Regenerated surd-openloop.png only; swapped into docx (Figure 5c = rId12 → media/image7.png, 1480×720).
  validate.py PASSED, 449 paras, embedded image md5-identical. Backup `…bak-<ts>-prefig5clegend`.

- **Prev (2026-08-12, session 32): removed the redundant annotation box from Figure 5b.**
  Author: "eliminate the box [on fig 5b] … I think it is already mentioned." Confirmed the §3.3 text already states
  the TE-null / SURD-mediated-path point, so nothing moved to the body. Deleted the `ax.annotate` box in
  `reports/figs/_make_surd_figs.py`, regenerated `surd-vs-te.png` (only 5b; other two SURD figs restored from
  backup), and swapped it into the live master docx (Figure 5b = rId11 → media/image6.png, 1480×880 unchanged).
  Also drops the stale "48/51 / 94%" stat (text says 2/54). validate.py PASSED, 449 paras (image-only), embedded
  image md5-identical to source PNG. Backup `…bak-<ts>-prefig5bbox`.

- **Prev (2026-08-12, session 31): merged "1.1 Background" into the Introduction.**
  Author: "merge section 1. introduction and 1.1 background and the section name is introduction." Edited the
  canonical master `reports/te-firewall-paper.docx` directly (XML). Removed the "1.1 Background" Heading3 (prose
  folds into §1) and its unreferenced `background` bookmark; kept heading "1. Introduction"; renumbered
  "1.2 Motivation and Contribution" → "1.1" (author decision) to keep numbering contiguous. Verified: validate.py
  PASSED (PYTHONUTF8=1), 450→449 paras, pandoc shows §1 Introduction → §1.1 Motivation → §2, all Background prose
  intact. Backup `…bak-<ts>-premergeintro`.

- **Prev (2026-08-11, session 30): added an Abbreviations group to the Nomenclature (19 acronyms, alphabetical).**
  Author: "add the abbreviations as well." Harvested acronyms from the docx, filtered out channel names (Table 1)
  and citation-venue codes; added a bold "Abbreviations" subheading after Greek symbols: AIS, DLC, FOWT, GPU,
  IDTxl, IEA, IEC, JIDT, JONSWAP, KSG, ML, NREL, OMA, OpenFAST, ROSCO, SCADA, SURD, TE, TurbSim (upright, same
  layout). Expansions verified against first-use context. pack PASSED, 430→450 paras. Backup `…bak-<ts>-abbrevs`.

- **Prev (2026-08-11, session 29): added a Nomenclature (Latin + Greek symbols, alphabetical) after the keywords.**
  Author: "make a Nomenclature in alphabetic order, grouped by English and Greek." Harvested all symbols from the
  docx math tokens + Greek contexts; inserted a Heading2 "Nomenclature" between keywords and §1 with two bold
  subheadings — **Latin symbols** (28, alphabetical) and **Greek symbols** (α, γ²(f), Δf, τ). Symbols italic with
  real sub/superscript runs; hanging-indent + tab layout; Compact style, left-justified. Acronyms NOT included
  (author asked only for English+Greek symbol groups; offered separately). "English" → labelled "Latin symbols"
  (standard convention). pack PASSED, 395→430 paras; pandoc verified both groups. Backup `…bak-<ts>-nomenclature`.

- **Prev (2026-08-11, session 28): Fig 5b — materiality gate moved to legend; footnote facts moved to §3.3 text.**
  Author: move the "SURD materiality gate 0.02" label to the legend, and the footnote (54 joined cases, first-pass
  KSG TE table, TE nonzero in only 2, positive in all 54) to text. Fig 5b = `surd-vs-te.png`. Removed inline gate
  annotation + added a "materiality gate (0.02)" legend entry; removed the `fig.text` footnote. Replaced the §3.3
  roadmap sentence with one carrying the footnote facts and citing Fig 5b (positivity already stated by the
  adjacent 5a sentence, so not repeated). Same PNG size (1480×880) → drop-in; other two SURD figs unchanged.
  image6 md5 verified (bb594c31…); pack PASSED, 395 paras. Backup `…bak-<ts>-fig5b`. (The "48/51, 94%" box was
  left in the figure — not part of the request; note it's still figure-only.)

- **Prev (2026-08-11, session 27): stated the IEA-15MW rated wind speed (10.59 m/s) in methods + Fig 5a caption.**
  The numeric rated speed was missing paper-wide despite the below/above-rated framing depending on it. Added
  "with a rated wind speed of 10.59 m/s" to the methods turbine description (Gaertner et al., 2020) and "(10.59
  m/s)" to the Fig 5a caption after "at and above rated". pack PASSED, 395 paras; both verified via pandoc.
  Backup `…bak-<ts>-ratedspeed`. (Context: followed a Q&A on why 8 m/s has no active pitch control — below
  rated the turbine is in Region 2, pitch parked at fine, torque loop active; pitch loop engages above rated.)

- **Prev (2026-08-11, session 26): Figure 5a — two-tone regime background bands (inactive grey / active teal).**
  Author asked to color-distinguish the two regimes; chose two-tone bands. Added two `axvspan` bands to the
  dose-response block of `_make_surd_figs.py` (grey α0.08 below-rated, teal α0.10 at/above-rated) split by a
  subtle dashed divider at the rated boundary (x=0.5, between 8 and 11 m/s), zorder 0–1 behind grid/data.
  Same PNG size → drop-in replace of `media/image5.png`; other two SURD figs unchanged. image5 md5 verified
  (254fea0f…); pack PASSED, 395 paras. Backup `…bak-<ts>-fig5a-bands`.

- **Prev (2026-08-11, session 25): Figure 5a — added dot/bar/gate legend; moved footnote facts into the §3.3 text.**
  Author: dot/bar/dash must be a legend; "circular-shift bias control subtracted / drop positive in 100%" must be
  in the text. Fig 5a = `surd-dose-response.png` from `_make_surd_figs.py`. Added a 3-item Line2D legend
  (individual case / regime median / materiality gate 0.02), removed the bottom footnote + redundant inline gate
  label. Revised the §3.3 dose-response sentence to state the bias-correction (circular-shift surrogate) and the
  "positive in every one of the 54 closed-loop cases." Same PNG size (1480×840) → drop-in; other two SURD figs
  re-rendered identical. pack PASSED, 395 paras; image5 md5 verified. Backup `…bak-<ts>-fig5a-legend`.

- **Prev (2026-08-11, session 24): narrated the Figure 5a dose–response result in Section 3.3.**
  User asked whether Fig 5a's point (firewall strength scales with operating region, ~2.8×) was in the text.
  It wasn't — §3.3 only pointed to the figure; the 2.8× factor and regime medians lived solely in the plot.
  Added one sentence to the SURD-redirection paragraph (docx `document.xml`) stating it: corrected controller
  leak-drop rises from a below-rated median 0.023 (pitch idle) to ~2.8× larger at/above rated (per-regime
  medians 0.042–0.066), positive in all 54 cases (Figure 5a). Numbers verified against `media/image5.png`.
  pack PASSED, 395 paras. Backup `…bak-<ts>-fig5a-doseresponse`.

- **Prev (2026-08-11, session 23): normalized "§" → "Section"/"Sections" throughout the docx.**
  Author: "the § sign within the text is not common." The docx already spelled out Section(s) in most places,
  so the 27 § were the inconsistent minority. Converted all in `document.xml`: multi-ref runs got plural
  grammar ("(Sections 2.2–2.9)", "(Sections 2.4 and 2.7)"); remaining single refs incl. Kraskov "§III.A" →
  "Section III.A". Fixed a self-inflicted glue ("Section2.7"→"Section 2.7") and restored two trimmed trailing
  spaces. Verified 0 § / 0 glued / 0 double-space; pack PASSED, 395 paras. Backup `…bak-<ts>-section-signs`.

- **Title decision (2026-08-11): title KEPT as "An information-flow firewall in floating offshore wind turbines: the controller as structural shield."**
  Author floated changing it to "information-flow considerations on Floating Offshore wind turbine." Claude pushed back
  ("considerations on…" is a vague, finding-free pattern that drops the firewall hook; also singular/capitalization
  slips) and offered a toned-down and a sober-descriptive alternative. Author chose **keep current**. No file change.

- **Latest (2026-08-11, session 22): shortened Figure 4 caption; moved the detail into the running text.**
  Author: "caption too long — make it shorter; if we keep it, it must be within the text." Trimmed the docx
  caption (`document.xml`) from ~90 words to one sentence ("**Figure 4.** Directed transfer-entropy network
  across the FOWT. Edge weight is the mean $TE_{frac}$ over the 54 cases."), removing the redundant second
  $TE_{frac}$ math + descriptive prose. Relocated the kept content (wave propagation/significance; wind
  intermittency + edge-label meaning; the firewall statement) into the paragraph that introduces the figure.
  `PYTHONUTF8=1 pack.py` → validations PASSED, 395 paras; pandoc re-extract confirms. Backup `…bak-<ts>-fig4-caption`.

- **Prev (2026-08-11, session 21): redesigned Figure 4 (TE network) — legible labels + a clearer firewall.**
  Author: "white font not clear; firewall part must be clearer." Fig 4 in the docx = `media/image4.png` =
  `reports/figs/fig3-te-network.png` from `_make_fig3_firewall_network.py`. Fixes to the generator:
  (1) contrast-aware node labels (`_lum` → dark ink on the light-green platform nodes, white elsewhere, with
  halos) — node colours unchanged; (2) firewall consolidated from 3 scattered cues into one motif — wind's
  bold dashed arrow hits a hatched red **wall + ✕**, a faint arrow shows the blocked continuation into the
  highlighted platform zone, plus one boxed **FIREWALL** label + a white-boxed "no significant edge (TE ≈ 0)"
  callout. New PNG same size (1900×1309) → drop-in replace, no XML/extent change. Embedded via unpack→replace→
  `PYTHONUTF8=1 pack.py`; validations PASSED, 395 paras; image4 md5 == fig3 md5; TNR + jc=both still intact.
  Backup `…bak-<ts>-fig4-redesign`.

- **Prev (2026-08-11, session 20): manuscript formatting pass on the canonical docx — Times New Roman, justified body, data-table rules removed.**
  Author asked for three docx changes (final.md FROZEN, untouched): (1) font → **Times New Roman**
  (changed `theme1.xml` major+minor `<a:latin>` from Aptos; Cambria Math + Consolas code kept — author
  chose "keep code monospace"); (2) **justify** body prose (`jc="both"` on `BodyText` style → cascades to
  FirstParagraph/Compact; headings + centered equations unaffected); (3) delete **data-table rules** — author
  clarified this meant the horizontal rules *inside* the data tables (not equation boxes); the only visible
  rules were 16 inline booktabs borders in **Table 1**, set `single`→`nil`; equation `TableGrid` boxes left
  intact. Repack `PYTHONUTF8=1` → validations PASSED, 395 paras preserved. Round-trip verified at XML level
  (no LibreOffice on this box → no PDF visual). Backup `…bak-<ts>-fmt-tnr-justify-rules`.

- **Prev (2026-08-11, session 19): added in-text `(Eq. N)` citations for Eqs 7, 8, 9 in the canonical docx.**
  Author asked to cite Eqs 7/8/9 within their introducing prose, as Eqs 1–6 already are. Edited
  `reports/te-firewall-paper.docx` `document.xml` directly (final.md FROZEN, untouched): §2.5 AIS gets
  "…storage of the target **(Eq. 7)**,"; §2.7 SURD gets "…synergistic atoms **(Eq. 8)**:"; §2.9 delay-resolved
  TE gets "…candidate delay $d$ is **(Eq. 9)**:". Repack required `PYTHONUTF8=1` (cp949/Korean-locale codec
  error in the validator on `fontTable.xml`); with UTF-8 forced, all validations PASSED, 395 paragraphs
  preserved. Verified via pandoc re-extract. Backup `…bak-<ts>-eqcite789`. (The two §2.7 target/source slips
  from session 18 remain unfixed — author has not yet asked.)

- **Prev (2026-08-11, session 18): synced `te-firewall-paper-final.md` §2.7 to the docx's rewritten SURD paragraph; explained why Eq. 8 has no leak.**
  Author added Eqs 7–9 to the docx and rewrote §2.7, and asked (a) why the leak is absent from the SURD
  decomposition (Eq. 8) and (b) to revise the md to match. Answer to (a): Eq. 8 is an identity for the *mutual
  information* `I(Q; sources) = R + U + S`; the leak is not part of the MI — it lives in the entropy budget
  `H(Q) = I(Q; sources) + ΔI_leak`, so its omission is correct and matches the SURD convention
  (Martínez-Sánchez et al., 2024). The md already carried Eqs 7/8/9 matching the docx; only §2.7 prose differed.
  Per author choice ("mirror docx wording into md") the md §2.7 post-equation paragraph now uses the docx wording,
  **with two corrections**: the docx says the leak captures "the source's future" and classifies atoms "about a
  source" — both should be the *target's* future `Q` (the leak is defined against `H(Q)`); and the docx §2.7 XML
  has a garbled duplicated tail fragment ("...3.1–3.2.ture entropy — ... 3.1–3.2."). The md was corrected/cleaned;
  **the docx (canonical) still carries both slips + the dangling fragment — flagged to the author for a separate
  in-place XML fix, not yet applied.**
  **Update (later in session 18):** author flagged the garbled tail directly; the **duplicate/corrupt tail fragment
  in the docx §2.7 was removed** (member-preserving XML edit; backup `…bak-20260811-130116-surd27junk`; testzip
  clean, 26 members, structure intact, §2.7 now ends "…Sections 3.1–3.2."). The **two target/source slips in the
  docx §2.7 remain unfixed** (author has not yet asked to change them; md already correct).

- **⚠ CANONICAL SOURCE FLIPPED (2026-08-10, author decision): `reports/te-firewall-paper.docx` is the LIVE MASTER; `te-firewall-paper-final.md` is FROZEN.**
  The author hand-edited the docx (numbered §2.1 equations (1)–(6); minor prose tweaks) and Claude added the
  in-text `(Eq. N)` citations directly in the docx. Asked how to sync, the author chose **"docx is canonical
  now."** So: **DO NOT run `pandoc → te-firewall-paper.docx`** — it would wipe the manual numbering + edits and
  is destructive. All future paper edits go **directly into the docx** (unpack → edit `word/document.xml` →
  `pack.py` with `PYTHONUTF8=1`). The markdown is an archived draft only. Rule recorded in
  [[project_paper_two_copy_sync]] (memory) and a `DO NOT REGENERATE` HTML-comment banner sits at the top of
  `te-firewall-paper-final.md`.

- **Latest (2026-08-10, session 17): cleaned up Figure 3 (case matrix) — removed the top subtitle line, moved the legend to right-centre.**
  Original figure had no saved generator (one-off; `_make_figures.py` `make_fig2()` is the superseded stale
  version). Wrote a dedicated reproducible generator `reports/figs/_make_fig3_case_matrix.py` (marker colours
  sampled from the original for fidelity), reproducing the 54-run grid with the subtitle removed and the legend
  at right-centre; kept title, `n =` counts, axis labels. Re-embedded in the docx (swapped `image2.png` and
  fixed the drawing extent `cy 3147995 → 2072669` for the new wider aspect, no squish). File keeps the name
  `fig2-dlc-matrix.png` though it is Figure 3. Backup `.bak-20260810-191545-fig3refresh`.

- **Latest (2026-08-10, session 17): shortened the Figure 2 caption; moved the module detail into §2.2 body.**
  Caption was a full paragraph enumerating every module. Trimmed it to one identifying sentence ("Figure 2.
  OpenFAST coupled aero-hydro-servo-elastic model — the modules used in this work and their coupling.") and
  relocated the enumeration into the §2.2 lead-in (external conditions → applied loads → turbine dynamics),
  avoiding duplication of the HydroDyn-QTF and ROSCO settings already there. Docx edited in place; structure
  unchanged; no content lost (all module keywords retained); backup `.bak-20260810-182831-prefig2cap`.

- **Latest (2026-08-10, session 17): retitled the manuscript.**
  New title: **"An information-flow firewall in floating offshore wind turbines: the controller as structural
  shield"** (was "An Information Firewall Between Wind and Platform Motion in Floating Offshore Wind Turbines:
  A Transfer-Entropy Analysis with Implications for Health Monitoring"). Leads with the firewall concept,
  credits the controller as the mechanism, and the "structural shield" subtitle stays within demonstrated
  scope (avoids asserting the unvalidated malfunction-diagnosis application). Edited the canonical docx in
  place across all three title locations (`document.xml` Title paragraph, `core.xml` `dc:title`, `app.xml`
  `TitlesOfParts`); structure unchanged; backup `.bak-20260810-181622-pretitle`. Markdown title left frozen.

- **Latest (2026-08-10, session 17): committed the Figure 2 work (`35140de`); cross-referenced §2.7 SURD from §2.1 and trimmed the duplicated atom listing.**
  Reviewed the uncommitted session-16 Figure 2 insertion, independently re-verified the +1 figure renumbering
  (captions + all in-text refs + internal cross-refs shift consistently), and committed it (`35140de`) with the
  previously-uncommitted §2.1 equation back-references and finalized records. Then, on the author's structural
  question ("should §2.7 SURD merge into §2.1 or move to §2.2?"), recommended **keep §2.7 in the methods cluster
  + add a cross-reference** — rejecting merge-into-§2.1 (would mix general theory with study-specific SURD
  params: `nbins=3`, atom names, normalization) and move-to-§2.2 (that section is the plant/campaign, not
  analysis methods). §2.1 already ends with the SURD *motivation* ("a limitation of pairwise TE…"); §2.7 holds
  the mechanics and directly feeds §2.8. Author agreed. Edited the canonical docx in place (`zipfile`, UTF-8):
  §2.1's closing SURD paragraph now defers to §2.7 ("…decomposing…into those distinct components…; the
  decomposition and its operating parameters are detailed in §2.7."), removing the duplicated
  unique/redundant/synergistic+leak listing. Structure unchanged (390 paras, 10 imgs, 12 tbls, 113 eqs, 8
  fig-caps); backup `.bak-20260810-175002-presurdxref`.

- **Latest (2026-08-10, session 16): added OpenFAST module schematic as Figure 2 (§2.2), corrected + renumbered.**
  Author asked to add a coupled-model schematic "so everything is clear." Verified every label against the
  actual run (`sims/dlc16_v11ms_s00`) and found errors in the author's PNG: OpenFAST **4.2.1→4.2.0**; **BeamDyn
  not used** (ElastoDyn blades); HydroDyn **"Morison drag"→"potential-flow (WAMIT) + 2nd-order difference QTF"**
  (`NMembers=0`, `DiffQTF=12`); AeroDyn **"dynamic stall"→"BEMT + tip-loss + dynamic wake (DBEMT)"**. Built a
  matplotlib generator `reports/figs/_make_fig0_openfast_modules.py`, inserted the corrected PNG into the
  canonical docx as **Figure 2** at the top of §2.2 (image10.png + rId1000 + caption + in-text ref; §2.2 now
  says "OpenFAST v4.2.0"), and renumbered old Figures **2→3 … 7→8** (4a/b/c→5a/b/c) across all 19 refs.
  Validation PASSED; captions now 1,2,3,4,5,5a/b/c,6,7,8. Rendered-PDF check skipped (no LibreOffice on this
  box); PNG viewed OK. Backup `.bak-20260810-160945-prefig2`. **Committed `35140de`** (session 17).

- **Latest (2026-08-10, session 15): cited equation numbers (1)–(6) in §2.1 text (docx edited in place).**
  Author numbered the six §2.1 theory equations manually in the docx and asked to cite them in the running
  text. Edited the docx in place (unpack → `document.xml` → repack; validation PASSED) — six `(Eq. N)` refs at
  the lead-in sentences (Shannon/joint-entropy/MI/entropy-rate/TE-def/entropy-rate-difference). Deliberately
  did **not** regenerate from markdown (would wipe the author's manual numbering + prose edits). Backups:
  `.bak-20260810-143806-preeqcite` (pre-citation) and `.bak-20260810-105802-pre2p1enrich`. See divergence flag
  above.

- **Latest (2026-08-10, session 14): §2.1 theory enrichment from Chen et al. (2019) + multivariate X vector.**
  Author asked whether to enrich the theory formula using the newly-added Chen et al. (2019) fault-detection
  paper, and to introduce `X = [x1,…,xn]`. Assessment surfaced that Chen is **already** cited 5× + in refs
  (the Shannon→MI→entropy-rate→TE buildup and the four-parameter framing already borrow it), so enrichment
  was scoped minimal. Author chose the **recommended** option (joint entropy + X vector; declined Chen's
  Eq. 7 joint-probability expansion, which clashes with the estimator-agnostic KSG framing of §2.4). Made two
  edits to `reports/te-firewall-paper-final.md` §2.1: added `H(X,Y) = -Σ p(x,y) log p(x,y)` between Shannon
  and MI (completing Chen's Eq1→Eq2→Eq3 chain), and introduced bold `**X** = [x1,…,xn]` tied to Table 1,
  reconciling scalar `X`/`Y` = components `x_i,x_j`. Fixed the `z1`→`x1` typo + vector/scalar-X collision via
  bolding. No results/tables/§2.4 touched; docx/PDF not regenerated.

- **Latest (2026-08-09, session 13): text audited for leftover Sobol; Figure 5 rebuilt (was stale Sobol).**
  Author asked whether removing the Sobol arm from Figure 1 required text deletions. **Text: no changes
  needed** — RAFT/Saltelli/design-parameter/Phase-6/two-arm/hybrid vocabulary is entirely absent; the two
  "Sobol" mentions are §1.2 foils (kept); "sensitivity" mentions are all generic. **But** the check found
  `fig5-combined-graph.png` was still the stale two-arm Sobol image (design-variable column + Sobol $S_T$
  edges), contradicting its TE+SURD caption/body. **Rebuilt** via new `reports/figs/_make_fig5_firewall_graph.py`
  (te_table wave edges + paper's SURD values): Wave→responses TE web, Wind→BldPitch1 (SURD ≈ 0.40),
  BldPitch1→PtfmPitch (U = 0.167), explicit empty wind→platform firewall. Old generator bannered SUPERSEDED
  (backup `fig5-combined-graph.png.bak-sobol`). docx regenerated. Remaining figure item: a visual spot-check
  of Figures 4a–c (SURD) and 6–7 (delay), which are in-scope and whose captions match.

- **Latest (2026-08-09, session 12): Figure 1 rebuilt to match the paper; Figures 2–3 audited.** Author
  flagged a possible "Sobol arm" in Figure 1 — confirmed stale: the old `fig1-methodology-arms.png` (from
  the superseded `reports/figs/_make_figures.py`) drew the broader original project's "TE arm + Sobol arm →
  Phase-6 combined causal graph" hybrid, which this paper does not do (Sobol is only a critiqued foil in
  §1.2). **Rebuilt** via new `reports/figs/_make_fig1_pipeline.py`: 3-arm schematic (directed TE [primary] ·
  linear coherence [foil] · SURD [mechanism] → monitoring-signature), matching the caption; committed.
  Added a "SUPERSEDED — DO NOT RUN" banner to `_make_figures.py`. **Figure 2 OK** (on-disk case-grid matches
  caption; not the stale box-diagram; minor British-spelling in its title). **Figure 3 DEFECT (fix pending):**
  `fig3-te-network.png` showed wave-only edges in TE_frac %, but its caption promised a wind+wave directed
  network showing the firewall (wind reaches blade/tower, not platform). Cause: the old generator's
  ">50%-of-cases-significant" filter dropped every wind edge. **REBUILT (author chose Option A):** new
  `reports/figs/_make_fig3_firewall_network.py` draws both drivers — Wave1Elev solid (width ∝ TE_frac) to
  its 7 channels; Wind1VelX dashed red to blade/tower (RootMxc1 39%, TwrBsMyt 28%, RootMyc1 17% of cases
  significant); wind→platform as a blocked ✕ + shaded "FIREWALL" band. Caption updated ("TE in nats" → mean
  TE_frac). Old generator bannered SUPERSEDED. docx regenerated. **All three figures now match the paper.**

- **Latest (2026-08-09, session 11): whole manuscript converted to US spelling.** Resolves the
  British/American mix the reverse-sync left. Explicit case-preserving map (not a blanket -ise→-ize, which
  would wrongly hit comprise/revise/precise), **References excluded** (cited titles stay verbatim): **85
  replacements** across 26 forms — analysed→analyzed, normalised→normalized, realisation(s)→realization(s),
  organis*→organiz*, quantisation→quantization, neighbour(s)→neighbor(s) ×17, artefact(s)→artifact(s) ×11,
  behaviour→behavior, favourable→favorable, labelled→labeled, modelled/modelling→modeled/modeling,
  analogue→analog, grey→gray, etc. Same-in-both words left alone. **Verified:** post-scan 0 residual British
  spellings in body; References untouched; docx regenerated (backup `…docx.bak-20260809-203601-preusspelling`;
  9 media, 6 tables, 0 stray British forms). Manuscript is now consistently US-spelled. Committed. (One
  debatable case flagged: analogue→analog in the "counterpart" sense — reversible.)

- **Latest (2026-08-09, session 10): reverse-sync — the author's manual `.docx` edits were merged back
  into `final.md`.** One-off reversal of the usual md→docx direction ([[paper-two-copy-sync]]). Author
  edited `reports/te-firewall-paper.docx` in Word; detected the real edits by diffing a fresh
  md-generated reference docx against it (identical pandoc path ⇒ only author edits surface; the ~13
  equation "diffs" were Word OMML/minus re-serialization and were ignored — md LaTeX untouched). Applied
  10 prose changes: four reworded paragraphs (§1.1 floating-monitoring; §1.2 common-methods, TE, gap),
  **§1.2 heading "Gap" → "Motivation and Contribution"**, and small edits. Author's rewrites came through
  plain (italics lost); applied verbatim. **Author decisions on flags: keep the US spellings**
  (stabilizes/recognized/organized — paper is otherwise British, so now a deliberate mix) and **restore
  `*information firewall*`** italics at its defining sentence only. **Verified:** fresh md→docx reference
  re-diffed against the author's docx = 0 prose differences; docx regenerated from synced md (author's
  edited copy backed up `…docx.bak-20260809-202844-usermanual`); 9 media, 6 tables. Committed. **Note the
  British/American spelling is now mixed by author's choice — a full US conversion is the obvious follow-up
  if a US venue is chosen.**

- **Latest (2026-08-09, session 9): paper reorganised — Background + Gap folded into the Introduction;
  Theory + Methods became §2.** At the author's request, old §2 "Background and Related Work" (SHM/CM +
  blade-pitch control) and the §2.4 gap statement moved **into §1** as light subsections **§1.1 Background**
  and **§1.2 Gap** (author chose subsection headings over continuous prose); TE theory (old §2.3) now heads
  a new **§2 "Theory and Methods"** with the former §3 methods (§2.1 theory, §2.2–§2.9 methods), and the
  Figure 1 pipeline overview moved to the §2 preamble. Downstream renumber: Results §4→§3, Discussion
  §5→§4, Conclusion §6→§5. Done via one cascade-safe Python script (`scratchpad/restructure.py`): authored
  §1 merge (CM duplication removed, §2.2 compressed, gap recap trimmed) + heading-anchor slicing + single-
  pass heading/cross-ref renumber. **Verified:** heading tree exact; all Section/§ cross-refs consistent
  (ranges + "and"/comma lists handled; no stale §5.x/§6); 9 figures (Fig 1 once), 6 tables, 30 refs, first-
  person 0. docx regenerated (backup `…docx.bak-20260809-170128-prerestructure`). **Committed.**

- **Latest (2026-08-09, session 8): Introduction strengthened + 10 verified references added (Tier 1+2).**
  Executed the queued Introduction/literature work from the 2026-08-07 prep doc (`reports/introduction.md`,
  Parts A–E). User picked (decision prompt) **reinforce §1 in place** (not a CPM re-lead) and **Tier 1+2**
  scope. Added 10 DOI-re-verified references — list **20 → 30**: Nichols 2005/2006 (TE-in-SHM lineage),
  Harris 1989 + Jelali 2006 (control-performance monitoring), Granger 1969 + Sugihara 2012/CCM (situate TE
  among causal methods), Kostecka 2025 + Park 2025 (floating SHM / closest adjacent work), Badihi 2022 (WT
  CM review), Namik & Stol 2010 (IPC). **§2.4 gap statement reframed** to the "earned-novelty" version
  (acknowledges Nichols + Harris/Jelali, then differentiates the controller-induced-*absence* quantity).
  Insertions in §1/§2.1/§2.3/§2.4/§5.2; one differentiating sentence vs Nichols + a one-line CCM nod (prep
  doc's safe defaults). One correction on verify (Sugihara: Hsieh C. → **C.-H.**). **Verified:** 30 refs
  alphabetical, Nichols-2006-before-2005 per APA 7.0, no orphan cites, first-person residual 0 (3 hits are
  all `10.1002/we.NNN` DOIs). docx regenerated by plain pandoc (backup
  `te-firewall-paper.docx.bak-20260809-161333-prelit`). **Deferred:** W6 canonical Sobol/coherence foil
  cites (need their own verified refs). Not committed. Now **all 2026-08-07 + this session's edits are
  uncommitted** on top of 3e3c030.

- **Latest (2026-08-03, session 7): project artifacts ingested into the `pages/` wiki
  graph (LLM Wiki pattern's "ingest" op).** User introduced the vault's origin (Karpathy
  LLM-maintained-wiki pattern, `LLM_Wiki_Pattern.md`), then asked to ingest the project
  directory into the wiki. Confirmed via decision prompt: target = **main `pages/` wiki**
  (not `vault-legacy/`), scope = **project artifacts** (excl. vendored `repos/`, binary sim
  outputs, build-script noise). Found the theory/reference layer well-covered but the project
  *state* living only in SYNTHESIS/log/memory and `analyses/` **empty**, and `overview.md`
  badly **stale** (dated 2026-05-12, "nothing verified / Phases 2–6 pending"). Created **8
  pages**: entities `te-pipeline`, `compute-servers`, `surd`; concepts `information-firewall`,
  `blade-pitch-health-monitoring`; analyses `te-firewall-54case-2026-08-03`,
  `firewall-attribution-surd-openloop-2026-08-03`, `firewall-manuscript-status-2026-08-03`.
  Updated `index.md`, **fixed the stale `overview.md`** (all 6 phases done + firewall finding),
  appended a `pages/log.md` ingest entry. All numbers cross-checked against the vetted
  manuscript `reports/te-firewall-paper-final.md`, not re-derived. **Verified:** 8 pages
  present; broken-link scan of the new pages = 0 (4 unresolved links are pre-existing index
  stubs). Deferred: full lint pass + reconciling `open-questions.md`/`wiki-improvement-plan.md`
  with the completed campaign. Not committed.

- **Latest (2026-08-03, session 6): title changed to drop the controller over-claim.**
  Old: "…: Blade-Pitch Control Decouples Wind from Platform Motion, with Implications for
  Health Monitoring". New: "An Information Firewall Between Wind and Platform Motion in
  Floating Offshore Wind Turbines: A Transfer-Entropy Analysis with Implications for Health
  Monitoring". Reason: old title asserted controller-as-mechanism (the exposed flank —
  open-loop TE-converse null + possible structural filtering); new title leads with the
  firewall finding + method, attribution stays in the body (SURD, contribution #2). User
  picked the "drop controller from title" option. Docx rebuilt+verified (backup
  `te-firewall-paper.docx.bak-20260803-161642`). UNCOMMITTED since 00a6156: abstract trim
  (session 5) + this title change.

- **Latest (2026-08-03, session 5): abstract trimmed 422 → 249 words** (MSSP/Elsevier ~250
  limit). Preserved all load-bearing claims/numbers (0.0009/0.029/3.7%/0.121/100%/0.72/54);
  dropped from the abstract only the te_frac 0.04% detail (kept in §4.1) and the per-channel
  delay list (kept in §4.5/Table 5). Refs still APA (venue undecided; numbered conversion
  available if Elsevier). Docx rebuilt+verified (backup `te-firewall-paper.docx.bak-20260803-160353`,
  1,842,062 B). Committed set 00a6156 is PRIOR to this abstract trim → the trim is uncommitted.

- **Latest (2026-08-03, session 4): carried-over reviewer polish (items 2/3 fixed; 1/4
  held).** (2) §5.3 rotor-averaged-check sentence de-narrated — dropped "we had expected …
  has since been computed" → "the open-loop twin's wind→platform TE is itself null (§4.3),
  … rather than as settling the attribution" (timeless). (3) Intro "This paper makes three
  contributions" → "two contributions and develops a motivated outlook" (+ prose "The two
  contributions above … Beyond them, we develop"), and fixed a cross-ref (graded-fault
  campaign is §5.3, not §5.2). (1) Rotor-averaged wind check STILL queued in §5.3 — can't run
  (server down; and must use ambient disk-average from wind.bts, NOT RtVAvgxh which is
  motion-contaminated, corr −0.31 w/ PtfmPitch); hedged framing is the protection, expect a
  major-revision ask. (4) Venue UNDECIDED → abstract kept at 422 words, refs kept APA
  author-year (19 entries); trim-to-~250 + numbered-ref conversion deferred until a venue is
  chosen (MSSP/Elsevier would need both; Wind Energy Science would not). Docx REBUILT +
  verified (backup `te-firewall-paper.docx.bak-20260803-154604`, 1,842,437 B; document.xml
  PASS — item 2/3 edits present, old text/leaks/dup-captions absent). Not committed.

- **Latest (2026-08-03, session 3): duplicated figure captions fixed.** Reviewer/author
  found every one of the 9 figures showed TWO captions in the rendered PDF/docx. Root cause:
  each image carried descriptive alt-text (`![Figure N. …](figs/…)`) and pandoc's
  `implicit_figures` renders non-empty alt-text as a figure caption — which then sat above
  the formal `**Figure N.**` caption. Fix: stripped the alt-text on all 9 images
  (`sed 's#!\[[^]]*\](figs/#![](figs/#g'`) so pandoc no longer auto-captions; the bold
  caption is now the sole caption. Verified in md (0 `![Figure`, 9 `![](figs/`, 9 `**Figure`)
  and in the rebuilt docx (backup `te-firewall-paper.docx.bak-20260803-153837`; document.xml
  scan: 7 alt-only phrases ABSENT, 4 sampled bold captions PRESENT ×1 each, leak regression 0).
  Docx current (1,842,477 B). Not committed.

- **Latest (2026-08-03, session 2): internal pipeline/code artifacts stripped from the
  manuscript (reviewer: "internal pipeline artifacts must come out").** A reviewer flagged
  that the paper cited internal repo paths as if reader-visible and carried an ARS-pipeline
  workflow note. Verified against the file and found MORE than the reviewer listed; removed
  all of them per user instruction ("remove the parts related to code and code files"),
  6 edits to `reports/te-firewall-paper-final.md`: (§References) deleted the note
  "*(APA 7.0 … verified at the Stage 2.5 integrity gate …)*"; (§3.4) dropped "read directly
  from te_pipeline.py"; (§3.7) dropped "(monitor_signature.parquet)"; (§3.8) dropped
  "implemented in delay_analysis.py"; (Data Availability) removed the four `.parquet` paths
  + two `.py` code-file names, retitled to "Data and Code Availability Statement", rewrote
  to "available from the corresponding author on reasonable request [Add repository/DOI at
  submission]"; (repro block) dropped "read directly from te_pipeline.py … repository commit
  to be fixed at submission". Verified: grep for `.py` / `.parquet` / `analysis/` / `reports/`
  / Stage-2.5 / integrity-gate / repository-commit → **zero matches**. All methodological
  content preserved. Then (user go-ahead) also cleaned the **AI-Usage Disclosure**: dropped "via the
  academic-pipeline workflow" and "at Stage 5" → "with AI assistance (Claude) … [Adjust to
  the target venue's AI-disclosure policy before submission]". Still carrying legit
  `[To be completed]` placeholders in CRediT/Funding (author's call, not leaks).
  **Docx REBUILT + verified (2026-08-03):** backup `te-firewall-paper.docx.bak-20260803-152834`,
  `pandoc te-firewall-paper-final.md -o te-firewall-paper.docx` (1,842,996 B); document.xml
  scan PASS — 10 leak strings (Stage 2.5 / integrity gate / te_pipeline / delay_analysis /
  .parquet / academic-pipeline workflow / at Stage 5 / monitor_signature / analysis/ /
  reports/) ABSENT, 5 content markers (Data and Code Availability, fault-adjacent, reasonable
  request, AI assistance (Claude), Blade-Pitch Control) PRESENT. Docx now current with the md
  for ALL of today's edits. Parquet sync remains independent/deferred (doesn't affect paper
  text). Not committed.

- **Latest (2026-08-03): §4.4 + §5.3 currency defect closed — the open-loop/pitch-lock
  "pending" language that a reviewer flagged as "worst of both" is gone; the computed
  null is now reported consistently.** A reviewer note observed §4.4 still said the
  pitch-lock fault case "does not yet have its transfer-entropy legs computed ... recorded
  as pending ... queued as a separate task" — directly contradicting §4.3, which already
  reports that same case (`dlca_v11ms_s00_openloop`, the open-loop twin) as a computed
  NULL. Root cause: the 2026-07-31 NEW-2 fix updated §4.3's currency but explicitly left
  §4.4 out of scope, and `monitor_signature.parquet` still carries that row as NaN /
  "pending TE legs". **Decision (user): "Reconcile & report the null"** — no re-run (the
  71.4 h CPU job already returned the null), no reframe to proof-of-concept (open-loop ≠
  pitch fault, n=1 stands). Applied THREE surgical prose edits to
  `reports/te-firewall-paper-final.md`: (§4.4) replaced the false "pending/queued"
  sentence with "the one fault-adjacent run — the open-loop twin (§4.3) — has its
  wind→platform TE computed and it is null; but loop≠fault and n=1, so it probes the
  attribution *mechanism*, not the monitoring hypothesis; the graded pitch-fault campaign
  (§5.3) is what the hypothesis requires and is not run here"; (§5.3) fixed "computing TE
  for the existing pitch-lock case" (stale — done) → "the graded-fault runs do not yet";
  (§5.3) fixed "the pending open-loop TE legs would settle the attribution" → "has since
  been computed and is null (§4.3), read cautiously". Abstract/intro/§4.6/conclusion
  UNCHANGED — their "no computed fault-case TE" is still true (open-loop = fault-*adjacent*,
  not a fault-case). Verified: grep for pending / existing pitch-lock / queued-as-separate /
  legs-computed / "the runs do not yet" → all gone; only the (true) injected-fault
  future-work statements remain. **OPEN / next step (DEFERRED — user temporarily off the server, 2026-08-03):** the durable
  artifact `reports/te_fault_openloop.parquet` is on the CPU server (isaactest@…) and is
  GITIGNORED (`reports/*.parquet`; only `surd_table.parquet` is force-tracked), which is
  why `git pull` never brought it. Plan: server `git add -f` + commit + push → pull here →
  update the `dlca_v11ms_s00_openloop` row of `monitor_signature.parquet` (NaN →
  te_wind_pitch≈0.0, sig=False) from the parquet → force-add both. NOT committed yet;
  prose edits are local only. Docx NOT yet regenerated (do after parquet sync so one rebuild
  covers everything).

- **Latest (2026-07-31, session 2): round-3 re-review confirmed + its two NEW issues
  fixed — technical body now submission-ready.** Ran `academic-paper-reviewer` re-review;
  a round-3 report already existed (2026-07-29, Minor Revision) confirming all round-2
  RR1–RR10 + S1–S4 addressed, but it flagged two post-round-2 issues that were STILL live
  in the manuscript. Fixed both: **(NEW-2, Major)** §4.3 called the open-loop TE converse
  "pending / would close both arguments at once" — but `te_fault_openloop.parquet` had
  since returned a NULL (wind→platform TE does not rise with the loop open). Rewrote §4.3
  to report the null, cite the same-run significant control edge (Wave1Elev→FAIRTEN3, TE
  ≈ 0.055 nats, p=0.005) proving the null is real, untangle the open-loop-twin converse
  from the still-uncomputed §4.4 pitch-fault test, read it conservatively (n=1; loop≠fault),
  and fold in the "partly structural firewall" reading (cross-ref §5.1); attribution now
  rests on the two SURD lines, NOT the TE-converse. Abstract/§4.6 unchanged (SURD
  organisation-collapse leg stands). **(NEW-1, Minor)** §4.1 robustness sentence now flags
  it as wind-side-only + why full-campaign wave magnitudes aren't adopted (~4 s source-lag
  window truncates the 6.3 s wave→surge delay). Note: the 2026-07-29 "no paper edit"
  decision covered §4.4 monitoring framing, NOT this §4.3 currency defect — that gap is now
  closed. Docx regenerated + verified (md & docx, 7/7 checks); resolution addendum in
  `reports/te-firewall-review-round3.md`. **Remaining before submission: RR10 final scripted
  table re-check vs `te_table.parquet` (advisory) + front/back matter (CRediT/funding/COI/
  data DOI/AI disclosure) + citation-check. No scientific work left.** Not committed.


- **Latest (2026-07-31): the last open follow-up is CLOSED — paper §4.1 robustness
  sentence confirmed present + docx rebuilt/verified.** On review, the robustness
  sentence the 2026-07-29 decision called for was already committed at
  `reports/te-firewall-paper-final.md` line 201 (commit `2ba1d80`; `git log -L`
  confirmed) — full-campaign GPU (OpenCL–Kraskov) re-estimation reproduces and
  tightens the wind→platform firewall (surge sig 11%→0%, max wind→platform TE
  <0.005 nats, at/below chance floor), framed as robustness only with NO
  wave-magnitude edits. No new sentence written (would duplicate). Docx
  regenerated by convention: backup `te-firewall-paper.docx.bak-20260731-105217`,
  then `pandoc te-firewall-paper-final.md -o te-firewall-paper.docx`; rebuild
  byte-identical (1,842,543 B) to the 2026-07-29 build. Verified via
  document.xml text scan — 5/5 checks PASS (robustness sentence + first-pass
  Table 1/2 magnitudes 0.1214/0.1069 intact). **No paper work outstanding.**
  Not yet committed. Note: `te_table_full.parquet` / `te_fault_openloop.parquet`
  remain on the servers (only `te_table.parquet` is local) — pulling them for the
  archive is the one nice-to-have left, not blocking anything.

- **Latest (2026-07-29): BOTH server campaigns finished — CPU fault-TE = clean
  NULL, GPU te_table_full = complete (3888 rows).** (1) **CPU fault-TE (open-loop
  twin, PID 1992582, done ~71.4 h): NO firewall breach.** `compute_fault_te.py
  --eval-only reports/te_fault_openloop.parquet` → Wind→PtfmPitch/Surge/Heave all
  TE=0.0000, significant=False, above_ceiling=False vs the 0.029-nats healthy
  ceiling → "No breach demonstrated." Real null, not a pipeline failure: the same
  log carries a *significant* control edge (conditional Wave1Elev→FAIRTEN3,
  TE=+0.0550, p=0.0050). **Interpretation (agreed): open-loop ≠ a pitch fault**, so
  this null neither refutes nor supports the monitoring claim — it is a robustness
  data point on an imperfect proxy, n=1 (dlca_v11ms_s00_openloop, one seed, 11 m/s).
  **Decision: accept the null; §4.4 stays an OUTLOOK (no paper edit); round-1
  roadmap #1/#3 closed as "test executed."** Do NOT reframe as a positive
  "structural firewall" finding on n=1. Reserve (only if we later choose to upgrade
  §4.4 to proof-of-concept): run ONE *targeted* stuck-pitch / pitch-bias fault case
  (the correct instrument), not more open-loop seeds. (2) **GPU Phase-4 full
  campaign (lams, `run_phase4_full.sh`) COMPLETE** — `reports/te_table_full.parquet`,
  3888 rows across [54/54] cases (written Jul 21; the `[1]+ Done` only surfaced
  Jul 29 because that shell sat open ~8 days). Graph `reports/te_full_graph.pkl`
  (5 nodes, 4 edges). Method summary: granger 818/972 sig (84%), bivariate_te_ksg
  264/972 (27%), coherence 972/972 (100%), **conditional_te_ksg|Wave1Elev 0/486
  (0%)**, conditional_te_ksg|Wind1VelX 251/486 (52%) — conditioning on wave collapses
  all transfer (wave-mediation, the SURD story). This is the authoritative full
  table for the deferred **te_table_full re-verification before Stage 5**.
  **FIREWALL RE-VERIFIED (PASS, on lams):** bivariate_te_ksg gated on `significant`,
  Wind1VelX→PtfmPitch/Surge/Heave = 1/1/0 significant of 54 (chance floor ~2.7),
  max gated TE 0.0047 nats ≪ 0.029 → wind→platform statistically indistinguishable
  from noise. Positive controls strong: Wave→PtfmPitch 52/54, Wave→PtfmSurge 47/54;
  Wind→RootMxc1 7/54 (real wind→blade load, above chance) → firewall is
  platform-specific, exactly the thesis. Conditional-on-wave 0/486 corroborates
  wave-mediation. **RESOLVED — paper-numbers decision (user, 2026-07-29): KEEP first-pass
  `te_table` numbers; cite `te_table_full` only as a firewall robustness check.**
  The comparison IS apples-to-apples — paper Table 2 caption = "mean over 54
  simulations" (all 54, gated), same as the full-run means. Finding: wind side
  agrees and is *cleaner* in the full run (Wind→PtfmSurge sig 11.1%→0%; max
  wind→platform 0.029→0.0047), but wave→platform *magnitudes* run 3–5× lower and
  **Wave→PtfmHeave flips 87%→13% significant (47/54→7/54)**. Cause = te_table_full's
  `--max-lag-sources 20` ≈ **4 s** source-lag window at 5 Hz, SHORTER than the
  physical **Wave→PtfmSurge delay of 6.3 s (≈Tp/2)** from delay_profiles → the full
  run cannot see the wave→platform delay and UNDERESTIMATES wave TE. So te_table_full
  is the better instrument for the *wind/firewall* side (near-zero delay) but a
  *worse* one for wave magnitudes than the first-pass. ⇒ Do NOT rewrite Table 2/3;
  the paper's first-pass magnitudes stand. **Reserve (rejected for now): targeted
  re-run with `--max-lag-sources ≥35`** to compare on equal footing — not needed for
  the thesis. **Next:** add ONE robustness sentence to `te-firewall-paper-final.md`
  (full-settings GPU re-estimation reproduces the wind→platform firewall) + regen
  docx; the DON'T-adopt-full-magnitudes rationale is captured here + in
  [[project-phase4-full-campaign]]. Both A100s idle; no live pipeline procs.

- **Prev (2026-07-16): fault-TE run on the CPU server was WEDGED — watchdog
  kill-escalation fix committed (24a44b1); RELAUNCHED as PID 1992582.** Both
  pre-launch gates passed on the server: `test_watchdog_kill.py` reaped a
  SIGTERM-immune child in 3.0 s (the SIGKILL escalation path, exercised for
  real) and `test_ar1_te.py` gave the canonical 0.1892/0.0000 nats. Relaunch
  uses the extended 9-target `--slow-drift-targets` (all tau=5) +
  `PYTHONUNBUFFERED=1`; log `logs/fault_te.log`. When the parquet lands:
  `compute_fault_te.py --eval-only reports/te_fault_openloop.parquet`.
  Original wedge story: user's log tail +
  `ps` showed 0/63 jobs done at 46.5 h: job 1 (AIS RootMyc1, tau=1, 150 candidates)
  legitimately timed out at 9000 s on the CPU/JIDT backend, but job 2's JVM **ate the
  watchdog's SIGTERM** and `_execute_watchdog`'s bare `p.join()` blocked the parent
  forever (same mode as the old Phase-4 CPU shard wedge). Fix: `_kill_stubborn_child()`
  (terminate → 30 s grace → SIGKILL) + regression test `analysis/test_watchdog_kill.py`;
  pushed on `phase4-full-rerun`. Also found a stray 44-day `te_pipeline.py` probe
  (PID 546698, `/tmp/te_probe.parquet`) to kill. **Next on server:** kill wedged tree
  (1737763/1737831/1754367) + stray, `git pull`, run `test_watchdog_kill.py` +
  `test_ar1_te.py`, relaunch te_pipeline on the openloop .outb with
  `--slow-drift-targets` extended to all 9 channels + `PYTHONUNBUFFERED=1`, then
  `compute_fault_te.py --eval-only` for the verdict (caveat: non-platform fault rows
  will be tau=5 vs healthy tau=1; verdict channels Ptfm* remain tau=5-matched).

- **Prev (2026-07-14): Round-2 ARS panel review → Major Revision; all 10 required
  items applied locally.** Panel report: `reports/te-firewall-review-round2.md`.
  Round 2 found the **final.md had regressed on the v0.6 delay corrections** (Table 5
  surge said 4.3 s; parquet argmax reproduces 6.3 s ≈ Tp/2 antiphase; abstract said
  "0.3–4.3 s"; "three orders of magnitude"; no Fig 7) while the **draft.md** still had
  the pre-gating §3.4 prose — the two copies had diverged in *both* directions.
  Fixes applied to draft+final (now byte-identical in body; docx regenerated &
  verified): v0.6 delay block ported into final (abstract, §3.8 half-period rule,
  §4.5+Table 5 antiphase reading, Fig 7, Fig 6 caption, two orders); sea states
  corrected — `run_campaign.py DLC_WAVES` varies (Hs,Tp) with wind speed (3.5 m/9 s …
  8 m/13 s; DLC1.6 8.3/12.95), so §3.1/§3.2 "Tp≈12.95 s / 0.077 Hz" was wrong for
  48/54 runs → now the full (Hs,Tp) list + 0.077–0.111 Hz; Intro "DLC 1.6 at four
  wind speeds" scope sentence fixed; §4.5 seeds identified as the DLC 1.6 set;
  coherence floor added to §3.5 (K=6 Welch averages, γ²₉₅ ≈ 0.45); **SURD units
  fixed** — `rus`/`drop` values are normalised (max-MI / leak fractions), NOT nats
  (§3.6 convention + §4.3 ×2 + Fig 4c + §5.3); open-loop twin stated as n=1;
  rotor-effective-vs-point-wind limitation added (§5.3, the DA's strongest
  counter-argument); §5.2 window–latency trade-off; abstract "if anything, total" →
  "within the resolution of the significance test". Draft header bumped v0.7.
  **Part 2 (same day): S2–S4 closed + draft archived + committed.** S2: verified
  the MoorDyn layout (line 1 = single up-wave line, fairlead (−58,0)→anchor
  (−837.6,0); lines 2/3 the symmetric down-wave pair) → §4.1 geometry observation
  added, mechanism explicitly NOT asserted (wave-sig by wind speed shows no trend:
  58/44/83/33%). S4: §3.1 now states dlca=paired wave seed, dlcb=decoupled
  (XOR bit-mask, per `run_campaign.py`). S3: §5.2 control-performance-monitoring
  bridge + operator action. **Draft is ARCHIVED/frozen — `te-firewall-paper-final.md`
  is the single source of truth from now on** (S2–S4 applied to final only).
  Docx regenerated & verified. **Deferred (server, unchanged):** fault-case TE,
  open-loop TE legs + seeds, rotor-averaged-wind TE, tau=1 control, te_table_full
  re-verification before Stage 5.

- **Prev (2026-07-13, part 4): applied the immediately-doable peer-review fixes.**
  Ran the ARS 5-reviewer panel (→ Major Revision; report at
  `reports/te-firewall-review-panel.docx`) and applied every roadmap item not needing
  the server/new sims (draft+final, docx regenerated & verified): §3.1 now states the
  verified ROSCO config (2.10.1, `Fl_Mode=2` floating feedback, `SS_Mode=1`) and hydro
  config (`PotMod=1`, `DiffQTF=12` full 2nd-order QTF) — answering the domain reviewer;
  §4.1 adds bootstrap 95% CIs (Wind→pitch [0.0000,0.0024], Wave→pitch [0.1051,0.1384]);
  §5.3 reconciles the k-sweep contradiction with §3.3; §4.3 flags that both attribution
  lines are SURD-based (not independent); §5.2 hedges the nacelle-anemometer claim;
  Figure 2 regenerated to the true dlca+dlcb+dlc16 matrix (12/18/12/12=54). **Deferred
  (need server/decision):** roadmap 1 (fault-case TE or retitle), roadmap 6 (more
  open-loop seeds), 20 m/s wind PSD. Config verified on local dlc16; dlca/dlcb inputs
  server-side. **Uncommitted.**

- **Prev (2026-07-13, part 3): fixed the negative TE in Table 2.** User caught
  Wind→PtfmHeave = −0.0005 nats (impossible; TE≥0). Cause: table means used raw
  **signed** KSG estimates (4/54 PtfmHeave cases negative, all non-significant),
  contradicting §3.4's "non-sig → 0 exactly." Fix (gating, user's choice): recomputed
  all table means with non-sig→0; changed cells — Wave→PtfmSurge 0.1068→0.1069 (T1+T2),
  Wind→PtfmHeave −0.0005→0.0001, Wind→RootMxc1 0.0018→0.0019, T3 15 m/s 0.0014→0.0018;
  §4.2 prose "≤0.0016"→"≤0.0018"; added a §3.4 clause documenting the gated-mean
  convention. Docx regenerated & verified (no negative TE remains). Gotcha logged:
  `te_table.parquet` te_nats is signed — gate on `significant` + filter
  `method=='bivariate_te_ksg'`. **Uncommitted.**

- **Prev (2026-07-13, part 2): ARS-gate manuscript hardening.** Audited the paper
  against the ARS pipeline quality gates (from ARCHITECTURE.md) and applied four
  fixes to draft+final (docx regenerated, verified): (1) **§3.1 + Fig 2** — the
  campaign is NOT "DLC 1.6, 4×6=54"; per `sims/run_campaign.py` it's `dlca`(NTM,
  4w×6s, paired wave) + `dlcb`(same, decoupled wave)=48 **plus** `dlc16`(DLC 1.6
  SSS, 11 m/s×6s)=6 = 54, so DLC 1.6 is only 6/54 — corrected the arithmetic and
  the overreach. (2) **§4.1** — labeled blade/tower wind edges as an estimator
  positive control (defends the platform null). (3) **Data Availability** — repro
  block (IDTxl 1.6.1, KSG k=4, 200 perms, α=0.05, ROSCO+6 seeds). **Corrected my
  own prior false alarm**: `te_table.parquet` does NOT contradict the firewall — I
  had aggregated its `coherence_scipy` γ² rows as TE; KSG rows show wind→PtfmPitch
  TE=0.000/ns (filter `method=='bivariate_te_ksg'`). **#1 open item unchanged:**
  monitoring claim has 1 fault row with NaN TE (`compute_fault_te.py`, server).
  Follow-up: `fig2-dlc-matrix.png` now mismatches its caption — regenerate.
  **Uncommitted.**

- **Prev (2026-07-13, part 1): §2.3 TE derivation reworked to follow Chen et al. (2019)
  + docx resynced.** Expanded the single Schreiber TE equation in §2.3 (draft+final)
  into Chen's core lineage — Shannon entropy → mutual information (with the
  H(X)+H(Y)−H(X,Y) identity) → entropy rate → transfer entropy + the
  entropy-rate-difference form `T_{Y→X}=h_X−h_{X|Y}`. Kept in the paper's own
  conventions (estimator-agnostic, nats via KSG per §3.3), *not* Chen's
  bits/kernel-density/fixed-order form, which would contradict §3.3 — user chose
  this. Discovered `te-firewall-paper.docx` is a git-ignored pandoc export of
  `…-final.md` and was 3 commits stale; regenerated it from the md (backup:
  `te-firewall-paper.docx.bak-<ts>`), which also ported the missing Jul 9–10
  content. Verified: validates, 8 figures intact, 182 OMML objects (was 94),
  round-trip confirms all new equations. `…-paper.tex` left stale (offer to
  regen). **Uncommitted** (docx is git-ignored; md/log/SYNTHESIS edits pending).

- **Prev (2026-07-10, part 4): cited Chen et al. 2019 (IEEE APAP) on the four
  TE parameters.** Added a §3.3 paragraph (draft+final) mapping the paper's four
  tunables to ours — sampling 5 Hz, window = full record, and the source/target
  Markov orders selected data-drivenly by IDTxl greedy embedding (not hand-set;
  bounds target ≤150 samp/30 s, source ≤30 samp/6 s). Citation from Crossref
  (DOI 10.1109/APAP47170.2019.9224680). Guard: Chen's Markov k/l ≠ KSG k=4.
  **Uncommitted** (on top of committed `d051eb6`).

- **Latest (2026-07-10, part 3): KSG estimator justified + k-robustness shown.**
  User asked (quoting an IEEE paper) whether to "consider the variables' PDF."
  Answer: the paper already uses the kNN/KSG family (distribution-free), the
  right call vs kernel-density. Ran k ∈ {3,4,6,8} sweep → coupling delay
  (2.7–2.9 s) and firewall (wind ≤0.03 nats, wave/wind 39–48×) k-invariant;
  only absolute nats scale with k (expected). Added a §3.3 estimator-
  justification paragraph + 3 refs (Frenzel & Pompe 2007, Khan 2007,
  Kozachenko & Leonenko 1987) to draft+final. Evidence:
  `reports/ksg-k-sensitivity.md`. **Uncommitted.**
- **Also 2026-07-10 (part 2): fixed Fig 6 panel (a) time axis.** It read
  100–200 s but plotted the post-600 s-transient record; now reads real sim
  time 700–800 s. Cosmetic only (TE recompute matched paper exactly).
  `analysis/delay_analysis.py` + regenerated `reports/figs/fig6-delay-analysis.png`
  + `reports/delay_profiles.parquet`. **Uncommitted.**

- **Latest (2026-07-10): wind–wave independence check done.** Answered a user
  methodology question — does wind↔wave correlation force conditional TE?
  Measured directly (`analysis/wind_wave_indep.py`) on all 8 locally-reachable
  FOWT runs (6× 11 m/s + 8 m/s + open-loop twin): **every run independent**
  (|r| ≤ 0.035, MI == bias floor, circular-shift surrogate min p = 0.17). So conditional TE ≡ bivariate TE; the paper's
  `BivariateTE` choice is justified. Writeup: `reports/wind-wave-independence.md`;
  closes open-question **Q6**. §3.3 robustness paragraph inserted (draft+final);
  Q6 marked 🔵. **Server script written + verified** to finish the 15/20 m/s
  bins: `analysis/run_wind_wave_indep.sh` → `analysis/wind_wave_indep_all.py`
  → `reports/wind_wave_independence.parquet` (CPU-only, runs in `fowt-te`,
  8/8 local runs INDEP). Remaining server follow-ups: run that script for
  all-54 coverage; optional `probe_conditional.py` belt-and-suspenders; carry
  the "H3 contrast not executed" note into `hypothesis-scorecard.md`.
  **All edits uncommitted.**

---

## §0 (prev, 2026-07-09)

- **Phase 4 full TE campaign is RUNNING on lams** (both A100s, single-process
  GPU launcher `0e550e0`), relaunched 2026-07-06 after the CPU-shard run
  wedged. **User-reported ETA: ~11 days** (→ ~2026-07-17). Output:
  `reports/te_table_full.parquet` (supersedes stale first-pass
  `te_table.parquet`).
- **Paper**: `reports/te-firewall-paper-draft.md` at **v0.6** — v0.5 (commit
  `4186414`, via full ARS pipeline) plus the Fig-7/surge-antiphase revision
  and the 2026-07-09 verification fixes (all numbers re-checked from parquet;
  abstract delay range, "two orders of magnitude", §3.4 negative-TE
  bookkeeping, §3.8 alias wording). Thesis: wind→platform TE≈0 is a
  blade-pitch-control *firewall*; TE rising = pitch fault → health monitoring.
  Open-loop drop is **−57%** (0.0612→0.0265), not the −59% in older notes.
- **SURD subproject COMPLETE through Phase 2**: 55-case `surd_table.parquet`;
  2.8× firewall dose-response at/above-rated; open-loop twin −59%; 94% of
  TE-null cases show the mediated path.
- **Uncommitted in tree**: conference-deck builds (`reports/_build_te_*.js/py`,
  `_conf2/`…`_conf9/`), new figures (Sobol, TE network, delay profiles,
  pipeline), paper-draft edits newer than v0.5, `analysis/delay_analysis.py`
  edits.
- **This 11-day window**: vault work. First deliverable (this session):
  SYNTHESIS.md + CLAUDE.md maintenance rules. `pages/log.md` was backfilled
  and committed (`8fe9488`).
- **When lams finishes**: pull `te_table_full.parquet`, re-score H1/H3/H5b/H6,
  then controller-off Q11 run if the H1 null survives; finalize report ver08.

---

## Session 2026-05-12/13 — Vault bootstrap *(reconstructed from pages/log.md)*

### Dialogue
- **User asked** to set up the project structure per the plan → **Claude**
  created `repos/`, `sims/`, `data/`, `analysis/`, `reports/`, cloned 7
  OpenFAST-ecosystem repos, seeded 17 notes.
- **User** renamed `wiki/` → `wiki-transfer entropy/`, pointed Obsidian at it,
  moved `PLAN.md` + `LLM_Wiki_Pattern.md` into the vault root → **Claude**
  fixed 9 relative-path references broken by the move.
- **User** dropped the full IEA-22-280-RWT repo into `raw/extracts/` →
  **Claude asked** whether to switch reference platform → **Decision: keep
  IEA-15 VolturnUS-S** (Option 3) for publication comparability (OC6
  validation data).
### Decisions
- Three-layer wiki split (`raw/` / `pages/` / `SCHEMA.md`) per LLM_Wiki_Pattern;
  type-foldered (concepts/entities/equations), not theme-foldered.
- Publication strategy section added to PLAN (venues, baselines, H1–H6).
### Files changed
- Vault scaffolding, `pages/log.md`, `SCHEMA.md`, `PLAN.md` (see log.md
  2026-05-12/13 entries).
### Open items then
- Q1/Q2 in [[pages/open-questions|open-questions]] (channel lock, sweep list).

## Session 2026-06-01 — New server + IDTxl silent-exit bug *(reconstructed from log.md)*

### Dialogue
- **User** deployed the pipeline on the new box `isaactest@oem-MD72-HB3-00`
  (env `fowt-te`); empty TE tables with EXIT=0 → **Claude** bisected to
  `idtxl/estimators_opencl.py:16` — a bare `sys.exit()` in an `ImportError`
  handler killing the process silently. Patched to `pass`.
### Decisions
- **Rule: validate the JIDT path with `test_ar1_te.py` (a real estimate) before
  launching any campaign** — now required in SERVER_DEPLOYMENT §3d.
- Full-settings Phase 4 rerun planned (`run_phase4_full.sh`: conditional +
  Granger + AIS + coherence ON, max_lag=150, 5 Hz, n_perm=200).
### Files changed
- `analysis/run_phase4_full.sh` (`e36bf36`), deploy-gap docs (`f80da28`),
  skip-trap fix (`ca99535`, 06-02).

## Session 2026-06-04/06 — GPU estimator + tau tooling *(reconstructed from git)*

### Decisions
- TE pipeline gets an OpenCL/GPU KSG estimator + process pool with multi-GPU
  round-robin; `--tau` subsampling flag; numpy-2.x scalar-return patch scoped
  to `_calculate_single_link`.
- Tau chosen data-driven: `pick_tau.py` + `compare_tau.py` validation.
### Files changed
- `da8d18a`, `8b06678`, `6e9f052`, `7e5cd45`, `d1481ff` (06-04);
  `993ea4f`, `57359aa`, `d1fa08a` (06-06).

## Session 2026-06-09/10 — Conference abstract + wind–wave diagnostics *(reconstructed from git)*

### Decisions
- Bilingual (EN/KO) conference abstract; talk outline uses **real numbers and
  the honest firewall framing**; novelty statement kept sweep-contingent
  (strong + fallback).
### Files changed
- `e5c6171`, `93c4b19`, `45cd119`, `a22a692` (`wind_wave_indep.py`),
  `7884b38`/`48f8741` (`load_band_attribution.py`, `--notch-1p`),
  `a83d1bb` (compare_tau merge-key fix).

## Session 2026-06-12 — Campaign hardening *(reconstructed from git)*

### Decisions
- Slow-drift channels (PtfmPitch/PtfmHeave) hang/NaN at tau=1 → **per-target
  tau=5**; per-job watchdog; workers pinned to 4 (proven reliable);
  stem-based `case_id`.
### Files changed
- `9ff4ffe`, `dde7991`, `142ed04`, `06459d4`, `d3acede`, `b797444` (06-11).

## Session 2026-06-17 — Conference deck *(reconstructed from git)*

### Files changed
- `1776f52` (figures reconciled to full-campaign TE data), `cc07e39`
  (LAMS/KSNU lab format, 32 slides), `bcc3312` (body text Korean → English).

## Session 2026-06-29 — KSG max_lag bug *(reconstructed from SESSION-LOG-2026-06-29.md — read that file for full detail)*

### Dialogue
- **User** reported the 1-case full-settings probe finished (9.1 h) →
  **Claude** found `TE(Wave→PtfmHeave)=0` while Granger saw 0.35 — a
  result-invalidating null. Diagnostic sweep: TE=0.066 at max_lag=30,
  collapses to 0 at max_lag≥60 → **greedy-selection artifact**, not physics.
### Decisions
- **Decouple `max_lag_sources` (short, sensitive) from target embedding
  `max_lag` (long, slow drift)** — `986f867`.
- Re-validate on lams before launching the 54-case campaign.
### Files changed
- `c43d59b`, `398025e`, `986f867`; session record `SESSION-LOG-2026-06-29.md`.
### Open items then
- Re-validation run → pick `max_lag_sources` → wire into launcher → launch.

## Session 2026-07-03 — Re-validation + CPU launch *(reconstructed from git + memory)*

### Decisions
- Re-validation passed (Wave→Heave TE≈0.067, p=0.005, on OpenCLKraskovCMI) →
  **`--max-lag-sources 20`** wired into `run_phase4_full.sh` (`e8d3622`).
- Repo hygiene: ignore root scratch binaries; track SURD plan/session
  log/scorecard (`18ed2bf`).
- 36-worker CPU-shard campaign launched — **this later wedged** (see next).

## Session 2026-07-06 — SURD Phases 0–2 + GPU relaunch *(reconstructed from git + memory)*

### Dialogue
- **User/Claude** diagnosed the wedged CPU run: JIDT JVM signal handlers
  swallowed the watchdog SIGTERM → 36 alive-but-dead parents, zero output.
  Also: re-validation ran on OpenCL but shards ran JIDT — estimator
  inconsistency. → **Decision: campaign must run GPU, single process.**
### Decisions
- Launcher rewritten (`0e550e0`): ONE process, `--gpu --gpus 0,1 --workers 4`,
  checkpointing per case into `reports/te_table_full.parquet`; **no shards, no
  merge step**. Relaunched on lams, both A100s ~99%.
- SURD Phase 0 gate PASSED → Phase 1 thin slice failed its bias control →
  refined with pitch-rate state, GATE OPEN → Phase 2 55-case campaign +
  analysis. Headline: 2.8× dose-response, open-loop −59%, 94% mediated-path.
- Hygiene: `te_frac` = TE/AIS everywhere; coherence flag is a threshold, not a
  statistical test (`5a80adf`).
### Files changed
- `2ba1706`, `0f9d106`, `2cd46de`, `200acc2`, `de98548`, `126aa5f`,
  `5a80adf`, `65486fb`, `0e550e0`.

## Session 2026-07-08 — Paper v0.5 *(reconstructed from git)*

### Decisions
- `reports/te-firewall-paper-draft.md` taken through the full ARS pipeline
  (write → review → revise → finalize) to **v0.5** (`4186414`), after Phase 1
  fault-detection signature-table scaffolding (`65486fb`).

## Session 2026-07-09 — Log backfill + SYNTHESIS.md created *(logged live)*

### Dialogue
- **User asked:** "what were we doing lastly?" → **Claude answered:** recap
  from git + memory — paper v0.5 was the last commit, SURD complete through
  Phase 2, Phase 4 GPU campaign in flight on lams, conference-deck work
  uncommitted in the tree.
- **User asked:** "what was the last task based on the log?" → **Claude
  answered:** last commit `4186414` (paper v0.5 via ARS pipeline), noting
  newer uncommitted work exists.
- **User asked:** "based on the wiki log in this directory" → **Claude
  answered:** `pages/log.md`'s last entry was 2026-06-01 (new-server
  bootstrap + IDTxl sys.exit bug) — the wiki log was 5 weeks stale;
  `SESSION-LOG-2026-06-29.md` and git held the newer record.
- **User asked:** "everyday we have done many tasks why didn't you update the
  log?" → **Claude answered:** honest process gap — nothing enforced wiki-log
  upkeep; sessions recorded work only in git commits. Fixed by (a) saving a
  standing memory rule to append to `pages/log.md` every session, (b)
  backfilling log.md with 9 entries covering 2026-06-04 → 2026-07-09.
- **User said:** "commit the log update" → **Claude** committed `8fe9488`
  (pages/log.md only).
- **User said:** "lams running takes 11 days. we need to make some changes to
  the vault" → **Claude asked** (multiple choice): content catch-up /
  structural changes / hygiene pass / something else? → **User answered:**
  "since you always forgetting what we did last day, please make a
  sythesis.md and every conversation between us, any plannings, your
  questions and my answers, my questions and your answers, your decisions,
  every update to the files should be logged in the sythesis.md"
- **Claude asked:** start from today, or backfill reconstructed history
  first? → **User answered:** **Backfill + ongoing.**
- **Claude presented a plan** (SYNTHESIS.md at vault root with §0 current-state
  block + per-session entries; new CLAUDE.md carrying the maintenance rule;
  memory updates; one commit) → **User approved** the plan.
- **User said:** "I need to do some update to the claude.md as well" →
  **Claude asked** what updates → **User answered:** make it structured and
  add role/mission sentences: planning agent + coding agent (not a chatbot);
  mission = turn vague goals into sequenced execution plans a coding agent
  can safely follow; senior planning agent with Ocean Engineering / offshore
  wind / OpenFAST / information-theory expertise; plans carry milestones,
  file-level work areas, verification steps, rollback notes, concise todos,
  implementation-ready; push back on unclear scope / hidden coupling / risky
  rewrites / missing acceptance criteria / unsplit work; during
  implementation mark completed items with evidence, not optimism.
- **User added (second batch):** before-edit workflow (inspect files, infer
  patterns, list assumptions, short plans, todos); during-implementation
  rules (scoped changes, preserve user work, prefer existing helpers, add
  tests/checks against regressions); an **output contract** (objective,
  assumptions, phased plan, touched areas, risk register, verification
  commands, open questions); clarifying questions only when missing info
  blocks safe implementation; **never guess — ask**. → **Claude** cleaned
  typos and restructured CLAUDE.md into 8 sections (Role / Mission / Planning
  standards / Execution workflow / Output contract / Session record /
  Project pointers / Working agreements).
### Decisions
- File named `SYNTHESIS.md` (spelling corrected from "sythesis.md"), vault
  root, append-only newest-at-bottom, §0 rewritten each session.
- `CLAUDE.md` created at vault root so the rule loads in **every** future
  session (memory recall alone was the failure mode).
- Division of labor: `pages/log.md` = task-level wiki record;
  `SYNTHESIS.md` = conversation/decision record. Both maintained every session.
- Phase 4 memory updated with the **~11-day lams ETA** (~2026-07-17).
### Files changed
- `pages/log.md` — backfilled 2026-06-04→07-09, committed **`8fe9488`**.
- `SYNTHESIS.md` (this file) — created.
- `CLAUDE.md` — created (maintenance rules). Committed together with this
  file as **`5b886b8`** (hash recorded in a small follow-up commit,
  `117a499`); today's log.md entry committed as `30861f7`.
- `CLAUDE.md` — restructured later the same session into the 8-section
  planning-agent charter (user-dictated role/mission/workflow/output-contract
  rules); committed together with this SYNTHESIS.md update and a log.md
  entry (hash: see git log, "CLAUDE.md: planning-agent charter").
- Memory (outside repo): `feedback_update_wiki_log.md` (new),
  `feedback_synthesis_log.md` (new), `project_phase4_full_campaign.md`
  (11-day ETA added), `MEMORY.md` (index lines).
### Dialogue (continued — manuscript double-check)
- **User asked:** "you must remember that yesterday you prepared a manuscript
  — do you want to double check the output?" → **Claude** re-verified every
  headline number in `te-firewall-paper-draft.md` against the parquet tables
  (te_table, surd_table, monitor_signature, delay_profiles). **All Tables 1–5
  values, edge counts, te_frac, coherence, SURD 0.402, open-loop
  0.167→0.000 and 0.0612→0.0265 (−57%), surge peaks reproduced exactly.**
  Four issues found: (1) abstract still said delays "0.3–4.3 s" — stale after
  the uncommitted Fig-7/surge revision changed surge to 6.3 s; (2) §4.1 said
  "three orders of magnitude" where 0.04% vs 4.3% is two; (3) §3.4 claimed
  non-significant channels return exactly 0, but 7 wind→heave rows retain
  non-zero (4 negative) estimates → Table 2's −0.0005 heave mean; (4) §3.8
  overclaimed that the half-period cap "avoids the aliases" when surge's
  selected delay sits at ≈Tp/2. → **User said** "yes" to fixing all four.
- **Claude applied** the four fixes, bumped the draft header to **v0.6**, and
  corrected its own memory (−59% → −57% for the open-loop drop; the paper
  had it right).
### Decisions (continued)
- Verification convention confirmed: paper numbers are checked against the
  first-pass `te_table.parquet`; **must be re-verified against
  `te_table_full.parquet` when the lams campaign lands, before Stage 5**.
### Open items / next steps
- Rest of the 11-day window: user to specify next vault changes (content
  catch-up for SURD/paper pages, structural changes, hygiene pass were the
  offered options — "something else" chosen was this file; the others remain
  candidates).
- **Paper**: re-verify all numbers against `te_table_full.parquet` when the
  lams run finishes; then Stage 5 (LaTeX/PDF). Fault-TE computation
  (`analysis/compute_fault_te.py`) still queued.

### Dialogue (continued — CLAUDE.md user rewrite)
- **User said** they edited CLAUDE.md themselves → **Claude** found no change
  on disk (file identical to `d0d5b05`, no other CLAUDE.md anywhere) →
  unsaved editor buffer → **User saved**, revealing a full rewrite: the
  8-section charter expanded to a **13-section operating manual** (Role /
  Core Principles / Working Modes / Planning Standard / Push Back /
  Implementation Rules / Verification Standard / Research Standards /
  Session Records / Project References / Output Contract /
  Project-Specific Agreements / Engineering Philosophy).
- **Claude reviewed** and flagged 4 issues: (1) the dictated Mission sentence
  was dropped; (2) §11 Output Contract's 10 sections applied to *every*
  response would bury short answers in boilerplate; (3) §3 Planning Mode's
  "do not modify files" contradicted §9's mandatory session records;
  (4) §1 heading level inconsistent + missing trailing newline.
  → **User asked** which to apply → **Claude recommended all four** →
  **User approved** ("ok good").
### Decisions (continued)
- CLAUDE.md is now the user's 13-section operating manual with: Mission
  restored into §1; Output Contract scoped (full contract for
  planning/implementation deliverables, applicable sections otherwise,
  Verification + Confidence always when work was performed); Planning Mode
  exempts the §9 session records; headings normalized.
- Uncommitted conference-deck work still needs sorting/committing.
- When lams finishes: pull `te_table_full.parquet`, re-score hypotheses,
  finalize report ver08.

---

## Session 2026-07-10 — Wind–wave independence / conditional-TE question

### Dialogue
- **User**: "In the manuscript, shall we consider calculation of the correlation
  between wind and wave? Because if they have correlation the calculation of the
  TE must be conditional, isn't it?"
- **Claude**: Confirmed the instinct is methodologically sound but qualified it.
  Bivariate TE (used in the paper's headline table, §3.3) conditions only on the
  target's past; correlated sources can confound it. But the threat is
  asymmetric: (a) the firewall wind→platform≈0 can only be broken by *synergy*,
  which SURD's synergistic atom already tests and does not find; (b) the
  wave-dominance side is the one exposed to *redundancy* inflation. Flagged that
  linear correlation is the wrong screen (TE is nonlinear → use MI) and that the
  relevant quantity is the *within-run* wind/wave dependence (independent
  TurbSim+JONSWAP seeds), not the across-DLC metocean correlation.
- **User**: "yes go ahead" (compute it).
- **Claude**: Found existing tooling (`analysis/wind_wave_indep.py`,
  `probe_conditional.py`). Ran the independence check on the 7 local runs.

### Work done
- Ran `wind_wave_indep.py` on 6× `dlc16_v11ms_s0*` + `dlca_v08ms_s00.outb`.
  All independent: |Pearson r| ≤ 0.035, max |cross-corr| ≤ 0.043 (±30 s),
  MI 0.033–0.043 nats.
- Caught a null-model subtlety: i.i.d.-shuffle null gave spurious z ≈ 5–12
  (destroys autocorrelation → inflates effective N → understates bias floor).
  Redid with **circular-shift surrogate** (autocorrelation-preserving) → MI
  indistinguishable from null (z ∈ [−1.79,+0.90], no p<0.05, mean excess
  −0.001 nats). True wind↔wave MI ≈ 0.
- IDTxl not installed locally (lazy import; server env `fowt-te`), so the
  conditional-TE confirmation could not run here.

### Decisions
- Wind and wave forcing are statistically independent within a run → conditional
  TE ≡ bivariate TE for these sources → paper's bivariate choice justified.
  Confounding worry retired for the wind/wave→structure edges.
- Report this as a §3.3 robustness paragraph rather than re-running the campaign;
  SURD already covers the synergy failure mode.

### Files changed (uncommitted)
- `reports/wind-wave-independence.md` (new) — full method, 7-run table, conclusion.
- `pages/log.md` — [2026-07-10] research entry; frontmatter updated → 2026-07-10.
- `SYNTHESIS.md` — this entry + §0 rewrite.
- `pages/open-questions.md` — **not yet edited**; Q6 should be flipped 🟢→🔵
  with a pointer to the results note (pending user go-ahead).

### Open items / next steps
1. Server (`fowt-te`): `wind_wave_indep.py` on 15/20 m/s bins → all-54 coverage.
2. Server: `probe_conditional.py` → numeric `TE(Wave→PtfmPitch|Wind)` ≈ bivariate.
3. Insert the §3.3 robustness paragraph into `te-firewall-paper-final.md`; note
   H3 (DLC-A/DLC-B contrast) was pre-registered but not executed.
4. Mark Q6 resolved in `open-questions.md`.

## Session 2026-07-14 — Round-2 panel review + revision *(logged live)*

### Dialogue
- **User asked:** "lets go for the review commend and revise the manuscript" →
  ran `/ars-reviewer` (full 5-reviewer panel, round 2) on
  `reports/te-firewall-paper-final.md`, then applied the revision (user's request
  covered both steps, so Phase 2.5 coaching was skipped).
- **Claude verified panel claims against the repo first** (not the manuscript):
  `delay_profiles.parquet` argmax, `run_campaign.py DLC_WAVES`,
  `te_pipeline.py coherence_nperseg`, `surd/phase2_campaign.py` normalisation,
  `analysis/delay_analysis.py` selection rule.

### Findings (the round-2 review's own catches)
1. **final.md regressed on the 2026-07-09 v0.6 delay fixes** (stale Table 5
   surge 4.3 s — irreproducible from parquet, which gives 6.4/6.2/6.2 s →
   6.3 s ≈ Tp/2 antiphase; stale abstract "0.3–4.3 s"; "three orders"; missing
   Fig 7 / §3.8 half-period rule). draft.md conversely retained the pre-gating
   §3.4 prose that final had already fixed. Two-way desync.
2. **§3.1 sea-state description wrong for 48/54 runs**: campaign uses
   wind-speed-matched (Hs,Tp) per `DLC_WAVES`, not "Tp ≈ 12.95 s".
3. **SURD numbers were mislabelled as nats** — they are normalised fractions
   (`rus` by max MI, `drop` = leak differences).
4. Coherence baseline had no zero-coherence significance floor (K = 6 averages
   → γ²₉₅ ≈ 0.45; all Table 4 peaks clear it).
5. §4.5's "three healthy 11 m/s seeds" are the DLC 1.6 severe-sea seeds.
6. Open-loop twin is n = 1 (now stated); DA's strongest counter-argument
   (rotor-effective vs point wind) added as an explicit §5.3 limitation.

### Decisions
- Panel decision: **Major Revision** (DA CRITICAL on the data/manuscript
  mismatch). All 10 required items were local-actionable and were applied to
  **both** draft and final in the same session; bodies are now byte-identical
  (only header/frontmatter differ). Draft bumped to v0.7; final date 2026-07-14.
- Rotor-effective-wind challenge resolved per R1's position: limitation text
  now, recomputation queued with the server campaign.
- FAIRTEN1 mooring-orientation explanation NOT applied (needs MoorDyn layout
  verification first) — carried as an open reviewer question (S2).

### Files changed (all uncommitted)
- `reports/te-firewall-review-round2.md` (new — full panel report + roadmap)
- `reports/te-firewall-paper-final.md` (15 edits per roadmap RR1–RR9 + Fig 6 caption)
- `reports/te-firewall-paper-draft.md` (18 edits: shared fixes + §3.4 sync + v0.7 header)
- `reports/te-firewall-paper.docx` (regenerated via pandoc; content-verified by
  python-docx assertions; backup `te-firewall-paper.docx.bak-20260714-*`)
- `SYNTHESIS.md` (§0 rewrite + this entry), `pages/log.md` (entry appended)

### Verification
- Stale-pattern grep over both md files: 0 hits for `0.3–4.3 / three orders /
  nats summed / if anything, total / peak period near 12.95 / marginally negative`.
- Body diff draft↔final after edits: 0 differing lines.
- docx assertions: Table 5 has `6.3 (≈ Tp/2…)`; all 12 new-content markers present.
- Table 5 values re-derived from `delay_profiles.parquet` (0.3/2.7/3.9/6.3 s ✓).

### Open items / next steps
- Commit the 2026-07-13 + 2026-07-14 manuscript work (user's call).
- Server queue unchanged: fault-case TE, open-loop TE legs + seed replication,
  rotor-averaged-wind robustness, tau=1 control, te_table_full re-verification.
- S2 (FAIRTEN1 orientation) and R2-Q1 (dlca/dlcb seed pairing) still open.
- Re-review (Stage 3′) after the server items land, before Stage 5.

### Part 2 (same session) — recommendation executed
- **User asked** "did you address all the comments?" → honest status: RR1–RR9 done,
  RR10 partial (full numeric re-verification gated on te_table_full), S2–S4 open.
  Then "what is your recommendation?" → close S2–S4 locally, commit, freeze the
  draft, no more paper edits until server items land. **User said go.**
- S2 verified before writing: MoorDyn points — line 1 fairlead (−58, 0, −14) →
  anchor (−837.6, 0, −200), i.e. the single up-wave in-plane line; lines 2/3
  symmetric at ±50.229 m / anchors (418.8, ±725.383). Wave→FAIRTEN1 significance
  by wind speed = 58/44/83/33% (no thrust trend) → mechanism NOT asserted in text.
- S4 verified: `run_campaign.py` — dlca/dlc16 wave_seed = wind_seed (paired);
  dlcb wave_seed = wind_seed XOR 0x5A5A5A5A (decoupled).
- Applied S2 (§4.1), S4 (§3.1), S3 (§5.2) to **final.md only**; draft.md frozen
  with an ARCHIVED banner naming final as single source of truth (two-copy sync
  policy retired). Docx regenerated + python-docx-verified (5 new-content markers).
- Commit hashes recorded in pages/log.md entry for this date.

### Part 3 (same session) — fault-case TE launched on the CPU server
- User chose to run the queued fault-TE job on the CPU box (isaactest@oem-MD72-HB3-00),
  driving the commands themselves (no key auth from this Windows box; probing LAN
  hosts with guessed usernames was rejected — don't do that again).
- Server repo was 1 local commit ahead / 18 behind → `git rebase origin/phase4-full-rerun`
  cleanly dropped the local commit (patch already upstream); server now at e020ac0.
- `analysis/test_ar1_te.py` (note: lives in analysis/, not repo root) **PASSED**:
  TE(X→Y)=0.1892 nats p=0.005 sig; TE(Y→X)=0.0000 p=1.0 non-sig.
- Launched: `nohup python analysis/compute_fault_te.py --outb
  sims/dlca_v11ms_s00_openloop/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb`
  → PID 1737763, log `logs/fault_te.log`, output `reports/te_fault_openloop.parquet`.
  CPU/JVM backend (no --gpu) — does not touch the lams A100 campaign.
- **Pending:** the verdict block (fault Wind→PtfmPitch/Surge/Heave vs healthy
  ceiling 0.029 nats + chance floor). Breach ⇒ §4.4 gets its first empirical
  test point AND the §4.3 attribution converse closes; no breach ⇒ reshape the
  graded-fault campaign. Either way: fold into the manuscript at the te_table_full
  re-verification pass, not before.

---

## Session 2026-07-16 — fault-TE wedge diagnosed, watchdog kill-escalation fix

**Dialogue.** User pasted `tail -f logs/fault_te.log` from the CPU server
(isaactest@oem-MD72-HB3-00): `java.lang.InterruptedException` traceback +
`TIMEOUT 9000s: ais None->RootMyc1` + a 150-candidate dump. Claude's first
read: one event seen three ways (watchdog SIGTERM → JPype JVM interrupt →
child's buffered stdout flushing at death); RootMyc1 is tau=1 (not in the
slow-drift list) so 150 candidates can't finish on CPU; verdict legs (Wind→
Ptfm*, tau=5) unaffected — recommended letting it run and gave census
commands. User's census flipped the diagnosis: **0/63 done at 46.5 h, only
one TIMEOUT ever** → run wedged, not slow. `ps` confirmed: te_pipeline parent
(1737831) at 0% CPU blocked in the bare `p.join()`, spawn child (1754367,
job 2 = AIS RootMxc1) at 45% CPU, ~42 h past its 9000 s deadline — the JVM
swallowed the SIGTERM. Same failure mode that wedged the Phase-4 CPU shard.

**Decisions.**
- Root-cause fix in `te_pipeline.py`: `_kill_stubborn_child()` — terminate,
  `join(30)`, then SIGKILL if still alive (uncatchable). Watchdog now calls it.
- Regression test `analysis/test_watchdog_kill.py` (spawn child that ignores
  SIGTERM must be reaped within grace+10 s); to be run on the server with
  `test_ar1_te.py` before relaunch, per the standing pre-campaign rule.
- Relaunch recommendation: extend `--slow-drift-targets` to all 9 response
  channels on CPU (tau=1 heavy jobs are near-guaranteed 2.5 h timeout burns;
  ~25 of them ≈ 2.5 days dead wall clock, rows dropped anyway). Provenance
  caveat accepted for non-platform channels; verdict channels stay matched.
- Kill the stray 44-day probe (PID 546698, `/tmp/te_probe.parquet`, 37% CPU).

**Files changed.** `analysis/te_pipeline.py` (kill escalation),
`analysis/test_watchdog_kill.py` (new) — commit **24a44b1**, pushed to
origin/phase4-full-rerun. Records: pages/log.md entry, SYNTHESIS §0 rewrite.

**Verification.** `py_compile` both files; test PASSes locally (Windows =
trivial path — TerminateProcess can't be ignored; the real SIGTERM-immune
path needs the POSIX server run). Diagnosis verified against live `ps`
output, `grep` census, and code reading; not yet against a healthy relaunch.

**Open items.** (1) Server: kill wedged tree + stray, pull 24a44b1, run both
tests, relaunch (extended slow-drift list, PYTHONUNBUFFERED=1). (2) Verdict
via `compute_fault_te.py --eval-only` when the parquet lands. (3) Unchanged
deferred set: open-loop TE legs + seeds, rotor-averaged-wind TE, tau=1
control, te_table_full re-verification before Stage 5.

## Session 2026-07-29 — Both server campaigns landed: fault-TE null + te_table_full complete

**Dialogue.** User: "let go back to the project I had two codes one on cpu and
the other on gpu." Read §0 + log tail; oriented on the two runs (CPU fault-TE
PID 1992582; GPU Phase-4 full). User had server access and ran the status
one-liners; agreed to do CPU first, then GPU.

**CPU fault-TE (isaactest@oem-MD72-HB3-00, ~/다운로드/Sina/fowt-te-causal).**
PID 1992582 DEAD (job *done*, not wedged). Log tail: `case done in 257114s,
67 rows` / `[1/1] OK`. Parquet `reports/te_fault_openloop.parquet` present;
header confirms input `sims/dlca_v11ms_s00_openloop/.../IEA-15-240-RWT-UMaineSemi.outb`.
Verdict via `python analysis/compute_fault_te.py --eval-only
reports/te_fault_openloop.parquet`:
Wind→PtfmPitch/Surge/Heave = 0.0000 nats, non-sig, below 0.029 ceiling →
"No breach demonstrated." Internal control positive (significant Wave1Elev→FAIRTEN3
edge in same log) → null is real, not a broken estimator.

**GPU Phase-4 full (lams, ~/Desktop/sina/fowt_te_causal/fowt-te-causal).**
Shell surfaced `[1]+ Done  nohup ./analysis/run_phase4_full.sh > analysis/run-full-gpu.log`.
Log: `[54/54] OK`, `reports/te_table_full.parquet` = 3888 rows / 54 cases
(written Jul 21 11:38 — finished 8 days ago, notification just fired), graph
`te_full_graph.pkl` (5 nodes, 4 edges), GPUs idle. Method summary logged in §0;
key on-thesis result: **conditional_te_ksg|Wave1Elev 0/486 significant** vs
|Wind1VelX 251/486 — wave-mediation collapse.

**Decisions.** (1) Accept the fault-TE null; §4.4 stays an OUTLOOK — no paper
edit; round-1 roadmap #1/#3 closed as "test executed." (2) Reject reframing the
null as a positive structural-firewall finding (n=1 open-loop, and open-loop ≠
pitch fault — the wrong instrument for the monitoring claim). (3) Reserve, not
scheduled: ONE targeted stuck-pitch/pitch-bias fault case is the correct
instrument if we later upgrade §4.4 to proof-of-concept. (4) te_table_full is
the authoritative data for the deferred Stage-5 re-verification.

**Stage-5 firewall re-verification (done, on lams).** bivariate_te_ksg gated on
`significant`: Wind→PtfmPitch/Surge/Heave = 1/1/0 sig of 54 (chance ~2.7), max
gated 0.0047 nats ≪ 0.029 → firewall PASS, cleaner than first-pass. Positive
controls strong (Wave→PtfmPitch 52/54, Wind→RootMxc1 7/54). BUT wave→platform
magnitudes run 3–5× low and Wave→PtfmHeave sig flips 87%→13% — traced to
te_table_full's `--max-lag-sources 20` (≈4 s at 5 Hz) being shorter than the
6.3 s Wave→PtfmSurge delay → it underestimates wave TE. Paper Table 2 aggregation
confirmed apples-to-apples ("mean over 54").

**Decision (user, this session).** KEEP the paper's first-pass `te_table`
magnitudes (Tables 2/3, abstract, CIs unchanged); cite te_table_full only as a
firewall robustness check. Rejected: adopting full magnitudes (imports the
source-lag-truncation bias) and a targeted `--max-lag-sources ≥35` re-run (held in
reserve, not needed for the thesis).

**Files changed.** SYNTHESIS.md (§0 rewritten + this entry); pages/log.md (4
entries: fault-TE null, GPU complete, firewall PASS, decision); memory
`project-phase4-full-campaign` (marked COMPLETE + wave-underestimate caveat);
**`reports/te-firewall-paper-final.md`** — one robustness sentence added to §4.1
positive-control paragraph (independent GPU OpenCL–Kraskov re-estimation reproduces
the firewall; wind→surge sig 11%→0%, max wind→platform TE <0.005 nats);
**`reports/te-firewall-paper.docx`** regenerated via pandoc 3.8 and verified
(new sentence present in docx XML). No code changes; server parquets read-only.

**Open items / next.** (a) Stage 3′ re-review is now unblocked on the fault-TE +
te_table_full fronts (both closed). (b) Remaining deferred (server): open-loop TE
legs + more seeds, rotor-averaged-wind TE, tau=1 control — none blocking. (c)
Reserve: targeted stuck-pitch fault case (upgrades §4.4 to proof-of-concept) and/or
`--max-lag-sources ≥35` full re-run (equal-footing wave magnitudes). (d) Uncommitted:
the paper edit + docx + these records are on `phase4-full-rerun`, not yet committed.

## Session 2026-08-03 — §4.4/§5.3 "pending pitch-lock" currency defect closed

**Dialogue.** User (relaying a reviewer note): §4.4 says the pitch-lock fault case
"exists in the dataset but its TE is recorded as pending ... queued as a separate
task." Reviewer: if the run and pipeline both exist, why not computed? "Either
compute it (n=1, honestly caveated) or remove all traces — the current middle
position is the worst of both." Claude investigated before acting and found the
premise had already moved: the computation is DONE. `openloop.outb` is a complete
3600 s run (BldPitch1 frozen at 1.0deg); SYNTHESIS 2026-07-29 records the CPU job
(PID 1992582, ~71.4 h) returned a clean NULL (Wind->PtfmPitch/Surge/Heave TE=0.0000,
sig=False, below the 0.029-nats ceiling; same run has a significant control edge
Wave1Elev->FAIRTEN3 TE=+0.055 p=0.005). §4.3 already reports this null. The defect
was purely bookkeeping: `git show` confirmed the "fault-TE null"/"open-loop TE null"
commits touched ONLY prose (no parquet committed); §4.4 + `monitor_signature.parquet`
(row `dlca_v11ms_s00_openloop`, still NaN/"pending TE legs") were never reconciled.
This is the un-fixed half of the 2026-07-31 NEW-2 currency defect (which fixed §4.3
but scoped out §4.4). Presented findings + a 3-way choice via AskUserQuestion.

**Decisions.**
- User chose **"Reconcile & report the null"** (not remove; not upgrade to
  proof-of-concept). Rationale: computation already exists; open-loop != pitch fault
  and n=1 still stand, so no reframe.
- User: sync the durable parquet **from the server via git push/pull**.

**Files changed (local, NOT committed).**
- `reports/te-firewall-paper-final.md` — 3 surgical edits:
  §4.4 stale "pending/queued" sentence -> computed-null-but-fault-adjacent framing
  (cross-ref §4.3); §5.3 "computing TE for the existing pitch-lock case" -> "graded-
  fault runs do not yet"; §5.3 "pending open-loop TE legs would settle attribution"
  -> "since computed and null (§4.3), read cautiously". Abstract/intro/§4.6/conclusion
  untouched (their "no fault-case TE" remains true; open-loop = fault-adjacent).
- `SYNTHESIS.md` §0 rewritten + this entry.
- `pages/log.md` — entry appended.

**Verification.** Grep of the manuscript for pending / existing-pitch-lock /
queued-as-separate / legs-computed / "the runs do not yet" -> all gone; only the
(true) injected-fault future-work statements + the genuinely-uncomputed graded-fault
campaign remain. Edits applied cleanly (Edit tool confirmed each).

**Open items / next steps.**
1. Server sync: `reports/te_fault_openloop.parquet` is GITIGNORED (`reports/*.parquet`;
   only `surd_table.parquet` force-tracked) — that's why `git pull` never fetched it.
   On server: `git add -f reports/te_fault_openloop.parquet && commit && push`; then
   pull here. Branch coordination TBD (local on `phase4-full-rerun`, ahead 2).
2. After sync: update `monitor_signature.parquet` row `dlca_v11ms_s00_openloop`
   (NaN -> te_wind_pitch~0.0, sig=False) from the parquet; force-add both parquets.
3. Regenerate docx (one rebuild covering both the 3 prose edits + any final matter).
4. Commit the whole set on `phase4-full-rerun`.

---

## Session 7 — 2026-08-03 — Wiki ingest of project artifacts

**Dialogue.**
- User: "what do you understand from this vault?" → Claude read SYNTHESIS §0 +
  directory layout and summarised the project (FOWT causal-TE, the firewall finding,
  the manuscript in reviewer-response, the two-server compute setup).
- User then explained the vault's *origin*: it instantiates Karpathy's
  LLM-maintained-wiki pattern from a single bootstrap prompt (`LLM_Wiki_Pattern.md`
  + the gist). Claude read the local pattern doc + fetched the gist, connected it to
  the vault, and flagged honestly that the wiki graph had drifted (frozen ~2026-05-13)
  while SYNTHESIS/log/memory carried real progress.
- User: "can you ingest the project directory … into this vault?"

**Decisions (user-confirmed via decision prompt).**
- Target vault = **main `pages/` wiki** (the pattern's LLM-owned layer), not
  `vault-legacy/` (older Obsidian tree) — where the shell happened to be cwd'd.
- Scope = **project artifacts** (code pipeline, campaign results, paper, infra,
  internal docs); **exclude** vendored `repos/` (OpenFAST source, 7784 files),
  binary sim outputs, and build-script noise (pattern's anti-wide-shallow rule).

**Files changed.**
- New (8): `pages/entities/{te-pipeline,compute-servers,surd}.md`,
  `pages/concepts/{information-firewall,blade-pitch-health-monitoring}.md`,
  `pages/analyses/{te-firewall-54case-2026-08-03,firewall-attribution-surd-openloop-2026-08-03,firewall-manuscript-status-2026-08-03}.md`
  (first real pages in the previously-empty `analyses/` layer).
- Updated: `pages/index.md` (new entries + `updated:` → 2026-08-03),
  `pages/overview.md` (**stale currency fixed**: phase table Phases 2–6 → DONE,
  "nothing verified" → firewall finding + verification note, `updated:` bumped),
  `pages/log.md` (ingest entry), this file.

**Verification.**
- All quantitative claims sourced from the vetted manuscript
  `reports/te-firewall-paper-final.md` (§4.1–§4.6, Tables 1–5) — read this session,
  not re-derived from parquet.
- 8 new pages confirmed present on disk.
- Broken-link scan over the new pages: **0 unresolved from new content** (the 4
  unresolved targets are pre-existing `*(stub)*` links already in `index.md`).

**Open items / next.**
- Deferred lint pass (orphans/stubs across the whole wiki; the 4 pre-existing stubs).
- Reconcile `open-questions.md` + `wiki-improvement-plan.md` (both dated 2026-05-12)
  with the completed campaign.
- Uncommitted, alongside the prior session-5/6 abstract-trim + title change.

---

## Session 8 — 2026-08-09 — Introduction + literature (Tier 1+2)

**Dialogue.**
- User: "check the last task you did and let me know what that was?" → reported the last committed task
  (3e3c030, first-person → agentless-passive conversion) plus the uncommitted `reports/introduction.md`
  prep and the `project_next_intro_literature` memory pointing at the Introduction/literature work.
- User: "where is `project_next_intro_literature.md`?" → it is a memory file under
  `…/.claude/projects/…/memory/`, not in the vault; showed path + contents.
- User: "start the Introduction and literature work." → executed.

**Decisions (via decision prompt).**
- Intro approach = **reinforce in place** (keep the 5-move §1 + two-contributions framing; weave citations
  and the reframed gap statement in) rather than re-leading on the control-performance-monitoring analogy.
- Literature scope = **Tier 1 + Tier 2** (10 refs, list 20 → 30). Tier 3 held in reserve.
- Two smaller open calls defaulted to the prep doc's safe options: a differentiating **sentence** (not a
  paragraph) vs Nichols; a **one-line CCM nod** (not a full method comparison).

**Work.**
- Re-verified all 10 DOIs against Crossref/landing pages (search subagent): 10/10 resolved; correction —
  Sugihara co-author Hsieh initial C. → **C.-H.**; Kostecka/Park volume+article numbers confirmed correct;
  Namik year **2010** confirmed (Crossref 2009 = online-first). Granger end page 438 not in Crossref
  (start-page-only); range 424–438 retained.
- 10 in-text insertions across §1, §2.1, §2.3, §2.4, §5.2; §2.4 gap statement replaced with the
  earned-novelty reframe. 6 reference-list insertions (alphabetical).

**Files changed.**
- `reports/te-firewall-paper-final.md` — source of truth (edited directly).
- `reports/te-firewall-paper.docx` — regenerated from final.md by plain pandoc 3.8 (`PYTHONUTF8=1`);
  backup `te-firewall-paper.docx.bak-20260809-161333-prelit`.
- `pages/log.md` — appended entry, `updated:` → 2026-08-09.
- `SYNTHESIS.md` — this entry + §0 rewrite.
- memory `project_next_intro_literature.md` — updated to reflect completion.

**Verification.**
- Reference list = 30 entries, alphabetical; Nichols (2006, sole) precedes Nichols et al. (2005) per
  APA 7.0 §9.47; all 10 new citations resolve both ways (no orphans; correct et-al./`&` forms).
- First-person residual = 0 (3 word-boundary hits are all `10.1002/we.NNN` Wind-Energy DOIs, not prose).
- docx internals: 9 media, 6 tables, title block intact; all new citations + reframed gap sentence present
  in `document.xml`.

**Open items / next.**
- **Not committed** — all 2026-08-07 paper edits + this session's Introduction/literature pass sit
  uncommitted on top of 3e3c030 (branch `phase4-full-rerun`).
- W6 deferred: canonical Sobol/coherence foil citations (Sobol′; Bendat & Piersol) — need their own DOI
  verification before insertion.
- Tier 3 references (Thornhill 2007, Qin 1998 [field-fix to *Computers & Chemical Engineering*], Jelali
  2013, Gorostidi 2023, Moghadam 2022, Kim 2019, Wu 2018, Zhang 2023, Deng 2024, Lan 2024, Jonkman 2008)
  held in reserve for reviewer response or a longer version.
- Venue still undecided → refs remain APA-7 author–year; numbered-ref conversion available if Elsevier.
- Still queued from earlier sessions: rotor-averaged-wind robustness check (server down); reconcile
  `open-questions.md` + `wiki-improvement-plan.md` with the completed campaign.

---

## Session 9 — 2026-08-09 — Paper restructure (Background+Gap → Intro; Theory+Methods → §2)

**Dialogue.**
- User asked what I thought about moving Background and the gap into the Introduction and making
  Theory+Methods §2. I gave a split opinion: strongly agree on moving TE theory down to join Methods
  (removes the old §2.3/§3.3 split); qualified agree on folding Background+Gap into §1 (fixes real §1↔§2
  redundancy — the CM paragraph and the gap statement were each stated twice — but risks a bloated intro
  unless tightened). Flagged it as venue-dependent and reversible. Recommended proceeding with a
  "merge-and-tighten" (not paste) and a single consolidated gap.
- User: "keep light subsection headings (e.g., §1.1 Background, §1.2 Gap)." → executed with those.

**Decisions.**
- Fold old §2.1/§2.2 (Background) into new **§1.1 Background**; old §2.4 (Gap) into new **§1.2 Gap**
  (contributions/scope/roadmap flow within §1.2).
- Promote old §2.3 TE theory to **§2.1**, heading a new **§2 "Theory and Methods"**; old §3 methods →
  §2.2–§2.9; Figure 1 overview → §2 preamble.
- Renumber Results §4→§3, Discussion §5→§4, Conclusion §6→§5.
- Tightening applied: merged the duplicated CM paragraph, compressed old §2.2 to one paragraph, trimmed
  the "three threads" recap in the gap. Earned-novelty framing (Nichols + Harris/Jelali) preserved.

**Files changed.**
- `reports/te-firewall-paper-final.md` — restructured via `scratchpad/restructure.py` (one script:
  §1 rewrite + heading-anchor slicing + cascade-safe heading/cross-ref renumber).
- `reports/te-firewall-paper.docx` — regenerated by plain pandoc; backup
  `te-firewall-paper.docx.bak-20260809-170128-prerestructure`.
- `pages/log.md`, `SYNTHESIS.md` — this entry + §0 bullet.

**Verification.**
- Heading tree matches target exactly (§1 + §1.1/§1.2; §2 Theory and Methods + §2.1–§2.9; §3 Results
  3.1–3.6; §4 Discussion 4.1–4.3; §5 Conclusion).
- Every Section/§ cross-reference audited and consistent with the new numbering (ranges and "and"/comma
  lists handled; theory→§2.4 estimator ref correct); no stale §5.x/§6 refs; old section headings absent.
- 9 figures (Figure 1 once, not duplicated by the move), 6 tables, 30 references unchanged, first-person 0.
- docx: 9 media, 6 tables, all new headings present once.

**Open items / next.**
- Committed this session (restructure). The paper's section numbering is now Intro→Theory&Methods→
  Results→Discussion→Conclusion.
- Unchanged carry-overs: W6 canonical Sobol/coherence foil cites; Tier 3 references; venue undecided
  (APA-7 author–year retained); rotor-averaged-wind robustness check (server down).

---

## Session 14 — 2026-08-10 · §2.1 theory enrichment (Chen 2019) + X vector

**Dialogue.**
- **User:** provided `raw/papers/Application_of_Transfer_Entropy_Algorithm_in_Fault_Detection_for_Power_System_with_Wind_Turbines.pdf` (Chen, Li, Feng & Li, 2019, IEEE APAP) — "we need to enrich the theory formula with considering this paper. what do you think? and at the same time we need to mention that X = [z1,x2,…xn]".
- **Claude:** read the paper in full (6 pp; fitz text extraction, no page-render available) and §2.1/§2.4 + refs of `te-firewall-paper-final.md`. Reported that Chen is **already** integrated (cited at lines 66/78/90/96/142, ref line 415 with DOI): the manuscript already borrows Shannon H(X), MI identity, entropy rate, TE definition, Chen's Eq.6 identity `T=h_X−h_{X|Y}`, and the four-parameters framing. So "enrich" = complete/strengthen, not add a large new block. Pushed back on importing Chen's Eq.7 (four-joint-probability expansion): it is kernel-density / fixed k=l=1 discrete form, contradicting the paper's KSG estimator-agnostic §2.4 stance — a reviewer flag. Recommended (a) joint entropy as its own equation, (b) the `X=[x1,…,xn]` vector (read `z1`→`x1` typo; flagged vector-vs-scalar-`X` collision → bold `**X**`).

**Decisions.**
- AskUserQuestion → author selected **"Joint entropy + X vector (Recommended)"**. Declined the Markov-assumption equation and Chen's Eq.7.

**Files changed.**
- `reports/te-firewall-paper-final.md` — §2.1 only: (1) inserted `H(X,Y) = -Σ p(x,y) log p(x,y)` between the Shannon and MI blocks; (2) prepended a paragraph defining `**X** = [x1,x2,…,xn]` (Table 1) and mapping scalar source/target `Y`/`X` onto components `x_j`/`x_i`.
- `pages/log.md`, `SYNTHESIS.md` — this entry + §0 bullet; log frontmatter `updated: 2026-08-10`.

**Verification.**
- Re-read edited §2.1 region: buildup now reads Shannon → joint entropy → MI (H(X)+H(Y)−H(X,Y) references a defined quantity); vector notation reconciled with the scalar equations that follow (untouched). LaTeX is standard (`\mathbf{X}`, `\dots`, `\sum`), pandoc/MathJax-safe.
- Not done: docx/PDF regeneration (text-only edit; no figure/table impact).

**Open items / next.**
- Regenerate `te-firewall-paper.docx` (+ PDF if wanted) when the author wants the compiled artifact refreshed.
- Carry-overs unchanged: W6 canonical Sobol/coherence foil cites; Tier 3 references; venue undecided; rotor-averaged-wind robustness check (server down).

---

## Session 18 — 2026-08-11 — Eq. 8 leak question + §2.7 md↔docx sync

**Dialogue**
- User: "I have added eq.7, eq.8 and eq.9. The 2.7 SURD attribution paragraph is totally changed. Please revise the md file based on the docx. In the SURD eq. (Eq. 8) the leak part is eliminated — does it have any specific reason?"
- Claude: Yes, and it is correct. Eq. 8 decomposes the *mutual information* `I(Q; sources)`, which equals R + U + S
  exactly; the leak is not an MI atom — it is the residual of the target's future *entropy*
  (`H(Q) = I(Q; sources) + ΔI_leak`). Two different budgets / denominators, consistent with the manuscript's own
  normalization sentence (atoms = fractions of max MI; leak = fraction of target future entropy). Standard SURD
  convention (Martínez-Sánchez et al., 2024).
- Claude also reported: the md already carried Eqs 7 (AIS, §2.5), 8 (SURD leak-free, §2.7), 9 (delay-resolved TE,
  §2.9), all matching the docx; only the §2.7 prose differed, and the docx's rewrite had introduced a target/source
  slip plus a garbled duplicate tail.
- Asked how to reconcile, user chose **"Mirror docx wording into md."**

**Decisions**
- md §2.7 post-equation paragraph replaced with the docx wording, but with the leak/classification phrasing
  corrected to reference the *target's* future `Q` (not "the source's future"), and the garbled duplicate tail
  fragment dropped.
- Docx (canonical master) left untouched this session; the two slips + dangling fragment in the docx §2.7 were
  flagged for a later in-place XML fix.

**Files changed**
- `reports/te-firewall-paper-final.md` — §2.7 paragraph (no commit made this session).
- `pages/log.md` — session entry appended; frontmatter `updated: 2026-08-11`.
- `SYNTHESIS.md` — §0 latest bullet + this entry; frontmatter `updated: 2026-08-11`.

**Open items / next steps**
- Optional: apply the same two corrections (leak "source's future" → "target's future"; classification "about a
  source" → "about the target") and remove the duplicated tail fragment **in the canonical docx** (unpack →
  `word/document.xml` → `pack.py`, `PYTHONUTF8=1`). The garbled fragment lives in the single §2.7 run in
  `word/document.xml`. Not done — awaiting author go-ahead.

---

## Session 19 — 2026-08-11 — Cite Eqs 7, 8, 9 in text

**Dialogue**
- User: "please cite the equations 7, 8, 9 within the text regarding the eqs."
- Claude: confirmed the canonical master is the docx (final.md frozen per prior decision),
  checked the existing `(Eq. 1)`…`(Eq. 6)` style, and applied the same convention to 7/8/9.

**Decisions**
- Match the established style: `(Eq. N)` closes the introductory clause immediately before the
  display equation. Edit the canonical docx only; leave the frozen final.md alone.

**Files changed**
- `reports/te-firewall-paper.docx` — three `document.xml` text runs amended:
  - §2.5 (AIS, Eq. 7): "…active information storage of the target **(Eq. 7)**,"
  - §2.7 (SURD, Eq. 8): "…unique, and synergistic atoms **(Eq. 8)**:"
  - §2.9 (delay-resolved TE, Eq. 9): "…each candidate delay $d$ is **(Eq. 9)**:"
  - Backup: `te-firewall-paper.docx.bak-<ts>-eqcite789`
- `pages/log.md` — appended entry.
- `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Repack: `PYTHONUTF8=1 pack.py` → "All validations PASSED", 395 paragraphs preserved
  (the default codepage triggered a cp949 error reading `fontTable.xml`; forcing UTF-8 fixed it —
  environmental, not a document defect; only `document.xml` was edited).
- pandoc re-extract shows "(Eq. 7),", "(Eq. 8):", "(Eq. 9):" at the three sites.

**Open items / next steps**
- Unchanged from session 18: the two §2.7 target/source slips ("source's future" / "about a source"
  → should be target `Q`) remain in the docx, awaiting author go-ahead.

---

## Session 20 — 2026-08-11 — Manuscript formatting (TNR, justify, remove table rules)

**Dialogue**
- User: "the font must change to Times new roman and the paragraphs must be justified, and the
  lines between sections must be deleted."
- Claude: surveyed the docx; found body/heading font = theme `Aptos`, no justified paragraphs,
  and two kinds of horizontal lines (equation `TableGrid` boxes; booktabs rules in data tables).
  "Lines between sections" was ambiguous, so asked two clarifying questions (which lines; whether
  inline code should also become TNR).
- User answers: delete the **data-table rules** (leave equations); **keep code monospace**.

**Decisions**
- Font via theme (major+minor `<a:latin>` → Times New Roman) — cleanest, converts all prose+headings;
  keep Cambria Math (equations) and Consolas (`VerbatimChar` code) explicit.
- Justify via style inheritance: `jc="both"` on `BodyText` only (FirstParagraph/Compact inherit).
- Table rules: only Table 1 had visible inline rules (16 booktabs borders); `single`→`nil`.

**Files changed**
- `reports/te-firewall-paper.docx` — `theme1.xml` (2 latin typefaces), `styles.xml` (BodyText jc),
  `document.xml` (16 Table-1 cell borders single→nil). Backup `…bak-<ts>-fmt-tnr-justify-rules`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Repack `PYTHONUTF8=1 pack.py` → "All validations PASSED", 395 paragraphs preserved.
- Round-trip re-unpack of the packed file: theme = Times New Roman ×2 (no Aptos); 1 `jc="both"`;
  0 `single` / 16 `nil` table borders; 606 Cambria Math runs; 32 Consolas refs; Eqs 7/8/9 citations present.
- Caveat: no LibreOffice on this Windows box → could not render a PDF for visual confirmation;
  verification is XML-level (definitive for these structural attributes).

**Open items / next steps**
- Unchanged from session 18: the two §2.7 target/source wording slips remain in the docx (author
  hasn't asked to change them).
- If the author wants a visual check, render the docx to PDF on a machine with Word/LibreOffice.

---

## Session 21 — 2026-08-11 — Redesign Figure 4 (TE network graph)

**Dialogue**
- User: "please redesign the figure 4 (white font color is not clear) and the firewall part must be clearer."
- Claude: identified Fig 4 in the canonical docx = `media/image4.png`, byte-identical to
  `reports/figs/fig3-te-network.png`, generated by `_make_fig3_firewall_network.py` (confirmed by md5).
  Viewed the current PNG: white node labels illegible on the light-green platform nodes; the firewall was
  three disconnected cues (pink box + mid-canvas ✕ + far-right vertical "FIREWALL").

**Decisions**
- Fix labels with a contrast-aware colour rule (`_lum` luminance test), not by recolouring nodes
  (keeps palette consistent with the other figures). Add halos for extra crispness.
- Consolidate the firewall into a single physical "wall" metaphor on the WIND path only (wave legitimately
  reaches the platform, so no wall across the platform's approach): bold dashed wind arrow → hatched red
  wall + ✕ → faint blocked continuation into the highlighted platform zone; one boxed FIREWALL label + one
  white-boxed callout. Iterated once to move labels into clean pockets with white bboxes (first render had
  the callout overlapping the wind fan / "sig 28%" label).

**Files changed**
- `reports/figs/_make_fig3_firewall_network.py` — imports (+Rectangle, patheffects), `_lum`, rewrote
  `circle()`, added `_draw_wall()`, restyled protected-zone band, rewrote the firewall block.
- `reports/figs/fig3-te-network.png` — regenerated (1900×1309, unchanged size).
- `reports/te-firewall-paper.docx` — `media/image4.png` replaced with the new PNG.
  Backup `te-firewall-paper.docx.bak-<ts>-fig4-redesign`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Regenerated figure inspected by eye: green-node labels now dark and legible; firewall reads clearly as
  wind stopped at a wall, not reaching the platform.
- Embedded `image4.png` md5 == `fig3-te-network.png` md5 (5f7c5992…).
- Repack `PYTHONUTF8=1 pack.py` → "All validations PASSED", 395 paragraphs preserved; theme = Times New
  Roman and `jc=both` still present; Figure 4 caption intact.
- No LibreOffice on this box → no full-page PDF render; figure verified as a standalone PNG (definitive
  for its content) and the docx verified structurally.

**Open items / next steps**
- Unchanged: the two §2.7 target/source wording slips remain in the docx (author hasn't asked to change them).

---

## Session 22 — 2026-08-11 — Shorten Figure 4 caption

**Dialogue**
- User: "figure 4's caption is too long please make it shorter, if we need to keep it it must be within the text."
- Claude: trimmed the caption to a single identifying sentence and moved the substantive content into the
  paragraph that introduces the figure (nothing dropped except the normalization gloss, which §2.5 already defines).

**Decisions**
- Caption keeps only figure identity + edge-weight definition (one $TE_{frac}$ math). Descriptive/interpretive
  claims belong in the body per the author's instruction.

**Files changed**
- `reports/te-firewall-paper.docx` — `document.xml`: caption paragraph trimmed (removed 2nd $TE_{frac}$ oMath +
  long descriptive run; run before it shortened to " over the 54 cases."); intro paragraph expanded with the
  relocated content. Backup `te-firewall-paper.docx.bak-<ts>-fig4-caption`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- `PYTHONUTF8=1 pack.py` → "All validations PASSED", 395 paragraphs preserved.
- pandoc plain-text re-extract: caption now one sentence; intro paragraph carries wave/wind detail + firewall
  statement and flows into the existing "The interpretation is not that wind…" paragraph.

**Open items / next steps**
- Unchanged: the two §2.7 target/source wording slips remain in the docx (author hasn't asked to change them).

---

## Session 23 — 2026-08-11 — Replace "§" with "Section"/"Sections"

**Dialogue**
- User: "I think the sign § within the text is not common within the text."
- Claude: confirmed the docx already spelled out Section(s) in most places (so § was the inconsistent
  minority), then converted all 27 § in `document.xml` to the spelled-out form.

**Decisions**
- Spell out "Section" (capital S, as a reference proper noun) everywhere; use plural "Sections" for
  ranges/lists; convert the Kraskov "§III.A" citation refs to "Section III.A" for full consistency.

**Files changed**
- `reports/te-firewall-paper.docx` — `document.xml`: 2 multi-ref runs edited for plural grammar; 22
  single refs bulk-replaced (+ space/whitespace fixups). Backup `…bak-<ts>-section-signs`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- 0 "§" left, 0 glued "SectionN", 0 double spaces; `PYTHONUTF8=1 pack.py` → "All validations PASSED",
  395 paragraphs preserved; pandoc re-extract confirms the converted refs.
- Process note: the bulk replace first glued the number and trimmed two trailing spaces; both caught by
  verification and fixed before repack — a reminder to check whitespace when replacing single chars in runs.

**Open items / next steps**
- Unchanged: the two §2.7 (now "Section 2.7") target/source wording slips remain in the docx.

---

## Session 24 — 2026-08-11 — Narrate Figure 5a dose–response in §3.3

**Dialogue**
- User: "what does figure 5a show?" → Claude described it (SURD firewall dose–response; below-rated median
  0.023 vs at/above-rated ~0.064, 2.8×, positive in 100% of 54 cases).
- User: "did you mention the point in the manuscript?" → Claude checked: the qualitative point appears in the
  abstract/intro ("strength depends on the operating region") and §3.3 points to Figure 5, but the quantitative
  result (2.8×, regime medians) was NOT in the body — only in the figure/caption.
- User: "yes add it to Section 3.3."

**Decisions**
- Insert one prose sentence stating the dose–response result, right after the SURD-redirection sentence.
  Keep the SURD code-term and the math symbol out of the sentence to avoid run fragmentation; cite Figure 5a.

**Files changed**
- `reports/te-firewall-paper.docx` — `document.xml`: added the dose–response sentence to the §3.3 SURD-redirection
  paragraph. Backup `te-firewall-paper.docx.bak-<ts>-fig5a-doseresponse`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Numbers cross-checked against Figure 5a (`media/image5.png`): 0.023 below-rated; per-regime medians
  0.066/0.064/0.042 (range 0.042–0.066); "median 2.8x below-rated"; "positive in 100% of cases".
- `PYTHONUTF8=1 pack.py` → "All validations PASSED", 395 paragraphs preserved; pandoc re-extract confirms the
  sentence reads correctly in context.

**Open items / next steps**
- Fig 5b/5c results are similarly figure-only if the author wants the same treatment (not requested).
- Unchanged: the two Section 2.7 target/source wording slips remain in the docx.

---

## Session 25 — 2026-08-11 — Figure 5a legend + footnote-to-text

**Dialogue**
- User: "in figure 5a, we need some changes: dot, bar, dash lines must be as legend, and 'circular-shift bias
  control subtracted. drop is positive in 100% of the cases' must be mentioned within the text."

**Decisions**
- Convert the dot/bar/dashed-gate encoding into a proper 3-item legend; delete the explanatory footnote and the
  redundant inline gate label. Relocate both footnote sentences into the §3.3 dose-response sentence (the
  100%-positive claim was already added there in session 24; added the circular-shift bias-correction clause).

**Files changed**
- `reports/figs/_make_surd_figs.py` — dose-response block: +Line2D import, +legend, −footnote, −inline gate
  annotation, `bottom` 0.16→0.18.
- `reports/figs/surd-dose-response.png` — regenerated (1480×840, unchanged size).
- `reports/te-firewall-paper.docx` — `document.xml` §3.3 sentence revised; `media/image5.png` replaced.
  Backup `te-firewall-paper.docx.bak-<ts>-fig5a-legend`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- New figure inspected: clean 3-item legend (individual case / regime median / materiality gate 0.02), footnote gone.
- Other two SURD figs (surd-openloop, surd-vs-te) re-rendered byte-identical (md5 unchanged) — no collateral change.
- Embedded image5 md5 == surd-dose-response md5 (4918636e…); `PYTHONUTF8=1 pack.py` → "All validations PASSED",
  395 paragraphs preserved; pandoc confirms the revised §3.3 sentence.

**Open items / next steps**
- No LibreOffice on this box → figure verified as standalone PNG; docx verified structurally.
- Unchanged: the two Section 2.7 target/source wording slips remain in the docx.

---

## Session 26 — 2026-08-11 — Figure 5a two-tone regime bands

**Dialogue**
- User (after the "do we need pitch control inactive?" discussion — Claude recommended keeping it):
  "shall we make a color spectral for this two parts?"
- Claude: yes; clarified the look via AskUserQuestion (two-tone bands / color the dots / spectral gradient /
  both). User chose **two-tone bands**.

**Decisions**
- Subtle background shading, not point recoloring: cool grey behind the inactive (below-rated) zone, light
  teal (paper accent) behind the active (at/above-rated) zone; split at the rated boundary with a faint dashed
  divider. Keep the existing bracket labels.

**Files changed**
- `reports/figs/_make_surd_figs.py` — dose-response block: two `axvspan` bands + `axvline` divider (zorder 0–1).
- `reports/figs/surd-dose-response.png` — regenerated (1480×840, unchanged size).
- `reports/te-firewall-paper.docx` — `media/image5.png` replaced. Backup `…bak-<ts>-fig5a-bands`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Figure inspected: grey vs teal bands read clearly; navy dots/medians and legend unaffected; labels sit over
  their bands.
- Other two SURD figs (surd-openloop, surd-vs-te) byte-identical (md5 unchanged).
- Embedded image5 md5 == surd-dose-response md5 (254fea0f…); `PYTHONUTF8=1 pack.py` → "All validations PASSED",
  395 paragraphs preserved.

**Open items / next steps**
- No LibreOffice → figure verified as standalone PNG; docx verified structurally.
- Unchanged: the two Section 2.7 target/source wording slips remain in the docx.

---

## Session 27 — 2026-08-11 — State the rated wind speed (10.59 m/s)

**Dialogue**
- User: "why in 8 m/s there was no active controller?" → Claude explained the control regions (Region 2 below
  rated: pitch parked at fine, generator-torque loop active; Region 3 above rated: collective-pitch loop
  engages to shed power/regulate thrust — the regime where the firewall operates). Rated ≈ 10.59 m/s (IEA-15MW).
- User: "the IEA-15MW has a rated wind speed of ~10.59 m/s. shall we mention it in the caption?"
- Claude: found the value was absent from the whole manuscript; recommended methods + caption. User chose both.

**Decisions**
- Put the numeric rated speed in the methods (turbine description, its proper home, serves Table 4/§3.3/Fig 5a)
  AND a compact "(10.59 m/s)" in the Fig 5a caption for standalone readability.

**Files changed**
- `reports/te-firewall-paper.docx` — `document.xml`: methods sentence + Fig 5a caption. Backup `…bak-<ts>-ratedspeed`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- `PYTHONUTF8=1 pack.py` → "All validations PASSED", 395 paragraphs preserved; pandoc shows "10.59 m/s" at both
  sites (methods turbine description; Fig 5a caption). Source: IEA-15-240-RWT (Gaertner et al., 2020).

**Open items / next steps**
- Unchanged: the two Section 2.7 target/source wording slips remain in the docx.

---

## Session 28 — 2026-08-11 — Fig 5b legend + footnote-to-text

**Dialogue**
- User: "5b is necessary?" → Claude: yes, keep it (most direct visual of the redirection thesis; carries the
  figure-only 94% stat).
- User: "surd materiality 0.02 move to legend; 54 joined cases (first-pass… TE is non-zero in only… move to text."

**Decisions**
- Fig 5b: gate label → legend (third entry, matching 5a's "materiality gate (0.02)"); footnote deleted.
- Footnote facts → §3.3 by replacing the generic Figure-5 roadmap sentence with a Fig-5b sentence (54 cases,
  first-pass KSG TE table, TE non-zero in only two). Positivity-in-all-54 not repeated (already in the 5a sentence).
- Left the "48/51, 94%" annotation box in the figure (not requested; still figure-only — candidate for later text).

**Files changed**
- `reports/figs/_make_surd_figs.py` — surd-vs-te block: −inline gate annotation, +legend gate entry
  (`get_legend_handles_labels` + Line2D), −footnote, bottom 0.18→0.13.
- `reports/figs/surd-vs-te.png` — regenerated (1480×880, unchanged size).
- `reports/te-firewall-paper.docx` — `document.xml` §3.3 sentence swapped; `media/image6.png` replaced.
  Backup `te-firewall-paper.docx.bak-<ts>-fig5b`.
- `pages/log.md` — appended entry. `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Figure inspected: legend now has the dashed gate; footnote gone.
- Other two SURD figs (dose-response, openloop) byte-identical (md5 unchanged).
- Embedded image6 md5 == surd-vs-te md5 (bb594c31…); `PYTHONUTF8=1 pack.py` → "All validations PASSED",
  395 paragraphs preserved; pandoc confirms the §3.3 sentence.

**Open items / next steps**
- Fig 5b's "48/51, 94%" statistic is still figure-only — offer to add to text if the author wants.
- Unchanged: the two Section 2.7 target/source wording slips remain in the docx.

---

## Session 29 — 2026-08-11 — Add Nomenclature (Latin + Greek)

**Dialogue**
- User: "make a Nomenclature in an alphabetic order, and groupby by English and Greek."

**Decisions**
- Two groups as requested: "Latin symbols" (= English/Latin-alphabet) and "Greek symbols", each alphabetical.
- Placement after keywords, before §1 Introduction (Elsevier-style front matter).
- Include only symbols (not acronyms) per the explicit English+Greek framing; offer an Abbreviations group separately.
- Typography: italic symbols with real vertAlign sub/superscripts; hanging-indent (1620 dxa) + tab so
  definitions align/wrap; Compact style, left-justified (override BodyText jc=both).

**Files changed**
- `reports/te-firewall-paper.docx` — `document.xml`: +35 paragraphs (Nomenclature heading + 2 subheadings +
  28 Latin + 4 Greek entries) inserted after the keywords run. Backup `…bak-<ts>-nomenclature`.
- `pages/log.md` — appended entry (full symbol list). `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Symbols harvested from docx math `m:t` tokens + per-Greek-letter context grep; borderline symbols (Hs, Tp,
  n_perm, AIS, TE_frac, K, r) confirmed present in the text before listing (no invented entries).
- `PYTHONUTF8=1 pack.py` → "All validations PASSED", paragraphs 395→430 (+35); pandoc re-extract shows both
  groups alphabetical with symbols + definitions intact; Greek group = α, γ²(f), Δf, τ.

**Open items / next steps**
- Offered but not added: an Abbreviations/acronyms group (TE, SURD, KSG, AIS, FOWT, OpenFAST, IDTxl, ROSCO, DLC…).
- If the author prefers the literal heading "English symbols" over "Latin symbols", trivial change.
- Unchanged: the two Section 2.7 target/source wording slips remain in the docx.

---

## Session 30 — 2026-08-11 — Add Abbreviations to the Nomenclature

**Dialogue**
- User: "yes add the abbreviations as well" (following the offer at end of session 29).

**Decisions**
- Add "Abbreviations" as a third bold subheading after Greek symbols (upright acronyms, same hanging-indent+tab
  layout). Include genuine acronyms + primary tools; exclude OpenFAST submodules, channel names, and citation
  venues. "English"/Latin symbols and Greek from session 29 unchanged.

**Files changed**
- `reports/te-firewall-paper.docx` — `document.xml`: +20 paragraphs (Abbreviations subheading + 19 entries)
  inserted after the τ (Greek) entry, before the frontmatter rule. Backup `…bak-<ts>-abbrevs`.
- `pages/log.md` — appended entry (full acronym list). `SYNTHESIS.md` — §0 rewritten + this entry.

**Verification**
- Expansions verified against first-use context in the text (OMA, ML, FOWT, IDTxl, JIDT, ROSCO, SCADA, etc.).
- `PYTHONUTF8=1 pack.py` → "All validations PASSED", paragraphs 430→450 (+20); pandoc re-extract shows the
  Abbreviations group alphabetical with expansions intact (KSG = "Kraskov–Stögbauer–Grassberger").

**Open items / next steps**
- Nomenclature now has three groups: Latin symbols (28), Greek symbols (4), Abbreviations (19).
- If the author prefers "English symbols" over "Latin symbols" heading, trivial change.
- Unchanged: the two Section 2.7 target/source wording slips remain in the docx.
