#!/usr/bin/env python3
"""
Example: How to use the paper generation API programmatically.

This shows how to use the paper generation functions in your own scripts.
"""

from pathlib import Path
import sys

# Add the scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate_paper import parse_deepresearch, generate_paper_qmd


def main():
    """Example of programmatic paper generation."""
    print("Example: Programmatic Paper Generation\n")
    
    # 1. Parse the deepresearch.md file
    print("Step 1: Parsing deepresearch.md...")
    data = parse_deepresearch()
    
    print(f"  ✓ Found {len(data['sections'])} sections")
    print(f"  ✓ Extracted {len(data['findings'])} findings")
    print(f"  ✓ Identified {len(data['citations'])} citations")
    
    # 2. Access specific sections
    print("\nStep 2: Accessing parsed data...")
    print(f"  Available sections:")
    for section_name in data['sections'].keys():
        print(f"    - {section_name}")
    
    # 3. Access findings with effect sizes
    print(f"\nStep 3: Effect sizes found:")
    for i, finding in enumerate(data['findings'][:3], 1):
        print(f"  {i}. Effect size = {finding['effect_size']}")
        print(f"     Context: {finding['context'][:80]}...")
    
    # 4. Generate paper
    print("\nStep 4: Generating paper...")
    paper_content = generate_paper_qmd(data)
    
    # 5. Show paper structure
    lines = paper_content.split('\n')
    headers = [line for line in lines if line.startswith('##')]
    print(f"  ✓ Generated paper with {len(headers)} sections:")
    for header in headers[:10]:  # Show first 10
        print(f"    {header}")
    
    print("\n✓ Example complete!")
    print("\nYou can now:")
    print("  - Modify sections programmatically")
    print("  - Add custom analysis")
    print("  - Integrate with data pipelines")
    print("  - Customize paper structure")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
