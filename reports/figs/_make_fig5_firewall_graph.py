# -*- coding: utf-8 -*-
"""Figure 5 — combined TE + SURD causal graph showing the firewall.

Supersedes the stale two-arm Sobol "combined causal graph" (design variables +
Sobol S_T edges) in _make_fig5_combined_graph.py, which the paper does not
support. Matches the manuscript caption/body: the wave-driven TE web, the wind
information captured by the controller (SURD), the controller organising
platform pitch, and the empty direct wind->platform edge (the firewall).

Reads reports/te_table.parquet for the wave TE_frac edges; the SURD values are
the paper's reported figures (wind->pitch-command redundancy ~0.40, §2.7/§3.3;
controller unique U:BldPitch1->PtfmPitch = 0.167, Figure 4c).

Writes reports/figs/fig5-combined-graph.png.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Patch
from matplotlib.lines import Line2D
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PARQUET = ROOT / "reports" / "te_table.parquet"
OUT = Path(__file__).resolve().parent / "fig5-combined-graph.png"

WAVE_C = "#2E75B6"; WIND_C = "#C00000"; CTRL_C = "#5B5BA6"; EDGE_WAVE = "#5A6B7B"
COL = {"motion": "#70AD47", "moor": "#7030A0", "load": "#C55A11"}
CAT = {"PtfmPitch": "motion", "PtfmHeave": "motion", "PtfmSurge": "motion",
       "TwrBsMyt": "load", "FAIRTEN3": "moor", "FAIRTEN2": "moor", "FAIRTEN1": "moor"}
LABEL = {"PtfmPitch": "Pitch", "PtfmHeave": "Heave", "PtfmSurge": "Surge",
         "TwrBsMyt": "TwrBs", "FAIRTEN3": "FT3", "FAIRTEN2": "FT2", "FAIRTEN1": "FT1"}
ORDER = ["PtfmPitch", "PtfmHeave", "PtfmSurge", "TwrBsMyt",
         "FAIRTEN3", "FAIRTEN2", "FAIRTEN1"]


def wave_edges():
    df = pd.read_parquet(PARQUET)
    m = df[df["method"] == "bivariate_te_ksg"]
    g = m.groupby(["source", "target"]).agg(sig=("significant", "mean"),
                                             te=("te_frac", "mean")).reset_index()
    return {r["target"]: r["te"] for _, r in g.iterrows()
            if r["source"] == "Wave1Elev" and r["sig"] > 0.5}


def circle(ax, xy, r, fc, label, fs=8.5):
    ax.add_patch(Circle(xy, r, facecolor=fc, edgecolor="white", lw=1.6, zorder=4))
    ax.text(*xy, label, ha="center", va="center", color="white",
            fontsize=fs, fontweight="bold", zorder=5)


def edge(ax, p0, p1, color, lw, dashed=False, alpha=0.85, rad=0.0):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle="-|>", mutation_scale=15, color=color, lw=lw,
        linestyle=(0, (4, 3)) if dashed else "solid", alpha=alpha,
        shrinkA=19, shrinkB=19, zorder=2,
        connectionstyle=f"arc3,rad={rad}"))


def main():
    W = wave_edges()
    fig, ax = plt.subplots(figsize=(12.5, 8))
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 10); ax.axis("off")
    r = 0.42
    wave_xy = (1.5, 7.7); wind_xy = (1.5, 2.3); ctrl_xy = (4.7, 4.35)
    x_tgt = 9.4
    ys = {t: 8.1 - i for i, t in enumerate(ORDER)}   # 8.1 .. 2.1
    plat = ["PtfmPitch", "PtfmHeave", "PtfmSurge"]

    # firewall band behind platform nodes
    py = [ys[t] for t in plat]
    ax.add_patch(FancyBboxPatch(
        (x_tgt - 0.7, min(py) - 0.58), 1.75, (max(py) - min(py)) + 1.16,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor="#C00000", alpha=0.08, edgecolor=WIND_C,
        linestyle=(0, (5, 3)), linewidth=1.6, zorder=1))
    ax.text(x_tgt + 1.55, sum(py) / len(py), "FIREWALL", ha="center", va="center",
            fontsize=12, fontweight="bold", color=WIND_C, rotation=90, zorder=6)

    # wave TE edges (solid), width ~ te_frac
    maxte = max(W.values())
    for t in ORDER:
        if t not in W:
            continue
        edge(ax, wave_xy, (x_tgt, ys[t]), EDGE_WAVE, 1.2 + 6 * W[t] / maxte)
        ax.text(x_tgt + 0.6, ys[t], f"{W[t]*100:.1f}%", ha="left", va="center",
                fontsize=9, fontweight="bold", color="#1F3864", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor="#CBD5E1", lw=0.8))

    # wind -> controller (SURD capture): thick red
    edge(ax, wind_xy, ctrl_xy, WIND_C, 3.4)
    ax.text(3.0, 3.05, "wind → pitch command\n(SURD ≈ 0.40)", ha="center", va="center",
            fontsize=8.5, color=WIND_C, style="italic", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor="#F0C4C4", lw=0.8))

    # controller -> platform pitch (unique info): indigo
    edge(ax, ctrl_xy, (x_tgt, ys["PtfmPitch"]), CTRL_C, 2.6, rad=-0.12)
    ax.text(6.9, 6.55, "U = 0.167", ha="center", va="center",
            fontsize=8.5, color=CTRL_C, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor="#C7C7E6", lw=0.8))

    # firewall: no direct wind -> platform
    ax.text(5.55, 4.95, "no direct\nwind → platform", ha="center", va="center",
            fontsize=8.2, color=WIND_C, style="italic", zorder=6)
    ax.text(5.55, 5.55, "✕", ha="center", va="center", fontsize=16,
            color=WIND_C, fontweight="bold", zorder=6)

    # nodes
    circle(ax, wave_xy, r, WAVE_C, "Wave", fs=8.5)
    circle(ax, wind_xy, r, WIND_C, "Wind", fs=8.5)
    circle(ax, ctrl_xy, r, CTRL_C, "BldPitch1", fs=7.4)
    for t in ORDER:
        circle(ax, (x_tgt, ys[t]), r, COL[CAT[t]], LABEL[t], fs=8)

    # headers
    ax.text(1.5, 9.2, "Drivers", ha="center", fontsize=11, fontweight="bold", color="#1F3864")
    ax.text(4.7, 9.2, "Controller", ha="center", fontsize=11, fontweight="bold", color="#1F3864")
    ax.text(x_tgt, 9.2, "Response channels", ha="center", fontsize=11, fontweight="bold", color="#1F3864")

    # legend
    handles = [
        Line2D([0], [0], color=EDGE_WAVE, lw=3, label="Wave TE edge (width ∝ TE_frac)"),
        Line2D([0], [0], color=WIND_C, lw=3, label="Wind → controller (SURD capture)"),
        Line2D([0], [0], color=CTRL_C, lw=2.6, label="Controller → platform (SURD unique)"),
        Patch(facecolor=CTRL_C, edgecolor="white", label="Control channel"),
        Patch(facecolor=COL["motion"], edgecolor="white", label="Platform motion DOF"),
        Patch(facecolor=COL["load"], edgecolor="white", label="Blade / tower load"),
        Patch(facecolor=COL["moor"], edgecolor="white", label="Fairlead tension"),
    ]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.05),
              ncol=4, frameon=False, fontsize=8.4)

    fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
