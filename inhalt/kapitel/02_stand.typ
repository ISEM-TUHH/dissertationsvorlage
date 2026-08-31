#import "/template/innenteil/isem.typ": *


== Modellbasierte Systementwicklung

#lorem(75)

Platzhaltertext mit einem Verweis auf @abb-beispiel. Verweise sind dynamisch:
Wird die Abbildung verschoben oder kommt eine dazu, ändert sich die Nummer
im Text von selbst mit. Dasselbe gilt für Verweise auf @kap-einleitung,
@tab-beispiel und @gl-beispiel.

#lorem(55)

Fachbegriffe lassen sich in einem Kasten hervorheben. Der Kasten zählt sich
selbst und erscheint zugleich im Glossar am Ende des Bandes — die Nummer
schreibst du nicht, sie entsteht:

#definitionsbox[Sicht][
    Eine Sicht ist eine zweckgebundene Auswahl aus einem Modell, die für eine
  bestimmte Personengruppe zu einem bestimmten Zeitpunkt relevant ist.
]

Die Abbildung wird #emph[unterhalb] beschriftet. Bilddateien liegen in
`inhalt/abbildungen/` und werden nur mit ihrem Dateinamen aufgerufen:
`abbildung("aufbau.png", alt: "…")`. Eine übernommene Abbildung bekommt ihre
Quelle mit `#bildquelle(<schlüssel>)` direkt in die Beschriftung — die
Fußnote mit der Quellenangabe steht dann auf der Seite der Abbildung, und im
Abbildungsverzeichnis hinten bleibt sie weg:

#figure(
  abbildung("beispiel.png", alt: "Platzhaltergrafik mit Rahmen und Diagonalen."),
  caption: [Platzhalter für eine übernommene Abbildung.#bildquelle(<beispiel2024>)],
) <abb-beispiel>

Eine Quelle wird über ihren Schlüssel zitiert @beispiel2024. Der
Zitierstil des ISEM setzt daraus selbst eine Fußnote. Steht das Zitat
innerhalb einer eigenen Fußnote, nimmt man `#quelle(<schlüssel>)` — sonst
entstünde eine Fußnote in der Fußnote.#footnote[So sieht das aus:
#quelle(<beispiel2024>) und #quelle(<beispiel2023>).]

#lorem(60)

== Sichten und Sichtenbildung

#lorem(80)

Eine nummerierte Gleichung wird kapitelweise gezählt:

#numbered-equation($ E = m c^2 $, alt: "E ist gleich m mal c hoch zwei") <gl-beispiel>

Tabellen werden dagegen #emph[oberhalb] beschriftet:

#figure(
  table(
    columns: (1fr, 1fr, 1fr),
    align: left,
    inset: (x: 0pt, y: 4pt),
    // Farbe ausdruecklich: `0.5pt` allein waere DeviceGray und wuerde im
    // Druck zu vierfarbigem Schwarz - siehe src/isem.typ.
    stroke: (x, y) => (
      top: if y <= 1 { 0.5pt + schwarz } else { none },
      bottom: if y == 2 { 0.5pt + schwarz } else { none },
    ),
    table.header([*Merkmal*], [*Ausprägung A*], [*Ausprägung B*]),
    [Erstes], [Wert], [Wert],
    [Zweites], [Wert], [Wert],
  ),
  caption: [Platzhalter für eine Tabelle.],
) <tab-beispiel>

#lorem(65)

Platzhaltertext mit mehreren Literaturverweisen @beispiel2024 @beispiel2023.

#lorem(70)
