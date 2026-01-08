# ingestion notes (how we add sources)

goal: get **numbers**.

## preferred order
1) supplementary csv/xlsx provided by the paper
2) tables in the paper (copy into csv)
3) digitize plots (webplotdigitizer) only when 1/2 unavailable

## for every raw file
create a twin `.meta.yaml` next to it with:
- citation_key
- species + population (ADHD / MDD / GAD / ASD / control)
- task_domain + task_name
- biomarker_type (pfc dopamine, d1 binding, net binding, pupil baseline, etc)
- units + transformations
- extraction_method (supplement / table / digitized)
- caveats

## digitizing plots
- store the digitized points as csv in `data/raw/`
- store a screenshot of the source figure in `data/raw/_figures/`
- record axis calibration + any smoothing in the meta file
