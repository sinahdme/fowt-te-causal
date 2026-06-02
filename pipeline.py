"""
pipeline.py — top-level orchestrator for the FOWT causal-TE project.

Wires the existing per-phase drivers into a single command with idempotent
skip-if-done logic, per-phase worker tuning, and a phase-status preflight.

Usage:
    python pipeline.py status                # show what's done / will-run
    python pipeline.py smoke                 # small versions of every phase
    python pipeline.py phase5 --N 256
    python pipeline.py phase2 --dlc dlca     # any DLC: dlc16, dlca, dlcb
    python pipeline.py phase4
    python pipeline.py graph
    python pipeline.py all --N 256           # phase5 + phase2-* + phase4 + graph

Workers per phase:
    --workers N            shared default across phases
    --raft-workers N       override for Phase 5 RAFT (lighter; can use more)
    --openfast-workers N   override for Phase 2 OpenFAST (heavy RAM; use fewer)
    --te-workers N         override for Phase 4 IDTxl (JVM-heavy; use moderate)

On a 65-core server, sensible defaults:
    --raft-workers 60 --openfast-workers 32 --te-workers 40

Env vars (all optional; defaults pinned for local Windows dev):
    OPENFAST_EXE, TURBSIM_EXE, ROSCO_DLL, JAVA_HOME, PYTHONUTF8
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable  # the env python we're running under

# Per-DLC expected output count
DLC_CASE_COUNTS = {"dlc16": 6, "dlca": 24, "dlcb": 24}
ALL_DLCS = ("dlc16", "dlca", "dlcb")


# ----------------------------------------------------------------------------
# Phase status detection (idempotency)
# ----------------------------------------------------------------------------

@dataclass
class PhaseStatus:
    name: str
    done: bool
    detail: str

    def __str__(self) -> str:
        mark = "[done]" if self.done else "[run ]"
        return f"  {self.name:18s}  {mark}  {self.detail}"


def phase5_status(suffix: str = "v2-N64") -> PhaseStatus:
    parquet = PROJECT_ROOT / "data" / f"raft_lhs_{suffix}.parquet"
    sobol = PROJECT_ROOT / "data" / f"raft_lhs_{suffix}_sobol.json"
    if parquet.exists() and sobol.exists():
        return PhaseStatus("phase5", True, f"{parquet.name} + sobol.json present")
    return PhaseStatus("phase5", False, f"will write {parquet.name}")


def phase2_dlc_status(dlc: str) -> PhaseStatus:
    expected = DLC_CASE_COUNTS[dlc]
    if dlc == "dlc16":
        wind_list = [11]
    else:
        wind_list = [8, 11, 15, 20]
    have = 0
    missing: list[str] = []
    for w in wind_list:
        for s in range(6):
            case_id = f"{dlc}_v{w:02d}ms_s{s:02d}"
            outb = (PROJECT_ROOT / "sims" / case_id
                    / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.outb")
            if outb.exists():
                have += 1
            else:
                missing.append(case_id)
    done = have == expected
    detail = (f"{have}/{expected} cases present"
              + (f"; missing: {missing[:3]}{'...' if len(missing) > 3 else ''}" if missing else ""))
    return PhaseStatus(f"phase2-{dlc}", done, detail)


# A journal-tier full Phase 4 table must carry the Granger baseline and the
# conditional TE, not just bivariate KSG + coherence. Checking only file
# existence let a committed scope-reduced first-pass table masquerade as a
# completed full run and silently skip the rerun on a fresh clone (2026-06-02).
def phase4_status(out_file: str = "reports/te_table.parquet") -> PhaseStatus:
    p = PROJECT_ROOT / out_file
    if not p.exists():
        return PhaseStatus("phase4", False, f"{p.name} missing")
    try:
        import pandas as pd
        methods = set(pd.read_parquet(p, columns=["method"])["method"].unique())
    except Exception as e:  # unreadable / pandas+pyarrow absent → treat as not done
        return PhaseStatus("phase4", False, f"{p.name} present but unreadable ({e})")
    # conditional TE is emitted as "conditional_te_ksg|<env>" — match by prefix.
    have = {
        "bivariate": "bivariate_te_ksg" in methods,
        "granger": "bivariate_granger" in methods,
        "conditional_te": any(m.startswith("conditional_te_ksg") for m in methods),
    }
    if all(have.values()):
        return PhaseStatus("phase4", True, f"{p.name}: full ({len(methods)} methods)")
    missing = [k for k, ok in have.items() if not ok]
    return PhaseStatus("phase4", False, f"{p.name}: first-pass only, missing {missing}")


def graph_status(out_file: str = "reports/te_graph.pkl") -> PhaseStatus:
    p = PROJECT_ROOT / out_file
    return PhaseStatus("graph", p.exists(), f"{p.name}{' present' if p.exists() else ' missing'}")


# ----------------------------------------------------------------------------
# Phase runners (thin wrappers around the existing drivers)
# ----------------------------------------------------------------------------

def _env_for_subprocess() -> dict:
    """Set PYTHONUTF8 + JAVA_HOME if not already set. Inherits caller's env."""
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault(
        "JAVA_HOME",
        str(Path(PYTHON).resolve().parent / "Library" / "lib" / "jvm"),
    )
    return env


