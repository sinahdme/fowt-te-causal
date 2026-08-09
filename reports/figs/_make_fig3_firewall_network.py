# -*- coding: utf-8 -*-
"""Figure 3 — directed TE network showing the firewall (two drivers).

Supersedes the wave-only fan in _make_fig3_te_network.py, which applied a
">50% of cases significant" filter that dropped every wind edge and therefore
hid the firewall (the paper's headline). This version keeps BOTH environmental
drivers:

  * Wave1Elev  — solid blue edges to the channels it drives (sig in >50% of the
                 54 cases); edge width proportional to mean TE_frac, labelled %.
  * Wind1VelX  — dashed red edges to the blade/tower channels it reaches
                 intermittently (labelled by fraction of cases significant), and
                 an explicit "firewall" annotation over the platform channels it
                 does NOT significantly reach (TE at the chance floor).

Reads reports/te_table.parquet. Writes reports/figs/fig3-te-network.png.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Patch
from matplotlib.lines import Line2D
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PARQUET = ROOT / "reports" / "te_table.parquet"
OUT = Path(__file__).resolve().parent / "fig3-te-network.png"

CAT = {
    "PtfmPitch": "motion", "PtfmHeave": "motion", "PtfmSurge": "motion",
    "FAIRTEN1": "moor", "FAIRTEN2": "moor", "FAIRTEN3": "moor",
    "TwrBsMyt": "load", "RootMxc1": "load", "RootMyc1": "load",
}
COL = {"motion": "#70AD47", "moor": "#7030A0", "load": "#C55A11"}
WAVE_C = "#2E75B6"; WIND_C = "#C00000"; EDGE_WAVE = "#5A6B7B"

# target order (top -> bottom): wave-driven cluster up top, wind-reached blades at the bottom
ORDER = ["FAIRTEN3", "FAIRTEN2", "PtfmPitch", "PtfmHeave", "PtfmSurge",
         "FAIRTEN1", "TwrBsMyt", "RootMxc1", "RootMyc1"]
PLATFORM = ["PtfmPitch", "PtfmHeave", "PtfmSurge"]
WIND_EDGES = ["TwrBsMyt", "RootMxc1", "RootMyc1"]   # sig in >=15% of cases


def load_edges():
    df = pd.read_parquet(PARQUET)
    m = df[df["method"] == "bivariate_te_ksg"]
    g = (m.groupby(["source", "target"])
           .agg(sig=("significant", "mean"), te=("te_frac", "mean"))
           .reset_index())
    d = {}
    for _, r in g.iterrows():
        d[(r["source"], r["target"])] = (r["sig"], r["te"])
    return d


def circle(ax, xy, r, fc, label, fs=8.5):
    ax.add_patch(Circle(xy, r, facecolor=fc, edgecolor="white", linewidth=1.6, zorder=4))
    ax.text(*xy, label, ha="center", va="center", color="white",
            fontsize=fs, fontweight="bold", zorder=5)


def edge(ax, p0, p1, color, lw, dashed=False, alpha=0.8):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle="-|>", mutation_scale=14, color=color, lw=lw,
        linestyle=(0, (4, 3)) if dashed else "solid", alpha=alpha,
        shrinkA=20, shrinkB=20, zorder=2))


def main():
    E = load_edges()
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off")

    x_src, x_tgt, r = 2.1, 8.7, 0.46
    ys = {t: 8.7 - i * 0.85 for i, t in enumerate(ORDER)}
    wave_xy = (x_src, 7.55); wind_xy = (x_src, 3.3)

    # firewall band behind the platform nodes
    py = [ys[t] for t in PLATFORM]
    ax.add_patch(FancyBboxPatch(
        (x_tgt - 0.72, min(py) - 0.6), 1.9, (max(py) - min(py)) + 1.2,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor="#C00000", alpha=0.08, edgecolor=WIND_C,
        linestyle=(0, (5, 3)), linewidth=1.6, zorder=1))

    # wave edges (solid), width ~ te_frac
    wave_ts = [t for t in ORDER if E.get(("Wave1Elev", t), (0, 0))[0] > 0.5]
    maxte = max(E[("Wave1Elev", t)][1] for t in wave_ts)
    for t in wave_ts:
        sig, te = E[("Wave1Elev", t)]
        edge(ax, wave_xy, (x_tgt, ys[t]), EDGE_WAVE, 1.2 + 6 * te / maxte)
        ax.text(x_tgt + 0.62, ys[t], f"{te*100:.1f}%", ha="left", va="center",
                fontsize=9.5, fontweight="bold", color="#1F3864", zorder=6,
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                          edgecolor="#CBD5E1", lw=0.8))

    # wind edges (dashed red) to blade/tower; label = fraction of cases significant
    for t in WIND_EDGES:
        sig, te = E[("Wind1VelX", t)]
        edge(ax, wind_xy, (x_tgt, ys[t]), WIND_C, 1.4, dashed=True, alpha=0.85)
        mx = (wind_xy[0] + x_tgt) / 2 + 0.3
        my = (wind_xy[1] + ys[t]) / 2 - 0.05
        ax.text(mx, my, f"sig {sig*100:.0f}%", ha="center", va="center",
                fontsize=8, color=WIND_C, style="italic", zorder=6,
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                          edgecolor="#F0C4C4", lw=0.7))

    # firewall: blocked wind->platform (dashed red stub with an X, no arrowhead reaching)
    bx, by = 5.4, 5.15
    ax.add_patch(FancyArrowPatch(
        (wind_xy[0] + 0.2, wind_xy[1] + 0.15), (bx, by), arrowstyle="-",
        color=WIND_C, lw=1.4, linestyle=(0, (4, 3)), alpha=0.7,
        shrinkA=20, shrinkB=6, zorder=2))
    ax.text(bx, by, "✕", ha="center", va="center", fontsize=17,
            color=WIND_C, fontweight="bold", zorder=6)
    ax.text(bx - 0.1, by - 0.55,
            "wind → platform:\nno significant edge",
            ha="center", va="top", fontsize=8.5, color=WIND_C,
            style="italic", zorder=6)
    ax.text(x_tgt + 2.15, sum(py) / len(py), "FIREWALL", ha="center", va="center",
            fontsize=12, fontweight="bold", color=WIND_C, rotation=90, zorder=6)

    # driver + target nodes
    circle(ax, wave_xy, r, WAVE_C, "Wave1Elev", fs=8)
    circle(ax, wind_xy, r, WIND_C, "Wind1VelX", fs=8)
    for t in ORDER:
        circle(ax, (x_tgt, ys[t]), r, COL[CAT[t]], t, fs=7.6)

    # headers
    ax.text(x_src, 9.55, "Environmental drivers", ha="center", fontsize=11.5,
            fontweight="bold", color="#1F3864")
    ax.text(x_tgt, 9.55, "Response channels", ha="center", fontsize=11.5,
            fontweight="bold", color="#1F3864")
    ax.text(5.4, 8.95,
            r"edge weight = mean $TE_{\mathrm{frac}}$ over the 54 cases",
            ha="center", fontsize=9.5, color="#64748B")

    # legend
    handles = [
        Line2D([0], [0], color=EDGE_WAVE, lw=3, label="Wave forcing (solid; width ∝ TE_frac)"),
        Line2D([0], [0], color=WIND_C, lw=1.6, linestyle=(0, (4, 3)),
               label="Wind forcing (dashed; intermittently significant)"),
        Patch(facecolor=COL["motion"], edgecolor="white", label="Platform motion DOF"),
        Patch(facecolor=COL["moor"], edgecolor="white", label="Fairlead tension"),
        Patch(facecolor=COL["load"], edgecolor="white", label="Blade / tower load"),
    ]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.04),
              ncol=3, frameon=False, fontsize=8.6)

    fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
