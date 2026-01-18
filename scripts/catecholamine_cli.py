#!/usr/bin/env python3
"""
Main CLI for the Catecholamine Paper Generation Pipeline.

This tool automates the process of converting raw research data and deep
research notes into structured scientific papers.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_command(cmd: list[str], description: str) -> int:
    """Run a command and print status."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, cwd=ROOT)
    
    if result.returncode != 0:
        print(f"\n✗ {description} failed with exit code {result.returncode}")
        return result.returncode
    
    print(f"\n✓ {description} completed successfully")
    return 0


def validate_data(args):
    """Validate raw data files."""
    cmd = ["python", str(SCRIPTS / "validate_raw.py")]
    return run_command(cmd, "Validating raw data")


def build_dataset(args):
    """Build the master dataset from raw data."""
    cmd = ["python", str(SCRIPTS / "build_dataset.py")]
    return run_command(cmd, "Building master dataset")


def build_reports(args):
    """Generate report tables."""
    cmd = ["python", str(SCRIPTS / "build_reports.py")]
    return run_command(cmd, "Building reports")


def generate_paper(args):
    """Generate paper from deep research."""
    cmd = ["python", str(SCRIPTS / "generate_paper.py")]
    return run_command(cmd, "Generating paper from deepresearch.md")


def render_paper(args):
    """Render the paper to HTML/PDF."""
    paper_dir = ROOT / "paper"
    output_dir = paper_dir / "_output"
    
    # Determine which file to render
    if args.source == "generated":
        qmd_file = "generated_paper.qmd"
    else:
        qmd_file = "paper.qmd"
    
    qmd_path = paper_dir / qmd_file
    if not qmd_path.exists():
        print(f"Error: {qmd_path} not found")
        return 1
    
    # Try Quarto first, fall back to simple renderer
    quarto_installed = shutil.which("quarto") is not None
    
    if quarto_installed and not getattr(args, "simple", False):
        print("\nUsing Quarto for rendering...")
        cmd = ["quarto", "render", qmd_file]
        result = subprocess.run(cmd, cwd=paper_dir)
        
        if result.returncode == 0:
            print(f"\n✓ Paper rendered successfully")
            print(f"\nOutput files in: {output_dir}")
            return 0
        else:
            print(f"\n✗ Quarto rendering failed, falling back to simple renderer")
    
    # Use simple renderer
    print("\nUsing simple HTML renderer...")
    cmd = ["python", str(SCRIPTS / "render_paper_simple.py")]
    return run_command(cmd, "Rendering paper to HTML")


def full_pipeline(args):
    """Run the full paper generation pipeline."""
    # Add default render args if not present
    if not hasattr(args, 'source'):
        args.source = 'generated'
    
    steps = [
        ("Validating data", validate_data),
        ("Building dataset", build_dataset),
        ("Building reports", build_reports),
        ("Generating paper", generate_paper),
        ("Rendering paper", render_paper),
    ]
    
    print("\n" + "="*60)
    print("  Running Full Paper Generation Pipeline")
    print("="*60)
    
    for description, func in steps:
        result = func(args)
        if result != 0 and not args.continue_on_error:
            print(f"\n✗ Pipeline stopped at: {description}")
            return result
    
    print("\n" + "="*60)
    print("  ✓ Pipeline completed successfully!")
    print("="*60)
    print(f"\nYour paper is ready in: {ROOT / 'paper' / '_output'}")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Catecholamine Research Paper Generation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the full pipeline
  %(prog)s full
  
  # Generate paper from deepresearch.md
  %(prog)s generate
  
  # Render the generated paper
  %(prog)s render --source generated
  
  # Validate and build dataset only
  %(prog)s validate
  %(prog)s build
  
  # Build reports
  %(prog)s reports
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Full pipeline
    full_parser = subparsers.add_parser('full', help='Run the complete pipeline')
    full_parser.add_argument(
        '--continue-on-error', 
        action='store_true',
        help='Continue even if a step fails'
    )
    full_parser.add_argument(
        '--simple', 
        action='store_true',
        help='Use simple HTML renderer instead of Quarto'
    )
    full_parser.set_defaults(func=full_pipeline)
    
    # Validate
    validate_parser = subparsers.add_parser('validate', help='Validate raw data')
    validate_parser.set_defaults(func=validate_data)
    
    # Build dataset
    build_parser = subparsers.add_parser('build', help='Build master dataset')
    build_parser.set_defaults(func=build_dataset)
    
    # Build reports
    reports_parser = subparsers.add_parser('reports', help='Generate report tables')
    reports_parser.set_defaults(func=build_reports)
    
    # Generate paper
    generate_parser = subparsers.add_parser('generate', help='Generate paper from deepresearch.md')
    generate_parser.set_defaults(func=generate_paper)
    
    # Render paper
    render_parser = subparsers.add_parser('render', help='Render paper to HTML/PDF')
    render_parser.add_argument(
        '--source',
        choices=['generated', 'manual'],
        default='generated',
        help='Which paper source to render (default: generated)'
    )
    render_parser.add_argument(
        '--simple',
        action='store_true',
        help='Use simple HTML renderer instead of Quarto'
    )
    render_parser.set_defaults(func=render_paper)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
