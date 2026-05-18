# raw/

The **immutable raw-source layer** of the wiki. The LLM reads from here but
never modifies anything in this folder. Drop your sources in the
appropriate subfolder and ask the agent to ingest.

## Subfolders

| Folder | What goes here |
|---|---|
| `papers/` | PDF papers and technical reports (TE theory, FOWT references, NREL reports) |
| `manuscripts/` | Drafts you are authoring (project write-up versions) |
| `extracts/` | Plain-text extractions of `papers/` PDFs and `repos/openfast/docs/` RST → MD conversions |
| `data/` | CSV / MAT / XLSX / JSON reference data (e.g., experimental measurements, validation data) |
| `figures/` | PNG / JPG / SVG reference figures (not script-generated — those go in `../../reports/figs/`) |
| `notes/` | Existing markdown notes you bring in from outside the project |

## Out-of-scope for this folder

| Material | Where it actually lives | Why outside `raw/` |
|---|---|---|
| OpenFAST source + docs | `../../repos/openfast/` | 1.6 GB total clone; kept external |
| Other ecosystem repos (ROSCO, WEIS, …) | `../../repos/` | same |
| OpenFAST run outputs (`.out`, `.outb`) | `../../sims/` | generated artefacts, not curated source |
| Cleaned Parquet time series | `../../data/` | derived from `sims/`, not raw |

The wiki references these external paths in `pages/` but never duplicates
their content here.

## Ingest workflow

1. Drop a file into the right subfolder.
2. Tell the agent (Claude Code, Codex, etc.) to ingest it.
3. The agent will produce / update `pages/sources/<key>.md` (and possibly
   `pages/papers/<key>.md`, `pages/concepts/...`, `pages/entities/...`).
4. Append entry to `pages/log.md`.

See [[SCHEMA]] for the project-specific delta and
[[LLM_Wiki_Pattern]] for the full pattern.
