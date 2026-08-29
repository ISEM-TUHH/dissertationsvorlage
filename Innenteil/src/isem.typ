// ===========================================================================
//  Satzspiegel und Auszeichnungen der ISEM-Dissertationsvorlage.
//
//  Die Masze sind aus der Referenzfassung
//  "Diss_Artur_Krause_ISEM-Vorlage.pdf" ausgemessen. Jene Datei ist aus Word
//  auf das Datenformat 154 x 216 mm exportiert; alle Angaben hier beziehen
//  sich auf das Endformat A5 (148 x 210 mm), also auf das Datenformat
//  abzueglich 3 mm Beschnitt ringsum. Den Beschnitt legt erst
//  tools/druckdatei.py an.
//
//  Schriftgrade, Satzbreite und Zeilenabstand sind aus der Referenz
//  uebernommen. Bei drei Punkten geht die Vorlage bewusst darueber hinaus,
//  weil die Referenz dort Word-Berichtssatz ist und kein Buchsatz:
//
//    Stege     Auszensteg breiter als Bundsteg (klassischer Buchsatz)
//    Absaetze  Erstzeileneinzug statt Absatzabstand
//    Register  alle senkrechten Abstaende sind Vielfache des Zeilenschritts
//
//  Grundwerte (Endformat 148 x 210 mm):
//    Satzspiegel    119 x 173 mm, 38 Zeilen, 74 Zeichen je Zeile
//    Bundsteg       14 mm, Auszensteg 15 mm (im Druck gespiegelt)
//    Kopfsteg       16,85 mm (bis Oberkante der ersten Textzeile)
//    Fuszsteg       20,1 mm
//    Grundschrift   Cambria 10 pt, Zeilenschritt 12,9 pt
//    Ueberschriften 18 / 12 / 11 / 10 pt fett
//    Kopfzeile      8 pt, Linie 0,45 pt schwarz
//    Fusznoten      9 pt, Trennlinie 2 Zoll in ISEM-Petrol
// ===========================================================================

// ── Schriften ─────────────────────────────────────────────────────────────
#let body-font = "Cambria"
#let display-font = "Cambria"
// Word setzt die Kommentar- und Beschriftungsschrift in Calibri; im Satz
// wird sie nicht gebraucht, bleibt aber als Ausweichname stehen.
#let sans-font = "Calibri"
#let mono-font = "Consolas"

// ── Ausgabe ───────────────────────────────────────────────────────────────
// `typst compile --input ausgabe=druck` setzt doppelseitig fuer den Druck.
#let ist-druck = sys.inputs.at("ausgabe", default: "online") == "druck"

// ── Farben ────────────────────────────────────────────────────────────────
// Wie beim Umschlag ist jede Farbe in BEIDEN Farbraeumen verbindlich
// hinterlegt und wird nicht umgerechnet. Fuer den Druck steht damit
//
//   Flieszttext  0/0/0/100  - reines Schwarz im K-Kanal. Eine nachtraegliche
//                Trennung ueber ein ICC-Profil macht daraus vierfarbiges
//                Schwarz; im Buchsatz ist das ein Fehler, weil schon eine
//                geringe Passerdifferenz die Schrift unscharf erscheinen
//                laeszt.
//   Petrol       100/18/0/49 - Hausfarbe der Reihe, identisch zum Umschlag
//                (Cover/src/farben.typ).
#let farbraum = sys.inputs.at(
  "farbraum",
  default: if ist-druck { "cmyk" } else { "rgb" },
)
#let prozessfarbe(c, m, y, k, r, g, b) = {
  if farbraum == "rgb" { rgb(r, g, b) } else { cmyk(c, m, y, k) }
}

#let accent = prozessfarbe(100%, 18%, 0%, 49%, 0, 106, 129)
#let schwarz = prozessfarbe(0%, 0%, 0%, 100%, 0, 0, 0)
#let weiss = prozessfarbe(0%, 0%, 0%, 0%, 255, 255, 255)
#let label-color = accent

/// Grauton im K-Kanal. `grau(30%)` statt `luma(70%)` - sonst entsteht im
/// Druck ein vierfarbiges Grau.
#let grau(anteil) = if farbraum == "rgb" {
  luma(100% - anteil)
} else {
  cmyk(0%, 0%, 0%, anteil)
}

// Farbe der Verweise. Im Buch stoert eingefaerbte Schrift den Grauwert der
// Seite - dort bleiben Verweise schwarz, aber anklickbar. Am Bildschirm
// zeigt Petrol, dass ein Verweis dahintersteckt.
#let link-color = if ist-druck { schwarz } else { accent }

