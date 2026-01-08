# Repository Architecture Guide

## Overview

This repository implements a reproducible pipeline for catecholamine research with built-in anti-cherrypicking safeguards. The architecture supports:

- **Multi-axis outcomes**: Behavior, biomarkers, and their correlations
- **Species separation**: Human, rodent, primate, in vitro data kept distinct
- **Population tracking**: ADHD, control, MDD, anxiety, ASD, etc.
- **Quantitative-first**: All data normalized to effect sizes with standard errors when available
- **Contradiction detection**: Automated flagging of conflicting findings with statistical tests

## Directory Structure

```
catecholamine/
├── data/
│   ├── raw/                    # Immutable source data
│   │   ├── paper_key_1/       # One folder per paper (recommended)
│   │   │   ├── table1.csv
│   │   │   ├── table1.csv.meta.yaml
│   │   │   └── README.md
│   │   ├── _template*.csv/yaml # Templates (excluded from processing)
│   │   └── *.csv              # Flat files also supported
│   └── derived/               # Generated datasets (rebuildable)
│       ├── master_dataset.parquet  # Main analysis file
│       ├── master_dataset.csv      # Human-readable copy
│       └── study_index.csv         # Quick reference
├── reports/                   # Generated analysis reports
│   ├── study_matrix.csv       # Paper counts by domain/species/population
│   ├── contradictions.csv     # Flagged conflicting findings
│   ├── candidates_openalex.csv     # Discovered papers pending review
│   └── rejected_candidates.csv     # Rejected papers with reasons
├── scripts/                   # Pipeline scripts
│   ├── validate_raw.py        # Validate raw data and metadata
│   ├── build_dataset.py       # Build master dataset
│   ├── build_reports.py       # Generate analysis reports
│   └── scrape/
│       └── search_openalex.py # Search for candidate papers
├── paper/                     # Manuscript and sections
│   ├── paper.qmd              # Main paper document (Quarto)
│   └── sections/              # Paper sections
│       ├── methods_extraction.qmd
│       └── methods_normalization.qmd
├── schemas/                   # Data validation schemas
│   └── raw_meta.schema.yaml   # Required metadata fields
└── protocol/                  # Research protocols
    └── PROTOCOL.md            # Extraction and inclusion rules
```

## Workflow

### 1. Paper Discovery and Screening

```bash
# Search for candidate papers
python scripts/scrape/search_openalex.py \
  --query "prefrontal dopamine working memory" \
  --rows 50

# Review candidates in reports/candidates_openalex.csv
# Move rejected papers to reports/rejected_candidates.csv with reasons
```

### 2. Data Extraction

For each included paper:

1. Create a paper_key folder: `data/raw/smith_2023_pfc/`
2. Extract data to CSV files with descriptive names
3. Create metadata file for each CSV: `<file>.csv.meta.yaml`
4. Use templates as guides:
   - `data/raw/_template_extraction.csv`
   - `data/raw/_template.meta.yaml`

Example structure:
```
data/raw/smith_2023_pfc/
├── table2_behavior.csv
├── table2_behavior.csv.meta.yaml
├── fig3_timecourse.csv
├── fig3_timecourse.csv.meta.yaml
└── README.md  (optional notes)
```

### 3. Validation

```bash
# Validate all raw data and metadata
python scripts/validate_raw.py
```

This checks:
- Every CSV/TSV has a `.meta.yaml` file
- Required metadata fields are present
- Species, task_domain, effect_type values are valid

### 4. Dataset Building

```bash
# Build normalized master dataset
python scripts/build_dataset.py
```

This:
- Recursively finds all data files in `data/raw/`
- Applies paper-specific normalizers
- Merges into long-format master dataset
- Outputs to `data/derived/master_dataset.parquet`

### 5. Report Generation

```bash
# Generate analysis reports
python scripts/build_reports.py
```

This produces:
- **study_matrix.csv**: Paper counts by domain/species/population
- **contradictions.csv**: Findings with conflicting signs
  - Uses confidence intervals when `effect_se` is available
  - Falls back to absolute threshold otherwise
  - Includes severity scoring (strong/moderate/weak)

