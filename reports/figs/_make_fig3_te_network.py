"""[SUPERSEDED for the paper — see _make_fig3_firewall_network.py]

WARNING: this generator applies a ">50% of cases significant" filter, under
which NO wind edge survives (none clears 50%), so it draws a wave-only fan that
hides the firewall — the paper's headline result — and contradicts the Figure 3
caption. The paper's Figure 3 is now produced by _make_fig3_firewall_network.py
(a two-driver network that keeps the wind edges and shows the wind->platform
absence explicitly). Do NOT run this script for the manuscript; it will
overwrite fig3-te-network.png with the wave-only version.

Generate Phase 6 TE causal-network figure (F3) from the Phase 4 table.

Reads reports/te_table.parquet, builds a NetworkX DiGraph via
analysis/te_pipeline.build_graph (mean te_frac edge weight, keeps only
edges significant in > 50% of cases), and renders a publication-quality
directed graph:

  - sources (Wind1VelX, Wave1Elev, ...) laid out on the left
  - response channels (PtfmPitch, RootMyc1, FAIRTEN*, ...) on the right
  - edge thickness ∝ mean TE_frac
  - edge label = TE_frac (%)
  - node colour by category (environment / motion / load / mooring)

Outputs:
  reports/te_graph.pkl                 (NetworkX DiGraph pickle)
  reports/figs/fig3-te-network.png     (publication figure)

Usage:
  python reports/figs/_make_fig3_te_network.py
  python reports/figs/_make_fig3_te_network.py --input reports/te_table.parquet
"""

from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis"))
from te_pipeline import build_graph  # noqa: E402


# -- channel categorisation for layout + colour --------------------------------

ENV_CHANNELS = {"Wind1VelX", "Wind1VelY", "Wind1VelZ", "Wave1Elev"}
MOTION_CHANNELS = {"PtfmHeave", "PtfmSurge", "PtfmSway",
                   "PtfmPitch", "PtfmRoll", "PtfmYaw"}
LOAD_CHANNELS = {"TwrBsMyt", "TwrBsMxt", "TwrBsMzt",
                 "RootMyc1", "RootMxc1", "RootMzc1",
                 "RootMyc2", "RootMxc2", "RootMzc2",
                 "RootMyc3", "RootMxc3", "RootMzc3"}
MOOR_CHANNELS = {"FAIRTEN1", "FAIRTEN2", "FAIRTEN3"}

CAT_COLORS = {
    "env":    "#5B9BD5",   # blue — wind/wave
    "motion": "#70AD47",   # green — platform DOFs
    "load":   "#C55A11",   # orange — structural loads
    "moor":   "#7030A0",   # purple — fairlead tensions
    "other":  "#A6A6A6",
}


def categorise(channel: str) -> str:
    if channel in ENV_CHANNELS: return "env"
    if channel in MOTION_CHANNELS: return "motion"
    if channel in LOAD_CHANNELS: return "load"
    if channel in MOOR_CHANNELS: return "moor"
    return "other"


def layered_positions(g: nx.DiGraph) -> dict:
    """Left-to-right layered layout: env on left, then motion, load, moor."""
    layers = {"env": [], "motion": [], "load": [], "moor": [], "other": []}
    for n in g.nodes():
        layers[categorise(n)].append(n)
    # Sort within layer for stable ordering
    for k in layers:
        layers[k].sort()

    pos = {}
    layer_x = {"env": 0.0, "motion": 1.5, "load": 3.0, "moor": 4.5, "other": 6.0}
    for layer, nodes in layers.items():
        if not nodes:
            continue
        n = len(nodes)
        for i, node in enumerate(nodes):
            y = (n - 1) / 2.0 - i  # centre vertically
            pos[node] = (layer_x[layer], y)
    return pos


