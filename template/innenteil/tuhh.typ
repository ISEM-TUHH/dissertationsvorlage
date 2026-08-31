// ===========================================================================
//  TUHH-Formalia: Deckblatt, Deckblattrueckseite und die Regeln, die sich
//  zwischen der eingereichten und der genehmigten Fassung unterscheiden.
//
//  Grundlage
//    Promotionsordnung TUHH, §§ 6 Abs. 2 und 16
//    Deckblattvorlage 2a "Deckblatt beim Einreichen der Dissertation"
//    Deckblattvorlage 4b "Deckblatt der Endfassung"
//    "Guidelines for Formal Aspects of Ph.D. Theses", Stand Juli 2023
//    "Hinweise finale Version der Dissertation", Stand August 2026
//
//  Der Wortlaut der Deckblaetter folgt den Vorlagen 2a und 4b. Die dort
//  offen gelassenen Genderformen und die Wahl Monografie/kumulativ werden
//  aus angaben.typ konkret eingesetzt, wie es die TUHH verlangt.
//
//  Der Satz folgt der Referenzfassung: Titel 14 pt fett, alles Weitere
//  12 pt, mittig im Satzspiegel, die Bloecke im Abstand von 51 pt.
// ===========================================================================

#import "isem.typ": display-font, leading-em, page-top-margin

// --- Regelwerk je Fassung ------------------------------------------------
//
// erlaubt   = darf enthalten sein
// pflicht   = muss enthalten sein
// verboten  = darf nicht enthalten sein
#let regeln = (
  eingereicht: (
    deckblatt: "vorgelegte",
    deckblatt-rueckseite: false,
    betreuung-auf-deckblatt: true,
    jahr-bedeutung: "Jahr der Einreichung",
    widmung: "verboten",
    vorwort: "verboten",
    danksagung: "verboten",
    zusammenfassung: "pflicht",
    lebenslauf: "pflicht",
    schmutztitel: "verboten",
  ),
  genehmigt: (
    deckblatt: "genehmigte",
    deckblatt-rueckseite: true,
    betreuung-auf-deckblatt: false,
    jahr-bedeutung: "Jahr der Veröffentlichung, nicht der mündlichen Prüfung",
    widmung: "erlaubt",
    vorwort: "erlaubt",
    danksagung: "erlaubt",
    zusammenfassung: "erlaubt",
    lebenslauf: "erlaubt",
    schmutztitel: "erlaubt",
  ),
)

/// Prueft die Angaben gegen die Regeln der gewaehlten Fassung und bricht
/// mit einer erklaerenden Meldung ab, wenn etwas nicht zusammenpasst.
#let pruefe(d) = {
  if d.fassung not in ("eingereicht", "genehmigt") {
    panic("angaben.typ: fassung muss \"eingereicht\" oder \"genehmigt\" sein, ist aber \"" + d.fassung + "\".")
  }
  let r = regeln.at(d.fassung)

  let teile = (
    ("mit_widmung", "widmung", "Widmung"),
    ("mit_vorwort", "vorwort", "Vorwort"),
    ("mit_danksagung", "danksagung", "Danksagung"),
    ("mit_zusammenfassung", "zusammenfassung", "Kurzfassung"),
    ("mit_lebenslauf", "lebenslauf", "Lebenslauf"),
    ("mit_schmutztitel", "schmutztitel", "Schmutztitel"),
  )
  for (feld, regel, name) in teile {
    let an = d.at(feld)
    let zustand = r.at(regel)
    if an and zustand == "verboten" {
      panic(
        "angaben.typ: " + name + " ist in der eingereichten Fassung nicht zulässig "
          + "(TUHH-Leitfaden: kein persönlicher Vorspann). "
          + feld + " auf false setzen oder fassung auf \"genehmigt\" ändern.",
      )
    }
    if not an and zustand == "pflicht" {
      panic(
        "angaben.typ: " + name + " ist in der " + d.fassung + "en Fassung Pflicht. "
          + feld + " auf true setzen.",
      )
    }
  }

  if d.fassung == "genehmigt" and d.gutachten.len() == 0 {
    panic("angaben.typ: Die Rückseite des Deckblatts muss die Gutachtenden nennen (PromO § 16 Abs. 3).")
  }
  if d.art not in ("Monografie", "kumulativ") {
    panic(
      "angaben.typ: art muss \"Monografie\" oder \"kumulativ\" sein. "
        + "Die Deckblattvorlagen 2a und 4b geben die Angabe in Klammern vor; "
        + "sie ist auszuwählen, nicht wegzulassen.",
    )
  }
  if d.sprache not in ("de", "en") {
    panic("angaben.typ: Die TUHH lässt nur \"de\" oder \"en\" zu.")
  }
}

