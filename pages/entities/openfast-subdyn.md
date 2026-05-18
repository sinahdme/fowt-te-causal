---
title: "OpenFAST SubDyn"
type: entity
created: 2026-05-12
updated: 2026-05-12
sources: []
tags: [openfast, module, structure]
---

## What it is

Linear finite-element substructure dynamics. Designed for fixed-bottom
support structures (jackets, monopiles). For a **floating** platform like
[[entities/iea-15mw-volturnus-s]] the platform is treated as a rigid body in
[[entities/openfast-elastodyn]], so SubDyn is typically **inactive**.

- Source: `../../../repos/openfast/modules/subdyn/`
- Input file: `SubDyn.dat`

## Status in this project

Inactive in our IEA-15MW VolturnUS-S configuration. Page exists for
completeness of the OpenFAST module catalogue.

## Appears in

- [[entities/openfast-overview]]

## Sources

- *(to ingest)* OpenFAST SubDyn manual
