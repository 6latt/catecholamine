# protocol (anti-cherrypick)

this repo is built to **avoid cherry-picking** by forcing a paper-by-paper log of what was extracted, how it was extracted, and what was excluded.

## scope

we're building quantitative datasets that relate catecholamine biology (dopamine + norepinephrine systems) to:

- attention / sustained attention / vigilance
- working memory
- cognitive flexibility (set shifting / reversal)
- salience processing (phasic vs tonic; network switching)
- mood / motivation / anhedonia

we keep **species** separate (human vs animal vs in vitro), and we tag population (adhd / asd / mdd / anxiety / schizophrenia / control, etc.).

## inclusion rules (v0)

include a study if it has at least one of:

1) quantitative outcome + manipulation or measurement of DA/NE tone (drug, stress, genotype, PET, microdialysis, receptor density, etc.)
2) enough summary statistics to compute an effect size (or the paper already reports an effect size)

exclude if:

- outcome isn't interpretable (no task definition / no metric)
- no usable quantitative results (and figures aren't digitizable)

## extraction rules

- prefer tables/supplemental csvs over figure digitization.
- if digitizing a figure, store digitized points as `data/raw/<paper_key>/digitized/<figure_id>.csv` and set `extraction_method: digitized`.
- never delete “bad” results; mark them with `quality_flags`.

## required metadata per raw file

every raw dataset must have a `.meta.yaml` with:

- citation (doi/pmid if possible)
- species + population
- task domain + task name
- outcome and units
- manipulation/measurement description
- extraction method and notes

see `schemas/raw_meta.schema.yaml`.

## reproducibility

- all derived datasets must be rebuildable from `data/raw/` using `scripts/build_dataset.py`.
- figures in the paper are generated from code (no manual figure editing).
