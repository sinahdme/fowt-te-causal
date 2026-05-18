# raw/data/

Curated reference datasets (CSV / MAT / XLSX / JSON).

## Out-of-scope

| Generated artefact | Lives at |
|---|---|
| OpenFAST run outputs (`.out`, `.outb`) | `../../../sims/` |
| Cleaned per-run Parquet time series | `../../../data/` |
| Aggregated KPI tables from Phase 4/5 | `../../../reports/` |

The wiki references those by relative path; they do not get duplicated
under `raw/data/`.

## What does belong here

- Experimental measurements (e.g., wave-tank data, field measurements)
- Externally-published validation tables (e.g., reference DEL values for
  the IEA-15MW)
- Manually curated lookup tables