// ── Satzspiegel ───────────────────────────────────────────────────────────
//
// Die Stege folgen dem klassischen Buchsatz: der Auszensteg ist breiter als
// der Bundsteg, damit die aufgeschlagene Doppelseite als Einheit wirkt und
// der Daumen Platz hat. Der Bundsteg bleibt mit 14 mm doppelt so breit wie
// die 7 mm Falzkante, die das Datenblatt fuer die ersten und letzten
// Blaetter des Hardcovers nennt.
//
// Im Druck wechseln Bund- und Auszensteg mit der Seite. Am Bildschirm wird
// nicht geblaettert, sondern gescrollt - dort stehen die Raender gleich, sonst
// springt der Text von Seite zu Seite.
#let seiten-breite = 148mm
#let seiten-hoehe = 210mm
#let inner-margin = 14mm // Bundsteg
#let outer-margin = 15mm // Auszensteg
#let online-margin = (inner-margin + outer-margin) / 2 // 14,5 mm, mittig
// Kopf- und Fuszsteg sind so gewaehlt, dass die erste Grundlinie auf
// 20,20 mm liegt und 38 Zeilen auf die Seite gehen - beides wie gemessen.
#let page-top-margin = 16.85mm
#let page-bottom-margin = 20.1mm
#let satz-breite = seiten-breite - inner-margin - outer-margin // 119 mm
#let page-body-height = seiten-hoehe - page-top-margin - page-bottom-margin // 171 mm

// Abstand der Kopfzeilenlinie zum Satzspiegel.
#let header-ascent = 3.68mm

// ── Vertikales Raster ─────────────────────────────────────────────────────
// Word legt die Zeilenbox mit Cambrias Schriftmaszen an (Oberlaenge 0,95 em,
// Unterlaenge 0,222 em) und rueckt die Grundlinien auf 1,29 em. Damit die
// erste Zeile genau auf dem Kopfsteg sitzt, werden die Kanten fest in em
// angegeben statt aus der Schrift gelesen.
#let text-top-edge = 0.95em
#let text-bottom-edge = -0.228em
#let zeilenkasten = 1.178 // Oberlaenge + Unterlaenge, in em
#let zeilenabstand = 1.29 // Grundlinienabstand, in em
#let leading-em = (zeilenabstand - zeilenkasten) * 1em // 0,112 em

// ── Grundlinienraster ─────────────────────────────────────────────────────
//
// Der Satz ist registerhaltig: die Grundlinien liegen auf allen Seiten - und
// damit auch auf Vorder- und Rueckseite eines Blattes - genau uebereinander.
// Im Buchdruck ist das der Regelfall, weil sonst die Zeilen der Rueckseite
// zwischen den Zeilen der Vorderseite durchscheinen und die Seite unruhig
// wirkt.
//
// Dazu muss jeder senkrechte Abstand ein Vielfaches des Zeilenschritts sein.
// `raster` ist dieser Schritt, `raster-phase` der Rest, der nach einem
// vollen Schritt bis zur Oberkante des naechsten Zeilenkastens fehlt - er
// steht deshalb unter jedem Rasterblock.
#let raster = 12.9pt
#let raster-phase = (zeilenabstand - zeilenkasten) * 10pt // 1,12 pt

// Erstzeileneinzug statt Absatzabstand: der klassische deutsche Buchsatz.
// Nach Ueberschriften, Abbildungen und Aufzaehlungen entfaellt er, weil dort
// schon der Umbruch den neuen Absatz anzeigt.
#let absatz-einzug = 1em

// Bildunterschriften stehen einen Grad kleiner als der Flieszttext.
#let beschriftung-groesze = 9pt

// Abstand der Kapitelueberschrift zum Kopfsteg: fuenf Rasterzeilen.
#let kapitel-abstand-oben = 5 * raster

// ── Ueberschriften: Einzuege ──────────────────────────────────────────────
// Nummer steht am Bundsteg, der Titel an einem festen Tabulator; laeuft der
// Titel um, beginnt die Folgezeile bei 16 mm.
#let heading-hang = 16mm
#let heading-tab = ("1": 8mm, "2": 8mm, "3": 10mm, "4": 10mm)
#let heading-size = ("1": 18pt, "2": 12pt, "3": 11pt, "4": 10pt)

// ── Sprachabhaengige Bezeichner ───────────────────────────────────────────
#let bezeichner-state = state("isem-bezeichner", (
  abbildung: "Abbildung",
  tabelle: "Tabelle",
))
#let benenne(abbildung: "Abbildung", tabelle: "Tabelle") = {
  bezeichner-state.update((abbildung: abbildung, tabelle: tabelle))
}
#let wort-abbildung() = bezeichner-state.get().abbildung
#let wort-tabelle() = bezeichner-state.get().tabelle

// ═══ Hilfsmittel ═══════════════════════════════════════════════════════════

