"""
run_iea15_single.py — real IEA-15 single-case OpenFAST sim + end-to-end TE.

Phase 2 first deliverable; replaces the case-3 ITIBarge stand-in.

Pipeline:
  1. Stage the IEA-15-240-RWT-UMaineSemi deck into sims/case-iea15-real/
  2. Generate a TurbSim full-field wind file (NTM, V=11 m/s, 320 s)
  3. Patch InflowFile.dat to use WindType=3 + the new .bts
  4. Patch .fst to TMax=300, OutFileFmt=2 (.outb only)
  5. Run OpenFAST 4.2.0 from openfast_env
  6. Parse the .outb, decimate to 10 Hz, drop first 60 s transient
  7. BivariateTE Wind1VelX -> PtfmPitch (forward + reverse sanity check)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_OPENFAST = PROJECT_ROOT / "repos" / "IEA-15-240-RWT" / "OpenFAST"
RUN_DIR = PROJECT_ROOT / "sims" / "case-iea15-real"
OUT_DIR = PROJECT_ROOT / "data"
TURBSIM_EXE = Path(r"C:\Users\kunsanuni3\miniconda3\envs\openfast_env\Library\bin\turbsim.exe")
OPENFAST_EXE = Path(r"C:\Users\kunsanuni3\miniconda3\envs\openfast_env\Library\bin\openfast.exe")

TMAX = 300.0
WIND_SPEED = 11.0     # m/s (rated, matches predecessor's DLC1.6 wind)
HUB_HT = 150.0
ROTOR_DIAM = 240.0
TURB_SECONDS = 360.0  # > TMAX with margin


TURBSIM_BASE = (
    PROJECT_ROOT / "repos" / "r-test" / "glue-codes" / "fast-farm"
    / "ModAmb_3" / "TurbSim" / "HighT1.inp"
)


_UNUSED_TEMPLATE = """---------TurbSim v2 (OpenFAST) Input File------------------
IEA-15MW rated-wind NTM case for case-3 single-case TE.
---------Runtime Options-----------------------------------
False         Echo            - Echo input data
4433456       RandSeed1       - First random seed
"RanLux"      RandSeed2       - Second random seed
False         WrBHHTP         -
False         WrFHHTP         -
False         WrADHH          -
True          WrADFF          - Output full-field .bts
False         WrBLFF          -
False         WrADTWR         -
False         WrHAWCFF        -
False         WrFMTFF         -
False         WrACT           -
0             ScaleIEC        -
--------Turbine/Model Specifications-----------------------
31            NumGrid_Z       - Vertical grid-point matrix dimension
31            NumGrid_Y       - Horizontal grid-point matrix dimension
0.05          TimeStep        - Time step [s]
{anatime:.1f}        AnalysisTime    - Analysis time [s]
"ALL"         UsableTime      - Usable time [s]
{hub_ht:.1f}         HubHt           - Hub height [m]
{grid_h:.1f}         GridHeight      - Grid height [m]
{grid_w:.1f}         GridWidth       - Grid width [m]
0             VFlowAng        -
0             HFlowAng        -
--------Meteorological Boundary Conditions-------------------
"IECKAI"      TurbModel       - Turbulence model
"unused"      UserFile        -
1             IECstandard     - IEC 61400-x edition
"B"           IECturbc        - IEC turbulence characteristic
"NTM"         IEC_WindType    - IEC turbulence type
"default"     ETMc            -
"default"     WindProfileType -
"unused"      ProfileFile     -
{hub_ht:.1f}         RefHt           - Reference height [m]
{uref:.2f}          URef            - Mean velocity at RefHt [m/s]
350           ZJetMax         -
"default"     PLExp           -
"default"     Z0              -
--------Non-IEC Meteorological Boundary Conditions------------
"default"     Latitude        -
0.05          RICH_NO         -
"default"     UStar           -
"default"     ZI              -
"default"     PC_UW           -
"default"     PC_UV           -
"default"     PC_VW           -
--------Spatial Coherence Parameters----------------------------
"default"     SCMod1          -
"default"     SCMod2          -
"default"     SCMod3          -
"default"     InCDec1         -
"default"     InCDec2         -
"default"     InCDec3         -
"default"     CohExp          -
--------Coherent Turbulence Scaling Parameters-------------------
"./EventData" CTEventPath     -
"Random"      CTEventFile     -
True          Randomize       -
1.0           DistScl         -
0.5           CTLy            -
0.5           CTLz            -
30.0          CTStartTime     -
==================================================
"""


def stage_case():
    print(f"Staging IEA-15 deck -> {RUN_DIR}")
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True)
    # The UMaineSemi .fst uses relative paths like
    # `../IEA-15-240-RWT/IEA-15-240-RWT_InflowFile.dat`, so we copy both subdirs.
    shutil.copytree(SRC_OPENFAST / "IEA-15-240-RWT", RUN_DIR / "IEA-15-240-RWT")
    shutil.copytree(SRC_OPENFAST / "IEA-15-240-RWT-UMaineSemi", RUN_DIR / "IEA-15-240-RWT-UMaineSemi")


def write_turbsim_input() -> Path:
    """Build wind.inp by patching r-test's HighT1.inp (known-good template)."""
    grid = max(2 * (ROTOR_DIAM / 2) + 20, ROTOR_DIAM + 20)
    txt = TURBSIM_BASE.read_text()

    def replace_value(text: str, keyword: str, new_value: str) -> str:
        """Replace the value field for `keyword` in a TurbSim-format line.
        Handles both bareword values ("31") and quoted-string values
        (`"6.000 "` -- TurbSim allows spaces inside double quotes)."""
        pattern = re.compile(rf'^(?:"[^"]*"|\S+)(\s+{keyword}\b)', re.M)
        match = pattern.search(text)
        if not match:
            raise RuntimeError(f"keyword {keyword!r} not found in TurbSim template")
        return pattern.sub(lambda _m: f"{new_value}{_m.group(1)}", text, count=1)

    # NTM with IECKAI spectrum (instead of HighT1's TIMESR/USRTimeSeries)
    txt = replace_value(txt, "TurbModel", '"IECKAI"')
    txt = replace_value(txt, "UserFile", '"unused"')
    txt = replace_value(txt, "IECturbc", '"B"')
    txt = replace_value(txt, "IEC_WindType", '"NTM"')
    txt = replace_value(txt, "WindProfileType", '"PL"')

    # Grid and turbine specs for IEA-15
    txt = replace_value(txt, "NumGrid_Z", "31")
    txt = replace_value(txt, "NumGrid_Y", "31")
    txt = replace_value(txt, "TimeStep", "0.05")
    txt = replace_value(txt, "AnalysisTime", f"{TURB_SECONDS:.1f}")
    txt = replace_value(txt, "HubHt", f"{HUB_HT:.1f}")
    txt = replace_value(txt, "GridHeight", f"{grid:.1f}")
    txt = replace_value(txt, "GridWidth", f"{grid:.1f}")
    txt = replace_value(txt, "RefHt", f"{HUB_HT:.1f}")
    txt = replace_value(txt, "URef", f"{WIND_SPEED:.2f}")

    path = RUN_DIR / "wind.inp"
    path.write_text(txt)
    return path


