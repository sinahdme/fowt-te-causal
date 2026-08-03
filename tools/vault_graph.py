#!/usr/bin/env python3
"""
vault_graph.py — Extract and analyze the link graph of an Obsidian vault.

Usage examples:
    python vault_graph.py /path/to/vault --stats
    python vault_graph.py /path/to/vault --backlinks "transfer-entropy-basics"
    python vault_graph.py /path/to/vault --path "sensor-data" "digital-twin"
    python vault_graph.py /path/to/vault --neighbors "MOC-mini-twin" --depth 2
    python vault_graph.py /path/to/vault --export graph.json

Requires: networkx  (pip install networkx)
"""

import argparse
import json
import re
import sys
from pathlib import Path

import networkx as nx

# Matches [[note]], [[note|alias]], [[note#heading]], ![[embedded note]]
WIKILINK_RE = re.compile(r"!?\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]")

# Folders inside the vault to ignore
IGNORE_DIRS = {".obsidian", ".git", ".trash", "node_modules", "venv", ".venv", "__pycache__"}


def build_graph(vault: Path) -> nx.DiGraph:
    """Scan all .md files and build a directed graph of wiki-links."""
    G = nx.DiGraph()

    md_files = [
        p for p in vault.rglob("*.md")
        if not any(part in IGNORE_DIRS for part in p.parts)
    ]

    # Map note name (stem) -> path, for resolving links
    name_to_path = {p.stem: p for p in md_files}

    for p in md_files:
        source = p.stem
        G.add_node(source, path=str(p.relative_to(vault)))
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for match in WIKILINK_RE.finditer(text):
            target = match.group(1).strip()
            # Links may include a path like "folder/note" — keep only the name
            target = Path(target).stem
            if target and target != source:
                resolved = target in name_to_path
                G.add_node(target, resolved=resolved)
                # Count multiple links between the same pair as edge weight
                if G.has_edge(source, target):
                    G[source][target]["weight"] += 1
                else:
                    G.add_edge(source, target, weight=1)

    return G


def show_stats(G: nx.DiGraph, top: int = 10) -> None:
    """Print overall graph statistics."""
    print(f"Notes (nodes):        {G.number_of_nodes()}")
    print(f"Links (edges):        {G.number_of_edges()}")

    unresolved = [n for n, d in G.nodes(data=True) if d.get("resolved") is False]
    print(f"Unresolved links:     {len(unresolved)}  (linked but file doesn't exist)")

    orphans = [n for n in G.nodes if G.degree(n) == 0]
    print(f"Orphan notes:         {len(orphans)}  (no links in or out)")

    print(f"\nTop {top} most referenced notes (by backlinks):")
    by_indegree = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)[:top]
    for name, deg in by_indegree:
        print(f"  {deg:4d} <- {name}")

    print(f"\nTop {top} hub notes (most outgoing links):")
    by_outdegree = sorted(G.out_degree(), key=lambda x: x[1], reverse=True)[:top]
    for name, deg in by_outdegree:
        print(f"  {deg:4d} -> {name}")

    if orphans:
        print("\nOrphan notes:")
        for n in sorted(orphans)[:20]:
            print(f"  - {n}")
        if len(orphans) > 20:
            print(f"  ... and {len(orphans) - 20} more")


def show_backlinks(G: nx.DiGraph, note: str) -> None:
    """Show which notes link TO the given note (the reverse direction)."""
    if note not in G:
        sys.exit(f"Note not found in graph: {note}")
    backlinks = sorted(G.predecessors(note))
    outlinks = sorted(G.successors(note))
    print(f"'{note}'")
    print(f"\nBacklinks ({len(backlinks)} notes link here):")
    for b in backlinks:
        print(f"  <- {b}")
    print(f"\nOutgoing links ({len(outlinks)}):")
    for o in outlinks:
        print(f"  -> {o}")


def show_path(G: nx.DiGraph, a: str, b: str) -> None:
    """Shortest chain of links connecting two notes (ignoring direction)."""
    for n in (a, b):
        if n not in G:
            sys.exit(f"Note not found in graph: {n}")
    U = G.to_undirected()
    try:
        path = nx.shortest_path(U, a, b)
        print(" -> ".join(path))
    except nx.NetworkXNoPath:
        print(f"No connection between '{a}' and '{b}'.")


def show_neighbors(G: nx.DiGraph, note: str, depth: int) -> None:
    """All notes reachable within N link-steps (both directions) — a 'context set'."""
    if note not in G:
        sys.exit(f"Note not found in graph: {note}")
    U = G.to_undirected()
    layers = {0: {note}}
    seen = {note}
    for d in range(1, depth + 1):
        frontier = set()
        for n in layers[d - 1]:
            frontier |= set(U.neighbors(n)) - seen
        layers[d] = frontier
        seen |= frontier
    for d in range(depth + 1):
        if layers[d]:
            print(f"\nDepth {d} ({len(layers[d])} notes):")
            for n in sorted(layers[d]):
                path = G.nodes[n].get("path", "(unresolved)")
                print(f"  {n}  [{path}]")


def export_json(G: nx.DiGraph, out: Path) -> None:
    """Export the graph as JSON — machine-readable, e.g. for Claude Code."""
    data = {
        "nodes": [
            {"id": n, **{k: v for k, v in d.items()}}
            for n, d in G.nodes(data=True)
        ],
        "edges": [
            {"source": u, "target": v, "weight": d["weight"]}
            for u, v, d in G.edges(data=True)
        ],
    }
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {G.number_of_nodes()} nodes / {G.number_of_edges()} edges -> {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze an Obsidian vault's link graph.")
    ap.add_argument("vault", type=Path, help="Path to the vault folder")
    ap.add_argument("--stats", action="store_true", help="Show graph statistics")
    ap.add_argument("--backlinks", metavar="NOTE", help="Show backlinks/outlinks of a note")
    ap.add_argument("--path", nargs=2, metavar=("A", "B"), help="Shortest link path between two notes")
    ap.add_argument("--neighbors", metavar="NOTE", help="Notes within --depth steps of NOTE")
    ap.add_argument("--depth", type=int, default=1, help="Depth for --neighbors (default 1)")
    ap.add_argument("--export", type=Path, metavar="FILE", help="Export graph as JSON")
    args = ap.parse_args()

    if not args.vault.is_dir():
        sys.exit(f"Not a directory: {args.vault}")

    G = build_graph(args.vault)

    if args.stats:
        show_stats(G)
    if args.backlinks:
        show_backlinks(G, args.backlinks)
    if args.path:
        show_path(G, args.path[0], args.path[1])
    if args.neighbors:
        show_neighbors(G, args.neighbors, args.depth)
    if args.export:
        export_json(G, args.export)

    if not any([args.stats, args.backlinks, args.path, args.neighbors, args.export]):
        show_stats(G)


if __name__ == "__main__":
    main()
