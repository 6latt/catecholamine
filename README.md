# Catecholamine Research Repository

A reproducible research pipeline for analyzing catecholamine effects on prefrontal cortex performance.

## Overview

This repository provides a systematic pipeline to:
- Collect and normalize quantitative findings from research papers (tables, supplementary data, digitized curves)
- Analyze data across cognitive domains (attention, working memory, flexibility, salience, mood)
- **Generate scientific papers from unstructured research notes**
- Generate reproducible manuscripts with citations and auto-generated figures

## Quick Start: Generate a Paper from Research Notes

The easiest way to generate a complete scientific paper from your deep research notes:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full paper generation pipeline
python scripts/catecholamine_cli.py full --simple
```

This will:
1. Validate your raw data
2. Build a master dataset
3. Generate analysis reports
4. Parse `deepresearch.md` and convert it into a structured scientific paper
5. Render the paper to HTML

Your paper will be available at: `paper/_output/generated_paper.html`

## Manual Workflow

### Traditional Data Analysis Pipeline

1. Place **raw** extracted data in `data/raw/` (CSV/TSV format). Never edit raw data files in place.
2. For each raw data file, create a sibling metadata file: `<file>.csv.meta.yaml`
3. Run `python scripts/validate_raw.py` to validate data and metadata
4. Run `python scripts/build_dataset.py` to produce `data/derived/master_dataset.parquet`
5. Run `python scripts/build_reports.py` to generate `reports/*.csv` files used by the paper
6. Render the paper with Quarto: `quarto render paper/paper.qmd`

### Paper Generation from Deep Research

If you have comprehensive research notes in `deepresearch.md`, you can automatically generate a structured scientific paper:

```bash
# Generate the paper structure from deepresearch.md
python scripts/generate_paper.py

# Render to HTML (works without Quarto)
python scripts/render_paper_simple.py

# Or render with Quarto (if installed)
cd paper
quarto render generated_paper.qmd
```

## CLI Tool

The `catecholamine_cli.py` provides a unified interface for all operations:

```bash
# Run the complete pipeline
python scripts/catecholamine_cli.py full

# Generate paper from deepresearch.md only
python scripts/catecholamine_cli.py generate

# Render the generated paper
python scripts/catecholamine_cli.py render --source generated

# Validate data
python scripts/catecholamine_cli.py validate

# Build dataset
python scripts/catecholamine_cli.py build

# Build reports
python scripts/catecholamine_cli.py reports

# See all options
python scripts/catecholamine_cli.py --help
```

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
