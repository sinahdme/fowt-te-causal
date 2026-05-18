---
title: "WEIS"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [software, python, optimization]
---

## What it is

Wind Energy with Integrated Servo-control — NREL's optimization framework
that wraps WISDEM, OpenFAST, and ROSCO into a single co-design pipeline.

- Repo: `../../../repos/WEIS/`
- Docs: in-repo

## Role in this project

**Optional driver** for the Phase 2 simulation campaign. The
`weis.aeroelasticse` subpackage already templates and parallelises OpenFAST
runs — if its dependency footprint is acceptable we will reuse it; otherwise
we will write a thin Jinja2 templating layer ourselves (see [[PLAN]]
Phase 2).

## Decision pending

Whether to take the WEIS dependency for Phase 2. Trade-off:

- **+** Production-tested templating + DLC support.
- **−** Heavy install (WISDEM + OpenMDAO + many BLAS builds on Windows).

Re-evaluate after [[validation/case-1-r-test-parse]] succeeds.

## Appears in

- Phase 2 of [[PLAN]] — campaign driver

## Sources

- *(to ingest)* WEIS GitHub README + Bortolotti et al. systems-engineering papers.
