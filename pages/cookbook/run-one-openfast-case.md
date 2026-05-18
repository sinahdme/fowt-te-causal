---
title: "Cookbook — run one OpenFAST case on the IEA-15 UMaineSemi deck"
type: cookbook
created: 2026-05-15
updated: 2026-05-15
sources: []
tags: [cookbook, openfast, turbsim, iea-15, umainsemi, phase-2]
---

End-to-end recipe for launching **one** OpenFAST simulation of the
IEA-15-240-RWT-UMaineSemi reference platform on this Windows setup.
Consolidates every gotcha discovered during 2026-05-13/14 from
`pages/log.md`, the project-input-gotchas memory, and
`sims/run_iea15_single.py`.

If you're scaling up to the DLC matrix, read this first then refactor
the relevant steps into `sims/run_campaign.py` (which adds per-case IDs
and no-clobber output dirs).

## Prerequisites

| Tool | Where | Version | How to invoke |
|---|---|---|---|
| OpenFAST | `miniconda3/envs/openfast_env/Library/bin/openfast.exe` | v4.2.0 (GCC, Jan 2026) | absolute path from any env |
| TurbSim | same dir as above | bundled with openfast_env | absolute path |
| ROSCO DLL | `anaconda3/envs/te-fowt/Lib/site-packages/rosco/lib/libdiscon.dll` | 2.10.1 (pip-installed) | referenced by absolute path in ServoDyn |
| openfast_toolbox | `te-fowt` env | 3.5.1 (editable from `repos/openfast_toolbox`) | `from openfast_io.FAST_output_file import ...` via [[analysis/load_runs.py]] |
| IDTxl + JIDT | `te-fowt` env (.pth bypass) | upstream + Java 11.0.30 | requires `JAVA_HOME` — see [[validation/case-4-sobol-3pt-mooring-ea]] |

The OpenFAST exe does NOT need the `te-fowt` env on PATH — it loads the
ROSCO DLL by absolute path from the `ServoDyn` input file (see gotcha 1).

## Stage the deck

Copy two subdirs from the read-only [[entities/iea-15mw-volturnus-s]]
clone into a per-case working directory:

```python
SRC = PROJECT_ROOT / "repos" / "IEA-15-240-RWT" / "OpenFAST"
shutil.copytree(SRC / "IEA-15-240-RWT",           RUN_DIR / "IEA-15-240-RWT")
shutil.copytree(SRC / "IEA-15-240-RWT-UMaineSemi", RUN_DIR / "IEA-15-240-RWT-UMaineSemi")
```

**Why both subdirs**: the UMaineSemi `.fst` references the sibling
`../IEA-15-240-RWT/` (geometry + airfoils + InflowFile shared with the
land-based reference). Copying just the UMaineSemi subdir leaves dangling
relative paths.

