#!/usr/bin/env python3
"""Generate audiobook from chapter text files using Piper TTS."""

import subprocess
import re
from pathlib import Path

# Configuration
PIPER_PATH = Path.home() / "Library/Python/3.9/bin/piper"
VOICE_MODEL = Path(__file__).parent / "voices/en_US-lessac-medium.onnx"
INPUT_DIR = Path(__file__).parent / "chapters_english"
OUTPUT_DIR = Path(__file__).parent / "dist/audiobook"


def clean_text_for_tts(text: str) -> str:
    """Clean text for better TTS output."""
    # Remove chapter headers (they'll be announced separately)
    lines = text.strip().split('\n')

    # Skip header lines (CHAPTER X, location, date)
    body_start = 0
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        if not line:
            continue
        # Skip chapter title, location (all caps), and date lines
        if (line.startswith('CHAPTER') or
            line == 'PROLOGUE' or
            line == 'EPILOGUE' or
            (line.isupper() and any(c.isalpha() for c in line)) or
            re.match(r'^(19|20)\d{2}$', line) or
            re.match(r'^[A-Z][a-z]+ \d{4}$', line)):
            body_start = i + 1
            continue
        break

    # Skip empty lines after headers
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    body = '\n'.join(lines[body_start:])

    # Clean up text
    # Replace em-dashes with pauses
    body = body.replace('—', ' — ')

    # Ensure proper sentence spacing
    body = re.sub(r'\s+', ' ', body)

    # Add pauses after paragraphs (double newline -> period + pause marker)
    paragraphs = re.split(r'\n\n+', body)
    body = '\n\n'.join(p.strip() for p in paragraphs if p.strip())

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

    # Handle prologue without explicit title
    if 'prologue' in filepath.stem.lower() and not title:
        title = 'Prologue'

    return {'title': title, 'location': location, 'date': date}


def generate_chapter_audio(chapter_path: Path, output_path: Path):
    """Generate audio for a single chapter."""
    # Parse header for announcement
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

    # Get chapter body
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()

    body = clean_text_for_tts(content)

    # Combine announcement and body
    full_text = announcement + body

    # Generate audio with piper
    print(f"Generating: {output_path.name}...")

    process = subprocess.run(
        [str(PIPER_PATH), '--model', str(VOICE_MODEL), '--output_file', str(output_path)],
        input=full_text.encode('utf-8'),
        capture_output=True
    )

    if process.returncode != 0:
        print(f"  Error: {process.stderr.decode()}")
        return False

    return True


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get all chapter files
    chapter_files = sorted(INPUT_DIR.glob('*.txt'))

    print(f"Generating audiobook from {len(chapter_files)} chapters...")
    print(f"Using voice: {VOICE_MODEL.name}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    for chapter_path in chapter_files:
        output_name = chapter_path.stem + '.wav'
        output_path = OUTPUT_DIR / output_name
        generate_chapter_audio(chapter_path, output_path)

    print()
    print(f"Done! Generated {len(chapter_files)} audio files in {OUTPUT_DIR}")
    print()
    print("To combine into a single file, you can use ffmpeg:")
    print("  ffmpeg -f concat -safe 0 -i filelist.txt -c copy audiobook.wav")


if __name__ == '__main__':
    main()
