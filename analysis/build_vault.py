"""
build_vault.py — convert OpenFAST RST docs to Markdown for the wiki.

Walks repos/openfast/docs/source/**/*.rst and writes one Markdown file
per RST into wiki-transfer entropy/raw/extracts/openfast-docs/, preserving
relative directory structure.

Per PLAN.md Phase 1: this script is one-shot, idempotent. Existing entity
pages in wiki/pages/entities/openfast-*.md are NOT touched.

Requires: pandoc on PATH (verified: pandoc 3.8).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "repos" / "openfast" / "docs" / "source"
DST = PROJECT_ROOT / "wiki-transfer entropy" / "raw" / "extracts" / "openfast-docs"


def convert_one(rst_path: Path) -> tuple[Path, int, str]:
    """Run pandoc on a single RST file. Returns (path, returncode, stderr)."""
    rel = rst_path.relative_to(SRC)
    md_path = DST / rel.with_suffix(".md")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            "pandoc",
            "-f", "rst",
            "-t", "gfm",
            "--wrap=none",
            "-o", str(md_path),
            str(rst_path),
        ],
        capture_output=True,
        text=True,
    )
    return rst_path, result.returncode, result.stderr


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=8, help="Parallel pandoc workers")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of files (debug)")
    args = parser.parse_args()

    if not SRC.exists():
        print(f"ERROR: source dir not found: {SRC}", file=sys.stderr)
        return 2

    rst_files = sorted(SRC.rglob("*.rst"))
    if args.limit:
        rst_files = rst_files[: args.limit]

    print(f"Converting {len(rst_files)} RST files → {DST}")
    DST.mkdir(parents=True, exist_ok=True)

    failed: list[tuple[Path, str]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(convert_one, p): p for p in rst_files}
        for i, fut in enumerate(as_completed(futures), 1):
            path, rc, stderr = fut.result()
            if rc != 0:
                failed.append((path, stderr.strip() or "non-zero exit"))
            if i % 25 == 0 or i == len(rst_files):
                print(f"  [{i}/{len(rst_files)}] last: {path.name}")

    if failed:
        print(f"\n{len(failed)} failures:", file=sys.stderr)
        for path, err in failed[:10]:
            print(f"  {path}: {err}", file=sys.stderr)
        return 1
    print(f"\nAll {len(rst_files)} files converted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