def run_turbsim(turbsim_inp: Path) -> Path:
    print(f"Running TurbSim ({TURB_SECONDS} s, V={WIND_SPEED} m/s, NTM-B)...")
    t0 = time.time()
    result = subprocess.run(
        [str(TURBSIM_EXE), str(turbsim_inp.name)],
        cwd=str(RUN_DIR),
        capture_output=True,
        text=True,
    )
    dt = time.time() - t0
    bts = RUN_DIR / "wind.bts"
    if result.returncode != 0 or not bts.exists():
        print("TurbSim stdout:", result.stdout[-2000:])
        print("TurbSim stderr:", result.stderr[-2000:])
        raise RuntimeError(f"TurbSim failed (rc={result.returncode}); see logs")
    print(f"  TurbSim done in {dt:.1f}s -> {bts.name}")
    return bts


def patch_inflowwind(bts_path: Path):
    inflow = RUN_DIR / "IEA-15-240-RWT" / "IEA-15-240-RWT_InflowFile.dat"
    txt = inflow.read_text()
    # Switch WindType from 1 (steady) to 3 (TurbSim binary FF)
    txt = re.sub(r"^\s*1(\s+WindType\b)", r"3\1", txt, count=1, flags=re.M)
    # Set the .bts filename. The IEA-15 cwd at run time is the UMaineSemi
    # subdir, so the path needs to climb out one level.
    bts_rel = f"../{bts_path.name}"
    txt = re.sub(
        r'"none"(\s+FileName_BTS\b)',
        f'"{bts_rel}"\\1',
        txt, count=1,
    )
    inflow.write_text(txt)
    print(f"Patched {inflow.name}: WindType=3, FileName_BTS={bts_rel!r}")


def patch_fst():
    fst = RUN_DIR / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.fst"
    txt = fst.read_text()
    txt = re.sub(r"^\s*\S+(\s+TMax\b)", f"{TMAX}\\1", txt, count=1, flags=re.M)
    txt = re.sub(r"^\s*\S+(\s+OutFileFmt\b)", r"2\1", txt, count=1, flags=re.M)
    fst.write_text(txt)
    print(f"Patched {fst.name}: TMax={TMAX}, OutFileFmt=2")


