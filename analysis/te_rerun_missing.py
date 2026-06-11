"""te_rerun_missing.py — salvage + targeted rerun for the te_v08 full run.

The 2026-06-11 full run wedged: an OpenCL KSG kernel hung on the PtfmPitch
pair, deadlocking the ProcessPoolExecutor with 60 of 63 jobs done but the
per-case parquet never written. This script:

  1. parses the `[done` lines already in the log (the 60 finished jobs carry
     their TE / p / AIS values),
  2. derives the still-missing jobs by diffing against the full expected job
     set (this auto-catches the duplicate AIS line + the bivariate gap),
  3. reruns ONLY those jobs, one at a time, each in its own child process with
     a hard wall-clock timeout — so a re-hang is terminated, not fatal,
  4. recomputes the cheap scipy coherence baseline for all pairs,
  5. merges everything and writes the final long-form parquet.

Channel preprocessing (drop / decimate / per-channel jitter seed) is replicated
exactly from te_pipeline.per_case_pipeline so rerun arrays match the originals.

Usage (on lams, env fowt-te-gpu, from the repo root):
    python analysis/te_rerun_missing.py \
        --outb /home/lams/Downloads/dlca_v08ms_s00.outb \
        --log  /tmp/te_v08_full.log \
        --out  /tmp/te_v08_full.parquet \
        --gpu --gpus 0,1 --timeout 10800

If a PtfmPitch conditional hangs again on the GPU, retry that job with either
`--cpu` (JidtKraskovCMI, slow but no OpenCL hang) or `--tau 5` (thins the 150
candidate lags to ~30 — the known speed lever; validate vs tau=1 before trusting).
"""
from __future__ import annotations

import argparse
import math
import multiprocessing as mp
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "analysis"))

import te_pipeline as tp  # noqa: E402
from te_pipeline import (  # noqa: E402
    TESettings, DEFAULT_ENV_SOURCES, DEFAULT_RESPONSES,
    load_outb, find_time_column, find_channel, preprocess_channel,
    coherence_baseline, _te_frac, _run_heavy_job,
)

# regexes for the two log line shapes
_RE_TE = re.compile(
    r"\[done\s+\d+s gpu\d+\]\s+(\S+)\s+(\S+)\s+->\s+(\S+)\s+TE=([+-][\d.]+)\s+p=([\d.]+)")
_RE_AIS = re.compile(
    r"\[done\s+\d+s gpu\d+\]\s+AIS\((\S+)\)\s*=\s*([\d.eE+-]+)\s+nats\s+\(p=([\d.]+)\)")


# ---------------------------------------------------------------------------
# 1. parse the salvage log
# ---------------------------------------------------------------------------
def parse_log(log_path: Path):
    """Return (done_set, te_records, ais_table).

    done_set    : set of (kind, source|None, target) already finished
    te_records  : list of dicts for bivariate_ksg / granger / conditional
    ais_table   : {target: ais_nats}
    """
    done, te_records, ais_table = set(), [], {}
    for line in log_path.read_text(errors="replace").splitlines():
        if "[done" not in line:
            continue
        m = _RE_AIS.search(line)
        if m:
            tgt, ais, p = m.group(1), float(m.group(2)), float(m.group(3))
            done.add(("ais", None, tgt))
            ais_table.setdefault(tgt, ais)          # first wins; ignores the dup
            continue
        m = _RE_TE.search(line)
        if m:
            kind, src, tgt, te, p = (m.group(1), m.group(2), m.group(3),
                                     float(m.group(4)), float(m.group(5)))
            key = (kind, src, tgt)
            if key in done:                          # skip duplicate log lines
                continue
            done.add(key)
            te_records.append({"kind": kind, "source": src, "target": tgt,
                               "te_nats": te, "p_value": p})
    return done, te_records, ais_table


# ---------------------------------------------------------------------------
# 2. full expected job set (mirrors te_pipeline.per_case_pipeline)
# ---------------------------------------------------------------------------
def expected_jobs(settings: TESettings, present: set):
    """Every (kind, source, target) the full run should contain, restricted to
    channels actually present in the file."""
    jobs = []
    for resp in settings.responses:
        if resp in present:
            jobs.append(("ais", None, resp))
    for src in settings.env_sources:
        if src not in present:
            continue
        for resp in settings.responses:
            if resp not in present:
                continue
            jobs.append(("bivariate_ksg", src, resp))
            jobs.append(("granger", src, resp))
            other = next((s for s in settings.env_sources
                          if s != src and s in present), None)
            if other is not None:
                jobs.append(("conditional", src, resp))
    return jobs


