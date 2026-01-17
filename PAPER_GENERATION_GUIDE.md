# Paper Generation Guide

This guide explains how to use the catecholamine pipeline to generate scientific papers from unstructured research notes.

## Overview

The paper generation system converts comprehensive research notes (like those in `deepresearch.md`) into properly structured scientific papers with:
- Abstract
- Introduction
- Methods
- Results (organized by domain)
- Discussion
- Conclusions
- References

## Input: deepresearch.md

Your research notes should contain:
1. **Comprehensive literature review content** organized by topics
2. **Quantitative findings** with effect sizes (e.g., "SMD ≈ +0.24", "d = 0.5")
3. **Citations** with author names and years
4. **Domain sections** covering different aspects of your research

Example structure:
```markdown
Introduction and Key Concepts

[Your introduction text with citations]

Attention and Attentional Control

[Research findings on attention with effect sizes and citations]

Working Memory (WM) and Executive Control

[Research findings on working memory]

...

References and Sources
• Author et al. (2022). Title of paper
• Another Author (2021). Another paper
```

## Output: Structured Scientific Paper

The generator produces:
1. **generated_paper.qmd** - A Quarto markdown document with proper structure
2. **generated_paper.html** - Rendered HTML version (via simple renderer)
3. **references.bib** - BibTeX bibliography (if needed)

## Usage

### Option 1: Full Pipeline (Recommended)

Run everything at once:
```bash
python scripts/catecholamine_cli.py full --simple
```

This will:
1. ✓ Validate raw data files
2. ✓ Build master dataset
3. ✓ Generate reports
4. ✓ Parse deepresearch.md and create scientific paper
5. ✓ Render to HTML

### Option 2: Step-by-Step

Generate the paper only:
```bash
# Generate the paper structure
python scripts/generate_paper.py

# Render to HTML
python scripts/render_paper_simple.py

# Or with Quarto (if installed)
cd paper
quarto render generated_paper.qmd
```

### Option 3: Using the CLI

```bash
# Generate paper from deepresearch.md
python scripts/catecholamine_cli.py generate

# Render the generated paper
python scripts/catecholamine_cli.py render --source generated
```

## Customization

### Modifying the Paper Structure

Edit `scripts/generate_paper.py` to customize:
- Abstract generation (`generate_abstract`)
- Section organization (`generate_results_section`)
- Discussion synthesis (`generate_discussion`)
- Citation extraction (`extract_citations`)

### Adding New Sections

To add new result sections, update the `key_sections` list in `generate_paper_qmd`:
```python
key_sections = [
    'Attention and Attentional Control',
    'Working Memory (WM) and Executive Control',
    'Your New Section Name',  # Add here
    ...
]
```

### Styling the Output

For HTML output, modify the CSS in `scripts/render_paper_simple.py` in the `generate_html` function.

## Advanced Features

### Effect Size Extraction

The generator automatically extracts effect sizes from patterns like:
- `SMD ≈ +0.24`
- `Cohen's d = 0.5`
- `effect size of 0.62`
- `(d = 0.41)`

These are catalogued in the `findings` dictionary.

### Citation Management

Citations are extracted from:
1. Author-year patterns: `Weber et al. (2022)`
2. Reference section bullets
3. Inline citation markers

For proper BibTeX generation, ensure your references section follows this format:
```
References and Sources
• Author et al. (YEAR). Title of the study
• Another Author (YEAR). Another title
```

### Rendering Options

**Simple HTML Renderer** (no dependencies):
- Fast
- Works anywhere
- Basic styling
- Good for quick previews

**Quarto Renderer** (requires Quarto installation):
- Professional PDF/HTML output
- Advanced formatting
- Citation management
- Cross-references and figure numbering

## Troubleshooting

### Missing Sections

If sections aren't appearing, check:
1. Section headers in `deepresearch.md` match exactly
2. Headers are capitalized properly
3. No extra whitespace or formatting

### Citations Not Working

Ensure your references section includes:
- Author names with proper capitalization
- Four-digit years in parentheses
- Consistent bullet format

### Empty Output

Run with verbose output to diagnose:
```bash
python scripts/generate_paper.py
# Check the console output for section counts
```

## Examples

### Minimal deepresearch.md

```markdown
Introduction and Key Concepts

Dopamine and norepinephrine are critical neurotransmitters. 
A meta-analysis (Smith et al., 2022) found effect sizes of d = 0.5 
for working memory improvements.

Attention and Attentional Control

Studies show that ADHD involves attention deficits. Stimulant 
medications improve attention with SMD ≈ +0.62 (Jones et al., 2021).

References and Sources
• Smith et al. (2022). Meta-analysis of dopamine effects
• Jones et al. (2021). Stimulants in ADHD treatment
```

Running the generator will produce a complete scientific paper with abstract, methods, results, discussion, and conclusions.

## Next Steps

1. **Review the generated paper** in `paper/generated_paper.qmd`
2. **Customize sections** by editing the generator script
3. **Add visualizations** by integrating with the data pipeline
4. **Render to PDF** using Quarto for publication-ready output

## Tips for Best Results

1. **Be comprehensive** in your deepresearch.md - more content = better paper
2. **Include effect sizes** - the generator extracts and highlights these
3. **Organize by domain** - clear sections help structure the results
4. **Cite liberally** - more citations = better reference extraction
5. **Use consistent formatting** - helps the parser identify sections

## Integration with Data Pipeline

The paper generator works alongside the quantitative data pipeline:

```bash
# Process quantitative data
python scripts/validate_raw.py
python scripts/build_dataset.py
python scripts/build_reports.py

# Generate narrative paper
python scripts/generate_paper.py

# Combine both in the final paper
quarto render paper/paper.qmd  # Includes data analysis
quarto render paper/generated_paper.qmd  # Pure narrative synthesis
```

You can merge both approaches by:
1. Generating the narrative paper
2. Adding data analysis sections from the quantitative pipeline
3. Creating a unified manuscript

See `paper/paper.qmd` for an example of integrating both approaches.
