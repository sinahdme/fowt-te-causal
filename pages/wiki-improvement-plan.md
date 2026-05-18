---
title: "Wiki Improvement Plan"
type: wiki-improvement-plan
created: 2026-05-12
updated: 2026-05-12
tags: [meta, planning, alignment]
---

# Wiki Improvement Plan

Meta-page recording lessons learned and planned wiki structural changes.
Not project content — the **wiki itself** is the subject.

## Status (snapshot 2026-05-12, late evening)

- Three-layer split established (`raw/` README-only, `pages/` seeded, `SCHEMA.md` written).
- **48 markdown pages**: 18 entities (9 OpenFAST modules + 1 reference platform +
  7 software + `openfast`), 6 concepts, 4 equations, 4 validation cases,
  3 README placeholders (sources/papers/analyses), 5 meta pages, 6 raw/ READMEs +
  raw/README, SCHEMA, PLAN, LLM_Wiki_Pattern.
- Migrated from previous theme-foldered `vault/` layout in a single restructure
  pass. Old `vault-legacy/` kept at project root for reversibility.
- User opened vault in Obsidian; moved `PLAN.md` and `LLM_Wiki_Pattern.md`
  into the vault root alongside `SCHEMA.md` for single-vault setup.
- All in-prose references to PLAN / SCHEMA / LLM_Wiki_Pattern converted from
  `../*.md` relative paths to `[[PLAN]]`, `[[SCHEMA]]`, `[[LLM_Wiki_Pattern]]`
  wikilinks (alignment pass, 22 files touched).
- Cleanup: removed Obsidian default `Welcome.md`, stray empty `Transfer Entropy/`
  folder, 7 `.clonelog` files in `repos/`.
- Phase 1 complete. Phase 2+ gated on Q1/Q2 in [[open-questions]].

## Next planned actions

Triggered when the user provides Q1/Q2 from [[open-questions]]:
- Create one `entities/channel-<name>.md` page per locked response channel.
- Update [[entities/iea-15mw-volturnus-s]] "Sweepable parameters" with the
  locked sweep list.
- Convert [[validation/case-3-iea15-single-case-te]] from stub to executable
  plan (specific OutList, TurbSim seed, runtime).

Triggered after the first OpenFAST run lands:
- Ingest the channel docstrings from `repos/openfast/docs/` into individual
  `entities/channel-*.md` pages (via `analysis/build_vault.py`).
- File a first `analyses/wind-vs-pitch-te-<date>.md` from the smoke-test
  run.

Triggered every ~10 page additions:
- Run a lint pass (orphans, stubs, broken links, inconsistent link paths).
- Update [[index]] for any divergence from filesystem state.

## Open structural decisions

- **Channel pages location**. Currently planning `pages/entities/channel-*.md`
  with `channel-` prefix to group them. Alternative: `pages/channels/` as
  its own folder, which would mirror the original `vault/Channels/`
  intent. *Decide once first 5–10 channel pages exist — if they dominate
  `entities/`, split out.*

- **Software entities vs sources/papers**. IDTxl, SALib, OpenFAST themselves
  have associated *papers*. Right now they live in `entities/` only. Once
  we ingest the corresponding paper PDFs into `raw/papers/`, we'll have
  `sources/<key>.md` and `papers/<key>.md` *in addition*. The entity page
  is the **tool**, the source page is the **citation** — keep both.

- **Equations folder size**. If `equations/` stays under ~15 pages it can
  stay flat. If it grows past that (e.g., a separate aero-momentum theory
  equation set), split into `equations/info-theory/` and `equations/physics/`.

## Lessons from this restructure

- The original `vault/` was theme-foldered (Modules / Models / Theory)
  rather than type-foldered (concepts / entities / equations). The
  type-foldered LLM_Wiki_Pattern works better because **the link graph
  cuts across themes naturally** — a TE concept page links to a module
  entity that links back to a channel. Putting them in the same folder
  obscures the type hierarchy.
- Equations were buried inside theory notes. Pulling them out as
  standalone `eq-*.md` pages makes them reusable across multiple concept
  pages (e.g., MI definition appears in both Sobol-companion-MI and
  TE-definition contexts).
- Started [[open-questions]] and this page on day 1 (per Part 4 of
  [[LLM_Wiki_Pattern]]) instead of after 30+ pages — paying off
  immediately as Q1/Q2 are already substantively tracked.

## Anti-patterns we will avoid

- Storing OpenFAST `.out`/`.outb` outputs in `raw/data/`. They live in
  `../sims/` (generated, not curated). The wiki references them by path.
- Inlining LaTeX-heavy derivations into concept pages. Equations get their
  own `eq-*.md` page; concept pages link out.
- Bare `[[X]]` links. Always `[[folder/X]]`.
