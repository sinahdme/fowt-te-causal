# raw/extracts/

Plain-text and markdown extractions of binary or non-markdown sources.

## Expected contents

- `<paper-key>.txt` — pdftotext output for each PDF in `../papers/`
- `openfast-docs/` — pandoc-converted markdown of `../../../repos/openfast/docs/source/**/*.rst`
  (will be populated by `../../../analysis/build_vault.py`, not yet run)

## Why this folder exists

PDF text and RST source aren't directly grep-able from inside a markdown
viewer. Extracts let the LLM and the user search the same content through
the same tooling that searches the rest of the wiki.

## Convention

- Extracts mirror the structure of their source.
- Never edit extracts by hand — re-run the extraction script.
- If an extract is wrong (bad OCR, broken table), record the issue on the
  corresponding `pages/sources/<key>.md` under "Open questions" rather than
  patching the extract in place.