/// Legt `inhalt` in einen Block, dessen Hoehe so bemessen ist, dass der
/// folgende Text wieder auf dem Grundlinienraster steht - gleich wie hoch der
/// Inhalt selbst ausfaellt.
///
/// Die Hoehe ist ein Vielfaches des Zeilenschritts abzueglich der
/// Rasterphase: den fehlenden Rest steuert Typst selbst bei, denn zwischen
/// zwei Bloecken steht immer mindestens der Absatzabstand (= die Phase).
/// Dadurch stimmt das Raster sowohl mitten im Text als auch dann, wenn der
/// Block oben auf einer Seite steht und sein Vorlauf entfaellt.
///
/// `luft` ist der Mindestabstand, der unter dem Inhalt frei bleiben soll,
/// bevor auf die naechste Rasterzeile aufgerundet wird.
#let auf-raster(inhalt, luft: 0pt) = layout(groesze => context {
  let hoehe = measure(inhalt, width: groesze.width).height
  let zeilen = calc.max(1, calc.ceil((hoehe + luft + raster-phase - 0.05pt) / raster))
  block(width: 100%, height: zeilen * raster - raster-phase, spacing: 0pt, inhalt)
})

/// Rasterblock mit Vorlauf: `vor` leere Rasterzeilen ueber dem Inhalt.
#let raster-block(inhalt, vor: 1, nach: 0, luft: 0pt, sticky: false) = block(
  above: vor * raster + raster-phase,
  below: nach * raster + raster-phase,
  breakable: false,
  sticky: sticky,
  auf-raster(inhalt, luft: luft),
)

/// Nummer an einem Tabulator, Fortsetzungszeilen haengend eingezogen.
/// Ist die Nummer breiter als der Tabulator, rueckt der Titel nach - so
/// verhaelt sich auch der Tabulator in Word.
#let nummeriert(nummer, titel, tab: 8mm, hang: heading-hang) = context {
  let breite = measure(nummer).width
  set par(hanging-indent: hang, justify: false)
  if breite >= tab {
    [#nummer#h(0.5em)#titel]
  } else {
    [#box(width: tab, nummer)#titel]
  }
}

// Im Anhang werden die Ebene-1-Ueberschriften wie Vorspannteile gesetzt
// (12 pt), aber nummeriert - so zeigt es die Referenz.
#let anhang-modus = state("isem-anhang", false)

// ═══ Mikrotypografie ═══════════════════════════════════════════════════════
//
// Im deutschen Satz steht zwischen den Gliedern einer Abkuerzung, zwischen
// Zahl und Einheit und hinter dem Paragrafenzeichen ein schmales geschuetztes
// Leerzeichen (U+202F). Es haelt "z. B." zusammen, damit die beiden Teile
// nicht auf zwei Zeilen fallen, und ist schmaler als ein Wortzwischenraum.
// Cambria enthaelt das Zeichen.
#let schmalraum = "\u{202F}"

/// Setzt eine mehrgliedrige Abkuerzung neu: "z.B." und "z. B." werden beide
/// zu "z. B." mit schmalem geschuetztem Leerzeichen.
#let mit-schmalraum(t) = {
  let teile = t.replace(regex("[\s\u{00A0}\u{202F}]+"), "").split(".")
  teile.filter(x => x != "").map(x => x + ".").join(schmalraum)
}

/// Name einer zitierten Person in Kapitaelchen.
///
///     #autor[Albers] beschreibt das Modell der SGE.
///
/// Cambria bringt echte Kapitaelchen mit (OpenType `smcp`); die Vorlage
/// nutzt sie dort, wo Word in der Referenz Versalien setzt.
/// Quellenangabe innerhalb einer Fusznote.
///
/// Der Zitierstil ist ein Notenstil: ein gewoehnliches Zitat erzeugt selbst
/// eine Fusznote und wuerde in einer Fusznote eine zweite verschachteln.
/// Die Prosaform vermeidet das, setzt das Jahr aber in Klammern - im
/// Flieszttext steht es dagegen mit Komma abgetrennt. Autor und Jahr
/// einzeln abgerufen ergeben genau die Form des Flieszttextes.
#let quelle(schluessel) = [#cite(schluessel, form: "author"), #cite(schluessel, form: "year")]

#let autor(name) = text(tracking: 0.02em, smallcaps(name))

// ═══ Kopfzeile ═════════════════════════════════════════════════════════════

/// Wahr, wenn die laufende Seite eine rechte (ungerade) Seite ist. Auch die
/// Onlinefassung wird doppelseitig gesetzt - die Referenz ist es ebenfalls.
#let page-is-odd() = calc.odd(here().page())

#let kopf-linie() = line(length: 100%, stroke: 0.45pt + schwarz)

/// Beginnt auf dieser Seite ein Kapitel? Dann bleibt der Seitenkopf leer.
#let oeffnet-kapitel() = {
  let cur = here().page()
  query(<isem-kapitelanfang>).any(m => m.location().page() == cur)
}

/// Beginnt auf dieser Seite ein Vorspann- oder Nachspannteil? Dann steht
/// im Kopf nur die Seitenzahl - so wie in der Referenz bei Kurzfassung,
/// Anhang, Literaturverzeichnis und den Verzeichnissen.
#let oeffnet-abschnitt() = {
  let cur = here().page()
  query(<isem-abschnittsanfang>).any(m => m.location().page() == cur)
}

