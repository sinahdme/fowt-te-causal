"""Extra figures for the conference deck — concept + result visualizations.
All result numbers are taken verbatim from reports/conference-outline.md
(preliminary single-condition, 11 m/s, DLC-A seed s00). Ocean Gradient palette.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent
DEEP = "#065A82"; TEAL = "#1C7293"; MID = "#21295C"; SEA = "#00A896"
MINT = "#02C39A"; INK = "#1E293B"; GREY = "#64748B"; LIGHT = "#EAF2F5"; CORAL = "#B85042"

plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.facecolor": "white",
                     "figure.facecolor": "white"})


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------------------
# 1. Concept: what transfer entropy measures (predictive view)
# ---------------------------------------------------------------------------
def fig_concept():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 5)

    def box(x, y, w, h, fc, ec, text, tc, fs=12, bold=True):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                     fc=fc, ec=ec, lw=2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=tc,
                fontsize=fs, fontweight="bold" if bold else "normal")

    # target future (the thing we predict)
    box(7.2, 2.0, 2.4, 1.0, LIGHT, MID, "Y's next value\n$Y_t$", MID, 13)
    # target own past
    box(0.4, 3.2, 3.4, 1.1, "#E6EDF0", GREY, "Target's own past\n$Y_{t-1}, Y_{t-2}, \\dots$", INK, 12)
    # source past (highlighted)
    box(0.4, 0.7, 3.4, 1.1, "#D7EAF2", DEEP, "Source's past\n$X_{t-1}, X_{t-2}, \\dots$", DEEP, 12)

    ax.add_patch(FancyArrowPatch((3.8, 3.75), (7.2, 2.75), arrowstyle="-|>", mutation_scale=22,
                 color=GREY, lw=2.2))
    ax.text(5.5, 3.55, "baseline prediction", color=GREY, fontsize=10.5, ha="center", style="italic")
    ax.add_patch(FancyArrowPatch((3.8, 1.25), (7.2, 2.25), arrowstyle="-|>", mutation_scale=22,
                 color=DEEP, lw=3.0))
    ax.text(4.9, 2.18, "extra information?", color=DEEP, fontsize=11, ha="center", fontweight="bold")

    ax.text(5.0, 4.75, "Does the source's past add predictive information,",
            ha="center", fontsize=13.5, color=MID, fontweight="bold")
    ax.text(5.0, 4.4, "beyond the target's own past?", ha="center", fontsize=13.5, color=MID, fontweight="bold")

    ax.add_patch(FancyBboxPatch((1.7, -0.55), 6.6, 0.85, boxstyle="round,pad=0.04,rounding_size=0.1",
                 fc=MID, ec="none"))
    ax.text(5.0, -0.12, r"$\mathrm{TE}_{X\to Y} = I\,(\,Y_t\ ;\ X_{\mathrm{past}}\ \mid\ Y_{\mathrm{past}}\,)$",
            ha="center", va="center", color="white", fontsize=15)
    ax.set_ylim(-0.7, 5.1)
    save(fig, "conf-te-concept.png")


# ---------------------------------------------------------------------------
# 2. Headline result — wind vs wave (horizontal bars)
# Data-driven from reports/te_table.parquet (full 54-case campaign) via the
# same build_graph rule used by the network figure, so the two never drift
# apart. Edge weight shown in nats. Across the campaign no wind -> structure
# edge survives the >50%-of-cases significance rule, so the chart is wave-only.
# ---------------------------------------------------------------------------
def _campaign_edges():
    """Return [(label, te_nats, kind), ...] for edges significant in >50% of
    cases, sorted descending by mean TE (nats). kind is 'wave' or 'wind'."""
    import sys
    import pandas as pd
    ROOT = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(ROOT / "analysis"))
    from te_pipeline import build_graph
    df = pd.read_parquet(ROOT / "reports" / "te_table.parquet")
    g = build_graph(df, method="bivariate_te_ksg", p_threshold=0.05)
    pretty = lambda n: n.replace("Wave1Elev", "Wave").replace("Wind1VelX", "Wind")
    edges = [(f"{pretty(u)} → {v}", float(d["mean_te_nats"]),
              "wind" if u == "Wind1VelX" else "wave")
             for u, v, d in g.edges(data=True)]
    edges.sort(key=lambda e: e[1], reverse=True)
    return edges


def fig_windwave():
    edges = _campaign_edges()
    n_total = 18  # 2 sources x 9 response channels
    has_wind = any(e[2] == "wind" for e in edges)
    edges = edges[::-1]  # smallest at bottom for barh
    labels = [e[0] for e in edges]
    vals = [e[1] for e in edges]
    cols = [DEEP if e[2] == "wave" else SEA for e in edges]
    xmax = max(vals) * 1.18

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    y = np.arange(len(edges))
    ax.barh(y, vals, color=cols, height=0.62)
    for yi, v, e in zip(y, vals, edges):
        ax.text(v + xmax * 0.012, yi, f"{v:.3f}", va="center", ha="left",
                fontsize=11.5, color=(DEEP if e[2] == "wave" else SEA),
                fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=12, fontfamily="monospace")
    ax.set_xlabel("transfer entropy  (nats)", fontsize=12, color=MID)
    ax.set_xlim(0, xmax)
    ax.set_title(f"Significant directed transfer — wave only "
                 f"({len(edges)} of {n_total} edges)",
                 fontsize=15, color=MID, fontweight="bold", pad=10)
    from matplotlib.patches import Patch
    handles = [Patch(color=DEEP, label="wave → structure")]
    if has_wind:
        handles.append(Patch(color=SEA, label="wind → structure"))
    ax.legend(handles=handles, frameon=False, fontsize=11, loc="lower right")
    if not has_wind:
        ax.text(0.97, 0.40, "no wind → structure edge\nis significant",
                transform=ax.transAxes, ha="right", va="center",
                fontsize=10.5, color=SEA, style="italic")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    save(fig, "conf-windwave-bars.png")


# ---------------------------------------------------------------------------
# 3. Ablation — controller on vs off
# ---------------------------------------------------------------------------
def fig_ablation():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.3), gridspec_kw={"width_ratios": [1.5, 1]})

    # panel A: wind -> structure edges
    ax = axes[0]
    names = ["Wind → PtfmHeave", "Wind → FAIRTEN2"]
    on = [0.000, 0.042]; off = [0.017, 0.000]
    x = np.arange(len(names)); w = 0.36
    ax.bar(x - w / 2, on, w, label="controller ON", color=GREY)
    ax.bar(x + w / 2, off, w, label="controller OFF (open-loop)", color=DEEP)
    for xi, v in zip(x - w / 2, on):
        ax.text(xi, v + 0.001, f"{v:.3f}", ha="center", va="bottom", fontsize=10, color=GREY)
    for xi, v in zip(x + w / 2, off):
        ax.text(xi, v + 0.001, f"{v:.3f}", ha="center", va="bottom", fontsize=10, color=DEEP, fontweight="bold")
    ax.annotate("appears", xy=(w / 2 - 0.13, 0.0168), xytext=(-0.12, 0.032), color=DEEP,
                fontsize=10.5, fontweight="bold", va="center",
                arrowprops=dict(arrowstyle="->", color=DEEP, lw=1.4))
    ax.annotate("vanishes", xy=(1 - w / 2 + 0.13, 0.0418), xytext=(1.06, 0.052), color=GREY,
                fontsize=10.5, fontweight="bold", va="center",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.4))
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=10.5, fontfamily="monospace")
    ax.set_ylabel("TE (nats)", fontsize=11.5, color=MID)
    ax.set_title("Wind → structure edges", fontsize=13, color=MID, fontweight="bold")
    ax.set_ylim(0, 0.062)
    ax.legend(frameon=False, fontsize=10, loc="upper center")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    # panel B: AIS inflation (the confound)
    ax = axes[1]
    ax.bar([0, 1], [1.50, 2.05], width=0.5, color=[GREY, CORAL])
    for xi, v in zip([0, 1], [1.50, 2.05]):
        ax.text(xi, v + 0.03, f"{v:.2f}", ha="center", va="bottom", fontsize=11,
                color=(GREY if xi == 0 else CORAL), fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["ON", "OFF"], fontsize=11)
    ax.set_ylabel("AIS RootMyc1 (nats)", fontsize=11.5, color=MID)
    ax.set_title("the confound:\nself-info inflates", fontsize=12.5, color=CORAL, fontweight="bold")
    ax.set_ylim(0, 2.45)
    ax.annotate("masks wind\nin bivariate TE", xy=(0.78, 2.02), xytext=(0.42, 1.55), color=CORAL,
                fontsize=9.5, ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.3))
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=GREY, label="controller ON"),
                       Patch(facecolor=CORAL, label="controller OFF")],
              frameon=False, fontsize=9, loc="upper left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.suptitle("Controller-off ablation — suggestive but confounded", fontsize=14.5,
                 color=MID, fontweight="bold", y=1.02)
    fig.tight_layout()
    save(fig, "conf-ablation.png")


if __name__ == "__main__":
    fig_concept()
    fig_windwave()
    fig_ablation()
    print("done")
