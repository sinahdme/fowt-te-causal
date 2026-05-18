# LLM-maintained Wiki — pattern + refined schema

A portable starter document you can take to a new project / vault. **Part 1** is the original pattern (the idea you shared). **Part 2** is the refined schema and workflows I evolved while building this vault. **Part 3** is a quickstart for bootstrapping a fresh vault. **Part 4** is the lessons learned that future versions should keep in mind.

To use: drop this file into the new vault's root, share it with the LLM agent of choice (Claude Code, Codex, etc.), and ask the agent to instantiate a `SCHEMA.md` and the folder structure based on it.

---

# Part 1 — The core idea (original)

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is **rediscovering knowledge from scratch on every question**. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. **The knowledge is compiled once and then kept current, not re-derived on every query.**

This is the key difference: the wiki is a persistent, compounding artefact. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarising, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, run the LLM agent on one side and Obsidian on the other. The LLM makes edits based on the conversation, you browse the results in real time — following links, checking the graph view, reading updated pages. Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase.

## Architecture (three layers)

1. **Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them.

2. **The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely.

3. **The schema** — a document (e.g., `CLAUDE.md`, `AGENTS.md`, or `SCHEMA.md`) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. You and the LLM co-evolve this over time as you figure out what works for your domain.

## Operations

- **Ingest.** You drop a new source into the raw collection and tell the LLM to process it. The LLM reads it, discusses key takeaways with you, writes a summary page, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10–15 wiki pages. Ingest one at a time when you want close supervision; batch when you don't.

- **Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. **Good answers can be filed back into the wiki as new pages**: a comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. Explorations should compound in the knowledge base just like ingested sources do.

- **Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps. The LLM is good at suggesting new questions to investigate. This keeps the wiki healthy as it grows.

## Indexing and logging

- **`index.md`** is content-oriented. A catalogue of every page with a one-line summary, organised by category. The LLM updates it on every ingest. The LLM reads it first when answering a query, then drills into specific pages.

- **`log.md`** is chronological. An append-only record of what happened and when — ingests, queries, lints. With consistent prefixes (e.g. `## [YYYY-MM-DD] ingest | Source title`) the log becomes parseable with grep.

## Tips & tricks

- Obsidian Web Clipper converts web articles to markdown — easy way to drop sources into `raw/`.
- Set Obsidian's attachment folder path to a fixed location (e.g. `raw/assets/`) and bind a "Download attachments" hotkey so images get downloaded locally.
- Obsidian's graph view is the best way to see the shape of your wiki.
- Marp turns markdown into slide decks; useful for generating presentations from wiki content.
- Dataview queries page frontmatter — if pages have YAML metadata (tags, dates, source counts), Dataview makes dynamic tables.
- The wiki is just a git repo of markdown — you get version history and collaboration for free.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the **bookkeeping**. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. **LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass.** The wiki stays maintained because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

---

# Part 2 — Refined schema (developed in practice)

This part is the concrete schema I converged on while building a real research wiki for a manuscript-finalization project. Use it directly, or treat it as a starting point and adapt to your domain.

## Folder layout

```
<vault-root>/
├── LLM_Wiki_Pattern.md       # This file
├── wiki/
│   ├── SCHEMA.md             # Domain-specific schema (extends Part 2)
│   ├── raw/                  # Source materials, never modified by LLM
│   │   ├── papers/           # Published PDFs / journal articles
│   │   ├── manuscripts/      # Drafts you're authoring (versioned)
│   │   ├── extracts/         # Plain-text extractions of PDFs/DOCX
│   │   ├── data/             # CSV, MAT, XLSX, JSON
│   │   ├── figures/          # PNG, JPG, SVG
│   │   └── notes/            # Existing markdown notes you bring in
│   └── pages/                # LLM-generated. LLM owns this entirely.
│       ├── index.md          # Catalogue
│       ├── log.md            # Chronological
│       ├── overview.md       # Top-level synthesis
│       ├── open-questions.md # Tracked research questions ←  added later
│       ├── wiki-improvement-plan.md  # Meta-plan ← added later
│       ├── sources/          # One page per raw item — citation + summary
│       ├── papers/           # Deep analytical pages for key references
│       ├── concepts/         # Definable ideas
│       ├── entities/         # Named things (sites, people, software, geometries)
│       ├── equations/        # Standalone pages for key equations
│       ├── validation/       # Test cases (if relevant to your domain)
│       └── analyses/         # Filed-back query answers (compound knowledge)
```

