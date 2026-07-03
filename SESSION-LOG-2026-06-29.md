# Session log — 2026-06-29

**Purpose:** durable record of this working session (Q&A + decisions + commands)
so it survives a PC restart / context loss. If you're resuming: read **§1 TL;DR**
and **§6 Commands**, then continue from **§7 Next steps**.

Branch: `phase4-full-rerun`. Repo (lams): `~/Desktop/sina/fowt_te_causal/fowt-te-causal`.

---

## 1. TL;DR — where we are right now

- The full-settings TE probe (1 case, `max_lag=150`, 5 Hz, `n_perm=200`, GPU) ran
  in **9.1 h** and exposed a **result-invalidating bug**: at `max_lag=150` the
  KSG transfer entropy **nulls a real coupling** — `TE(Wave→PtfmHeave)=0` — while
  Granger still sees it strongly (0.35). This would have wrecked the H2/H6 story.
- A focused diagnostic proved it's a **greedy-selection artifact** (option *a*),
  not a real absence: `TE(Wave→Heave)` KSG = **0.066 at `max_lag=30`** but
  collapses to **0 at `max_lag≥60`** (`n_src` 1→0).
- **Fix applied & pushed:** decoupled `max_lag_sources` (short, sensitive source
  search) from the target embedding `max_lag` (long, for slow-drift dynamics).
- **Currently waiting on:** a re-validation run on lams to confirm the fix
  recovers `Wave→Heave` with `max_lag_sources≈30, max_lag_target=150`. Once that
  passes, we wire `--max-lag-sources 30` into the launcher and start the 54-case
  campaign.

---

## 2. Commits made this session (branch `phase4-full-rerun`, all pushed to origin)

| hash | summary |
|---|---|
| `c43d59b` | run_phase4_full: fix case_id collision + add `--slow-drift-tau 5` |
| `398025e` | diag: max_lag sweep script to explain the KSG wave-coupling nulls |
| `986f867` | te_pipeline: decouple `max_lag_sources` from target embedding |

(Earlier baseline this session started from: `4984844`.)

---

## 3. What we did, in order (your questions → outcomes)

1. **"review whole the project"** (+ you launched a cloud ultrareview).
   Whole-project review found, beyond the diff: the committed `te_table.parquet`
   is the **stale first-pass** (bivariate + coherence only, old 2 Hz / max_lag=60
   settings — no conditional/Granger); a `te_frac` docstring mismatch
   (`build_graph` says `TE/(H−AIS)` but code computes `TE/AIS`); coherence rows
   are 100% "significant" (threshold artifact); **512 MB of `.outb` at repo root
   are NOT gitignored** (risk of an accidental >100 MB commit); repo sprawl.
2. **Read the SURD paper** (Martínez-Sánchez, Arranz & Lozano-Durán, *Nat.
   Commun.* 15, 9296, 2024). It decomposes causality into **Redundant / Unique /
   Synergistic + a causality leak** (unobserved drivers). Recommendation:
   **augment, not replace** TE — use SURD on scoped groups to (a) measure the
   controller "firewall" via the leak, (b) make H3/H5b rigorous. → SURD subproject.
3. **Cloud ultrareview** returned 2 findings; I verified both against the code:
   - *bug_001 (case_id collision):* `run_phase4_full.sh` fed 54 identically-named
     `.outb` files → stem-based `case_id` collapsed all cases to ~2 after
     `merge_parquet_parts.py drop_duplicates`. **Fixed** via folder-named symlink
     staging (like `run_campaign.sh`).
   - *bug_002 (missing `--slow-drift-tau`):* Granger uses the Gaussian estimator
     which "goes singular (TE=nan)" on the 4 slow-drift channels at tau=1.
     **Fixed** by adding `--slow-drift-tau 5` to `COMMON_ARGS`.
   → commit `c43d59b`.
4. **SURD subproject brainstormed & planned** → `surd/PLAN.md` (see §5).
5. **You shared the 9.1 h probe output.** Findings in §4.
6. Built **`analysis/diag_maxlag_sweep.py`** (`398025e`) to isolate why KSG nulls
   the wave coupling. Ran it → confirmed the artifact (§4).
7. **Applied the asymmetric-lag fix** (`986f867`) and prepared the re-validation.

---

## 4. Key findings (the science — load-bearing)

### 4a. The 9.1 h full-settings probe (1 case: dlca_v11ms_s00)
- **Bug-2 fix verified on hardware:** all 4 slow-drift channels returned real,
  non-NaN Granger + AIS (`AIS(PtfmPitch)=3.99`, `AIS(PtfmHeave)=2.59`, etc.).
- **H1 (Wind→Pitch) confirmed null AND robust to conditioning:** bivariate KSG
  `Wind→PtfmPitch=0`; conditional-on-wave `=0`. Conditioning on wave did **not**
  rescue it → strengthens the controller-firewall / SURD-leak motivation.