# ---------------------------------------------------------------------------
# 3. watchdog'd single-job execution
# ---------------------------------------------------------------------------
def _child(job, settings, q):
    q.put(_run_heavy_job(job, settings))


def run_with_timeout(job, settings, timeout_s):
    """Run one heavy job in a spawned child; terminate if it exceeds timeout_s."""
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=_child, args=(job, settings, q))
    t0 = time.time()
    p.start()
    p.join(timeout_s)
    if p.is_alive():
        p.terminate(); p.join()
        print(f"  !! TIMEOUT after {timeout_s}s: {job['kind']} "
              f"{job.get('source')}->{job['target']} (terminated)", flush=True)
        return {"kind": job["kind"], "source": job.get("source"),
                "target": job["target"], "other_env": job.get("other_env"),
                "ok": False, "result": {}, "runtime_s": time.time() - t0,
                "timeout": True}
    return q.get()


# ---------------------------------------------------------------------------
# build the array cache with the SAME per-channel seeds as the original run
# ---------------------------------------------------------------------------
def build_cache(outb: Path, settings: TESettings):
    df = load_outb(outb)
    t = df[find_time_column(df)].to_numpy()
    dt = float(np.median(np.diff(t)))
    cached, dt_out, seed = {}, dt, 0
    for name in (*settings.env_sources, *settings.responses):
        try:
            col = find_channel(df, name)
        except KeyError:
            print(f"  (channel {name} absent — skipped)", flush=True)
            continue
        clean, dt_out = preprocess_channel(df[col].to_numpy(), dt, settings, seed=seed)
        cached[name] = clean
        seed += 1
    return cached, 1.0 / dt_out


