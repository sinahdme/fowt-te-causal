"""run_openloop.py — controller-ablation re-run of an existing OpenFAST case.

Duplicates a controller-ON case directory, disables the *active pitch
controller* (the 'firewall' mechanism), and re-runs OpenFAST. Wind (wind.bts)
and wave (SeaState seed) are inherited unchanged, so the only difference vs the
controller-on run is the controller — a clean A/B for the
"controller-as-causal-firewall" test (PLAN.md Q11 / H1-null).

Ablation (see ServoDyn deck analysis):
  PCMode   5 -> 0   : blade pitch held fixed; the pitch controller can no
                      longer regulate rotor thrust against wind fluctuations.
  VSContrl 5 -> 1   : switch from the ROSCO DLL to ServoDyn's simple built-in
                      variable-speed torque law (already parameterised:
                      VS_RtTq / VS_Rgn2K / VS_RtGnSp). Keeps a passive torque so
                      the rotor does NOT freewheel/run away. (Pure VSContrl=0 is
                      unusable here: the GenModel=1 fallback params are all
                      9999.9 placeholders -> runaway overspeed.)

After the run it prints a rotor-speed / pitch sanity summary; if the rotor
overspeeds badly the TE on that output is not trustworthy.

Usage:
    python sims/run_openloop.py sims/dlca_v11ms_s00
    OPENFAST_EXE=/path/to/openfast python sims/run_openloop.py sims/dlca_v11ms_s00
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DECK_SUBDIR = "IEA-15-240-RWT-UMaineSemi"
RATED_ROTOR_RPM = 7.56  # IEA-15 rated rotor speed; overspeed flag reference


def patch_servodyn_openloop(deck_dir: Path) -> None:
    """PCMode 5->0 (fix pitch) and VSContrl 5->1 (simple passive torque)."""
    sd = deck_dir / f"{DECK_SUBDIR}_ServoDyn.dat"
    txt = sd.read_text(encoding="utf-8")
    txt, n_pc = re.subn(r"^\s*\S+(\s+PCMode\b)", r"0\1", txt, count=1, flags=re.M)
    txt, n_vs = re.subn(r"^\s*\S+(\s+VSContrl\b)", r"1\1", txt, count=1, flags=re.M)
    if not (n_pc and n_vs):
        raise RuntimeError(f"ServoDyn patch missed PCMode({n_pc})/VSContrl({n_vs})")
    sd.write_text(txt, encoding="utf-8")
    print(f"  patched {sd.name}: PCMode=0, VSContrl=1")


def run_openfast(deck_dir: Path, openfast_exe: str) -> Path:
    fst = deck_dir / f"{DECK_SUBDIR}.fst"
    outb = fst.with_suffix(".outb")
    outb.unlink(missing_ok=True)  # force a fresh run
    log = deck_dir.parent / "openfast_openloop.log"
    print(f"  running OpenFAST (this is the long step)...", flush=True)
    t0 = time.time()
    with log.open("w") as lf:
        r = subprocess.run([str(openfast_exe), fst.name], cwd=str(deck_dir),
                           stdout=lf, stderr=subprocess.STDOUT)
    if r.returncode != 0 or not outb.exists():
        raise RuntimeError(f"OpenFAST failed (rc={r.returncode}); see {log}")
    print(f"  OpenFAST done in {time.time()-t0:.0f}s -> {outb.name}", flush=True)
    return outb


def sanity_check(outb: Path) -> None:
    """Print rotor-speed / pitch stats so we can judge whether the open-loop
    run stayed physical before trusting any TE on it."""
    sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
    from load_runs import load_outb
    df = load_outb(outb)

    def col(name):
        for c in df.columns:
            if c.split("_[")[0].lower() == name.lower():
                return df[c].to_numpy()
        return None

    print("\n=== open-loop sanity check ===")
    rot = col("RotSpeed")
    if rot is not None:
        print(f"  RotSpeed [rpm]  min={rot.min():.2f}  mean={rot.mean():.2f}  "
              f"max={rot.max():.2f}   (rated ~{RATED_ROTOR_RPM})")
        if rot.max() > 1.5 * RATED_ROTOR_RPM:
            print(f"  !! WARNING: rotor overspeed ({rot.max():.1f} rpm > "
                  f"1.5x rated) — TE on this run may be dominated by the "
                  f"runaway, not wind/wave coupling. Inspect before trusting.")
    for ch in ("BldPitch1", "GenPwr", "GenSpeed"):
        v = col(ch)
        if v is not None:
            print(f"  {ch:10s}  min={v.min():.3g}  mean={v.mean():.3g}  max={v.max():.3g}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base_case", type=Path,
                    help="Existing controller-on case dir (e.g. sims/dlca_v11ms_s00)")
    ap.add_argument("--openfast-exe",
                    default=os.environ.get("OPENFAST_EXE", "openfast"))
    ap.add_argument("--suffix", default="_openloop")
    ap.add_argument("--no-run", action="store_true",
                    help="Stage + patch only; skip the OpenFAST run.")
    args = ap.parse_args()

    base = args.base_case.resolve()
    deck = base / DECK_SUBDIR
    if not (deck / f"{DECK_SUBDIR}.fst").exists():
        raise SystemExit(f"No deck at {deck} — give a staged controller-on case dir.")
    if not (base / "wind.bts").exists():
        print(f"  note: no wind.bts in {base} (inherited wind may be elsewhere)")

    out = base.parent / (base.name + args.suffix)
    print(f"Open-loop ablation: {base.name} -> {out.name}")
    if out.exists():
        raise SystemExit(f"{out} already exists — remove it to re-run.")
    shutil.copytree(base, out)
    patch_servodyn_openloop(out / DECK_SUBDIR)

    if args.no_run:
        print("  --no-run: staged + patched, skipping OpenFAST.")
        return 0
    outb = run_openfast(out / DECK_SUBDIR, args.openfast_exe)
    sanity_check(outb)
    print(f"\nDone. Open-loop output: {outb}")
    print("Next: run te_pipeline.py on it (same flags as the controller-on run), "
          "then compare_tau.py the two tables.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
