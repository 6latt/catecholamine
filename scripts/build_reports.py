"""Generate small 'reports' tables used by the paper.

Outputs (in reports/):
  - study_matrix.csv : counts by domain/species/population
  - contradictions.csv : where effects disagree in sign
    (flags studies with both positive AND negative effects with |value| >= 0.1)

Run:
  python scripts/build_dataset.py
  python scripts/build_reports.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"


def load_master() -> pd.DataFrame:
    p = DERIVED / "master_dataset.parquet"
    if not p.exists():
        raise FileNotFoundError("run scripts/build_dataset.py first")
    return pd.read_parquet(p)


def build_study_matrix(df: pd.DataFrame) -> pd.DataFrame:
    # count unique papers contributing observations
    g = (
        df.groupby(["task_domain", "species", "population", "measure_kind"], dropna=False)[
            "paper_key"
        ]
        .nunique()
        .reset_index()
        .rename(columns={"paper_key": "n_papers"})
        .sort_values(["task_domain", "species", "population", "measure_kind"])
    )
    return g


def build_contradictions(df: pd.DataFrame, min_abs: float = 0.1) -> pd.DataFrame:
    """
    Flag cells where we see both positive and negative effects.

    This is deliberately simple and will get smarter as we add SE/CI and
    standardize outcome direction.
    """
    beh = df[df["measure_kind"] == "behavior"].copy()
    beh = beh[pd.to_numeric(beh["effect_value"], errors="coerce").notna()]
    beh["effect_value"] = pd.to_numeric(beh["effect_value"], errors="coerce")

    # ignore tiny effects by default (noise)
    beh = beh[beh["effect_value"].abs() >= min_abs]
    if beh.empty:
        return pd.DataFrame(columns=[
            "task_domain",
            "species",
            "population",
            "measure_name",
            "pos_papers",
            "neg_papers",
            "n_pos",
            "n_neg",
        ])

    rows = []
    for keys, grp in beh.groupby(["task_domain", "species", "population", "measure_name"], dropna=False):
        pos = grp[grp["effect_value"] > 0]["paper_key"].dropna().unique().tolist()
        neg = grp[grp["effect_value"] < 0]["paper_key"].dropna().unique().tolist()
        if pos and neg:
            rows.append(
                {
                    "task_domain": keys[0],
                    "species": keys[1],
                    "population": keys[2],
                    "measure_name": keys[3],
                    "pos_papers": ", ".join(sorted(pos)),
                    "neg_papers": ", ".join(sorted(neg)),
                    "n_pos": len(pos),
                    "n_neg": len(neg),
                }
            )

    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(["task_domain", "species", "population", "measure_name"])
    return out


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    df = load_master()

    matrix = build_study_matrix(df)
    matrix.to_csv(REPORTS / "study_matrix.csv", index=False)

    contradictions = build_contradictions(df)
    contradictions.to_csv(REPORTS / "contradictions.csv", index=False)

    print("wrote reports/")


if __name__ == "__main__":
    main()
