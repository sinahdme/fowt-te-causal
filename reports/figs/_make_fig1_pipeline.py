# -*- coding: utf-8 -*-
"""Generate Figure 1 — the paper's methodology overview.

Replaces the stale two-arm/Sobol `fig1-methodology-arms.png`. Matches the
manuscript caption: three analysis arms — directed transfer entropy, a linear
coherence baseline, and SURD attribution — operate on the same conditioned
OpenFAST signals and feed the monitoring-signature construction.

Deliberately light on text (conditioning details and estimator settings live in
the Methods text, not the figure). Schematic only. Writes fig1-methodology-arms.png.
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
    fig, ax = plt.subplots(figsize=(12, 8.4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off")

    ax.text(6.0, 9.6, "Methodology — three analysis arms on the same conditioned signals",
            ha="center", fontsize=14, fontweight="bold", color=BLUE_DARK)

    # Input + conditioning (kept minimal; details are in the Methods text)
    box(ax, (4.0, 8.5), 4.0, 0.7, "OpenFAST 54-case DLC campaign",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=11, fontweight="bold")
    box(ax, (4.3, 7.5), 3.4, 0.62, "Signal conditioning",
        fc="white", ec=BLUE_MID, fontsize=11)
    arrow(ax, (6.0, 8.5), (6.0, 8.12), color=BLUE_DARK, lw=2.0)

    panels = [
        dict(x=0.15, fc=ORANGE_LIGHT, ec=ORANGE, title="Directed transfer entropy",
             sub="primary — directed, model-free",
             boxes=["IDTxl bivariate + conditional KSG\n(JIDT · circular-shift surrogates)",
                    "AIS-normalized effect size\n$TE_{\\mathrm{frac}}$ + permutation significance",
                    "Delay-resolved TE\n(coupling lag · robustness)"]),
        dict(x=4.1, fc=BLUE_LIGHT, ec=BLUE_MID, title="Linear coherence baseline",
             sub="linear foil",
             boxes=["Welch magnitude-squared\ncoherence  $\\gamma^2(f)$",
                    "linear-spectrum ceiling:\nan apparent wind–platform link\nthat TE refutes"]),
        dict(x=8.05, fc=GREEN_LIGHT, ec=GREEN, title="SURD attribution",
             sub="mechanism",
             boxes=["synergistic / unique / redundant\ndecomposition",
                    "wind information redirected\ninto the blade-pitch command",
                    "open-loop twin\n(controller removed)"]),
    ]
    pw, ptop, pbot = 3.85, 6.6, 2.4
    for p in panels:
        x = p["x"]; cx = x + pw / 2
        box(ax, (x, pbot), pw, ptop - pbot, "", fc=p["fc"], ec=p["ec"], lw=2)
        ax.text(cx, ptop - 0.34, p["title"], ha="center", fontsize=11.5,
                fontweight="bold", color=p["ec"])
        ax.text(cx, ptop - 0.64, p["sub"], ha="center", fontsize=9,
                style="italic", color=p["ec"])
        arrow(ax, (6.0, 7.5), (cx, ptop), color=BLUE_MID, lw=1.6)
        n = len(p["boxes"])
        top, bottom = 5.5, 2.75
        bh = (top - bottom - 0.18 * (n - 1)) / n
        for i, t in enumerate(p["boxes"]):
            by = top - bh - i * (bh + 0.18)
            box(ax, (x + 0.22, by), pw - 0.44, bh, t, fc="white", ec=p["ec"],
                fontsize=8.6)
        arrow(ax, (cx, pbot), (6.0 + (cx - 6.0) * 0.30, 1.82), color=p["ec"], lw=1.8)

    # Monitoring signature (convergence) — concise
    box(ax, (3.0, 0.5), 6.0, 1.25,
        "Monitoring-signature construction\n"
        "healthy baseline: TE(wind → platform) ≈ 0\n"
        "a breach is the fault diagnostic",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=11, fontweight="bold")

    out = OUT / "fig1-methodology-arms.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    make_fig1()
