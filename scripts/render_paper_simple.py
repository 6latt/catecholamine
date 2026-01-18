#!/usr/bin/env python3
"""
Simple paper renderer that converts the generated QMD to HTML without Quarto.

This is a fallback renderer for environments where Quarto is not installed.
It provides basic markdown-to-HTML conversion while preserving the structure.
"""

from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"
OUTPUT_DIR = PAPER_DIR / "_output"


def parse_qmd_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and remaining content."""
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = {}
            for line in parts[1].split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"')
            return frontmatter, parts[2]
    return {}, content


def markdown_to_html(text: str) -> str:
    """Basic markdown to HTML conversion."""
    # Headers
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold (process first to avoid conflict with italic)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Italic (avoid matching asterisks that are part of bold or other adjacent-asterisk syntax)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    
    # Lists
    lines = text.split('\n')
    output_lines = []
    in_list = False
    list_type = None
    
    for line in lines:
        if re.match(r'^\d+\.\s', line):
            # Numbered list item
            if in_list and list_type != 'ol':
                # Close previous list if it's a different type
                output_lines.append(f'</{list_type}>')
                in_list = False
            if not in_list:
                output_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            item = re.sub(r'^\d+\.\s', '', line)
            output_lines.append(f'<li>{item}</li>')
        elif line.strip().startswith('-'):
            # Bullet list item
            if in_list and list_type != 'ul':
                # Close previous list if it's a different type
                output_lines.append(f'</{list_type}>')
                in_list = False
            if not in_list:
                output_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            item = line.strip()[1:].strip()
            output_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                output_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            output_lines.append(line)
    
    if in_list:
        output_lines.append(f'</{list_type}>')
    
    text = '\n'.join(output_lines)
    
    # Paragraphs
    paragraphs = text.split('\n\n')
    output = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            output.append(f'<p>{p}</p>')
        else:
            output.append(p)
    
    return '\n\n'.join(output)


def generate_html(qmd_path: Path) -> str:
    """Convert QMD file to standalone HTML."""
    content = qmd_path.read_text()
    frontmatter, body = parse_qmd_frontmatter(content)
    
    title = frontmatter.get('title', 'Scientific Paper')
    author = frontmatter.get('author', 'Anonymous')
    
    # Remove citation markers (￼) and clean up
    body = body.replace('￼', '')
    
    html_body = markdown_to_html(body)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
        }}
        p {{
            text-align: justify;
            margin-bottom: 15px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .author {{
            font-style: italic;
            color: #666;
            margin-top: 10px;
        }}
        .date {{
            color: #888;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        strong {{
            color: #2c3e50;
        }}
        ul, ol {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #888;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="author">{author}</div>
        <div class="date">Generated: {datetime.now().strftime('%B %d, %Y')}</div>
    </div>
    
    {html_body}
    
    <div class="footer">
        <p>Generated from comprehensive research synthesis using automated paper generation pipeline.</p>
        <p>Repository: <a href="https://github.com/6latt/catecholamine">github.com/6latt/catecholamine</a></p>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """Main execution function."""
    qmd_path = PAPER_DIR / "generated_paper.qmd"
    
    if not qmd_path.exists():
        print(f"Error: {qmd_path} not found. Run generate_paper.py first.")
        return 1
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Rendering paper to HTML...")
    html = generate_html(qmd_path)
    
    output_path = OUTPUT_DIR / "generated_paper.html"
    output_path.write_text(html)
    
    print(f"✓ Paper rendered to {output_path}")
    print(f"\nTo view the paper, open:")
    print(f"  {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())
