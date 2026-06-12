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
import math
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field, replace
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
    # Embedding window: needs to span at least one period of the slowest
    # dynamics of interest. Platform pitch / surge / heave eigenfrequencies
    # for VolturnUS-S are ~0.0345 / 0.01 / 0.05 Hz; the wave second-order
    # difference-frequency forcing (DiffQTF=12 in HydroDyn) drives pitch at
    # the pitch natural frequency, period ~29 s = 145 samples at 5 Hz.
    # max_lag=150 captures one full slow-drift cycle. Raised from 30 on
    # 2026-05-20 after the slow-drift physics correction (see report §6.3).
    max_lag: int = 150                  # = 30 s window at 5 Hz
    min_lag: int = 1
    # Embedding candidate spacing (IDTxl `tau`/`tau_sources`/`tau_target`).
    # tau=1 considers every lag 1..max_lag (default, PLAN-canonical). tau>1
    # thins the candidate grid — tau=5 keeps the same max_lag window but cuts
    # 150 candidates to ~30, the main lever against the serial greedy search.
    # Changes the embedding, hence the AIS/TE values: validate against the
    # tau=1 baseline before trusting a sweep. Must satisfy 0 < tau <= max_lag.
    tau: int = 1
    n_perm: int = 200
    alpha: float = 0.05
    perm_type: str = "circular"         # 2026-05-15 reconciliation
    # KSG CMI backend. "JidtKraskovCMI" = JVM CPU (default, no GPU needed);
    # "OpenCLKraskovCMI" = GPU, batches the n_perm surrogate CMIs onto the
    # device — the dominant cost in significance testing. Granger always
    # uses JidtGaussianCMI regardless (analytic, GPU buys nothing).
    ksg_estimator: str = "JidtKraskovCMI"
    gpuid: int = 0
    # Parallelism. n_workers=1 keeps the original serial path. With >1, the
    # independent AIS/TE jobs run in a spawn-based process pool, round-robined
    # across gpu_ids (each worker drives its own OpenCL context). Since a single
    # N~15k KSG estimate leaves an A100 almost idle (latency-bound), packing
    # many jobs per device is how the wall-clock actually drops.
    n_workers: int = 1
    gpu_ids: tuple = (0,)
    # Coherence-baseline band
    band_lo_hz: float = 0.01
    band_hi_hz: float = 0.5
    # Welch segment length for coherence γ²(f). 4096 samples at 5 Hz gives
    # Δf ≈ 0.0012 Hz, sharp enough to resolve the platform pitch eigenfreq
    # (0.0345 Hz) separately from the JONSWAP peak (0.077 Hz for Tp=12.95).
    # Raised from 256 on 2026-05-20.
    coherence_nperseg: int = 4096
    # Optional: limit pairs to enable smoke testing
    env_sources: tuple = DEFAULT_ENV_SOURCES
    responses: tuple = DEFAULT_RESPONSES
    # Per-target tau override for the slow-drift platform channels. At tau=1 the
    # greedy multivariate search over max_lag=150 candidates on PtfmPitch/PtfmHeave
    # hangs the OpenCL KSG kernel (deadlocking the pool) or goes singular in the
    # Gaussian estimator (TE=nan). slow_drift_tau=5 thins ~150 lags to ~30, which
    # those channels need; 0 disables the override (all targets use `tau`).
    # See concepts/slow-drift-tau or memory project_slowdrift_tau5_fix.
    slow_drift_targets: tuple = ("PtfmPitch", "PtfmHeave")
    slow_drift_tau: int = 0
    # Per-job wall-clock cap (s) for the worker pool. A single hung OpenCL kernel
    # must not deadlock the whole sweep again: when >0, jobs run in a watchdog'd
    # spawn pool and any job exceeding this is terminated and flagged ok=False
    # (its row is simply dropped). 0 keeps the original ProcessPoolExecutor path.
    # 9000 s ≈ 2.5 h sits well above the ~1.7 h legit conditional max.
    job_timeout_s: float = 9000.0


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
        base["tau"] = settings.tau
    else:
        base["max_lag_sources"] = settings.max_lag
        base["min_lag_sources"] = settings.min_lag
        base["max_lag_target"] = settings.max_lag
        base["tau_sources"] = settings.tau
        base["tau_target"] = settings.tau
    return base


_OPENCL_PATCHED = False


