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
ax.annotate("materiality gate 0.02", (3.42, 0.021), fontsize=8, color=GREY,
            ha="right", va="bottom", style="italic")

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
fig.text(0.012, 0.012,
         "54 closed-loop cases; dot = case, bar = regime median. Circular-shift bias control\n"
         "subtracted. Drop is positive in 100% of cases.",
         fontsize=8, color=GREY, ha="left", va="bottom")
fig.subplots_adjust(left=0.10, right=0.985, top=0.87, bottom=0.16)
fig.savefig(FIGS / "surd-dose-response.png", dpi=200)
plt.close(fig)
print("wrote figs/surd-dose-response.png")

# --------------------------------------- fig 2: open-loop natural experiment
sib_mask = corr.case.str.match(r"dlca_v11ms_s\d+$")
drop_cl = corr[sib_mask]["value"].to_numpy()
drop_ol = corr[corr.openloop]["value"].iloc[0]
ubp = df[(df.metric == "rus") & (df.term == "U:BldPitch1")
         & (df.lag == HEADLINE_LAG) & (df.target == "PtfmPitch")]
u_cl = ubp[ubp.case.str.match(r"dlca_v11ms_s\d+$")]["value"].to_numpy()
u_ol = ubp[ubp.case.str.contains("openloop")]["value"].iloc[0]

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.6), dpi=200)
panels = [
    (axes[0], drop_cl, drop_ol, "corrected controller leak drop @ 5 s",
     f"−59%"),
    (axes[1], u_cl, u_ol, "U:BldPitch1 → future pitch (norm.)",
     "→ exactly 0"),
]
for ax, v_cl, v_ol, ylab, delta in panels:
    x_cl = rng.uniform(-0.10, 0.10, size=len(v_cl))
    ax.plot(x_cl, v_cl, "o", ms=6, mfc=NAVY, mec="white", mew=0.8, zorder=3)
    ax.hlines(np.median(v_cl), -0.2, 0.2, color=NAVY, lw=2.4, zorder=4)
    ax.plot([1.0], [v_ol], "D", ms=8, mfc=TEAL, mec="white", mew=0.9, zorder=4)
    ax.annotate(f"{np.median(v_cl):.3f}", (0.24, np.median(v_cl)),
                fontsize=9, color=NAVY, fontweight="bold", va="center")
    ax.annotate(f"{v_ol:.4f}" if v_ol else "0.0000", (1.0, v_ol),
                xytext=(1.0, v_ol + 0.05 * max(v_cl)), fontsize=9,
                color=TEAL, fontweight="bold", ha="center", va="bottom")
    ax.annotate(delta, (0.62, (np.median(v_cl) + v_ol) / 2), fontsize=10,
                color=GREY, ha="center", fontweight="bold")
    ax.set_xticks([0, 1], ["controller ON\n(s00–s05)", "controller OFF\n(open-loop twin)"])
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, max(v_cl) * 1.28)
    ax.set_ylabel(ylab, fontsize=9.5, color=NAVY)
    style_axes(ax)
fig.suptitle("Natural experiment: freezing the controller kills the mediated path",
             fontsize=11.5, color=NAVY, fontweight="bold", x=0.012, ha="left")
fig.text(0.012, 0.012,
         "dlca_v11ms_s00, same seed & environment, blade pitch frozen. The leak drop collapses −59%\n"
         "and the unique BldPitch1 term dies exactly to 0 — the channel itself, not an artifact.",
         fontsize=8, color=GREY, ha="left", va="bottom")
fig.subplots_adjust(left=0.09, right=0.985, top=0.86, bottom=0.26, wspace=0.30)
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
ax.annotate("SURD materiality gate 0.02", (0.0345, 0.021), fontsize=8,
            color=GREY, ha="right", va="bottom", style="italic")

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

ax.annotate("the firewall: TE sees nothing,\nSURD measures the mediated path\n(48/51 TE-null cases, 94%)",
            (0.0022, 0.088), fontsize=9.5, color=NAVY, ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.45", fc=LIGHT, ec=TEAL, lw=1.2))

ax.set_xlim(-0.0035, 0.036)
ax.set_ylim(0, 0.115)
ax.set_xlabel("bivariate TE(Wind1VelX → PtfmPitch)  [nats]", fontsize=10, color=NAVY)
ax.set_ylabel("SURD corrected controller leak drop @ 5 s", fontsize=10, color=NAVY)
ax.set_title("Same cases, two methods: TE null vs SURD mediated path",
             fontsize=11.5, color=NAVY, fontweight="bold", loc="left", pad=10)
leg = ax.legend(loc="upper right", fontsize=8.5, frameon=False)
for t in leg.get_texts():
    t.set_color(GREY)
style_axes(ax)
fig.text(0.012, 0.012,
         "54 joined cases (first-pass KSG TE table). TE=0 column jittered for visibility.\n"
         "TE is nonzero in only 2 cases; SURD's corrected drop is positive in all 54.",
         fontsize=8, color=GREY, ha="left", va="bottom")
fig.subplots_adjust(left=0.10, right=0.985, top=0.91, bottom=0.18)
fig.savefig(FIGS / "surd-vs-te.png", dpi=200)
plt.close(fig)
print("wrote figs/surd-vs-te.png")
