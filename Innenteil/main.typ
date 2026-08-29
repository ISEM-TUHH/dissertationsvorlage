// ===========================================================================
//  Hauptdatei des Innenteils.
//
//  Inhalte stehen in kapitel/ und anhang/, alle Angaben in angaben.typ.
//  Gebaut wird mit .\bauen.ps1 - siehe ../ANLEITUNG.md.
//
//  Die Reihenfolge der Bestandteile folgt der Referenzfassung
//  "Diss_Artur_Krause_ISEM-Vorlage.pdf".
// ===========================================================================

#import "src/isem.typ": *
#import "src/tuhh.typ": deckblatt, deckblatt-rueckseite, pruefe, regeln
#import "src/impressum.typ": impressumsseite, schmutztitel
#import "src/bezeichner.typ": bezeichner
#import "angaben.typ": diss, abkuerzungen, formelzeichen

#import "kapitel/01_einleitung.typ": inhalt as kapitel01
#import "kapitel/02_stand.typ": inhalt as kapitel02
#import "kapitel/03_zusammenfassung.typ": inhalt as kapitel03
#import "anhang/A_ergaenzungen.typ": inhalt as anhangA
#import "anhang/B_weiteres.typ": inhalt as anhangB

// Bricht ab, wenn Bestandteile und Fassung nicht zusammenpassen.
#pruefe(diss)

#let t = bezeichner(diss.sprache)
#let regel = regeln.at(diss.fassung)

#show: configure.with((
  title: diss.titel,
  name: diss.vorname + " " + diss.nachname,
))

// Abbildungs- und Tabellenbezeichner der eingestellten Sprache
#benenne(abbildung: t.abbildung, tabelle: t.tabelle)

#set text(lang: diss.sprache, region: if diss.sprache == "de" { "DE" } else { "GB" })
#set heading(numbering: "1.1")
// Ein Verweis auf eine Ebene-1-Ueberschrift heiszt sonst "Abschnitt 1".
#show heading.where(level: 1): set heading(supplement: [Kapitel])
#show heading.where(level: 2): set heading(supplement: [Abschnitt])
// Formelsatz: eigene Mathe-Schrift, damit Variablen kursiv stehen.
#show math.equation: set text(font: diss.schrift_mathe)
#set cite(form: "normal")
// Nur Weblinks werden eingefaerbt; Verweise innerhalb des Dokuments
// (Inhaltsverzeichnis, Querverweise) bleiben schwarz wie in der Referenz.
// Im Druck bleibt auch der Weblink schwarz - siehe link-color.
#show link: it => if type(it.dest) == str { text(fill: link-color, it) } else { it }

// PDF-Lesezeichen bis zur dritten Gliederungsebene
#show heading.where(level: 4): set heading(bookmarked: false)
#show heading.where(level: 5): set heading(bookmarked: false)
#show heading.where(level: 6): set heading(bookmarked: false)

// Auf Vakatseiten steht nichts - auch keine Kopfzeile.
#show pagebreak.where(to: "odd"): set page(header: none, footer: none)
#show pagebreak.where(to: "even"): set page(header: none, footer: none)

// ═══ Titelei ═══════════════════════════════════════════════════════════════
// Im Vorspann steht im Kopf nur die roemische Seitenzahl.
#set page(header: titelei-kopf(), numbering: "I")

// Das Impressum steht auf der Rueckseite des Schmutztitels - einer linken
// Seite, wie es in Buchreihen ueblich ist. Ohne Schmutztitel bekommt es eine
// eigene Seite hinter dem Deckblatt.
#let impressum-inhalt(seitenwechsel) = impressumsseite(
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

#if diss.mit_schmutztitel {
  schmutztitel(
    reihe: diss.reihe,
    band: diss.band,
    herausgeber: diss.herausgeber,
    titel: if diss.kurztitel != none { diss.kurztitel } else { diss.titel },
    verfasser: diss.vorname + " " + diss.nachname,
    rueckseite: if diss.mit_impressum { impressum-inhalt(false) },
  )
}

#deckblatt(diss)
#deckblatt-rueckseite(diss)

#if diss.mit_impressum and not diss.mit_schmutztitel {
  impressum-inhalt(true)
}

