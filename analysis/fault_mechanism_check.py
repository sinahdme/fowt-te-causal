#!/usr/bin/env python3
"""fault_mechanism_check.py - did the injected pitch fault actually perturb the platform?

Compares post-transient motion std (RotSpeed + PtfmPitch/Surge/Heave) of each faulted run
against its healthy sibling. This tells us whether the clean wind->platform TE null is
"structural filtering" (the fault DOES move the rotor/platform, yet no wind information gets
through) rather than "the fault did nothing" or degenerate data. Run in the fowt-openfast env
(needs openfast_toolbox). Reads sims/<case>/<deck>/<deck>.outb directly.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from load_runs import load_outb  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
DECK = "IEA-15-240-RWT-UMaineSemi"
CHANS = ("RotSpeed", "PtfmPitch", "PtfmSurge", "PtfmHeave")
DROP = 24000  # 600 s transient at 40 Hz
FAULT_RE = re.compile(r"_(pitchlock|gain\d+|stuckb\d)$")


def outb(case: str) -> Path:
    return REPO / "sims" / case / DECK / f"{DECK}.outb"


def col(df, name: str):
    for c in df.columns:
        if c.split("_[")[0].lower() == name.lower():
            return df[c].to_numpy()
    return None


def main() -> int:
    faults = sorted(p.name for p in (REPO / "sims").glob("dlca_v*ms_s*_*")
                    if FAULT_RE.search(p.name) and outb(p.name).exists())
    if not faults:
        print("No faulted case dirs found under sims/.", file=sys.stderr)
        return 1
    print(f"{'arm':<34}{'chan':<11}{'healthy_std':>12}{'fault_std':>11}{'x':>7}")
    print("-" * 75)
    for f in faults:
        healthy = FAULT_RE.sub("", f)
        if not outb(healthy).exists():
            print(f"{f:<34}(no healthy sibling {healthy})")
            continue
        hd, fd = load_outb(outb(healthy)), load_outb(outb(f))
        for ch in CHANS:
            hv, fv = col(hd, ch), col(fd, ch)
            if hv is None or fv is None:
                continue
            hs, fs = float(np.std(hv[DROP:])), float(np.std(fv[DROP:]))
            ratio = fs / hs if hs > 1e-9 else float("nan")
            print(f"{f:<34}{ch:<11}{hs:>12.4f}{fs:>11.4f}{ratio:>7.2f}")
        print()
    print("Read: fault_std/healthy_std ('x') > 1 on PtfmPitch/Surge/Heave means the fault "
          "DID perturb platform motion, so wind->platform TE=0 is structural (a real null), "
          "not 'fault did nothing'. RotSpeed x>>1 confirms the rotor lost regulation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
