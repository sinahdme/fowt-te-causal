#!/usr/bin/env bash
# pull-results.sh — sync server-side run outputs back to this Windows vault.
#
# How to run on Windows:
#   1. Right-click the vault folder in File Explorer → "Open Git Bash here"
#      (Git Bash ships with GitHub Desktop and bundles rsync.)
#   2. First time, edit REMOTE_DEFAULT below to your actual server path,
#      OR pass it as an argument:
#        ./pull-results.sh user@server.example.com:/home/user/fowt-te-causal
#
# What it pulls:
#   sims/<case>/...     OpenFAST outputs (.outb, .sum, .dbg, openfast.log)
#   data/*.parquet      Phase 4/5 derived data (TE results, Sobol indices)
#   data/*.json         Sobol summary JSON
#   analysis/*.log      Pipeline runtime stdout/stderr (for narrative log)
#   reports/            Phase 6 figures and write-ups
#
# What it skips:
#   repos/              (vendored, lives on both machines independently)
#   pages/, *.md        (source-of-truth on Windows; flows the other way via Git)
#   .git/               (Git handles its own state)

set -euo pipefail

REMOTE_DEFAULT="USER@SERVER:/path/to/fowt-te-causal"
REMOTE="${1:-$REMOTE_DEFAULT}"

if [[ "$REMOTE" == "$REMOTE_DEFAULT" ]]; then
    echo "ERROR: REMOTE not set." >&2
    echo "Either edit REMOTE_DEFAULT in this script or pass it as arg 1." >&2
    echo "  e.g. ./pull-results.sh user@server.example.com:/home/user/fowt-te-causal" >&2
    exit 1
fi

LOCAL_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Pulling from : $REMOTE"
echo "Into         : $LOCAL_ROOT"
echo ""

# ---- sims/ ------------------------------------------------------------------
# Pull only the outputs (not the regeneratable .dat/.fst input decks, which
# run_campaign.py rebuilds per case from templates).
echo "── sims/ (OpenFAST outputs) ──"
rsync -av --progress \
    --include='*/' \
    --include='*.outb' \
    --include='*.sum' \
    --include='*.dbg' \
    --include='*.MD.out' \
    --include='openfast.log' \
    --include='turbsim.log' \
    --exclude='*' \
    "$REMOTE/sims/" "$LOCAL_ROOT/sims/"

# ---- data/ ------------------------------------------------------------------
echo ""
echo "── data/ (derived Parquet + JSON) ──"
rsync -av --progress \
    --include='*.parquet' --include='*.json' \
    --exclude='*' \
    "$REMOTE/data/" "$LOCAL_ROOT/data/"

# ---- analysis/ logs ---------------------------------------------------------
echo ""
echo "── analysis/ runtime logs ──"
rsync -av --progress \
    --include='*.log' \
    --exclude='*' \
    "$REMOTE/analysis/" "$LOCAL_ROOT/analysis/"

# ---- reports/ ---------------------------------------------------------------
echo ""
echo "── reports/ (figures, write-ups) ──"
rsync -av --progress "$REMOTE/reports/" "$LOCAL_ROOT/reports/" 2>/dev/null || \
    echo "  (reports/ not present on server yet — skipping)"

echo ""
echo "✓ Pull complete."
echo "Next: review outputs locally, then ask Claude to append a narrative"
echo "      entry to pages/log.md."
