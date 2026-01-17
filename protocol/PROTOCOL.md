# Research Protocol

## Anti-Cherry-Picking Approach

This repository is designed to prevent cherry-picking by maintaining a comprehensive, paper-by-paper log that documents:
- What data was extracted
- How extraction was performed
- What was excluded and why

## Research Scope

This project builds quantitative datasets relating catecholamine biology (dopamine and norepinephrine systems) to cognitive and affective domains:

- Attention, sustained attention, and vigilance
- Working memory
- Cognitive flexibility (set shifting and reversal learning)
- Salience processing (phasic vs tonic activity, network switching)
- Mood, motivation, and anhedonia

Data is organized by **species** (human, animal model, in vitro) and tagged by **population** (ADHD, ASD, MDD, anxiety, schizophrenia, control, etc.).

## Inclusion Criteria (Version 0)

Include a study if it meets at least one of these criteria:

1. **Quantitative Outcome:** Study reports quantitative behavioral or cognitive outcomes with manipulation or measurement of dopamine/norepinephrine tone (drug intervention, stress, genotype, PET imaging, microdialysis, receptor density measurements, etc.)

2. **Effect Size Data:** Study provides sufficient summary statistics to compute an effect size, or reports effect sizes directly

### Exclusion Criteria

Exclude studies if:
- Outcome measures are not interpretable (no task definition or measurement metric)
- No usable quantitative results are available and figures cannot be reliably digitized

## Data Extraction Rules

- **Preference:** Use tables and supplementary CSV files over figure digitization when available
- **Figure Digitization:** When digitizing figures, store data as `data/raw/<paper_key>/digitized/<figure_id>.csv` and set `extraction_method: digitized` in metadata
- **Quality Control:** Never delete questionable results; instead, mark them with `quality_flags` in the metadata

## Required Metadata

Every raw dataset file must have an accompanying `.meta.yaml` file containing:

- Citation information (DOI or PMID when available)
- Species and population details
- Task domain and task name
- Outcome measures and units
- Manipulation or measurement description
- Extraction method and relevant notes

Refer to `schemas/raw_meta.schema.yaml` for the complete specification.

## Reproducibility Standards

- **Derived Datasets:** All derived datasets must be rebuildable from `data/raw/` using `scripts/build_dataset.py`
- **Figures:** All figures in manuscripts must be generated from code (no manual figure editing permitted)
