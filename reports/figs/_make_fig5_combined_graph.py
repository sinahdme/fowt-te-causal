"""[SUPERSEDED for the paper — see _make_fig5_firewall_graph.py]

WARNING: this draws the broader original project's two-arm combined graph — a
"Sobol arm" of design variables (D_OCol, D_Pt, H_Pt, L_u) with Sobol S_T edges
alongside the TE edges. This paper performs no Sobol/design-parameter analysis,
so this image contradicts the Figure 5 caption (which describes a TE + SURD
firewall graph). The manuscript's Figure 5 is now produced by
_make_fig5_firewall_graph.py. Do NOT run this script for the manuscript; it will
overwrite fig5-combined-graph.png with the stale Sobol version.

Generate Phase 6 combined causal-graph figure (F5).

Merges the two methodology arms into a single directed graph:

  - **TE edges** (solid): time-varying environmental forcing
    (wind / wave → response channels). Read from reports/te_graph.pkl.
    Edge weight = mean TE_frac across DLC cases.

  - **Sobol edges** (dashed): constants-per-run design parameters
    (D_MCol, D_OCol, ..., EA, L_u → response channels). Read from
    data/raft_lhs_<suffix>_sobol.json. Edge weight = total-order Sₜ
    above a threshold (default Sₜ ≥ 0.1).

Output:
  reports/figs/fig5-combined-graph.png

Usage:
  python reports/figs/_make_fig5_combined_graph.py
  python reports/figs/_make_fig5_combined_graph.py --sobol-suffix v2-N256 \
      --sobol-threshold 0.15
"""

from __future__ import annotations

import argparse
import json
import pickle
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

# Sobol variable ordering — sims/run_raft_lhs.py:47
SOBOL_VARS = ["D_MCol", "D_OCol", "R_MO", "D_Pt", "H_Pt", "H_FB",
              "H_Draft", "EA", "L_u"]

# Sobol-channel-name → OpenFAST-channel-name mapping
SOBOL_CHANNEL_MAP = {
    "surge_std":  "PtfmSurge",  "sway_std":   "PtfmSway",
    "heave_std":  "PtfmHeave",  "roll_std":   "PtfmRoll",
    "pitch_std":  "PtfmPitch",  "yaw_std":    "PtfmYaw",
    "Tmoor0_std": "FAIRTEN1",   "Tmoor1_std": "FAIRTEN2",
    "Tmoor2_std": "FAIRTEN3",
}

CAT_COLORS = {
    "design": "#FFC000",   # yellow — Sobol design vars
    "env":    "#5B9BD5",   # blue — wind/wave
    "motion": "#70AD47",   # green
    "load":   "#C55A11",   # orange
    "moor":   "#7030A0",   # purple
    "other":  "#A6A6A6",
}


def categorise(n: str) -> str:
    if n in SOBOL_VARS: return "design"
    if n in {"Wind1VelX", "Wind1VelY", "Wave1Elev"}: return "env"
    if n.startswith("Ptfm"): return "motion"
    if n.startswith(("TwrBs", "Root")): return "load"
    if n.startswith(("FAIRTEN", "Tmoor")): return "moor"
    return "other"


def load_te_graph(pkl_path: Path) -> nx.DiGraph:
    if not pkl_path.exists():
        print(f"WARNING: TE graph pickle not found: {pkl_path}")
        print(f"  Drawing Sobol-only figure. Run "
              f"reports/figs/_make_fig3_te_network.py first.")
        return nx.DiGraph()
    with open(pkl_path, "rb") as fh:
        return pickle.load(fh)


