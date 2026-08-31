// Impressumsseite der Reihe - Herausgeber, Nummern, Rechtehinweis.
//
// Aufbau nach dem Vorbild wissenschaftlicher Verlagsreihen: die Herausgeber
// zweispaltig mit Einrichtung und Ort, darunter die Kennnummern, das
// Coverdesign und der Rechtehinweis.
//
// Die Seite gehört zur Reihe, nicht zur Dissertation. Die TUHH verlangt sie
// nicht - sie ist Teil der Buchausgabe.

#import "isem.typ": accent, prozessfarbe, schwarz, weiss, display-font, raster, raster-phase

// ORCID-Grün nach dem Gestaltungsraster von ORCID. Der CMYK-Wert ist mit
// ISOcoated_v2_300_eci aus dem RGB-Wert gerechnet (relativ farbmetrisch).
#let orcid-gruen = prozessfarbe(45%, 0%, 94%, 0%, 166, 206, 57)

/// ORCID-iD als Marke mit Verweis auf das Profil.
///
/// Das Zeichen steht hinter dem Namen, die Nummer selbst wird darunter nicht
/// wiederholt - der Verweis führt darauf.
#let orcid(id) = {
  if id == none { return }
  let nummer = id.replace("https://orcid.org/", "")
  h(0.35em)
  box(baseline: 0.15em, link("https://orcid.org/" + nummer,
    circle(
      radius: 0.34em,
      fill: orcid-gruen,
      stroke: none,
      align(center + horizon,
        text(size: 0.4em, fill: weiss, weight: "bold", baseline: 0pt, "iD")),
    )))
}

/// Ein Eintrag im Herausgeber- oder Verfasserblock.
#let person(name, orcid-id: none, zeilen: ()) = {
  set par(justify: false, leading: 0.20em, first-line-indent: 0pt)
  block(width: 100%, breakable: false, {
    [#name#orcid(orcid-id)]
    for z in zeilen {
      linebreak()
      z
    }
  })
}

/// Schmutztitel (Vortitel) und seine Rueckseite.
///
/// Ein gebundenes Buch beginnt nicht mit dem Haupttitel, sondern mit einem
/// Vortitel: Reihe, Band und der gekuerzte Titel, alles klein und ruhig
/// gesetzt. Die Rueckseite bleibt leer. Erst danach folgt das Deckblatt.
///
/// In der eingereichten Fassung entfaellt der Schmutztitel - dort verlangt
/// die TUHH das Deckblatt als erste Seite.
#let schmutztitel(
  reihe: "",
  band: "",
  herausgeber: none,
  titel: "",
  verfasser: "",
  rueckseite: none, // Inhalt der Rueckseite, ueblicherweise das Impressum
) = {
  set page(header: none, footer: none, numbering: none)
  set par(justify: false, first-line-indent: 0pt, spacing: 0pt)
  set text(size: 10pt)

  v(6 * raster)
  align(center)[
    #text(size: 9pt, tracking: 0.08em, upper(reihe))
    #if band != "" [
      #linebreak()
      #v(raster - raster-phase)
      #text(size: 9pt, band)
    ]
    #if herausgeber != none [
      #linebreak()
      #v(raster - raster-phase)
      #text(size: 9pt, herausgeber)
    ]
  ]
  v(10 * raster)
  align(center, text(font: display-font, size: 12pt, weight: "bold", titel))
  v(2 * raster)
  align(center, text(size: 10pt, verfasser))
  pagebreak()

  // Rueckseite des Schmutztitels. Im Buchsatz steht dort das Impressum -
  // eine linke Seite, wie es die Reihen halten. Ohne Impressum bleibt sie
  // leer.
  set page(header: none, footer: none, numbering: none)
  if rueckseite != none { rueckseite } else { [] }
  pagebreak()
}

/// Die Impressumsseite.
#let impressumsseite(
  reihe: "",
  herausgeber: (), // Liste von Wörterbüchern: name, orcid, zeilen
  verfasser: none, // dasselbe für die Verfasserin oder den Verfasser
  issn-druck: none,
  issn-online: none,
  isbn-druck: none,
  isbn-online: none,
  doi: none,
  // Das Coverdesign der Reihe ist fuer alle Baende dasselbe - das Credit
  // gehoert deshalb zur Vorlage, nicht in die angaben.typ des Bandes.
  coverdesign: "Cerrigan Rose und Felix Förster",
  herstellung: none,
  papier: none,
  rechte: none,
  mit-seitenwechsel: true, // false, wenn die Seite schon steht
) = {
  set page(header: none, footer: none, numbering: none)
  set text(size: 9pt)
  set par(justify: true, leading: 0.20em, first-line-indent: 0pt)

  v(8mm)

  if herausgeber.len() > 0 {
    text(style: "italic", size: 9pt)[Herausgeber der Reihe]
    if reihe != "" [ #sym.dash.en #reihe]
    v(2mm)
    // Zweispaltig, wie in Verlagsreihen üblich - bei einer ungeraden Zahl
    // bleibt die letzte Spalte frei.
    grid(
      columns: (1fr, 1fr),
      column-gutter: 6mm,
      row-gutter: 5mm,
      ..herausgeber.map(h => person(
        h.at("name", default: ""),
        orcid-id: h.at("orcid", default: none),
        zeilen: h.at("zeilen", default: ()),
      )),
    )
    v(6mm)
  }

  if verfasser != none {
    text(style: "italic", size: 9pt)[Verfasser]
    v(2mm)
    person(
      verfasser.at("name", default: ""),
      orcid-id: verfasser.at("orcid", default: none),
      zeilen: verfasser.at("zeilen", default: ()),
    )
    v(6mm)
  }

  v(1fr)

  // Kennnummern: gedruckt links, elektronisch rechts - so wie sie auch
  // vergeben werden.
  let nummer(bezeichnung, druck, online) = {
    if druck == none and online == none { return }
    // Die Nummern brauchen so viel Platz, wie sie brauchen; der Ausgleich
    // liegt in der Mitte. Sonst rutscht der Zusatz "(elektronisch)" um.
    grid(
      columns: (auto, auto, 1fr, auto, auto),
      column-gutter: 0.6em,
      strong(bezeichnung), if druck != none { druck } else { [] },
      [],
      if online != none { strong(bezeichnung) } else { [] },
      // box verhindert, dass "(elektronisch)" umbrochen wird
      if online != none { [#online #h(0.4em) #box[(elektronisch)]] } else { [] },
    )
    v(1.2mm)
  }

  nummer("ISSN", issn-druck, issn-online)
  nummer("ISBN", isbn-druck, isbn-online)
  if doi != none {
    let nummer = doi.replace("https://doi.org/", "")
    let ziel = "https://doi.org/" + nummer
    link(ziel, text(fill: accent, ziel))
    v(1.2mm)
  }

  if coverdesign != none {
    v(3mm)
    [Coverdesign: #coverdesign]
  }

  // Herstellungsangaben - im Buchsatz gehoert das in den Kolophon.
  if herstellung != none {
    v(1.2mm)
    [Herstellung und Druck: #herstellung]
  }
  if papier != none {
    v(1.2mm)
    papier
  }

  if rechte != none {
    v(3mm)
    set text(size: 8pt)
    set par(leading: 0.20em)
    rechte
  }

  v(6mm)
  if mit-seitenwechsel { pagebreak() }
}
