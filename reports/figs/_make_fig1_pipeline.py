# -*- coding: utf-8 -*-
"""Generate Figure 1 — the paper's methodology overview.

Replaces the stale `fig1-methodology-arms.png` (which depicted a two-arm
"TE arm + Sobol arm -> combined causal graph" hybrid from the broader original
project; this paper performs no Sobol/RAFT design-parameter analysis). This
figure matches the manuscript caption: three analysis arms — directed transfer
entropy, a linear coherence baseline, and SURD attribution — operate on the
same conditioned OpenFAST signals and feed the monitoring-signature construction.

Schematic only (no data). Writes reports/figs/fig1-methodology-arms.png.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent

BLUE_DARK="#1F3864"; BLUE_MID="#2E75B6"; BLUE_LIGHT="#D9E2F3"
ORANGE="#C55A11"; ORANGE_LIGHT="#FBE5D6"
GREEN="#548235"; GREEN_LIGHT="#E2EFDA"
GRAY="#595959"


def box(ax, xy, w, h, text, fc, ec, fontsize=10, fontweight="normal",
        textcolor="black", lw=1.5):
    x, y = xy
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor=fc, edgecolor=ec, linewidth=lw))
    if text:
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=fontsize, fontweight=fontweight, color=textcolor,
                linespacing=1.3)


def arrow(ax, start, end, color=GRAY, lw=1.8):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=2, shrinkB=2))


def make_fig1():
    fig, ax = plt.subplots(figsize=(12, 8.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off")

    ax.text(6.0, 9.6, "Methodology — three analysis arms on the same conditioned signals",
            ha="center", fontsize=14, fontweight="bold", color=BLUE_DARK)

    # Input + conditioning
    box(ax, (4.0, 8.5), 4.0, 0.7, "OpenFAST 54-case DLC campaign",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=11, fontweight="bold")
    box(ax, (3.1, 7.35), 5.8, 0.8,
        "Signal conditioning\ndrop 600 s transient  ·  decimate 40 → 5 Hz  ·  KSG jitter  ·  z-score",
        fc="white", ec=BLUE_MID, fontsize=9.5)
    arrow(ax, (6.0, 8.5), (6.0, 8.15), color=BLUE_DARK, lw=2.0)
    ax.text(6.0, 6.98, "the same conditioned signals feed three parallel arms",
            ha="center", fontsize=9.5, style="italic", color=GRAY)

    # Three arm panels
    panels = [
        dict(x=0.2, fc=ORANGE_LIGHT, ec=ORANGE, title="Directed transfer entropy",
             sub="primary — directed, model-free",
             boxes=["IDTxl bivariate + conditional KSG\n(JIDT  ·  circular-shift surrogates)",
                    "AIS-normalized effect size\n$TE_{\\mathrm{frac}}$ + permutation significance",
                    "Delay-resolved TE\n(coupling lag  ·  robustness)"],
             out="directed environment → response edges"),
        dict(x=4.15, fc=BLUE_LIGHT, ec=BLUE_MID, title="Linear coherence baseline",
             sub="linear foil",
             boxes=["Welch magnitude-squared\ncoherence  $\\gamma^2(f)$",
                    "linear-spectrum ceiling:\nreports an apparent wind–platform\nlink that TE refutes"],
             out="undirected apparent links"),
        dict(x=8.1, fc=GREEN_LIGHT, ec=GREEN, title="SURD attribution",
             sub="mechanism",
             boxes=["synergistic / unique / redundant\ndecomposition",
                    "wind information redirected\ninto the blade-pitch command",
                    "open-loop twin\n(controller removed)"],
             out="where wind information goes"),
    ]
    pw, ptop, pbot = 3.75, 6.6, 2.5
    for p in panels:
        x = p["x"]; cx = x + pw/2
        box(ax, (x, pbot), pw, ptop-pbot, "", fc=p["fc"], ec=p["ec"], lw=2)
        ax.text(cx, ptop-0.33, p["title"], ha="center", fontsize=11.5,
                fontweight="bold", color=p["ec"])
        ax.text(cx, ptop-0.62, p["sub"], ha="center", fontsize=9,
                style="italic", color=p["ec"])
        arrow(ax, (6.0, 7.35), (cx, ptop), color=BLUE_MID, lw=1.6)
        n = len(p["boxes"])
        # stack sub-boxes between y=5.5 and y=3.05
        top, bottom = 5.5, 3.05
        bh = (top - bottom - 0.15*(n-1)) / n
        for i, t in enumerate(p["boxes"]):
            by = top - bh - i*(bh+0.15)
            box(ax, (x+0.2, by), pw-0.4, bh, t, fc="white", ec=p["ec"],
                fontsize=8.6)
        ax.text(cx, 2.78, "Output:  " + p["out"], ha="center", fontsize=8.0,
                fontweight="bold", color=p["ec"])
        arrow(ax, (cx, pbot), (6.0 + (cx-6.0)*0.28, 1.82), color=p["ec"], lw=1.8)

    # Monitoring signature (convergence)
    box(ax, (2.5, 0.55), 7.0, 1.25,
        "Monitoring-signature construction\n"
        "Healthy TE(wind → platform) sits at a near-zero, tightly bounded baseline —\n"
        "a breach (wind re-entering platform motion) is the fault diagnostic",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=10, fontweight="bold")

    out = OUT / "fig1-methodology-arms.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    make_fig1()
