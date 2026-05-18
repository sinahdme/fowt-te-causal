"""
run_raft_lhs.py v2 — Phase 5 Saltelli ensemble via RAFT (production).

Lifted from v1 (4 vars, N=8 hardcoded, serial, no resume) to:
  - All 9 locked Phase 5 design variables (see PLAN.md Phase 5 + the
    pages/cookbook/build-saltelli-ensemble.md mapping).
  - N via --N CLI flag (default 8 = smoke; production N>=64 recommended).
  - Per-eval checkpoint to partial parquet; resume skips already-done samples.
  - Parallel via concurrent.futures.ProcessPoolExecutor.
  - One DLC per design (rated wind 11 m/s, JONSWAP Hs=8.3 Tp=12.95 matching
    sources/jeon-2025 DLC1.6) so wall-clock stays manageable.

Variables are parameterised as multiplicative *factors* on the YAML baseline
in [0.8, 1.2] (= +/- 20% around IEA-15 baseline, locked 2026-05-13). Sobol
indices are scale-invariant — factor-vs-dimension makes no difference to
S1/ST values, and the factor form is mechanically simpler.

Constraint policy (from jeon-2025): geometrically infeasible designs are
flagged feasible=False and not evaluated; for Sobol we impute Y at infeasible
rows with the median of feasible Y (documented in the cookbook).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DESIGN_YAML = (
    PROJECT_ROOT / "repos" / "WEIS" / "examples" / "00_setup" / "ref_turbines"
    / "IEA-15-240-RWT_VolturnUS-S_raft.yaml"
)

# 9 vars as multiplicative factors on the YAML baseline (range = +/-20%).
PROBLEM = {
    "num_vars": 9,
    "names":  ["D_MCol", "D_OCol", "R_MO", "D_Pt", "H_Pt", "H_FB", "H_Draft", "EA", "L_u"],
    "bounds": [[0.8, 1.2]] * 9,
}

# Dimensional baselines used only for the constraint check.
# (D_Pt = rect-width baseline 12.5 m; cookbook also notes 9.6148 m
# equivalent-circular. Constraints from jeon-2025 use rect dims.)
BASE = {
    "D_MCol":  10.0,    # main column diameter [m]
    "D_OCol":  12.5,    # offset column diameter [m]
    "R_MO":    51.75,   # offset column radial distance [m]
    "D_Pt":    12.5,    # pontoon rect width [m]
    "H_Pt":    7.0,     # pontoon rect height [m]
    "H_FB":    15.0,    # platform freeboard / column-top z [m]
    "H_Draft": 20.0,    # column-bottom |z| [m]
    "EA":      2.922815e9,  # YAML stiffness baseline [N] (differs from MoorDyn 3.27e9)
    "L_u":     850.0,   # mooring unstretched line length [m]
}


# ----------------------------------------------------------------------------
# YAML patching
# ----------------------------------------------------------------------------

def coerce_to_rigid(obj):
    """Cookbook gotcha 1 — replace integer member.type values with 'rigid'."""
    if isinstance(obj, dict):
        if "type" in obj and not isinstance(obj["type"], str):
            obj["type"] = "rigid"
        for v in obj.values():
            coerce_to_rigid(v)
    elif isinstance(obj, list):
        for v in obj:
            coerce_to_rigid(v)


def _scale_d(d_field, factor: float):
    """Scale a member 'd' field. Supports flat list (circ) and rect [[w,h], ...]."""
    out = []
    for v in d_field:
        if isinstance(v, list):
            out.append([v[0] * factor, *v[1:]])
        else:
            out.append(v * factor)
    return out


def _scale_d_height(d_field, factor: float):
    """Scale the second dim of a rect d-field (pontoon height)."""
    out = []
    for v in d_field:
        if isinstance(v, list) and len(v) >= 2:
            out.append([v[0], v[1] * factor, *v[2:]])
        else:
            out.append(v)
    return out


def patch_design(design: dict, factors: np.ndarray) -> None:
    """Apply 9 variable factors in-place to the design YAML dict.

    Mapping (see pages/cookbook/build-saltelli-ensemble.md §9-variable table):
      D_MCol  -> members[0].d (main column diameters)
      D_OCol  -> members[1..3].d (offset column diameters)
      R_MO    -> x,y of offset-column endpoints + pontoon far-endpoints
      D_Pt    -> rect-width of members[7..9].d entries
      H_Pt    -> rect-height of members[7..9].d entries
      H_FB    -> rB[2] (top z) of column members[0..3]
      H_Draft -> rA[2] (bottom z) of column members + pontoon z
      EA      -> mooring.line_types[main].stiffness
      L_u     -> mooring.lines[*].length
    """
    f = dict(zip(PROBLEM["names"], factors))
    members = design["platform"]["members"]

    for m in members:
        name = m.get("name", "")
        if name.endswith("member1_"):
            # Main column (centred at origin; z spans bottom to top)
            m["d"] = _scale_d(m["d"], f["D_MCol"])
            m["rA"] = [m["rA"][0], m["rA"][1], m["rA"][2] * f["H_Draft"]]
            m["rB"] = [m["rB"][0], m["rB"][1], m["rB"][2] * f["H_FB"]]
        elif name.endswith(("member2_", "member3_", "member4_")):
            # Offset columns: x,y scale with R_MO; z follows H_FB / H_Draft
            m["d"] = _scale_d(m["d"], f["D_OCol"])
            m["rA"] = [m["rA"][0] * f["R_MO"], m["rA"][1] * f["R_MO"], m["rA"][2] * f["H_Draft"]]
            m["rB"] = [m["rB"][0] * f["R_MO"], m["rB"][1] * f["R_MO"], m["rB"][2] * f["H_FB"]]
        elif name.endswith(("member8_", "member9_", "member10_")):
            # Pontoons (rect cross-section: [width, height])
            m["d"] = _scale_d(m["d"], f["D_Pt"])
            m["d"] = _scale_d_height(m["d"], f["H_Pt"])
            for endpoint in ("rA", "rB"):
                r = list(m[endpoint])
                # Far-side endpoint (offset-col side): scale x,y with R_MO.
                # Near-side endpoint (main-col side, |r| < 15 m): leave x,y alone.
                if abs(r[0]) > 15.0 or abs(r[1]) > 15.0:
                    r[0] *= f["R_MO"]
                    r[1] *= f["R_MO"]
                # Pontoons submerged; z tracks platform draft.
                r[2] *= f["H_Draft"]
                m[endpoint] = r
        # else: members[4..6] are small auxiliary (helical strakes etc.) — leave alone

    # Mooring
    for lt in design["mooring"]["line_types"]:
        if lt["name"] == "main":
            lt["stiffness"] = BASE["EA"] * f["EA"]
    for ln in design["mooring"]["lines"]:
        ln["length"] = BASE["L_u"] * f["L_u"]


# ----------------------------------------------------------------------------
# Feasibility (jeon-2025 geometric constraints)
# ----------------------------------------------------------------------------

def feasibility(factors: np.ndarray) -> tuple[bool, str]:
    d = {n: BASE[n] * fac for n, fac in zip(PROBLEM["names"], factors)}
    if d["D_OCol"] <= d["D_Pt"]:
        return False, f"D_OCol={d['D_OCol']:.2f} <= D_Pt={d['D_Pt']:.2f}"
    if d["H_Pt"] <= 0.5 * d["D_Pt"]:
        return False, f"H_Pt={d['H_Pt']:.2f} <= 0.5*D_Pt={0.5 * d['D_Pt']:.2f}"
    if d["H_Draft"] <= 0.5 * d["D_Pt"] + d["H_Pt"]:
        return False, (
            f"H_Draft={d['H_Draft']:.2f} <= "
            f"0.5*D_Pt + H_Pt = {0.5 * d['D_Pt'] + d['H_Pt']:.2f}"
        )
    return True, ""


# ----------------------------------------------------------------------------
# RAFT driver (one design — runs in worker process)
# ----------------------------------------------------------------------------

def _restrict_to_dlc16(design: dict) -> None:
    """Replace YAML's 26 load cases with one DLC1.6-equivalent case."""
    design["cases"]["data"] = [
        [11.0, 0.0, "IB_NTM", "operating", 0.0, "JONSWAP", 12.95, 8.3, 0.0],
    ]