/// Kopfzeile des Hauptteils.
///   linke Seite:   Seitenzahl auszen, Kapitelnummer und -titel innen
///   rechte Seite:  Abschnittsnummer und -titel innen, Seitenzahl auszen
#let laufender-kopf() = context {
  if oeffnet-kapitel() { return [] }
  if page.numbering == none { return [] }

  let odd = page-is-odd()
  if oeffnet-abschnitt() {
    let zahl = counter(page).display()
    return block(width: 100%, {
      set text(size: 8pt)
      set block(spacing: 0pt)
      set par(spacing: 0pt)
      if odd { align(right, zahl) } else { align(left, zahl) }
      v(0.42mm, weak: false)
      kopf-linie()
    })
  }
  // Links steht das Kapitel, rechts der zuletzt begonnene Abschnitt.
  let ebenen = if odd {
    heading.where(level: 1).or(heading.where(level: 2))
  } else {
    heading.where(level: 1)
  }
  let vorher = query(ebenen.before(here()))
  let titel = if vorher.len() == 0 {
    []
  } else {
    let u = vorher.last()
    let nummer = if u.numbering != none {
      numbering(u.numbering, ..counter(heading).at(u.location())) + h(0.7em)
    } else { [] }
    [#nummer#u.body]
  }
  let zahl = counter(page).display()

  block(width: 100%, {
    set text(size: 8pt)
    set block(spacing: 0pt)
    set par(spacing: 0pt, leading: leading-em)
    if odd {
      grid(columns: (1fr, auto), column-gutter: 1em, titel, zahl)
    } else {
      grid(columns: (auto, 1fr), column-gutter: 1em, zahl, align(right, titel))
    }
    v(0.42mm, weak: false)
    kopf-linie()
  })
}

/// Kopfzeile der Titelei und der Verzeichnisse: nur die Seitenzahl, auszen.
#let titelei-kopf() = context {
  if page.numbering == none { return [] }
  let zahl = counter(page).display()
  block(width: 100%, {
    set text(size: 8pt)
    set block(spacing: 0pt)
    set par(spacing: 0pt)
    if page-is-odd() { align(right, zahl) } else { align(left, zahl) }
    v(0.42mm, weak: false)
    kopf-linie()
  })
}

// ═══ Grundeinrichtung ══════════════════════════════════════════════════════