Adapt the subfolders. For a research project you'll likely keep all of these. For a personal-knowledge / book-reading wiki you might drop `equations/` and `validation/` and add `themes/`, `chapters/`, etc.

## Page types and naming

All filenames are **kebab-case** and end in `.md`. Use `[[wiki-link]]` syntax for cross-references (Obsidian-compatible). Aim for many small pages over a few large ones — the wiki's value comes from the link graph, and many small linkable nodes beats a few monolithic ones.

| Type | Folder | Filename pattern | Purpose |
|------|--------|------------------|---------|
| Source | `sources/` | `<author><year>-<short-title>.md` | One per raw item — summary, key claims, where the file lives |
| Paper | `papers/` | `<author><year>.md` | Deeper analytical companion for key references |
| Concept | `concepts/` | `<concept-name>.md` | A definable idea |
| Entity | `entities/` | `<entity-name>.md` | A named thing — site, person, software, dataset, geometry |
| Equation | `equations/` | `eq-<name>.md` | A formula with derivation, units, where used |
| Validation | `validation/` | `case-<n>-<name>.md` | A specific test case (research-paper context) |
| Analysis | `analyses/` | `<topic>-<YYYY-MM-DD>.md` | Filed-back answers to substantive queries |

## Frontmatter

Every page starts with YAML frontmatter:

```yaml
---
title: "Human-readable title"
type: source | paper | concept | entity | equation | validation | analysis | overview | index | log
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["citation-key-1", "citation-key-2"]   # citation keys this page draws on
tags: [domain-tag, methodology-tag]              # free-form
---
```

For `source` pages, also include:

```yaml
source_path: "raw/papers/<filename>.pdf"
authors: ["Lastname, F.", "Lastname, G."]
year: 2024
venue: "Journal name"
doi: "10.xxxx/yyyy"
citation_key: "lastname-2024"
```

## Page body structure (templates)

### Source / Paper page
```markdown
## Citation
<full bibliographic citation>

## TL;DR
<3–5 bullet takeaways>

## Key claims
- Claim with [[concept-link]] reference
- ...

## Equations introduced (if any)
- [[eq-...]] — Eq. N

## Methods
<methodology in 1–2 paragraphs>

## Data / cases
<centrifuge tests, field sites, datasets, etc.>

## How it informs this project
<concrete impact on simulation code, validation, manuscript, etc.>

## Open questions / contradictions
<things flagged for future investigation>
```

### Concept page
```markdown
## Definition
<one paragraph>

## Why it matters here
<connection to project>

## Related concepts
- [[other-concept]] — relationship

## Sources
- [[source-key]] §Section
```

### Entity page
```markdown
## What it is
<definition>

## Properties / parameters
<table or list>

## Appears in
- [[where-it-shows-up-1]]

## Sources
```

### Analysis page (filed-back query)
```markdown
## Question
<what was asked>

## Hypothesis (if applicable)
<what we expected>

## Method
<what was done>

## KPI / result table
<concrete numbers>

## Conclusion
<what this means for the project>

## Source artefacts
- Code: <files>
- Figures: <files>
- Data: <files>

## Related
- [[other analyses]]
- [[concepts/...]]
```

## Conventions

- **Citation keys** are `<lastname-year>` (lowercase, hyphenated). Multi-author: first author. Use these as filenames in `sources/` and `papers/`.
- **Cross-references** use `[[link]]`. Link concepts and entities the first time they appear on a page. Be consistent about path prefixes (always `[[sources/X]]`, never bare `[[X]]`) — bare links work in Obsidian but break elsewhere.
- **Quotes from sources** use blockquotes with citation: `> ... (citation-key, p. 561)`.
- **Numbers in source pages match the source exactly**. If you adjust a value in synthesis, note "adjusted from <original> because <reason>" with a link.
- **Never delete a page** without recording it in `log.md`. If a page becomes wrong, prefer updating it (with `updated:` bumped) over silent rewrite.
- **Keep pages short**. If a page exceeds ~400 lines, split along a natural boundary.