def _run(cmd: list[str], cwd: Path | None = None, label: str = "") -> int:
    cwd = cwd or PROJECT_ROOT
    print(f"\n=== {label or ' '.join(cmd[:3])} ===")
    print(f"$ cd {cwd}")
    print(f"$ {' '.join(cmd)}\n", flush=True)
    rc = subprocess.run(cmd, cwd=str(cwd), env=_env_for_subprocess()).returncode
    if rc != 0:
        print(f"!! command failed with exit code {rc}", file=sys.stderr)
    return rc


def run_phase5(N: int, workers: int, suffix: str = "v2-N64",
               skip_existing: bool = True, force: bool = False) -> int:
    """Phase 5 — RAFT Saltelli ensemble + Sobol indices."""
    if not force and phase5_status(suffix).done:
        print(f"[phase5] already done (suffix={suffix}); pass --force to re-run.")
        return 0
    cmd = [PYTHON, "-u", str(PROJECT_ROOT / "sims" / "run_raft_lhs.py"),
           "--N", str(N), "--workers", str(workers), "--out-suffix", suffix]
    if skip_existing:
        cmd.append("--skip-existing")
    return _run(cmd, label=f"phase5  N={N}  workers={workers}")


def run_phase2(dlc: str, workers: int, tmax: float = 3600.0,
               transient_drop: float = 600.0, force: bool = False) -> int:
    """Phase 2 — OpenFAST DLC campaign for a single DLC set."""
    if dlc not in DLC_CASE_COUNTS:
        raise SystemExit(f"unknown DLC {dlc}; must be one of {list(DLC_CASE_COUNTS)}")
    if not force and phase2_dlc_status(dlc).done:
        print(f"[phase2-{dlc}] already done; pass --force to re-run.")
        return 0
    cmd = [PYTHON, "-u", str(PROJECT_ROOT / "sims" / "run_campaign.py"),
           "--dlc", dlc, "--tmax", str(tmax),
           "--transient-drop", str(transient_drop),
           "--workers", str(workers)]
    return _run(cmd, label=f"phase2-{dlc}  workers={workers}  TMax={tmax}")