#let configure(meta, body) = {
  set document(title: meta.title, author: meta.name)

  set text(
    font: body-font,
    size: 10pt,
    fill: schwarz,
    top-edge: text-top-edge,
    bottom-edge: text-bottom-edge,
  )
  set par(
    justify: true,
    leading: leading-em,
    // Zwischen zwei Absaetzen steht nur die Rasterphase: die Grundlinien
    // ruecken damit um genau einen Zeilenschritt weiter.
    spacing: raster-phase,
    first-line-indent: (amount: absatz-einzug, all: false),
  )
  // Alle Linien und Flaechen erben die Prozessfarbe. Ohne das setzte Typst
  // sie als DeviceGray, und die Trennung ueber das ICC-Profil machte daraus
  // vierfarbiges Schwarz - im Buch ein Fehler. Wer im Text nur eine Staerke
  // angibt (`stroke: 0.5pt`), bekommt die Farbe von hier.
  // Nur dort, wo Typst ohnehin eine schwarze Linie zeichnet, wird die
  // Prozessfarbe gesetzt - sonst entstuenden Rahmen, wo keine sein sollen.
  // Alles andere (`rect`, `grid`, eigene Striche) braucht die Farbe
  // ausdruecklich: `stroke: 0.5pt + schwarz`. tools/pruefen.py meldet, wo
  // sie fehlt.
  set line(stroke: 1pt + schwarz)
  set table(stroke: 1pt + schwarz)

  // ── Schmale geschuetzte Leerzeichen ─────────────────────────────────────
  // Mehrgliedrige Abkuerzungen. Die laengste Form steht zuerst, damit
  // "i. d. R." nicht als "d. h." missverstanden wird.
  show regex(
    "\b(?:i\.\s?d\.\s?R|u\.\s?s\.\s?w|d\.\s?h|z\.\s?B|z\.\s?T"
      + "|u\.\s?a|u\.\s?U|u\.\s?Ä|o\.\s?Ä|v\.\s?a|s\.\s?o|s\.\s?u"
      + "|n\.\s?Chr|v\.\s?Chr|i\.\s?A|m\.\s?E)\.",
  ): it => mit-schmalraum(it.text)

  // Einzelne Abkuerzung vor dem, worauf sie sich bezieht.
  show regex(
    "\b(?:Nr|Bd|Abb|Tab|Kap|Gl|Anh|Hrsg|Prof|Dipl|vgl|ca|ggf|evtl|Art|Abs"
      + "|Aufl|Jh|St|Zt)\.[ \u{00A0}]",
  ): it => it.text.trim() + schmalraum

  // Zahl und Einheitenzeichen. Ohne Wortgrenze am Ende, sonst greift die
  // Regel bei "15 %," nicht - hinter dem Prozentzeichen steht kein Buchstabe.
  show regex("[0-9][ \u{00A0}](?:%|‰|°C|°|€)"): it => (
    it.text.replace(regex("[ \u{00A0}]"), schmalraum)
  )

  // Zahl und Einheit in Buchstaben. Bewusst ohne mehrdeutige Kuerzel wie
  // "a" (Jahr) oder "d" (Tag), die auch Woerter sein koennen.
  show regex(
    "[0-9][ \u{00A0}](?:EUR|mm|cm|dm|km|µm|nm|kg|mg|kN|Nm|kWh|MWh"
      + "|kW|MW|Wh|kHz|MHz|Hz|kPa|MPa|GPa|Pa|bar|ml|dpi|min|ms|kB|MB|GB|TB"
      + "|m|g|t|s|h|W|V|A|N|l)\b",
  ): it => it.text.replace(regex("[ \u{00A0}]"), schmalraum)

  // Paragrafenzeichen und Datumsangaben.
  show regex("§§?[ \u{00A0}]"): it => it.text.trim() + schmalraum
  show regex(
    "\b[0-9]{1,2}\.[ \u{00A0}](?:Januar|Februar|März|April|Mai|Juni|Juli"
      + "|August|September|Oktober|November|Dezember)\b",
  ): it => it.text.replace(regex("[ \u{00A0}]"), schmalraum)

  // Umbruchqualitaet. Typst bricht den ganzen Absatz auf einmal um; mit
  // erhoehten Kosten fuer Schusterjungen, Hurenkinder und einzelne Woerter
  // in der letzten Zeile wird der Satz ruhiger, als Word ihn liefert.
  set text(costs: (
    hyphenation: 120%, // Trennungen sparsamer setzen
    runt: 400%, // keine Restzeile mit einem einzelnen Wort
    widow: 400%, // keine Anfangszeile allein am Seitenfusz
    orphan: 400%, // keine Schluszzeile allein am Seitenkopf
  ))

  set page(
    width: seiten-breite,
    height: seiten-hoehe,
    margin: if ist-druck {
      (
        inside: inner-margin,
        outside: outer-margin,
        top: page-top-margin,
        bottom: page-bottom-margin,
      )
    } else {
      (
        left: online-margin,
        right: online-margin,
        top: page-top-margin,
        bottom: page-bottom-margin,
      )
    },
    numbering: none,
    header: laufender-kopf(),
    header-ascent: header-ascent,
    footer: none,
  )

  // ── Listen ──────────────────────────────────────────────────────────────
  // Aufzaehlungszeichen und Nummern tragen die Hausfarbe - wie die
  // Bezeichner der Abbildungen und die Fusznotenlinie.
  set list(
    indent: absatz-einzug,
    body-indent: 0.55em,
    spacing: raster-phase,
    marker: (
      text(fill: accent, sym.bullet),
      text(fill: accent, sym.dash.en),
      text(fill: accent, sym.ast.basic),
    ),
  )
  set enum(
    indent: absatz-einzug,
    body-indent: 0.55em,
    spacing: raster-phase,
    numbering: (..n) => text(fill: accent, numbering("1.", ..n.pos())),
  )
  show list: set block(above: raster-phase, below: raster-phase)
  show enum: set block(above: raster-phase, below: raster-phase)

  // ── Ueberschriften ──────────────────────────────────────────────────────
  // Ebene 1 wird von `kapitel()` gesetzt und ist hier nur verborgen
  // vorhanden; die Ebenen 2 bis 4 folgen dem Muster der Referenz.
  // Ebene 1 traegt drei Gestalten: Kapitel (18 pt, tief auf der Seite),
  // Anhangteil und Vorspannteil (beide 12 pt am Kopfsteg). Alle drei sind
  // echte Ueberschriften - fuer die Gliederung im PDF, fuer den laufenden
  // Kolumnentitel und fuer PDF/UA, das eine lueckenlose Hierarchie verlangt.
  show heading.where(level: 1): it => context {
    let nummer = if it.numbering != none {
      counter(heading).display(it.numbering)
    } else { none }
    let im-anhang = anhang-modus.get()
    let groesze = if nummer != none and not im-anhang { 18pt } else { 12pt }
    let koerper = text(font: display-font, size: groesze, weight: "bold", {
      if nummer == none {
        set par(justify: false, hanging-indent: heading-hang, first-line-indent: 0pt)
        it.body
      } else {
        nummeriert(
          nummer,
          it.body,
          tab: if groesze == 18pt { heading-tab.at("1") } else { heading-tab.at("2") },
        )
      }
    })
    if groesze == 18pt { v(kapitel-abstand-oben, weak: false) }
    raster-block(vor: 0, luft: 6pt, sticky: true, koerper)
  }

  show heading.where(level: 2).or(heading.where(level: 3)).or(heading.where(level: 4)): it => {
    let stufe = calc.min(it.level, 4)
    let groesze = heading-size.at(str(stufe), default: 10pt)
    // Eine Rasterzeile Vorlauf, der Rest wird auf volle Zeilen aufgerundet;
    // `sticky` haelt die Ueberschrift beim folgenden Text.
    raster-block(vor: 1, luft: 6pt, sticky: true,
      text(font: display-font, size: groesze, weight: "bold", {
        if it.numbering != none {
          nummeriert(
            counter(heading).display(it.numbering),
            it.body,
            tab: heading-tab.at(str(stufe), default: 8mm),
          )
        } else {
          set par(justify: false, hanging-indent: heading-hang, first-line-indent: 0pt)
          it.body
        }
      }))
  }

  // ── Abbildungen und Tabellen ────────────────────────────────────────────
  set figure(numbering: n => context numbering(
    "1.1",
    counter(heading).get().first(),
    n,
  ))
  // Abbildung samt Beschriftung belegt volle Rasterzeilen, damit der Text
  // darunter wieder auf dem Raster steht.
  set figure(gap: raster - raster-phase)
  show figure: it => raster-block(vor: 1, nach: 1, luft: 0pt, it)
  show figure.where(kind: table): set figure.caption(position: top)

  // Die Beschriftung ist kein Flieszttext: sie steht einen Grad kleiner,
  // ohne Blocksatz und mit haengendem Einzug, damit sie sich auch bei
  // mehreren Zeilen klar vom Text daneben absetzt.
  show figure.caption: it => context {
    set align(left)
    set text(size: beschriftung-groesze)
    set par(
      justify: false,
      leading: leading-em,
      hanging-indent: 0pt,
      first-line-indent: 0pt,
    )
    block(width: 100%, {
      text(fill: label-color, weight: "bold", [#it.supplement #it.counter.display(it.numbering)])
      h(0.45em)
      it.body
    })
  }

  // Verweise auf Abbildungen und Tabellen erscheinen fett in Petrol,
  // Verweise auf Kapitel und Abschnitte bleiben schwarz.
  show ref: it => {
    let el = it.element
    if el != none and el.func() == figure {
      text(fill: label-color, weight: "bold", it)
    } else {
      it
    }
  }

  // ── Fusznoten ───────────────────────────────────────────────────────────
  set footnote.entry(
    // Die Trennlinie bekommt etwas Luft nach unten, sonst klebt der erste
    // Eintrag daran.
    separator: pad(bottom: 3.5pt, line(length: 2in, stroke: 0.5pt + accent)),
    clearance: 16pt,
    gap: 0pt,
    // Die Referenz setzt hinter die Ziffer nur einen schmalen Zwischenraum,
    // keinen haengenden Einzug.
    indent: 4pt,
  )
  show footnote.entry: it => {
    set text(size: 9pt)
    set par(justify: false, leading: leading-em, spacing: 0pt, hanging-indent: 0pt)
    it
  }

  // ── Formeln ─────────────────────────────────────────────────────────────
  // Nummeriert wird nur, was ausdruecklich mit `numbered-equation` gesetzt
  // wird - abgesetzte Formeln ohne Nummer bleiben ohne.
  show math.equation.where(block: true): it => raster-block(vor: 1, it)

  body
}

// ═══ Bausteine ═════════════════════════════════════════════════════════════

/// Ueberschrift eines Vorspann- oder Nachspannteils: 12 pt fett, direkt am
/// Kopfsteg. `verzeichnet: true` nimmt den Teil ins Inhaltsverzeichnis auf -
/// so wie es die Referenz fuer Anhang, Literatur- und Verzeichnisteile tut,
/// nicht aber fuer Kurzfassung, Abstract, Vorwort und Danksagung.
#let front-heading(title, verzeichnet: false) = [
  #pagebreak(weak: true, to: "odd")
  #metadata("abschnittsanfang")<isem-abschnittsanfang>
  #heading(level: 1, outlined: verzeichnet, numbering: none, bookmarked: true)[#title]
]