def add_sobol_edges(g: nx.DiGraph, sobol_path: Path,
                    st_threshold: float) -> int:
    """Add Sₜ-above-threshold edges from each design var to each channel."""
    if not sobol_path.exists():
        print(f"WARNING: Sobol JSON not found: {sobol_path}")
        return 0
    d = json.loads(sobol_path.read_text())
    added = 0
    for ch_key, of_channel in SOBOL_CHANNEL_MAP.items():
        if ch_key not in d:
            continue
        st_vals = d[ch_key]["ST"]
        for var, st in zip(SOBOL_VARS, st_vals):
            if st < st_threshold:
                continue
            g.add_edge(var, of_channel,
                       weight=float(st),
                       edge_type="sobol",
                       sobol_channel=ch_key)
            added += 1
    # Mark TE edges with edge_type='te' (if not already present)
    for u, v, data in g.edges(data=True):
        data.setdefault("edge_type", "te")
    return added


def layered_positions(g: nx.DiGraph) -> dict:
    """5-column layout: design | env | motion | load | moor."""
    cols = {"design": [], "env": [], "motion": [], "load": [], "moor": [], "other": []}
    for n in g.nodes():
        cols[categorise(n)].append(n)
    for k in cols:
        cols[k].sort()

    layer_x = {"design": -2.0, "env": 0.0, "motion": 2.0,
               "load": 4.0, "moor": 6.0, "other": 8.0}
    pos = {}
    for cat, nodes in cols.items():
        if not nodes: continue
        n = len(nodes)
        for i, node in enumerate(nodes):
            y = ((n - 1) / 2.0 - i) * 1.6
            pos[node] = (layer_x[cat], y)
    return pos


