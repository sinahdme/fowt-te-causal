---
title: "Analyses — README"
type: index
created: 2026-05-12
updated: 2026-05-12
tags: [meta, readme]
---

# Analyses

Filed-back query answers. One file per substantive question that's been
answered with synthesis. Filename: `<topic>-<YYYY-MM-DD>.md`.

## When to file a query as an analysis page

After the LLM answers a question, ask yourself: "Would I want to find this
answer again in three months?" If yes, file it. If it's a one-off lookup,
don't.

## Template

```yaml
---
title: "<Question summary>"
type: analysis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["source-key", ...]
tags: [...]
---

## Question
<what was asked>

## Hypothesis
<what we expected, if applicable>

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
- [[concepts/...]]
- [[validation/...]]
```

Anticipated first analyses (after Phase 4/5 kicks off):

- `wind-vs-wave-conditional-te-<date>.md`
- `mooring-stiffness-sobol-ranking-<date>.md`
- `controller-gain-mi-influence-<date>.md`

## Related

- [[index]] · [[../../SCHEMA]]
