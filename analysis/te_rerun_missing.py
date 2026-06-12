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
def parse_logs(log_paths):
    """Union the [done jobs across one or more logs. Returns (done_set,
    te_records, ais_table).

    NaN TE lines (TE=+nan) and `!! TIMEOUT` lines never match the regexes, so a
    failed/terminated job stays 'missing' and gets rerun — exactly what we want
    when harvesting a partial rerun log alongside the original run.
    """
    done, te_records, ais_table = set(), [], {}
    for log_path in log_paths:
        lp = Path(log_path)
        if not lp.exists():
            print(f"  (log {lp} not found — skipped)", flush=True)
            continue
        for line in lp.read_text(errors="replace").splitlines():
            if "[done" not in line:
                continue
            m = _RE_AIS.search(line)
            if m:
                tgt, ais = m.group(1), float(m.group(2))
                done.add(("ais", None, tgt))
                ais_table.setdefault(tgt, ais)       # first valid wins; ignores dups
                continue
            m = _RE_TE.search(line)
            if m:
                kind, src, tgt = m.group(1), m.group(2), m.group(3)
                key = (kind, src, tgt)
                if key in done:                       # skip duplicate log lines
                    continue
                done.add(key)
                te_records.append({"kind": kind, "source": src, "target": tgt,
                                   "te_nats": float(m.group(4)),
                                   "p_value": float(m.group(5))})
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


def _fail_row(job, t0, flag):
    return {"kind": job["kind"], "source": job.get("source"),
            "target": job["target"], "other_env": job.get("other_env"),
            "ok": False, "result": {}, "runtime_s": time.time() - t0, flag: True}


def run_jobs_watchdog(jobs, settings, timeout_s, gpu_ids, max_parallel):
    """Run jobs concurrently (up to max_parallel at once), each in its own
    spawned child pinned to a round-robin GPU. Any child that exceeds
    timeout_s is terminated and flagged — a re-hang can't stall the others."""
    ctx = mp.get_context("spawn")
    pending = list(enumerate(jobs))
    running, results = [], []

    def launch(idx, job):
        job = dict(job)
        job["gpuid"] = gpu_ids[idx % len(gpu_ids)]
        q = ctx.Queue()
        p = ctx.Process(target=_child, args=(job, settings, q))
        p.start()
        print(f"[launch] {job['kind']:13s} {(job.get('source') or '-'):>10} -> "
              f"{job['target']:<10} gpu{job['gpuid']} pid={p.pid}", flush=True)
        return {"job": job, "proc": p, "queue": q, "t0": time.time()}

    while pending or running:
        while pending and len(running) < max_parallel:
            running.append(launch(*pending.pop(0)))
        time.sleep(5)
        still = []
        for d in running:
            p, job = d["proc"], d["job"]
            if not p.is_alive():
                try:
                    results.append(d["queue"].get(timeout=10))
                except Exception:
                    print(f"  !! CRASH (no result): {job['kind']} "
                          f"{job.get('source')}->{job['target']}", flush=True)
                    results.append(_fail_row(job, d["t0"], "crashed"))
            elif time.time() - d["t0"] > timeout_s:
                p.terminate(); p.join()
                print(f"  !! TIMEOUT after {timeout_s}s: {job['kind']} "
                      f"{job.get('source')}->{job['target']} (terminated)", flush=True)
                results.append(_fail_row(job, d["t0"], "timeout"))
            else:
                still.append(d)
        running = still
    return results


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
    ap.add_argument("--log", type=Path, nargs="+",
                    default=[Path("/tmp/te_v08_full.log")],
                    help="one or more logs to harvest [done lines from (later "
                         "reruns can append /tmp/rerun.log here)")
    ap.add_argument("--out", type=Path, default=Path("/tmp/te_v08_full.parquet"))
    ap.add_argument("--gpu", action="store_true", help="OpenCL KSG (default if neither flag given)")
    ap.add_argument("--cpu", action="store_true", help="force JidtKraskovCMI (no OpenCL hang)")
    ap.add_argument("--gpus", type=str, default="0,1")
    ap.add_argument("--max-lag", type=int, default=150)
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--tau", type=int, default=1,
                    help="embedding candidate spacing for the RERUN jobs; tau=5 "
                         "thins ~150 lags to ~30 (untangles the slow-drift channels). "
                         "Reran rows are tagged with this tau in the parquet.")
    ap.add_argument("--max-parallel", type=int, default=4,
                    help="how many rerun jobs to run at once (round-robined across --gpus)")
    ap.add_argument("--force-targets", type=str, default="",
                    help="comma-separated targets to recompute ENTIRELY at --tau, "
                         "even if already done (e.g. PtfmPitch,PtfmHeave). Their "
                         "salvaged rows are dropped so the target ends up uniform "
                         "in tau — for the slow-drift channels that needed tau=5.")
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

    # 1. salvage (union across every log given)
    done, te_records, ais_table = parse_logs(args.log)
    print(f"[salvage] {len(done)} unique jobs across {len(args.log)} log(s) "
          f"({len(te_records)} TE rows, {len(ais_table)} AIS)", flush=True)

    # 2. prepare arrays + figure out what is missing
    cached, fs_out = build_cache(args.outb, settings)
    present = set(cached)
    force = {t.strip() for t in args.force_targets.split(",") if t.strip()}
    if force:
        print(f"[force] recomputing all edges for {sorted(force)} at tau={settings.tau}",
              flush=True)
    missing = [j for j in expected_jobs(settings, present)
               if (j not in done) or (j[2] in force)]
    print(f"[missing] {len(missing)} job(s) to rerun:", flush=True)
    for kind, src, tgt in missing:
        print(f"    {kind:14s} {src or '-':>10} -> {tgt}", flush=True)

    # 3. rerun missing jobs concurrently, each watchdog'd
    missing_jobs = [make_job(kind, src, tgt, cached, settings, 0)
                    for kind, src, tgt in missing]
    print(f"[rerun] {len(missing_jobs)} job(s), up to {args.max_parallel} at once, "
          f"tau={settings.tau}, {settings.ksg_estimator}, timeout={args.timeout}s",
          flush=True)
    rerun_results = run_jobs_watchdog(missing_jobs, settings, args.timeout,
                                      gpu_ids, args.max_parallel)
    for res in rerun_results:
        if res.get("kind") == "ais" and res.get("ok"):
            ais_table[res["target"]] = res["result"].get("ais_nats", float("nan"))

    # 4. assemble final long-form table -------------------------------------
    rows = []

    # 4a. salvaged TE rows (drop force-target rows — they are recomputed at --tau)
    for r in te_records:
        kind, src, tgt = r["kind"], r["source"], r["target"]
        if tgt in force:
            continue
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
                     "ais_nats": ais, "te_frac": frac,
                     "tau": 1, "source_origin": "salvaged"})

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
                     "runtime_s": res.get("runtime_s"),
                     "tau": settings.tau, "source_origin": "reran"})

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
                             "tau": 1, "source_origin": "reran"})
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
