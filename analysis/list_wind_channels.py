#!/usr/bin/env python3
"""list_wind_channels.py - list any wind-related channels in an OpenFAST .outb, so we can find
a rotor-averaged / disk-averaged wind signal (e.g. RtVAvgxh) to use as a TE source instead of
the single-point Wind1VelX. Run in fowt-openfast (openfast_toolbox)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from load_runs import load_outb  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
DECK = "IEA-15-240-RWT-UMaineSemi"
default = REPO / "sims" / "dlca_v08ms_s00" / DECK / f"{DECK}.outb"
outb = Path(sys.argv[1]) if len(sys.argv) > 1 else default

df = load_outb(outb)
pat = re.compile(r"wind|RtV|Vavg|Avgx|Vx[hy]|WindV|RtSkew|RtVAvg|RtAero|HWind", re.I)
hits = [c for c in df.columns if pat.search(c)]
print(f"{outb.name}: {len(df.columns)} channels total")
print("wind-related candidates (look for a rotor-averaged one like RtVAvgxh):")
for c in hits:
    print("  ", c)
if not hits:
    print("  (none matched — decks may not output a rotor-averaged wind)")
