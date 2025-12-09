#!/usr/bin/env python3
"""Convert plain text chapters to Typst format."""

import re
import os
from pathlib import Path

def escape_typst(text: str) -> str:
    """Escape special Typst characters."""
    # Escape characters that have special meaning in Typst
    text = text.replace('\\', '\\\\')
    text = text.replace('#', '\\#')
    text = text.replace('$', '\\$')
    text = text.replace('@', '\\@')
    text = text.replace('<', '\\<')
    text = text.replace('>', '\\>')
    text = text.replace('[', '\\[')
    text = text.replace(']', '\\]')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('*', '\\*')
    text = text.replace('_', '\\_')
    text = text.replace('`', '\\`')
    # Keep em-dashes as-is (—)
    return text

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
    while i < len(lines) and i < 10:  # Only check first 10 lines for headers
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # Check for chapter title (CHAPTER X or PROLOGUE)
        if line.startswith('CHAPTER') or line == 'PROLOGUE' or line == 'EPILOGUE':
            title = line
            i += 1
            continue

        # Check for location (all caps, possibly with comma)
        if line.isupper() and not line.startswith('CHAPTER'):
            # Could be location or date
            if re.match(r'^[A-Z][A-Z\s,]+$', line) and not re.match(r'^\d{4}$', line):
                if any(c.isalpha() for c in line):
                    location = line.title()  # Convert to title case
                    i += 1
                    continue

        # Check for date (year like 1944, 2019, or month/date patterns)
        if re.match(r'^(19|20)\d{2}$', line) or re.match(r'^[A-Z][a-z]+ \d{4}$', line):
            date = line
            i += 1
            continue

        # If we hit regular text, we're done with headers
        if line and not line.isupper():
            break

        i += 1

    # Find where the actual body starts (skip empty lines after headers)
    while i < len(lines) and not lines[i].strip():
        i += 1

    body_start = i

    # Get body content
    body_lines = lines[body_start:]
    body = '\n'.join(body_lines)

    return {
        'title': title,
        'location': location,
        'date': date,
        'body': body
    }

def convert_body(body: str) -> str:
    """Convert body text to Typst format."""
    # Escape special characters first
    body = escape_typst(body)

    # Split into paragraphs
    paragraphs = re.split(r'\n\n+', body)

    result = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Check for scene breaks (lines of just asterisks or dashes)
        if re.match(r'^[\*\-\s\\]+$', para) or para in ['\\*\\*\\*', '\\* \\* \\*']:
            result.append('#scenebreak')
            continue

        # Join lines within a paragraph
        para = ' '.join(para.split('\n'))
        para = re.sub(r'\s+', ' ', para)

        result.append(para)

    return '\n\n'.join(result)

def convert_chapter(input_path: Path, output_path: Path):
    """Convert a single chapter file."""
    parsed = parse_chapter(input_path)

    # Build the Typst chapter
    parts = ['#import "../template.typ": chapter, scenebreak, letter', '', '#chapter(']

    if parsed['title']:
        # Escape quotes in title
        safe_title = parsed['title'].replace('"', '\\"')
        parts.append(f'  title: "{safe_title}",')
    else:
        parts.append('  title: none,')

    if parsed['location']:
        safe_location = parsed['location'].replace('"', '\\"')
        parts.append(f'  location: "{safe_location}",')
    else:
        parts.append('  location: none,')

    if parsed['date']:
        safe_date = parsed['date'].replace('"', '\\"')
        parts.append(f'  date: "{safe_date}",')
    else:
        parts.append('  date: none,')

    parts.append(')[')

    # Add body
    body = convert_body(parsed['body'])
    parts.append(body)

    parts.append(']')

    output = '\n'.join(parts)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Converted: {input_path.name} -> {output_path.name}")

def main():
    base_dir = Path(__file__).parent
    input_dir = base_dir / 'chapters_english_revised'
    output_dir = base_dir / 'chapters_typ'

    output_dir.mkdir(exist_ok=True)

    # Get all chapter files
    chapter_files = sorted(input_dir.glob('*.txt'))

    for input_path in chapter_files:
        output_name = input_path.stem + '.typ'
        output_path = output_dir / output_name
        convert_chapter(input_path, output_path)

    print(f"\nConverted {len(chapter_files)} chapters to {output_dir}")

if __name__ == '__main__':
    main()
