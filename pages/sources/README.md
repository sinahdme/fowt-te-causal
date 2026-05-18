---
title: "Sources — README"
type: index
created: 2026-05-12
updated: 2026-05-12
tags: [meta, readme]
---

# Sources

One markdown file per ingested raw source. Filename = citation key
(lowercase, hyphenated; see [[SCHEMA]] §"Citation key convention").

## Template

```yaml
---
title: "Source — <full short title>"
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_path: "raw/papers/<filename>.pdf"
authors: ["Lastname, F.", ...]
year: 2024
venue: "Journal name"
doi: "10.xxxx/yyyy"
citation_key: "lastname-2024"
tags: [...]
---

## Citation
<full bibliographic citation>

## TL;DR
- ...

## Key claims
- Claim with [[concepts/<link>]]

## Equations introduced
- [[equations/eq-<name>]]

## Methods
...

## Data / cases
...

## How it informs this project
...

## Open questions / contradictions
...
```

Source pages are **created on ingest** (workflow in [[SCHEMA]]).
Currently empty. Anticipated first batch listed in `../../raw/papers/README.md`.

## Related

- [[index]]
- [[../../SCHEMA]]
