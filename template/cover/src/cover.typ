// Druckfertiger Umschlag: U4 | Buchruecken | U1, inklusive Beschnitt.
//
// Spezifikation: WirMachenDruck, "Buch DIN A5 hoch, Hardcover, gerader
// Buchruecken, Umschlag 4/0-farbig" (assets/datenblatt-wirmachendruck.pdf):
//
//   Endformat Umschlag   (306 mm + B) x 215 mm     B = Bundstaerke
//   Datenformat Umschlag (336 mm + B) x 245 mm     -> 15 mm Beschnitt umlaufend
//   Sicherheitsabstand   5 mm ab Endformat
//   Falzkante            ca. 7 mm beidseits des Rueckens
//   Ruecken-Toleranz     10 % (produktionsbedingt)
//
// Der Hardcover-Umschlag ist bewusst groesser als der Buchblock: 153 x 215 mm
// je Deckel gegenueber 148 x 210 mm Inhalt.

#import "farben.typ": *
#import "logos.typ": *
#import "design.typ": u1-inhalt, u4-inhalt, A, ref-w, ref-h

// --- feste Groessen der Druckspezifikation -------------------------------
#let deckel-breite = 153mm
#let deckel-hoehe = 215mm
#let beschnitt = 15mm
#let sicherheit = 5mm
#let falzkante = 7mm

// --- Bundstaerke aus der Seitenzahl --------------------------------------
// Buchrueckenstaerke laut dem Produktkonfigurator von WirMachenDruck fuer
// FADENHEFTUNG bei Inhalt 115 g/m^2 Bilderdruck matt (die Bindung und das
// Papier der Reihe), je Seitenzahl abgefragt am 2026-08-31 unter "mehr
// Produktdetails". Zwischen den Stuetzstellen wird linear interpoliert,
// darueber hinaus mit der Steigung der letzten Strecke fortgeschrieben.
//
// Die aeltere Naeherungsformel (Blattdicke 0,104 mm + 2 x 2,2 mm Graupappe)
// wich bei dicken Baenden um mehr als 1 mm ab; blattdicke/pappe bleiben nur
// als Parameter fuer Sonderfaelle erhalten (werden von der Tabelle nicht
// mehr benutzt, sobald sie unveraendert sind).
#let pappe-default = 2.2mm
#let blatt-default = 0.104mm

#let wmd-ruecken-fadenheftung = (
  (48, 6mm), (52, 7mm), (64, 7mm), (76, 8mm), (80, 8mm), (96, 9mm),
  (100, 10mm), (112, 10mm), (128, 11mm), (144, 12mm), (148, 12mm),
  (160, 13mm), (176, 14mm), (192, 14mm), (204, 15mm), (208, 15mm),
  (224, 16mm), (240, 16mm), (252, 17mm), (256, 17mm), (272, 18mm),
  (288, 19mm), (300, 20mm), (304, 20mm), (320, 21mm), (336, 22mm),
  (352, 22mm), (356, 22mm), (368, 23mm), (384, 24mm), (400, 25mm),
  (416, 25mm), (432, 26mm), (448, 27mm), (464, 28mm), (480, 28mm),
  (496, 29mm), (500, 29mm), (512, 30mm), (528, 31mm), (544, 31mm),
  (560, 32mm), (576, 33mm), (592, 34mm), (600, 34mm),
)

#let bundstaerke(seiten, blattdicke: blatt-default, pappe: pappe-default) = {
  // Weicht der Aufrufer von den Standardwerten ab, gilt seine Formel.
  if blattdicke != blatt-default or pappe != pappe-default {
    return seiten / 2 * blattdicke + 2 * pappe
  }
  let t = wmd-ruecken-fadenheftung
  if seiten <= t.first().at(0) { return t.first().at(1) }
  let letzte = t.first()
  for punkt in t.slice(1) {
    if seiten <= punkt.at(0) {
      let anteil = (seiten - letzte.at(0)) / (punkt.at(0) - letzte.at(0))
      return letzte.at(1) + anteil * (punkt.at(1) - letzte.at(1))
    }
    letzte = punkt
  }
  // jenseits der Tabelle: mit der letzten Steigung fortschreiben
  let vorletzte = t.at(t.len() - 2)
  let steigung = (letzte.at(1) - vorletzte.at(1)) / (letzte.at(0) - vorletzte.at(0))
  letzte.at(1) + (seiten - letzte.at(0)) * steigung
}

