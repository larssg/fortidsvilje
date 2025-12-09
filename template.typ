// Template module for book styling

// Chapter styling function
#let chapter(title: none, location: none, date: none, body) = {
  pagebreak(weak: true, to: "odd")

  v(2in)

  if title != none {
    align(center)[
      #text(size: 14pt, weight: "bold", tracking: 0.1em)[#upper(title)]
    ]
  }

  v(0.5in)

  if location != none {
    align(center)[
      #text(size: 10pt, style: "italic")[#location]
    ]
  }

  if date != none {
    align(center)[
      #text(size: 10pt)[#date]
    ]
  }

  v(0.5in)

  body
}

// Scene break
#let scenebreak = {
  v(1em)
  align(center)[#text(tracking: 0.5em)[\* \* \*]]
  v(1em)
}

// Letter/document styling
#let letter(body) = {
  v(0.5em)
  pad(left: 1em, right: 1em)[
    #set text(style: "italic")
    #body
  ]
  v(0.5em)
}