def run_phase4(workers: int, dlcs: tuple[str, ...] = ALL_DLCS,
               out_file: str = "reports/te_table.parquet",
               smoke: bool = False, force: bool = False,
               n_perm: int | None = None,
               max_lag: int | None = None,
               decimate_target_hz: float | None = None,
               no_conditional: bool = False,
               no_granger: bool = False,
               no_ais: bool = False) -> int:
    """Phase 4 — TE pipeline over every .outb produced by the requested DLCs.

    Scope-control knobs (added 2026-05-20 after the max_lag=150 wall-time
    blow-up): n_perm and max_lag override the te_pipeline.py defaults;
    no_conditional / no_granger / no_ais disable individual estimators
    to cut runtime. None = use te_pipeline.py default."""
    if not force and phase4_status(out_file).done:
        print(f"[phase4] already done ({out_file}); pass --force to re-run.")
        return 0

    outb_paths: list[str] = []
    for dlc in dlcs:
        if dlc == "dlc16":
            wind_list = [11]
        else:
            wind_list = [8, 11, 15, 20]
        for w in wind_list:
            for s in range(6):
                p = (PROJECT_ROOT / "sims" / f"{dlc}_v{w:02d}ms_s{s:02d}"
                     / "IEA-15-240-RWT-UMaineSemi" / "IEA-15-240-RWT-UMaineSemi.outb")
                if p.exists():
                    outb_paths.append(str(p))
    if not outb_paths:
        print("[phase4] no .outb files found; run phase2 first.")
        return 1
    print(f"[phase4] {len(outb_paths)} .outb files to process")

    # te_pipeline.py is currently single-process. The --workers knob is here for
    # forward-compat: when we add a ProcessPoolExecutor over per-case calls,
    # this becomes a real parallelism dial. For now it's documented but unused.
    cmd = [PYTHON, "-u", str(PROJECT_ROOT / "analysis" / "te_pipeline.py"),
           *outb_paths, "-o", out_file]
    if smoke:
        cmd.append("--smoke")
    if n_perm is not None:
        cmd += ["--n-perm", str(n_perm)]
    if max_lag is not None:
        cmd += ["--max-lag", str(max_lag)]
    if decimate_target_hz is not None:
        cmd += ["--decimate-target-hz", str(decimate_target_hz)]
    if no_conditional:
        cmd.append("--no-conditional")
    if no_granger:
        cmd.append("--no-granger")
    if no_ais:
        cmd.append("--no-ais")
    return _run(cmd, label=f"phase4  cases={len(outb_paths)}  smoke={smoke}  "
                           f"n_perm={n_perm}  max_lag={max_lag}  fs={decimate_target_hz}")


def run_graph(in_file: str = "reports/te_table.parquet",
              out_file: str = "reports/te_graph.pkl",
              force: bool = False) -> int:
    """Phase 6 — build the NetworkX directed graph from the Phase 4 table."""
    if not force and graph_status(out_file).done:
        print(f"[graph] already done ({out_file}); pass --force to re-run.")
        return 0
    cmd = [PYTHON, "-u", "-c",
           f"import sys; sys.path.insert(0, str({str(PROJECT_ROOT / 'analysis')!r}));"
           f"import pandas as pd, pickle;"
           f"from te_pipeline import build_graph;"
           f"df = pd.read_parquet({str(PROJECT_ROOT / in_file)!r});"
           f"g = build_graph(df);"
           f"pickle.dump(g, open({str(PROJECT_ROOT / out_file)!r}, 'wb'));"
           f"print(f'wrote graph: nodes={{g.number_of_nodes()}}, edges={{g.number_of_edges()}}')"]
    return _run(cmd, label="graph")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def cmd_status(args) -> int:
    print("Phase status (in PROJECT_ROOT =", PROJECT_ROOT, "):\n")
    statuses = [
        phase5_status(args.suffix),
        *[phase2_dlc_status(d) for d in ALL_DLCS],
        phase4_status(),
        graph_status(),
    ]
    for s in statuses:
        print(s)
    print()
    return 0


def cmd_phase5(args) -> int:
    return run_phase5(N=args.N, workers=args.raft_workers, suffix=args.suffix,
                      force=args.force)


def cmd_phase2(args) -> int:
    return run_phase2(dlc=args.dlc, workers=args.openfast_workers,
                      tmax=args.tmax, transient_drop=args.transient_drop,
                      force=args.force)


def cmd_phase4(args) -> int:
    return run_phase4(workers=args.te_workers, smoke=args.smoke, force=args.force,
                      n_perm=args.n_perm, max_lag=args.max_lag,
                      decimate_target_hz=args.decimate_target_hz,
                      no_conditional=args.no_conditional,
                      no_granger=args.no_granger,
                      no_ais=args.no_ais)


def cmd_graph(args) -> int:
    return run_graph(force=args.force)


