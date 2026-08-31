// Farbpalette. Zentraler Ort fuer alle Farben - hier aendern, alles zieht nach.
//
// Jede Farbe ist in BEIDEN Farbraeumen verbindlich hinterlegt. Es wird nicht
// zwischen CMYK und RGB umgerechnet: die Vorgaben sind eigenstaendige Werte,
// eine Umrechnung wuerde sie verfehlen.
//
//   Druck      (Standard)  -> DeviceCMYK, kein RGB-Wert im PDF
//   Bildschirm             -> RGB
// Umschaltung ueber `typst compile --input farbraum=rgb ...`

#let farbraum = sys.inputs.at("farbraum", default: "cmyk")

/// Farbe mit getrennter CMYK- und RGB-Definition.
#let prozessfarbe(c, m, y, k, r, g, b) = {
  if farbraum == "rgb" { rgb(r, g, b) } else { cmyk(c, m, y, k) }
}

// --- vom Auftraggeber verbindlich vorgegeben -----------------------------
//                              C     M    Y    K      R    G    B
#let tuhh-cyan = prozessfarbe(70%, 0%, 13%, 0%, 0, 193, 212) // Logo-Tuerkis
#let petrol = prozessfarbe(100%, 18%, 0%, 49%, 0, 106, 129) // Flaeche, Ruecken

#let isem-cyan = tuhh-cyan // ISEM-Logo: E, M
#let isem-cyan2 = tuhh-cyan // ISEM-Logo: Trennstrich

// --- CMYK noch nicht bestaetigt ------------------------------------------
// RGB stammt aus assets/isem-logo.svg (#7c93ad), CMYK ist daraus gerechnet.
#let isem-grau = prozessfarbe(28%, 15%, 0%, 32%, 124, 147, 173) // ISEM: I, S

// --- Prozessschwarz / Papierweiss ----------------------------------------
#let weiss = prozessfarbe(0%, 0%, 0%, 0%, 255, 255, 255)
#let schwarz = prozessfarbe(0%, 0%, 0%, 100%, 0, 0, 0) // reines K im Druck
