#!/usr/bin/env python
"""
Generate reports/figs/fig0-openfast-modules.png — the OpenFAST coupled
aero-hydro-servo-elastic module schematic for the te-firewall paper (§2.2).

All labels are verified against the actual campaign run
(sims/dlc16_v11ms_s00): OpenFAST log + SeaState/HydroDyn/AeroDyn input files.

Verified facts (do not "improve" these into unverified specifics):
  - OpenFAST-v4.2.0  (openfast.log)                       [NOT 4.2.1]
  - Modules running: ElastoDyn, InflowWind, SeaState, AeroDyn, HydroDyn,
    MoorDyn v2.3.8, ServoDyn (ROSCO via Bladed libdiscon DLL).  No BeamDyn,
    no SubDyn.
  - AeroDyn15: Wake_Mod=1 (BEMT), TipLoss=True, HubLoss=True, DBEMT_Mod=2
    (dynamic wake).  [dynamic-stall/UA not confirmed -> not claimed]
  - HydroDyn: PotMod=1 (potential-flow/WAMIT), DiffQTF=12 (full 2nd-order
    difference-frequency QTF), SumQTF=0, NMembers=0 (NO Morison members).
  - SeaState: WaveMod=2 (JONSWAP); DLC1.6 shown case Hs=8.3 m, Tp=12.95 s.
  - MoorPy is an *external* quasi-static cross-check, not an OpenFAST module.

Run:  python reports/figs/_make_fig0_openfast_modules.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---- palette (matched to the original schematic) --------------------------
ORANGE_E, ORANGE_F = "#D9822B", "#FBE5D2"      # wind / aero / moor
BLUE_E,   BLUE_F   = "#2E6DA4", "#D6E4F2"       # waves / hydro / elasto children
GREEN_E,  GREEN_F  = "#4E7C2F", "#DDEBCB"       # servodyn
NAVY_E,   NAVY_F   = "#1F3D6E", "#FFFFFF"       # elastodyn outer
WHITE_F            = "#FFFFFF"
BAR_F              = "#D6E0F2"
TITLE_C            = "#1F4E79"
HDR_C              = "#6E6E6E"

FS_TITLE, FS_HDR, FS_BOXHDR, FS_BODY, FS_CHILD = 21, 15, 15, 13, 12.5


def rbox(ax, x, y, w, h, ec, fc, lw=2.2, r=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0,rounding_size={r*100}",
                 mutation_aspect=1.0, ec=ec, fc=fc, lw=lw, zorder=2))


def txt(ax, x, y, s, size=FS_BODY, color="#111111", weight="normal",
        ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=4)


def arrow(ax, p0, p1, color, lw=2.4):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=20,
                 color=color, lw=lw, zorder=3, shrinkA=0, shrinkB=0))


def main():
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # ---- title + column headers ------------------------------------------
    txt(ax, 50, 97,
        "OpenFAST coupled aero-hydro-servo-elastic model — modules used in this work",
        size=FS_TITLE, color=TITLE_C, weight="bold")
    txt(ax, 15, 90, "External\nConditions", size=FS_HDR, color=HDR_C, weight="bold")
    txt(ax, 40, 90.5, "Applied\nLoads", size=FS_HDR, color=HDR_C, weight="bold")
    txt(ax, 78, 90.5, "Wind Turbine (multi-physics dynamics)",
        size=FS_HDR, color=HDR_C, weight="bold")

    # dashed column separators
    for xsep in (27.5, 52.5):
        ax.plot([xsep, xsep], [4, 86], ls=(0, (5, 5)), color="#B8B8B8", lw=1.2, zorder=1)

    # ================= External Conditions column =========================
    # Wind
    rbox(ax, 3, 66, 22, 18, ORANGE_E, WHITE_F)
    txt(ax, 14, 81, "Wind", size=FS_BOXHDR, color=ORANGE_E, weight="bold")
    rbox(ax, 5, 74.5, 18, 5.0, ORANGE_E, ORANGE_F, lw=1.8)
    txt(ax, 14, 77.0, "TurbSim", size=FS_CHILD, weight="bold")
    rbox(ax, 5, 68.0, 18, 5.0, ORANGE_E, WHITE_F, lw=1.8)
    txt(ax, 14, 70.5, "InflowWind", size=FS_CHILD)

    # Waves & currents
    rbox(ax, 3, 30, 22, 20, BLUE_E, WHITE_F)
    txt(ax, 14, 47, "Waves & currents", size=FS_BOXHDR, color=BLUE_E, weight="bold")
    rbox(ax, 5, 39.5, 18, 5.2, BLUE_E, BLUE_F, lw=1.8)
    txt(ax, 14, 42.1, "SeaState", size=FS_CHILD, weight="bold")
    rbox(ax, 5, 32.8, 18, 5.2, BLUE_E, WHITE_F, lw=1.8)
    txt(ax, 14, 35.4, "(JONSWAP / SSS)", size=FS_CHILD)

    # ================= Applied Loads column ===============================
    # AeroDyn
    rbox(ax, 31, 62, 19, 22, ORANGE_E, ORANGE_F)
    txt(ax, 40.5, 78.5, "AeroDyn 15", size=FS_BOXHDR, weight="bold")
    txt(ax, 40.5, 71.5, "BEMT + tip-loss\n+ dynamic wake (DBEMT)",
        size=FS_BODY, weight="bold")
    # HydroDyn
    rbox(ax, 31, 30, 19, 22, BLUE_E, BLUE_F)
    txt(ax, 40.5, 46.5, "HydroDyn", size=FS_BOXHDR, weight="bold")
    txt(ax, 40.5, 39.0, "potential-flow (WAMIT)\n+ 2nd-order difference QTF",
        size=FS_BODY, weight="bold")

    # ================= Wind Turbine column ================================
    # ServoDyn
    rbox(ax, 55, 62, 43, 24, GREEN_E, WHITE_F)
    txt(ax, 58.5, 83.2, "ServoDyn", size=FS_BOXHDR, color=GREEN_E, weight="bold", ha="left")
    rbox(ax, 57, 75.5, 39, 5.6, GREEN_E, GREEN_F, lw=1.8)
    txt(ax, 76.5, 78.3, "ROSCO controller  (libdiscon.so)", size=FS_CHILD, weight="bold")
    for cx, lbl in [(63.5, "Rotor\nDynamics"), (76.5, "Drivetrain\nDynamics"),
                    (89.5, "Power\nGeneration")]:
        rbox(ax, cx - 6, 64.0, 12, 8.5, GREEN_E, WHITE_F, lw=1.8)
        txt(ax, cx, 68.25, lbl, size=FS_CHILD)

    # ElastoDyn
    rbox(ax, 55, 30, 43, 27, NAVY_E, NAVY_F)
    txt(ax, 58.5, 54.0, "ElastoDyn   (blades, tower, nacelle, platform)",
        size=FS_BOXHDR, color=NAVY_E, weight="bold", ha="left")
    for i, lbl in enumerate(["Nacelle Dynamics", "Tower Dynamics", "Platform Dynamics"]):
        yy = 47.5 - i * 6.6
        rbox(ax, 57, yy, 39, 5.6, BLUE_E, BLUE_F, lw=1.8)
        txt(ax, 76.5, yy + 2.8, lbl, size=FS_CHILD, weight="bold")

    # MoorDyn
    rbox(ax, 55, 9, 43, 17, ORANGE_E, WHITE_F)
    txt(ax, 58.5, 23.2, "MoorDyn v2   (dynamic mooring; MoorPy quasi-static cross-check)",
        size=13.0, color=ORANGE_E, weight="bold", ha="left")
    rbox(ax, 60, 12.0, 33, 6.5, ORANGE_E, ORANGE_F, lw=1.8)
    txt(ax, 76.5, 15.25, "Mooring Dynamics", size=FS_CHILD, weight="bold")

    # ---- bottom orchestration bar ----------------------------------------
    rbox(ax, 3, 1.5, 95, 5.2, NAVY_E, BAR_F, lw=2.2)
    txt(ax, 50, 4.1,
        "OpenFAST 4.2.0   —   orchestrates the coupled time-step integration of all modules",
        size=FS_BODY + 1, weight="bold", color="#1a1a1a")

    # ---- connector arrows -------------------------------------------------
    arrow(ax, (25.2, 74.0), (30.8, 74.0), ORANGE_E)   # Wind -> AeroDyn
    arrow(ax, (50.2, 73.5), (54.8, 73.5), ORANGE_E)   # AeroDyn -> ServoDyn
    arrow(ax, (25.2, 40.0), (30.8, 40.0), BLUE_E)     # Waves -> HydroDyn
    arrow(ax, (50.2, 41.0), (54.8, 43.0), BLUE_E)     # HydroDyn -> ElastoDyn
    # ServoDyn <-> ElastoDyn (two-way)
    arrow(ax, (74.5, 61.8), (74.5, 57.2), GREEN_E)
    arrow(ax, (78.5, 57.2), (78.5, 61.8), NAVY_E)
    # ElastoDyn <-> MoorDyn (two-way)
    arrow(ax, (74.5, 29.8), (74.5, 26.2), NAVY_E)
    arrow(ax, (78.5, 26.2), (78.5, 29.8), ORANGE_E)

    out = os.path.join(os.path.dirname(__file__), "fig0-openfast-modules.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main()
