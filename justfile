# Justfile for "The Will of the Past" by Knud Sehested

# Default recipe - build both formats
default: build

# Build both PDF and EPUB
build: pdf epub

# Build paperback PDF with Typst
pdf:
    typst compile book.typ dist/typst/book.pdf
    @echo "Built: dist/typst/book.pdf"

# Build EPUB with Pandoc
epub: markdown
    pandoc metadata.yaml \
        chapters_md/00_prologue.md \
        chapters_md/01_chapter.md \
        chapters_md/02_chapter.md \
        chapters_md/03_chapter.md \
        chapters_md/04_chapter.md \
        chapters_md/05_chapter.md \
        chapters_md/06_chapter.md \
        chapters_md/07_chapter.md \
        chapters_md/08_chapter.md \
        chapters_md/09_chapter.md \
        chapters_md/10_chapter.md \
        chapters_md/11_chapter.md \
        chapters_md/12_chapter.md \
        chapters_md/13_chapter.md \
        chapters_md/14_chapter.md \
        chapters_md/15_chapter.md \
        chapters_md/16_chapter.md \
        chapters_md/17_chapter.md \
        chapters_md/18_chapter.md \
        chapters_md/19_chapter.md \
        chapters_md/20_chapter.md \
        chapters_md/21_chapter.md \
        chapters_md/22_chapter.md \
        chapters_md/23_chapter.md \
        chapters_md/24_chapter.md \
        chapters_md/25_chapter.md \
        chapters_md/26_chapter.md \
        chapters_md/27_chapter.md \
        chapters_md/28_chapter.md \
        chapters_md/29_chapter.md \
        -o dist/pandoc/book.epub \
        --toc \
        --toc-depth=1 \
        --split-level=1
    @echo "Built: dist/pandoc/book.epub"

# Convert source chapters to Typst format
typst-chapters:
    python3 convert_chapters.py

# Convert source chapters to Markdown format
markdown:
    python3 convert_to_markdown.py

# Convert all chapter formats
convert: typst-chapters markdown

# Watch Typst for changes and auto-recompile
watch:
    typst watch book.typ dist/typst/book.pdf

# Clean generated files
clean:
    rm -rf dist/typst/* dist/pandoc/*
    @echo "Cleaned dist folders"

# Clean all generated files including intermediate formats
clean-all: clean
    rm -rf chapters_typ/* chapters_md/*
    @echo "Cleaned all generated files"

# Open the PDF
open-pdf:
    open dist/typst/book.pdf

# Open the EPUB
open-epub:
    open dist/pandoc/book.epub

# Open both outputs
open: open-pdf open-epub

# Generate audiobook with Piper (WAV files per chapter)
audiobook-piper:
    python3 generate_audiobook.py

# Generate audiobook with Coqui TTS (WAV files per chapter)
audiobook:
    python3 generate_audiobook_coqui.py

# Combine audiobook chapters into single MP3 (requires ffmpeg)
audiobook-combine:
    #!/usr/bin/env bash
    cd dist/audiobook_coqui
    # Create file list
    ls -1 *.wav | sort | sed "s/^/file '/" | sed "s/$/'/" > filelist.txt
    # Combine and convert to MP3
    ffmpeg -y -f concat -safe 0 -i filelist.txt -acodec libmp3lame -ab 128k ../audiobook.mp3
    rm filelist.txt
    echo "Created: dist/audiobook.mp3"

# Full audiobook build (generate + combine)
audiobook-full: audiobook audiobook-combine

# Show file sizes
stats:
    @echo "Output files:"
    @ls -lh dist/typst/book.pdf dist/pandoc/book.epub dist/audiobook.mp3 2>/dev/null || echo "Run 'just build' or 'just audiobook-full'"