/// Kapitelanfang: rechte Seite, kein Seitenkopf, 18 pt fett, fuenf
/// Rasterzeilen unter dem Kopfsteg.
///
///     #kapitel("Einleitung", "1", kennung: "kap-einleitung")[..]
#let kapitel(title, number: none, body, kennung: none) = [
  // Jedes Kapitel beginnt auf einer rechten Seite. `weak` verhindert einen
  // zweiten Umbruch, wenn die Seite ohnehin frisch ist.
  #pagebreak(weak: true, to: "odd")
  #metadata("kapitelanfang")<isem-kapitelanfang>
  #counter(math.equation).update(0)
  #counter(figure.where(kind: image)).update(0)
  #counter(figure.where(kind: table)).update(0)
  #[#heading(level: 1)[#title]#if kennung != none { label(kennung) }]
  #body
]
// Alter Name, damit bestehende Dateien weiter uebersetzen.
#let chapter = kapitel

/// Inhaltsverzeichnis im Zuschnitt der Referenz: Ebene 1 fett, Punktlinie,
/// Seitenzahl rechtsbuendig.
#let contents-page(titel: "Inhaltsverzeichnis") = [
  #front-heading(titel, verzeichnet: true)
  #context {
    let eintraege = query(selector(heading)).filter(it => it.outlined and it.level <= 3)
    // Auch das Verzeichnis steht auf dem Raster: jede Zeile ein Schritt,
    // vor einem Kapitel zusaetzlich eine leere Zeile.
    set par(leading: leading-em, first-line-indent: 0pt)
    let einzug = (
      "1": (nummer: 0mm, text: 5mm, oben: raster + raster-phase),
      "2": (nummer: 5mm, text: 12mm, oben: raster-phase),
      "3": (nummer: 12mm, text: 21mm, oben: raster-phase),
    )
    for e in eintraege {
      let s = einzug.at(str(e.level))
      let nummer = if e.numbering != none {
        numbering(e.numbering, ..counter(heading).at(e.location()))
      } else { none }
      let seite = counter(page).at(e.location()).first()
      // Der haengende Einzug wird unmittelbar am Absatz gesetzt, nicht
      // ueber eine set-Regel: sonst greift er innerhalb von `pad` nicht,
      // und die zweite Zeile eines langen Titels rutscht unter die Nummer
      // statt unter den Titel.
      let zeile = pad(left: s.nummer, par(
        justify: false,
        leading: leading-em,
        first-line-indent: 0pt,
        hanging-indent: s.text - s.nummer,
        {
          if nummer != none {
            box(width: s.text - s.nummer, nummer)
          }
          e.body
          box(width: 1fr, inset: (x: 0.4em), repeat(justify: false, [.]))
          [#seite]
        },
      ))
      block(
        above: s.oben,
        below: 0pt,
        width: 100%,
        link(e.location(), if e.level == 1 { strong(zeile) } else { zeile }),
      )
    }
  }
]

