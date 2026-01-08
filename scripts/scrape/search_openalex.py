"""Search OpenAlex for candidate papers (metadata only).

This is for *discovery*, not full-text scraping.

Example:
  python scripts/scrape/search_openalex.py --query "prefrontal dopamine inverted U working memory" --rows 50

Writes:
  reports/candidates_openalex.csv

To track rejections (anti-cherrypicking):
  Manually review candidates and move rejected ones to reports/rejected_candidates.csv
  with reason, reviewer, and date.

OpenAlex docs: https://docs.openalex.org/
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from datetime import datetime

import requests


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "candidates_openalex.csv"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--rows", type=int, default=50)
    ap.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds")
    args = ap.parse_args()

    params = {
        "search": args.query,
        "per-page": args.rows,
    }
    r = requests.get("https://api.openalex.org/works", params=params, timeout=args.timeout)
    r.raise_for_status()
    data = r.json()

    # Generate timestamp-based prefix for unique candidate IDs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "candidate_id",
                "title",
                "year",
                "doi",
                "openalex_id",
                "is_oa",
                "oa_url",
                "cited_by_count",
                "review_status",
            ],
        )
        w.writeheader()
        for idx, item in enumerate(data.get("results", []), start=1):
            title = item.get("display_name")
            year = item.get("publication_year")
            doi = item.get("doi")
            oid = item.get("id")
            oa = item.get("open_access", {}) or {}
            
            # Use timestamp and index for unique candidate ID
            candidate_id = f"cand_{timestamp}_{idx:03d}"
            
            w.writerow(
                {
                    "candidate_id": candidate_id,
                    "title": title,
                    "year": year,
                    "doi": doi,
                    "openalex_id": oid,
                    "is_oa": oa.get("is_oa"),
                    "oa_url": oa.get("oa_url"),
                    "cited_by_count": item.get("cited_by_count"),
                    "review_status": "pending",
                }
            )

    print(f"wrote {OUT}")
    print("\nNext steps:")
    print("1. Review candidates in reports/candidates_openalex.csv")
    print("2. For rejected papers, copy the row to reports/rejected_candidates.csv")
    print("3. Add rejection reason, reviewed_by, and review_date columns")


if __name__ == "__main__":
    main()
