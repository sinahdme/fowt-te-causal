---
title: "openfast_toolbox (pyFAST)"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [software, python, openfast]
---

## What it is

NREL's Python toolbox for reading and writing OpenFAST input / output files,
post-processing time series, and templating cases. Formerly known as
`pyFAST`.

- Repo: `../../../repos/openfast_toolbox/`
- pip: `pip install openfast_toolbox`

## Role in this project

The **`.out` / `.outb` reader** for Phase 3 data extraction. Used to:

- Parse binary OpenFAST output via `openfast_toolbox.io.FASTOutputFile`
- Convert to pandas `DataFrame`
- Optionally template input decks (we may layer Jinja2 on top instead).

## Appears in

- [[validation/case-1-r-test-parse]] — first parsing smoke test
- Phase 3 of [[PLAN]]

## Sources

- *(no separate citation — toolbox docs in repo)*
