# Reference Materials

This folder contains reference documents for authors and editors working on "The Will of the Past" (Fortidsvilje).

## Contents

### Character & Story References

| File | Description |
|------|-------------|
| [characters.md](characters.md) | Complete character profiles with attributes, relationships, and arcs |
| [timeline.md](timeline.md) | Detailed chronology of events (1922-2019) |
| [locations.md](locations.md) | All settings with descriptions and significance |
| [objects-artifacts.md](objects-artifacts.md) | Key objects (chest, suitcase, keys, weapons, Porsche) |

### Writing & Editing Tools

| File | Description |
|------|-------------|
| [plot-structure.md](plot-structure.md) | Three-act structure, chapter breakdown, dual timeline analysis |
| [style-guide.md](style-guide.md) | Voice, formatting, conventions, dialogue guidelines |
| [continuity-checklist.md](continuity-checklist.md) | Quick-reference checklist for consistency verification |

### Background Research

| File | Description |
|------|-------------|
| [historical-research.md](historical-research.md) | Historical context, SS details, Mussolini's capture, sources |

---

## Quick Links by Task

### "I need to check a character detail"
→ [characters.md](characters.md)

### "When did X happen?"
→ [timeline.md](timeline.md)

### "Where is this scene set?"
→ [locations.md](locations.md)

### "What's in the suitcase/chest?"
→ [objects-artifacts.md](objects-artifacts.md)

### "Which chapter covers X?"
→ [plot-structure.md](plot-structure.md)

### "How should I format/write this?"
→ [style-guide.md](style-guide.md)

### "Did I introduce a continuity error?"
→ [continuity-checklist.md](continuity-checklist.md)

### "Is this historically accurate?"
→ [historical-research.md](historical-research.md)

---

## Critical Consistency Points

These are the most common sources of errors. Always verify:

1. **Jens's sister = Lillian** (not Helga)
2. **Paul's niece = Helga Jantzen** (in Koblenz)
3. **Jens died of heart surgery** (not lung cancer)
4. **Keys are IN the suitcase** (not forgotten)
5. **Chest buried 74-75 years** / **Suitcase hidden 67 years**

---

## File Locations

```
fortidsvilje/
├── chapters_english/          # Original chapters
├── chapters_english_revised/  # Revised chapters (use these)
├── chapters_typ/              # Generated Typst files
├── chapters_md/               # Generated Markdown files
├── reference/                 # THIS FOLDER
│   ├── README.md
│   ├── characters.md
│   ├── timeline.md
│   ├── locations.md
│   ├── objects-artifacts.md
│   ├── plot-structure.md
│   ├── style-guide.md
│   ├── continuity-checklist.md
│   └── historical-research.md
├── dist/                      # Built outputs
│   ├── typst/book.pdf
│   └── pandoc/book.epub
├── book.typ                   # Main Typst file
├── metadata.yaml              # EPUB metadata
├── convert_chapters.py        # TXT → Typst converter
├── convert_to_markdown.py     # TXT → Markdown converter
└── justfile                   # Build commands
```

---

## Build Commands

```bash
# Build both PDF and EPUB
just build

# Build only PDF
just pdf

# Build only EPUB
just epub

# Regenerate intermediate formats from source
just convert

# Watch for changes (auto-rebuild PDF)
just watch

# Show output file sizes
just stats
```

---

## Version History

| Date | Changes |
|------|---------|
| 2019-12-09 | Initial reference documents created |
| 2019-12-09 | Revised chapters created with consistency fixes |

---

## Contact

For questions about these materials, consult the main project documentation or the original author.
