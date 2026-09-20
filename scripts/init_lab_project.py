#!/usr/bin/env python3
"""Create a lab-report project from the bundled neutral template."""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

def copy_without_overwrite(src: str, dst: str) -> str:
    target = Path(dst)
    return str(target) if target.exists() else shutil.copy2(src, dst)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new or empty output directory")
    parser.add_argument("--force", action="store_true", help="merge without overwriting existing files")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent.parent / "assets" / "project-template"
    destination = args.destination.resolve()
    if not source.is_dir():
        raise SystemExit(f"Template directory not found: {source}")
    if destination.exists() and any(destination.iterdir()) and not args.force:
        raise SystemExit("Destination is not empty; choose another directory or pass --force.")
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, dirs_exist_ok=True, copy_function=copy_without_overwrite)
    print(f"Initialized project at {destination}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