// --- Umschlag ------------------------------------------------------------
#let umschlag(
  titel: "",
  autor: "",
  reihe: "Forschungsberichte des ISEM",
  herausgeber: "",
  band: "",
  ruecken-titel: none, // none = titel
  ruecken-autor: none, // Name am Rueckenfuss; none = autor
  ruecken-groesse: 9pt,
  u4-text: none,
  isbn: none,
  seiten: 204,
  bund: none, // Bundstaerke direkt vorgeben; sonst aus `seiten`
  blattdicke: blatt-default,
  pappe: pappe-default,
  hilfslinien: false, // Endformat, Sicherheitsabstand, Falze einblenden
  ..rest, // nimmt den Dokumentkoerper der show-Regel auf; wird nicht gesetzt
) = {
  let B = if bund != none { bund } else {
    bundstaerke(seiten, blattdicke: blattdicke, pappe: pappe)
  }

  let W = 2 * deckel-breite + B + 2 * beschnitt // = 336 mm + B
  let H = deckel-hoehe + 2 * beschnitt // = 245 mm

  let u4-x = beschnitt
  let bund-x = beschnitt + deckel-breite
  let u1-x = bund-x + B
  let oben = beschnitt

  let ry(v) = v / ref-h * deckel-hoehe

  // Oberkante der Petrolflaeche, ueber Ruecken und U4 fortgesetzt.
  // t = 0 an der linken U1-Kante, t = 1 an der rechten.
  let schraege(x) = {
    let t = (x - u1-x) / deckel-breite
    oben + ry(A.flaeche.y0 - A.flaeche.m * ref-w * t)
  }

  set page(width: W, height: H, margin: 0pt, fill: weiss)
  set text(font: "Bahnschrift", fill: schwarz)

  // 1) durchlaufende Petrolflaeche ueber die gesamte Doppelseite
  place(top + left, polygon(
    fill: petrol,
    (0mm, schraege(0mm)), (W, schraege(W)), (W, H), (0mm, H),
  ))

  // 2) Titelseite U1 - Layout 1:1 aus dem Originalentwurf.
  //    Flaeche und Bundstufe entfallen: die Flaeche ist bereits gezeichnet,
  //    die Stufe liefe auf der Doppelseite genau in die Falzkante.
  place(top + left, dx: u1-x, dy: oben,
    u1-inhalt(deckel-breite, deckel-hoehe,
      titel: titel, autor: autor, reihe: reihe,
      herausgeber: herausgeber, band: band,
      flaeche: false, bundstufe: false))

  // 3) Rueckseite U4
  place(top + left, dx: u4-x, dy: oben,
    u4-inhalt(deckel-breite, deckel-hoehe,
      reihe: reihe, herausgeber: herausgeber,
      text-oben: u4-text, isbn: isbn, flaeche: false))

  // 4) Buchruecken - von oben nach unten lesbar (deutsche Leserichtung).
  //    Die Farbgrenze folgt der Schraege: ISEM-Logo im weissen Feld
  //    darueber, Verfasser und Bandnummer weiss im Petrolfeld darunter.
  //    Ein Titel steht nicht auf dem Ruecken; `ruecken-titel` bleibt nur
  //    aus Kompatibilitaet als Parameter erhalten.
  let ra = if ruecken-autor != none { ruecken-autor } else { autor }
  let ruecken-kante = schraege(bund-x + B / 2)

  /// Setzt `inhalt` um 90 Grad gedreht mittig in ein Rueckenfeld.
  /// ausrichtung: top = Textbeginn oben, bottom = Textende unten.
  let ruecken-feld(y0, y1, ausrichtung, inhalt) = place(top + left,
    dx: bund-x, dy: y0,
    box(width: B, height: y1 - y0,
      place(center + horizon, rotate(90deg, reflow: false,
        box(width: y1 - y0,
          align(if ausrichtung == top { left } else { right }, inhalt))))))

  // Kopf: nur das ISEM-Logo - beginnt auf der Oberkante des TUHH-Logos
  // von U1, laeuft mit der Leserichtung des Rueckens mit und skaliert mit
  // der Rueckenbreite.
  ruecken-feld(oben + ry(A.tuhh.y), ruecken-kante - 4mm, top,
    box(baseline: 22%, isem-logo(height: calc.min(B - 2.5mm, 4.2mm))))
  // Fuss: Verfassername (fett) unter der Farbkante, die Bandnummer (fett)
  // endet auf der Grundlinie der Bandangabe von U1.
  if ra != "" {
    ruecken-feld(ruecken-kante + 4mm, oben + ry(A.band.y), bottom,
      text(size: ruecken-groesse, fill: weiss, weight: "bold", {
        ra
        h(1fr)
        band
      }))
  }

  // 5) Hilfslinien - nur zur Kontrolle, niemals in der Druckdatei
  if hilfslinien {
    let mag = cmyk(0%, 100%, 0%, 0%)
    let blau = cmyk(100%, 60%, 0%, 0%)
    let rot = cmyk(0%, 100%, 100%, 0%)
    let l(x0, y0, x1, y1, farbe, dash) = place(top + left,
      line(start: (x0, y0), end: (x1, y1),
        stroke: (paint: farbe, thickness: 0.3pt, dash: dash)))

    // Endformat
    l(beschnitt, oben, W - beschnitt, oben, mag, none)
    l(beschnitt, H - beschnitt, W - beschnitt, H - beschnitt, mag, none)
    l(beschnitt, oben, beschnitt, H - beschnitt, mag, none)
    l(W - beschnitt, oben, W - beschnitt, H - beschnitt, mag, none)

    // Sicherheitsabstand
    let s0 = beschnitt + sicherheit
    l(s0, oben + sicherheit, W - s0, oben + sicherheit, blau, "dashed")
    l(s0, H - s0, W - s0, H - s0, blau, "dashed")
    l(s0, oben + sicherheit, s0, H - s0, blau, "dashed")
    l(W - s0, oben + sicherheit, W - s0, H - s0, blau, "dashed")

    // Ruecken und Falzzonen
    l(bund-x, 0mm, bund-x, H, rot, none)
    l(u1-x, 0mm, u1-x, H, rot, none)
    l(bund-x - falzkante, 0mm, bund-x - falzkante, H, rot, "dashed")
    l(u1-x + falzkante, 0mm, u1-x + falzkante, H, rot, "dashed")

    place(top + left, dx: bund-x - 20mm, dy: 4mm,
      box(width: B + 40mm, align(center, text(size: 6pt, fill: rot,
        "Ruecken " + str(calc.round(B / 1mm, digits: 2)) + " mm"))))
  }
}

// --- Bildschirmfassung ---------------------------------------------------
// Zweiseitiges PDF ohne Beschnitt: Titelseite vorne, Rueckseite hinten.
// Gedacht zum Voran- und Nachstellen an die digitale Fassung der Arbeit.
#let bildschirm(
  titel: "",
  autor: "",
  reihe: "Forschungsberichte des ISEM",
  herausgeber: "",
  band: "",
  u4-text: none,
  isbn: none,
  breite: 148mm, // Voreinstellung DIN A5, passend zum Buchblock
  hoehe: 210mm,
  ..rest,
) = {
  set page(width: breite, height: hoehe, margin: 0pt, fill: weiss)
  set text(font: "Bahnschrift", fill: schwarz)

  u1-inhalt(breite, hoehe,
    titel: titel, autor: autor, reihe: reihe,
    herausgeber: herausgeber, band: band,
    flaeche: true, bundstufe: true)

  pagebreak()

  // U4 steht hier fuer sich; die Schraege beginnt daher wie auf U1.
  u4-inhalt(breite, hoehe,
    reihe: reihe, herausgeber: herausgeber,
    text-oben: u4-text, isbn: isbn,
    flaeche: true, versatz: 0.0)
}
