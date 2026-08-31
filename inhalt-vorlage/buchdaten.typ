// ===========================================================================
//  ALLE ANGABEN ZUM BUCH - HIER UND NUR HIER WIRD ETWAS EINGETRAGEN.
//  Format, Beschnitt, Bundstaerke, Farben und Logos ergeben sich automatisch.
// ===========================================================================

#let buch = (
  // --- die vier Hauptangaben -------------------------------------------
  titel: "Modellbasierte Entwicklung smarter Maschinenelemente in der frühen Phase der Produktentstehung",
  autor: "Max Mustermann",
  band: "Band 005",

  // Seitenzahl des gedruckten Buchblocks (Papierseiten, nicht Blätter).
  // Daraus wird die Bundstärke berechnet und daraus das Umschlagformat.
  seiten: 52,

  // --- Reihe ------------------------------------------------------------
  reihe: "Forschungsberichte des ISEM",
  herausgeber: "Prof. Dr.-Ing. Nikola Bursac (Hrsg.)",

  // --- Buchrücken -------------------------------------------------------
  // Der Rücken trägt ISEM-Logo, Verfassername und Bandnummer - keinen
  // Titel. ruecken-titel bleibt nur aus Kompatibilität stehen.
  ruecken-titel: "Modellbasierte Entwicklung smarter Maschinenelemente",
  // Name am Fuß des Rückens - Vor- und Nachname, ohne Grad.
  ruecken-autor: "Max Mustermann",

  // --- Rückseite (U4) ---------------------------------------------------
  u4-text: none, // Klappentext / Kurzfassung; none = leer
  isbn: none, // z. B. "ISBN 978-3-..."

  // --- Feineinstellungen zur Bundstärke ---------------------------------
  // none = aus der Seitenzahl über die Konfigurator-Tabelle von
  // WirMachenDruck berechnen (Fadenheftung, 115 g/m² Bilderdruck matt -
  // hinterlegt in template/cover/src/cover.typ). Nennt der Konfigurator
  // für deine Seitenzahl etwas anderes, hier direkt eintragen (z. B. 15mm).
  bund: none,

  // Nur für Sonderfälle (anderes Papier): weicht einer der beiden Werte
  // von der Voreinstellung ab, rechnet der Umschlag wieder linear mit
  // seiten/2 x blattdicke + 2 x pappe statt mit der Tabelle.
  blattdicke: 0.104mm,
  // Graupappe je Buchdeckel laut Produktbeschreibung.
  pappe: 2.2mm,

  // --- Bildschirmfassung ------------------------------------------------
  // Format der zweiseitigen RGB-Fassung (Titelseite vorn, Rückseite hinten).
  // Voreinstellung DIN A5, passend zum Buchblock.
  bildschirm-breite: 148mm,
  bildschirm-hoehe: 210mm,
)
