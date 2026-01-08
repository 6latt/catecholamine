# data/raw

drop extracted quantitative data here. **raw is immutable**: don't overwrite old files; add new versions with new names.

## naming convention

either:

- `data/raw/<paper_key>.csv`

or (preferred as the repo grows):

- `data/raw/<paper_key>/tables/<table_id>.csv`
- `data/raw/<paper_key>/digitized/<figure_id>.csv`

## metadata (required)

every data file needs a sibling metadata file:

- `<file>.csv.meta.yaml`

see `schemas/raw_meta.schema.yaml` for required fields.

## minimum columns

you can store raw stats however the paper reports them, but **the build step must normalize** to the standard long format (see `scripts/build_dataset.py`).

## digitizing figures

use a digitizer (e.g., webplotdigitizer) and export points to csv.
set `extraction_method: digitized` in the meta.
