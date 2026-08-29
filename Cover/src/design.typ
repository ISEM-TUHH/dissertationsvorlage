// Layout von Titelseite (U1) und Rueckseite (U4) - formatunabhaengig.
//
// Alle Koordinaten stammen aus assets/entwurf-original.pdf und sind auf dessen
// Referenzflaeche 432 x 648 pt bezogen. Beim Zeichnen werden sie linear auf das
// gewuenschte Zielformat abgebildet (x ueber die Breite, y ueber die Hoehe).
// Dadurch laesst sich dasselbe Layout im Originalformat (zur Pruefung), im
// Druck-Endformat 153 x 215 mm und im Bildschirmformat A5 erzeugen.

#import "farben.typ": *
#import "logos.typ": *

#let ref-w = 432pt
#let ref-h = 648pt

// --- Ankerpunkte aus dem Original (pt im Referenzsystem) -----------------
#let A = (
  // Logos: linke Kante, Oberkante, Hoehe
  tuhh: (x: 34.800pt, y: 32.590pt, h: 40.340pt),
  isem: (x: 260.400pt, y: 33.090pt, h: 39.070pt),

  // Textzeilen: x = Textursprung, y = Grundlinie der ersten Zeile
  // Der Verfassername steht ueber dem Titel: so liegt er immer auf
  // derselben Hoehe, gleich wie lang der Titel ist. Der Titel beginnt
  // einen festen Abstand darunter und waechst nach unten.
  autor: (x: 46.248pt, y: 187.660pt, groesse: 12pt),
  titel: (x: 44.904pt, y: 215.570pt, groesse: 18pt, zeile: 21.600pt),
  reihe: (x: 45.000pt, y: 436.080pt, groesse: 18pt),
  hrsg: (x: 45.000pt, y: 459.170pt, groesse: 12pt),
  band: (rand: 45.000pt, y: 611.448pt, groesse: 12pt),

  // Schraege Oberkante der Petrolflaeche: y = y0 - m * x
  flaeche: (y0: 406.4220pt, m: 0.0475767),

  // Stufe an der Bundkante und weisse Marke neben dem Reihentitel
  stufe: (x0: 0pt, x1: 35.000pt, y: 390.070pt),
  marke: (x0: 34.195pt, x1: 35.612pt, y1: 479.640pt),

  // Rueckseite: Reihenangabe im unteren Drittel, ueber der ISBN
  u4-reihe: (y: 560.000pt, groesse: 13pt),
  u4-hrsg: (y: 580.000pt, groesse: 10pt),

  // Textbreite des Titelblocks (bestimmt den Zeilenumbruch)
  titel-breite: 262pt,
  // Abstand von der letzten Titelgrundlinie zur Grundlinie des Namens,
  // aus dem Originalentwurf: 280,39 - 252,48 pt
  autor-abstand: 27.910pt,
)

// --- Hilfsfunktionen -----------------------------------------------------

/// Baseline-Text: die Box ist 0 hoch, ihre Oberkante liegt exakt auf der
/// Grundlinie. So laesst sich jede Zeile schriftmetrik-unabhaengig setzen.
#let grundlinie(inhalt) = text(top-edge: "baseline", bottom-edge: "baseline", inhalt)

/// Die Petrolflaeche mit schraeger Oberkante, ueber die Breite b.
/// `versatz` verschiebt die Schraege horizontal (fuer U4, wo die Flaeche
/// die Fortsetzung derjenigen von U1 ist).
#let petrolflaeche(b, h, versatz: 0.0) = {
  let ry(v) = v / ref-h * h
  let yl = ry(A.flaeche.y0 - A.flaeche.m * ref-w * versatz)
  let yr = ry(A.flaeche.y0 - A.flaeche.m * ref-w * (versatz + 1.0))
  place(top + left, polygon(fill: petrol, (0mm, yl), (b, yr), (b, h), (0mm, h)))
}