// Abstaende auf dem Deckblatt, aus der Referenz gemessen:
//   Titel beginnt 22,46 pt unter dem Kopfsteg,
//   Titel -> erster Block  54,27 pt von Grundlinie zu Grundlinie,
//   Block -> Block         51,00 pt von Grundlinie zu Grundlinie.
#let deckblatt-oben = 22.46pt
#let deckblatt-titelluecke = 39.68pt
#let deckblatt-luecke = 36.86pt

// --- Deckblatt -----------------------------------------------------------
/// Deckblatt nach Vorlage 2a (eingereicht) bzw. 4b (genehmigt).
#let deckblatt(d) = {
  let r = regeln.at(d.fassung)
  // Die Vorlagen 2a und 4b sehen die Art in Klammern zwingend vor.
  let zusatz = " (" + d.art + ")"
  let vorgelegt-oder-genehmigt = if r.deckblatt == "vorgelegte" {
    "vorgelegte Dissertation" + zusatz
  } else {
    "genehmigte Dissertation" + zusatz
  }
  // Die Hochschulzeile steht in angaben.typ, weil sie gebeugt wird:
  // "der Technischen Universität Hamburg", aber "des Karlsruher Instituts
  // für Technologie".
  let einleitung = if r.deckblatt == "vorgelegte" {
    "Dem Promotionsausschuss"
  } else {
    "Vom Promotionsausschuss"
  }

  set page(header: none, footer: none, numbering: none)
  set par(justify: false, first-line-indent: 0pt, leading: leading-em, spacing: 0pt)

  v(deckblatt-oben)
  align(center, text(font: display-font, size: 14pt, weight: "bold", d.titel))
  v(deckblatt-titelluecke)

  set text(size: 12pt)
  align(center)[
    #einleitung \
    #d.hochschule
  ]
  v(deckblatt-luecke)
  align(center)[
    zur Erlangung des akademischen Grades \
    #d.grad
  ]
  v(deckblatt-luecke)
  align(center, vorgelegt-oder-genehmigt)
  v(deckblatt-luecke)
  align(center)[
    von \
    #d.vorname #d.nachname
  ]
  v(deckblatt-luecke)
  align(center)[
    aus \
    #d.geburtsort
  ]
  v(deckblatt-luecke)
  align(center, str(d.jahr))
  if r.betreuung-auf-deckblatt {
    v(deckblatt-luecke)
    align(left, d.betreuung)
  }
  pagebreak()
}

// --- Rueckseite des Deckblatts -------------------------------------------
/// Pflicht in der genehmigten Fassung: Gutachtende und Tag der mündlichen
/// Prüfung, im unteren Drittel der linken Seite. In der eingereichten
/// Fassung nicht vorgesehen - dann bleibt die Seite leer, damit der
/// Vorspann wieder rechts beginnt.
#let deckblatt-rueckseite(d) = {
  set page(header: none, footer: none, numbering: none)
  set par(justify: false, first-line-indent: 0pt, leading: leading-em, spacing: 0pt)
  if regeln.at(d.fassung).deckblatt-rueckseite {
    v(1fr)
    set text(size: 10pt)
    // Zweispaltig mit Tabulator bei 25 mm, wie in der Referenz. Ist die
    // Bezeichnung laenger, laeuft der Name unmittelbar dahinter weiter.
    for zeile in d.gutachten {
      let teile = zeile.split(": ")
      if teile.len() >= 2 {
        let kopf = teile.at(0) + ":"
        let rest = teile.slice(1).join(": ")
        block(above: 0pt, below: 11.14pt)[
          #box(width: 25mm, kopf)#h(0pt)#rest
        ]
      } else {
        block(above: 0pt, below: 11.14pt, zeile)
      }
    }
    if d.pruefungsvorsitz != none and d.pruefungsvorsitz != "" {
      block(above: 0pt, below: 11.14pt, d.pruefungsvorsitz)
    }
    v(11.14pt)
    block(above: 0pt, below: 0pt, d.pruefungstag)
    v(15.57mm)
  }
  pagebreak()
}