- **Conditional TE removed a spurious edge:** `Wind→FAIRTEN2` bivariate
  `=0.042 (sig)` but conditional-on-wave `=0`. (Resolves the "Wind→FAIRTEN2 0.042
  gotcha".)
- **🚩 The red flag:** at `max_lag=150`, KSG nulled `Wave→PtfmHeave` (=0) and most
  wave/wind edges, while Granger still found them. That contradicts the first-pass
  H2/H6 (wave coupling 100% significant). Gated the campaign on a diagnostic.

### 4b. The diagnostic (`diag_maxlag_sweep`, symmetric sweep, tau=5)
| target | max_lag | KSG TE | KSG n_src | Granger TE |
|---|---|---|---|---|
| PtfmHeave | **30** | **0.0662 ✓** | **1** | 0.215 |
| PtfmHeave | 60 | 0.0000 ✗ | 0 | 0.289 |
| PtfmHeave | 100 | 0.0000 ✗ | 0 | 0.327 |
| PtfmHeave | 150 | 0.0000 ✗ | 0 | 0.350 |
| PtfmPitch | 30→150 | 0.0071→0.0066 (stable ✓) | 1→1 | 0.05→0.12 |

**Verdict = (a) greedy-selection artifact for heave.** IDTxl's source-inclusion
max-statistic tightens as the candidate pool grows; with ≥12 source candidates it
rejects the genuine moderate `Wave→Heave` coupling that a ~6-candidate search
(`max_lag=30`, tau=5) recovers. Pitch is *not* an artifact — its KSG value is just
genuinely small (~0.0066) and stable. **H2 stands**; `max_lag=150` was suppressing
it.

### 4c. The fix (`986f867`)
Separate the two windows IDTxl already supports:
- `max_lag` (= `max_lag_target`) stays **150** → long target embedding for
  slow-drift self-dynamics (and AIS).
- `max_lag_sources` set **~30** → short, sensitive, *cheap* source search.
`max_lag_sources=0` ties to `max_lag` (old symmetric behaviour, backward-compatible).
Bonus: far fewer source candidates ⇒ the 9 h/case should drop substantially.

---

## 5. SURD subproject (planned, not yet started)

Plan committed at **`surd/PLAN.md`** (untracked as of this session — see §8). Gist:
a `surd/` track reusing the same `.outb` data/preprocessing; **observe the
controller firewall** by adding `RotThrust`, `BldPitch1` to the variable set and
measuring the **leak drop** on `PtfmPitch`. Phase 0 = validate on the paper's
synthetic mediator case; Phase 1 = thin slice `{Wind, Wave, BldPitch1, RotThrust,
PtfmPitch}` on one case; Phase 2 = scale. All controller/drivetrain channels
confirmed present in the `.outb`. Honest caveat: near-perfect cancellation means
SURD *relocates* wind's causality into the controller channels, it doesn't conjure
a hidden wind→pitch effect.

---

## 6. Commands — copy/paste on lams

```bash
# 0. get the latest code (must end up at 986f867)
cd ~/Desktop/sina/fowt_te_causal/fowt-te-causal
git pull origin phase4-full-rerun
git log --oneline -1            # confirm: 986f867

# 1. RE-VALIDATION (current step): fix target=150, sweep source window 20/30/45.
#    Success = Wave->PtfmHeave KSG comes back nonzero+significant (n_src>=1).
python analysis/diag_maxlag_sweep.py \
  sims/dlca_v11ms_s00/IEA-15-240-RWT-UMaineSemi/IEA-15-240-RWT-UMaineSemi.outb \
  --gpu --gpuid 0 --tau 5 --max-lag-target 150 --max-lags 20,30,45 --n-perm 200 \
  -o reports/diag_revalidate.parquet
# ~30-40 min; checkpoints + prints each row as it lands.

# 2. (AFTER re-validation passes — NOT yet) launch the 54-case campaign.
#    I will first wire --max-lag-sources 30 into run_phase4_full.sh and push.
#    Then:
#    ./analysis/run_phase4_full.sh 36
#    python analysis/merge_parquet_parts.py --prefix te_table_full_p --out te_table_full.parquet
```

Note: a local edit to `analysis/run_phase4_parallel.sh` exists on lams; it's
unrelated and won't block the fast-forward pull.

---

## 7. Next steps / decisions pending

1. **Run the re-validation** (§6 step 1) and paste the table back.
2. From it, **pick `max_lag_sources`** (expected ~30, since symmetric 30 gave
   0.066). Confirm slow-drift channels still complete.
3. I **wire `--max-lag-sources` into `run_phase4_full.sh`**, push.
4. **Launch the 54-case campaign** (faster than 9 h/case now).
5. Then resume the **SURD subproject** (Phase 0 validation) — independent, can run
   in parallel; needs network to clone `github.com/Computational-Turbulence-Group/SURD`.

---

## 8. Outstanding hygiene (not urgent, not done)

- **gitignore the root `.outb`** (`/*.outb`, `raw/*.mp4`, `reports/node_modules/`)
  — 512 MB at repo root currently un-ignored; one `git add -A` risks a >100 MB push.
- **`surd/PLAN.md`** is untracked — commit when convenient.
- **`te_frac` docstring vs code** mismatch (`build_graph`); coherence 100%-sig
  threshold artifact — reconcile before the report quotes them.
- The committed `te_table.parquet` is the **stale first-pass** — the campaign in
  step 4 produces the real `te_table_full.parquet`; don't confuse them.
