// ===========================================================================
//  Dissertationen und Schutzrechte - Informationsblatt und Rechtseinraeumung
//  fuer die Reihe "Forschungsberichte des ISEM".
//
//  Aufgebaut nach dem Vorbild des TUHH-Informationsblatts "Abschlussarbeiten
//  und Schutzrechte" (ZPA, Stand 01.10.2018), uebertragen auf Dissertationen
//  und die Veroeffentlichung in der Reihe.
//
//  Name, Titel und Betreuung werden aus inhalt/angaben.typ uebernommen.
//  Bauen (aus dem Wurzelordner):
//
//      typst compile --root . template/recht/nutzungsrechte.typ build/nutzungsrechte.pdf
//
//  MUSTER OHNE GEWAEHR: Dieses Dokument ist eine Arbeitshilfe des Instituts
//  und keine Rechtsberatung. Im Zweifel das Justiziariat der TUHH fragen.
// ===========================================================================

#let inhaltsordner = sys.inputs.at("inhalt", default: "inhalt")
#import "/" + inhaltsordner + "/angaben.typ": diss

#let petrol = rgb(0, 106, 129)
#let verfasser = diss.vorname + " " + diss.nachname

#set document(
  title: "Dissertationen und Schutzrechte — Forschungsberichte des ISEM",
  author: "ISEM, Technische Universität Hamburg",
)
#set page(paper: "a4", margin: (x: 25mm, top: 22mm, bottom: 22mm), footer: context [
  #set text(size: 8pt, fill: luma(40%))
  Forschungsberichte des ISEM — Dissertationen und Schutzrechte
  #h(1fr) Stand: 31.08.2026 · Seite #counter(page).display()
])
#set text(font: "Cambria", size: 10pt, lang: "de", region: "DE")
#set par(justify: true, leading: 0.65em, spacing: 0.9em)
#show heading: set text(fill: petrol)
#show heading.where(level: 2): set block(above: 1.6em, below: 0.9em)

#let kopf = {
  grid(columns: (1fr, auto), align: (left + horizon, right + horizon),
    text(size: 14pt, weight: "bold", fill: petrol)[ISEM],
    text(size: 9pt, fill: luma(30%))[
      Institut für Smarte Entwicklung und Maschinenelemente\
      Technische Universität Hamburg
    ])
  v(2mm)
  line(length: 100%, stroke: 0.6pt + petrol)
  v(4mm)
}

#kopf

#align(center, box(stroke: 0.8pt + black, inset: 3.5mm, width: 100%)[
  #set align(center)
  *INFORMATION FÜR PROMOVIERENDE UND BETREUENDE* \
  *Dissertationen und Schutzrechte in der Reihe „Forschungsberichte des ISEM“*
])

== 1. Urheberrecht

Dissertationen sind urheberrechtlich geschützte Werke (§§ 1, 2 UrhG).
Urheber sind allein die Promovierenden (§ 7 UrhG); das Urheberrecht ist
nicht übertragbar (§ 29 Abs. 1 UrhG). Betreuung oder ein
Beschäftigungsverhältnis an der TUHH ändern daran nichts — für
wissenschaftliche Werke greift § 43 UrhG nicht.

== 2. Erfindungen und Patente

Erfindungen unterliegen dem Patentrecht; für Beschäftigte der TUHH gilt
das ArbnErfG (§ 42). Diensterfindungen sind unabhängig von diesem Blatt
nach den Verfahren der TUHH zu melden.

== 3. Nutzungsrechte für die Reihe

Für Druck, Vertrieb und dauerhafte Online-Stellung des Bandes (TORE, DNB)
sowie die Weiterverwendung in Forschung, Lehre, Transfer und
Wissenschaftskommunikation braucht das ISEM Nutzungsrechte (§ 31 UrhG).
Sie werden mit der umseitigen Erklärung unentgeltlich eingeräumt; alle
übrigen Rechte verbleiben beim Verfasser (§ 16 PromO bleibt unberührt).
Optional kann der Band zusätzlich unter CC BY 4.0 gestellt werden.

#v(1fr)
#text(size: 9pt, fill: luma(30%))[
  Arbeitshilfe des ISEM nach dem Vorbild des TUHH-Blatts „Abschlussarbeiten
  und Schutzrechte“ (ZPA); keine Rechtsberatung — verbindliche Auskünfte
  erteilt das Justiziariat der TUHH. Die unterschriebene Erklärung wird im
  Institut aufbewahrt.
]
#pagebreak()
#kopf

An das\
Institut für Smarte Entwicklung und Maschinenelemente (ISEM)\
der Technischen Universität Hamburg

#v(6mm)

#box(stroke: 0.8pt + black, fill: luma(96%), inset: 4mm, width: 100%)[
  #set par(spacing: 1.4em)
  Name, Vorname: #h(0.5em) *#diss.nachname, #diss.vorname*

  ORCID (falls vorhanden): #h(0.5em) #box(width: 1fr, baseline: -2pt, line(length: 100%, stroke: 0.5pt))
]

#v(4mm)

Ich habe an der Technischen Universität Hamburg
(#diss.at("betreuung", default: "Betreuung: ")) eine Dissertation zum Thema

#v(2mm)
#pad(x: 4mm)[*#diss.titel*]
#v(2mm)

angefertigt. Sie soll als *#diss.band* der Reihe „#diss.reihe“ erscheinen.

== Rechtseinräumung

Hiermit räume ich dem ISEM und der TUHH unentgeltlich das *einfache, nicht
ausschließliche Nutzungsrecht* ein, meine Dissertation

+ als Band der Reihe „#diss.reihe“ zu vervielfältigen, zu verbreiten und
  drucken zu lassen (einschließlich Nachauflagen und Print on Demand),
+ elektronisch zu veröffentlichen und dauerhaft öffentlich zugänglich zu
  machen (insbesondere über das Repositorium TORE der TUHH und die
  Ablieferung an die Deutsche Nationalbibliothek),
+ in den Metadaten der Reihe (Titel, Kurzfassung, Umschlagabbildung) zu
  nutzen sowie
+ ganz oder in Teilen für Zwecke der *Forschung, Lehre, des Transfers und
  der Wissenschaftskommunikation des ISEM* zu vervielfältigen, zu
  bearbeiten und öffentlich wiederzugeben — etwa in Lehrveranstaltungen
  und Lehrmaterialien, in Folgeforschung des Instituts, auf Webseite und
  Social-Media-Kanälen, in Vorträgen, auf Messen sowie in der
  Pressearbeit des Instituts.

Das Urheberrecht und alle hier nicht ausdrücklich eingeräumten Rechte
verbleiben bei mir. Die Pflichten aus der Promotionsordnung der TUHH
bleiben unberührt.

#v(2mm)
#box(inset: (left: 4mm))[
  #box(width: 4mm, height: 4mm, stroke: 0.7pt + black) #h(2mm)
  *Zusätzlich* stelle ich den Band unter die Lizenz *CC BY 4.0*
  (Namensnennung); der Lizenzhinweis wird ins Impressum aufgenommen.
]

#v(14mm)
#grid(columns: (1fr, 8mm, 1fr), row-gutter: 2mm,
  line(length: 100%, stroke: 0.5pt), [], line(length: 100%, stroke: 0.5pt),
  text(size: 9pt)[Ort, Datum], [], text(size: 9pt)[Unterschrift #verfasser],
)
