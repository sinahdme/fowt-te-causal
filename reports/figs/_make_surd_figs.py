# -*- coding: utf-8 -*-
"""SURD Phase 2 comparison figures (surd/PLAN.md Phase 2 deliverable).

Consumes reports/surd_table.parquet + reports/te_table.parquet and writes
  surd-dose-response.png  corrected controller leak drop @5 s by wind regime
  surd-openloop.png       controller ON vs OFF natural experiment (2 panels)
  surd-vs-te.png          TE(Wind->PtfmPitch) vs SURD corrected drop per case

Numbers match surd/analyze_phase2.py (HEADLINE_LAG = 25 samples = 5 s @ 5 Hz).
"""
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

NAVY = "#1F3A5F"; TEAL = "#2A9D8F"; GREY = "#5B6470"
LIGHT = "#EEF2F6"; GRID = "#E1E0D9"

HEADLINE_LAG = 25
FIGS = Path(__file__).resolve().parent
REPORTS = FIGS.parent

rng = np.random.default_rng(7)  # jitter only; fixed for reproducible pixels


def regime_of(case: str) -> str:
    m = re.search(r"_v(\d+)ms", case)
    return f"{int(m.group(1))} m/s" if m else "other"


def style_axes(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=GREY, labelsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)


df = pd.read_parquet(REPORTS / "surd_table.parquet")
corr = df[(df.metric == "drop") & (df.term == "corrected")
          & (df.lag == HEADLINE_LAG)].copy()
corr["regime"] = corr["case"].map(regime_of)
corr["openloop"] = corr["case"].str.contains("openloop")

# ------------------------------------------------- fig 1: dose-response strip
ORDER = ["8 m/s", "11 m/s", "15 m/s", "20 m/s"]
cl = corr[~corr.openloop]

fig, ax = plt.subplots(figsize=(7.4, 4.2), dpi=200)
# two-regime background bands: pitch control inactive (below rated) vs active,
# split at the rated boundary (~10.6 m/s, between the 8 and 11 m/s columns)
ax.axvspan(-0.5, 0.5, color=GREY, alpha=0.08, zorder=0)   # inactive — cool grey
ax.axvspan(0.5, 3.5, color=TEAL, alpha=0.10, zorder=0)    # active — teal highlight
ax.axvline(0.5, color=GREY, lw=0.8, ls=(0, (2, 3)), alpha=0.55, zorder=1)
for i, reg in enumerate(ORDER):
    v = cl[cl.regime == reg]["value"].to_numpy()
    x = i + rng.uniform(-0.13, 0.13, size=len(v))
    ax.plot(x, v, "o", ms=5.5, mfc=NAVY, mec="white", mew=0.8, alpha=0.85,
            zorder=3)
    med = np.median(v)
    ax.hlines(med, i - 0.24, i + 0.24, color=NAVY, lw=2.4, zorder=4)
    ax.annotate(f"{med:.3f}", (i + 0.27, med), fontsize=9, color=NAVY,
                fontweight="bold", va="center")
ax.axhline(0.02, color=GREY, lw=1.0, ls=(0, (4, 3)))

# rated bracket: pitch control active at/above 10.59 m/s (IEA-15 rated)
ax.annotate("", xy=(0.96, 0.118), xytext=(3.04, 0.118),
            arrowprops=dict(arrowstyle="-", color=GREY, lw=1.0))
ax.annotate("pitch control active (at/above rated)\nmedian 2.8x below-rated",
            (2.0, 0.121), fontsize=8.5, color=GREY, ha="center", va="bottom")
ax.annotate("pitch control\ninactive", (0, 0.121), fontsize=8.5, color=GREY,
            ha="center", va="bottom", style="italic")