⚠️ **Per-case isolation**: `run_iea15_single.py` does
`if RUN_DIR.exists(): shutil.rmtree(RUN_DIR)` every run. That works for
*one* case but wipes the matrix. The campaign refactor (task #9) must
key `RUN_DIR` by a per-case ID like
`sims/case_dlc-a_v11ms_wcorr_s01/`.

## Gotcha 1 — ServoDyn DLL path

The r-test cases ship `DLL_FileName` as a Linux CI path:

```
"/home/runner/miniconda3/envs/test/lib/libdiscon.so"
```

On Windows this is unloadable; OpenFAST aborts during `SrvD_Init`.
Replace with the absolute Windows path:

```python
sd = RUN_DIR / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi_ServoDyn.dat"
txt = sd.read_text()
ROSCO_DLL = r"C:\Users\kunsanuni3\anaconda3\envs\te-fowt\Lib\site-packages\rosco\lib\libdiscon.dll"
txt = re.sub(r'"/home/runner/[^"]+libdiscon\.so"', f'"{ROSCO_DLL}"', txt, count=1)
sd.write_text(txt)
```

Keep a `.dat.bak` so you can re-stage cleanly. The case-iea15-real run
preserved one as `*_ServoDyn.dat.bak`.

## Gotcha 2 — TurbSim grid must reach z = 15 m (tower base)

The UMaineSemi tower base sits at z = 15 m (platform deck). AeroDyn's
lowest tower node queries InflowWind at that elevation. The default
`wind.inp` from r-test has `HubHt 150` + `GridHeight 260` → grid bottom
at z = 20 m → AeroDyn aborts in `Grid3DField_GetCell: G3D wind array
boundaries violated. Grid too small in Z direction`.

**Fix**: set `GridHeight ≥ 270` (use 280 for margin) and regenerate
`wind.bts`:

```python
grid = max(2 * (ROTOR_DIAM / 2) + 20, ROTOR_DIAM + 20)  # = 260 for 240 m rotor
grid = max(grid, 280.0)                                 # clear z = 15 m base
```

Use the `replace_value` helper from `run_iea15_single.py:134` (handles
quoted-string values like `"6.000 "` correctly).

## Build the TurbSim deck

Starting template: `repos/r-test/glue-codes/fast-farm/ModAmb_3/TurbSim/HighT1.inp`.

Required patches for IEA-15 NTM:

| Key | Value | Why |
|---|---|---|
| `TurbModel` | `"IECKAI"` | Kaimal spectrum, not HighT1's TIMESR |
| `UserFile` | `"unused"` | drop the time-series input file |
| `IECstandard` | `1` | IEC 61400-1 |
| `IECturbc` | `"B"` | Normal-turbulence class B |
| `IEC_WindType` | `"NTM"` | Normal Turbulence Model |
| `WindProfileType` | `"PL"` | power-law shear |
| `NumGrid_Z`, `NumGrid_Y` | `31` | 31×31 grid (default sufficient) |
| `TimeStep` | `0.05` | 20 Hz output (matches OpenFAST DT_Out) |
| `AnalysisTime` | TMax + 60 s margin | TurbSim's grid must outlive OpenFAST's run |
| `HubHt`, `RefHt` | `150.0` | IEA-15 hub elevation |
| `URef` | mean wind (e.g. `11.00`) | DLC-specific |
| `GridHeight`, `GridWidth` | ≥ 280 | gotcha 2 |

Run:

```python
subprocess.run([str(TURBSIM_EXE), "wind.inp"], cwd=RUN_DIR, capture_output=True, text=True)
```

A successful run produces `wind.bts` (~110 MB for 360 s at 20 Hz with
31×31 grid). `turbsim.log` ends with `TurbSim terminated normally`.

## Patch InflowWind

The UMaineSemi `.fst` runs OpenFAST with **cwd = the UMaineSemi subdir**
(because `cwd=str(fst.parent)` in the `subprocess.run` call). So the
`.bts` path written into `IEA-15-240-RWT_InflowFile.dat` must climb out
one level:

```python
inflow = RUN_DIR / "IEA-15-240-RWT" / "IEA-15-240-RWT_InflowFile.dat"
txt = inflow.read_text()
txt = re.sub(r"^\s*1(\s+WindType\b)", r"3\1", txt, count=1, flags=re.M)
txt = re.sub(r'"none"(\s+FileName_BTS\b)', '"../wind.bts"\\1', txt, count=1)
inflow.write_text(txt)
```

`WindType=3` = TurbSim binary full-field. `WindType=1` (steady) is the
deck's default.

## Patch .fst

```python
fst = RUN_DIR / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.fst"
txt = fst.read_text()
txt = re.sub(r"^\s*\S+(\s+TMax\b)",      f"{TMAX}\\1", txt, count=1, flags=re.M)
txt = re.sub(r"^\s*\S+(\s+OutFileFmt\b)", r"2\1",      txt, count=1, flags=re.M)
fst.write_text(txt)
```

`OutFileFmt=2` writes `.outb` only (binary, ~22 MB for 300 s × 930
channels). Saves disk vs `OutFileFmt=1` (`.out` plus a duplicate `.outb`).

## Invoke OpenFAST

```python
log = RUN_DIR / "openfast.log"
with log.open("w") as lf:
    subprocess.run([str(OPENFAST_EXE), fst.name],
                   cwd=str(fst.parent),
                   stdout=lf, stderr=subprocess.STDOUT)
```

**cwd must be the .fst's directory** — OpenFAST resolves every input
sub-file (ElastoDyn, HydroDyn, etc.) relative to the .fst location. If
you cd up one level, all the inner `.dat` references break.

Successful run prints `OpenFAST terminated normally` near the end of
`openfast.log`. The output `.outb` lands at
`<fst>.with_suffix(".outb")`.

**Performance**: 300 s sim ≈ 2.3 min wall on this machine (single core,
single-precision build). Time ratio sim/CPU ≈ 2.4×. Phase 2 DLC matrix
at TMax=3600 s ≈ 27 min/case × 24 cases = ~11 h serial (parallelise).

## Parse the .outb

```python
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
from load_runs import load_outb, find_time_column

df = load_outb(outb_path)                  # pandas DataFrame, units-suffixed cols
t_col = find_time_column(df)               # finds "Time_[s]"
```

[[analysis/load_runs.py]] handles two openfast_toolbox/NumPy-2 quirks
internally: `use_buffer=True` to bypass a broadcast bug, and the
`find_time_column` helper for the `Time_[s]` column-name convention.

## Common failure modes

| Error / symptom | Probable cause | Fix |
|---|---|---|
| `SrvD_Init` aborts with `libdiscon.so` path | Gotcha 1 — Linux DLL path | Replace ServoDyn `DLL_FileName` |
| `Grid3DField_GetCell: G3D wind array boundaries violated. Grid too small in Z direction` | Gotcha 2 — GridHeight too small | Set `GridHeight ≥ 270` in TurbSim, regenerate `.bts` |
| `IfW_FlowField_GetVelAcc` failure during AeroDyn init | Same as above | Same fix |
| TurbSim fails with cryptic spectrum error | `TurbModel` left as TIMESR/USRTimeSeries | Switch to `"IECKAI"` |
| Inner `.dat` file not found | wrong `cwd` for subprocess | cwd must be `fst.parent` |
| OpenFAST hangs at t = 0.1 | ROSCO DLL loaded but `DISCON.IN` malformed | Check `*_DISCON.IN` consistency |
| `JVMNotFoundException` when running TE downstream | `JAVA_HOME` unset for direct env-python invocation | `JAVA_HOME=…/te-fowt/Library/lib/jvm python script.py` |

## Phase 2 hooks (when refactoring into `run_campaign.py`)

1. **Per-case ID**: build from the DLC tuple `(dlc, wind_speed_ms, wave_mode, seed)`. Example: `dlca_v11ms_wcorr_s01`. Use as `RUN_DIR.name`.
2. **No-clobber**: skip a case if its `.outb` already exists at the expected path.
3. **Env-var paths**: replace the hardcoded `OPENFAST_EXE` / `TURBSIM_EXE` / `ROSCO_DLL` constants with env-var reads that fall back to the current absolute paths.
4. **Parallelism**: each case is fully independent — use `concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()-1)`. OpenFAST is single-threaded so the parallelism is across cases.
5. **TMax + transient drop**: production runs use `TMax = 3600 s` and drop the first 600 s. Predecessor-DLC1.6 cross-comparability runs use `TMax = 730 s` with first 100 s dropped (per [[sources/jeon-2025]]).
6. **TurbSim seeds**: use the DLC's seed index to set `RandSeed1` (replace the hard-coded `4433456` in the template).
7. **JONSWAP via HydroDyn**: the UMaineSemi `.fst` uses WAMIT for first-order kinematics; irregular waves are configured in `SeaState.dat` / `HydroDyn.dat`. For DLC-A correlated wave-wind: derive Hs, Tp from wind speed via the predecessor's lookup (or per IEC 61400-3). For DLC-B: same Hs/Tp but independent seed → set wave seed independently.

## Related

- [[validation/case-3-iea15-single-case-te]] — first end-to-end run + TE
- [[entities/iea-15mw-volturnus-s]] · [[entities/openfast]] ·
  [[entities/turbsim]] · [[entities/rosco]]
- [[PLAN]] Phase 2 — DLC matrix definitions
- [[sources/jeon-2025]] — predecessor's DLC1.6 parameters
