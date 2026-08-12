"""run_fault.py - inject a graded pitch fault into an existing OpenFAST case and re-run.

Clones a staged healthy case dir, patches the deck to inject ONE pitch fault, inherits
wind.bts + SeaState seed unchanged (clean A/B vs the healthy sibling), re-runs OpenFAST,
and sanity-checks the result. Feed the tagged .outb to analysis/compute_fault_te.py to test
whether the fault lifts wind->platform TE above the healthy firewall ceiling (~0.029 nats).

This is the injection half of the graded pitch-fault campaign the paper specifies in 4.3
(plan: fluffy-forging-trinket). It reuses run_openloop.py's clone-patch-rerun machinery.

Faults (see the ServoDyn / DISCON.IN deck analysis):
  pitchlock  All blades seize at the healthy *operating* pitch at --onset-s, via the native
             ServoDyn override maneuver (TPitManS/PitManRat/BlPitchF). PCMode/VSContrl are left
             at 5 so ROSCO torque keeps regulating speed -> avoids the above-rated overspeed
             that freezing at fine pitch (PCMode=0) would cause. Pitch stops responding to wind.
  stuck      Only blade --blade seizes (same maneuver); the other two keep ROSCO pitch control.
             A genuine partial-authority fault; pitch still moves on 2/3 blades.
  gain       Reduce the P/I pitch gains: scale every entry of the PC_GS_KP and PC_GS_KI
             30-float gain-schedule rows in DISCON.IN by --severity (e.g. 0.10). Pitch keeps
             moving but under-regulates thrust -> the cleanest "re-admit wind" test, and (unlike
             lock) it keeps BldPitch1 varying so SURD stays valid.

Usage:
    python sims/run_fault.py sims/dlca_v20ms_s00 --fault pitchlock --onset-s 600
    python sims/run_fault.py sims/dlca_v15ms_s00 --fault gain --severity 0.10
    python sims/run_fault.py sims/dlca_v20ms_s00 --fault stuck --blade 1 --onset-s 600
    python sims/run_fault.py sims/dlc16_v11ms_s00 --fault gain --severity 0.10 --no-run  # stage+patch only
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))  # allow "import run_openloop"
from run_openloop import (  # noqa: E402  reuse the clone-patch-rerun machinery
    DECK_SUBDIR,
    PROJECT_ROOT,
    RATED_ROTOR_RPM,
    run_openfast,
    sanity_check,
)

FAULT_TYPES = ("pitchlock", "stuck", "gain")
FAULTS_DIR = PROJECT_ROOT / "sims" / "faults"  # flat dir of tagged .outb links for the TE step


def _sub1(txt: str, pattern: str, repl: str, what: str) -> str:
    """Value-first single substitution (run_openloop idiom); assert exactly one hit."""
    txt2, n = re.subn(pattern, repl, txt, count=1, flags=re.M)
    if n != 1:
        raise RuntimeError(f"deck patch missed {what} (count={n})")
    return txt2


def healthy_operating_pitch(base: Path, transient_s: float = 600.0) -> float:
    """Mean BldPitch1 [deg] over the post-transient healthy run - the realistic lock angle."""
    outb = base / DECK_SUBDIR / f"{DECK_SUBDIR}.outb"
    if not outb.exists():
        raise SystemExit(
            f"need the healthy run {outb} to read the operating pitch for a lock/stuck fault; "
            f"run the healthy case first, or pass --final-deg to set the seize angle explicitly."
        )
    sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
    from load_runs import load_outb

    df = load_outb(outb)

    def _col(name: str):
        for c in df.columns:
            if c.split("_[")[0].lower() == name.lower():
                return df[c].to_numpy()
        return None

    pitch = _col("BldPitch1")
    time = _col("Time")
    if pitch is None or time is None:
        raise SystemExit(f"{outb.name}: no BldPitch1/Time channel to read operating pitch.")
    mask = time >= (time[0] + transient_s)
    op = float(np.mean(pitch[mask]))
    print(f"  healthy operating pitch (mean BldPitch1 after {transient_s:.0f}s): {op:.3f} deg")
    return op


# --------------------------------------------------------------- per-fault patchers

def patch_pitchlock(deck_dir: Path, onset_s: float, final_deg: float, rate_degps: float,
                    blades=(1, 2, 3)) -> None:
    """Seize the given blades at final_deg via the ServoDyn override maneuver at onset_s.

    Leaves PCMode=5 / VSContrl=5 (ROSCO torque still active). Used for both full pitchlock
    (all blades) and single-blade stuck (one blade); the untouched blades keep 9999.9 =
    ROSCO-controlled.
    """
    sd = deck_dir / f"{DECK_SUBDIR}_ServoDyn.dat"
    txt = sd.read_text(encoding="utf-8")
    for b in blades:
        txt = _sub1(txt, rf"^\s*\S+(\s+TPitManS\({b}\))", f"{onset_s}\\1", f"TPitManS({b})")
        txt = _sub1(txt, rf"^\s*\S+(\s+PitManRat\({b}\))", f"{rate_degps}\\1", f"PitManRat({b})")
        txt = _sub1(txt, rf"^\s*\S+(\s+BlPitchF\({b}\))", f"{final_deg}\\1", f"BlPitchF({b})")
    sd.write_text(txt, encoding="utf-8")
    which = "all blades" if len(blades) == 3 else f"blade {blades[0]}"
    print(f"  patched {sd.name}: seize {which} at {final_deg:.3f} deg "
          f"(onset {onset_s:.0f}s, rate {rate_degps} deg/s)")


def _scale_gs_row(txt: str, key: str, factor: float) -> str:
    """Multiply every float in a ROSCO gain-schedule row ('<30 floats>  ! KEY ...') by factor."""
    pat = re.compile(rf"^([^\n!]*?)(\s*!\s*{re.escape(key)}\b)", re.M)

    def _repl(m: "re.Match") -> str:
        nums = m.group(1).split()
        if len(nums) != 30:
            raise RuntimeError(f"{key}: expected 30 gain entries, got {len(nums)}")
        scaled = "   ".join(f"{float(x) * factor:+.4e}" for x in nums)
        return scaled + m.group(2)

    new, n = pat.subn(_repl, txt, count=1)
    if n != 1:
        raise RuntimeError(f"DISCON patch missed gain-schedule row {key} (count={n})")
    return new


def patch_gain(deck_dir: Path, factor: float) -> None:
    """Reduce pitch P/I authority: scale PC_GS_KP and PC_GS_KI schedules by factor in (0,1)."""
    if not (0.0 < factor < 1.0):
        raise SystemExit(f"--severity for gain fault must be in (0,1); got {factor}")
    dc = deck_dir / f"{DECK_SUBDIR}_DISCON.IN"
    txt = dc.read_text(encoding="utf-8")
    txt = _scale_gs_row(txt, "PC_GS_KP", factor)
    txt = _scale_gs_row(txt, "PC_GS_KI", factor)
    dc.write_text(txt, encoding="utf-8")
    print(f"  patched {dc.name}: PC_GS_KP & PC_GS_KI scaled x{factor}")


# --------------------------------------------------------------- driver

def default_tag(args: argparse.Namespace) -> str:
    if args.fault == "gain":
        return f"gain{int(round(args.severity * 100)):03d}"   # 0.10 -> gain010
    if args.fault == "stuck":
        return f"stuckb{args.blade}"
    return "pitchlock"


def apply_fault(deck_dir: Path, base: Path, args: argparse.Namespace) -> None:
    if args.fault == "pitchlock":
        final = args.final_deg if args.final_deg is not None else healthy_operating_pitch(base)
        patch_pitchlock(deck_dir, args.onset_s, final, args.rate, blades=(1, 2, 3))
    elif args.fault == "stuck":
        final = args.final_deg if args.final_deg is not None else healthy_operating_pitch(base)
        patch_pitchlock(deck_dir, args.onset_s, final, args.rate, blades=(args.blade,))
    elif args.fault == "gain":
        patch_gain(deck_dir, args.severity)
    else:  # pragma: no cover - argparse restricts choices
        raise SystemExit(f"unknown fault {args.fault}")


def link_tagged_outb(outb: Path, base_id: str, tag: str) -> Path:
    """Expose the run's .outb under a unique fault-tagged stem so the TE pipeline (which keys
    on the .outb filename stem) gives each arm a distinct case id. Hardlink to avoid copying
    ~256 MB; fall back to copy if hardlink is unavailable."""
    FAULTS_DIR.mkdir(parents=True, exist_ok=True)
    dst = FAULTS_DIR / f"{base_id}_{tag}.outb"
    dst.unlink(missing_ok=True)
    try:
        os.link(outb, dst)          # hardlink (same volume, instant, no privilege)
    except OSError:
        shutil.copy2(outb, dst)     # last resort
    print(f"  tagged output for TE: {dst}")
    return dst


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base_case", type=Path,
                    help="Existing staged healthy case dir (e.g. sims/dlca_v20ms_s00)")
    ap.add_argument("--fault", choices=FAULT_TYPES, required=True)
    ap.add_argument("--severity", type=float, default=0.10,
                    help="gain fault: PC_GS_KP/KI scale factor in (0,1). Default 0.10.")
    ap.add_argument("--onset-s", type=float, default=600.0,
                    help="lock/stuck: fault onset time [s] (>= transient drop). Default 600.")
    ap.add_argument("--blade", type=int, default=1, choices=(1, 2, 3),
                    help="stuck fault: which blade seizes. Default 1.")
    ap.add_argument("--final-deg", type=float, default=None,
                    help="lock/stuck: seize angle [deg]. Default = healthy operating pitch.")
    ap.add_argument("--rate", type=float, default=2.0,
                    help="lock/stuck: pitch maneuver rate to the seize angle [deg/s]. Default 2.0.")
    ap.add_argument("--tag", default=None, help="Override the fault tag (case-id suffix).")
    ap.add_argument("--openfast-exe", default=os.environ.get("OPENFAST_EXE", "openfast"))
    ap.add_argument("--no-run", action="store_true", help="Stage + patch only; skip OpenFAST.")
    args = ap.parse_args()

    base = args.base_case.resolve()
    deck = base / DECK_SUBDIR
    if not (deck / f"{DECK_SUBDIR}.fst").exists():
        raise SystemExit(f"No deck at {deck} - give a staged healthy case dir.")
    if not (base / "wind.bts").exists():
        raise SystemExit(f"No wind.bts in {base} - faulted run must inherit the healthy wind field.")

    tag = args.tag or default_tag(args)
    out = base.parent / f"{base.name}_{tag}"
    print(f"Fault injection: {base.name} --{args.fault}--> {out.name}")
    if out.exists():
        raise SystemExit(f"{out} already exists - remove it to re-run.")
    shutil.copytree(base, out)
    apply_fault(out / DECK_SUBDIR, base, args)

    if args.no_run:
        print("  --no-run: staged + patched, skipping OpenFAST.")
        return 0

    outb = run_openfast(out / DECK_SUBDIR, args.openfast_exe)
    sanity_check(outb)
    verify_fault(outb, args)
    tagged = link_tagged_outb(outb, base.name, tag)
    parquet = PROJECT_ROOT / "reports" / f"te_fault_{base.name}_{tag}.parquet"
    print(f"\nDone. Faulted output: {outb}")
    print("Next - compute wind->platform TE and test against the healthy ceiling:")
    print(f"  python analysis/compute_fault_te.py --outb {tagged} -o {parquet}")
    return 0


def verify_fault(outb: Path, args: argparse.Namespace) -> None:
    """Fault-specific asserts on the output: confirm the fault actually took (see plan)."""
    sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
    from load_runs import load_outb

    df = load_outb(outb)

    def _col(name: str):
        for c in df.columns:
            if c.split("_[")[0].lower() == name.lower():
                return df[c].to_numpy()
        return None

    time = _col("Time")
    after = time >= (time[0] + args.onset_s) if time is not None else slice(None)
    print("=== fault verification ===")
    for ch in ("BldPitch1", "BldPitch2", "BldPitch3"):
        v = _col(ch)
        if v is None:
            continue
        sd_after = float(np.std(v[after]))
        print(f"  {ch} std after onset = {sd_after:.4f} deg")
    if args.fault in ("pitchlock", "stuck"):
        print("  (expect ~0 std on the seized blade(s); moving blades stay non-zero)")
    else:
        print("  (gain fault: pitch should still move - std > 0 on all blades)")


if __name__ == "__main__":
    sys.exit(main())
