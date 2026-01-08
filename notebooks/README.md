# Notebooks

This directory contains exploratory analysis notebooks for the catecholamine research project.

## File Format

Notebooks are stored as Python files using [jupytext](https://jupytext.readthedocs.io/) in the `py:percent` format. This approach:

- Makes notebooks more git-friendly (better diffs)
- Allows running notebooks as scripts
- Keeps the exploratory nature while maintaining reproducibility

## Converting to Jupyter Notebooks

To open as a Jupyter notebook:

```bash
# Install jupytext if not already installed
pip install jupytext

# Pair with notebook format
jupytext --set-formats py:percent,ipynb notebook_name.py
```

Or open the `.py` files directly in Jupyter Lab/Notebook with the jupytext extension installed.

## Running Notebooks

### As Python Script
```bash
python notebooks/01_explore_inverted_u.py
```

### As Jupyter Notebook
Open in Jupyter Lab/Notebook with jupytext extension enabled.

## Notebook Organization

- Prefix notebooks with numbers for ordering (01_, 02_, etc.)
- Use descriptive names that indicate the analysis focus
- Keep notebooks focused on specific questions or explorations
- For production analysis, move code to `src/catecholamine/` modules

## Example Notebooks

- `01_explore_inverted_u.py` - Exploratory analysis of inverted-U relationships

## Best Practices

- Load data from `data/derived/` for consistency
- Save figures to `figures/` directory
- Document key findings in comments
- For paper-ready analysis, use Quarto documents in `paper/`
