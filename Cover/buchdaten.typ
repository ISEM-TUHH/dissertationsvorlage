// ===========================================================================
//  ALLE ANGABEN ZUM BUCH - HIER UND NUR HIER WIRD ETWAS EINGETRAGEN.
//  Format, Beschnitt, Bundstaerke, Farben und Logos ergeben sich automatisch.
// ===========================================================================

#let buch = (
  // --- die vier Hauptangaben -------------------------------------------
  titel: "Intuitive und stakeholder-gerechte Sichten im MBSE zur Steigerung von Veränderlichkeit und Akzeptanz",
  autor: "Felix Förster",
  band: "Band 005",

  // Seitenzahl des gedruckten Buchblocks (Papierseiten, nicht Blätter).
  // Daraus wird die Bundstärke berechnet und daraus das Umschlagformat.
  seiten: 48,

  // --- Reihe ------------------------------------------------------------
  reihe: "Forschungsberichte des ISEM",
  herausgeber: "Prof. Dr.-Ing. Nikola Bursac (Hrsg.)",

  // --- Buchrücken -------------------------------------------------------
  // Der Rücken ist schmal - hier gehört eine gekürzte Titelfassung hin.
  // none = der volle Titel wird verwendet.
  ruecken-titel: "Intuitive und stakeholdergerechte Sichten im MBSE",
  // Name am Fuß des Rückens - Vor- und Nachname, ohne Grad.
  ruecken-autor: "Felix Förster",

  // --- Rückseite (U4) ---------------------------------------------------
  u4-text: none, // Klappentext / Kurzfassung; none = leer
  isbn: none, // z. B. "ISBN 978-3-..."

  // --- Feineinstellungen zur Bundstärke ---------------------------------
  // Nennt die Druckerei eine abweichende Bundstärke, hier direkt eintragen
  // (z. B. 15mm). none = aus der Seitenzahl berechnen.
  bund: none,

  // Papier des Buchblocks. Voreinstellung: 115 g/m² Bilderdruck matt,
  // aus der Herstellerangabe zurückgerechnet (204 Seiten -> 15 mm Rücken).
  blattdicke: 0.104mm,
  // Graupappe je Buchdeckel laut Produktbeschreibung.
  pappe: 2.2mm,

  // --- Bildschirmfassung ------------------------------------------------
  // Format der zweiseitigen RGB-Fassung (Titelseite vorn, Rückseite hinten).
  // Voreinstellung DIN A5, passend zum Buchblock.
  bildschirm-breite: 148mm,
  bildschirm-hoehe: 210mm,
)