ax.set_xticks(range(4), ORDER)
ax.set_xlim(-0.5, 3.5)
ax.set_ylim(0, 0.135)
ax.set_ylabel("corrected controller leak drop @ 5 s", fontsize=10, color=NAVY)
ax.set_title("Controller firewall dose-response across operating regimes",
             fontsize=11.5, color=NAVY, fontweight="bold", loc="left", pad=14)
style_axes(ax)
legend_handles = [
    Line2D([], [], marker="o", linestyle="none", mfc=NAVY, mec="white",
           mew=0.8, ms=6, label="individual case"),
    Line2D([], [], color=NAVY, lw=2.4, label="regime median"),
    Line2D([], [], color=GREY, lw=1.0, ls=(0, (4, 3)),
           label="materiality gate (0.02)"),
]
ax.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(0.5, -0.14),
          ncol=3, frameon=False, fontsize=8.5, handletextpad=0.5,
          columnspacing=1.8)
fig.subplots_adjust(left=0.10, right=0.985, top=0.87, bottom=0.18)
fig.savefig(FIGS / "surd-dose-response.png", dpi=200)
plt.close(fig)
print("wrote figs/surd-dose-response.png")

# --------------------------------------- fig 2: open-loop natural experiment
# Paired same-seed comparison: seed s00 run closed-loop vs its open-loop twin
# (the twin is built from s00). s00 is the highlighted reference; the other
# five 11 m/s seeds are shown only as light context for the closed-loop spread.
# Reference values match the main-text §3.3 numbers (0.0612 and 0.167).
drop_sib = corr[corr.case.str.match(r"dlca_v11ms_s\d+$")].set_index("case")["value"]
drop_s00 = drop_sib["dlca_v11ms_s00"]
drop_ctx = drop_sib.drop("dlca_v11ms_s00").to_numpy()
drop_ol = corr[corr.openloop]["value"].iloc[0]
ubp = df[(df.metric == "rus") & (df.term == "U:BldPitch1")
         & (df.lag == HEADLINE_LAG) & (df.target == "PtfmPitch")]
u_sib = ubp[ubp.case.str.match(r"dlca_v11ms_s\d+$")].set_index("case")["value"]
u_s00 = u_sib["dlca_v11ms_s00"]
u_ctx = u_sib.drop("dlca_v11ms_s00").to_numpy()
u_ol = ubp[ubp.case.str.contains("openloop")]["value"].iloc[0]

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.6), dpi=200)
panels = [
    (axes[0], drop_s00, drop_ctx, drop_ol, "corrected controller leak drop @ 5 s", "{:.4f}"),
    (axes[1], u_s00, u_ctx, u_ol, "U:BldPitch1 → future pitch (norm.)", "{:.3f}"),
]
for ax, v_s00, v_ctx, v_ol, ylab, fmt in panels:
    ymax = max(v_s00, v_ctx.max(), v_ol)
    # other five closed-loop seeds — light context only
    x_ctx = rng.uniform(-0.12, 0.12, size=len(v_ctx))
    ax.plot(x_ctx, v_ctx, "o", ms=5, mfc=GREY, mec="white", mew=0.6,
            alpha=0.35, zorder=2)
    # paired closed-loop reference (seed s00)
    ax.hlines(v_s00, -0.2, 0.2, color=NAVY, lw=2.4, zorder=3)
    ax.plot([0.0], [v_s00], "o", ms=7, mfc=NAVY, mec="white", mew=0.9, zorder=4)
    ax.annotate(fmt.format(v_s00), (0.24, v_s00), fontsize=9, color=NAVY,
                fontweight="bold", va="center")
    # open-loop twin (same seed s00)
    ax.plot([1.0], [v_ol], "D", ms=8, mfc=TEAL, mec="white", mew=0.9, zorder=4)
    ax.annotate(f"{v_ol:.4f}" if v_ol else "0.0000", (1.0, v_ol),
                xytext=(1.0, v_ol + 0.05 * ymax), fontsize=9,
                color=TEAL, fontweight="bold", ha="center", va="bottom")
    ax.set_xticks([0, 1], ["controller ON\n(seed s00)", "controller OFF\n(open-loop twin)"])
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, ymax * 1.28)
    ax.set_ylabel(ylab, fontsize=9.5, color=NAVY)
    style_axes(ax)
