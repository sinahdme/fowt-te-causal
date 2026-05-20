"""Generate the three figures for the technical report (v2 — improved text layout).

Produces:
  reports/figs/fig1-methodology-arms.png
  reports/figs/fig2-dlc-matrix.png
  reports/figs/fig3-te-pipeline.png

Key changes vs v1: larger boxes, pre-wrapped text with explicit \\n, smaller
fonts where boxes are tight, more vertical padding so labels don't touch
box edges.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent

# Color palette
BLUE_DARK = "#1F3864"
BLUE_MID = "#2E75B6"
BLUE_LIGHT = "#D9E2F3"
ORANGE = "#C55A11"
ORANGE_LIGHT = "#FBE5D6"
GREEN = "#548235"
GREEN_LIGHT = "#E2EFDA"
GRAY = "#595959"
GRAY_LIGHT = "#F2F2F2"


def box(ax, xy, w, h, text, fc, ec, fontsize=10, fontweight="normal",
        textcolor="black", lw=1.5):
    x, y = xy
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.05,rounding_size=0.12",
        facecolor=fc, edgecolor=ec, linewidth=lw,
    )
    ax.add_patch(rect)
    if text:
        ax.text(x + w / 2, y + h / 2, text,
                ha="center", va="center",
                fontsize=fontsize, fontweight=fontweight, color=textcolor,
                linespacing=1.3)


def arrow(ax, start, end, color=GRAY, lw=1.8):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=2, shrinkB=2))


# ============================================================================
# Figure 1 — Methodology arms
# ============================================================================

def make_fig1():
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    # Title at the very top
    ax.text(5.5, 9.2, "Hybrid methodology — two arms feed one causal graph",
            ha="center", fontsize=13, fontweight="bold", color=BLUE_DARK)

    # Research question at top
    box(ax, (2.5, 7.6), 6.0, 1.0,
        "Research question\n\nCausal effect of (environment + design parameters)\non FOWT response",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=10.5, fontweight="bold")

    # Two arms — wider, taller, more padding
    # TE arm
    box(ax, (0.3, 2.9), 5.0, 4.2, "", fc=ORANGE_LIGHT, ec=ORANGE, lw=2)
    ax.text(2.8, 6.7, "TE arm",
            ha="center", fontsize=12.5, fontweight="bold", color=ORANGE)
    ax.text(2.8, 6.35, "time-varying environment",
            ha="center", fontsize=9.5, style="italic", color=ORANGE)

    box(ax, (0.7, 5.4), 4.2, 0.75,
        "OpenFAST DLC matrix\n(time-domain, 54 cases)",
        fc="white", ec=ORANGE, fontsize=10)
    box(ax, (0.7, 4.4), 4.2, 0.75,
        "IDTxl bivariate + conditional KSG\n(JIDT, circular-shift surrogates)",
        fc="white", ec=ORANGE, fontsize=10)
    box(ax, (0.7, 3.4), 4.2, 0.75,
        "AIS normalisation + Granger / coherence\nlinear baselines (apples-to-apples)",
        fc="white", ec=ORANGE, fontsize=9.5)
    ax.text(2.8, 3.05, "Output:  directed environment → response edges",
            ha="center", fontsize=9.5, fontweight="bold", color=ORANGE)

    # Sobol arm
    box(ax, (5.7, 2.9), 5.0, 4.2, "", fc=GREEN_LIGHT, ec=GREEN, lw=2)
    ax.text(8.2, 6.7, "Sobol arm",
            ha="center", fontsize=12.5, fontweight="bold", color=GREEN)
    ax.text(8.2, 6.35, "constant design parameters",
            ha="center", fontsize=9.5, style="italic", color=GREEN)

    box(ax, (6.1, 5.4), 4.2, 0.75,
        "RAFT Saltelli ensemble\n(frequency-domain, 9 vars × N)",
        fc="white", ec=GREEN, fontsize=10)
    box(ax, (6.1, 4.4), 4.2, 0.75,
        "SALib Sobol decomposition\n(first-order S₁ + total-order S_T)",
        fc="white", ec=GREEN, fontsize=10)
    box(ax, (6.1, 3.4), 4.2, 0.75,
        "KSG mutual-information ranking\n(IDTxl — nonlinear companion)",
        fc="white", ec=GREEN, fontsize=10)
    ax.text(8.2, 3.05, "Output:  parameter → response edges",
            ha="center", fontsize=9.5, fontweight="bold", color=GREEN)

    # Arrows from question to arms
    arrow(ax, (4.5, 7.6), (3.0, 7.1), color=BLUE_DARK, lw=2.0)
    arrow(ax, (6.5, 7.6), (8.0, 7.1), color=BLUE_DARK, lw=2.0)

    # Combined causal graph at bottom
    box(ax, (2.0, 0.9), 7.0, 1.6,
        "Combined causal graph (Phase 6)\n\n"
        "Directed, weighted, multivariate.   Edge weight = TE_frac (env edges)\n"
        "or Sobol-S_T (parameter edges).   NetworkX DiGraph + figures.",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=10.5, fontweight="bold")

    # Arrows from both arms down to the graph
    arrow(ax, (2.8, 2.9), (4.0, 2.5), color=ORANGE, lw=2.0)
    arrow(ax, (8.2, 2.9), (7.0, 2.5), color=GREEN, lw=2.0)

    # Caption note at the very bottom
    ax.text(5.5, 0.35,
            "Why both:  TE applies only to time series; design parameters are constants per simulation.\n"
            "The hybrid produces a single graph that ranks environmental and design contributions together.",
            ha="center", fontsize=9, color=GRAY, style="italic", linespacing=1.4)

    plt.tight_layout()
    out = OUT / "fig1-methodology-arms.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Wrote {out}")


# ============================================================================
# Figure 2 — DLC matrix
# ============================================================================

def make_fig2():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    # Title
    ax.text(6.5, 8.0,
            "Phase 2 Design Load Case matrix",
            ha="center", fontsize=13.5, fontweight="bold", color=BLUE_DARK)
    ax.text(6.5, 7.6,
            "54 OpenFAST cases × 1 hour simulated time each = 14 GB raw .outb",
            ha="center", fontsize=10.5, color=GRAY, style="italic")

    # Three DLC bins — wider boxes with more vertical padding
    bins = [
        {
            "x": 0.3, "name": "DLC-1.6",
            "subtitle": "predecessor cross-comparability",
            "wind": "Wind:  NTM  V = 11 m/s",
            "wave": "Wave:  SSS  Hs = 8.3 m,  Tp = 12.95 s",
            "seeds": "Seeds:  6  (correlated wind–wave seed)",
            "count": "6 cases",
            "fc": ORANGE_LIGHT, "ec": ORANGE,
        },
        {
            "x": 4.4, "name": "DLC-A",
            "subtitle": "primary TE test — H1, H2",
            "wind": "Wind:  NTM  V = 8 / 11 / 15 / 20 m/s",
            "wave": "Wave:  JONSWAP  correlated wind–wave seed",
            "seeds": "Seeds:  6 per wind speed",
            "count": "24 cases",
            "fc": BLUE_LIGHT, "ec": BLUE_MID,
        },
        {
            "x": 8.5, "name": "DLC-B",
            "subtitle": "conditional-TE validation — H3",
            "wind": "Wind:  same wind seeds as DLC-A",
            "wave": "Wave:  JONSWAP  decoupled\n            (wind_seed XOR 0x5A5A5A5A)",
            "seeds": "Seeds:  6 per wind speed",
            "count": "24 cases",
            "fc": GREEN_LIGHT, "ec": GREEN,
        },
    ]

    for d in bins:
        box(ax, (d["x"], 3.3), 4.1, 3.7, "", fc=d["fc"], ec=d["ec"], lw=2)
        cx = d["x"] + 2.05
        ax.text(cx, 6.6, d["name"],
                ha="center", fontsize=13, fontweight="bold", color=d["ec"])
        ax.text(cx, 6.25, d["subtitle"],
                ha="center", fontsize=9, color=GRAY, style="italic")
        ax.text(cx, 5.65, d["wind"], ha="center", fontsize=9.5)
        ax.text(cx, 5.20, d["wave"], ha="center", fontsize=9.5, linespacing=1.3)
        ax.text(cx, 4.55, d["seeds"], ha="center", fontsize=9.5)
        ax.text(cx, 3.80, "→  " + d["count"],
                ha="center", fontsize=12, fontweight="bold", color=d["ec"])

    # "What each DLC tests" panel
    box(ax, (0.3, 0.9), 12.3, 1.8, "", fc=GRAY_LIGHT, ec=GRAY)
    ax.text(6.5, 2.45, "What each DLC tests",
            ha="center", fontsize=11, fontweight="bold")

    ax.text(0.7, 1.95, "•  DLC-1.6 alone:",
            ha="left", fontsize=9.5, fontweight="bold")
    ax.text(3.1, 1.95,
            "cross-comparability with Jeon (2025);  wave-dominant regime baseline",
            ha="left", fontsize=9.5)

    ax.text(0.7, 1.55, "•  DLC-A alone:",
            ha="left", fontsize=9.5, fontweight="bold")
    ax.text(3.1, 1.55,
            "absolute TE values for H1 (wind → pitch), H2 (wave → heave), H6 (TE-PSD peak)",
            ha="left", fontsize=9.5)

    ax.text(0.7, 1.15, "•  DLC-A ↔ DLC-B contrast:",
            ha="left", fontsize=9.5, fontweight="bold")
    ax.text(3.9, 1.15,
            "tests H3 — conditional TE must shrink more under correlated forcing",
            ha="left", fontsize=9.5)

    # Footer note
    ax.text(6.5, 0.35,
            "9 response channels logged (Q1 lockdown):"
            "  3 structural loads,  3 platform motions,  3 mooring tensions",
            ha="center", fontsize=9, color=GRAY, style="italic")

    plt.tight_layout()
    out = OUT / "fig2-dlc-matrix.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Wrote {out}")


# ============================================================================
# Figure 3 — TE pipeline (per-case)
# ============================================================================

def make_fig3():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    ax.text(7.25, 9.0, "Phase 4 — per-case TE pipeline (analysis/te_pipeline.py)",
            ha="center", fontsize=13.5, fontweight="bold", color=BLUE_DARK)
    ax.text(7.25, 8.55, "applied to every .outb file in the DLC matrix",
            ha="center", fontsize=10, color=GRAY, style="italic")

    # ---- Row 1: preprocessing chain ----
    y1 = 6.6
    h1 = 1.1
    boxes_row1 = [
        ("OpenFAST\n.outb\n40 Hz, 3600 s", 0.3, BLUE_LIGHT, BLUE_MID),
        ("Drop transient\n(first 600 s)", 2.6, BLUE_LIGHT, BLUE_MID),
        ("Decimate\n40 → 5 Hz", 4.9, BLUE_LIGHT, BLUE_MID),
        ("Jitter\n1e-10 Gaussian", 7.2, BLUE_LIGHT, BLUE_MID),
        ("Z-score\nnormalise", 9.5, BLUE_LIGHT, BLUE_MID),
        ("Cached array\nN = 15 001", 11.8, "white", BLUE_MID),
    ]
    for label, x, fc, ec in boxes_row1:
        box(ax, (x, y1), 2.0, h1, label, fc=fc, ec=ec, fontsize=9.5)
    for i in range(len(boxes_row1) - 1):
        x1 = boxes_row1[i][1] + 2.0
        x2 = boxes_row1[i + 1][1]
        arrow(ax, (x1, y1 + h1 / 2), (x2, y1 + h1 / 2), color=BLUE_MID)

    # ---- Banner between row 1 and row 2 ----
    ax.text(7.25, 5.85,
            "For each (source, response) pair:   sources ∈ {Wind1VelX, Wave1Elev},   responses ∈ {9 channels}",
            ha="center", fontsize=10.5, fontweight="bold", color=BLUE_DARK)

    # ---- Row 2: per-pair analyses, five columns ----
    y2 = 2.8
    col_w = 2.6
    col_h = 2.6
    spacing = 0.15
    cols = [
        ("AIS\nper response", "Active Information\nStorage (KSG)",
         "Effect-size denominator\n(Wollstadt 2019)", ORANGE_LIGHT, ORANGE),
        ("Bivariate TE\nKSG", "BivariateTE\nJidtKraskovCMI",
         "200 circular surrogates\n→ p-value, significance", ORANGE_LIGHT, ORANGE),
        ("Conditional TE\nKSG", "MultivariateTE\nJidtKraskovCMI",
         "Greedy parent-set\nover both env sources", ORANGE_LIGHT, ORANGE),
        ("Granger\nbaseline", "MultivariateTE\nJidtGaussianCMI",
         "Same IDTxl pipeline,\nlinear estimator", BLUE_LIGHT, BLUE_MID),
        ("Coherence γ²(f)\nbaseline", "scipy.signal.coherence",
         "Linear-spectrum ceiling\npeak in 0.01–0.5 Hz", BLUE_LIGHT, BLUE_MID),
    ]
    x_start = 0.3
    for i, (label, sub, footer, fc, ec) in enumerate(cols):
        x = x_start + i * (col_w + spacing)
        # Header (title)
        box(ax, (x, y2 + 1.85), col_w, 0.75, label,
            fc=fc, ec=ec, fontsize=10, fontweight="bold")
        # Middle (what)
        box(ax, (x, y2 + 0.95), col_w, 0.8, sub,
            fc="white", ec=ec, fontsize=9)
        # Bottom (why)
        box(ax, (x, y2 + 0.05), col_w, 0.8, footer,
            fc="white", ec=ec, fontsize=8.5)
        # Arrow from preprocessing row to column header
        arrow(ax, (x + col_w / 2, y1), (x + col_w / 2, y2 + col_h),
              color=GRAY, lw=1.2)

    # ---- Row 3: aggregation ----
    box(ax, (0.3, 0.7), 6.7, 1.4,
        "Per-case long-form DataFrame\n\n"
        "rows: (case, source, target, method)\n"
        "cols: TE_nats, p_value, AIS, TE_frac, γ²_peak, runtime",
        fc=GREEN_LIGHT, ec=GREEN, fontsize=9.5)

    box(ax, (7.5, 0.7), 6.7, 1.4,
        "Aggregate over 54 cases\n\n"
        "reports/te_table.parquet\n"
        "+  reports/te_graph.pkl (NetworkX DiGraph)",
        fc=GREEN_LIGHT, ec=GREEN, fontsize=10, fontweight="bold")

    # Arrows from analyses down + cross-arrow
    arrow(ax, (3.6, y2 + 0.05), (3.6, 2.1), color=GREEN, lw=1.3)
    arrow(ax, (10.9, y2 + 0.05), (10.9, 2.1), color=GREEN, lw=1.3)
    arrow(ax, (7.0, 1.4), (7.5, 1.4), color=GREEN, lw=2.0)

    plt.tight_layout()
    out = OUT / "fig3-te-pipeline.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Wrote {out}")


def make_fig0_openfast_modules():
    """OpenFAST module architecture diagram, redrawn for our toolchain.
    Adapted from NREL/Jonkman's classic OpenFAST coupling diagram with
    SeaState (new module in v3.x+), TurbSim made explicit, MoorDyn called
    out (we don't use MAP++ or FEAMooring), and ROSCO shown inside ServoDyn.
    """
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(6.5, 8.65,
            "OpenFAST coupled aero-hydro-servo-elastic model — modules used in this work",
            ha="center", fontsize=13, fontweight="bold", color=BLUE_DARK)

    # Three column headers
    ax.text(2.0, 8.05, "External\nConditions",
            ha="center", fontsize=11, fontweight="bold", color=GRAY,
            linespacing=1.2)
    ax.text(5.1, 8.05, "Applied\nLoads",
            ha="center", fontsize=11, fontweight="bold", color=GRAY,
            linespacing=1.2)
    ax.text(9.7, 8.05, "Wind Turbine (multi-physics dynamics)",
            ha="center", fontsize=11, fontweight="bold", color=GRAY)

    # Vertical dashed dividers between columns
    for x in [3.55, 6.65]:
        ax.plot([x, x], [0.4, 7.6], "--", color=GRAY, linewidth=0.8, alpha=0.6)

    # ---- External Conditions column (left) ----
    # Wind block
    box(ax, (0.4, 6.05), 3.0, 1.3, "", fc="white", ec=ORANGE, lw=1.6)
    ax.text(1.9, 7.15, "Wind", ha="center", fontsize=10, fontweight="bold", color=ORANGE)
    box(ax, (0.65, 6.55), 2.5, 0.45, "TurbSim", fc=ORANGE_LIGHT, ec=ORANGE, fontsize=9.5, fontweight="bold")
    box(ax, (0.65, 6.10), 2.5, 0.40, "InflowWind", fc="white", ec=ORANGE, fontsize=9)

    # Waves block
    box(ax, (0.4, 3.05), 3.0, 1.4, "", fc="white", ec=BLUE_MID, lw=1.6)
    ax.text(1.9, 4.25, "Waves & currents", ha="center", fontsize=10, fontweight="bold", color=BLUE_MID)
    box(ax, (0.65, 3.55), 2.5, 0.45, "SeaState", fc=BLUE_LIGHT, ec=BLUE_MID, fontsize=9.5, fontweight="bold")
    box(ax, (0.65, 3.10), 2.5, 0.40, "(JONSWAP / SSS)", fc="white", ec=BLUE_MID, fontsize=9)

    # ---- Applied Loads column (middle) ----
    box(ax, (3.85, 5.95), 2.6, 1.5,
        "AeroDyn 15\n\nBEM + tip-loss\n+ dynamic stall",
        fc=ORANGE_LIGHT, ec=ORANGE, fontsize=9.5, fontweight="bold")
    box(ax, (3.85, 2.95), 2.6, 1.5,
        "HydroDyn\n\npotential-flow\n+ Morison drag",
        fc=BLUE_LIGHT, ec=BLUE_MID, fontsize=9.5, fontweight="bold")

    # ---- Wind Turbine column (right) — three module groupings ----
    # ServoDyn group (top)
    box(ax, (6.95, 5.50), 5.6, 1.9, "", fc="white", ec=GREEN, lw=1.6)
    ax.text(7.15, 7.20, "ServoDyn", ha="left", fontsize=10, fontweight="bold", color=GREEN)
    box(ax, (7.15, 6.45), 5.2, 0.55, "ROSCO controller  (libdiscon.so)",
        fc=GREEN_LIGHT, ec=GREEN, fontsize=9.5, fontweight="bold")
    box(ax, (7.15, 5.65), 1.65, 0.65, "Rotor\nDynamics",
        fc="white", ec=GREEN, fontsize=9)
    box(ax, (8.92, 5.65), 1.65, 0.65, "Drivetrain\nDynamics",
        fc="white", ec=GREEN, fontsize=9)
    box(ax, (10.70, 5.65), 1.65, 0.65, "Power\nGeneration",
        fc="white", ec=GREEN, fontsize=9)

    # ElastoDyn group (middle)
    box(ax, (6.95, 2.55), 5.6, 2.65, "", fc="white", ec=BLUE_DARK, lw=1.6)
    ax.text(7.15, 4.98, "ElastoDyn   (+ optional BeamDyn for higher-order blade)",
            ha="left", fontsize=10, fontweight="bold", color=BLUE_DARK)
    box(ax, (7.5, 4.25), 4.6, 0.55, "Nacelle Dynamics",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=9.5, fontweight="bold")
    box(ax, (7.5, 3.55), 4.6, 0.55, "Tower Dynamics",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=9.5, fontweight="bold")
    box(ax, (7.5, 2.75), 4.6, 0.55, "Platform Dynamics",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=9.5, fontweight="bold")

    # MoorDyn (bottom)
    box(ax, (6.95, 0.85), 5.6, 1.3, "", fc="white", ec=ORANGE, lw=1.6)
    ax.text(7.15, 1.93, "MoorDyn   (MoorPy quasi-static cross-check)",
            ha="left", fontsize=10, fontweight="bold", color=ORANGE)
    box(ax, (7.5, 1.05), 4.6, 0.55, "Mooring Dynamics",
        fc=ORANGE_LIGHT, ec=ORANGE, fontsize=9.5, fontweight="bold")

    # ---- Arrows: External → Applied Loads → Wind Turbine ----
    # Wind path
    arrow(ax, (3.4, 6.7), (3.85, 6.7), color=ORANGE, lw=1.5)
    arrow(ax, (6.45, 6.7), (6.95, 6.55), color=ORANGE, lw=1.5)
    # Wave path
    arrow(ax, (3.4, 3.75), (3.85, 3.75), color=BLUE_MID, lw=1.5)
    arrow(ax, (6.45, 3.75), (6.95, 3.45), color=BLUE_MID, lw=1.5)

    # Internal couplings (vertical, within Wind Turbine column)
    # ServoDyn (pitch & torque) → ElastoDyn rotor/drivetrain (down)
    arrow(ax, (9.75, 5.50), (9.75, 5.20), color=GREEN, lw=1.3)
    # ElastoDyn (motion feedback) → ServoDyn (up)
    arrow(ax, (10.30, 5.20), (10.30, 5.50), color=BLUE_DARK, lw=1.3)
    # ElastoDyn platform → MoorDyn
    arrow(ax, (9.75, 2.55), (9.75, 2.15), color=BLUE_DARK, lw=1.3)
    # MoorDyn → ElastoDyn (tensions back)
    arrow(ax, (10.30, 2.15), (10.30, 2.55), color=ORANGE, lw=1.3)

    # OpenFAST orchestration label (bottom band)
    box(ax, (0.4, 0.15), 12.2, 0.45,
        "OpenFAST 4.2.1   —   orchestrates the coupled time-step integration of all modules",
        fc=BLUE_LIGHT, ec=BLUE_DARK, fontsize=10, fontweight="bold")

    plt.tight_layout()
    out = OUT / "fig0-openfast-modules.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Wrote {out}")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print("Generating figures…")
    make_fig0_openfast_modules()
    make_fig1()
    make_fig2()
    make_fig3()
    print("Done.")
