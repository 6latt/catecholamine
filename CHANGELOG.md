# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-08

### Added
- Initial repository setup
- Extracted and organized catecholamine research repository structure
- Added comprehensive documentation:
  - README.md with project overview and workflow
  - CONTRIBUTING.md with contribution guidelines
  - STRUCTURE.md with project organization details
  - LICENSE (MIT)
- Added Python package configuration (pyproject.toml)
- Added .gitignore for Python, data, and IDE files
- Included core pipeline scripts:
  - validate_raw.py - Data validation
  - build_dataset.py - Dataset building
  - build_reports.py - Report generation
- Included research protocol documentation
- Included data schemas for validation
- Included example datasets and metadata
- Included paper template (Quarto)
- Verified all dependencies install correctly
- Verified all pipeline scripts run successfully

### Repository Structure
- `data/` - Raw and derived datasets
- `scripts/` - Pipeline and utility scripts
- `src/catecholamine/` - Core Python package
- `paper/` - Manuscript and related files
- `protocol/` - Research methodologies
- `schemas/` - Data validation schemas
- `notebooks/` - Exploratory analysis
- `figures/` - Generated figures
- `reports/` - Generated reports
- `refs/` - Bibliography

[0.1.0]: https://github.com/6latt/catecholamine/releases/tag/v0.1.0
