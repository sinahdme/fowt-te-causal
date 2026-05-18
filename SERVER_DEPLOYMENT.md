# Server deployment guide — FOWT causal-TE project

Step-by-step instructions to deploy this project on a new server (e.g. the
65-core Linux machine). Written for a user new to git / conda.

Two sync paths supported:
- **Git via GitHub Desktop** (recommended for ongoing development)
- **One-time rsync / scp / zip-copy** (acceptable for a single deployment)

---

## 0. What you'll have at the end

- The full project at `/path/on/server/wiki-transfer entropy/`
- A conda env `fowt-te` activated, with OpenFAST + Python + JVM all working
- One command (`python pipeline.py smoke`) that verifies the install end-to-end in ~5 min
- One command (`python pipeline.py all --raft-workers 60 --openfast-workers 32 --te-workers 40`) that runs the whole production pipeline

Total setup time: **~30 min** (first time) including conda solve.

---

## 1. Sync the code to the server

### Option A — Git via GitHub Desktop (recommended)

On **this Windows machine**:

1. **Create a GitHub account** at https://github.com if you don't have one. Free.
2. **Create a private repo** via the web UI:
    - Click "+" top-right → "New repository"
    - Name: e.g. `fowt-te-causal` (any name)
    - Visibility: **Private** ← important
    - Do NOT initialize with README/.gitignore (we already have files locally)
    - Click "Create repository"
    - Note the URL: `https://github.com/<your-user>/fowt-te-causal`
3. **Install GitHub Desktop** from https://desktop.github.com — free, signed in with your GitHub account.
4. In GitHub Desktop: **File → Add Local Repository** → point at `D:\Causal Effect with transfer entropy\wiki-transfer entropy\` → "Add Repository".
   - It will say "this isn't a git repo yet — initialize?" → click "create a repository here".
5. Click **"Publish repository"** at the top-right → pick the GitHub remote you created → uncheck "Keep this code private" if you want it public, leave it checked for private → "Publish".

Your local code is now mirrored to GitHub. Every future change Claude makes here gets committed locally; you click **"Push origin"** in GitHub Desktop to upload, and `git pull` on the server downloads it.

On the **server**:

```bash
# Install git if missing
sudo apt-get install -y git           # Ubuntu/Debian
sudo dnf install -y git               # Fedora/RHEL

# Clone the repo (use the URL from step 2 above)
cd ~
git clone https://github.com/<your-user>/fowt-te-causal.git

# When prompted, paste a Personal Access Token (PAT). To create one:
#   GitHub web UI → Settings → Developer settings → Personal access tokens
#   → "Generate new token (classic)" → tick "repo" scope → copy the token
# (You only need to paste it once if you have credential helper enabled.)
```

You now have the project at `~/fowt-te-causal/`.

For future updates from this machine: I commit → you click Push in GitHub Desktop → on server `git pull`. That's the whole loop.

### Option B — One-time copy (simpler, no version history)

```bash
# On Windows: zip the vault root
# (right-click "wiki-transfer entropy" folder → Send to → Compressed (zipped) folder)
# Then scp the zip to the server:
scp "wiki-transfer entropy.zip" user@server:/path/

# On the server:
cd /path/
unzip "wiki-transfer entropy.zip"
mv "wiki-transfer entropy" fowt-te-causal
```

When Claude makes future changes, you re-zip → re-scp → unzip-overwrite. No diff visibility, but works.

---

## 2. Install conda + create the env

If conda/miniconda isn't already on the server:

```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
source $HOME/miniconda3/etc/profile.d/conda.sh
echo 'source $HOME/miniconda3/etc/profile.d/conda.sh' >> ~/.bashrc
```

Create the env from the provided file:

```bash
cd /path/to/fowt-te-causal
conda env create -f environment.yml
conda activate fowt-te
```

Conda solve takes 5–15 min. The env footprint is ~3 GB (OpenFAST binaries +
JDK + scientific Python stack).

---

## 3. Post-conda steps

Two pieces don't fit in `environment.yml` because they're path-pinned to the
cloned repos.

### 3a. Editable installs from `repos/`

```bash
cd /path/to/fowt-te-causal

