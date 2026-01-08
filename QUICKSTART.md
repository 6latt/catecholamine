# Quick Start Guide

Get up and running with the catecholamine research pipeline in 5 minutes.

## Prerequisites

- Python 3.9+
- Git

## Setup

```bash
# Clone the repository
git clone https://github.com/6latt/catecholamine.git
cd catecholamine

# Install dependencies
pip install -r requirements.txt
```

## Verify Installation

```bash
# Test the pipeline with example data
python scripts/validate_raw.py
python scripts/build_dataset.py
python scripts/build_reports.py

# You should see:
# ✓ raw validation passed
# ✓ wrote .../master_dataset.parquet
# ✓ wrote reports/
```

## Your First Data Extraction

### Option 1: Use Templates (Recommended for Beginners)

```bash
# 1. Copy templates
cp data/raw/_template_extraction.csv data/raw/yourpaper_2024.csv
cp data/raw/_template.meta.yaml data/raw/yourpaper_2024.csv.meta.yaml

# 2. Edit the files with your data
# 3. Validate and build
python scripts/validate_raw.py
python scripts/build_dataset.py
```

### Option 2: Use Paper-Key Folder (Recommended for Multiple Extractions)

```bash
# 1. Create folder
mkdir -p data/raw/yourpaper_2024

# 2. Add data file
cat > data/raw/yourpaper_2024/table1.csv << 'EOF'
study_id,measure_kind,measure_name,effect_value,effect_se,n
study1,behavior,accuracy,0.45,0.12,48
study1,biomarker,dopamine_level,0.32,0.10,48
EOF

# 3. Add metadata
cat > data/raw/yourpaper_2024/table1.csv.meta.yaml << 'EOF'
paper_key: yourpaper_2024
citation:
  title: "Your Paper Title"
  year: 2024
  doi: "10.1234/example"
species: human
population: control
task_domain: working_memory
task_name: "n-back"
outcome:
  name: "accuracy"
  units: "percent"
  direction_higher_is_better: true
manipulation:
  kind: drug
  drug: "methylphenidate"
effect_type: cohens_d
extraction_method: table
notes: ""
quality_flags: []
EOF

# 4. Validate and build
python scripts/validate_raw.py
python scripts/build_dataset.py
python scripts/build_reports.py
```

## View Results

```bash
# Study matrix (papers by domain/species)
cat reports/study_matrix.csv

# Contradictions (conflicting findings)
cat reports/contradictions.csv

# Master dataset
head data/derived/master_dataset.csv
```

## Render the Paper (Optional)

Requires [Quarto](https://quarto.org/):

```bash
quarto render paper/paper.qmd
open paper/_output/paper.html
```

## Common Tasks

### Search for Candidate Papers

```bash
python scripts/scrape/search_openalex.py \
  --query "dopamine working memory" \
  --rows 50

# Review: reports/candidates_openalex.csv
# Reject: Copy rejected rows to reports/rejected_candidates.csv with reasons
```

### Add a New Paper (Full Workflow)

```bash
# 1. Create structure
mkdir -p data/raw/smith_2023

# 2. Extract data (manual step - copy tables, digitize figures)

# 3. Create metadata for each file
# (use _template.meta.yaml as guide)

# 4. Validate
python scripts/validate_raw.py

# 5. Build dataset
python scripts/build_dataset.py

# 6. Generate reports
python scripts/build_reports.py

# 7. Check for contradictions
cat reports/contradictions.csv
```

### Fix Validation Errors

```bash
# Run validation to see errors
python scripts/validate_raw.py

# Common fixes:
# - Missing metadata file? Create <file>.csv.meta.yaml
# - Missing required field? Add to metadata
# - Invalid value? Check schemas/raw_meta.schema.yaml for allowed values
```

## File Organization

```
data/raw/
├── _template*.csv/yaml      # Copy these as starting points
├── yourpaper_2024/          # One folder per paper (recommended)
│   ├── table1.csv
│   ├── table1.csv.meta.yaml
│   └── README.md (optional)
└── flatfile.csv             # Also works (but folders better)
    └── flatfile.csv.meta.yaml
```

## Understanding the Pipeline

1. **Raw Data** (`data/raw/`) → Always immutable source files
2. **Validation** (`validate_raw.py`) → Ensures metadata completeness
3. **Master Dataset** (`build_dataset.py`) → Normalizes to standard format
4. **Reports** (`build_reports.py`) → Detects contradictions, counts papers
5. **Paper** (`paper.qmd`) → Renders manuscript with auto-generated figures

## Key Features

✅ **Paper-key folders**: Organize multiple extractions per paper  
✅ **Anti-cherrypick**: Track rejected papers with reasons  
✅ **CI-based contradictions**: Statistical test when SE available  
✅ **Species separation**: Never mix human/rodent/primate data  
✅ **Quality flags**: Mark concerns rather than exclude data  

## Need Help?

- **Full workflow**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Protocol details**: See [protocol/PROTOCOL.md](protocol/PROTOCOL.md)
- **Implementation**: See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## Next Steps

1. ✅ Verify installation works with example data
2. 📝 Extract your first real paper
3. 🔍 Search for more candidates
4. 📊 Generate reports with contradictions
5. 📄 Render the paper with your data

Happy researching! 🧠
