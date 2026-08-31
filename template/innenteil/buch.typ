// ===========================================================================
//  Zusammenbau des Innenteils.
//
//  Diese Datei gehoert zur Vorlage und wird nicht angepasst. Was in den Band
//  kommt, steht in inhalt/angaben.typ; die Kapitel- und Anhangliste steht in
//  inhalt/main.typ. Aufgerufen wird sie von dort:
//
//      #show: buch.with(diss, kapitel: (...), ...)
//
//  Die Reihenfolge der Bestandteile folgt der Referenzfassung
//  "Diss_Artur_Krause_ISEM-Vorlage.pdf".
// ===========================================================================

#import "isem.typ": *
#import "tuhh.typ": deckblatt, deckblatt-rueckseite, pruefe, regeln
#import "impressum.typ": impressumsseite, schmutztitel
#import "bezeichner.typ": bezeichner

// Der Parameter der Buchfunktion heiszt ebenfalls `kapitel` - die
// Satzfunktion aus isem.typ bekommt darum vorab einen zweiten Namen.
#let kapitel-setzen = kapitel
#let anhang-setzen = anhang-teil

#let buch(
  diss,
  abkuerzungen: (),
  formelzeichen: (),
  literatur: none,
  kapitel: (),
  anhaenge: (),
  body,
) = {
  // Bricht ab, wenn Bestandteile und Fassung nicht zusammenpassen.
  pruefe(diss)

  let t = bezeichner(diss.sprache)

  show: configure.with((
    title: diss.titel,
    name: diss.vorname + " " + diss.nachname,
    keywords: diss.at("schlagworte", default: ()),
  ))

  // Abbildungs- und Tabellenbezeichner der eingestellten Sprache
  benenne(abbildung: t.abbildung, tabelle: t.tabelle)

  set text(lang: diss.sprache, region: if diss.sprache == "de" { "DE" } else { "GB" })
  set heading(numbering: "1.1")
  // Ein Verweis auf eine Ebene-1-Ueberschrift heiszt sonst "Abschnitt 1".
  show heading.where(level: 1): set heading(supplement: [Kapitel])
  show heading.where(level: 2): set heading(supplement: [Abschnitt])
  // Formelsatz: eigene Mathe-Schrift, damit Variablen kursiv stehen.
  show math.equation: set text(font: diss.schrift_mathe)
  set cite(form: "normal")
  // Nur Weblinks werden eingefaerbt; Verweise innerhalb des Dokuments
  // (Inhaltsverzeichnis, Querverweise) bleiben schwarz wie in der Referenz.
  // Im Druck bleibt auch der Weblink schwarz - siehe link-color.
  show link: it => if type(it.dest) == str { text(fill: link-color, it) } else { it }

  // PDF-Lesezeichen bis zur dritten Gliederungsebene
  show heading.where(level: 4): set heading(bookmarked: false)
  show heading.where(level: 5): set heading(bookmarked: false)
  show heading.where(level: 6): set heading(bookmarked: false)

  // Auf Vakatseiten steht nichts - auch keine Kopfzeile.
  show pagebreak.where(to: "odd"): set page(header: none, footer: none)
  show pagebreak.where(to: "even"): set page(header: none, footer: none)

  // ═══ Titelei ═══════════════════════════════════════════════════════════
  // Im Vorspann steht im Kopf nur die roemische Seitenzahl.
  set page(header: titelei-kopf(), numbering: "I")

  // Das Impressum steht auf der Rueckseite des Schmutztitels - einer linken
  // Seite, wie es in Buchreihen ueblich ist. Ohne Schmutztitel bekommt es
  // eine eigene Seite hinter dem Deckblatt.
  let impressum-inhalt(seitenwechsel) = impressumsseite(
    reihe: diss.reihe,
    herausgeber: diss.reihenherausgeber,
    verfasser: diss.verfasser_impressum,
    issn-druck: diss.issn_druck,
    issn-online: diss.issn_online,
    isbn-druck: diss.isbn_druck,
    isbn-online: diss.isbn_online,
    doi: diss.doi,
    coverdesign: diss.coverdesign,
    herstellung: diss.herstellung,
    papier: diss.papier,
    rechte: diss.rechte,
    mit-seitenwechsel: seitenwechsel,
  )

  if diss.mit_schmutztitel {
    schmutztitel(
      reihe: diss.reihe,
      band: diss.band,
      herausgeber: diss.herausgeber,
      titel: if diss.kurztitel != none { diss.kurztitel } else { diss.titel },
      verfasser: diss.vorname + " " + diss.nachname,
      rueckseite: if diss.mit_impressum { impressum-inhalt(false) },
    )
  }

  deckblatt(diss)
  deckblatt-rueckseite(diss)

  if diss.mit_impressum and not diss.mit_schmutztitel {
    impressum-inhalt(true)
  }

  if diss.mit_herausgebervorwort [
    #front-heading(t.herausgebervorwort)
    #include "/inhalt/titelei/herausgebervorwort.typ"
  ]
  if diss.mit_vorwort [
    #front-heading(t.vorwort)
    #include "/inhalt/titelei/vorwort.typ"
  ]
  if diss.mit_danksagung [
    #front-heading(t.danksagung)
    #include "/inhalt/titelei/danksagung.typ"
  ]
  if diss.mit_zusammenfassung [
    #front-heading(t.zusammenfassung)
    #include "/inhalt/titelei/zusammenfassung.typ"
  ]
  if diss.mit_abstract [
    #front-heading(t.abstract)
    #include "/inhalt/titelei/abstract.typ"
  ]
  if diss.mit_motto [
    #include "/inhalt/titelei/motto.typ"
  ]
  if diss.mit_widmung [
    #include "/inhalt/titelei/widmung.typ"
  ]

  // Das Inhaltsverzeichnis ist das einzige Verzeichnis vor dem Text.
  contents-page(titel: t.inhalt)

  // ═══ Hauptteil ═════════════════════════════════════════════════════════
  set page(header: laufender-kopf(), numbering: "1")
  // Erst umbrechen, dann die arabische Zaehlung starten: so traegt die erste
  // Kapitelseite wirklich die 1 und nicht eine vorangehende Vakatseite.
  pagebreak(to: "odd")
  counter(page).update(1)

  for k in kapitel {
    kapitel-setzen(k.titel, kennung: k.at("kennung", default: none))[#k.inhalt]
  }

  // ═══ Anhang ════════════════════════════════════════════════════════════
  // Zuerst die Trennseite mit einer kurzen Einfuehrung, dann die einzelnen
  // Anhaenge - im Satz wie die uebrigen Nachspannteile, aber nummeriert.
  if anhaenge.len() > 0 {
    counter(heading).update(0)
    set heading(numbering: "A.1")
    anhang-beginn()
    front-heading(t.anhang, verzeichnet: true)
    include "/inhalt/anhang/00_einfuehrung.typ"

    for a in anhaenge {
      anhang-setzen(a.titel, kennung: a.at("kennung", default: none))[#a.inhalt]
    }
  }

  // ═══ Literaturverzeichnis ══════════════════════════════════════════════
  // Zitierstil des ISEM, ein Fusznotenstil: die Belege erscheinen am Fusz
  // der Seite. Der bibliography()-Aufruf steht in inhalt/main.typ, damit der
  // Pfad zur literatur.bib dort aufgeloest wird.
  set heading(numbering: none)

  bibliography-page(titel: t.literatur, literatur)

  if diss.mit_studentische_arbeiten [
    #front-heading(t.studentische_arbeiten)
    #include "/inhalt/titelei/studentische_arbeiten.typ"
  ]

  // ═══ Verzeichnisse ═════════════════════════════════════════════════════
  if diss.mit_abbildungsverzeichnis { list-page(t.abbildungen, image, t.abbildung) }
  if diss.mit_tabellenverzeichnis { list-page(t.tabellen, table, t.tabelle) }
  if diss.mit_formelzeichen { acronym-page(titel: t.formelzeichen, formelzeichen) }
  if diss.mit_abkuerzungen { acronym-page(titel: t.abkuerzungen, abkuerzungen) }
  if diss.mit_glossar { definitionen-page(titel: t.glossar) }

  // ═══ Erklaerungen ══════════════════════════════════════════════════════
  if diss.mit_ki_erklaerung [
    #front-heading(t.ki_erklaerung)
    #include "/inhalt/titelei/ki_erklaerung.typ"
  ]
  if diss.mit_eidesstattliche_erklaerung [
    #front-heading(t.eidesstattlich)
    #include "/inhalt/titelei/eidesstattliche_erklaerung.typ"
  ]

  // ═══ Lebenslauf ════════════════════════════════════════════════════════
  // In der eingereichten Fassung Pflicht und ausdruecklich die letzte
  // bedruckte Seite; in der genehmigten Fassung optional.
  if diss.mit_lebenslauf [
    #front-heading(t.lebenslauf)
    #include "/inhalt/titelei/lebenslauf.typ"
  ]

  // Was in main.typ hinter dem show-Aufruf steht, landet hier - im
  // Regelfall nichts.
  body
}