## Workflows

### Ingest — adding a new source

1. User drops a file into the appropriate `raw/` subfolder (or asks the LLM to file an existing one).
2. LLM reads the source. For PDFs, extract to text and place in `raw/extracts/<basename>.txt`.
3. Discuss key takeaways (skip if batch-ingesting).
4. Create `pages/sources/<citation-key>.md` (and `pages/papers/<citation-key>.md` if it warrants deeper analysis).
5. For each new concept introduced, create or update `pages/concepts/<concept>.md`.
6. For each new entity (site, person, software), create or update `pages/entities/<entity>.md`.
7. For each new equation, create or update `pages/equations/eq-<name>.md`.
8. Update `pages/index.md` — add the new entries under the right category.
9. Append an entry to `pages/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | <Title>
   - Source: [[sources/<key>]]
   - New pages: [[concepts/x]], [[entities/y]]
   - Updated: [[overview]] (added <one-line>)
   - Notes: <anything surprising, contradictions flagged, follow-ups>
   ```
10. If the new source contradicts existing pages, **flag it on both pages** under "Open questions" and surface to the user. Add to `open-questions.md` if substantive.

### Query — answering a question

1. Read `pages/index.md` first to find candidate pages.
2. Drill into 3–8 relevant pages.
3. Synthesise an answer with `[[wiki-link]]` citations to wiki pages and `(citation-key)` to raw sources.
4. **If the answer is non-trivial and likely to be re-asked or built upon**, propose filing it as `pages/analyses/<topic>-<YYYY-MM-DD>.md`. Include the question, method, results table, and links to source artefacts. Update `index.md`.
5. Append a one-line query entry to `log.md`.

### Lint — periodic health check

Run when asked, or every ~10 ingests. Check:

- **Orphans**: pages with no inbound `[[links]]` — should they exist or merge?
- **Stubs**: pages under 20 lines that look incomplete.
- **Broken links**: `[[X]]` references where no file `X.md` exists. Decide: create stub, fix the link, or remove.
- **Inconsistent link paths**: `[[X]]` vs `[[sources/X]]` vs `[[papers/X]]` for the same target — standardise.
- **Mentioned-but-missing**: concepts/entities mentioned in body text but no page exists.
- **Stale claims**: pages where `updated:` is much older than newest source they cite, or that contain numbers superseded by later analyses.
- **Contradictions**: numbers/claims that disagree across pages without an explicit reconciliation.
- **Index drift**: entries in `index.md` pointing to nonexistent files, or files not in the index.

Output a punch list to the user. Do not auto-fix without confirmation.

## Two special pages I added later

These weren't in Part 1 but turned out to be high-value once the wiki had ~30+ pages:

- **`open-questions.md`** — a single tracked list of research questions with status (🟢 open / 🟡 under investigation / 🔵 resolved / ⚪ deferred). Without it, the slow drift of "things to investigate" is forgotten between sessions.

- **`wiki-improvement-plan.md`** — a meta page recording how the wiki itself should evolve. Lessons-learned, planned additions, things to revisit at the next milestone. Useful when picking up the wiki after a long gap.

---

# Part 3 — Quickstart for a new vault

When starting a fresh project, do this on day 1:

## Step 1 — Bootstrap

1. Create the folder structure shown in Part 2 above.
2. Drop `LLM_Wiki_Pattern.md` (this file) at the vault root.
3. Open the LLM agent (Claude Code, Codex, OpenCode, etc.) in the vault root.
4. Ask: *"Read `LLM_Wiki_Pattern.md` and instantiate a `wiki/SCHEMA.md` adapted to my domain, which is X. Create empty `index.md`, `log.md`, and `overview.md`."*

## Step 2 — Define the domain

Before ingesting, give the LLM a short paragraph describing:
- What the project is about (one sentence)
- Who you are and what role this wiki plays for you (researcher, student, founder, hobbyist…)
- What "success" looks like (publish a paper, finish a book, make a decision, build a product)

