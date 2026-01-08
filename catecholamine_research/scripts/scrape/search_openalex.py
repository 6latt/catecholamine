"""Search OpenAlex for candidate papers (metadata only).

This is for *discovery*, not full-text scraping.

Example:
  python scripts/scrape/search_openalex.py --query "prefrontal dopamine inverted U working memory" --rows 50

Writes:
  reports/candidates_openalex.csv

OpenAlex docs: https://docs.openalex.org/
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "candidates_openalex.csv"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--rows", type=int, default=50)
    args = ap.parse_args()

    params = {
        "search": args.query,
        "per-page": args.rows,
    }
    r = requests.get("https://api.openalex.org/works", params=params, timeout=60)
    r.raise_for_status()
    data = r.json()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "title",
                "year",
                "doi",
                "openalex_id",
                "is_oa",
                "oa_url",
                "cited_by_count",
            ],
        )
        w.writeheader()
        for item in data.get("results", []):
            title = item.get("display_name")
            year = item.get("publication_year")
            doi = item.get("doi")
            oid = item.get("id")
            oa = item.get("open_access", {}) or {}
            w.writerow(
                {
                    "title": title,
                    "year": year,
                    "doi": doi,
                    "openalex_id": oid,
                    "is_oa": oa.get("is_oa"),
                    "oa_url": oa.get("oa_url"),
                    "cited_by_count": item.get("cited_by_count"),
                }
            )

    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
