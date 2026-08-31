// Tabellarisch, lückenlos, chronologisch mit Monat/Jahr - nach Muster 1d_b.
// Lücken über 2-3 Monate müssen benannt werden.

#table(
  columns: (auto, 1fr),
  stroke: none,
  column-gutter: 1em,
  row-gutter: 0.5em,
  [Name, Vorname], [Mustermann, Max],
  [Staatsangehörigkeit], [deutsch],
  [Geburtsdatum], [TT.MM.JJJJ],
  [Geburtsort und -land], [Musterstadt, Deutschland],
)

#v(1em)

#table(
  columns: (auto, 1fr),
  stroke: none,
  column-gutter: 1em,
  row-gutter: 0.5em,
  [MM.JJJJ – MM.JJJJ], [Einrichtung, Ort, Abschluss],
  [MM.JJJJ – heute], [Einrichtung, Ort],
)
