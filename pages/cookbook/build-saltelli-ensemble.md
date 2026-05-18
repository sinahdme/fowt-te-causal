---
title: "Cookbook — build a Saltelli ensemble over the 9 Phase 5 variables"
type: cookbook
created: 2026-05-15
updated: 2026-05-15
sources: ["jeon-2025"]
tags: [cookbook, raft, sobol, salib, phase-5, sensitivity]
---

End-to-end recipe for running a Saltelli sample-driven RAFT ensemble
over the 9 locked Phase 5 design variables, computing Sobol-`S1`/`ST`
per response, and saving results to parquet. Pulls from
[[PLAN]] Phase 5 (variable list + bounds + constraint policy),
`analysis/case4_sobol_ea.py` (RAFT driver template), `sims/run_raft_lhs.py`
(v1 smoke test), and the three Windows gotchas surfaced 2026-05-13.

If you're scaling v1 (4 vars, N=8) up to v2 production (9 vars, N=64 or
larger), read this first then refactor.

## Prerequisites

| Tool | Where | How to invoke |
|---|---|---|
| RAFT | `te-fowt` env, via `repos/WEIS` editable install | `import raft; raft.Model(design)` |
| MoorPy | `te-fowt` env (installed by WEIS) | called internally by RAFT |
| SALib | `te-fowt` env | `from SALib.sample import saltelli` |
| JIDT (Java) | `anaconda3/envs/te-fowt/Library/lib/jvm/` | only needed if pipeline also runs IDTxl downstream |
| Source YAML | `repos/WEIS/examples/00_setup/ref_turbines/IEA-15-240-RWT_VolturnUS-S_raft.yaml` | starting design for every Saltelli row |

`top-level import weis` fails because `pyOpenFAST` isn't installed, but
`import raft` works standalone — which is all we need for Phase 5.

## The 9 design variables (locked 2026-05-13)

| # | Symbol | Where it lives in the YAML | −20 % | Baseline (IEA-15) | +20 % |
|---|---|---|---|---|---|
| 1 | `D_MCol` | `platform.members[main_column].d` (list, replicate per joint) | 8.00 m | 10.00 m | 12.00 m |
| 2 | `D_OCol` | `platform.members[offset_col_{2,3,4}].d` (list × 3 members) | 10.00 m | 12.50 m | 15.00 m |
| 3 | `R_MO` | offset-column member `joint1`/`joint2` radial coordinates × 3 | 41.40 m | 51.75 m | 62.10 m |
| 4 | `D_Pt` | pontoon member `d` × 3 + `H_Pt`-dependent joint z | 7.692 m | 9.6148 m | 11.538 m |
| 5 | `H_Pt` | pontoon-top joint `z`; couples with `D_Pt` | 5.60 m | 7.00 m | 8.40 m |
| 6 | `H_FB` | platform top elevation `z`; shifts main + offset top joints | 12.00 m | 15.00 m | 18.00 m |
| 7 | `H_Draft` | platform bottom joints `z` (sign flip; draft = negative z) | 16.00 m | 20.00 m | 24.00 m |
| 8 | `EA` | `mooring.line_types[main].stiffness` | 2.616 × 10⁹ N | 3.27 × 10⁹ N | 3.924 × 10⁹ N |
| 9 | `L_u` | `mooring.lines[*].length` (all 3 lines) | 680 m | 850 m | 1020 m |

**v1 (smoke test, `sims/run_raft_lhs.py`) covers only vars 1, 2, 8, 9** —
the ones with single-line YAML edits. Vars 3-7 (geometry coordinates)
require multi-joint coordinate updates and are deferred to v2.

## Geometric infeasibility — flag, don't reject

The predecessor [[sources/jeon-2025]] uses three constraints:

```
D_OCol > D_Pt          # offset column wider than its pontoon
H_Pt   > 0.5 * D_Pt    # pontoon clear of column base
H_Draft > 0.5 * D_Pt + H_Pt   # draft clears pontoon + column base
```

Some Saltelli samples in the ±20 % box violate these (e.g.
`D_OCol = 10` (min) and `D_Pt = 11.538` (max) violates the first).

