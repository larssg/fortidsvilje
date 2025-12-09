#!/usr/bin/env python3
"""Generate audiobook from chapter text files using Coqui TTS."""

import subprocess
import re
from pathlib import Path

# Configuration
TTS_PATH = Path.home() / "Library/Python/3.9/bin/tts"
MODEL = "tts_models/en/vctk/vits"
SPEAKER = "p283"
INPUT_DIR = Path(__file__).parent / "chapters_english"
OUTPUT_DIR = Path(__file__).parent / "dist/audiobook_coqui"


def clean_text_for_tts(text: str) -> str:
    """Clean text for better TTS output."""
    lines = text.strip().split('\n')

    # Skip header lines (CHAPTER X, location, date)
    body_start = 0
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        if not line:
            continue
        if (line.startswith('CHAPTER') or
            line == 'PROLOGUE' or
            line == 'EPILOGUE' or
            (line.isupper() and any(c.isalpha() for c in line)) or
            re.match(r'^(19|20)\d{2}$', line) or
            re.match(r'^[A-Z][a-z]+ \d{4}$', line)):
            body_start = i + 1
            continue
        break

    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    body = '\n'.join(lines[body_start:])

    # Split into paragraphs and rejoin
    paragraphs = re.split(r'\n\n+', body)
    body = '\n\n'.join(p.strip() for p in paragraphs if p.strip())

    # Clean up text - collapse whitespace first, then handle em-dashes
    body = re.sub(r'\s+', ' ', body)
    # Replace em-dash with comma for a natural pause
    body = body.replace('—', ', ')

    return body


def parse_chapter_header(filepath: Path) -> dict:
    """Extract chapter metadata for announcement."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.strip().split('\n')

    title = None
    location = None
    date = None

    for line in lines[:10]:
        line = line.strip()
        if not line:
            continue

        if line.startswith('CHAPTER') or line == 'PROLOGUE' or line == 'EPILOGUE':
            title = line.title()
        elif line.isupper() and any(c.isalpha() for c in line) and not line.startswith('CHAPTER'):
            location = line.title()
        elif re.match(r'^(19|20)\d{2}$', line) or re.match(r'^[A-Z][a-z]+ \d{4}$', line):
            date = line

    if 'prologue' in filepath.stem.lower() and not title:
        title = 'Prologue'

    return {'title': title, 'location': location, 'date': date}


def generate_chapter_audio(chapter_path: Path, output_path: Path):
    """Generate audio for a single chapter."""
    header = parse_chapter_header(chapter_path)

    # Build announcement text
    announcement_parts = []
    if header['title']:
        announcement_parts.append(header['title'])
    if header['location']:
        announcement_parts.append(header['location'])
    if header['date']:
        announcement_parts.append(header['date'])

    announcement = '. '.join(announcement_parts) + '.\n\n'

    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()

    body = clean_text_for_tts(content)
    full_text = announcement + body

    print(f"Generating: {output_path.name}...")

    process = subprocess.run(
        [
            str(TTS_PATH),
            '--text', full_text,
            '--model_name', MODEL,
            '--speaker_idx', SPEAKER,
            '--out_path', str(output_path)
        ],
        capture_output=True,
        text=True
    )

    if process.returncode != 0:
        print(f"  Error: {process.stderr}")
        return False

    return True


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chapter_files = sorted(INPUT_DIR.glob('*.txt'))

    print(f"Generating audiobook from {len(chapter_files)} chapters...")
    print(f"Using model: {MODEL}, speaker: {SPEAKER}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    for chapter_path in chapter_files:
        output_name = chapter_path.stem + '.wav'
        output_path = OUTPUT_DIR / output_name
        generate_chapter_audio(chapter_path, output_path)

    print()
    print(f"Done! Generated {len(chapter_files)} audio files in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
