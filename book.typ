// Book configuration for paperback novel
// Standard paperback size: 5.5" x 8.5" (US Trade) or 5" x 8" (Digest)

#import "template.typ": chapter, scenebreak, letter

#let title = "The Will of the Past"
#let subtitle = "The past is not forgotten. It is armed."
#let author = "Knud Sehested"

// Page setup - US Trade paperback size
#set page(
  width: 5.5in,
  height: 8.5in,
  margin: (
    top: 0.75in,
    bottom: 0.75in,
    inside: 0.875in,  // Larger margin for binding
    outside: 0.625in,
  ),
  numbering: "1",
  number-align: center + bottom,
)

// Typography - using Libertinus Serif (open source, similar to Linux Libertine)
#set text(
  font: "Libertinus Serif",
  size: 11pt,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em,
)

// No indent after headings and breaks
#show heading: it => {
  it
  par(text(size: 0pt, ""))
}


// ============================================
// FRONT MATTER
// ============================================

// Cover page
#set page(numbering: none, margin: 0pt)
#image("assets/cover.jpg", width: 100%, height: 100%)

// Reset margins for rest of book
#set page(
  margin: (
    top: 0.75in,
    bottom: 0.75in,
    inside: 0.875in,
    outside: 0.625in,
  ),
)

// Half title page
#align(center + horizon)[
  #text(size: 18pt, tracking: 0.15em)[#upper(title)]
]
#pagebreak()

// Blank page
#pagebreak()

// Full title page
#align(center + horizon)[
  #text(size: 24pt, weight: "bold", tracking: 0.1em)[#upper(title)]

  #if subtitle != none {
    v(0.5em)
    text(size: 14pt, style: "italic")[#subtitle]
  }

  #v(2em)

  #text(size: 14pt)[#author]
]
#pagebreak()

// Copyright page
#align(bottom)[
  #set text(size: 9pt)
  #set par(leading: 0.5em)

  Copyright \u{00A9} 2024 #author

  All rights reserved.

  This is a work of fiction. Names, characters, places, and incidents either are the product of the author's imagination or are used fictitiously. Any resemblance to actual persons, living or dead, events, or locales is entirely coincidental.

  #v(1em)

  First Edition
]
#pagebreak()

// Blank page before content
#pagebreak()


// ============================================
// MAIN CONTENT
// ============================================

#set page(numbering: "1")
#counter(page).update(1)

// Include all chapters
#include "chapters_typ/00_prologue.typ"
#include "chapters_typ/01_chapter.typ"
#include "chapters_typ/02_chapter.typ"
#include "chapters_typ/03_chapter.typ"
#include "chapters_typ/04_chapter.typ"
#include "chapters_typ/05_chapter.typ"
#include "chapters_typ/06_chapter.typ"
#include "chapters_typ/07_chapter.typ"
#include "chapters_typ/08_chapter.typ"
#include "chapters_typ/09_chapter.typ"
#include "chapters_typ/10_chapter.typ"
#include "chapters_typ/11_chapter.typ"
#include "chapters_typ/12_chapter.typ"
#include "chapters_typ/13_chapter.typ"
#include "chapters_typ/14_chapter.typ"
#include "chapters_typ/15_chapter.typ"
#include "chapters_typ/16_chapter.typ"
#include "chapters_typ/17_chapter.typ"
#include "chapters_typ/18_chapter.typ"
#include "chapters_typ/19_chapter.typ"
#include "chapters_typ/20_chapter.typ"
#include "chapters_typ/21_chapter.typ"
#include "chapters_typ/22_chapter.typ"
#include "chapters_typ/23_chapter.typ"
#include "chapters_typ/24_chapter.typ"
#include "chapters_typ/25_chapter.typ"
#include "chapters_typ/26_chapter.typ"
#include "chapters_typ/27_chapter.typ"
#include "chapters_typ/28_chapter.typ"
#include "chapters_typ/29_chapter.typ"
