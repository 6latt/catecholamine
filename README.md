# Catecholamine Research Repository

A reproducible research pipeline for analyzing catecholamine effects on prefrontal cortex performance.

## Overview

This repository provides a systematic pipeline to:
- Collect and normalize quantitative findings from research papers (tables, supplementary data, digitized curves)
- Analyze data across cognitive domains (attention, working memory, flexibility, salience, mood)
- Generate reproducible manuscripts with citations and auto-generated figures

## Workflow

1. Place **raw** extracted data in `data/raw/` (CSV/TSV format). Never edit raw data files in place.
2. For each raw data file, create a sibling metadata file: `<file>.csv.meta.yaml`
3. Run `python scripts/validate_raw.py` to validate data and metadata
4. Run `python scripts/build_dataset.py` to produce `data/derived/master_dataset.parquet`
5. Run `python scripts/build_reports.py` to generate `reports/*.csv` files used by the paper
6. Render the paper with Quarto: `quarto render paper/paper.qmd`

## Why Quarto?

While Jupyter notebooks are excellent for exploratory analysis, Quarto documents provide additional benefits for manuscript preparation:

- Clean rendering to HTML/PDF formats
- Code and narrative integrated in a single document
- Stable citations and figure numbering
- Git-friendly diff and merge operations

**Recommendation:** Use Quarto (`.qmd`) with a Python kernel for manuscript preparation, while continuing to use Jupyter notebooks for exploratory data analysis.

## Setup

### Python Environment

You can use any Python environment manager (uv, Poetry, conda). For a minimal pip installation:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Rendering the Paper

Install [Quarto](https://quarto.org/docs/get-started/) (system-level installation), then:

```bash
quarto render paper/paper.qmd
```

Output files will be generated in `paper/_output/`.

## Data Provenance Rules

**Important:** Every raw data file must have an accompanying metadata file:

- Data file: `data/raw/weber2022_table3.csv`
- Metadata file: `data/raw/weber2022_table3.csv.meta.yaml`

The metadata file should include:
- Paper citation key
- Population/species information
- Task description
- Units of measurement
- Extraction method (table, digitized, supplementary material)
- Any relevant caveats or notes

## Citation Workflow

- Maintain BibTeX entries in `refs/references.bib`
- Cite in Quarto documents using: `@citation_key`

**Recommended:** Use Zotero with Better BibTeX to export citations automatically. Manual maintenance is also supported.

## What's Included

This repository includes:
- Starter dataset with example data
- Processing scripts for data validation and normalization
- Paper skeleton with basic structure
- Documentation and schemas

Replace or extend these with your own research data and analysis.
