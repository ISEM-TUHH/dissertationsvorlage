// Motto oder Zitat. Der TUHH-Leitfaden lässt themenbezogene Zitate zu,
// rät aber von themenfremden ab. Religiöse Sprüche sind unzulässig,
// eine dritte Sprache ebenfalls.
//
// Motto und Widmung stehen auf derselben Höhe: das obere Drittel der Seite
// bleibt frei. Beide Seiten sind gleich aufgebaut, damit sie gleich sitzen.

#import "../src/isem.typ": raster, raster-phase

// Erst die Seite wechseln: sonst beginnt der Leerblock noch auf der Seite
// davor und wird umbrochen - das Motto säße dann zu hoch. Der Leerraum
// steht in einem Block, weil Typst ein bloßes #v() am Seitenanfang verwirft.
#pagebreak(weak: true)

#block(height: 12 * raster, width: 100%, spacing: 0pt)[]

#align(center, emph[Platzhalter für ein themenbezogenes Zitat.])

#v(2 * raster - raster-phase)

#align(center)[#text(size: 9pt)[Quelle des Zitats]]
#pagebreak()