def cmd_all(args) -> int:
    rc = run_phase5(N=args.N, workers=args.raft_workers, suffix=args.suffix,
                    force=args.force)
    if rc:
        return rc
    for dlc in ALL_DLCS:
        rc = run_phase2(dlc=dlc, workers=args.openfast_workers,
                        tmax=args.tmax, transient_drop=args.transient_drop,
                        force=args.force)
        if rc:
            return rc
    rc = run_phase4(workers=args.te_workers, force=args.force)
    if rc:
        return rc
    return run_graph(force=args.force)


def cmd_smoke(args) -> int:
    """Tiny end-to-end test of every phase. Useful for verifying server install."""
    # Phase 5 smoke: N=4 (44 evals)
    rc = run_phase5(N=4, workers=min(args.raft_workers, 4),
                    suffix="smoke", force=True)
    if rc:
        return rc
    # Phase 2 smoke: dlc16, TMax=120 (~2 min per case)
    rc = run_phase2(dlc="dlc16", workers=min(args.openfast_workers, 6),
                    tmax=120.0, transient_drop=20.0, force=True)
    if rc:
        return rc
    # Phase 4 smoke: 1 pair, n_perm=50
    rc = run_phase4(workers=1, dlcs=("dlc16",), smoke=True,
                    out_file="reports/te_table_smoke.parquet", force=True)
    return rc


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    # Shared options
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1),
                   help="Shared default worker count (overridden by per-phase flags).")
    p.add_argument("--raft-workers", type=int, default=None)
    p.add_argument("--openfast-workers", type=int, default=None)
    p.add_argument("--te-workers", type=int, default=None)
    p.add_argument("--force", action="store_true",
                   help="Force re-run even if outputs already exist.")
    p.add_argument("--suffix", default="v2-N64",
                   help="Phase 5 output suffix (data/raft_lhs_<suffix>.parquet)")
    p.add_argument("--tmax", type=float, default=3600.0)
    p.add_argument("--transient-drop", type=float, default=600.0)
    p.add_argument("-N", "--N", dest="N", type=int, default=64,
                   help="Phase 5 Saltelli base sample size (total evals = N*(D+2))")

    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("phase5").set_defaults(func=cmd_phase5)
    p2 = sub.add_parser("phase2")
    p2.add_argument("--dlc", choices=ALL_DLCS, required=True)
    p2.set_defaults(func=cmd_phase2)
    p4 = sub.add_parser("phase4")
    p4.add_argument("--smoke", action="store_true")
    p4.add_argument("--n-perm", type=int, default=None,
                    help="Surrogate count override (te_pipeline.py default = 200). "
                         "Use 50 for the scope-reduced first-pass campaign.")
    p4.add_argument("--max-lag", type=int, default=None,
                    help="Embedding max-lag override (te_pipeline.py default = 150).")
    p4.add_argument("--decimate-target-hz", type=float, default=None,
                    help="Decimated sample rate (te_pipeline.py default = 5 Hz). "
                         "Use 2.0 to drop N from 15001 to 6001 with no aliasing of "
                         "FOWT-relevant modes; cuts per-case runtime by ~10×.")
    p4.add_argument("--no-conditional", action="store_true",
                    help="Skip conditional / multivariate TE (saves ~⅓ of per-pair time).")
    p4.add_argument("--no-granger", action="store_true",
                    help="Skip Gaussian-Granger baseline.")
    p4.add_argument("--no-ais", action="store_true",
                    help="Skip AIS (only do this if you don't need TE_frac normalisation).")
    p4.set_defaults(func=cmd_phase4)
    sub.add_parser("graph").set_defaults(func=cmd_graph)
    sub.add_parser("all").set_defaults(func=cmd_all)
    sub.add_parser("smoke").set_defaults(func=cmd_smoke)

    args = p.parse_args()

    # Fill in per-phase worker defaults from the shared --workers
    if args.raft_workers is None:    args.raft_workers = args.workers
    if args.openfast_workers is None: args.openfast_workers = args.workers
    if args.te_workers is None:       args.te_workers = args.workers

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