def draw_network(g: nx.DiGraph, out_png: Path,
                 min_te_frac: float = 0.01) -> None:
    """Draw the TE causal network as a driver -> response fan.

    The project graph is a star: a single environmental driver (Wave1Elev)
    feeds every structural response.  A two-column "fan" layout — drivers on
    the left, response channels stacked on the right and ranked by TE_frac —
    keeps every node label inside its circle and pins each percentage to its
    own arrow (the old 4-column layout placed labels at straight-line
    midpoints, so curved fan edges collided and numbers landed on the wrong
    arrows).
    """
    import math
    from matplotlib.patches import Patch

    if g.number_of_edges() == 0:
        print("WARNING: graph has no edges; drawing empty placeholder.")

    # Edge filtering — drop tiny TE_frac edges to keep figure readable.
    g_draw = g.copy()
    to_remove = [(u, v) for u, v, d in g_draw.edges(data=True)
                 if abs(d.get("weight", 0.0)) < min_te_frac]
    g_draw.remove_edges_from(to_remove)
    if g_draw.number_of_edges() == 0 and g.number_of_edges() > 0:
        print(f"WARNING: all {g.number_of_edges()} edges below "
              f"min_te_frac={min_te_frac}; redrawing without filter.")
        g_draw = g.copy()

    # Drop now-isolated nodes so the layout only shows connected channels.
    used = {n for e in g_draw.edges() for n in e}
    g_draw.remove_nodes_from([n for n in list(g_draw.nodes())
                              if n not in used])

    # --- fan layout: drivers (no incoming edge) left, responses right -------
    sources = sorted(n for n in g_draw.nodes() if g_draw.in_degree(n) == 0)
    targets = [n for n in g_draw.nodes() if n not in sources]

    def in_weight(n):
        return sum(abs(d.get("weight", 0.0))
                   for _, _, d in g_draw.in_edges(n, data=True))
    targets.sort(key=in_weight, reverse=True)  # strongest at the top

    pos = {}
    x_src, x_tgt = 0.0, 3.4
    nt = max(len(targets), 1)
    for i, n in enumerate(targets):
        pos[n] = (x_tgt, (nt - 1) / 2.0 - i)
    ns = len(sources)
    for i, n in enumerate(sources):
        pos[n] = (x_src, (ns - 1) / 2.0 - i)
    if not pos:  # empty graph
        pos = {"(no edges)": (0.0, 0.0)}
        g_draw.add_node("(no edges)")

    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_axis_off()

    node_size = 4300

    # --- nodes (coloured by category) ---
    for cat, color in CAT_COLORS.items():
        nodes = [n for n in g_draw.nodes() if categorise(n) == cat]
        if not nodes:
            continue
        nx.draw_networkx_nodes(
            g_draw, pos, nodelist=nodes, node_color=color,
            node_size=node_size, edgecolors="white", linewidths=1.8, ax=ax,
        )
    nx.draw_networkx_labels(
        g_draw, pos, font_size=8, font_weight="bold",
        font_color="white", ax=ax,
    )

    # --- edges: width proportional to TE_frac, straight so labels stay true -
    weights = [abs(d.get("weight", 0.0))
               for _, _, d in g_draw.edges(data=True)]
    max_w = max(weights, default=1.0) or 1.0
    for u, v, d in g_draw.edges(data=True):
        lw = 1.0 + 6.0 * abs(d.get("weight", 0.0)) / max_w
        nx.draw_networkx_edges(
            g_draw, pos, edgelist=[(u, v)], width=lw,
            edge_color="#5A6B7B", alpha=0.75,
            arrows=True, arrowstyle="-|>", arrowsize=15,
            node_size=node_size, ax=ax,
        )

    # --- edge labels: pinned to the RIGHT of each target node so every -------
    #     percentage sits unambiguously on its own response channel ----------
    label_dx = 0.62  # horizontal offset right of the target-node centre
    for u, v, d in g_draw.edges(data=True):
        tx, ty = pos[v]
        ax.text(tx + label_dx, ty, f"{d['weight'] * 100:.1f}%",
                fontsize=10, fontweight="bold", color="#1F3864",
                ha="left", va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="#CBD5E1", linewidth=0.9, alpha=0.97))

    # --- column headers ---
    y_top = (max(p[1] for p in pos.values()) if pos else 0) + 0.9
    ax.text(x_src, y_top, "Environmental driver", ha="center", va="bottom",
            fontsize=11, fontweight="bold", color="#1F3864")
    ax.text(x_tgt, y_top, "Response channels", ha="center", va="bottom",
            fontsize=11, fontweight="bold", color="#1F3864")

    # --- legend ---
    legend_handles = []
    for cat, color in CAT_COLORS.items():
        if cat == "other":
            continue
        if not any(categorise(n) == cat for n in g_draw.nodes()):
            continue
        label = {"env": "Environment (wind/wave)",
                 "motion": "Platform motion DOF",
                 "load": "Structural load channel",
                 "moor": "Fairlead tension"}[cat]
        legend_handles.append(Patch(facecolor=color, edgecolor="white",
                                    label=label))
    if legend_handles:
        ax.legend(handles=legend_handles, loc="lower center",
                  bbox_to_anchor=(0.5, -0.02), ncol=4,
                  frameon=False, fontsize=9)

    ax.margins(x=0.12, y=0.10)

    n_edges = g.number_of_edges()
    n_shown = g_draw.number_of_edges()
    # Header = the TE_frac definition (replaces the old descriptive title).
    formula = (r"$TE_{\mathrm{frac}}(X\!\rightarrow\!Y)\;=\;"
               r"\frac{TE_{X\rightarrow Y}}{\mathrm{AIS}_Y}\;=\;"
               r"\frac{TE_{X\rightarrow Y}}{I\,(\,Y_{t+1}\,;\,Y_t^{(k)}\,)}$")
    fig.suptitle(formula, fontsize=17, y=0.965, color="#1F3864")
    fig.text(0.5, 0.905, r"edge weight = mean $TE_{\mathrm{frac}}$ over the 54 DLC cases",
             ha="center", va="top", fontsize=9.5, color="#64748B")

    fig.subplots_adjust(top=0.85, bottom=0.06, left=0.04, right=0.96)
    fig.savefig(out_png, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out_png}")


