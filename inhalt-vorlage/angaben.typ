// ===========================================================================
//  ALLE ANGABEN ZUR DISSERTATION - HIER UND NUR HIER WIRD ETWAS EINGETRAGEN.
//
//  Format, Beschnitt, Satzspiegel, Farbraum und die Regeln der jeweiligen
//  Fassung ergeben sich daraus automatisch.
//
//  Die Angaben zum Buchumschlag stehen getrennt in buchdaten.typ -
//  warum, steht in ../docs/ANLEITUNG.md.
// ===========================================================================

#let diss = (
  // ══ Welche Fassung? ═══════════════════════════════════════════════════
  //
  //   "eingereicht"  Gutachterfassung nach PromO § 6 Abs. 2.
  //                  Deckblatt "vorgelegte Dissertation" (Vorlage 2a),
  //                  Lebenslauf ist Pflicht, Vorwort/Danksagung/Widmung
  //                  sind verboten.
  //
  //   "genehmigt"    Veroeffentlichungsfassung nach PromO § 16.
  //                  Deckblatt "genehmigte Dissertation" (Vorlage 4b) mit
  //                  Pflichtrueckseite, Vorwort/Danksagung/Widmung erlaubt,
  //                  Lebenslauf optional.
  //
  // Die Vorlage prueft beim Kompilieren, dass die Bestandteile zur Fassung
  // passen, und bricht mit einer Meldung ab, wenn nicht.
  fassung: "genehmigt",

  // ══ Deckblatt ═════════════════════════════════════════════════════════
  titel: "Modellbasierte Entwicklung smarter Maschinenelemente in der frühen Phase der Produktentstehung",
  vorname: "Max",
  nachname: "Mustermann",
  // Geburtsort. Bei Geburt auszerhalb Deutschlands zusaetzlich das Land,
  // z. B. "Baltimore, USA".
  geburtsort: "Musterstadt",

  // Die Zeile hinter "Vom Promotionsausschuss". Sie wird gebeugt:
  // "der Technischen Universität Hamburg", aber "des Karlsruher
  // Instituts für Technologie".
  hochschule: "der Technischen Universität Hamburg",

  // Genderform konkret aufloesen - die TUHH verlangt ausdruecklich
  // "Doktor-Ingenieur" ODER "Doktor-Ingenieurin", nicht "Doktor-Ingenieur(in)".
  grad: "Doktor-Ingenieur (Dr.-Ing.)",
  // Die Vorlagen 2a und 4b geben vor: "Dissertation (Monografie) bzw.
  // (kumulativ)". Eine der beiden Klammern wird ausgewählt und bleibt stehen -
  // Weglassen ist nicht vorgesehen. Zulässig: "Monografie" oder "kumulativ".
  art: "Monografie",

  // Jahr auf dem Deckblatt.
  //   eingereichte Fassung: Jahr der Einreichung
  //   genehmigte Fassung:   Jahr der VEROEFFENTLICHUNG, nicht das Jahr der
  //                         muendlichen Pruefung
  jahr: 2026,

  // Nur auf dem Deckblatt der eingereichten Fassung, dort verlangt.
  // Genderform konkret: "Betreuer" oder "Betreuerin".
  betreuung: "Betreuer: Prof. Dr.-Ing. Nikola Bursac",

  // ══ Rueckseite des Deckblatts ═════════════════════════════════════════
  // Pflicht in der genehmigten Fassung, in der eingereichten nicht vorgesehen.
  gutachten: (
    "1. Gutachter: Prof. Dr.-Ing. Nikola Bursac",
    "2. Gutachter: N. N.",
  ),
  pruefungsvorsitz: "Vorsitzender des Prüfungsausschusses: N. N.",
  pruefungstag: "Tag der mündlichen Prüfung: 1. Januar 2026",

  // ══ Bestandteile ══════════════════════════════════════════════════════
  // true = wird gesetzt. Was in der gewaehlten Fassung unzulaessig ist,
  // fuehrt beim Kompilieren zu einer Fehlermeldung.
  // ── vorn, in dieser Reihenfolge ─────────────────────────────────────
  mit_herausgebervorwort: true, // Vorwort des Reihenherausgebers zum Band
  mit_vorwort: true, // nur genehmigte Fassung; hier gehören die
  //                              Vorabveröffentlichungen hin
  mit_danksagung: true, // nur genehmigte Fassung
  mit_zusammenfassung: true, // Kurzfassung; eingereichte Fassung: Pflicht
  mit_abstract: true, // englische Kurzfassung, frei
  mit_motto: false, // nur genehmigte Fassung; kein religiöser
  //                              Bezug, themenbezogen, Sprache der Arbeit
  mit_widmung: false, // nur genehmigte Fassung, ohne religiösen Bezug

  // ── hinten, nach dem Anhang und dem Literaturverzeichnis ────────────
  mit_studentische_arbeiten: true, // betreute Abschlussarbeiten
  mit_abbildungsverzeichnis: true,
  mit_tabellenverzeichnis: true,
  mit_formelzeichen: true, // Symbol-/Formelzeichenverzeichnis
  mit_abkuerzungen: true,
  mit_glossar: true, // Verzeichnis der Definitionen
  mit_ki_erklaerung: true, // Erklärung zur Nutzung generativer KI
  mit_eidesstattliche_erklaerung: true,
  mit_lebenslauf: false, // eingereichte Fassung: Pflicht, letzte Seite

  // ══ Formelsatz ═══════════════════════════════════════════════════════
  // Für Mathematik braucht es eine Schrift mit OpenType-Math-Tabellen.
  // Cambria Math gehört zur Grundschrift Cambria und passt im Duktus;
  // Variablen stehen damit kursiv, wie es die TUHH verlangt.
  schrift_mathe: "Cambria Math",

  // ══ Sprache ═══════════════════════════════════════════════════════════
  // "de" oder "en" - eine dritte Sprache laesst die TUHH nicht zu.
  sprache: "de",

  // ══ PDF-Metadaten ═════════════════════════════════════════════════════
  // Schlagworte, die in den Metadaten der PDF stehen (Suchmaschinen,
  // Repositorien, DNB). Titel und Verfasser werden von selbst eingetragen.
  schlagworte: (
    "Dissertation",
    "MBSE",
    "Systems Engineering",
    "Technische Universität Hamburg",
  ),

  // ══ Impressum der Buchausgabe ════════════════════════════════════════
  // Diese Seiten gehören zur Reihe, nicht zur Dissertation - die TUHH
  // verlangt sie nicht.
  //
  // Der Schmutztitel ist der Vortitel eines gebundenen Buches: Reihe, Band
  // und Kurztitel vor dem eigentlichen Deckblatt. In der eingereichten
  // Fassung ist er nicht zulässig, dort muss das Deckblatt vorn stehen.
  mit_schmutztitel: true,
  mit_impressum: true,

  // Kurztitel für den Schmutztitel und den Buchrücken.
  // none = der volle Titel wird verwendet.
  kurztitel: "Modellbasierte Entwicklung smarter Maschinenelemente",

  // Herausgeber der Reihe, zweispaltig gesetzt. ORCID ohne Präfix genügt.
  reihenherausgeber: (
    (
      name: "Prof. Dr.-Ing. Nikola Bursać",
      orcid: "0000-0000-0000-0000",
      zeilen: (
        "Institut für Smarte Entwicklung und Maschinenelemente",
        "Technische Universität Hamburg",
        "Hamburg, Deutschland",
      ),
    ),
  ),

  // Die Verfasserin oder der Verfasser dieses Bandes
  verfasser_impressum: (
    name: "Max Mustermann",
    orcid: "0000-0000-0000-0000",
    zeilen: (
      "Institut für Smarte Entwicklung und Maschinenelemente",
      "Technische Universität Hamburg",
      "Hamburg, Deutschland",
    ),
  ),

  // Kennnummern. Die Reihe "Forschungsberichte des ISEM" bekommt eine ISSN,
  // die einzelnen Baende bekommen KEINE ISBN. Jeder Band erhaelt stattdessen
  // eine DOI ueber das Repositorium der TUHH.
  // none = Zeile entfaellt.
  issn_druck: "0000-0000",
  issn_online: "0000-0001",
  isbn_druck: none,
  isbn_online: none,
  doi: "10.15480/000.0000",

  // Kolophon der Buchausgabe. none = Zeile entfaellt.
  // (Das Coverdesign-Credit ist fuer die ganze Reihe gleich und steht fest
  // in der Vorlage - template/innenteil/impressum.typ.)
  herstellung: "WIRmachenDRUCK GmbH, Backnang",
  papier: [
    Gedruckt auf säurefreiem und alterungsbeständigem Papier
    (115 g/m² Bilderdruck matt).
  ],

  rechte: [
    © Der/die Verfasser*in. Alle Rechte vorbehalten.

    Die Deutsche Nationalbibliothek verzeichnet diese Publikation in der
    Deutschen Nationalbibliografie; detaillierte bibliografische Daten sind
    im Internet über portal.dnb.de abrufbar.
  ],

  // ══ Reihe (nur fuer die Buchausgabe relevant) ═════════════════════════
  reihe: "Forschungsberichte des ISEM",
  band: "Band 005",
  herausgeber: "Prof. Dr.-Ing. Nikola Bursac (Hrsg.)",
)

// ── Abkürzungsverzeichnis ─────────────────────────────────────────────────
// Steht hinten. Je Eintrag: Kürzel, Bedeutung.
#let abkuerzungen = (
  ([MBSE], [Model-Based Systems Engineering]),
  ([SysML], [Systems Modeling Language]),
)

// ── Formelzeichenverzeichnis ──────────────────────────────────────────────
// Der TUHH-Leitfaden empfiehlt ein Symbol- und Abkürzungsverzeichnis.
// Je Eintrag: Zeichen, Bedeutung mit Einheit. Variablen kursiv, Einheiten
// aufrecht - der Leitfaden verlangt diese Notation durchgängig, auch in
// den Abbildungen.
// `mathe(..., alt: ...)` gibt der Formel eine Textalternative. Ohne sie
// laesst sich die barrierefreie Fassung (PDF/UA) nicht erzeugen.
#import "/template/innenteil/isem.typ": mathe

#let formelzeichen = (
  (mathe($E$, alt: "E"), [Energie in J]),
  (mathe($m$, alt: "m"), [Masse in kg]),
  (mathe($c$, alt: "c"), [Lichtgeschwindigkeit in m/s]),
)
