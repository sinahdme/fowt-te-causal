"""
run_campaign.py — Phase 2 DLC matrix runner for IEA-15 UMaineSemi.

Production OpenFAST campaign driver. Replaces the smoke-test
`run_iea15_single.py` with: per-case IDs, no-clobber outputs,
env-var-driven conda paths, parallel pool, per-case TurbSim + HydroDyn
seeds, and skip-if-already-run resume support.

DLC matrix supported (per PLAN.md Phase 2):
  - dlca : NTM at 4 winds (8/11/15/20 m/s) x 6 seeds, JONSWAP correlated.
           Baseline for TE(wind -> resp), TE(wave -> resp).
  - dlcb : Same winds + seeds but decoupled wave seed.
           Conditional-TE validation (Q8 H3 contrast vs A).
  - dlc16: Predecessor-DLC1.6. V=11 m/s x 6 seeds, SSS Hs=8.3 Tp=12.95.
           Cross-comparability with sources/jeon-2025.

Per-case structure:
  sims/<case_id>/                        # case work dir
    IEA-15-240-RWT/                      # shared geometry copy
    IEA-15-240-RWT-UMaineSemi/           # patched per-case deck
      *.fst, *.outb, *.SrvD.sum, ...
    wind.inp, wind.bts                   # per-case TurbSim
    openfast.log, turbsim.log

Resume: if `<case_id>/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb`
exists, the case is skipped. Delete the file (or the whole `<case_id>/` dir)
to force re-run.

Env vars (override hardcoded defaults — see cookbook):
  OPENFAST_EXE  path to openfast.exe (default: te-fowt env)
  TURBSIM_EXE   path to turbsim.exe
  ROSCO_DLL     path to libdiscon.dll
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_OPENFAST = PROJECT_ROOT / "repos" / "IEA-15-240-RWT" / "OpenFAST"
TURBSIM_TEMPLATE = (
    PROJECT_ROOT / "repos" / "r-test" / "glue-codes" / "fast-farm"
    / "ModAmb_3" / "TurbSim" / "HighT1.inp"
)

# Defaults — overridable by env vars (see cookbook)
DEFAULT_OPENFAST_EXE = Path(r"C:\Users\kunsanuni3\miniconda3\envs\openfast_env\Library\bin\openfast.exe")
DEFAULT_TURBSIM_EXE = Path(r"C:\Users\kunsanuni3\miniconda3\envs\openfast_env\Library\bin\turbsim.exe")
DEFAULT_ROSCO_DLL = Path(r"C:\Users\kunsanuni3\anaconda3\envs\te-fowt\Lib\site-packages\rosco\lib\libdiscon.dll")

HUB_HT = 150.0
ROTOR_DIAM = 240.0

# Wave conditions (Hs [m], Tp [s]) per DLC per nominal wind speed.
# DLC-A and DLC-B share the spectrum; they differ only in wave seed.
# Values approximated from joint Hs|V distributions for North-Atlantic wind seas;
# replace with site-specific values for the publication baseline if needed.
DLC_WAVES = {
    "dlca": {8.0: (3.5, 9.0), 11.0: (4.5, 10.0), 15.0: (6.0, 11.0), 20.0: (8.0, 13.0)},
    "dlcb": {8.0: (3.5, 9.0), 11.0: (4.5, 10.0), 15.0: (6.0, 11.0), 20.0: (8.0, 13.0)},
    "dlc16": {11.0: (8.3, 12.95)},
}

# 6 deterministic seeds for reproducibility. Values lifted from
# run_iea15_single.py + 5 additional uncorrelated 7-digit primes.
WIND_SEEDS = [4433456, 8675309, 1234567, 7777777, 9988776, 5544332]


@dataclass(frozen=True)
class Case:
    dlc: str
    wind_ms: float
    seed_idx: int

    @property
    def case_id(self) -> str:
        return f"{self.dlc}_v{int(self.wind_ms):02d}ms_s{self.seed_idx:02d}"

    @property
    def run_dir(self) -> Path:
        return PROJECT_ROOT / "sims" / self.case_id

    @property
    def outb(self) -> Path:
        return self.run_dir / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.outb"

    @property
    def wind_seed(self) -> int:
        return WIND_SEEDS[self.seed_idx]

    @property
    def wave_seed(self) -> int:
        # DLC-B: wave seed XOR'd with the seed_idx mixed with a fixed
        # mask so wave and wind are decoupled but reproducible.
        if self.dlc == "dlcb":
            return (self.wind_seed ^ 0x5A5A5A5A) & 0x7FFFFFFF
        return self.wind_seed  # DLC-A and DLC-16: correlated (same seed)

    @property
    def hs_tp(self) -> tuple[float, float]:
        return DLC_WAVES[self.dlc][self.wind_ms]


# ----------------------------------------------------------------------------
# Per-case staging + patching
# ----------------------------------------------------------------------------

def stage_case(case: Case) -> None:
    """Copy both IEA-15 subdirs into the case work dir. Idempotent: if the
    run_dir already exists with both subdirs, leave it alone (resume support)."""
    case.run_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("IEA-15-240-RWT", "IEA-15-240-RWT-UMaineSemi"):
        dst = case.run_dir / sub
        if not dst.exists():
            shutil.copytree(SRC_OPENFAST / sub, dst)


def _replace_value(text: str, keyword: str, new_value: str) -> str:
    """Replace the value field for `keyword` in a TurbSim-format line.
    Handles both bareword values and double-quoted strings (which may
    contain whitespace, e.g. `"6.000 "`)."""
    pattern = re.compile(rf'^(?:"[^"]*"|\S+)(\s+{keyword}\b)', re.M)
    if not pattern.search(text):
        raise RuntimeError(f"keyword {keyword!r} not found in TurbSim template")
    return pattern.sub(lambda m: f"{new_value}{m.group(1)}", text, count=1)


def write_turbsim_input(case: Case, analysis_time_s: float) -> Path:
    """Build wind.inp by patching r-test's HighT1.inp (known-good template).
    Returns the path to the written wind.inp."""
    # Grid: 31x31, height = max(rotor_diam + 20, 280) to clear z=15 tower base.
    grid = max(ROTOR_DIAM + 20.0, 280.0)
    txt = TURBSIM_TEMPLATE.read_text(encoding="utf-8")
    txt = _replace_value(txt, "TurbModel",       '"IECKAI"')
    txt = _replace_value(txt, "UserFile",        '"unused"')
    txt = _replace_value(txt, "IECstandard",     "1")
    txt = _replace_value(txt, "IECturbc",        '"B"')
    txt = _replace_value(txt, "IEC_WindType",    '"NTM"')
    txt = _replace_value(txt, "WindProfileType", '"PL"')
    txt = _replace_value(txt, "NumGrid_Z",       "31")
    txt = _replace_value(txt, "NumGrid_Y",       "31")
    txt = _replace_value(txt, "TimeStep",        "0.05")
    txt = _replace_value(txt, "AnalysisTime",    f"{analysis_time_s:.1f}")
    txt = _replace_value(txt, "HubHt",           f"{HUB_HT:.1f}")
    txt = _replace_value(txt, "GridHeight",      f"{grid:.1f}")
    txt = _replace_value(txt, "GridWidth",       f"{grid:.1f}")
    txt = _replace_value(txt, "RefHt",           f"{HUB_HT:.1f}")
    txt = _replace_value(txt, "URef",            f"{case.wind_ms:.2f}")
    txt = _replace_value(txt, "RandSeed1",       f"{case.wind_seed}")

    path = case.run_dir / "wind.inp"
    path.write_text(txt, encoding="utf-8")
    return path


def run_turbsim(case: Case, turbsim_exe: Path) -> Path:
    """Run TurbSim from inside the case dir. Returns path to wind.bts."""
    bts = case.run_dir / "wind.bts"
    if bts.exists():
        return bts
    t0 = time.time()
    log = case.run_dir / "turbsim.log"
    with log.open("w") as lf:
        result = subprocess.run(
            [str(turbsim_exe), "wind.inp"],
            cwd=str(case.run_dir),
            stdout=lf, stderr=subprocess.STDOUT,
        )
    dt = time.time() - t0
    if result.returncode != 0 or not bts.exists():
        raise RuntimeError(f"TurbSim failed for {case.case_id} (rc={result.returncode}); see {log}")
    print(f"  [{case.case_id}] TurbSim done in {dt:.1f}s", flush=True)
    return bts


def patch_servodyn(case: Case, rosco_dll: Path) -> None:
    """Cookbook gotcha 1 — replace Linux CI DLL path with Windows ROSCO DLL.
    Uses lambda for the replacement to prevent re.sub from interpreting
    backslashes in the Windows path as regex escapes (e.g. C:\\U... → bad escape)."""
    sd = case.run_dir / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi_ServoDyn.dat"
    txt = sd.read_text(encoding="utf-8")
    repl = f'"{rosco_dll}"'
    new = re.sub(r'"/home/runner/[^"]+libdiscon\.so"', lambda _m: repl, txt, count=1)
    if new == txt and str(rosco_dll) not in txt:
        # Maybe already-patched .so path or different shape — try a broader pattern.
        new = re.sub(r'"[^"]+\.so"(\s+DLL_FileName\b)',
                     lambda m: f'{repl}{m.group(1)}', txt, count=1)
    sd.write_text(new, encoding="utf-8")


def patch_hydrodyn(case: Case) -> None:
    """Set wave seed + Hs/Tp on the HydroDyn / SeaState input file.
    The UMaineSemi deck uses the v4 SeaState module, so JONSWAP params live there."""
    hs, tp = case.hs_tp
    sea = case.run_dir / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi_SeaState.dat"
    if not sea.exists():
        # Older deck variant — fall back to HydroDyn.dat
        sea = case.run_dir / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi_HydroDyn.dat"
    txt = sea.read_text(encoding="utf-8")
    # WaveHs
    txt = re.sub(r"^\s*\S+(\s+WaveHs\b)", f"{hs}\\1", txt, count=1, flags=re.M)
    # WaveTp
    txt = re.sub(r"^\s*\S+(\s+WaveTp\b)", f"{tp}\\1", txt, count=1, flags=re.M)
    # WaveSeed(1) — primary wave random seed. NB: pattern ends with `\)`
    # not `\)\b` because \b requires word/non-word transition; ")" is
    # non-word and the following whitespace is also non-word — no boundary.
    new_txt = re.sub(
        r"^\s*\S+(\s+WaveSeed\(1\))",
        f"{case.wave_seed}\\1", txt, count=1, flags=re.M,
    )
    if new_txt == txt:
        raise RuntimeError(f"patch_hydrodyn: WaveSeed(1) line not matched in {sea.name}")
    txt = new_txt
    sea.write_text(txt, encoding="utf-8")


def patch_inflowwind(case: Case) -> None:
    """Switch WindType to 3 (TurbSim binary FF) and point at wind.bts."""
    inflow = case.run_dir / "IEA-15-240-RWT" / "IEA-15-240-RWT_InflowFile.dat"
    txt = inflow.read_text(encoding="utf-8")
    txt = re.sub(r"^\s*1(\s+WindType\b)", r"3\1", txt, count=1, flags=re.M)
    txt = re.sub(
        r'"none"(\s+FileName_BTS\b)',
        r'"../wind.bts"\1', txt, count=1,
    )
    inflow.write_text(txt, encoding="utf-8")


def patch_fst(case: Case, tmax: float) -> None:
    """Set TMax + OutFileFmt=2 (.outb only)."""
    fst = case.run_dir / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.fst"
    txt = fst.read_text(encoding="utf-8")
    txt = re.sub(r"^\s*\S+(\s+TMax\b)",       f"{tmax}\\1", txt, count=1, flags=re.M)
    txt = re.sub(r"^\s*\S+(\s+OutFileFmt\b)", r"2\1",       txt, count=1, flags=re.M)
    fst.write_text(txt, encoding="utf-8")


def run_openfast(case: Case, openfast_exe: Path) -> Path:
    fst = case.run_dir / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.fst"
    log = case.run_dir / "openfast.log"
    t0 = time.time()
    with log.open("w") as lf:
        result = subprocess.run(
            [str(openfast_exe), fst.name],
            cwd=str(fst.parent),
            stdout=lf, stderr=subprocess.STDOUT,
        )
    dt = time.time() - t0
    outb = fst.with_suffix(".outb")
    if result.returncode != 0 or not outb.exists():
        raise RuntimeError(f"OpenFAST failed for {case.case_id} (rc={result.returncode}); see {log}")
    print(f"  [{case.case_id}] OpenFAST done in {dt:.0f}s ({outb.stat().st_size/1e6:.0f} MB)", flush=True)
    return outb


# ----------------------------------------------------------------------------
# Per-case orchestration
# ----------------------------------------------------------------------------

def run_one_case(case: Case, tmax: float, transient_drop_s: float,
                 openfast_exe: str, turbsim_exe: str, rosco_dll: str) -> dict:
    """Run one DLC case end-to-end. Pickle-safe; skips if .outb already exists."""
    os.environ.setdefault("PYTHONUTF8", "1")

    t_start = time.time()
    if case.outb.exists():
        return {"case_id": case.case_id, "status": "skipped",
                "outb": str(case.outb), "duration_s": 0.0}
    try:
        stage_case(case)
        analysis_time = tmax + 60.0  # TurbSim grid must outlive OpenFAST run
        write_turbsim_input(case, analysis_time)
        run_turbsim(case, Path(turbsim_exe))
        patch_servodyn(case, Path(rosco_dll))
        patch_hydrodyn(case)
        patch_inflowwind(case)
        patch_fst(case, tmax)
        outb = run_openfast(case, Path(openfast_exe))
        return {
            "case_id": case.case_id, "status": "ok",
            "outb": str(outb),
            "outb_size_mb": outb.stat().st_size / 1e6,
            "duration_s": time.time() - t_start,
        }
    except Exception as e:
        return {
            "case_id": case.case_id, "status": "failed",
            "error": str(e)[:400],
            "duration_s": time.time() - t_start,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dlc", choices=("dlca", "dlcb", "dlc16"), default="dlca",
                        help="Design Load Case set. Default: dlca.")
    parser.add_argument("--winds", nargs="+", type=float, default=None,
                        help="Wind speeds [m/s]. Defaults: dlca/dlcb=[8,11,15,20], dlc16=[11].")
    parser.add_argument("--seeds", type=int, default=6,
                        help="Number of seeds per (DLC, wind). Default: 6.")
    parser.add_argument("--tmax", type=float, default=3600.0,
                        help="OpenFAST TMax [s]. Default: 3600 (PLAN-canonical).")
    parser.add_argument("--transient-drop", type=float, default=600.0,
                        help="Post-run transient discard [s]. Default: 600.")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 2) - 1),
                        help="Parallel worker count. Default = cpu_count - 1.")
    parser.add_argument("--openfast-exe",
                        default=os.environ.get("OPENFAST_EXE", str(DEFAULT_OPENFAST_EXE)))
    parser.add_argument("--turbsim-exe",
                        default=os.environ.get("TURBSIM_EXE", str(DEFAULT_TURBSIM_EXE)))
    parser.add_argument("--rosco-dll",
                        default=os.environ.get("ROSCO_DLL", str(DEFAULT_ROSCO_DLL)))
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the case list and exit; do not run.")
    args = parser.parse_args()

    if args.winds is None:
        args.winds = [11.0] if args.dlc == "dlc16" else [8.0, 11.0, 15.0, 20.0]
    args.seeds = min(args.seeds, len(WIND_SEEDS))

    # Validate every requested (dlc, wind) has wave params
    for w in args.winds:
        if w not in DLC_WAVES[args.dlc]:
            raise SystemExit(f"No wave params for DLC {args.dlc} at wind {w} m/s. "
                             f"Available: {sorted(DLC_WAVES[args.dlc].keys())}")

    cases = [Case(dlc=args.dlc, wind_ms=w, seed_idx=s)
             for w in args.winds for s in range(args.seeds)]

    print(f"Campaign: {args.dlc.upper()}  ({len(cases)} cases = "
          f"{len(args.winds)} winds × {args.seeds} seeds)")
    print(f"TMax={args.tmax}s  transient={args.transient_drop}s  workers={args.workers}")
    print(f"OpenFAST: {args.openfast_exe}")
    print(f"TurbSim:  {args.turbsim_exe}")
    print(f"ROSCO:    {args.rosco_dll}\n")

    existing = sum(1 for c in cases if c.outb.exists())
    print(f"Already done (will skip): {existing}/{len(cases)}")
    pending = [c for c in cases if not c.outb.exists()]
    if args.dry_run or not pending:
        for c in cases:
            hs, tp = c.hs_tp
            mark = "[skip]" if c.outb.exists() else "[run ]"
            print(f"  {mark} {c.case_id}  V={c.wind_ms:5.1f}  wind_seed={c.wind_seed:>10}  "
                  f"wave_seed={c.wave_seed:>10}  Hs={hs:.1f} Tp={tp:.2f}")
        if args.dry_run:
            return 0

    print()
    t_start = time.time()
    results: list[dict] = []
    if args.workers <= 1:
        for c in pending:
            r = run_one_case(c, args.tmax, args.transient_drop,
                             args.openfast_exe, args.turbsim_exe, args.rosco_dll)
            results.append(r)
            print(f"  [{len(results)}/{len(pending)}] {r['case_id']}: {r['status']}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as ex:
            futures = {
                ex.submit(run_one_case, c, args.tmax, args.transient_drop,
                          args.openfast_exe, args.turbsim_exe, args.rosco_dll): c
                for c in pending
            }
            for fut in as_completed(futures):
                r = fut.result()
                results.append(r)
                print(f"  [{len(results)}/{len(pending)}] {r['case_id']}: {r['status']}", flush=True)

    elapsed = time.time() - t_start
    n_ok = sum(1 for r in results if r["status"] == "ok")
    n_skip = sum(1 for r in results if r["status"] == "skipped") + existing
    n_fail = sum(1 for r in results if r["status"] == "failed")
    print(f"\nCampaign done in {elapsed/60:.1f} min")
    print(f"  ok      : {n_ok}")
    print(f"  skipped : {n_skip}")
    print(f"  failed  : {n_fail}")
    if n_fail:
        print("\nFailures:")
        for r in results:
            if r["status"] == "failed":
                print(f"  {r['case_id']}: {r.get('error','?')}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
