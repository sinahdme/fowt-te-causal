"""Quick diagnostic analysis of an OpenFAST .outb file."""
from pathlib import Path
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openfast_toolbox.io import FASTOutputFile

CASE_DIR = Path(r"D:\Causal Effect with transfer entropy\sims\case-iea15-real")
RUN_DIR  = CASE_DIR / "IEA-15-240-RWT-UMaineSemi"
OUTB     = RUN_DIR / "IEA-15-240-RWT-UMaineSemi.outb"
PLOT_DIR = CASE_DIR / "analysis_plots"
PLOT_DIR.mkdir(exist_ok=True)

# Skip initial transient before reporting stats
TRANSIENT_S = 60.0


def load():
    f = FASTOutputFile(str(OUTB))
    df = f.toDataFrame()
    # Channel names often arrive as "Name_[unit]"; strip units for easy lookup
    rename = {}
    for c in df.columns:
        base = c.split("_[")[0] if "_[" in c else c
        rename[c] = base
    df = df.rename(columns=rename)
    return df


def stats(df, names):
    t = df["Time"].values
    mask = t >= TRANSIENT_S
    rows = []
    for n in names:
        if n not in df.columns:
            rows.append((n, "MISSING", "", "", ""))
            continue
        v = df[n].values[mask]
        rows.append((n, f"{v.mean():.3f}", f"{v.std():.3f}",
                     f"{v.min():.3f}", f"{v.max():.3f}"))
    w = max(len(r[0]) for r in rows) + 2
    print(f"  {'channel'.ljust(w)} {'mean':>12} {'std':>12} {'min':>12} {'max':>12}")
    for r in rows:
        print(f"  {r[0].ljust(w)} {r[1]:>12} {r[2]:>12} {r[3]:>12} {r[4]:>12}")


def plot_operating(df):
    t = df["Time"].values
    fig, ax = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
    if "Wind1VelX" in df: ax[0].plot(t, df["Wind1VelX"], lw=0.8)
    ax[0].set_ylabel("Hub wind U [m/s]"); ax[0].grid(alpha=.3)
    if "GenPwr" in df: ax[1].plot(t, df["GenPwr"]/1e3, lw=0.8, color="tab:orange")
    ax[1].set_ylabel("Gen power [MW]"); ax[1].grid(alpha=.3)
    if "RotSpeed" in df: ax[2].plot(t, df["RotSpeed"], lw=0.8, color="tab:green")
    ax[2].set_ylabel("Rotor speed [rpm]"); ax[2].grid(alpha=.3)
    for k, c in [("BldPitch1", "tab:blue"), ("BldPitch2", "tab:red"), ("BldPitch3", "tab:purple")]:
        if k in df: ax[3].plot(t, df[k], lw=0.7, label=k, color=c)
    ax[3].set_ylabel("Blade pitch [deg]"); ax[3].grid(alpha=.3); ax[3].legend(loc="best", fontsize=8)
    ax[3].set_xlabel("Time [s]")
    fig.suptitle("Operating channels", y=0.995)
    fig.tight_layout()
    p = PLOT_DIR / "01_operating.png"
    fig.savefig(p, dpi=120); plt.close(fig)
    return p


def plot_platform(df):
    t = df["Time"].values
    fig, ax = plt.subplots(3, 2, figsize=(12, 8), sharex=True)
    dofs = [("PtfmSurge", "m"), ("PtfmSway", "m"), ("PtfmHeave", "m"),
            ("PtfmRoll", "deg"), ("PtfmPitch", "deg"), ("PtfmYaw", "deg")]
    for a, (k, u) in zip(ax.ravel(), dofs):
        if k in df: a.plot(t, df[k], lw=0.7)
        a.set_ylabel(f"{k} [{u}]"); a.grid(alpha=.3)
    for a in ax[-1, :]: a.set_xlabel("Time [s]")
    fig.suptitle("Platform 6-DOF motions", y=0.995)
    fig.tight_layout()
    p = PLOT_DIR / "02_platform.png"
    fig.savefig(p, dpi=120); plt.close(fig)
    return p


def plot_loads(df):
    t = df["Time"].values
    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    if "TwrBsFxt" in df: ax[0].plot(t, df["TwrBsFxt"]/1e3, lw=0.7)
    ax[0].set_ylabel("TwrBs Fx [MN]"); ax[0].grid(alpha=.3)
    if "TwrBsMyt" in df: ax[1].plot(t, df["TwrBsMyt"]/1e3, lw=0.7, color="tab:orange")
    ax[1].set_ylabel("TwrBs My [MN·m]"); ax[1].grid(alpha=.3)
    for k, c in [("RootMyc1", "tab:blue"), ("RootMyc2", "tab:red"), ("RootMyc3", "tab:purple")]:
        if k in df: ax[2].plot(t, df[k]/1e3, lw=0.6, label=k, color=c)
    ax[2].set_ylabel("Blade root Mflap [MN·m]"); ax[2].grid(alpha=.3); ax[2].legend(fontsize=8)
    ax[2].set_xlabel("Time [s]")
    fig.suptitle("Tower-base & blade-root loads", y=0.995)
    fig.tight_layout()
    p = PLOT_DIR / "03_loads.png"
    fig.savefig(p, dpi=120); plt.close(fig)
    return p


def main():
    print(f"file: {OUTB}")
    print(f"size: {OUTB.stat().st_size/1e6:.2f} MB")
    df = load()
    t = df["Time"].values
    dt = t[1] - t[0]
    print(f"channels: {len(df.columns)}, samples: {len(df):,}, "
          f"dt={dt:.4f} s, t=[{t[0]:.2f}, {t[-1]:.2f}] s")

    # NaN / inf check
    bad = [c for c in df.columns if not np.isfinite(df[c].values).all()]
    print(f"non-finite channels: {len(bad)}{(': ' + ', '.join(bad[:5])) if bad else ''}")

    print(f"\nstats over t >= {TRANSIENT_S} s:\n")
    print("operating:")
    stats(df, ["Wind1VelX", "GenPwr", "GenSpeed", "RotSpeed",
               "BldPitch1", "GenTq", "RotThrust", "RotTorq"])
    print("\nplatform 6-DOF:")
    stats(df, ["PtfmSurge", "PtfmSway", "PtfmHeave",
               "PtfmRoll", "PtfmPitch", "PtfmYaw"])
    print("\ntower base / blade root:")
    stats(df, ["TwrBsFxt", "TwrBsMyt", "RootMyc1", "RootFxc1"])
    print("\nwaves / mooring (if present):")
    stats(df, ["Wave1Elev", "FAIRTEN1", "FAIRTEN2", "FAIRTEN3"])

    print("\nplots:")
    for p in (plot_operating(df), plot_platform(df), plot_loads(df)):
        print(f"  {p}")


if __name__ == "__main__":
    main()
