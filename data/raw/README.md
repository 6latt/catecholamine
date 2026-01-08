# data/raw

drop extracted quantitative data here. **raw is immutable**: don't overwrite old files; add new versions with new names.

## naming convention

### Flat structure (simple, for small repos):
- `data/raw/<paper_key>.csv`
- `data/raw/<paper_key>.csv.meta.yaml`

### Paper-key folder structure (preferred as the repo grows):
- `data/raw/<paper_key>/` - One folder per paper
  - `<paper_key>/table1.csv` (and `table1.csv.meta.yaml`)
  - `<paper_key>/table2.csv` (and `table2.csv.meta.yaml`)
  - `<paper_key>/digitized_fig3a.csv` (and `digitized_fig3a.csv.meta.yaml`)
  - `<paper_key>/README.md` (optional notes about this paper's extraction)

Both structures are supported. The validation and build scripts recursively search all subdirectories.

## metadata (required)

every data file needs a sibling metadata file:

- `<file>.csv.meta.yaml`

Example: if you have `weber2022/table3.csv`, you need `weber2022/table3.csv.meta.yaml`

see `schemas/raw_meta.schema.yaml` for required fields.

## templates

Use the provided templates as starting points:
- `_template_extraction.csv` - Example data format
- `_template.meta.yaml` - Complete metadata template with all fields documented

(Files prefixed with underscore are excluded from validation and processing)

## minimum columns

you can store raw stats however the paper reports them, but **the build step must normalize** to the standard long format (see `scripts/build_dataset.py`).

## digitizing figures

use a digitizer (e.g., webplotdigitizer) and export points to csv.
set `extraction_method: digitized` in the meta.