### 6. Paper Rendering

```bash
# Render the manuscript
quarto render paper/paper.qmd
```

Output appears in `paper/_output/`

## Anti-Cherrypicking Safeguards

### 1. Immutable Raw Data
- Original extractions never modified
- Corrections made in build pipeline, not source files
- Full git history tracks all changes

### 2. Rejection Documentation
- All rejected candidates documented in `reports/rejected_candidates.csv`
- Requires: candidate_id, title, reason, reviewed_by, date
- Prevents silent exclusion of inconvenient results

### 3. Comprehensive Extraction
- Extract ALL relevant outcomes from included papers
- Flag problematic data with `quality_flags` rather than exclude
- Document extraction method and notes

### 4. Contradiction Detection
- Automated flagging of conflicting findings
- Statistical testing using confidence intervals
- Transparent reporting of disagreements

### 5. Version Control
- All data, metadata, and code in git
- Changes tracked with commit messages
- Reproducible from any point in history

## Data Schema

### Required Metadata Fields

Every `.meta.yaml` file must include:

```yaml
paper_key: unique_identifier
citation: {title, year, doi, pmid, journal}
species: human | rodent | primate | in_vitro | mixed
population: control | adhd | mdd | anxiety | asd | etc
task_domain: attention | working_memory | flexibility | salience | mood | other
task_name: "specific task name"
outcome:
  name: "outcome variable"
  units: "measurement units"
  direction_higher_is_better: true/false
manipulation:
  kind: drug | stress | genotype | pet_measure | microdialysis
  # Additional fields depend on kind
effect_type: cohens_d | hedges_g | r | beta | mean_diff | raw
extraction_method: table | supplement | digitized | reported_effect | computed
notes: "optional notes"
quality_flags: []  # optional quality concerns
```

### Standard Dataset Columns

The master dataset includes:

- **paper_key**: Unique paper identifier
- **citation_key**: Citation reference
- **study_id**: Within-paper study identifier
- **species**: Species of subjects
- **population**: Population characteristics
- **task_domain**: Cognitive domain
- **task_name**: Specific task
- **measure_kind**: `behavior` or `biomarker`
- **measure_name**: Specific measure
- **effect_type**: Type of effect size
- **effect_value**: Numeric effect value
- **effect_se**: Standard error (when available)
- **n**: Sample size
- **extraction_method**: How data were extracted
- **notes**: Additional context

## Adding New Papers

1. **Create paper_key folder**: `data/raw/yourpaper_2024/`

2. **Extract data**: Save tables/figures as CSV with metadata

3. **Validate**: `python scripts/validate_raw.py`

4. **Add normalizer** (if needed): Edit `scripts/build_dataset.py`
   ```python
   elif f.name == "yourpaper_data.csv":
       df_norm = normalize_yourpaper(df_raw, meta)
   ```

5. **Rebuild**: `python scripts/build_dataset.py`

6. **Generate reports**: `python scripts/build_reports.py`

7. **Update paper**: `quarto render paper/paper.qmd`

## Tips

- **Templates**: Copy `_template*.csv/yaml` as starting points
- **Flat vs folders**: Both supported; folders recommended for multiple extractions
- **Effect SE**: Always include when available for better contradiction detection
- **Quality flags**: Use to mark concerns rather than exclude data
- **Git commits**: Commit after each paper extraction

## Troubleshooting

### Validation fails
- Check metadata file exists with correct naming: `<file>.csv.meta.yaml`
- Verify all required fields present
- Check species/task_domain/effect_type against allowed values

### Build fails
- Ensure pandas/numpy/pyarrow installed: `pip install -r requirements.txt`
- Check CSV format is valid
- Add custom normalizer for unusual data formats

### Contradictions not detected
- Verify `effect_value` is numeric
- Check if `effect_se` is provided for CI-based detection
- Review `contradiction_type` and `severity` in output

## Further Reading

- **Protocol**: See `protocol/PROTOCOL.md` for inclusion/exclusion criteria
- **Schemas**: See `schemas/raw_meta.schema.yaml` for full metadata spec
- **Methods**: See `paper/sections/methods_*.qmd` for detailed methodology
