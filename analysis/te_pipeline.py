"""
te_pipeline.py — Phase 4 transfer-entropy production pipeline.

End-to-end pipeline per PLAN.md Phase 4 + Wollstadt 2019:
  load .outb -> drop transient -> decimate -> jitter -> per-pair tests:
    BivariateTE (KSG)            via IDTxl BivariateTE + JidtKraskovCMI
    Conditional MultivariateTE   via IDTxl MultivariateTE + JidtKraskovCMI
    Granger baseline             via IDTxl MultivariateTE + JidtGaussianCMI
    AIS (effect-size denominator) via IDTxl ActiveInformationStorage + KSG
    Coherence baseline           via scipy.signal.coherence
  -> per-pair table -> NetworkX DiGraph with edge weight TE_frac

Surrogate null is circular-shift (perm_type='circular') per the
2026-05-15 reconciliation — preserves source spectrum + amplitude
distribution, destroys directed coupling. See
concepts/surrogate-significance for the rationale.

Default channels (locked 2026-05-13 per Q1):
  Env sources : Wind1VelX, Wave1Elev
  Responses   : RootMyc1, RootMxc1, TwrBsMyt,
                PtfmHeave, PtfmSurge, PtfmPitch,
                FAIRTEN1, FAIRTEN2, FAIRTEN3

Usage:
    python analysis/te_pipeline.py path/to/run.outb [run2.outb ...] -o reports/te_table.parquet
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))
from load_runs import load_outb, find_time_column  # noqa: E402


# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------

DEFAULT_ENV_SOURCES = ("Wind1VelX", "Wave1Elev")
DEFAULT_RESPONSES = (
    "RootMyc1", "RootMxc1", "TwrBsMyt",
    "PtfmHeave", "PtfmSurge", "PtfmPitch",
    "FAIRTEN1", "FAIRTEN2", "FAIRTEN3",
)


@dataclass
class TESettings:
    """Per-pipeline configuration. Defaults are PLAN-canonical."""
    decimate_target_hz: float = 5.0
    transient_drop_s: float = 600.0     # PLAN-canonical for 3600 s runs
    jitter_scale: float = 1e-10         # kraskov-2004 §III.A
    kraskov_k: int = 4
    max_lag: int = 30                   # = 6 s window at 5 Hz
    min_lag: int = 1
    n_perm: int = 200
    alpha: float = 0.05
    perm_type: str = "circular"         # 2026-05-15 reconciliation
    # Coherence-baseline band
    band_lo_hz: float = 0.01
    band_hi_hz: float = 0.5
    # Optional: limit pairs to enable smoke testing
    env_sources: tuple = DEFAULT_ENV_SOURCES
    responses: tuple = DEFAULT_RESPONSES


# ----------------------------------------------------------------------------
# Channel resolution + preprocessing
# ----------------------------------------------------------------------------

def find_channel(df: pd.DataFrame, basename: str) -> str:
    """Map a canonical OpenFAST channel name ('PtfmPitch') to the
    openfast_toolbox column name ('PtfmPitch_[deg]'). Case-insensitive."""
    for col in df.columns:
        if col.split("_[")[0].lower() == basename.lower():
            return col
    raise KeyError(f"channel {basename!r} not in {list(df.columns)[:8]}...")


def preprocess_channel(
    arr: np.ndarray,
    dt_in: float,
    settings: TESettings,
    seed: int,
) -> tuple[np.ndarray, float]:
    """Drop transient, decimate, jitter. Returns (cleaned, dt_out)."""
    src_hz = 1.0 / dt_in
    factor = max(1, int(round(src_hz / settings.decimate_target_hz)))
    drop_n = int(settings.transient_drop_s / dt_in)
    out = arr[drop_n:][::factor]
    rng = np.random.default_rng(seed)
    out = out + settings.jitter_scale * rng.standard_normal(out.shape)
    return out, dt_in * factor


# ----------------------------------------------------------------------------
# IDTxl-backed analysers
# ----------------------------------------------------------------------------

def _idtxl_base_settings(settings: TESettings, *, for_ais: bool = False) -> dict:
    """The settings dict shared across IDTxl analysers in this pipeline.

    BivariateTE/MultivariateTE use `max_lag_target` / `max_lag_sources`;
    ActiveInformationStorage uses a single `max_lag`. for_ais=True swaps
    in the AIS-flavoured keys.

    `perm_type='circular'` requires `max_shift` to be set explicitly
    (the documented n/2 default doesn't reach the surrogate code path
    in single-replication mode). Use n/4 to be safe — half the data
    can't shift past itself for an n/2 surrogate.
    """
    base = {
        "kraskov_k": str(settings.kraskov_k),
        "n_perm_max_stat": settings.n_perm,
        "n_perm_min_stat": settings.n_perm,
        "n_perm_omnibus": settings.n_perm,
        "n_perm_max_seq": settings.n_perm,
        "alpha_max_stat": settings.alpha,
        "alpha_min_stat": settings.alpha,
        "alpha_omnibus": settings.alpha,
        # Single-replication time series; circular shift preserves spectrum.
        "permute_in_time": True,
        "perm_type": settings.perm_type,
        "verbose": False,
    }
    if for_ais:
        base["max_lag"] = settings.max_lag
    else:
        base["max_lag_sources"] = settings.max_lag
        base["min_lag_sources"] = settings.min_lag
        base["max_lag_target"] = settings.max_lag
    return base


def _extract_te_pval(target_results: dict) -> tuple[float, float, list]:
    te = target_results.get("te")
    pval = target_results.get("omnibus_pval")
    selected = target_results.get("selected_vars_sources") or []
    te_val = float(te[0]) if (te is not None and len(te) > 0) else 0.0
    p_val = float(pval) if pval is not None else 1.0
    return te_val, p_val, list(selected)


def run_bivariate_te(source: np.ndarray, target: np.ndarray,
                     settings: TESettings, estimator: str = "JidtKraskovCMI") -> dict:
    """Bivariate TE(source → target). Returns dict with te, p_value, selected_vars."""
    from idtxl.bivariate_te import BivariateTE
    from idtxl.data import Data

    data = Data(np.vstack([source, target]), dim_order="ps", normalise=True)
    # Set max_shift now that we know N (required for perm_type='circular')
    s = {**_idtxl_base_settings(settings), "cmi_estimator": estimator,
         "max_shift": max(1, len(target) // 4)}
    analysis = BivariateTE()
    results = analysis.analyse_single_target(settings=s, data=data, target=1, sources=[0])
    tr = results.get_single_target(1, fdr=False)
    te_val, p_val, selected = _extract_te_pval(tr)
    return {
        "te_nats": te_val,
        "p_value": p_val,
        "significant": bool(p_val < settings.alpha and te_val > 0),
        "n_selected_sources": len(selected),
    }


def run_multivariate_te(source: np.ndarray, target: np.ndarray,
                        conditional: np.ndarray | None,
                        settings: TESettings,
                        estimator: str = "JidtKraskovCMI") -> dict:
    """Conditional TE(source → target | conditional). If conditional is None,
    falls back to MultivariateTE with just the one source (still does the
    full greedy parent search, distinct from BivariateTE)."""
    from idtxl.multivariate_te import MultivariateTE
    from idtxl.data import Data

    if conditional is None:
        arr = np.vstack([source, target])
        sources_idx = [0]
        target_idx = 1
    else:
        arr = np.vstack([source, target, conditional])
        sources_idx = [0, 2]   # source + conditioning channel both as candidates
        target_idx = 1

    data = Data(arr, dim_order="ps", normalise=True)
    s = {**_idtxl_base_settings(settings), "cmi_estimator": estimator,
         "max_shift": max(1, target.shape[0] // 4)}
    analysis = MultivariateTE()
    results = analysis.analyse_single_target(
        settings=s, data=data, target=target_idx, sources=sources_idx,
    )
    tr = results.get_single_target(target_idx, fdr=False)
    te_val, p_val, selected = _extract_te_pval(tr)
    # Split selected vars by source process for diagnostics
    n_from_source = sum(1 for v in selected if v[0] == 0)
    n_from_cond = sum(1 for v in selected if v[0] == 2)
    return {
        "te_nats": te_val,
        "p_value": p_val,
        "significant": bool(p_val < settings.alpha and te_val > 0),
        "n_selected_from_source": n_from_source,
        "n_selected_from_conditional": n_from_cond,
    }


def run_ais(target: np.ndarray, settings: TESettings) -> dict:
    """Active Information Storage. Effect-size denominator (Wollstadt 2019)."""
    from idtxl.active_information_storage import ActiveInformationStorage
    from idtxl.data import Data

    data = Data(target.reshape(1, -1), dim_order="ps", normalise=True)
    s = {
        **_idtxl_base_settings(settings, for_ais=True),
        "cmi_estimator": "JidtKraskovCMI",
        "max_shift": max(1, len(target) // 4),
    }
    analysis = ActiveInformationStorage()
    results = analysis.analyse_single_process(settings=s, data=data, process=0)
    tr = results.get_single_process(0, fdr=False)
    ais = tr.get("ais")
    p_val = tr.get("ais_pval")
    return {
        "ais_nats": float(ais) if ais is not None else 0.0,
        "p_value": float(p_val) if p_val is not None else 1.0,
    }


# ----------------------------------------------------------------------------
# scipy coherence baseline (not via IDTxl)
# ----------------------------------------------------------------------------

def coherence_baseline(source: np.ndarray, target: np.ndarray,
                       fs: float, band_lo: float, band_hi: float) -> dict:
    """Peak magnitude-squared coherence γ²(f) in the [band_lo, band_hi] Hz band."""
    from scipy.signal import coherence
    nperseg = min(len(source) // 4, 256)
    f, cxy = coherence(source, target, fs=fs, nperseg=nperseg)
    band = (f >= band_lo) & (f <= band_hi)
    if not band.any():
        return {"gamma2_peak": float("nan"), "gamma2_peak_hz": float("nan")}
    cxy_b = cxy[band]
    f_b = f[band]
    j = int(np.argmax(cxy_b))
    return {
        "gamma2_peak": float(cxy_b[j]),
        "gamma2_peak_hz": float(f_b[j]),
    }


# ----------------------------------------------------------------------------
# Per-case orchestrator
# ----------------------------------------------------------------------------

def per_case_pipeline(
    outb_path: Path,
    settings: TESettings,
    *,
    do_conditional: bool = True,
    do_granger: bool = True,
    do_coherence: bool = True,
    do_ais: bool = True,
) -> pd.DataFrame:
    """Run the full Phase-4 pipeline on one .outb file.

    Returns a long-form DataFrame: one row per (source, target, method) combo.
    Columns: case, source, target, method, te_nats, p_value, significant,
             ais_nats, te_frac, gamma2_peak, runtime_s.
    """
    print(f"[{outb_path.parent.name}] loading {outb_path.name}", flush=True)
    t_load0 = time.time()
    df = load_outb(outb_path)
    t_col = find_time_column(df)
    t = df[t_col].to_numpy()
    dt = float(np.median(np.diff(t)))
    src_hz = 1.0 / dt
    print(f"  rate {src_hz:.1f} Hz, dropping {settings.transient_drop_s}s, "
          f"decimating to ~{settings.decimate_target_hz} Hz", flush=True)

    # Pre-process every channel of interest once
    cached: dict[str, np.ndarray] = {}
    dt_out = dt
    seed = 0
    for name in (*settings.env_sources, *settings.responses):
        try:
            col = find_channel(df, name)
        except KeyError:
            warnings.warn(f"channel {name} not in {outb_path.name}; skipping")
            continue
        arr = df[col].to_numpy()
        clean, dt_out = preprocess_channel(arr, dt, settings, seed=seed)
        cached[name] = clean
        seed += 1
    fs_out = 1.0 / dt_out
    n_post = len(next(iter(cached.values()))) if cached else 0
    print(f"  cached {len(cached)} channels @ {fs_out:.2f} Hz, N={n_post}", flush=True)

    # AIS per response (used as effect-size denominator)
    ais_table: dict[str, float] = {}
    if do_ais:
        for resp in settings.responses:
            if resp not in cached:
                continue
            t0 = time.time()
            try:
                r = run_ais(cached[resp], settings)
                ais_table[resp] = r["ais_nats"]
                print(f"  AIS({resp}) = {r['ais_nats']:.4f} nats "
                      f"(p={r['p_value']:.4f}, {time.time()-t0:.0f}s)", flush=True)
            except Exception as e:
                warnings.warn(f"AIS({resp}) failed: {e}")
                ais_table[resp] = float("nan")

    rows: list[dict] = []
    case_id = outb_path.parent.parent.name  # sims/<case_id>/IEA-15-...-UMaineSemi/foo.outb

    for src_name in settings.env_sources:
        if src_name not in cached:
            continue
        for resp_name in settings.responses:
            if resp_name not in cached:
                continue
            src_arr = cached[src_name]
            resp_arr = cached[resp_name]

            # Bivariate KSG-TE
            t0 = time.time()
            try:
                r = run_bivariate_te(src_arr, resp_arr, settings)
                te_frac = (r["te_nats"] / ais_table[resp_name]
                           if (do_ais and ais_table.get(resp_name) not in (None, 0, float("nan")))
                           else float("nan"))
                rows.append({
                    "case": case_id, "source": src_name, "target": resp_name,
                    "method": "bivariate_te_ksg",
                    **r,
                    "ais_nats": ais_table.get(resp_name, float("nan")),
                    "te_frac": te_frac,
                    "runtime_s": time.time() - t0,
                })
                print(f"  bivariate_KSG  {src_name:>10} -> {resp_name:>10}  "
                      f"TE={r['te_nats']:+.4f} p={r['p_value']:.4f}  "
                      f"({time.time()-t0:.0f}s)", flush=True)
            except Exception as e:
                warnings.warn(f"bivariate_te {src_name}->{resp_name}: {e}")

            # Bivariate Gaussian-Granger baseline (same pipeline, swap estimator)
            if do_granger:
                t0 = time.time()
                try:
                    r = run_bivariate_te(src_arr, resp_arr, settings,
                                         estimator="JidtGaussianCMI")
                    rows.append({
                        "case": case_id, "source": src_name, "target": resp_name,
                        "method": "bivariate_granger",
                        **r,
                        "ais_nats": ais_table.get(resp_name, float("nan")),
                        "te_frac": float("nan"),
                        "runtime_s": time.time() - t0,
                    })
                    print(f"  bivariate_GAUS {src_name:>10} -> {resp_name:>10}  "
                          f"I={r['te_nats']:+.4f} p={r['p_value']:.4f}  "
                          f"({time.time()-t0:.0f}s)", flush=True)
                except Exception as e:
                    warnings.warn(f"granger {src_name}->{resp_name}: {e}")

            # Conditional KSG-TE: TE(src -> resp | other_env)
            if do_conditional:
                other_env = next((s for s in settings.env_sources
                                  if s != src_name and s in cached), None)
                if other_env is not None:
                    t0 = time.time()
                    try:
                        r = run_multivariate_te(
                            src_arr, resp_arr, cached[other_env], settings,
                        )
                        te_frac = (r["te_nats"] / ais_table[resp_name]
                                   if (do_ais and ais_table.get(resp_name)
                                       not in (None, 0, float("nan")))
                                   else float("nan"))
                        rows.append({
                            "case": case_id, "source": src_name, "target": resp_name,
                            "method": f"conditional_te_ksg|{other_env}",
                            **r,
                            "ais_nats": ais_table.get(resp_name, float("nan")),
                            "te_frac": te_frac,
                            "runtime_s": time.time() - t0,
                        })
                        print(f"  cond_KSG       {src_name:>10} -> {resp_name:>10} "
                              f"| {other_env:<9} TE={r['te_nats']:+.4f} "
                              f"p={r['p_value']:.4f} ({time.time()-t0:.0f}s)", flush=True)
                    except Exception as e:
                        warnings.warn(f"cond_te {src_name}->{resp_name}|{other_env}: {e}")

            # Coherence baseline
            if do_coherence:
                try:
                    coh = coherence_baseline(
                        src_arr, resp_arr, fs_out,
                        settings.band_lo_hz, settings.band_hi_hz,
                    )
                    rows.append({
                        "case": case_id, "source": src_name, "target": resp_name,
                        "method": "coherence_scipy",
                        "te_nats": coh["gamma2_peak"],         # γ² in te_nats slot for unified schema
                        "p_value": float("nan"),
                        "significant": bool(coh["gamma2_peak"] > 0.3),  # rough threshold
                        "ais_nats": ais_table.get(resp_name, float("nan")),
                        "te_frac": float("nan"),
                        "gamma2_peak_hz": coh["gamma2_peak_hz"],
                        "runtime_s": 0.0,
                    })
                except Exception as e:
                    warnings.warn(f"coherence {src_name}->{resp_name}: {e}")

    print(f"  case done in {time.time()-t_load0:.0f}s, {len(rows)} rows", flush=True)
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# Cross-case aggregation + graph
# ----------------------------------------------------------------------------

def build_graph(df_results: pd.DataFrame, method: str = "bivariate_te_ksg",
                p_threshold: float = 0.05):
    """NetworkX DiGraph aggregating across cases. Edge weight = mean te_frac
    (TE/(H(Y)-AIS(Y)) — fraction of externally-driven predictability).
    Only edges significant in > 50% of cases are kept."""
    import networkx as nx

    sub = df_results[df_results["method"] == method]
    g = nx.DiGraph()
    if sub.empty:
        return g
    grouped = sub.groupby(["source", "target"])
    for (src, tgt), rows in grouped:
        sig_frac = float((rows["p_value"] < p_threshold).mean())
        if sig_frac <= 0.5:
            continue
        weight = float(rows["te_frac"].mean())
        g.add_edge(src, tgt,
                   weight=weight,
                   mean_te_nats=float(rows["te_nats"].mean()),
                   mean_p=float(rows["p_value"].mean()),
                   sig_frac=sig_frac,
                   n_cases=int(len(rows)))
    return g


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path,
                        help="One or more OpenFAST .outb files")
    parser.add_argument("-o", "--output", type=Path,
                        default=PROJECT_ROOT / "reports" / "te_table.parquet",
                        help="Output parquet path for the long-form table")
    parser.add_argument("--graph-out", type=Path,
                        default=None,
                        help="Optional output path for pickled NetworkX graph")
    parser.add_argument("--decimate-target-hz", type=float, default=5.0)
    parser.add_argument("--transient-drop-s", type=float, default=600.0)
    parser.add_argument("--max-lag", type=int, default=30)
    parser.add_argument("--n-perm", type=int, default=200)
    parser.add_argument("--no-conditional", action="store_true")
    parser.add_argument("--no-granger", action="store_true")
    parser.add_argument("--no-coherence", action="store_true")
    parser.add_argument("--no-ais", action="store_true")
    parser.add_argument("--smoke", action="store_true",
                        help="Smoke-test mode: 1 env source × 1 response,"
                             " n_perm=50, no conditional/granger.")
    args = parser.parse_args()

    settings = TESettings(
        decimate_target_hz=args.decimate_target_hz,
        transient_drop_s=args.transient_drop_s,
        max_lag=args.max_lag,
        n_perm=50 if args.smoke else args.n_perm,
    )
    if args.smoke:
        settings.env_sources = ("Wind1VelX",)
        settings.responses = ("PtfmPitch",)

    dfs: list[pd.DataFrame] = []
    for inp in args.inputs:
        try:
            df = per_case_pipeline(
                inp, settings,
                do_conditional=not args.no_conditional and not args.smoke,
                do_granger=not args.no_granger and not args.smoke,
                do_coherence=not args.no_coherence,
                do_ais=not args.no_ais,
            )
            dfs.append(df)
        except Exception as e:
            warnings.warn(f"per_case_pipeline({inp}) failed: {e}")

    if not dfs:
        print("No cases produced results.")
        return 1

    full = pd.concat(dfs, ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    full.to_parquet(args.output, compression="zstd")
    print(f"\nWrote {args.output}  ({len(full)} rows)")

    # Summary by method
    print("\n=== Summary by method ===")
    for method, grp in full.groupby("method"):
        n = len(grp)
        n_sig = int(grp["significant"].sum())
        print(f"  {method:30s} {n:4d} rows  {n_sig:4d} significant ({100*n_sig/n:.0f}%)")

    # Build graph (KSG bivariate TE)
    if args.graph_out:
        import pickle
        g = build_graph(full, method="bivariate_te_ksg",
                        p_threshold=settings.alpha)
        args.graph_out.parent.mkdir(parents=True, exist_ok=True)
        with args.graph_out.open("wb") as f:
            pickle.dump(g, f)
        print(f"Wrote graph ({g.number_of_nodes()} nodes, "
              f"{g.number_of_edges()} edges) to {args.graph_out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