/// Abbildungs- oder Tabellenverzeichnis. `art` ist `image` oder `table`.
#let list-page(title, art, kind-name) = [
  #front-heading(title, verzeichnet: true)
  #context {
    let eintraege = query(figure.where(kind: art)).filter(f => f.caption != none)
    if eintraege.len() == 0 [
      #emph[Noch keine Einträge.]
    ] else {
      for e in eintraege {
        let ort = e.location()
        let nummer = numbering(
          "1.1",
          counter(heading).at(ort).first(),
          counter(figure.where(kind: art)).at(ort).first(),
        )
        block(above: raster-phase, below: 0pt, width: 100%, {
          set par(justify: false, hanging-indent: 21mm, leading: leading-em,
                  first-line-indent: 0pt)
          link(ort, {
            text(fill: label-color, weight: "bold")[#kind-name #nummer]
            h(0.45em)
            e.caption.body
            box(width: 1fr, inset: (x: 0.4em), repeat(justify: false, [.]))
            [#counter(page).at(ort).first()]
          })
        })
      }
    }
  }
]

/// Glossar: Verzeichnis der nummerierten Definitionen.
///
/// Gebaut wie die uebrigen Verzeichnisse, nur dass die Eintraege nicht aus
/// Abbildungen stammen, sondern aus den Marken der Definitionskaesten.
#let definitionen-page(titel: "Glossar") = [
  #front-heading(titel, verzeichnet: true)
  #context {
    let eintraege = query(<isem-definition>)
    if eintraege.len() == 0 [
      #emph[Noch keine Definitionen.]
    ] else {
      for e in eintraege {
        let ort = e.location()
        block(above: raster-phase, below: 0pt, width: 100%, {
          set par(justify: false, hanging-indent: 21mm, leading: leading-em,
                  first-line-indent: 0pt)
          link(ort, {
            text(fill: label-color, weight: "bold")[Definition #e.value.nummer]
            h(0.45em)
            e.value.titel
            box(width: 1fr, inset: (x: 0.4em), repeat(justify: false, [.]))
            [#counter(page).at(ort).first()]
          })
        })
      }
    }
  }
]

/// Abkuerzungs- oder Formelzeichenverzeichnis.
#let acronym-page(items, titel: "Abkürzungsverzeichnis") = [
  #front-heading(titel, verzeichnet: true)
  #table(
    columns: (28mm, 1fr),
    inset: (x: 0pt, y: 0pt),
    row-gutter: raster-phase,
    stroke: none,
    ..items.flatten(),
  )
]

/// Literaturverzeichnis. Der Koerper wird uebergeben, damit der
/// `bibliography()`-Aufruf in main.typ stehen bleibt - Typst loest den Pfad
/// relativ zur aufrufenden Datei auf.
#let bibliography-page(body, titel: "Literaturverzeichnis") = [
  #front-heading(titel, verzeichnet: true)
  // Literaturangaben stehen dicht: der haengende Einzug trennt sie schon
  // deutlich genug, eine leere Zeile dazwischen zoege das Verzeichnis nur
  // unnoetig in die Laenge.
  #set par(spacing: raster-phase, justify: false, first-line-indent: 0pt)
  #body
]