def _patch_opencl_scalar_return() -> None:
    """Reconcile IDTxl's OpenCL estimators with numpy 2.x.

    OpenCLKraskovCMI/MI.estimate() returns a (n_chunks,) array. Two IDTxl call
    sites consume the result incompatibly:
      * network_analysis._calculate_single_link does `links[i] = estimate(...)`
        and needs a SCALAR — numpy 2.x won't put a 1-element array into a scalar
        slot ("setting an array element with a sequence").
      * stats.max_statistic_*_bivariate call estimate_parallel(...) and iterate
        the result, so they need an ARRAY — a coerced float gives "'float'
        object is not iterable".
    numpy 1.x's 1-element array satisfied both; numpy 2.x neither uniformly. So
    coerce a single averaged value to float ONLY while inside
    _calculate_single_link (gated by a per-estimator flag), leaving the
    estimate_parallel/iterating paths as arrays. Multi-chunk surrogate batches
    (size==n_perm) and local-value/return_counts paths are never coerced. No-op
    when the OpenCL estimators / IDTxl aren't importable (CPU runs)."""
    global _OPENCL_PATCHED
    if _OPENCL_PATCHED:
        return
    try:
        from idtxl import estimators_opencl as ocl
        from idtxl.network_analysis import NetworkAnalysis
    except Exception:
        return

    # 1. estimate(): coerce size-1 -> float only when the scoping flag is set.
    for name in ("OpenCLKraskovCMI", "OpenCLKraskovMI"):
        cls = getattr(ocl, name, None)
        if cls is None or getattr(cls, "_te_scalar_patched", False):
            continue
        orig = cls.estimate

        def estimate(self, *args, _orig=orig, **kwargs):
            out = _orig(self, *args, **kwargs)
            if (getattr(self, "_te_coerce_single", False)
                    and isinstance(out, np.ndarray) and out.size == 1
                    and not self.settings.get("local_values", False)
                    and not self.settings.get("return_counts", False)):
                return float(out.reshape(-1)[0])
            return out

        cls.estimate = estimate
        cls._te_scalar_patched = True

    # 2. _calculate_single_link(): enable coercion only for its scalar-slot loop
    #    (links[i] = estimate(...)). The estimate_parallel paths that iterate the
    #    result stay outside this scope and keep their arrays.
    if not getattr(NetworkAnalysis, "_te_link_patched", False):
        orig_link = NetworkAnalysis._calculate_single_link

        def _calculate_single_link(self, *args, _orig=orig_link, **kwargs):
            est = getattr(self, "_cmi_estimator", None)
            prev = getattr(est, "_te_coerce_single", False) if est is not None else False
            if est is not None:
                est._te_coerce_single = True
            try:
                return _orig(self, *args, **kwargs)
            finally:
                if est is not None:
                    est._te_coerce_single = prev

        NetworkAnalysis._calculate_single_link = _calculate_single_link
        NetworkAnalysis._te_link_patched = True

    _OPENCL_PATCHED = True


def _apply_estimator(s: dict, estimator: str, settings: TESettings) -> dict:
    """Set the CMI estimator + its estimator-specific keys, in place.

    The base settings stringify kraskov_k for JIDT (Java side wants a str),
    but OpenCLKraskovCMI uses it as an int32 in the GPU kernel call and needs
    a `gpuid`. Gaussian ignores k entirely. Keep this the single place that
    knows the per-backend quirks."""
    s["cmi_estimator"] = estimator
    if estimator.startswith("OpenCL"):
        s["kraskov_k"] = int(settings.kraskov_k)
        s["gpuid"] = int(settings.gpuid)
        _patch_opencl_scalar_return()
    return s


def _extract_te_pval(target_results: dict) -> tuple[float, float, list]:
    te = target_results.get("te")
    pval = target_results.get("omnibus_pval")
    selected = target_results.get("selected_vars_sources") or []
    te_val = float(te[0]) if (te is not None and len(te) > 0) else 0.0
    p_val = float(pval) if pval is not None else 1.0
    return te_val, p_val, list(selected)