def make_job(kind, src, tgt, cached, settings, gpuid):
    if kind == "ais":
        arrays = {"target": cached[tgt]}
        return {"kind": kind, "source": None, "target": tgt,
                "arrays": arrays, "gpuid": gpuid}
    common = {"src": cached[src], "target": cached[tgt]}
    job = {"kind": kind, "source": src, "target": tgt, "gpuid": gpuid}
    if kind == "conditional":
        other = next((s for s in settings.env_sources
                      if s != src and s in cached), None)
        job["other_env"] = other
        job["arrays"] = {**common, "cond": cached[other]}
    else:
        job["arrays"] = common
    return job


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outb", type=Path, default=Path("/home/lams/Downloads/dlca_v08ms_s00.outb"))
    ap.add_argument("--log", type=Path, default=Path("/tmp/te_v08_full.log"))
    ap.add_argument("--out", type=Path, default=Path("/tmp/te_v08_full.parquet"))
    ap.add_argument("--gpu", action="store_true", help="OpenCL KSG (default if neither flag given)")
    ap.add_argument("--cpu", action="store_true", help="force JidtKraskovCMI (no OpenCL hang)")
    ap.add_argument("--gpus", type=str, default="0,1")
    ap.add_argument("--max-lag", type=int, default=150)
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--tau", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=10800, help="per-job wall-clock cap (s)")
    args = ap.parse_args()

    use_gpu = args.gpu and not args.cpu
    gpu_ids = tuple(int(x) for x in args.gpus.split(",") if x.strip())
    settings = TESettings(
        max_lag=args.max_lag, n_perm=args.n_perm, tau=args.tau,
        ksg_estimator="OpenCLKraskovCMI" if use_gpu else "JidtKraskovCMI",
        gpuid=gpu_ids[0], gpu_ids=gpu_ids, n_workers=1,
        env_sources=DEFAULT_ENV_SOURCES, responses=DEFAULT_RESPONSES,
    )
    case_id = args.outb.stem

    # 1. salvage
    done, te_records, ais_table = parse_log(args.log)
    print(f"[salvage] {len(done)} unique jobs in log "
          f"({len(te_records)} TE rows, {len(ais_table)} AIS)", flush=True)

    # 2. prepare arrays + figure out what is missing
    cached, fs_out = build_cache(args.outb, settings)
    present = set(cached)
    missing = [j for j in expected_jobs(settings, present) if j not in done]
    print(f"[missing] {len(missing)} job(s) to rerun:", flush=True)
    for kind, src, tgt in missing:
        print(f"    {kind:14s} {src or '-':>10} -> {tgt}", flush=True)

    # 3. rerun missing jobs, one at a time, with the watchdog
    rerun_results = []
    for i, (kind, src, tgt) in enumerate(missing):
        gpuid = gpu_ids[i % len(gpu_ids)]
        job = make_job(kind, src, tgt, cached, settings, gpuid)
        print(f"[rerun {i+1}/{len(missing)}] {kind} {src or '-'}->{tgt} "
              f"on gpu{gpuid} ({settings.ksg_estimator})", flush=True)
        res = run_with_timeout(job, settings, args.timeout)
        rerun_results.append(res)
        if res.get("kind") == "ais" and res.get("ok"):
            ais_table[tgt] = res["result"].get("ais_nats", float("nan"))

    # 4. assemble final long-form table -------------------------------------
    rows = []

    # 4a. salvaged TE rows
    for r in te_records:
        kind, src, tgt = r["kind"], r["source"], r["target"]
        ais = ais_table.get(tgt, float("nan"))
        if kind == "bivariate_ksg":
            method = "bivariate_te_ksg"
            frac = _te_frac(r["te_nats"], ais, True)
        elif kind == "granger":
            method = "bivariate_granger"; frac = float("nan")
        elif kind == "conditional":
            other = next((s for s in settings.env_sources if s != src), "")
            method = f"conditional_te_ksg|{other}"
            frac = _te_frac(r["te_nats"], ais, True)
        else:
            continue
        rows.append({"case": case_id, "source": src, "target": tgt,
                     "method": method, "te_nats": r["te_nats"],
                     "p_value": r["p_value"],
                     "significant": bool(r["p_value"] < settings.alpha and r["te_nats"] > 0),
                     "ais_nats": ais, "te_frac": frac, "source_origin": "salvaged"})

    # 4b. reran TE rows
    for res in rerun_results:
        if res["kind"] == "ais" or not res.get("ok"):
            continue
        rr, src, tgt = res["result"], res["source"], res["target"]
        ais = ais_table.get(tgt, float("nan"))
        if res["kind"] == "bivariate_ksg":
            method, frac = "bivariate_te_ksg", _te_frac(rr["te_nats"], ais, True)
        elif res["kind"] == "granger":
            method, frac = "bivariate_granger", float("nan")
        else:
            method = f"conditional_te_ksg|{res.get('other_env','')}"
            frac = _te_frac(rr["te_nats"], ais, True)
        rows.append({"case": case_id, "source": src, "target": tgt,
                     "method": method, **rr, "ais_nats": ais, "te_frac": frac,
                     "runtime_s": res.get("runtime_s"), "source_origin": "reran"})

    # 4c. coherence baseline (cheap scipy — recompute fresh for every pair)
    for src in settings.env_sources:
        if src not in cached:
            continue
        for tgt in settings.responses:
            if tgt not in cached:
                continue
            try:
                coh = coherence_baseline(cached[src], cached[tgt], fs_out,
                                         settings.band_lo_hz, settings.band_hi_hz,
                                         nperseg_target=settings.coherence_nperseg)
                rows.append({"case": case_id, "source": src, "target": tgt,
                             "method": "coherence_scipy", "te_nats": coh["gamma2_peak"],
                             "p_value": float("nan"),
                             "significant": bool(coh["gamma2_peak"] > 0.3),
                             "ais_nats": ais_table.get(tgt, float("nan")),
                             "te_frac": float("nan"),
                             "gamma2_peak_hz": coh["gamma2_peak_hz"],
                             "source_origin": "reran"})
            except Exception as e:
                print(f"  !! coherence {src}->{tgt}: {e}", flush=True)

    full = pd.DataFrame(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    full.to_parquet(args.out, compression="zstd")
    print(f"\n[write] {args.out}  ({len(full)} rows)", flush=True)

    # summary
    print("\n=== merged summary by method ===")
    for method, grp in full.groupby("method"):
        nsig = int(grp["significant"].sum())
        print(f"  {method:28s} {len(grp):3d} rows  {nsig:3d} significant")
    timed_out = [r for r in rerun_results if r.get("timeout")]
    if timed_out:
        print("\n!! still-hanging jobs (terminated; rows absent from parquet):")
        for r in timed_out:
            print(f"   {r['kind']} {r.get('source')}->{r['target']} "
                  f"— try --cpu or --tau 5 for this one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
