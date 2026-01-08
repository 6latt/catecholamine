# Project Structure

This document describes the organization of the catecholamine research repository.

## Directory Structure

```
catecholamine/
├── data/               # All data files
│   ├── raw/           # Immutable raw data files with metadata
│   └── derived/       # Generated datasets (rebuildable from raw)
├── figures/           # Output figures (generated, not committed)
├── notebooks/         # Exploratory analysis notebooks
├── paper/             # Paper manuscript and related files
│   └── sections/      # Paper sections (if split)
├── protocol/          # Research protocols and methodologies
├── refs/              # Bibliography and citation files
├── reports/           # Generated reports from scripts
├── schemas/           # Data validation schemas
├── scripts/           # Pipeline scripts
│   ├── scrape/       # Data scraping utilities
│   ├── validate_raw.py    # Validate raw data
│   ├── build_dataset.py   # Build master dataset
│   └── build_reports.py   # Generate reports
└── src/               # Reusable Python modules
    └── catecholamine/ # Main package
```

## Key Files

- `README.md` - Project overview and quickstart
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Python package configuration
- `LICENSE` - MIT license
- `CONTRIBUTING.md` - Contribution guidelines
- `.gitignore` - Git ignore patterns

## Data Flow

1. **Raw Data** (`data/raw/`) - Immutable source data with metadata
2. **Validation** (`scripts/validate_raw.py`) - Ensure data quality
3. **Master Dataset** (`scripts/build_dataset.py`) - Build normalized dataset
4. **Reports** (`scripts/build_reports.py`) - Generate analysis reports
5. **Paper** (`paper/paper.qmd`) - Render final manuscript

## Important Principles

### Data Provenance
- Every raw data file must have a `.meta.yaml` companion file
- Never edit raw data in place
- All derived data must be rebuildable from raw data

### Reproducibility
- All figures generated from code
- Paper rendered from Quarto documents
- Complete dependency specification

### Anti-Cherry-Picking
- Document all inclusion/exclusion decisions
- Log extraction methods
- Use quality flags for questionable data

## Getting Started

See README.md for setup instructions and workflow overview.