def _worker_init():
    """Each worker process needs PYTHONUTF8 + JAVA_HOME (cookbook gotchas 2, 3).
    JAVA_HOME points at <env>/Library/lib/jvm (one level above the bin/server
    that holds jvm.dll). sys.executable = <env>/python.exe, so .parent = <env>."""
    os.environ.setdefault("PYTHONUTF8", "1")
    if "JAVA_HOME" not in os.environ:
        os.environ["JAVA_HOME"] = str(
            Path(sys.executable).resolve().parent / "Library" / "lib" / "jvm"
        )


def run_one_design(sample_id: int, factors: list[float], design_yaml_path: str) -> dict:
    """Run RAFT once for a single Saltelli-sample design. Pickle-safe."""
    rec = {"sample_id": sample_id, **{n: float(v) for n, v in zip(PROBLEM["names"], factors)}}

    arr = np.asarray(factors, dtype=float)
    ok, reason = feasibility(arr)
    if not ok:
        rec.update({"feasible": False, "infeasible_reason": reason, "error": ""})
        return rec

    try:
        import raft

        design = yaml.load(Path(design_yaml_path).read_text(), Loader=yaml.FullLoader)
        _restrict_to_dlc16(design)
        patch_design(design, arr)

        coerce_to_rigid(design["platform"])
        if "turbine" in design and "tower" in design["turbine"]:
            coerce_to_rigid(design["turbine"]["tower"])
        for mi in design["platform"]["members"]:
            mi["potMod"] = False

        t0 = time.time()
        model = raft.Model(design)
        model.analyzeCases(display=0)
        dt = time.time() - t0

        m = model.results["case_metrics"][0][0]
        stats: dict[str, float] = {}
        for dof in ("surge", "sway", "heave", "roll", "pitch", "yaw"):
            stats[f"{dof}_avg"] = float(m[f"{dof}_avg"])
            stats[f"{dof}_std"] = float(m[f"{dof}_std"])
        if "Tmoor_avg" in m:
            avg = np.asarray(m["Tmoor_avg"]).flatten()
            std = np.asarray(m.get("Tmoor_std", np.zeros_like(avg))).flatten()
            for i, v in enumerate(avg):
                stats[f"Tmoor{i}_avg"] = float(v)
                stats[f"Tmoor{i}_std"] = float(std[i]) if i < len(std) else 0.0

        # Sanity guard: RAFT's mooring static solver can converge to a runaway
        # "equilibrium" at extreme designs, returning unphysical magnitudes
        # without raising. Bounds:
        #   surge/sway/heave : translational [m], absolute cap 1000 m
        #   roll/pitch/yaw   : rotational [deg], absolute cap 90 deg
        #   any NaN/Inf      : always flagged
        # Extended 2026-05-15 (was surge/sway/heave only — missed pitch_avg
        # corruption of order 1e6 deg in N=64 run).
        UNPHYSICAL_OFFSET_M = 1000.0
        UNPHYSICAL_ROT_DEG = 90.0
        def _bad_value(key: str, val: float) -> bool:
            if not np.isfinite(val):
                return True
            if key.startswith(("surge_", "sway_", "heave_")):
                return abs(val) > UNPHYSICAL_OFFSET_M
            if key.startswith(("roll_", "pitch_", "yaw_")):
                return abs(val) > UNPHYSICAL_ROT_DEG
            return False
        bad = any(_bad_value(k, v) for k, v in stats.items())
        if bad:
            rec.update({
                "feasible": False,
                "infeasible_reason": "raft_diverged",
                "error": f"unphysical magnitudes; max|val|={max(abs(v) for v in stats.values()):.1e}",
                "runtime_s": dt,
            })
        else:
            rec.update({
                "feasible": True,
                "infeasible_reason": "",
                "error": "",
                "runtime_s": dt,
                **stats,
            })
    except Exception as e:
        rec.update({
            "feasible": False,
            "infeasible_reason": "raft_failure",
            "error": str(e)[:300],
        })
    return rec


