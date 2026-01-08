# Contributing to Catecholamine Research

Thank you for your interest in contributing to this research repository!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up your development environment (see README.md)
4. Create a new branch for your contribution

## Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Contributing Data

### Adding Raw Data

All raw data must follow the data provenance rules outlined in `protocol/PROTOCOL.md`:

1. Place raw data files in `data/raw/`
2. Create a companion `.meta.yaml` file for each data file
3. Follow the schema defined in `schemas/raw_meta.schema.yaml`
4. Run validation: `python scripts/validate_raw.py`

### Data Quality

- Never edit raw data in place
- Document extraction methods clearly
- Include all relevant metadata
- Mark questionable data with quality flags

## Code Contributions

### Scripts and Analysis

- Keep scripts modular and well-documented
- Follow existing code style
- Add comments for complex logic
- Test your scripts before submitting

### Paper Contributions

- Use Quarto for narrative documents (`.qmd`)
- Keep code and narrative together
- Ensure all figures are generated from code
- Maintain citation integrity in `refs/references.bib`

## Pull Request Process

1. Ensure your code passes validation scripts
2. Update documentation as needed
3. Describe your changes clearly in the PR
4. Link to any relevant issues

## Research Ethics

- Ensure all data sources are properly cited
- Follow anti-cherry-picking protocols
- Document inclusion/exclusion decisions
- Maintain reproducibility standards

## Questions?

Open an issue for questions or discussions about the research protocol or contribution process.