def run_openfast() -> Path:
    fst = RUN_DIR / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.fst"
    print(f"Running OpenFAST 4.2.0 (TMax={TMAX}s)... (this is the long step)")
    t0 = time.time()
    log = RUN_DIR / "openfast.log"
    with log.open("w") as lf:
        result = subprocess.run(
            [str(OPENFAST_EXE), fst.name],
            cwd=str(fst.parent),
            stdout=lf, stderr=subprocess.STDOUT,
        )
    dt = time.time() - t0
    outb = fst.with_suffix(".outb")
    if result.returncode != 0 or not outb.exists():
        print(f"OpenFAST failed (rc={result.returncode}); see {log}")
        raise RuntimeError("OpenFAST run failed")
    print(f"  OpenFAST done in {dt:.1f}s ({TMAX/dt:.2f}x real-time) -> {outb.name}")
    return outb


def run_te_pipeline(outb_path: Path):
    sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
    from load_runs import load_outb, find_time_column

    df = load_outb(outb_path)
    print(f"Parsed {df.shape[0]} rows x {df.shape[1]} channels")

    t_col = find_time_column(df)
    wind_col = next(c for c in df.columns if c.split("_[")[0].lower() == "wind1velx")
    pitch_col = next(c for c in df.columns if c.split("_[")[0].lower() == "ptfmpitch")
    t = df[t_col].to_numpy()
    dt = float(np.median(np.diff(t)))
    src_hz = 1.0 / dt
    target_hz = 10.0
    factor = max(1, int(round(src_hz / target_hz)))
    transient_drop_s = 60.0
    drop_idx = int(transient_drop_s / dt)
    print(f"  src={src_hz:.1f} Hz, decimate by {factor} -> {src_hz/factor:.1f} Hz; drop first {transient_drop_s}s")

    wind = df[wind_col].to_numpy()[drop_idx:][::factor]
    pitch = df[pitch_col].to_numpy()[drop_idx:][::factor]
    n_analysis = len(wind)
    print(f"  analysis N = {n_analysis} samples ({n_analysis*factor/src_hz:.0f}s)")

    # Jitter (kraskov-2004 §III.A) + run IDTxl BivariateTE both directions
    rng = np.random.default_rng(0)
    wind_j = wind + 1e-10 * rng.standard_normal(wind.shape)
    pitch_j = pitch + 1e-10 * rng.standard_normal(pitch.shape)

    from idtxl.bivariate_te import BivariateTE
    from idtxl.data import Data

    def te(s, tgt):
        data = Data(np.vstack([s, tgt]), dim_order="ps", normalise=True)
        analysis = BivariateTE()
        settings = {
            "cmi_estimator": "JidtKraskovCMI",
            "kraskov_k": "4",
            "max_lag_sources": 5,
            "min_lag_sources": 1,
            "max_lag_target": 5,
            "n_perm_max_stat": 200, "n_perm_min_stat": 200,
            "n_perm_omnibus": 200, "n_perm_max_seq": 200,
            "alpha_max_stat": 0.05, "alpha_min_stat": 0.05, "alpha_omnibus": 0.05,
            "permute_in_time": True,
        }
        res = analysis.analyse_single_target(settings=settings, data=data, target=1, sources=[0])
        tr = res.get_single_target(1, fdr=False)
        te_arr = tr.get("te")
        pval = tr.get("omnibus_pval")
        return (float(te_arr[0]) if te_arr is not None and len(te_arr) else 0.0,
                float(pval) if pval is not None else 1.0)

    print("\nForward: TE(Wind1VelX -> PtfmPitch)")
    te_fwd, p_fwd = te(wind_j, pitch_j)
    print(f"  TE = {te_fwd:+.4f} nats, p = {p_fwd:.4f}")

    print("\nReverse: TE(PtfmPitch -> Wind1VelX)")
    te_rev, p_rev = te(pitch_j, wind_j)
    print(f"  TE = {te_rev:+.4f} nats, p = {p_rev:.4f}")

    print("\n=== Verdict ===")
    pass_fwd = (p_fwd < 0.05) and (te_fwd > 0)
    pass_rev = (p_rev >= 0.05) or (te_rev < 0.2 * max(te_fwd, 1e-6))
    print(f"  TE(wind->pitch) significant?     {'PASS' if pass_fwd else 'FAIL'}")
    print(f"  TE(pitch->wind) NOT significant? {'PASS' if pass_rev else 'FAIL'}")

    # Save the Parquet for downstream Phase 4 work
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    parquet = OUT_DIR / "case-iea15-real.parquet"
    df.to_parquet(parquet, compression="zstd")
    print(f"\nWrote {parquet}")
    return pass_fwd and pass_rev


def main() -> int:
    os.environ.setdefault("PYTHONUTF8", "1")
    stage_case()
    ts_inp = write_turbsim_input()
    bts = run_turbsim(ts_inp)
    patch_inflowwind(bts)
    patch_fst()
    outb = run_openfast()
    ok = run_te_pipeline(outb)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