#if diss.mit_herausgebervorwort [
  #front-heading(t.herausgebervorwort)
  #include "titelei/herausgebervorwort.typ"
]
#if diss.mit_vorwort [
  #front-heading(t.vorwort)
  #include "titelei/vorwort.typ"
]
#if diss.mit_danksagung [
  #front-heading(t.danksagung)
  #include "titelei/danksagung.typ"
]
#if diss.mit_zusammenfassung [
  #front-heading(t.zusammenfassung)
  #include "titelei/zusammenfassung.typ"
]
#if diss.mit_abstract [
  #front-heading(t.abstract)
  #include "titelei/abstract.typ"
]
#if diss.mit_motto [
  #include "titelei/motto.typ"
]
#if diss.mit_widmung [
  #include "titelei/widmung.typ"
]

// Das Inhaltsverzeichnis ist das einzige Verzeichnis vor dem Text.
#contents-page(titel: t.inhalt)

// ═══ Hauptteil ═════════════════════════════════════════════════════════════
#set page(header: laufender-kopf(), numbering: "1")
// Erst umbrechen, dann die arabische Zaehlung starten: so traegt die erste
// Kapitelseite wirklich die 1 und nicht eine vorangehende Vakatseite.
#pagebreak(to: "odd")
#counter(page).update(1)

#kapitel("Einleitung", kennung: "kap-einleitung")[#kapitel01]
#kapitel("Stand der Forschung", kennung: "kap-stand")[#kapitel02]
#kapitel("Zusammenfassung und Ausblick", kennung: "kap-fazit")[#kapitel03]

// ═══ Anhang ════════════════════════════════════════════════════════════════
// Zuerst die Trennseite mit einer kurzen Einfuehrung, dann die einzelnen
// Anhaenge - im Satz wie die uebrigen Nachspannteile, aber nummeriert.
#counter(heading).update(0)
#set heading(numbering: "A.1")
#anhang-beginn()
#front-heading(t.anhang, verzeichnet: true)
#include "anhang/00_einfuehrung.typ"

#anhang-teil("Erster Anhang", kennung: "anh-a")[#anhangA]
#anhang-teil("Zweiter Anhang", kennung: "anh-b")[#anhangB]

// ═══ Literaturverzeichnis ══════════════════════════════════════════════════
// Zitierstil des ISEM. Die CSL-Datei liegt neben dieser Datei; sie ist ein
// Fusznotenstil, die Belege erscheinen also am Fusz der Seite.
#set heading(numbering: none)

#bibliography-page(
  titel: t.literatur,
  bibliography("literatur.bib", title: none, style: "ISEM-Zitationsstil.csl"),
)

#if diss.mit_studentische_arbeiten [
  #front-heading(t.studentische_arbeiten)
  #include "titelei/studentische_arbeiten.typ"
]

// ═══ Verzeichnisse ═════════════════════════════════════════════════════════
#if diss.mit_abbildungsverzeichnis { list-page(t.abbildungen, image, t.abbildung) }
#if diss.mit_tabellenverzeichnis { list-page(t.tabellen, table, t.tabelle) }
#if diss.mit_formelzeichen { acronym-page(titel: t.formelzeichen, formelzeichen) }
#if diss.mit_abkuerzungen { acronym-page(titel: t.abkuerzungen, abkuerzungen) }
#if diss.mit_glossar { definitionen-page(titel: t.glossar) }

// ═══ Erklaerungen ══════════════════════════════════════════════════════════
#if diss.mit_ki_erklaerung [
  #front-heading(t.ki_erklaerung)
  #include "titelei/ki_erklaerung.typ"
]
#if diss.mit_eidesstattliche_erklaerung [
  #front-heading(t.eidesstattlich)
  #include "titelei/eidesstattliche_erklaerung.typ"
]

// ═══ Lebenslauf ════════════════════════════════════════════════════════════
// In der eingereichten Fassung Pflicht und ausdruecklich die letzte bedruckte
// Seite; in der genehmigten Fassung optional.
#if diss.mit_lebenslauf [
  #front-heading(t.lebenslauf)
  #include "titelei/lebenslauf.typ"
]

