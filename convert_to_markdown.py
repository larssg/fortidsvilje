#!/usr/bin/env python3
"""Convert plain text chapters to Markdown for Pandoc EPUB generation."""

import re
from pathlib import Path

def parse_chapter(filepath: Path) -> dict:
    """Parse a chapter file and extract metadata."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.strip().split('\n')

    # Initialize
    title = None
    location = None
    date = None
    body_start = 0

    # Parse header lines
    i = 0
    while i < len(lines) and i < 10:
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Check for chapter title
        if line.startswith('CHAPTER') or line == 'PROLOGUE' or line == 'EPILOGUE':
            title = line
            i += 1
            continue

        # Check for location (all caps)
        if line.isupper() and not line.startswith('CHAPTER'):
            if re.match(r'^[A-Z][A-Z\s,]+$', line) and not re.match(r'^\d{4}$', line):
                if any(c.isalpha() for c in line):
                    location = line.title()
                    i += 1
                    continue

        # Check for date
        if re.match(r'^(19|20)\d{2}$', line) or re.match(r'^[A-Z][a-z]+ \d{4}$', line):
            date = line
            i += 1
            continue

        if line and not line.isupper():
            break

        i += 1

    # Skip empty lines after headers
    while i < len(lines) and not lines[i].strip():
        i += 1

    body_start = i
    body_lines = lines[body_start:]
    body = '\n'.join(body_lines)

    return {
        'title': title,
        'location': location,
        'date': date,
        'body': body
    }

def convert_body(body: str) -> str:
    """Convert body text to Markdown format."""
    # Split into paragraphs
    paragraphs = re.split(r'\n\n+', body)

    result = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Check for scene breaks
        if re.match(r'^[\*\-\s]+$', para) or para in ['***', '* * *']:
            result.append('\n* * *\n')
            continue

        # Join lines within a paragraph
        para = ' '.join(para.split('\n'))
        para = re.sub(r'\s+', ' ', para)

        result.append(para)

    return '\n\n'.join(result)

def convert_chapter(input_path: Path) -> str:
    """Convert a single chapter file to Markdown."""
    parsed = parse_chapter(input_path)

    parts = []

    # Handle prologue file without explicit PROLOGUE header
    if 'prologue' in input_path.stem.lower() and not parsed['title']:
        parsed['title'] = 'PROLOGUE'

    # Chapter heading with location and year
    if parsed['title']:
        # Build location/date suffix
        suffix_parts = []
        if parsed['location']:
            suffix_parts.append(parsed['location'])
        if parsed['date']:
            suffix_parts.append(parsed['date'])
        suffix = f" — {', '.join(suffix_parts)}" if suffix_parts else ""

        if parsed['title'] == 'PROLOGUE':
            parts.append(f'# Prologue{suffix}')
        elif parsed['title'] == 'EPILOGUE':
            parts.append(f'# Epilogue{suffix}')
        else:
            # Extract chapter number
            match = re.match(r'CHAPTER\s+(\d+)', parsed['title'])
            if match:
                parts.append(f"# Chapter {match.group(1)}{suffix}")
            else:
                parts.append(f"# {parsed['title'].title()}{suffix}")

    parts.append('')

    # Body
    body = convert_body(parsed['body'])
    parts.append(body)

    return '\n'.join(parts)

def main():
    base_dir = Path(__file__).parent
    input_dir = base_dir / 'chapters_english'
    output_dir = base_dir / 'chapters_md'

    output_dir.mkdir(exist_ok=True)

    # Get all chapter files
    chapter_files = sorted(input_dir.glob('*.txt'))

    for input_path in chapter_files:
        output_name = input_path.stem + '.md'
        output_path = output_dir / output_name

        markdown = convert_chapter(input_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"Converted: {input_path.name} -> {output_name}")

    print(f"\nConverted {len(chapter_files)} chapters to {output_dir}")

if __name__ == '__main__':
    main()
