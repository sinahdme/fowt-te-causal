---
title: "Validation Case 1 — r-test parse smoke test"
type: validation
created: 2026-05-12
updated: 2026-05-13
sources: []
tags: [validation, smoke-test, openfast]
status: PASS
---

## Goal

Confirm that [[entities/openfast-toolbox]] correctly parses an OpenFAST `.outb`
file end-to-end, and that the resulting pandas DataFrame has the expected
columns / dtypes / time grid. This is the first dependency check for the
Phase 3 data pipeline.

## Inputs

- Reference case: **`5MW_Land_BD_DLL_WTurb`** from `../../../repos/r-test/`
  (land-based, fast-running; not the floating reference but ideal as a
  parsing smoke test).
- Tool: `openfast_toolbox.io.FASTOutputFile`.

## Method

1. `openfast.exe` run the case in `repos/r-test/glue-codes/openfast/5MW_Land_BD_DLL_WTurb/`.
   *(r-test ships pre-computed outputs too — using those is acceptable for
   parsing alone; for end-to-end we want our own run.)*
2. Load the resulting `.outb` via `openfast_toolbox.io.FASTOutputFile`.
3. Convert to pandas, write to Parquet.
4. Round-trip read the Parquet and compare numerical values.

## KPI

| KPI | Pass criterion |
|---|---|
| Channel count | matches OutList length in `.fst` |
| Time vector | monotonic, expected `DT_Out` spacing |
| `Time` column | starts at 0, ends at `TMax` |
| Numerical round-trip | max abs diff < 1e-9 between read and re-read |

## Source artefacts (will be filled after run)

- Code: `analysis/load_runs.py`
- Output: `data/case-1-5MW_Land_BD_DLL_WTurb.parquet`

## Status / notes — PASS (2026-05-13)

Executed via `analysis/load_runs.py` on the pre-computed
`.outb` shipped with r-test (no need to re-run OpenFAST for the parse-only test).

Result:
```
Loaded 2001 rows × 67 channels from 5MW_Land_BD_DLL_WTurb.outb
  n_samples: 2001
  n_channels: 67
  time_column: Time_[s]
  t_start: 0.0
  t_end: 20.0
  dt_mean: 0.01           (100 Hz)
  dt_std: 8.88e-16        (machine precision — uniform grid)
  monotonic: True
Wrote data/case-1-5MW_Land_BD_DLL_WTurb.parquet;
  round-trip max abs diff = 0.000e+00
```

All four KPIs pass.

**Implementation notes** (worth keeping for Phase 3):
- `openfast_toolbox.io.FASTOutputFile` had a NumPy 2.x broadcast bug
  (line 617 of `fast_output_file.py`: `data − ColOff` where ColOff is
  shape `(Nch, 1)` and data is `(Nt, Nch)`). Workaround: instantiate with
  `use_buffer=True`, which forces the per-column scaling path. Captured
  in `analysis/load_runs.py:load_outb`.
- Column names are `<Name>_[<units>]` (e.g., `Time_[s]`, `Wind1VelX_[m/s]`).
  `analysis/load_runs.py:find_time_column` strips the units suffix to
  identify the time column.

## Related

- [[entities/openfast-toolbox]] · [[entities/openfast]]
- [[validation/case-3-iea15-single-case-te]] — uses the same loader on the
  reference floating case
- Phase 3 of [[PLAN]]
