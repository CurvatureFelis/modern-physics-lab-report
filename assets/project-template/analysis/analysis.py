#!/usr/bin/env python3
"""Neutral, reproducible analysis entry point; adapt model-specific sections."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"
GENERATED = ROOT / "report" / "generated"
TRANSCRIPTION = PROCESSED / "manual_transcription.csv"
TRANSCRIPTION_COLUMNS = [
    "record_id", "sample_id", "quantity", "value", "unit", "condition",
    "source_file", "source_region", "verification_note",
]

def prepare_directories() -> None:
    for path in (RAW, PROCESSED, FIGURES, GENERATED / "tables"):
        path.mkdir(parents=True, exist_ok=True)

def write_manifest() -> None:
    rows = []
    for path in sorted(p for p in RAW.rglob("*") if p.is_file()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(RAW).as_posix()}")
    (ROOT / "data" / "raw_manifest.sha256").write_text("\n".join(rows) + ("\n" if rows else ""), encoding="utf-8")

def load_inputs() -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {}
    for path in sorted(RAW.iterdir()):
        if path.suffix.lower() == ".csv":
            tables[path.name] = pd.read_csv(path)
        elif path.suffix.lower() in {".xlsx", ".xls"}:
            book = pd.read_excel(path, sheet_name=None)
            tables.update({f"{path.name}::{sheet}": frame for sheet, frame in book.items()})
    if TRANSCRIPTION.exists():
        transcription = pd.read_csv(TRANSCRIPTION)
        missing_columns = [column for column in TRANSCRIPTION_COLUMNS if column not in transcription.columns]
        if missing_columns:
            raise SystemExit(
                "manual_transcription.csv is missing required columns: " + ", ".join(missing_columns)
            )
        if not transcription.empty:
            tables["processed/manual_transcription.csv"] = transcription
    return tables

def audit_table(name: str, frame: pd.DataFrame) -> dict[str, object]:
    return {"source": name, "rows": int(frame.shape[0]), "columns": [str(c) for c in frame.columns],
            "missing_by_column": {str(k): int(v) for k, v in frame.isna().sum().items()},
            "duplicate_rows": int(frame.duplicated().sum())}

def analyze(tables: dict[str, pd.DataFrame]) -> dict[str, object]:
    if not tables:
        raise SystemExit(
            "No machine-readable table was found. Add CSV/XLS/XLSX files to data/raw "
            "or transcribe image records into data/processed/manual_transcription.csv."
        )
    # Model-specific work belongs here. Never silently drop NA, duplicates, or outliers.
    return {
        "status": "inputs_indexed",
        "audits": [audit_table(name, frame) for name, frame in tables.items()],
    }

def write_outputs(results: dict[str, object]) -> None:
    (ROOT / "analysis" / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    tex = "% Auto-generated; model-specific result macros are written here.\n"
    (GENERATED / "results.tex").write_text(tex, encoding="utf-8")

def main() -> int:
    prepare_directories()
    plt.rcParams.update({"figure.dpi": 120, "savefig.dpi": 300, "axes.grid": False})
    write_manifest()
    results = analyze(load_inputs())
    write_outputs(results)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
