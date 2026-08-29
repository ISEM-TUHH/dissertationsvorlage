#import "../src/isem.typ": *

#let inhalt = [

== Modellbasierte Systementwicklung

Platzhaltertext mit einem Verweis auf @abb-beispiel. Verweise sind dynamisch:
Wird die Abbildung verschoben oder kommt eine dazu, ändert sich die Nummer
im Text von selbst mit. Dasselbe gilt für Verweise auf @kap-einleitung,
@tab-beispiel und @gl-beispiel.

Fachbegriffe lassen sich in einem Kasten hervorheben:

#definitionsbox[Sicht][
    Eine Sicht ist eine zweckgebundene Auswahl aus einem Modell, die für eine
  bestimmte Personengruppe zu einem bestimmten Zeitpunkt relevant ist.
]

Die Abbildung wird #emph[unterhalb] beschriftet:

#figure(
  // Bei einem echten Bild: abbildung("../abbildungen/bild.png", alt: "…")
  rect(width: 100%, height: 45mm, stroke: 0.5pt + schwarz),
  caption: [Platzhalter für eine Abbildung.],
) <abb-beispiel>

Eine Quelle wird über ihren Schlüssel zitiert @beispiel2024. Der
Zitierstil des ISEM setzt daraus selbst eine Fußnote.

== Sichten und Sichtenbildung

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

Platzhaltertext mit mehreren Literaturverweisen @beispiel2024 @beispiel2023.

]
