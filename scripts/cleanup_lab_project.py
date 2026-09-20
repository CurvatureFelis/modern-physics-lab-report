#!/usr/bin/env python3
"""Scan and optionally remove only allowlisted, reproducible lab-project temporary files."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

TEMP_DIR_NAMES = {"tmp", "__pycache__", ".pytest_cache"}
LATEX_AUX_SUFFIXES = {".aux", ".fdb_latexmk", ".fls", ".log", ".out", ".synctex.gz", ".xdv", ".toc"}
PROTECTED_DIRS = {"raw", "processed", "figures", "generated", "config"}

def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False

def scan(root: Path) -> list[Path]:
    candidates: set[Path] = set()
    for path in root.rglob("*"):
        if any(part in PROTECTED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_dir() and path.name in TEMP_DIR_NAMES:
            candidates.add(path)
        elif path.is_file() and any(path.name.lower().endswith(suffix) for suffix in LATEX_AUX_SUFFIXES):
            candidates.add(path)
    # When a directory is removed, omit its children from the displayed list.
    dirs = {p for p in candidates if p.is_dir()}
    return sorted((p for p in candidates if not any(parent in dirs for parent in p.parents)), key=lambda p: str(p).lower())

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--apply", action="store_true", help="remove scanned allowlisted paths")
    args = parser.parse_args()
    root = args.project.resolve()
    if not root.is_dir():
        raise SystemExit(f"Project directory not found: {root}")
    candidates = scan(root)
    print(f"Scanned project: {root}")
    if not candidates:
        print("No allowlisted temporary files found.")
        return 0
    for path in candidates:
        print(f"{'DELETE' if args.apply else 'FOUND '}  {path.relative_to(root)}")
    if args.apply:
        for path in candidates:
            if not is_within(path, root):
                raise RuntimeError(f"Refusing path outside project: {path}")
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        print(f"Removed {len(candidates)} allowlisted path(s).")
    else:
        print("Dry run only. Re-run with --apply after final PDF verification.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
