"""RR10 reproducibility check: regenerate manuscript Tables 1-3 from the deposited
first-pass te_table.parquet and compare against the values printed in
te-firewall-paper-final.md.

Convention (paper §3.4): per-edge mean TE is *gated* — non-significant cases
contribute 0. Max is the raw te_nats maximum; significance fraction is over all
54 cases. Run from the repository root:  python reports/_verify_tables_rr10.py

Tables 4 (coherence) and 5 (delay-resolved) derive from other artefacts and are
verified elsewhere; this script covers the te_table-derived tables only.
"""
import re
import numpy as np
import pandas as pd

df = pd.read_parquet('reports/te_table.parquet')
te = df[df.method == 'bivariate_te_ksg'].copy()
te['gated'] = np.where(te.significant, te.te_nats, 0.0)

W, V = 'Wind1VelX', 'Wave1Elev'


def row(src, tgt):
    sub = te[(te.source == src) & (te.target == tgt)]
    return dict(n=len(sub), mean=sub.gated.mean(), max=sub.te_nats.max(),
                sig=100 * sub.significant.mean())


def chk(computed, paper, tol):
    return abs(computed - paper) <= tol


fails = 0


def report(cond, label):
    global fails
    if not cond:
        fails += 1
    print(("OK " if cond else "XX ") + label)


# --- Table 1: drivers -> platform pitch/surge ---
paper1 = {('Wind1VelX', 'PtfmPitch'): (0.0009, 0.0293, 3.7),
          ('Wave1Elev', 'PtfmPitch'): (0.1214, 0.2658, 100.0),
          ('Wind1VelX', 'PtfmSurge'): (0.0013, 0.0239, 11.1),
          ('Wave1Elev', 'PtfmSurge'): (0.1069, 0.2796, 92.6)}
print("=== Table 1 ===")
for (s, t), (pm, px, ps) in paper1.items():
    a = row(s, t)
    report(chk(a['mean'], pm, 5e-4) and chk(a['max'], px, 2e-3) and chk(a['sig'], ps, 0.5),
           f"{s[:4]}->{t}: mean {a['mean']:.4f}|{pm:.4f} max {a['max']:.4f}|{px:.4f} sig {a['sig']:.1f}|{ps:.1f}")

# --- Table 2: nine structural targets ---
paper2 = {'PtfmSurge': (0.0013, 11.1, 0.1069, 92.6), 'PtfmHeave': (0.0001, 5.6, 0.1139, 87.0),
          'PtfmPitch': (0.0009, 3.7, 0.1214, 100.0), 'FAIRTEN1': (0.0024, 9.3, 0.0195, 53.7),
          'FAIRTEN2': (0.0012, 5.6, 0.1113, 100.0), 'FAIRTEN3': (0.0018, 9.3, 0.1101, 100.0),
          'RootMxc1': (0.0019, 38.9, 0.0008, 18.5), 'RootMyc1': (0.0029, 16.7, 0.0042, 18.5),
          'TwrBsMyt': (0.0058, 27.8, 0.0230, 61.1)}
print("=== Table 2 ===")
for tgt, (wm, ws, vm, vs) in paper2.items():
    aw, av = row(W, tgt), row(V, tgt)
    report(chk(aw['mean'], wm, 5e-4) and chk(aw['sig'], ws, 0.5)
           and chk(av['mean'], vm, 5e-4) and chk(av['sig'], vs, 0.5),
           f"{tgt}: wind {aw['mean']:.4f}|{wm:.4f}/{aw['sig']:.1f}|{ws:.1f} "
           f"wave {av['mean']:.4f}|{vm:.4f}/{av['sig']:.1f}|{vs:.1f}")

# --- Table 3: wind -> platform pitch by wind speed ---
def wspeed(c):
    m = re.search(r'v(\d+)ms', c)
    return int(m.group(1)) if m else None
wp = te[(te.source == W) & (te.target == 'PtfmPitch')].copy()
wp['ws'] = wp.case.map(wspeed)
paper3 = {8: (12, 0.0000, 0.0000, 0.0), 11: (18, 0.0016, 0.0293, 5.6),
          15: (12, 0.0018, 0.0218, 8.3), 20: (12, 0.0000, 0.0000, 0.0)}
print("=== Table 3 ===")
for ws, (pn, pm, px, ps) in paper3.items():
    sub = wp[wp.ws == ws]
    cn, cm, cx, cs = len(sub), sub.gated.mean(), sub.te_nats.max(), 100 * sub.significant.mean()
    report(cn == pn and chk(cm, pm, 5e-4) and chk(cx, px, 2e-3) and chk(cs, ps, 0.5),
           f"{ws} m/s n={cn}|{pn} mean {cm:.4f}|{pm:.4f} max {cx:.4f}|{px:.4f} sig {cs:.1f}|{ps:.1f}")

print(f"\n{'ALL TABLES REPRODUCE' if fails == 0 else str(fails) + ' MISMATCH(ES)'}")
raise SystemExit(1 if fails else 0)