def run_bivariate_te(source: np.ndarray, target: np.ndarray,
                     settings: TESettings, estimator: str | None = None) -> dict:
    """Bivariate TE(source → target). Returns dict with te, p_value, selected_vars.

    estimator=None uses settings.ksg_estimator (CPU or OpenCL/GPU); Granger
    callers pass JidtGaussianCMI explicitly."""
    from idtxl.bivariate_te import BivariateTE
    from idtxl.data import Data

    estimator = estimator or settings.ksg_estimator
    data = Data(np.vstack([source, target]), dim_order="ps", normalise=True)
    # Set max_shift now that we know N (required for perm_type='circular')
    s = _apply_estimator(
        {**_idtxl_base_settings(settings), "max_shift": max(1, len(target) // 4)},
        estimator, settings)
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
                        estimator: str | None = None) -> dict:
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

    estimator = estimator or settings.ksg_estimator
    data = Data(arr, dim_order="ps", normalise=True)
    s = _apply_estimator(
        {**_idtxl_base_settings(settings), "max_shift": max(1, target.shape[0] // 4)},
        estimator, settings)
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
    s = _apply_estimator(
        {
            **_idtxl_base_settings(settings, for_ais=True),
            "max_shift": max(1, len(target) // 4),
        },
        settings.ksg_estimator, settings)
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
                       fs: float, band_lo: float, band_hi: float,
                       nperseg_target: int = 4096) -> dict:
    """Peak magnitude-squared coherence γ²(f) in the [band_lo, band_hi] Hz band.

    nperseg_target sets the upper cap on the Welch segment length; the
    actual nperseg used is min(N//4, nperseg_target). For our 15001-sample
    case at 5 Hz, nperseg=4096 gives Δf≈0.0012 Hz, enough resolution to
    separate the platform pitch eigenfreq (0.0345 Hz) from the JONSWAP
    peak (~0.077 Hz at Tp=12.95 s)."""
    from scipy.signal import coherence
    nperseg = min(len(source) // 4, nperseg_target)
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
# Parallel job execution (one heavy IDTxl task per job)
# ----------------------------------------------------------------------------

def _te_frac(te_nats: float, ais_val: float, do_ais: bool) -> float:
    """TE / AIS effect-size fraction; NaN when the denominator is unusable."""
    if not do_ais or ais_val is None:
        return float("nan")
    try:
        if ais_val == 0 or math.isnan(ais_val):
            return float("nan")
    except TypeError:
        return float("nan")
    return te_nats / ais_val


def _run_heavy_job(job: dict, settings: "TESettings") -> dict:
    """Worker entry point: run one AIS/TE task, returning metadata + result
    (never the input arrays, to keep the pickled return small).

    Pinned to job['gpuid'] so a pool spreads OpenCL work across devices.
    Exceptions are caught and flagged ok=False so one bad pair can't sink the
    whole sweep — mirrors the per-task try/except of the serial version.
    """
    s = replace(settings, gpuid=job["gpuid"])
    # Slow-drift platform channels need a thinned candidate grid (tau=5) or the
    # greedy search hangs / goes singular. Applied per target so the rest stay tau=1.
    if settings.slow_drift_tau and job.get("target") in settings.slow_drift_targets:
        s = replace(s, tau=settings.slow_drift_tau)
    kind = job["kind"]
    arr = job["arrays"]
    t0 = time.time()
    ok, err, r = True, None, {}
    try:
        if kind == "ais":
            r = run_ais(arr["target"], s)
        elif kind == "bivariate_ksg":
            r = run_bivariate_te(arr["src"], arr["target"], s)
        elif kind == "granger":
            r = run_bivariate_te(arr["src"], arr["target"], s,
                                 estimator="JidtGaussianCMI")
        elif kind == "conditional":
            r = run_multivariate_te(arr["src"], arr["target"], arr["cond"], s)
        else:
            raise ValueError(f"unknown job kind {kind!r}")
    except Exception as e:
        import traceback
        ok, err = False, f"{type(e).__name__}: {e}"
        traceback.print_exc()
        sys.stderr.flush()
    dt = time.time() - t0
    label = f"{kind:13s} {(job.get('source') or '-'):>10} -> {job['target']:<10}"
    if ok and kind == "ais":
        print(f"  [done {dt:5.0f}s gpu{job['gpuid']}] AIS({job['target']}) "
              f"= {r.get('ais_nats', float('nan')):.4f} nats "
              f"(p={r.get('p_value', 1.0):.4f})", flush=True)
    elif ok:
        print(f"  [done {dt:5.0f}s gpu{job['gpuid']}] {label} "
              f"TE={r.get('te_nats', float('nan')):+.4f} "
              f"p={r.get('p_value', 1.0):.4f}", flush=True)
    else:
        print(f"  !! [{label}] {err}", file=sys.stderr, flush=True)
    return {"kind": kind, "source": job.get("source"), "target": job["target"],
            "other_env": job.get("other_env"), "result": r, "ok": ok,
            "runtime_s": dt, "tau_used": s.tau}


def _pool_child(job: dict, settings: "TESettings", q) -> None:
    """Spawn-pool entry point: run one job and put its result on the queue."""
    q.put(_run_heavy_job(job, settings))


def _execute_watchdog(jobs: list, settings: "TESettings",
                      n_workers: int, timeout_s: float) -> list:
    """Run jobs up to n_workers at a time, each in its own spawned child pinned
    to its pre-assigned gpuid. Any child exceeding timeout_s is terminated and
    flagged ok=False — so one hung OpenCL kernel can't deadlock the whole sweep.
    Returns the same list-of-result-dicts shape as the ProcessPoolExecutor path."""
    ctx = mp.get_context("spawn")
    pending, running, results = list(jobs), [], []

    def launch(job):
        q = ctx.Queue()
        p = ctx.Process(target=_pool_child, args=(job, settings, q))
        p.start()
        return {"job": job, "proc": p, "queue": q, "t0": time.time()}

    while pending or running:
        while pending and len(running) < n_workers:
            running.append(launch(pending.pop(0)))
        time.sleep(5)
        still = []
        for d in running:
            p, job = d["proc"], d["job"]
            if not p.is_alive():
                try:
                    results.append(d["queue"].get(timeout=10))
                except Exception:
                    print(f"  !! [{job['kind']} {job.get('source')}->{job['target']}] "
                          f"crashed with no result", file=sys.stderr, flush=True)
                    results.append({"kind": job["kind"], "source": job.get("source"),
                                    "target": job["target"],
                                    "other_env": job.get("other_env"),
                                    "result": {}, "ok": False,
                                    "runtime_s": time.time() - d["t0"],
                                    "tau_used": settings.tau})
            elif time.time() - d["t0"] > timeout_s:
                p.terminate(); p.join()
                print(f"  !! TIMEOUT {timeout_s:.0f}s: {job['kind']} "
                      f"{job.get('source')}->{job['target']} (terminated)",
                      file=sys.stderr, flush=True)
                results.append({"kind": job["kind"], "source": job.get("source"),
                                "target": job["target"],
                                "other_env": job.get("other_env"),
                                "result": {}, "ok": False,
                                "runtime_s": time.time() - d["t0"],
                                "tau_used": settings.tau})
            else:
                still.append(d)
        running = still
    return results


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

    rows: list[dict] = []
    case_id = outb_path.parent.parent.name  # sims/<case_id>/IEA-15-...-UMaineSemi/foo.outb

    # Coherence baseline is cheap scipy (no IDTxl, no GPU): compute inline.
    # ais_nats is backfilled once the AIS jobs land below.
    if do_coherence:
        for src_name in settings.env_sources:
            if src_name not in cached:
                continue
            for resp_name in settings.responses:
                if resp_name not in cached:
                    continue
                try:
                    coh = coherence_baseline(
                        cached[src_name], cached[resp_name], fs_out,
                        settings.band_lo_hz, settings.band_hi_hz,
                        nperseg_target=settings.coherence_nperseg,
                    )
                    rows.append({
                        "case": case_id, "source": src_name, "target": resp_name,
                        "method": "coherence_scipy",
                        "te_nats": coh["gamma2_peak"],   # γ² in te_nats slot for unified schema
                        "p_value": float("nan"),
                        "significant": bool(coh["gamma2_peak"] > 0.3),  # rough threshold
                        "ais_nats": float("nan"),
                        "te_frac": float("nan"),
                        "gamma2_peak_hz": coh["gamma2_peak_hz"],
                        "runtime_s": 0.0,
                    })
                except Exception as e:
                    print(f"  !! coherence {src_name}->{resp_name} raised "
                          f"{type(e).__name__}: {e}", file=sys.stderr, flush=True)
                    sys.stderr.flush()

    # Build the heavy IDTxl jobs. Each is independent; the bivariate/conditional
    # te_frac needs the target's AIS, but that's resolved at assembly after all
    # jobs finish, so AIS and TE can run concurrently rather than AIS-then-TE.
    gpu_ids = list(settings.gpu_ids) or [settings.gpuid]
    jobs: list[dict] = []
    if do_ais:
        for resp in settings.responses:
            if resp in cached:
                jobs.append({"kind": "ais", "source": None, "target": resp,
                             "arrays": {"target": cached[resp]}})
    for src_name in settings.env_sources:
        if src_name not in cached:
            continue
        for resp_name in settings.responses:
            if resp_name not in cached:
                continue
            common = {"src": cached[src_name], "target": cached[resp_name]}
            jobs.append({"kind": "bivariate_ksg", "source": src_name,
                         "target": resp_name, "arrays": common})
            if do_granger:
                jobs.append({"kind": "granger", "source": src_name,
                             "target": resp_name, "arrays": common})
            if do_conditional:
                other_env = next((s for s in settings.env_sources
                                  if s != src_name and s in cached), None)
                if other_env is not None:
                    jobs.append({"kind": "conditional", "source": src_name,
                                 "target": resp_name, "other_env": other_env,
                                 "arrays": {**common, "cond": cached[other_env]}})
    for i, job in enumerate(jobs):
        job["gpuid"] = gpu_ids[i % len(gpu_ids)]

    # Execute: serial when n_workers<=1 (original path), else a spawn-based pool.
    n_workers = max(1, settings.n_workers)
    print(f"  {len(jobs)} IDTxl jobs | {n_workers} worker(s) | gpus={gpu_ids}",
          flush=True)
    results: list[dict] = []
    if n_workers == 1 and settings.job_timeout_s <= 0:
        for job in jobs:
            results.append(_run_heavy_job(job, settings))
    elif settings.job_timeout_s > 0:
        # Watchdog pool: a hung OpenCL kernel is terminated, not fatal.
        print(f"  (per-job timeout {settings.job_timeout_s:.0f}s)", flush=True)
        results = _execute_watchdog(jobs, settings, n_workers, settings.job_timeout_s)
    else:
        ctx = mp.get_context("spawn")
        with ProcessPoolExecutor(max_workers=n_workers, mp_context=ctx) as ex:
            futures = [ex.submit(_run_heavy_job, job, settings) for job in jobs]
            for fut in as_completed(futures):
                results.append(fut.result())

    # Assemble: AIS table first (effect-size denominator), then the TE rows.
    ais_table: dict[str, float] = {}
    for res in results:
        if res["kind"] == "ais":
            ais_table[res["target"]] = (
                res["result"].get("ais_nats", float("nan"))
                if res["ok"] else float("nan"))
    for row in rows:  # backfill ais_nats onto the coherence rows
        row["ais_nats"] = ais_table.get(row["target"], float("nan"))

    for res in results:
        if res["kind"] == "ais" or not res["ok"]:
            continue
        r = res["result"]
        src_name, resp_name = res["source"], res["target"]
        ais_val = ais_table.get(resp_name, float("nan"))
        tau_used = res.get("tau_used", settings.tau)
        if res["kind"] == "bivariate_ksg":
            rows.append({
                "case": case_id, "source": src_name, "target": resp_name,
                "method": "bivariate_te_ksg", **r,
                "ais_nats": ais_val,
                "te_frac": _te_frac(r["te_nats"], ais_val, do_ais),
                "runtime_s": res["runtime_s"], "tau": tau_used,
            })
        elif res["kind"] == "granger":
            rows.append({
                "case": case_id, "source": src_name, "target": resp_name,
                "method": "bivariate_granger", **r,
                "ais_nats": ais_val, "te_frac": float("nan"),
                "runtime_s": res["runtime_s"], "tau": tau_used,
            })
        elif res["kind"] == "conditional":
            rows.append({
                "case": case_id, "source": src_name, "target": resp_name,
                "method": f"conditional_te_ksg|{res['other_env']}", **r,
                "ais_nats": ais_val,
                "te_frac": _te_frac(r["te_nats"], ais_val, do_ais),
                "runtime_s": res["runtime_s"], "tau": tau_used,
            })

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
    parser.add_argument("--max-lag", type=int, default=150,
                        help="Embedding window in samples (at decimated rate). "
                             "Default 150 = 30 s at 5 Hz, covers one slow-drift cycle.")
    parser.add_argument("--n-perm", type=int, default=200)
    parser.add_argument("--tau", type=int, default=1,
                        help="Embedding candidate spacing (1 = every lag). "
                             "tau=5 keeps the max-lag window but thins ~150 "
                             "candidates to ~30 — the main per-task speedup. "
                             "Changes AIS/TE values; validate vs tau=1 first. "
                             "Must be 0 < tau <= max_lag.")
    parser.add_argument("--gpu", action="store_true",
                        help="Use the OpenCLKraskovCMI GPU estimator for KSG "
                             "(needs pyopencl + an OpenCL driver). Granger stays "
                             "on the analytic Gaussian estimator either way.")
    parser.add_argument("--gpuid", type=int, default=0,
                        help="OpenCL device ID when --gpu is set (default 0). "
                             "Ignored if --gpus lists multiple devices.")
    parser.add_argument("--workers", type=int, default=1,
                        help="Parallel worker processes for the heavy AIS/TE "
                             "jobs. 1 = serial (default). The jobs are "
                             "independent, so this is the main wall-clock lever "
                             "given the per-estimate GPU work is latency-bound.")
    parser.add_argument("--gpus", type=str, default=None,
                        help="Comma-separated OpenCL device IDs to round-robin "
                             "KSG jobs across, e.g. '0,1'. Defaults to --gpuid.")
    parser.add_argument("--slow-drift-tau", type=int, default=0,
                        help="Per-target tau override for the slow-drift platform "
                             "channels (--slow-drift-targets). 0 = off. Use 5: at "
                             "tau=1 those channels hang the OpenCL KSG kernel or go "
                             "singular (TE=nan); tau=5 thins ~150 lags to ~30 so they "
                             "complete. Reran rows carry the per-target tau in output.")
    parser.add_argument("--slow-drift-targets", type=str, default="PtfmPitch,PtfmHeave",
                        help="Comma-separated targets that get --slow-drift-tau.")
    parser.add_argument("--job-timeout", type=float, default=9000.0,
                        help="Per-job wall-clock cap (s). >0 runs jobs in a watchdog "
                             "pool that terminates any hung job (so one stuck OpenCL "
                             "kernel can't deadlock the sweep). 0 = original pool. "
                             "Default 9000 (~2.5 h) sits above the legit conditional max.")
    parser.add_argument("--no-conditional", action="store_true")
    parser.add_argument("--no-granger", action="store_true")
    parser.add_argument("--no-coherence", action="store_true")
    parser.add_argument("--no-ais", action="store_true")
    parser.add_argument("--smoke", action="store_true",
                        help="Smoke-test mode: 1 env source × 1 response,"
                             " n_perm=50, no conditional/granger.")
    args = parser.parse_args()

    gpu_ids = (tuple(int(x) for x in args.gpus.split(",") if x.strip() != "")
               if args.gpus else (args.gpuid,))

    settings = TESettings(
        decimate_target_hz=args.decimate_target_hz,
        transient_drop_s=args.transient_drop_s,
        max_lag=args.max_lag,
        tau=args.tau,
        n_perm=50 if args.smoke else args.n_perm,
        ksg_estimator="OpenCLKraskovCMI" if args.gpu else "JidtKraskovCMI",
        gpuid=gpu_ids[0],
        n_workers=args.workers,
        gpu_ids=gpu_ids,
        slow_drift_tau=args.slow_drift_tau,
        slow_drift_targets=tuple(
            t.strip() for t in args.slow_drift_targets.split(",") if t.strip()),
        job_timeout_s=args.job_timeout,
    )
    if args.smoke:
        settings.env_sources = ("Wind1VelX",)
        settings.responses = ("PtfmPitch",)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    dfs: list[pd.DataFrame] = []
    for i, inp in enumerate(args.inputs, 1):
        print(f"\n=== [{i}/{len(args.inputs)}] {inp} ===", flush=True)
        try:
            df = per_case_pipeline(
                inp, settings,
                do_conditional=not args.no_conditional and not args.smoke,
                do_granger=not args.no_granger and not args.smoke,
                do_coherence=not args.no_coherence,
                do_ais=not args.no_ais,
            )
            dfs.append(df)
            print(f"  [{i}/{len(args.inputs)}] OK ({len(df)} rows)", flush=True)
        except Exception as e:
            import traceback
            print(f"!! per_case_pipeline({inp}) raised {type(e).__name__}: {e}",
                  file=sys.stderr, flush=True)
            traceback.print_exc()
            sys.stderr.flush()
        except BaseException as e:
            import traceback
            print(f"!! per_case_pipeline({inp}) killed by {type(e).__name__}: {e}",
                  file=sys.stderr, flush=True)
            traceback.print_exc()
            sys.stderr.flush()
            raise

        # Checkpoint: write partial parquet after every case so a later crash
        # doesn't lose what we already computed.
        if dfs:
            try:
                pd.concat(dfs, ignore_index=True).to_parquet(
                    args.output, compression="zstd")
                print(f"  [checkpoint] {args.output.name}: {sum(len(d) for d in dfs)} rows "
                      f"across {len(dfs)} case(s)", flush=True)
            except Exception as e:
                print(f"!! checkpoint write failed: {e}", file=sys.stderr, flush=True)

    if not dfs:
        print("No cases produced results.")
        return 1

    full = pd.concat(dfs, ignore_index=True)
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