/// Anhangteil: wie eine Vorspann-Ueberschrift gesetzt (12 pt fett), aber
/// nummeriert und im Inhaltsverzeichnis gefuehrt - so zeigt es die Referenz.
#let anhang-teil(title, number: none, body, kennung: none) = [
  #pagebreak(weak: true, to: "odd")
  #metadata("abschnittsanfang")<isem-abschnittsanfang>
  #counter(math.equation).update(0)
  #counter(figure.where(kind: image)).update(0)
  #counter(figure.where(kind: table)).update(0)
  #[#heading(level: 1)[#title]#if kennung != none { label(kennung) }]
  #body
]

/// Schaltet auf Anhangsatz um: ab hier werden Ebene-1-Ueberschriften wie
/// Vorspannteile gesetzt, aber weiter nummeriert.
#let anhang-beginn() = anhang-modus.update(true)

/// Freier Vorspann-/Nachspannteil ohne Verzeichniseintrag.
#let textseite(titel, body, verzeichnet: false) = [
  #front-heading(titel, verzeichnet: verzeichnet)
  #body
]

// ═══ Auszeichnungen im Text ════════════════════════════════════════════════

/// Abbildung, die sicher auf die Seite passt: skaliert auf Satzbreite und
/// begrenzt die Hoehe, falls das Bild sonst ueber den Satzspiegel liefe.
#let max-abbildungshoehe = page-body-height - 40mm
#let abbildung(pfad, hoehe: max-abbildungshoehe, alt: none) = layout(verfuegbar => {
  let bild = image(pfad, width: verfuegbar.width, alt: alt)
  let gemessen = measure(bild)
  if gemessen.height > hoehe {
    image(pfad, height: hoehe, alt: alt)
  } else {
    bild
  }
})

/// Zwischentitel: eine fette Zeile, die einen Abschnitt gliedert, ohne
/// eine Ueberschrift zu sein.
///
/// Fuer Zwischenstufen, die weder ins Inhaltsverzeichnis noch in die
/// Gliederung gehoeren. Eine echte Ueberschrift waere hier falsch: sie
/// risse eine Luecke in die Ebenenfolge, und PDF/UA verlangt eine
/// lueckenlose Hierarchie ("skipped from heading level 2 to 4").
#let zwischentitel(body) = raster-block(vor: 1, luft: 4pt, sticky: true, {
  set par(justify: false, first-line-indent: 0pt)
  text(font: display-font, size: 10pt, weight: "bold", body)
})

/// Formel, die als Bild vorliegt - etwa aus einem zurueckgelesenen Altband.
///
/// Sie wird auf 300 dpi skaliert, mittig gestellt und belegt volle
/// Rasterzeilen. `alt` ist Pflicht, sobald die Archivfassung (PDF/UA)
/// gebaut wird.
#let formelbild(pfad, alt: none) = raster-block(vor: 1, luft: 0pt, context {
  let bild = image(pfad, alt: alt)
  let masz = measure(bild)
  // Die Bilder liegen in 300 dpi vor; 1 Bildpunkt entspricht 72/300 pt.
  align(center, image(pfad, alt: alt, height: masz.height * 72 / 300))
})

/// Kasten fuer Definitionen: duenne Petrol-Linie links.
/// Zaehler der Definitionen. Sie laufen durch das ganze Buch, nicht
/// kapitelweise - so fuehrt es auch das Glossar.
#let definitionszaehler = counter("isem-definition")

/// Definitionskasten mit Titel.
///
///     #definitionsbox[Zielsystem][Ein vollstaendiges Zielsystem ...]
///
/// Die Nummer setzt der Kasten selbst. Er legt ausserdem eine Marke ab, aus
/// der das Glossar Nummer, Titel und Seite liest.
#let definitionsbox(titel, body) = raster-block(vor: 1, luft: 0pt, block(
  width: 100%,
  spacing: 0pt,
  inset: (left: 3mm, top: raster - raster-phase, bottom: raster - raster-phase),
  stroke: (left: 1pt + accent),
  {
    // Im Kasten stehen die Absaetze eine Rasterzeile auseinander.
    set par(first-line-indent: 0pt, spacing: raster + raster-phase)
    definitionszaehler.step()
    context [
      #metadata((
        nummer: definitionszaehler.get().first(),
        titel: titel,
      )) <isem-definition>
      #strong[Definition #definitionszaehler.display("1"): #titel]
    ]
    parbreak()
    body
  },
))

/// Nummerierte Gleichung, kapitelweise gezaehlt.
#let gleichungs-nummer = n => context numbering(
  "(1.1)",
  counter(heading).get().first(),
  n,
)
#let numbered-equation(body, alt: none) = math.equation(
  block: true,
  numbering: gleichungs-nummer,
  alt: alt,
  body,
)

/// Formelzeichen oder eingebettete Formel mit Textalternative.
/// Fuer PDF/UA muss jede Formel beschrieben sein - Screenreader lesen sonst
/// nichts vor.
///
///     #mathe($E$, alt: "E")
#let mathe(inhalt, alt: none) = math.equation(alt: alt, inhalt)

/// Unterschriftenzeile.
#let unterschrift(links, rechts) = block(width: 100%, above: 20pt)[
  #grid(columns: (1fr, 1fr), column-gutter: 8mm, links, rechts)
]