// --- Titelseite U1 -------------------------------------------------------
#let u1-inhalt(
  b, h,
  titel: "",
  autor: "",
  reihe: "Forschungsberichte des ISEM",
  herausgeber: "",
  band: "",
  flaeche: true, // Petrolflaeche mitzeichnen (auf der Doppelseite laeuft sie durch)
  bundstufe: true, // Stufe an der Bundkante (nur fuer die Einzelseite sinnvoll)
) = {
  let rx(v) = v / ref-w * b
  let ry(v) = v / ref-h * h
  // Schriftgrade folgen der Breite, damit Satzbreite und Format zusammenpassen
  let rs(v) = v / ref-w * b

  box(width: b, height: h, {
    if flaeche { petrolflaeche(b, h) }

    // Stufe an der Bundkante
    if bundstufe {
      place(top + left, dx: rx(A.stufe.x0), dy: ry(A.stufe.y),
        rect(width: rx(A.stufe.x1 - A.stufe.x0), height: h - ry(A.stufe.y),
          fill: petrol, stroke: none))
    }

    // weisse Marke links neben der Reihenzeile
    place(top + left, dx: rx(A.marke.x0), dy: ry(A.stufe.y),
      rect(width: rx(A.marke.x1 - A.marke.x0), height: ry(A.marke.y1 - A.stufe.y),
        fill: weiss, stroke: none))

    // Logos
    place(top + left, dx: rx(A.tuhh.x), dy: ry(A.tuhh.y), tuhh-logo(height: ry(A.tuhh.h)))
    place(top + left, dx: rx(A.isem.x), dy: ry(A.isem.y), isem-logo(height: ry(A.isem.h)))

    // Verfasser - ueber dem Titel und damit auf fester Hoehe.
    place(top + left, dx: rx(A.autor.x), dy: ry(A.autor.y),
      grundlinie(text(font: "Bahnschrift", size: rs(A.autor.groesse),
        fill: schwarz, autor)))

    // Titel
    place(top + left, dx: rx(A.titel.x), dy: ry(A.titel.y),
      block(width: rx(A.titel-breite), {
        set text(font: "Bahnschrift", size: rs(A.titel.groesse), fill: schwarz)
        set par(leading: ry(A.titel.zeile), spacing: 0pt, justify: false)
        grundlinie(titel)
      }))

    // Reihentitel
    place(top + left, dx: rx(A.reihe.x), dy: ry(A.reihe.y),
      grundlinie(text(font: "Bahnschrift", size: rs(A.reihe.groesse), fill: weiss, reihe)))

    // Herausgeber
    place(top + left, dx: rx(A.hrsg.x), dy: ry(A.hrsg.y),
      grundlinie(text(font: "Bahnschrift", size: rs(A.hrsg.groesse), fill: weiss, herausgeber)))

    // Bandangabe, rechtsbuendig mit demselben Rand wie der linke Satzspiegel
    place(top + left, dx: rx(A.band.rand), dy: ry(A.band.y),
      block(width: b - 2 * rx(A.band.rand), align(right,
        grundlinie(text(font: "Bahnschrift", size: rs(A.band.groesse), fill: weiss, band)))))
  })
}

// --- Rueckseite U4 -------------------------------------------------------
// Bewusst ruhig gehalten: der Entwurf gibt fuer U4 nichts vor. Uebernommen
// werden Flaeche, Marke und Grundlinien von U1, damit beide Deckel
// zusammengehoeren.
#let u4-inhalt(
  b, h,
  reihe: "Forschungsberichte des ISEM",
  herausgeber: "",
  text-oben: none,
  isbn: none,
  flaeche: true,
  mit-reihenangabe: true, // Reihentitel auf der Rueckseite zeigen
  versatz: -1.0, // Lage der Schraege relativ zu U1 (Doppelseite: eine Deckelbreite links)
) = {
  let rx(v) = v / ref-w * b
  let ry(v) = v / ref-h * h
  let rs(v) = v / ref-w * b

  box(width: b, height: h, {
    if flaeche { petrolflaeche(b, h, versatz: versatz) }

    if text-oben != none {
      place(top + left, dx: rx(A.reihe.x), dy: ry(A.tuhh.y),
        block(width: b - 2 * rx(A.reihe.x),
          text(font: "Bahnschrift", size: rs(10pt), fill: schwarz, text-oben)))
    }

    // Reihenangabe auf der Rueckseite: tiefer als auf der Titelseite, dicht
    // ueber der ISBN. Oben auf U1 traegt sie den Blickfang, hier waere sie
    // nur eine Wiederholung mitten in der Flaeche.
    if mit-reihenangabe {
      place(top + left, dx: rx(A.reihe.x), dy: ry(A.u4-reihe.y),
        grundlinie(text(font: "Bahnschrift", size: rs(A.u4-reihe.groesse),
          fill: weiss, reihe)))
      place(top + left, dx: rx(A.hrsg.x), dy: ry(A.u4-hrsg.y),
        grundlinie(text(font: "Bahnschrift", size: rs(A.u4-hrsg.groesse),
          fill: weiss, herausgeber)))
    }

    if isbn != none {
      place(top + left, dx: rx(A.band.rand), dy: ry(A.band.y),
        block(width: b - 2 * rx(A.band.rand), align(right,
          grundlinie(text(font: "Bahnschrift", size: rs(A.band.groesse), fill: weiss, isbn)))))
    }
  })
}
