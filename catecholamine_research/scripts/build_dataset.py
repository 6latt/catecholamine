#!/usr/bin/env python3
"""Build a unified 'master_dataset' from raw extracted sources.

Design goals:
- keep raw files immutable
- normalize to a tidy table with explicit columns:
  species, population, diagnosis, task_domain, task_name,
  manipulation (drug/dose/genotype/etc), biomarker_type,
  biomarker_value, outcome_type, outcome_value, effect_size, n,
  and a citation key.

This script is intentionally conservative:
  - it keeps everything in a *long* format so domains/species/populations
    don't get accidentally mixed.
  - it preserves provenance (paper_key + citation info + extraction notes).

You extend this by adding loaders/normalizers for new raw formats.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"


STANDARD_COLS = [
    "paper_key",
    "citation_key",
    "study_id",
    "species",
    "population",
    "task_domain",
    "task_name",
    "measure_kind",  # behavior | biomarker
    "measure_name",
    "effect_type",
    "effect_value",
    "effect_se",
    "n",
    "extraction_method",
    "notes",
]


def load_meta_for_datafile(datafile: Path) -> dict:
    """Support both <file>.csv.meta.yaml and legacy <stem>.meta.yaml."""
    candidate1 = datafile.with_suffix(datafile.suffix + ".meta.yaml")
    candidate2 = datafile.with_suffix(".meta.yaml")
    if candidate1.exists():
        return yaml.safe_load(candidate1.read_text()) or {}
    if candidate2.exists():
        return yaml.safe_load(candidate2.read_text()) or {}
    raise FileNotFoundError(f"missing meta for {datafile}")


def normalize_example_inverted_u(df: pd.DataFrame, meta: dict) -> pd.DataFrame:
    """Convert the starter example into long format.

    Expected columns:
      - study
      - species
      - behavior_effect_size_d
      - dopamine_effect_size_d
    """
    out_rows = []
    for _, r in df.iterrows():
        study = str(r.get("study"))
        species = str(r.get("species", meta.get("species")))

        # biomarker row
        if pd.notna(r.get("dopamine_effect_size_d")):
            out_rows.append(
                {
                    "study_id": study,
                    "species": species,
                    "measure_kind": "biomarker",
                    "measure_name": str(r.get("biomarker_type", "PFC_dopamine")),
                    "effect_type": "cohens_d",
                    "effect_value": float(r.get("dopamine_effect_size_d")),
                }
            )

        # behavior row
        if pd.notna(r.get("behavior_effect_size_d")):
            out_rows.append(
                {
                    "study_id": study,
                    "species": species,
                    "measure_kind": "behavior",
                    "measure_name": meta.get("outcome", {}).get("name", "behavior"),
                    "effect_type": "cohens_d",
                    "effect_value": float(r.get("behavior_effect_size_d")),
                }
            )

    out = pd.DataFrame(out_rows)
    return out


def attach_meta(df: pd.DataFrame, meta: dict) -> pd.DataFrame:
    """Attach provenance + fill missing standard columns from meta."""
    df = df.copy()
    df["paper_key"] = meta.get("paper_key", "unknown")
    df["citation_key"] = meta.get("paper_key", "unknown")  # default citekey

    for col in ("population", "task_domain", "task_name", "extraction_method", "notes"):
        if col not in df.columns or df[col].isna().all():
            df[col] = meta.get(col)
        else:
            df[col] = df[col].fillna(meta.get(col))

    # default n/effect_se if absent
    if "n" not in df.columns:
        df["n"] = None
    if "effect_se" not in df.columns:
        df["effect_se"] = None

    return df


def coerce_standard(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure we have at least the standard columns; keep extra columns."""
    for c in STANDARD_COLS:
        if c not in df.columns:
            df[c] = None
    return df


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)

    data_files = list(RAW.glob("*.csv")) + list(RAW.glob("*.tsv"))
    if not data_files:
        print("no data/raw/*.csv yet")
        return

    all_parts = []
    for f in sorted(data_files):
        meta = load_meta_for_datafile(f)
        df_raw = pd.read_csv(f)

        # format-specific normalizers
        if f.name == "example_inverted_u.csv":
            df_norm = normalize_example_inverted_u(df_raw, meta)
        else:
            df_norm = df_raw

        df_norm = attach_meta(df_norm, meta)
        df_norm = coerce_standard(df_norm)
        all_parts.append(df_norm)

    master = pd.concat(all_parts, ignore_index=True)

    out_parquet = DERIVED / "master_dataset.parquet"
    master.to_parquet(out_parquet, index=False)
    master.to_csv(DERIVED / "master_dataset.csv", index=False)

    # lightweight index for quick counts
    idx = (
        master[["paper_key", "species", "population", "task_domain"]]
        .drop_duplicates()
        .sort_values(["task_domain", "species", "population", "paper_key"])
    )
    idx.to_csv(DERIVED / "study_index.csv", index=False)

    print(f"wrote {out_parquet}")


if __name__ == "__main__":
    main()
