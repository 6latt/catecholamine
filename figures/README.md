# Figures

This directory contains generated figures for the paper and reports.

## Important Notes

- **Do not commit** generated figures to the repository
- All figures should be generated from code using the scripts in `scripts/` or from the paper document
- Figures are automatically created when running the paper rendering or report generation scripts

## Generating Figures

Figures are generated through:

1. **Report generation**: `python scripts/build_reports.py`
2. **Paper rendering**: `quarto render paper/paper.qmd`
3. **Exploratory notebooks**: Run notebooks in `notebooks/` directory

## File Naming Convention

Use descriptive names that indicate the figure content:
- `inverted_u_curve.png`
- `task_performance_by_dose.png`
- `effect_sizes_comparison.png`

Include date/version if generating multiple iterations:
- `results_20260108.png`
