# catecholamine / pfc performance research repo

this is a reproducible pipeline to:
- collect + normalize quantitative findings from papers (tables, supplementary csv, digitized curves)
- analyze across axes (attention, wm, flexibility, salience, mood)
- render a real paper with citations and auto-generated figures

## tldr workflow
1) put **raw** extracted numbers in `data/raw/` (csv/tsv). never edit in-place.
2) for every raw file, add a sibling metadata file: `<file>.csv.meta.yaml`.
3) run `python scripts/validate_raw.py` (fast sanity guardrail).
4) run `python scripts/build_dataset.py` to produce `data/derived/master_dataset.parquet`.
5) run `python scripts/build_reports.py` to generate `reports/*.csv` used by the paper.
6) render the paper with quarto (`paper/paper.qmd`).

## is jupyter outdated?
no. it’s still the default for exploratory analysis.

but for a *paper* you want something that:
- renders cleanly to html/pdf
- keeps code + narrative together
- gives stable citations + figure numbering
- diff/merge-friendly in git

**recommended:** quarto (`.qmd`) + a python kernel.
- you can still use notebooks for exploration.
- the paper is a quarto document that calls your real analysis code.

## setup (python)
use whatever you like (uv/poetry/conda). minimal pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## rendering the paper
install quarto (system install), then:

```bash
quarto render paper/paper.qmd
```

outputs land in `paper/_output/`.

## data provenance rules (important)
- every dataset file must have a twin metadata file next to it, e.g.
  - `data/raw/weber2022_table3.csv`
  - `data/raw/weber2022_table3.csv.meta.yaml`
- the meta file should include: paper citation key, population/species, task, units, extraction method (table vs digitized vs supp), and any caveats.

## citation workflow
- keep bibtex in `refs/references.bib`
- cite in quarto as `@weber2022_invertedu`.

(ideal: zotero + better bibtex exporting to that file, but you can also hand-maintain it.)

## what’s already included
a starter dataset + scripts + a paper skeleton. replace/extend with your own sources.