# OpenFAST output-file parser (we use the local clone so the NumPy 2.x patch
# at line 617 of fast_output_file.py is in effect)
pip install -e repos/openfast_toolbox

# WEIS — pulls in RAFT + MoorPy + WISDEM as transitive editable deps
# (Top-level `import weis` is known to fail because pyOpenFAST isn't built —
# we only need `import raft` which works standalone.)
pip install -e repos/WEIS
```

### 3b. IDTxl `.pth` bypass

Upstream `pip install idtxl` requires a C compiler for an HDE Cython extension
we don't use. We register IDTxl via a `.pth` file pointing at the local clone:

```bash
# Find your env site-packages dir
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")
echo $SITE_PACKAGES

# Write the .pth file
echo "/path/to/fowt-te-causal/repos/IDTxl/IDTxl-master" > $SITE_PACKAGES/idtxl.pth
```

### 3c. Verify imports

```bash
python -c "
import importlib
for pkg in ('openfast_toolbox', 'idtxl', 'raft', 'salib', 'jpype'):
    try:
        m = importlib.import_module(pkg)
        print(f'{pkg:20s} OK  ({getattr(m, \"__file__\", \"<namespace>\")})')
    except ImportError as e:
        print(f'{pkg:20s} FAIL  {e}')
"
```

All five should print `OK`.

---

## 4. Configure env vars (Linux-specific paths)

The project's drivers default to Windows paths. On Linux, override via env
vars. Add to `~/.bashrc` (or a project-local activation script):

```bash
# Conda env binaries (Linux conda layout)
export OPENFAST_EXE="$CONDA_PREFIX/bin/openfast"
export TURBSIM_EXE="$CONDA_PREFIX/bin/turbsim"

# ROSCO DLL — Linux name is libdiscon.so; the pip-installed rosco package
# puts it under site-packages/rosco/lib/
export ROSCO_DLL="$(python -c 'import rosco, pathlib; print(pathlib.Path(rosco.__file__).parent / "lib" / "libdiscon.so")')"

# JAVA_HOME — point at the JDK installed by conda
export JAVA_HOME="$CONDA_PREFIX/lib/jvm"   # or $CONDA_PREFIX/jre depending on openjdk pkg version
# Sanity check: $JAVA_HOME/lib/server/libjvm.so should exist
ls $JAVA_HOME/lib/server/libjvm.so

# Force UTF-8 (matters for input file parsing)
export PYTHONUTF8=1
```

Verify:
```bash
echo $OPENFAST_EXE && file $OPENFAST_EXE
echo $TURBSIM_EXE && file $TURBSIM_EXE
echo $ROSCO_DLL && file $ROSCO_DLL
echo $JAVA_HOME
```

---

## 5. Patch the IEA-15 deck for Linux

Two r-test gotchas (see `pages/project-input-gotchas` for context):

```bash
# 1. ServoDyn DLL path — the IEA-15 deck ships with a Linux CI path
#    (/home/runner/...) that doesn't match our actual ROSCO install.
#    run_campaign.py patches this per case, so no manual fix is needed.

# 2. TurbSim grid bottom — run_campaign.py sets GridHeight ≥ 280 internally.
#    No manual fix needed.
```

Both gotchas are handled automatically by `sims/run_campaign.py` per case.

---

## 6. Smoke test the pipeline

```bash
cd /path/to/fowt-te-causal

# Status check (no compute) — verifies all paths resolve and lists what's
# already done from any previously-synced state.
python pipeline.py status

# Smoke test — 5 min end-to-end. Runs a tiny version of every phase.
python pipeline.py smoke
```

The smoke runs:
- Phase 5 (RAFT): N=4 Saltelli sample (~44 evals on 4 workers, <1 min)
- Phase 2 (OpenFAST): dlc16 with TMax=120 s (~2 min per case on 6 workers)
- Phase 4 (TE): smoke mode (1 pair, n_perm=50, ~2 min per case)

Total wall time on a 65-core server: ~5 min. If it completes with exit code 0,
your install is good.

---

## 7. Run the production pipeline

Sensible defaults for a 65-core machine (leave ~5 cores for OS + you):

```bash
# Run everything that isn't done yet (idempotent — uses skip-if-done)
python pipeline.py all \
    --raft-workers 60 \
    --openfast-workers 32 \
    --te-workers 40 \
    --N 256

