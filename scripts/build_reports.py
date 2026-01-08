"""Generate small 'reports' tables used by the paper.

Outputs (in reports/):
  - study_matrix.csv : counts by domain/species/population
  - contradictions.csv : where effects disagree in sign
    - Uses confidence intervals when effect_se is available (statistical test)
    - Falls back to absolute effect threshold (|value| >= 0.1) when SE unavailable

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


def confidence_intervals_overlap(effect1: float, se1: float, effect2: float, se2: float, z: float = 1.96) -> bool:
    """
    Check if 95% confidence intervals of two effects overlap.
    z = 1.96 for 95% CI (default), 2.58 for 99% CI.
    
    Returns True if CIs overlap (no statistical contradiction), False if they don't overlap.
    """
    ci1_lower = effect1 - z * se1
    ci1_upper = effect1 + z * se1
    ci2_lower = effect2 - z * se2
    ci2_upper = effect2 + z * se2
    
    # No overlap if one interval is entirely below or above the other
    return not (ci1_upper < ci2_lower or ci2_upper < ci1_lower)


def build_contradictions(df: pd.DataFrame, min_abs: float = 0.1) -> pd.DataFrame:
    """
    Flag cells where we see both positive and negative effects.
    
    Logic:
    1. If effect_se exists for observations: use CI-based test (statistical significance)
    2. Otherwise: fall back to simple threshold (|effect| >= min_abs)
    
    A contradiction is "strong" if:
    - CIs exist and don't overlap (statistically significant disagreement)
    - CIs don't exist but effects have opposite signs with |effect| >= min_abs
    """
    beh = df[df["measure_kind"] == "behavior"].copy()
    beh = beh[pd.to_numeric(beh["effect_value"], errors="coerce").notna()]
    beh["effect_value"] = pd.to_numeric(beh["effect_value"], errors="coerce")
    beh["effect_se"] = pd.to_numeric(beh["effect_se"], errors="coerce")

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
            "contradiction_type",
            "severity",
        ])

    rows = []
    for keys, grp in beh.groupby(["task_domain", "species", "population", "measure_name"], dropna=False):
        # Split into positive and negative effects
        pos_grp = grp[grp["effect_value"] > 0].copy()
        neg_grp = grp[grp["effect_value"] < 0].copy()
        
        if pos_grp.empty or neg_grp.empty:
            continue  # No contradiction if all same sign
        
        # Determine contradiction type and severity
        both_groups_have_se = (
            pos_grp["effect_se"].notna().any() and 
            neg_grp["effect_se"].notna().any()
        )
        
        contradiction_type = "ci_based" if both_groups_have_se else "threshold_based"
        severity = "unknown"
        
        if both_groups_have_se:
            # Check if any pair of pos/neg effects have non-overlapping CIs
            ci_conflicts = False
            for _, pos_row in pos_grp[pos_grp["effect_se"].notna()].iterrows():
                for _, neg_row in neg_grp[neg_grp["effect_se"].notna()].iterrows():
                    if not confidence_intervals_overlap(
                        pos_row["effect_value"], pos_row["effect_se"],
                        neg_row["effect_value"], neg_row["effect_se"]
                    ):
                        ci_conflicts = True
                        break
                if ci_conflicts:
                    break
            
            severity = "strong" if ci_conflicts else "weak"
        else:
            # Fall back to threshold-based: check if effects exceed min_abs
            pos_strong = (pos_grp["effect_value"].abs() >= min_abs).any()
            neg_strong = (neg_grp["effect_value"].abs() >= min_abs).any()
            
            if pos_strong and neg_strong:
                severity = "moderate"
            else:
                severity = "weak"
        
        pos_papers = pos_grp["paper_key"].dropna().unique().tolist()
        neg_papers = neg_grp["paper_key"].dropna().unique().tolist()
        
        rows.append({
            "task_domain": keys[0],
            "species": keys[1],
            "population": keys[2],
            "measure_name": keys[3],
            "pos_papers": ", ".join(sorted(pos_papers)),
            "neg_papers": ", ".join(sorted(neg_papers)),
            "n_pos": len(pos_papers),
            "n_neg": len(neg_papers),
            "contradiction_type": contradiction_type,
            "severity": severity,
        })

    out = pd.DataFrame(rows)
    if not out.empty:
        severity_order = pd.CategoricalDtype(["strong", "moderate", "weak"], ordered=True)
        out["severity"] = out["severity"].astype(severity_order)
        out = out.sort_values(["severity", "task_domain", "species", "population", "measure_name"])
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
