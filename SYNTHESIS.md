---
title: "Synthesis — conversation & decision record"
type: synthesis
created: 2026-07-09
updated: 2026-07-09
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

## §0 Current state — read this first (rewritten 2026-07-09)

- **Phase 4 full TE campaign is RUNNING on lams** (both A100s, single-process
  GPU launcher `0e550e0`), relaunched 2026-07-06 after the CPU-shard run
  wedged. **User-reported ETA: ~11 days** (→ ~2026-07-17). Output:
  `reports/te_table_full.parquet` (supersedes stale first-pass
  `te_table.parquet`).
- **Paper**: `reports/te-firewall-paper-draft.md` at **v0.5** (commit
  `4186414`, via full ARS pipeline). Thesis: wind→platform TE≈0 is a
  blade-pitch-control *firewall*; TE rising = pitch fault → health monitoring.
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
### Open items / next steps
- Rest of the 11-day window: user to specify next vault changes (content
  catch-up for SURD/paper pages, structural changes, hygiene pass were the
  offered options — "something else" chosen was this file; the others remain
  candidates).
- Uncommitted conference-deck work still needs sorting/committing.
- When lams finishes: pull `te_table_full.parquet`, re-score hypotheses,
  finalize report ver08.
