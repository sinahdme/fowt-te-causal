---
title: "Wiki Schema — FOWT Causal Effect via Transfer Entropy"
type: schema
created: 2026-05-12
updated: 2026-05-12
tags: [meta, schema]
---

# Wiki Schema — FOWT Causal Effect via Transfer Entropy

This is the **domain-specific delta** on top of [[LLM_Wiki_Pattern]] (Part 2).
The LLM owns `pages/`. The user owns `raw/`. This file is co-evolved.

## Domain

- **Project**: quantify causal drivers of floating offshore wind turbine
  (FOWT) structural response.
- **Methods**: Transfer Entropy (IDTxl, KSG) for time-series environmental
  forcing; Sobol sensitivity + Mutual Information (SALib + IDTxl) for
  structural design parameters.
- **Reference platform**: IEA-15MW UMaine VolturnUS-S semisubmersible (locked).
- **User**: FOWT researcher (see `../.claude` memory).
- **Success**: a combined causal graph + per-response narrative published as
  a report, plus a navigable Obsidian vault for the OpenFAST ecosystem.

## Three-layer split (recap)

Updated 2026-05-15: vault was flattened — every working dir now sits
inside the vault root (`D:\Causal Effect with transfer entropy\wiki-transfer entropy\`).
There is no longer an "external" tier; everything is reachable from
vault-relative paths.

| Layer | Path (vault-relative) | Owner | Mutability |
|---|---|---|---|
| Raw — small | `raw/` | User | Immutable (LLM reads only) |
| Raw — vendored | `repos/` (~2.5 GB git clones) | User | Immutable (LLM reads only) |
| Generated — sims | `sims/` (OpenFAST `.out`/`.outb`) | Simulator | Append-only per case |
| Generated — data | `data/` (cleaned Parquet) | Analysis | Regeneratable from sims |
| Code | `analysis/`, `sims/run_*.py` | LLM + User | Versioned via git (when set up) |
| Pages | `pages/` | LLM | LLM-owned, evolves |
| Reports | `reports/` | LLM | Generated from pages + data |
| Schema | `SCHEMA.md`, `LLM_Wiki_Pattern.md` | Shared | Co-evolved |

**Obsidian indexing trade-off**: `repos/` at 2.5 GB and `sims/` at 124 MB
will slow Obsidian's graph view, file search, and tag indexing if let in.
The user opted to let Obsidian index everything; if it becomes painful,
exclude `repos/`, `sims/`, `data/` via Settings → Files & Links → Excluded
files. Files stay on disk and scripts still reach them; only the indexer
ignores them.

`analysis/build_vault.py` continues to write pandoc-converted MD copies
of OpenFAST RST docs under `raw/extracts/openfast-docs/` — those are
inside the user-owned `raw/` tier, distinct from the vendored `repos/`
clone they were derived from.

## Subfolder semantics for this project

### `pages/sources/`
One file per ingested *external* source (paper, technical report, dataset,
software docs page worth its own citation). Filename = citation key.
- Examples we expect to ingest: `schreiber-2000.md` (original TE paper),
  `kraskov-2004.md` (KSG estimator), `iea-task37-2020.md` (IEA-15MW reference),
  `allen-2020.md` (VolturnUS-S report), `jonkman-2007.md` (FAST docs).

### `pages/papers/`
Deep analytical companion for the small subset of references central to the
project. We expect 3–5: the original TE paper, the KSG paper, the IEA-15MW
reference, the VolturnUS-S design report, the IDTxl methods paper.

### `pages/concepts/`
Definable ideas. For us:
- Information-theoretic: transfer-entropy, mutual-information, ksg-estimator,
  surrogate-significance, conditional-transfer-entropy, time-delay-embedding,
  effect-size-normalisation.
- Statistical: sobol-sensitivity, saltelli-sampling, latin-hypercube-sampling,
  stationarity-adf-test.
- FOWT physics: jonswap-spectrum, blade-element-momentum, morison-equation,
  catenary-mooring, design-load-case, damage-equivalent-load.

### `pages/entities/`
Named things — physical, software, organisational. For us:
- OpenFAST modules: `openfast-aerodyn`, `openfast-hydrodyn`,
  `openfast-elastodyn`, `openfast-beamdyn`, `openfast-servodyn`,
  `openfast-moordyn`, `openfast-inflowwind`, `openfast-subdyn`,
  `openfast-overview`.
- Reference platforms: `iea-15mw-volturnus-s`, `oc4-deepcwind`, `oc3-hywind`.
- Software: `idtxl`, `salib`, `openfast-toolbox`, `rosco`, `moorpy`, `weis`,
  `turbsim`, `openfast` (the solver itself).
- OpenFAST output channels: `channel-ptfmpitch`, `channel-wind1velx`, etc.
  *Only* create a channel entity once the user locks the response-channel
  list (see `pages/open-questions.md`).

### `pages/equations/`
Filename pattern `eq-<name>.md`. Each page: statement, symbol legend, units,
where used, link to source citation. Initial set:
`eq-transfer-entropy`, `eq-mutual-information`, `eq-sobol-first-order`,
`eq-sobol-total`, `eq-jonswap-spectrum`, `eq-morison`, `eq-blade-element-momentum`.

### `pages/validation/`
The verification checklist from [[PLAN]] "Verification" section:
- `case-1-r-test-parse.md` — confirm `openfast_toolbox` reads r-test output
- `case-2-ar1-te-recovery.md` — known-answer synthetic TE test
- `case-3-iea15-single-case-te.md` — one IEA-15MW case, end-to-end TE
- `case-4-sobol-3pt-mooring-ea.md` — 3-point Sobol on mooring `EA`

### `pages/analyses/`
Filed-back query answers. Each file: `<topic>-YYYY-MM-DD.md`. Examples we
*expect* to produce:
- `wind-vs-wave-conditional-te-<date>.md`
- `mooring-stiffness-sobol-ranking-<date>.md`
- `controller-gain-mi-influence-<date>.md`

## Citation key convention

`<first-author-lastname>-<year>` lowercase, hyphenated. Multi-author: first
author only. Disambiguate same-author/same-year with a suffix letter:
`jonkman-2010a`, `jonkman-2010b`.

## Link path convention

**Always use folder-prefixed wikilinks**, never bare:

- Good: `[[entities/openfast-aerodyn]]`, `[[concepts/transfer-entropy]]`
- Bad: `[[openfast-aerodyn]]`, `[[Transfer Entropy]]`

The relative path is from `wiki/pages/`. Inside a page in
`wiki/pages/entities/`, link as `[[concepts/transfer-entropy]]` (Obsidian
resolves; portable to other Markdown tools that index by basename).

## Frontmatter — required keys

```yaml
---
title: "Human-readable title"
type: source | paper | concept | entity | equation | validation | analysis | overview | index | log | schema
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["citation-key-1"]   # citation keys this page draws on (may be empty)
tags: [domain-tag, ...]
---
```

Additional keys per type — see Part 2 of [[LLM_Wiki_Pattern]].

## Channel-naming convention

OpenFAST output channels are written in **CamelCase** in input decks
(`PtfmPitch`, `Wind1VelX`). On wiki pages we keep the CamelCase form when
referring to the channel name, but the entity filename uses kebab-case with
a `channel-` prefix: `entities/channel-ptfm-pitch.md`. Inside the page body
we write the OpenFAST canonical name in backticks: `` `PtfmPitch` ``.

## Workflows — project-specific notes

### Ingest
- For OpenFAST RST docs ingested via `analysis/build_vault.py`:
  put the converted MD under `raw/extracts/openfast-docs/` and create one
  `entities/openfast-<module>.md` page per module **only if it doesn't
  already exist**. Update existing pages rather than overwriting.

### Query
- TE questions: start at `pages/concepts/transfer-entropy.md` →
  `pages/concepts/conditional-transfer-entropy.md` →
  `pages/validation/case-*-te-*.md`.
- Sensitivity questions: start at `pages/concepts/sobol-sensitivity.md` →
  `pages/concepts/mutual-information.md`.

### Lint
- Watch for **channel pages drifting from PLAN.md**. Whenever the user
  locks new channels, add to `pages/entities/channel-*.md` *and* note in
  `pages/log.md`.

## Open structural items

Tracked in `pages/open-questions.md`:
1. Response-channel list (blocking Phase 2 simulation).
2. Structural parameter sweep list with ranges (blocking Phase 5).

## Conventions specific to this domain

- All physical quantities carry SI units in equation pages and in
  channel-entity pages.
- For OpenFAST-internal sign conventions, link to the relevant OpenFAST
  module entity (which mirrors the OpenFAST documentation).
- Plots are stored in `raw/figures/` (manual) or `reports/figs/` (script-
  generated). Wiki pages reference them by relative path; never embed
  binary blobs in markdown.
