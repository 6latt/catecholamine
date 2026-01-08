"""Validate raw data + metadata.

Usage:
  python scripts/validate_raw.py

This enforces:
  - every CSV/TSV in data/raw/** has a sibling .meta.yaml
  - required metadata fields exist
  - basic value sanity (species/task_domain/effect_type)

The goal is not to be a perfect schema validator; it's to prevent
silent drift and accidental mixing of species/populations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from rich.console import Console
from rich.table import Table


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SCHEMA = ROOT / "schemas" / "raw_meta.schema.yaml"

console = Console()


def load_schema() -> Dict[str, Any]:
    with open(SCHEMA, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_meta(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def check_required(meta: Dict[str, Any], required: List[str]) -> List[str]:
    missing = []
    for k in required:
        if k not in meta or meta.get(k) in (None, ""):
            missing.append(k)
    return missing


def allowed_check(meta: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    fields = schema.get("fields", {})
    for k, spec in fields.items():
        if k not in meta:
            continue
        allowed = spec.get("allowed")
        if allowed is not None:
            v = meta.get(k)
            if v not in allowed:
                errs.append(f"{k}={v!r} not in allowed={allowed}")
    return errs


def validate() -> int:
    schema = load_schema()
    required = schema.get("required", [])
    problems: List[Tuple[str, str]] = []

    if not RAW.exists():
        console.print("[yellow]no data/raw directory found[/yellow]")
        return 0

    data_files = []
    for ext in ("*.csv", "*.tsv"):
        # Exclude template files (starting with underscore)
        all_files = RAW.rglob(ext)
        data_files.extend([f for f in all_files if not f.name.startswith('_')])

    # allow empty repo
    if not data_files:
        console.print("[green]no raw data files yet — ok[/green]")
        return 0

    for df in data_files:
        meta_path = df.with_suffix(df.suffix + ".meta.yaml")
        if not meta_path.exists():
            problems.append((str(df.relative_to(ROOT)), "missing .meta.yaml"))
            continue

        meta = load_meta(meta_path)
        missing = check_required(meta, required)
        if missing:
            problems.append((str(meta_path.relative_to(ROOT)), f"missing required: {missing}"))

        errs = allowed_check(meta, schema)
        for e in errs:
            problems.append((str(meta_path.relative_to(ROOT)), e))

    if problems:
        table = Table(title="raw validation problems")
        table.add_column("file", style="cyan")
        table.add_column("problem", style="red")
        for f, p in problems:
            table.add_row(f, p)
        console.print(table)
        console.print("\n[red]validation failed[/red]")
        return 1

    console.print("[green]raw validation passed[/green]")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