# Or run phases individually:
python pipeline.py phase5 --raft-workers 60 --N 256       # ~3 min (2816 evals)
python pipeline.py phase2 --dlc dlca --openfast-workers 24 # ~80 min (24 cases)
python pipeline.py phase2 --dlc dlcb --openfast-workers 24 # ~80 min
python pipeline.py phase4 --te-workers 40                  # ~30 min
python pipeline.py graph                                    # ~30 s
```

Why `--openfast-workers 32` not 60? Each OpenFAST case uses ~500 MB working
set and TurbSim is partly multi-threaded (1.5–2 cores per case). 24–32 cases
in parallel covers the 24-case-per-DLC sets without RAM pressure.

Wall-time estimate at 65 cores for everything from scratch:
| Phase | Estimate |
|---|---|
| Phase 5 (N=256) | ~3 min |
| Phase 2 dlc16 (6 cases) | ~80 min |
| Phase 2 dlca (24 cases) | ~80 min (single batch) |
| Phase 2 dlcb (24 cases) | ~80 min |
| Phase 4 (54 cases × ~18 pairs) | ~30 min |
| Phase 6 graph | ~30 s |
| **Total** | **~4 hours** |

vs ~3 days on the local 8-core box. The order-of-magnitude payoff is real.

---

## 8. Troubleshooting

### `openfast: command not found`
Conda env not activated. Run `conda activate fowt-te`.

### `JVMNotFoundException: No JVM shared library file (libjvm.so)`
`JAVA_HOME` mismatch. On Linux conda envs, the JVM is at
`$CONDA_PREFIX/lib/jvm/lib/server/libjvm.so`. Adjust the export above.

### `ImportError: No module named 'openfast_toolbox'`
Editable install didn't re-register. Re-run §3a:
`pip install -e repos/openfast_toolbox`.

### `ImportError: No module named 'idtxl'`
`.pth` file missing or wrong path. Re-run §3b.

### `Grid3DField_GetCell: G3D wind array boundaries violated`
TurbSim GridHeight too small. Should not happen if `run_campaign.py` patches
correctly — verify the `write_turbsim_input` function sets `GridHeight ≥ 280`.

### `SrvD_Init` aborts with `libdiscon.so` path missing
ROSCO DLL path wrong. Verify `$ROSCO_DLL` (or default in `run_campaign.py`)
points at a real `libdiscon.so` file.

### Phase 5 RAFT crashes with `AttributeError: 'int' object has no attribute 'lower'`
RAFT YAML coercion shim missed. See `pages/cookbook/build-saltelli-ensemble`
gotcha 1. `run_raft_lhs.py` already handles this via `coerce_to_rigid`.

### `UnicodeDecodeError: 'cp949' codec`
Korean Windows codepage (shouldn't occur on Linux). Verify `PYTHONUTF8=1`.

### Phase 2 cases mysteriously slow
Check that `repos/IEA-15-240-RWT/HydroData/` is on **local NVMe**, not NFS.
Every OpenFAST case reads the WAMIT files shared from there; NFS contention
can multiply wall time.

---

## 9. Updating from new commits

For the recurring code-push → run → results-pull cycle, see the dedicated
short doc: **[PER_ROUND_CHECKLIST.md](PER_ROUND_CHECKLIST.md)** — TL;DR
table at the top, full step-by-step below, plus troubleshooting.

**Two cases that warrant re-running first-time steps from this doc:**

- If `environment.yml` changed → on server:
  `conda env update -f environment.yml`
- If `repos/` editable contents changed → on server: re-run §3a
  (`pip install -e repos/openfast_toolbox` etc.)

If neither changed, the per-round checklist's `git pull` → `pipeline.py all`
→ `pull-results.sh` loop is all you need.

---

## 10. Reference

- Phase definitions: see [PLAN.md](PLAN.md) §"Big-picture phases"
- Visual dashboard: see [pages/project-flow.md](pages/project-flow.md)
- Methodology cookbook: see [pages/cookbook/](pages/cookbook/)
- Validation cases: see [pages/validation/](pages/validation/)
- Decisions + open items: see [pages/open-questions.md](pages/open-questions.md)
