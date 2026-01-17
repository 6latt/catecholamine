#!/usr/bin/env python3
"""
Demo script to showcase the paper generation pipeline.

This script demonstrates how to use the catecholamine pipeline to
automatically generate a scientific paper from unstructured research notes.
"""

import subprocess
import sys
from pathlib import Path


def print_banner(text):
    """Print a banner with text."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def main():
    """Run the demo."""
    print_banner("Catecholamine Paper Generation Demo")
    
    print("This demo will show you how to generate a scientific paper from")
    print("unstructured research notes in deepresearch.md")
    print()
    
    # Check if deepresearch.md exists
    deepresearch = Path("deepresearch.md")
    if not deepresearch.exists():
        print("❌ Error: deepresearch.md not found!")
        print("   This file should contain your comprehensive research notes.")
        return 1
    
    print(f"✓ Found deepresearch.md ({deepresearch.stat().st_size:,} bytes)")
    print()
    
    input("Press Enter to start the paper generation pipeline...")
    
    # Run the full pipeline
    print_banner("Step 1: Running Full Pipeline")
    print("This will:")
    print("  1. Validate raw data files")
    print("  2. Build master dataset")
    print("  3. Generate analysis reports")
    print("  4. Parse deepresearch.md")
    print("  5. Generate structured scientific paper")
    print("  6. Render to HTML")
    print()
    
    result = subprocess.run(
        ["python", "scripts/catecholamine_cli.py", "full", "--simple"],
        cwd=Path.cwd()
    )
    
    if result.returncode != 0:
        print("\n❌ Pipeline failed!")
        return 1
    
    # Show results
    print_banner("Success! Your Paper is Ready")
    
    output_html = Path("paper/_output/generated_paper.html")
    output_qmd = Path("paper/generated_paper.qmd")
    
    if output_html.exists():
        print(f"✓ HTML Paper: {output_html}")
        print(f"  Size: {output_html.stat().st_size:,} bytes")
    
    if output_qmd.exists():
        print(f"✓ Quarto Source: {output_qmd}")
        print(f"  Size: {output_qmd.stat().st_size:,} bytes")
    
    print()
    print("What was generated:")
    print("  • Complete scientific paper with:")
    print("    - Abstract")
    print("    - Introduction")
    print("    - Methods")
    print("    - Results (organized by cognitive domain)")
    print("    - Discussion")
    print("    - Conclusions")
    print("    - References")
    print()
    print(f"View your paper by opening: {output_html}")
    print()
    
    print_banner("Next Steps")
    print("1. Review the generated paper")
    print("2. Customize by editing scripts/generate_paper.py")
    print("3. Re-run with: python scripts/catecholamine_cli.py generate")
    print("4. For PDF output, install Quarto and run:")
    print("   cd paper && quarto render generated_paper.qmd")
    print()
    
    print("For more information, see:")
    print("  • README.md - Overview and quick start")
    print("  • PAPER_GENERATION_GUIDE.md - Detailed guide")
    print("  • STRUCTURE.md - Repository organization")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
        sys.exit(1)
