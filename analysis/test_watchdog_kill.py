#!/usr/bin/env python3
"""Regression test: the watchdog must reap a child that ignores SIGTERM.

JPype's JVM installs its own signal handlers and can swallow the watchdog's
terminate(); before the kill-escalation fix, _execute_watchdog then blocked
forever in a bare join() — this wedged the 2026-07-14 fault-TE run at job 2
(41 h stuck, 0/63 jobs done) and the earlier Phase-4 CPU shard.

Run before relaunching any watchdog'd campaign (alongside test_ar1_te.py):

    python analysis/test_watchdog_kill.py

Exit 0 = PASS. On Windows terminate() is TerminateProcess and cannot be
ignored, so the test passes without exercising the escalation; the SIGTERM
path only reproduces on POSIX (i.e. the servers, where it matters).
"""
from __future__ import annotations

import multiprocessing as mp
import signal
import sys
import time


def _stubborn(started) -> None:
    """Child that shrugs off SIGTERM, like a JVM mid-KSG-estimate."""
    if sys.platform != "win32":
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    started.set()
    time.sleep(600)


def main() -> int:
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from te_pipeline import _kill_stubborn_child

    grace_s = 3.0
    ctx = mp.get_context("spawn")
    started = ctx.Event()
    p = ctx.Process(target=_stubborn, args=(started,))
    p.start()
    if not started.wait(60):
        print("FAIL: child never signalled startup")
        p.kill()
        return 1

    t0 = time.time()
    _kill_stubborn_child(p, grace_s=grace_s)
    dt = time.time() - t0

    if p.is_alive():
        print(f"FAIL: SIGTERM-immune child still alive {dt:.1f}s after reap")
        p.kill()
        return 1
    if dt > grace_s + 10.0:
        print(f"FAIL: reap took {dt:.1f}s (grace {grace_s}s) — escalation too slow")
        return 1
    print(f"PASS: SIGTERM-immune child reaped in {dt:.1f}s (grace {grace_s}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