**Policy** (matches predecessor's reward = −100 treatment):
1. Evaluate **every** sample in the Saltelli sequence — SALib's analyser
   requires the complete sequence in order.
2. Mark constraint-violating samples as `feasible=False` with a reason
   string.
3. Compute Sobol-`S1`/`ST` over the **feasible subset only**.
4. Report `n_feasible / n_total` as a diagnostic alongside the indices.

Code skeleton:

```python
def feasibility(sample: dict) -> tuple[bool, str]:
    if sample["D_OCol"] <= sample["D_Pt"]: return False, "D_OCol <= D_Pt"
    if sample["H_Pt"]   <= 0.5 * sample["D_Pt"]: return False, "H_Pt <= 0.5*D_Pt"
    if sample["H_Draft"] <= 0.5 * sample["D_Pt"] + sample["H_Pt"]:
        return False, "H_Draft <= 0.5*D_Pt + H_Pt"
    return True, ""
```

## Gotcha 1 — RAFT YAML `member.type` coercion

The WEIS-bundled IEA-15 RAFT YAML uses **integer** `type` fields (older
schema). Standalone RAFT 2.0.4 expects `'rigid'` or `'beam'`. Without
coercion you get `AttributeError: 'int' object has no attribute 'lower'`
deep in RAFT's member init.

Recursive shim (lifts from [[validation/case-4-sobol-3pt-mooring-ea]]):

```python
def coerce_to_rigid(obj):
    if isinstance(obj, dict):
        if "type" in obj and not isinstance(obj["type"], str):
            obj["type"] = "rigid"
        for v in obj.values():
            coerce_to_rigid(v)
    elif isinstance(obj, list):
        for v in obj:
            coerce_to_rigid(v)

coerce_to_rigid(design["platform"])
if "turbine" in design and "tower" in design["turbine"]:
    coerce_to_rigid(design["turbine"]["tower"])
```

All-rigid is fine for frequency-domain hydro screening — surge/heave
responses are dominated by hydro + mooring, not platform structural
flexibility.

Also set `member.potMod = False` on every platform member: forces RAFT
to use strip-theory hydrodynamics on the geometry we just edited
(WAMIT `.hst/.1/.3` files are pre-meshed for the baseline geometry and
won't reflect the perturbations).

## Gotcha 2 — MoorPy UTF-8 / cp949 on Korean Windows

MoorPy reads bundled mooring config YAMLs via Python's default `open()`.
On Korean Windows the system codepage is cp949, and MoorPy chokes on
the UTF-8 BOM in its own bundled files.

**Fix**: set `PYTHONUTF8=1` at the top of `main()`:

```python
os.environ.setdefault("PYTHONUTF8", "1")
```

This affects the current process's default file encoding to UTF-8 and
also propagates to child processes via env inheritance.

## Gotcha 3 — `JAVA_HOME` for direct env-python invocation

Only relevant if your driver also runs IDTxl downstream. JIDT's
`startJVM()` searches via `jpype._jvmfinder.getDefaultJVMPath()`,
which on Windows looks at the `JAVA_HOME` env var. If you invoke
`anaconda3/envs/te-fowt/python.exe` directly (not via `conda activate`
or `conda run`), `JAVA_HOME` is unset.

In **bash** (and the Claude Code Bash tool):

```bash
JAVA_HOME="C:/Users/kunsanuni3/anaconda3/envs/te-fowt/Library/lib/jvm" PYTHONUTF8=1 python script.py
```

In **PowerShell**:

```powershell
$env:JAVA_HOME = 'C:\Users\kunsanuni3\anaconda3\envs\te-fowt\Library\lib\jvm'
$env:PYTHONUTF8 = '1'
python script.py
```

cmd.exe `set X=Y` does NOT work in the bash tool; PowerShell needs
`$env:VAR =`. Easy to get wrong; documented per
[[validation/case-4-sobol-3pt-mooring-ea]].

## SALib — order of operations

Saltelli + Sobol is a **specific sampling/analyser pair** — you cannot
analyse a sub-sample or a re-ordered subset. The Y vector passed to
`sobol.analyze` must correspond row-for-row to the X matrix from
`saltelli.sample`.

```python
from SALib.sample import saltelli
from SALib.analyze import sobol

problem = {
    "num_vars": 9,
    "names":  ["D_MCol", "D_OCol", "R_MO", "D_Pt", "H_Pt", "H_FB", "H_Draft", "EA", "L_u"],
    "bounds": [[8.0, 12.0], [10.0, 15.0], [41.4, 62.1], [7.692, 11.538],
               [5.6, 8.4], [12.0, 18.0], [16.0, 24.0],
               [2.616e9, 3.924e9], [680.0, 1020.0]],
}

N = 64  # base sample size; total evals = N * (D + 2) = 64 * 11 = 704
samples = saltelli.sample(problem, N, calc_second_order=False)

# Y must come out in the SAME order as samples; do NOT shuffle.
Y_per_response = {resp: np.full(len(samples), np.nan) for resp in RESPONSE_KEYS}

for i, row in enumerate(samples):
    sample_dict = dict(zip(problem["names"], row))
    ok, reason = feasibility(sample_dict)
    if not ok:
        # leave NaN; track feasibility separately
        continue
    stats = run_one_design(row)
    for resp in RESPONSE_KEYS:
        Y_per_response[resp][i] = stats[resp]

# Sobol requires the full vector with no missing entries.
# Options for handling infeasible:
#   (a) impute infeasible Y with median of feasible (biases indices toward 0)
#   (b) drop only when computing per-response (NOT supported by SALib for Saltelli)
#   (c) re-sample replacements (rerun Saltelli with different seed; slow)
# We use (a) for v1, document the n_feasible/n_total in the parquet.
for resp, y in Y_per_response.items():
    nan_mask = np.isnan(y)
    if nan_mask.any():
        y[nan_mask] = np.nanmedian(y)
    indices = sobol.analyze(problem, y, calc_second_order=False, print_to_console=False)
```

`calc_second_order=False` keeps the budget at `N * (D + 2)` evals
(704 here). Set to `True` only if you need pairwise interactions —
budget jumps to `N * (2D + 2) = 1280`.

## Output parquet schema

One row per Saltelli sample, with `sample_id` preserved for order. Suggested columns:

| Column | Type | Notes |
|---|---|---|
| `sample_id` | int | Saltelli row index (0…N*(D+2)-1) |
| `feasible` | bool | passes the 3 geometric constraints |
| `infeasible_reason` | str | empty if feasible |
| `D_MCol` … `L_u` | float | the 9 variable values |
| `runtime_s` | float | per-design RAFT wall time |
| `surge_avg`, `surge_std`, … | float | per-DOF stats from `model.results['case_metrics']` |
| `Tmoor_avg_0`, `Tmoor_std_0` … | float | mooring line tensions if RAFT exposes them |
| `error` | str | exception message if `run_one_design` raised |

Save with `compression='zstd'` (faster + smaller than snappy for these
sparse tables).

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `Nan detected in response vector Xi` | RAFT couldn't converge for that geometry (eigensolve / mooring static failure) | Catch the exception; flag as infeasible-by-numerics; impute Y with median for Sobol |
| `'int' object has no attribute 'lower'` | Gotcha 1 — `member.type` integer | Run `coerce_to_rigid()` on the design dict |
| `UnicodeDecodeError: 'cp949'` | Gotcha 2 — MoorPy reading UTF-8 with cp949 | `PYTHONUTF8=1` |
| `JVMNotFoundException` | Gotcha 3 — `JAVA_HOME` unset | Set inline as shown above |
| Sobol-`ST` close to 0 for all variables | Response too noisy / variance dominated by infeasible imputation | Increase N; verify n_feasible / n_total > 0.7 |
| `surge_std` barely changes with `EA` | RAFT `min_freq = 0.0159 Hz` is above the surge eigenfrequency (~0.008 Hz) | Either widen `min_freq` in the YAML's `settings` block, or use `surge_avg` (static offset) as the EA-sensitive response |

## Phase 5 production hooks (when refactoring v1 → v2)

1. **N via CLI**: `argparse --N 64` (default 8 = smoke-test budget).
2. **Per-eval checkpoint**: after every successful `run_one_design`,
   append the row to a partial parquet at
   `data/raft_lhs_partial.parquet`. Resume by reading partial, skipping
   any `sample_id` already present.
3. **Parallelism**: `concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()-1)`.
   Each RAFT call is single-threaded and ~10 s; embarrassingly parallel.
   ⚠️ JVM startup (~1 s) happens per process — amortise by submitting
   batches of ~20 designs per worker if using a pool.
4. **Load-case restriction**: the bundled YAML has 26 load cases. For
   v1, restrict to 1 case (DLC1.6 equivalent at V=11 m/s, JONSWAP
   Hs=8.3 Tp=12.95) so wall time stays manageable. v2 can use the full
   26.
5. **Constraint violations**: log to a separate
   `data/raft_lhs_infeasible.csv` for the publication appendix —
   reviewers will ask what fraction of the design space was excluded.
6. **Sobol confidence intervals**: SALib returns `S1_conf` / `ST_conf`
   alongside indices — record them. With N=64 the CIs are ±0.05; for
   publication-quality narrow CIs go to N ≥ 256 (eval budget × 4).

## Related

- [[validation/case-4-sobol-3pt-mooring-ea]] — smoke-test that
  validated the RAFT driver pipeline
- [[entities/raft]] · [[entities/salib]] · [[entities/moorpy]]
- [[entities/iea-15mw-volturnus-s]] §"Substructure geometry" and
  §"Mooring properties" — baselines + provenance
- [[PLAN]] Phase 5 — variable list, bounds, constraint policy
- [[sources/jeon-2025]] — predecessor 7-var optimisation + Case_03 trade-off
- [[concepts/sobol-sensitivity]] — what the indices mean