# ----------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------

def _checkpoint(new_rows: list[dict], out_parquet: Path,
                done_ids: set[int], t_start: float, n_evals: int) -> None:
    """Append new_rows to partial parquet; update done_ids in place."""
    if not new_rows:
        return
    new_df = pd.DataFrame(new_rows)
    if out_parquet.exists():
        existing = pd.read_parquet(out_parquet)
        merged = pd.concat([existing, new_df], ignore_index=True)
    else:
        merged = new_df
    merged = (merged.drop_duplicates(subset="sample_id", keep="last")
                    .sort_values("sample_id").reset_index(drop=True))
    merged.to_parquet(out_parquet, compression="zstd")
    done_ids.update(new_df["sample_id"].astype(int).tolist())
    new_rows.clear()
    elapsed = time.time() - t_start
    n_done = len(done_ids)
    rate = n_done / max(elapsed, 1e-6)
    eta = (n_evals - n_done) / max(rate, 1e-6)
    print(f"  [{n_done:4d}/{n_evals}]  elapsed={elapsed:6.0f}s  "
          f"rate={rate:5.2f}/s  ETA={eta:5.0f}s", flush=True)


def main() -> int:
    os.environ.setdefault("PYTHONUTF8", "1")
    _worker_init()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, default=8,
                        help="Saltelli base size; total evals = N*(D+2). "
                             "Default 8 (smoke). Production: N>=64.")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1),
                        help="Parallel worker count. Default = cpu_count-1.")
    parser.add_argument("--out-suffix", default="v2",
                        help="Output suffix; writes data/raft_lhs_<suffix>.parquet "
                             "and data/raft_lhs_<suffix>_sobol.json")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Resume: skip sample_ids already in partial parquet.")
    parser.add_argument("--no-parallel", action="store_true",
                        help="Disable ProcessPoolExecutor; run serially.")
    args = parser.parse_args()

    from SALib.sample import saltelli
    from SALib.analyze import sobol

    out_parquet = PROJECT_ROOT / "data" / f"raft_lhs_{args.out_suffix}.parquet"
    out_sobol = PROJECT_ROOT / "data" / f"raft_lhs_{args.out_suffix}_sobol.json"
    out_parquet.parent.mkdir(parents=True, exist_ok=True)

    samples = saltelli.sample(PROBLEM, args.N, calc_second_order=False)
    n_evals = samples.shape[0]
    print(f"Saltelli sample: N={args.N}, d={PROBLEM['num_vars']}, "
          f"calc_second_order=False  ->  {n_evals} RAFT evals")
    print(f"Workers: {args.workers}  ;  output: {out_parquet.name}\n", flush=True)

    done_ids: set[int] = set()
    if args.skip_existing and out_parquet.exists():
        existing = pd.read_parquet(out_parquet)
        done_ids = set(existing["sample_id"].astype(int).tolist())
        print(f"Resume: {len(done_ids)} samples already done in {out_parquet.name}; "
              f"evaluating {n_evals - len(done_ids)} new.\n", flush=True)

    todo = [(i, samples[i].tolist(), str(DESIGN_YAML))
            for i in range(n_evals) if i not in done_ids]

    rows: list[dict] = []
    t_start = time.time()

    if args.no_parallel or args.workers <= 1:
        for sid, factors, yaml_path in todo:
            rows.append(run_one_design(sid, factors, yaml_path))
            _checkpoint(rows, out_parquet, done_ids, t_start, n_evals)
    else:
        with ProcessPoolExecutor(max_workers=args.workers, initializer=_worker_init) as ex:
            futures = {ex.submit(run_one_design, sid, factors, yaml_path): sid
                       for sid, factors, yaml_path in todo}
            for fut in as_completed(futures):
                rows.append(fut.result())
                _checkpoint(rows, out_parquet, done_ids, t_start, n_evals)

    df = (pd.read_parquet(out_parquet) if out_parquet.exists()
          else pd.DataFrame(rows)).sort_values("sample_id").reset_index(drop=True)
    print(f"\nWrote {out_parquet}  ({len(df)} rows)")

    feasible = df[df["feasible"] == True].copy()  # noqa: E712
    n_feas = len(feasible)
    print(f"Feasible: {n_feas}/{len(df)}  ({100 * n_feas / max(len(df), 1):.1f}%)")
    if n_feas < len(df):
        reasons = df.loc[df["feasible"] == False, "infeasible_reason"].value_counts()
        print("Infeasibility reasons:")
        for k, v in reasons.items():
            print(f"   {v:4d}  {k}")

    # Sobol analysis (impute NaN with median per cookbook policy)
    response_cols = [c for c in df.columns if any(c.endswith(s) for s in ("_avg", "_std"))]
    sobol_results: dict[str, dict] = {}
    if len(df) == n_evals:
        for resp in response_cols:
            y = df[resp].to_numpy(dtype=float, na_value=np.nan)
            mask = np.isnan(y)
            if mask.any():
                med = float(np.nanmedian(y)) if (~mask).any() else 0.0
                y = np.where(mask, med, y)
            if np.std(y) < 1e-12:
                sobol_results[resp] = {"note": "response variance ~0; skipped"}
                continue
            try:
                S = sobol.analyze(PROBLEM, y, calc_second_order=False, print_to_console=False)
                sobol_results[resp] = {
                    "S1": S["S1"].tolist(),
                    "S1_conf": S["S1_conf"].tolist(),
                    "ST": S["ST"].tolist(),
                    "ST_conf": S["ST_conf"].tolist(),
                    "n_feasible": int(n_feas),
                    "n_total": int(len(df)),
                }
            except Exception as e:
                sobol_results[resp] = {"error": str(e)[:200]}
        out_sobol.write_text(json.dumps(sobol_results, indent=2))
        print(f"Wrote {out_sobol}")

        print("\n=== Sobol summary (selected responses) ===")
        for resp in ("surge_avg", "surge_std", "pitch_std", "heave_std"):
            S = sobol_results.get(resp)
            if S and "ST" in S:
                print(f"\n  {resp}  (n_feasible={S['n_feasible']}/{S['n_total']}):")
                for j, name in enumerate(PROBLEM["names"]):
                    print(f"    ST[{name:>7}] = {S['ST'][j]:+.3f} +/- {S['ST_conf'][j]:.3f}")
    else:
        print(f"\nSKIPPED Sobol analyze: have {len(df)} rows, need full {n_evals}.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
