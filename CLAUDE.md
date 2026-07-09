# CLAUDE.md — standing instructions for this vault

## Session record (MANDATORY, every session)

This project has two durable records. Git commits are NOT a substitute for
either — they went stale for 5 weeks once and the user objected.

1. **`SYNTHESIS.md`** (vault root) — the conversation record.
   - **At session start:** read §0 ("Current state") before answering any
     "where were we / what were we doing" question.
   - **Before ending any session with substantive work or decisions:** append
     a session entry (Dialogue: user↔Claude Q&A, Decisions, Files changed
     with commit hashes, Open items) and **rewrite §0** to reflect the new
     state. Log plannings, Claude's questions + user's answers, user's
     questions + Claude's answers, and every file update.
   - Append-only, newest at the bottom. §0 is the only section that gets
     rewritten.

2. **`pages/log.md`** — the task-level wiki log.
   - Append entries for substantive tasks (campaign launches, bug fixes,
     paper milestones, structural changes) using the conventions in its
     header (`## [YYYY-MM-DD] ingest|query|lint|structure | <Title>`),
     newest at the bottom. Update its `updated:` frontmatter date.

## Project pointers

- Server round-trips (push → run → pull): `PER_ROUND_CHECKLIST.md`.
- First-time server setup: `SERVER_DEPLOYMENT.md`.
- Wiki structure rules: `SCHEMA.md`; project plan: `PLAN.md`.
- Skills index: `SKILLS.md`.

## Working agreements (from user feedback)

- Don't silently pick an interpretation — surface assumptions, ask when
  unclear.
- Cite authoritative sources (OpenFAST GitHub; IDTxl repo / Schreiber /
  Kraskov / Wollstadt papers), don't just paraphrase.
- No wall-clock schedule assumptions ("tomorrow", "in the morning") — phrase
  next steps as task state ("when the run finishes").
- Validate the JIDT path with a real estimate (`test_ar1_te.py`) before
  launching any TE campaign.