def draw(g: nx.DiGraph, out_png: Path,
         te_min: float, sobol_min: float) -> None:
    pos = layered_positions(g)
    if not pos:
        print("Empty graph; nothing to draw.")
        return

    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    ax.set_axis_off()

    # --- nodes ---
    for cat, color in CAT_COLORS.items():
        nodes = [n for n in g.nodes() if categorise(n) == cat]
        if not nodes: continue
        nx.draw_networkx_nodes(
            g, pos, nodelist=nodes, node_color=color, node_size=5400,
            edgecolors="black", linewidths=1.6, alpha=0.95, ax=ax,
        )
    # Short display labels so the text fits inside the circles; the column
    # headers (Platform motion / Structural loads / Mooring tensions) supply
    # the context. Design-var symbols are already short and kept as-is.
    disp = {"Wave1Elev": "Wave", "Wind1VelX": "Wind",
            "PtfmHeave": "Heave", "PtfmPitch": "Pitch", "PtfmSurge": "Surge",
            "PtfmSway": "Sway", "PtfmYaw": "Yaw", "PtfmRoll": "Roll",
            "TwrBsMyt": "TwrBs", "RootMyc1": "RootMy", "RootMxc1": "RootMx",
            "FAIRTEN1": "FT1", "FAIRTEN2": "FT2", "FAIRTEN3": "FT3"}
    # Per-category label colour for contrast: dark text on the light nodes
    # (yellow design, blue env, green motion), white on the dark ones
    # (orange load, purple mooring).
    label_colors = {"design": "#101010", "env": "#101010", "motion": "#101010",
                    "load": "white", "moor": "white", "other": "#101010"}
    for cat in CAT_COLORS:
        cnodes = [n for n in g.nodes() if categorise(n) == cat]
        if not cnodes:
            continue
        nx.draw_networkx_labels(
            g, pos, labels={n: disp.get(n, n) for n in cnodes},
            font_size=14, font_weight="bold",
            font_color=label_colors[cat], ax=ax,
        )

    # --- edges split by type ---
    te_edges = [(u, v, d) for u, v, d in g.edges(data=True)
                if d.get("edge_type") == "te"]
    sobol_edges = [(u, v, d) for u, v, d in g.edges(data=True)
                   if d.get("edge_type") == "sobol"]

    if te_edges:
        max_w = max(abs(d["weight"]) for _, _, d in te_edges) or 1.0
        widths = [0.7 + 4.5 * abs(d["weight"]) / max_w
                  for _, _, d in te_edges]
        nx.draw_networkx_edges(
            g, pos, edgelist=[(u, v) for u, v, _ in te_edges],
            width=widths, alpha=0.7, edge_color="#1F3864",
            arrows=True, arrowstyle="-|>", arrowsize=15,
            style="solid", connectionstyle="arc3,rad=0.08",
            node_size=5400, ax=ax,
        )

    if sobol_edges:
        max_st = max(abs(d["weight"]) for _, _, d in sobol_edges) or 1.0
        widths = [0.5 + 3.5 * abs(d["weight"]) / max_st
                  for _, _, d in sobol_edges]
        nx.draw_networkx_edges(
            g, pos, edgelist=[(u, v) for u, v, _ in sobol_edges],
            width=widths, alpha=0.55, edge_color="#7F6000",
            arrows=True, arrowstyle="-|>", arrowsize=13,
            style="dashed", connectionstyle="arc3,rad=-0.12",
            node_size=5400, ax=ax,
        )

    # --- legend ---
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    node_handles = []
    label_map = {
        "design": "Design variable (Sobol arm)",
        "env":    "Environment (TE arm)",
        "motion": "Platform motion DOF",
        "load":   "Structural load",
        "moor":   "Fairlead tension",
    }
    for cat, label in label_map.items():
        if any(categorise(n) == cat for n in g.nodes()):
            node_handles.append(Patch(facecolor=CAT_COLORS[cat],
                                      edgecolor="black", label=label))
    edge_handles = [
        Line2D([0], [0], color="#1F3864", lw=2.0,
               label=f"TE edge (mean $TE_{{frac}}$ ≥ {te_min*100:.0f}%)"),
        Line2D([0], [0], color="#7F6000", lw=2.0, ls="--",
               label=f"Sobol edge ($S_T$ ≥ {sobol_min:.2f})"),
    ]
    leg1 = ax.legend(handles=node_handles, loc="upper left",
                     bbox_to_anchor=(0.0, 0.0), ncol=3,
                     frameon=False, fontsize=9)
    ax.add_artist(leg1)
    ax.legend(handles=edge_handles, loc="upper right",
              bbox_to_anchor=(1.0, 0.0), ncol=2,
              frameon=False, fontsize=9)

    # --- column headers ---
    y_top = max(p[1] for p in pos.values()) + 1.3
    for lbl, x in [("Design vars\n(Sobol arm)", -2.0),
                   ("Environment\n(TE arm)", 0.0),
                   ("Platform motion", 2.0),
                   ("Structural loads", 4.0),
                   ("Mooring tensions", 6.0)]:
        ax.text(x, y_top, lbl, ha="center", va="bottom",
                fontsize=12.5, fontweight="bold", color="#1F3864")

    # Internal title omitted — the slide caption carries it, and it would
    # collide with the column headers; keeps the header row clean.
    fig.subplots_adjust(top=0.95, bottom=0.06, left=0.02, right=0.98)
    fig.savefig(out_png, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out_png}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--te-graph", type=Path,
                    default=ROOT / "reports" / "te_graph.pkl")
    ap.add_argument("--sobol-suffix", default="v2-N64")
    ap.add_argument("--sobol-threshold", type=float, default=0.10)
    ap.add_argument("--te-min", type=float, default=0.01,
                    help="(legend annotation only — TE filtering happens in build_graph)")
    ap.add_argument("--fig-out", type=Path,
                    default=OUT / "fig5-combined-graph.png")
    args = ap.parse_args()

    g = load_te_graph(args.te_graph)
    print(f"TE graph: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")

    sobol_path = ROOT / "data" / f"raft_lhs_{args.sobol_suffix}_sobol.json"
    n_sobol = add_sobol_edges(g, sobol_path, args.sobol_threshold)
    print(f"Added {n_sobol} Sobol edges (S_T ≥ {args.sobol_threshold})")
    print(f"Combined graph: {g.number_of_nodes()} nodes, "
          f"{g.number_of_edges()} edges")

    draw(g, args.fig_out, args.te_min, args.sobol_threshold)
    return 0


if __name__ == "__main__":
    sys.exit(main())