def summarise_graph(g: nx.DiGraph) -> None:
    print(f"\nGraph summary:")
    print(f"  Nodes: {g.number_of_nodes()}")
    print(f"  Edges: {g.number_of_edges()}")
    if g.number_of_edges() == 0:
        return
    print(f"\n  Top 10 edges by mean TE_frac:")
    edges = sorted(g.edges(data=True),
                   key=lambda e: abs(e[2].get("weight", 0)), reverse=True)
    for u, v, d in edges[:10]:
        print(f"    {u:14s} -> {v:14s}  "
              f"TE_frac={d['weight']*100:6.2f}%  "
              f"sig_frac={d['sig_frac']*100:5.1f}%  "
              f"n={d['n_cases']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path,
                    default=ROOT / "reports" / "te_table.parquet")
    ap.add_argument("--graph-out", type=Path,
                    default=ROOT / "reports" / "te_graph.pkl")
    ap.add_argument("--fig-out", type=Path,
                    default=Path(__file__).resolve().parent
                    / "fig3-te-network.png")
    ap.add_argument("--method", default="bivariate_te_ksg")
    ap.add_argument("--p-threshold", type=float, default=0.05)
    ap.add_argument("--min-te-frac", type=float, default=0.01,
                    help="Drop edges with |mean TE_frac| < this (default 0.01)")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"ERROR: input parquet not found: {args.input}",
              file=sys.stderr)
        print(f"Pull it from the server first:", file=sys.stderr)
        print(f"  scp <server>:.../reports/te_table.parquet "
              f"{args.input.parent}/", file=sys.stderr)
        return 1

    print(f"Loading {args.input} ...")
    df = pd.read_parquet(args.input)
    print(f"  {len(df)} rows, methods = {df['method'].unique().tolist()}")
    print(f"  {df['case'].nunique()} cases, "
          f"{df.groupby(['source','target']).ngroups} (src,tgt) pairs")

    g = build_graph(df, method=args.method, p_threshold=args.p_threshold)
    summarise_graph(g)

    args.graph_out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.graph_out, "wb") as fh:
        pickle.dump(g, fh)
    print(f"\nwrote {args.graph_out}")

    draw_network(g, args.fig_out, min_te_frac=args.min_te_frac)
    return 0


if __name__ == "__main__":
    sys.exit(main())
