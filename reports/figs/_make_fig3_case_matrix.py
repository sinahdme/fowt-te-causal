"""Regenerate the simulation case-matrix figure.

NOTE ON NUMBERING: this is *Figure 3* in the manuscript (the figures were
renumbered when the OpenFAST module schematic was inserted as Figure 2). The
output file keeps its historical name ``fig2-dlc-matrix.png`` because that is
the media the canonical docx embeds (word/media/image2.png); renaming would
force a docx re-point for no benefit.

This is a clean, dedicated generator that replaces a lost one-off script. It
reproduces the original case grid (dlca/dlcb over 4 speeds x 6 seeds = 48, plus
dlc16 at 11 m/s x 6 seeds = 6 -> 54 runs) with two author-requested changes:
  * the explanatory subtitle line at the top is removed (declutter);
  * the legend moves from the bottom to the right-centre.

Marker colours were sampled from the original PNG for fidelity.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent

# --- palette (sampled from the original figure) ---
C_DLCA = "#0C6CB4"   # dlca  — NTM wind, JONSWAP wave (seed A)
C_DLCB = "#E49C0C"   # dlcb  — NTM wind, decoupled wave seed
C_DLC16 = "#0C9C6C"  # dlc16 — DLC 1.6 severe sea state
GRID = "#D9D9D9"
GRAY = "#666666"

SPEEDS = [8, 11, 15, 20]          # hub-height wind speed (m/s)
SEEDS = [f"s{i:02d}" for i in range(6)]

# variants present in each speed column, left -> right, with x-offsets
def variants(speed):
    if speed == 11:
        return [(-0.26, C_DLCA), (0.0, C_DLC16), (0.26, C_DLCB)]
    return [(-0.17, C_DLCA), (0.17, C_DLCB)]

COUNTS = {8: 12, 11: 18, 15: 12, 20: 12}   # runs per speed column

fig, ax = plt.subplots(figsize=(8.4, 4.7), dpi=180)

# faint horizontal guides per seed row
for y in range(len(SEEDS)):
    ax.axhline(y, color=GRID, lw=0.8, zorder=0)

# markers
for xi, sp in enumerate(SPEEDS):
    for yi in range(len(SEEDS)):
        for dx, col in variants(sp):
            ax.scatter(xi + dx, yi, marker="s", s=200, c=col,
                       edgecolors="none", zorder=3)

# per-column run counts, just above the top row
for xi, sp in enumerate(SPEEDS):
    ax.text(xi, len(SEEDS) - 0.35, f"n = {COUNTS[sp]}",
            ha="center", va="bottom", fontsize=10, color=GRAY)

# axes cosmetics
ax.set_xlim(-0.6, len(SPEEDS) - 0.4)
ax.set_ylim(-0.7, len(SEEDS) + 0.1)
ax.set_xticks(range(len(SPEEDS)))
ax.set_xticklabels([f"{s} m/s" for s in SPEEDS], fontsize=11)
ax.set_yticks(range(len(SEEDS)))
ax.set_yticklabels(SEEDS, fontsize=11)
ax.set_xlabel("Hub-height wind speed", fontsize=12)
ax.set_ylabel("Turbulence / wave seed", fontsize=12)
ax.set_title("Simulation case matrix — 54 analysed OpenFAST runs",
             fontsize=14, pad=16)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
for spine in ("left", "bottom"):
    ax.spines[spine].set_color(GRAY)
ax.tick_params(length=0)

# legend -> right centre, outside the plot
handles = [
    Line2D([0], [0], marker="s", ls="none", ms=11, mfc=C_DLCA, mec="none",
           label="dlca — NTM wind, JONSWAP wave (seed A)"),
    Line2D([0], [0], marker="s", ls="none", ms=11, mfc=C_DLCB, mec="none",
           label="dlcb — NTM wind, decoupled wave seed"),
    Line2D([0], [0], marker="s", ls="none", ms=11, mfc=C_DLC16, mec="none",
           label="dlc16 — DLC 1.6 severe sea state (Hs 8.3 m, Tp 12.95 s)"),
]
ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5),
          frameon=False, fontsize=10, handletextpad=0.6, labelspacing=0.9)

out = OUT / "fig2-dlc-matrix.png"
plt.savefig(out, dpi=180, bbox_inches="tight", facecolor="white")
print("wrote", out)
