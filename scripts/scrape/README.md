# scraping / ingestion helpers

we **do not** scrape paywalled full-text.

what we *can* automate, legally:

* paper discovery + metadata (title/doi/pmid/year/journal) via open APIs
* pulling open-access full text (when clearly licensed)
* downloading supplemental CSVs when they are publicly accessible

workflow:

1) run a metadata search script to build a `candidates.csv` list
2) manually screen for relevance + open-access availability
3) extract numbers (tables/supplements/digitized figures)
4) store extractions in `data/raw/` with `.meta.yaml`

starter scripts here are templates. you’ll likely add api keys / rate-limits later.
