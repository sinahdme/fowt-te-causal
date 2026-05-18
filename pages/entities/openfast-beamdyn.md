---
title: "OpenFAST BeamDyn"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, structure, blade]
---

## What it is

Geometrically nonlinear blade structural model based on Legendre spectral
finite elements (LSFEs). Used as an alternative to ElastoDyn's modal blade
model when large blade deflections matter — relevant for the long, slender
[[entities/iea-15mw-volturnus-s]] blades.

- Source: `../../../repos/openfast/modules/beamdyn/`
- Input file: `BeamDyn.dat` (per blade)

## Properties / parameters

| Parameter | Role |
|---|---|
| `order_elem` | Polynomial order of the LSFE |
| `member_total` | Number of beam members |
| Stiffness / mass matrices per station | 6×6 per blade station |

The IEA-15MW reference deck uses BeamDyn for the blades by default; switch
to ElastoDyn-only if a fast-running smoke test is needed.

## TE relevance

- Provides blade-root and blade-span loads to [[entities/openfast-elastodyn]].
- TE targets typically taken from ElastoDyn output channels rather than
  BeamDyn-internal nodes.

## Appears in

- [[entities/openfast-overview]] · [[entities/openfast-elastodyn]] ·
  [[entities/openfast-aerodyn]]

## Sources

- *(to ingest)* OpenFAST BeamDyn manual