fig.suptitle("Natural experiment: freezing the controller kills the mediated path",
             fontsize=11.5, color=NAVY, fontweight="bold", x=0.012, ha="left")
legend_handles = [
    Line2D([], [], marker="o", ms=7, mfc=NAVY, mec="white", mew=0.9, ls="none",
           label="closed-loop seed s00 (paired)"),
    Line2D([], [], marker="o", ms=5, mfc=GREY, mec="white", mew=0.6, ls="none",
           alpha=0.5, label="other closed-loop seeds"),
    Line2D([], [], marker="D", ms=8, mfc=TEAL, mec="white", mew=0.9, ls="none",
           label="open-loop twin"),
]
leg = fig.legend(handles=legend_handles, loc="lower center", ncol=3,
                 fontsize=8.5, frameon=False, bbox_to_anchor=(0.5, 0.005))
for t in leg.get_texts():
    t.set_color(GREY)
fig.subplots_adjust(left=0.09, right=0.985, top=0.86, bottom=0.24, wspace=0.30)
fig.savefig(FIGS / "surd-openloop.png", dpi=200)
plt.close(fig)
print("wrote figs/surd-openloop.png")

# ---------------------------------------------------- fig 3: TE vs SURD join
te = pd.read_parquet(REPORTS / "te_table.parquet")
wp = te[(te.source == "Wind1VelX") & (te.target == "PtfmPitch")
        & (te.method == "bivariate_te_ksg")][["case", "te_nats"]]
j = corr[~corr.openloop].merge(wp, on="case", how="inner")
j["below_rated"] = j.regime == "8 m/s"

fig, ax = plt.subplots(figsize=(7.4, 4.4), dpi=200)
ax.axhline(0.02, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)

for mask, color, label in [(~j.below_rated, NAVY, "pitch control active (42)"),
                           (j.below_rated, TEAL, "below rated, 8 m/s (12)")]:
    g = j[mask]
    x = g.te_nats + np.where(g.te_nats == 0,
                             rng.uniform(-0.0006, 0.0006, size=len(g)), 0.0)
    ax.plot(x, g.value, "o", ms=6, mfc=color, mec="white", mew=0.8,
            alpha=0.85, zorder=3, ls="none", label=label)

for _, r in j[j.te_nats > 0].iterrows():
    ax.annotate(r.case.replace("dlcb_", "DLC-b "), (r.te_nats, r.value),
                xytext=(r.te_nats, r.value + 0.007), fontsize=8,
                color=NAVY, ha="center")

ax.set_xlim(-0.0035, 0.036)
ax.set_ylim(0, 0.115)
ax.set_xlabel("bivariate TE(Wind1VelX → PtfmPitch)  [nats]", fontsize=10, color=NAVY)
ax.set_ylabel("SURD corrected controller leak drop @ 5 s", fontsize=10, color=NAVY)
ax.set_title("Same cases, two methods: TE null vs SURD mediated path",
             fontsize=11.5, color=NAVY, fontweight="bold", loc="left", pad=10)
handles, _ = ax.get_legend_handles_labels()
handles.append(Line2D([], [], color=GREY, lw=1.0, ls=(0, (4, 3)),
                      label="materiality gate (0.02)"))
leg = ax.legend(handles=handles, loc="upper right", fontsize=8.5, frameon=False)
for t in leg.get_texts():
    t.set_color(GREY)
style_axes(ax)
fig.subplots_adjust(left=0.10, right=0.985, top=0.91, bottom=0.13)
fig.savefig(FIGS / "surd-vs-te.png", dpi=200)
plt.close(fig)
print("wrote figs/surd-vs-te.png")