The LLM uses this to bias schema choices. A research wiki needs `papers/` and `equations/`; a book-reading wiki needs `themes/` and `characters/`; a competitive-analysis wiki needs `companies/` and `products/`.

## Step 3 — Ingest your first source

Pick one source (not all of them). Walk through the ingest workflow with the LLM watching you. This calibrates the LLM's understanding of your taste — what level of detail you want, which concepts you treat as canonical, etc.

After 3–5 ingests, the LLM will be ingesting at the right level of abstraction without you needing to nudge each time.

## Step 4 — Ask your first non-trivial question

Once you have ~5 sources ingested, ask a question that requires synthesizing across them. This is when the wiki starts paying off (RAG could not have given you this answer cleanly).

If the answer is good: ask the LLM to file it as an `analyses/<topic>-<date>.md` page.

## Step 5 — Schedule maintenance

Mark a recurring slot to:
- Run a lint pass (every ~10 ingests, or quarterly).
- Re-read `wiki-improvement-plan.md` and update the priorities.
- Update `open-questions.md` with anything that surfaced during the period.

This is the part most wikis fail at when humans maintain them. With the LLM doing the work, you only need to *ask*.

---

# Part 4 — Lessons learned

These are things I'd do the same on the next vault, and things to consider differently.

## What worked

- **Three-layer split** (`raw/` immutable, `pages/` LLM-owned, `SCHEMA.md` shared) — kept everyone honest. The LLM never accidentally edited a source PDF; the user never accidentally rewrote a generated page.
- **Many small pages over a few large ones**. The wiki's value is the link graph, and many linkable nodes beats a few monoliths.
- **Frontmatter from day 1**. Even simple frontmatter (title, type, created, updated, tags) pays for itself the first time you need to do a structured query (Dataview or grep).
- **Filed-back analyses**. The single highest-leverage practice. Without it, every substantive query produces value that disappears into chat history. With it, the wiki compounds with every conversation.
- **Open-questions as a tracked artefact**. Stops research drift forgetting what was wanted to investigate.

## What to do differently next time

- **Standardise link paths from the start**. Don't allow bare `[[X]]` links — always use `[[folder/X]]`. Saves a lint pass.
- **Lint earlier, more often**. The first lint pass at ~40 pages had ~6 fixable items. If lint had run at 15 pages it would have caught some of them earlier.
- **Don't let the source extracts and the source pages drift**. Do them in the same step.
- **A code-snapshots folder** for reproducibility, if the project involves running scripts. Capture default parameters and key entry points alongside the wiki content.
- **Decide on Obsidian vs portable upfront**. If the wiki may move out of Obsidian later, avoid Obsidian-only features (Dataview, advanced wikilinks). If it'll stay in Obsidian, lean into them.
- **Start `wiki-improvement-plan.md` and `open-questions.md` on day 1**, not after 30+ pages. They cost nothing empty and accumulate value as you go.

## Anti-patterns to avoid

- **Don't try to ingest a backlog of 50 sources at once**. The LLM will produce wide, shallow pages. Pace it: one or two per session.
- **Don't write the wiki yourself**. Even a sentence here and there blurs the ownership boundary; the LLM stops feeling responsible for the page's correctness.
- **Don't store ephemeral chat-state as wiki pages**. The wiki is for things future-you needs. If the question is one-off, just answer it.
- **Don't skip `log.md`**. It feels redundant when you remember everything from this week. In two months, when you don't remember, the log is the only thread back.
- **Don't auto-fix during a lint pass without confirmation**. Lint surfaces; user decides.

---

# Closing note

This document is intentionally not domain-specific. The schema in Part 2 is what I converged on for a research-paper-finalization project, but it's a starting point — the right structure for a new vault depends on what you're trying to accomplish there. Adapt freely; the only fixed parts are (a) the three-layer split, (b) the LLM owning the `pages/` layer, and (c) the ingest / query / lint operations.

Share this file with the LLM agent at the start of the new vault and ask it to instantiate a project-specific `SCHEMA.md` that's a delta on top of Part 2. From there, the wiki grows.
