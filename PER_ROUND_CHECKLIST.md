# Per-round checklist — push code, run, pull results

Use this every time Claude makes changes that need to run on the 65-core
server. **First-time** server setup is a separate doc:
[SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md).

---

## TL;DR cheat sheet

| Step | Where     | Command / Action                                           |
|:----:|-----------|------------------------------------------------------------|
|  1   | Windows   | (Claude commits locally — nothing for you to do)           |
|  2   | Windows   | GitHub Desktop → **Push origin**                           |
|  3   | Server    | `cd ~/fowt-te-causal && git pull`                          |
|  4   | Server    | `python pipeline.py all --raft-workers 60 --openfast-workers 32 --te-workers 40 --N 256` |
|  5   | Server    | (wait ~4 h, then exit SSH)                                 |
|  6   | Windows   | `./pull-results.sh user@server:/home/user/fowt-te-causal`  |
|  7   | Windows   | Tell Claude "the run finished, check the logs"             |

---

## 1. Windows — push Claude's changes

Claude has already committed locally. You just push:

1. Open **GitHub Desktop**.
2. Top-left should show **"X commits to push to origin"**.
3. Click **Push origin** (top-right).

That's it for the Windows side, for now.

---

## 2. Server — pull, run, leave

SSH to the server:

```bash
ssh user@server.example.com
```

Then three commands:

```bash
cd ~/fowt-te-causal
git pull                                   # fetch Claude's new code
python pipeline.py all \
    --raft-workers 60 \
    --openfast-workers 32 \
    --te-workers 40 \
    --N 256
```

### Disconnect-safe long runs

The full pipeline takes ~4 h. If you close the SSH session, the run dies.
Two ways to detach:

**Option A — tmux** (recommended):
```bash
tmux new -s fowt        # creates session "fowt"
# ...run the python pipeline.py command above...
# To detach: press Ctrl-b, then d
# Reconnect later: tmux attach -t fowt
```

**Option B — nohup**:
```bash
nohup python pipeline.py all \
    --raft-workers 60 --openfast-workers 32 --te-workers 40 --N 256 \
    > pipeline.out 2>&1 &
disown                  # so it survives logout
# Check progress: tail -f pipeline.out
```

### Just one phase, not the whole pipeline

```bash
python pipeline.py phase5 --raft-workers 60 --N 256       # ~3 min  (Sobol)
python pipeline.py phase2 --dlc dlca --openfast-workers 24 # ~80 min (DLC-A)
python pipeline.py phase2 --dlc dlcb --openfast-workers 24 # ~80 min (DLC-B)
python pipeline.py phase4 --te-workers 40                  # ~30 min (TE)
python pipeline.py graph                                    # ~30 s  (causal graph)
```

The orchestrator is idempotent — re-running skips work that's already done.

---

## 3. Windows — pull results back

When the server-side run is finished:

1. Right-click the vault folder (`D:\Causal Effect with transfer entropy\wiki-transfer entropy\`)
   in File Explorer → **Open Git Bash here**.
   *(Git Bash ships with GitHub Desktop and bundles `rsync`.)*
2. Run the pull script. **First time**, edit `REMOTE_DEFAULT` in the
   script to your actual server path, then just:
   ```bash
   ./pull-results.sh
   ```
   Or pass the path as an argument every time:
   ```bash
   ./pull-results.sh user@server.example.com:/home/user/fowt-te-causal
   ```

What it pulls:
- `sims/<case>/...` — OpenFAST `.outb`, `.sum`, `.log`
- `data/*.parquet`, `data/*.json` — Phase 4/5 derived data
- `analysis/*.log` — pipeline runtime stdout/stderr
- `reports/...` — Phase 6 figures and write-ups

What it skips:
- `repos/` (vendored — lives on both machines independently)
- `pages/`, `*.md` (source flows the *other* way via Git, never via rsync)
- `.git/` (Git handles its own state)

---

## 4. Windows — tell Claude

Open Claude Code in this vault and say something like:

> *"The server run finished. Read `analysis/*.log` and the new `data/*.parquet`,
> then write a narrative entry in `pages/log.md` summarizing what happened and
> what's next."*

Claude will read the logs and parquet outputs, append a dated entry to
`pages/log.md`, draft any figures or follow-up scripts, and propose the next
iteration. You then push that update back to GitHub for the next round.

---

## Troubleshooting

### `Permission denied (publickey)` when SSHing

You haven't set up SSH keys to the server yet. Easiest:
```bash
ssh-keygen -t ed25519                       # on Windows, in Git Bash, accept defaults
ssh-copy-id user@server.example.com         # one-time, asks for server password
```
After that, future SSH and rsync calls don't ask for a password.

### `./pull-results.sh: Permission denied`

```bash
chmod +x pull-results.sh
```

### `rsync: command not found` in Git Bash

Unusual — Git Bash bundles rsync. If yours doesn't, install it via:
```bash
# Git Bash
pacman -S rsync                             # if pacman is available
# Or use WSL:
wsl rsync -av ...                           # prefix any rsync call with `wsl`
```

### `git pull` says "Your local changes would be overwritten"

You edited files on the server. **Don't.** The server is read-only for code.
To recover:
```bash
git stash                  # set aside the local edits
git pull                   # now succeeds
git stash drop             # discard the stashed edits (the canonical version
                           # is what we just pulled)
```
If you actually meant to make a code change, do it on Windows so it goes
through GitHub.

### Pipeline crashed mid-run

`pipeline.py all` is idempotent — re-running it skips finished work and
picks up where it left off. Just re-run the same command after fixing the
cause. For deeper issues see [SERVER_DEPLOYMENT.md §8 Troubleshooting](SERVER_DEPLOYMENT.md#8-troubleshooting).
