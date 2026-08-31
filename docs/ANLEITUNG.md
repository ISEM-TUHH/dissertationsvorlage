---
titel: ISEM-Dissertationsvorlage (Typst)
zweck: Dissertation nach TUHH-Vorgaben setzen, als Buch drucken lassen und online bereitstellen
zielgruppe: Promovierende am ISEM, auch ohne Typst-Vorkenntnisse
stand: 2026-08-31
---

# ISEM-Dissertationsvorlage

Diese Vorlage setzt eine Dissertation nach den Formalia der TUHH und erzeugt
daraus drei Dinge:

| Was | Datei | wofür |
|---|---|---|
| Umschlag | `build/Druckversion/umschlag.pdf` | an die Druckerei |
| Innenteil | `build/Druckversion/innenteil.pdf` | an die Druckerei |
| Gesamtdatei | `build/Onlineversion/dissertation.pdf` | zum Lesen, Verschicken, Hochladen |

Wenn du noch nie mit Typst gearbeitet hast: Arbeite Kapitel 1 bis 4 einmal
durch. Danach brauchst du im Alltag nur noch zwei Dateien und einen Befehl.

---

## 1. Was Typst ist — und was das für dich heißt

Typst ist ein Satzprogramm. Du schreibst Text in einfachen Textdateien, und
Typst macht daraus ein PDF. Anders als in Word siehst du beim Schreiben kein
Layout, sondern nur deinen Text plus ein paar Markierungen. Das Layout steckt
in der Vorlage und ist überall gleich — genau das ist der Vorteil: Es kann
nicht passieren, dass eine Überschrift plötzlich anders aussieht als die
anderen.

Was du dir merken musst:

```typst
== Eine Überschrift der Ebene 2        // = wäre Ebene 1, === wäre Ebene 3
*fett*  _kursiv_
@quelle2024                            // ein Literaturverweis
@abb-schema                            // ein Verweis auf eine Abbildung
```

Mehr braucht es für den Anfang nicht.

---

## 2. Installation

### 2.1 Typst

Windows, in PowerShell:

```powershell
winget install --id Typst.Typst
```

Danach **PowerShell neu öffnen** und prüfen:

```powershell
typst --version
```

> **Fallstrick:** Wenn `typst` nicht gefunden wird, hat das neue Fenster den
> aktualisierten Suchpfad noch nicht. Fenster schließen, neu öffnen.

### 2.2 Python (für die Prüfskripte und die Druckdateien)

```powershell
winget install --id Python.Python.3.12
pip install pymupdf
```

### 2.3 Ghostscript (nur für die Druckdatei des Innenteils)

Wandelt die Farben nach CMYK. Ohne Ghostscript entsteht die Druckdatei
trotzdem, bleibt aber in RGB — das reicht zum Anschauen, nicht für die
Druckerei.

Ghostscript gibt es nicht über winget. Installer von der offiziellen Seite
holen und ausführen:

<https://ghostscript.com/releases/gsdnld.html> → *Ghostscript AGPL Release*,
64-bit-Installer für Windows.

Prüfen (neues PowerShell-Fenster):

```powershell
gswin64c --version
```

Findet PowerShell den Befehl nicht, liegt Ghostscript trotzdem meist unter
`C:\Program Files\gs\gs<version>\bin\` — die Vorlage sucht dort auch
selbst nach. Fehlt es ganz, sagt das Skript beim Bauen Bescheid und erzeugt
die Druckdatei in RGB statt CMYK.

### 2.4 Schriften

Die Vorlage setzt in **Cambria** — der Schrift, in der auch die
Referenzfassung der Reihe gesetzt ist. Cambria gehört zu Microsoft Office
und ist auf den meisten Arbeitsplätzen vorhanden. Prüfen:

```powershell
typst fonts | Select-String Cambria
```

Erwartet werden zwei Einträge: `Cambria` und `Cambria Math`.

> **Fallstrick:** Findet Typst die Schrift nicht, setzt es stillschweigend
> eine Ersatzschrift — das PDF sieht dann falsch aus, ohne dass eine
> Fehlermeldung kommt. Deshalb: einmal `typst fonts` prüfen. Fehlt Cambria,
> hilft eine Office-Installation oder das Nachinstallieren der
> „ClearType-Schriftartensammlung".

Zusätzlich verwendet die Vorlage **Bahnschrift** (bei Windows dabei) für den
Umschlag und **Cambria Math** für Formeln.

### 2.5 Farbprofil

`template/ISOcoated_v2_300_eci.icc` liegt bei und gehört dazu. Es ist die
Ausgabebedingung, für die WirMachenDruck produziert: Ghostscript trennt damit
nach CMYK, und die Druckdateien tragen es als *OutputIntent* eingebettet.
Ohne diese Datei bauen die Skripte trotzdem durch, rechnen die Farben dann
aber mit dem Ghostscript-Standard und sagen es in der Ausgabe.

### 2.6 Editor

Empfehlung: **Visual Studio Code** mit der Erweiterung **Tinymist Typst**.
Die zeigt das PDF live neben dem Text an.

```powershell
winget install --id Microsoft.VisualStudioCode
code --install-extension myriad-dreamin.tinymist
```

---

## 3. Der erste Durchlauf

Alles bauen:

```powershell
cd "C:\Arbeitsordner\ISEM Dissertationsvorlage Typst"
.\bauen.ps1          # unter macOS/Linux: ./bauen.sh
```

Das dauert ein paar Sekunden und erzeugt alle PDF. Am Ende siehst du
Prüfberichte — die solltest du lesen, dazu Kapitel 7.

Nur den Innenteil bauen, während du schreibst:

```powershell
cd inhalt
typst watch --root .. main.typ ../build/Onlineversion/innenteil.pdf
```

`watch` baut bei jedem Speichern neu. Mit Strg+C beenden.

> **Fallstrick:** Das `--root ..` ist Pflicht. Deine Hauptdatei liegt in
> `inhalt/`, die Vorlage in `template/` — Typst darf standardmäßig aber nur
> auf den Ordner der Hauptdatei zugreifen. `--root ..` macht das ganze
> Repositorium zur Wurzel. Wer in VS Code den Repositoriumsordner öffnet,
> braucht nichts weiter: Tinymist nimmt den Arbeitsbereich als Wurzel.

### 3.1 Fork und Vorlagen-Updates

Die Trennung in `inhalt/` (deine Arbeit) und `template/` (die Vorlage) ist
dafür gemacht, dass du dieses Repositorium **forkst** und die Vorlage
während der Schreibzeit aktuell halten kannst:

```powershell
git remote add vorlage https://github.com/ISEM-TUHH/dissertationsvorlage.git   # einmalig
git fetch vorlage
git merge vorlage/main
```

Verbesserungen an der Vorlage betreffen nur `template/` (und gelegentlich
die Bau-Skripte und diese Anleitung) — deine Dateien in `inhalt/` bleiben
beim Merge unberührt. Konflikte kann es nur geben, wenn du selbst in
`template/` etwas geändert hast; genau deshalb gilt: in `template/` wird
nichts angepasst. Fehlt dir dort etwas, mach ein Issue daraus — dann bekommt
es jede zukünftige Arbeit.

---

## 4. Wo du was einträgst

Alles, was zu deiner Arbeit gehört, liegt in **`inhalt/`** — die Vorlage
selbst in `template/`, und dort änderst du nichts. Im Alltag brauchst du
**zwei Dateien**:

| Datei | Inhalt |
|---|---|
| `inhalt/angaben.typ` | alles über die Arbeit: Titel, Name, Gutachter, Fassung, Schlagworte, welche Verzeichnisse |
| `inhalt/buchdaten.typ` | alles über das Buch: Bandnummer, Seitenzahl, Rückentext |

Titel, Name und Schlagworte aus `angaben.typ` landen zugleich in den
**PDF-Metadaten** aller erzeugten Dateien — Repositorien und Suchmaschinen
lesen sie aus.

Der Text selbst steht in:

```
inhalt/kapitel/01_einleitung.typ      ein Kapitel je Datei
inhalt/anhang/A_ergaenzungen.typ
inhalt/titelei/vorwort.typ            Vorwort, Danksagung, Zusammenfassung …
inhalt/literatur.bib                  die Quellen
inhalt/abbildungen/                   Bilddateien
inhalt/main.typ                       Reihenfolge deiner Kapitel und Anhänge
```

Ein neues Kapitel: Datei in `inhalt/kapitel/` anlegen (erste Zeile
`#import "/template/innenteil/isem.typ": *`) und in `inhalt/main.typ` eine
Zeile in die Kapitelliste eintragen — Titel, Kennung, Datei.

### 4.1 Die wichtigste Variable: `fassung`

In `inhalt/angaben.typ`:

```typst
fassung: "eingereicht",   // oder "genehmigt"
```

Die TUHH kennt genau zwei Fassungen, und sie unterscheiden sich nicht im
Inhalt, sondern im Vorspann:

| | `"eingereicht"` (Gutachterfassung) | `"genehmigt"` (Veröffentlichung) |
|---|---|---|
| Deckblatt | „**Dem** Promotionsausschuss … **vorgelegte** Dissertation" | „**Vom** Promotionsausschuss … **genehmigte** Dissertation" |
| Deckblattrückseite | nicht vorgesehen | **Pflicht**: Gutachtende + Tag der mündlichen Prüfung |
| Jahreszahl | Jahr der Einreichung | Jahr der **Veröffentlichung**, nicht der Prüfung |
| Betreuung auf dem Deckblatt | ja | nein |
| Vorwort, Danksagung, Widmung, Motto | **verboten** | erlaubt |
| Zusammenfassung | **Pflicht** | erlaubt |
| Lebenslauf | **Pflicht**, letzte bedruckte Seite | optional |

Du musst dir das nicht merken: Wenn du etwas einschaltest, das in der
gewählten Fassung nicht zulässig ist, bricht Typst mit einer Meldung ab, die
sagt, was zu tun ist. Beispiel:

```
error: angaben.typ: Vorwort ist in der eingereichten Fassung nicht zulässig
       (TUHH-Leitfaden: kein persönlicher Vorspann).
       mit_vorwort auf false setzen oder fassung auf "genehmigt" ändern.
```

### 4.2 Die übrigen Variablen

Alle Variablen stehen kommentiert in den beiden Dateien. Die, bei denen
erfahrungsgemäß etwas schiefgeht:

| Variable | Achtung |
|---|---|
| `hochschule` | Die Zeile hinter „Vom Promotionsausschuss". Sie wird **gebeugt**: „*der* Technischen Universität Hamburg", aber „*des* Karlsruher Instituts für Technologie". Nur bei Fremdbänden der Reihe zu ändern. |
| `grad` | Genderform **konkret** ausschreiben: „Doktor-Ingenieur" oder „Doktor-Ingenieurin", nie „Doktor-Ingenieur(in)". Die TUHH verlangt das ausdrücklich. |
| `art` | „Monografie" oder „kumulativ" — die Angabe gehört auf das Deckblatt und ist nicht weglassbar. |
| `geburtsort` | Bei Geburt außerhalb Deutschlands **mit Land**: „Baltimore, USA". |
| `jahr` | In der genehmigten Fassung das Jahr der **Veröffentlichung**. Nicht das Jahr der mündlichen Prüfung — ein klassischer Fehler. |
| `seiten` (in `buchdaten.typ`) | Muss der tatsächlichen Seitenzahl des Innenteils entsprechen, sonst stimmt die Rückenstärke nicht. `.\bauen.ps1` prüft das und sagt dir die richtige Zahl. |

---

## 5. Aufbau der Arbeit

Die Reihenfolge ist bewusst so gewählt, dass der Text früh beginnt:

```
Schmutztitel (Reihe, Band, Kurztitel)      ┐  ungezählt
Deckblatt                                  │
Deckblattrückseite (Gutachtende)           │
Impressum der Reihe mit Kolophon           │
Vorwort des Herausgebers                   │  römisch nummeriert
Vorwort zum Band                           │  (I, II, III, …)
Danksagung                                 │
Kurzfassung / Abstract                     │
Motto / Widmung                            │
Inhaltsverzeichnis                         ┘  das einzige Verzeichnis vorn

1  Einleitung                              ┐
2  Stand der Forschung                     │  arabisch, beginnt neu bei 1
3  Zusammenfassung und Ausblick            │
Anhang (Trennseite mit Einführung)         │
  A  Erster Anhang                         │
  B  Zweiter Anhang                        │
Literaturverzeichnis                       │  läuft arabisch weiter —
Studentische Arbeiten im Rahmen der Arbeit │  kein dritter Nummernkreis
Abbildungs-, Tabellenverzeichnis           │
Formelzeichen, Abkürzungen                 │
KI-Erklärung, Eidesstattliche Erklärung    │
Lebenslauf                                 ┘
```

Alles Nachschlagbare steht hinten. Vorn steht nur, was man vor dem Lesen
braucht. Die PDF-Seitenlabels bilden dieselbe Zählung ab: Was im PDF-Reader
als Seitenzahl steht, steht auch gedruckt auf der Seite.

Ein Bestandteil lässt sich in `angaben.typ` an- und abschalten:

```typst
mit_motto: false,
mit_formelzeichen: true,
```

### 5.1 Wie der Satz aufgebaut ist

Der Innenteil ist als Buch gesetzt, nicht als Bericht:

| | Wert | warum |
|---|---|---|
| Format | 148 × 210 mm (A5) | Endformat laut Datenblatt |
| Satzspiegel | 119 × 173 mm, 38 Zeilen | 74 Zeichen je Zeile — im Optimum für Blocksatz |
| Bundsteg / Außensteg | 14 / 15 mm, gespiegelt | außen breiter als innen: die Doppelseite wirkt als Einheit, der Daumen hat Platz. 14 mm Bund sind doppelt so viel wie die 7 mm Falzkante des Hardcovers |
| Kopfsteg / Fußsteg | 16,85 / 20,1 mm | erste Grundlinie auf 20,2 mm |
| Grundschrift | Cambria 10 pt | |
| Zeilenschritt | 12,9 pt | Grundlinienraster |
| Absätze | 1 em Einzug, kein Abstand | klassischer deutscher Buchsatz; nach Überschriften und Abbildungen entfällt der Einzug |

**Registerhaltigkeit.** Alle senkrechten Abstände sind Vielfache von 12,9 pt.
Dadurch liegen die Grundlinien auf jeder Seite — und damit auch auf Vorder-
und Rückseite eines Blattes — genau übereinander. Sonst scheinen die Zeilen
der Rückseite zwischen den Zeilen der Vorderseite durch.

Wer eigene Bausteine baut, setzt sie in `raster-block(...)`; der rundet die
Höhe auf volle Zeilen auf, damit der Text darunter wieder im Raster steht:

```typst
#raster-block(vor: 1, luft: 6pt)[ ... ]
```

**Farben.** Im Druck wird direkt in CMYK gesetzt, nicht nachträglich
umgerechnet. Deshalb gibt es `schwarz`, `weiss`, `grau(30%)` und `accent`
statt `black`, `white` und `luma(...)`:

```typst
#table(stroke: 0.5pt + schwarz, ...)   // richtig
#table(stroke: 0.5pt, ...)             // wird im Druck vierfarbiges Schwarz
```

Der Grund: `black` ist DeviceGray, und die Trennung über das ICC-Profil macht
daraus C 78 / M 68 / Y 58 / K 94. Feine Linien und Schrift werden damit bei
der kleinsten Passerdifferenz unscharf. `template/innenteil/tools/pruefen.py` meldet
so etwas mit Seitenzahl.

### 5.2 Mikrotypografie

Zwei Dinge nimmt die Vorlage dem Schreiben ab:

**Schmale geschützte Leerzeichen.** „z.B." und „z. B." werden beide zu
„z. B." mit einem schmalen geschützten Leerzeichen (U+202F). Dasselbe gilt
für „u. a.", „d. h.", „i. d. R.", für „Abb. 3", „Kap. 2", „Nr. 5",
„Prof. Dr.", für „§ 6", für Zahl und Einheit („15 %", „230 V", „12,5 kg")
und für Datumsangaben („1. Januar 2026"). Die Teile fallen damit nie auf
zwei Zeilen, und der Abstand ist schmaler als ein Wortzwischenraum.

**Kapitälchen für zitierte Personen.** Die Referenz setzt Autornamen im
Fließtext in Versalien. Typografisch richtig sind Kapitälchen, und Cambria
bringt echte mit:

```typst
#autor[Albers] beschreibt das Modell der SGE.
```

### 5.3 Unterschied Druck- und Onlinefassung

Beide entstehen aus derselben Quelle; `--input ausgabe=druck` schaltet um.

Es entstehen **drei** Dateien aus derselben Quelle:

| | `Druckversion/innenteil.pdf` | `Onlineversion/innenteil.pdf` | `Archivversion/innenteil.pdf` |
|---|---|---|---|
| wofür | die Druckerei | lesen und verschicken | TORE und DNB |
| Farbraum | CMYK, ISO Coated v2 300 % (ECI) | RGB | RGB, PDF/A-OutputIntent |
| Schwarz | reines K | Schwarz | Schwarz |
| Seitenformat | 154 × 216 mm mit 3 mm Beschnitt | 148 × 210 mm | 148 × 210 mm |
| Seitenränder | gespiegelt (innen 14, außen 15 mm) | mittig, je 14,5 mm | mittig |
| Umfang | auf ein Vielfaches von 4 aufgefüllt | ohne Vakatseiten | ohne Vakatseiten |
| Verweise | schwarz, aber klickbar | Petrol | Petrol |
| Bildauflösung | 300 dpi | verkleinert | wie gesetzt |
| Standard | — | — | PDF/A-2b + PDF/UA-1 |

Die **Archivfassung** kommt unbearbeitet aus Typst. Jede Nachbearbeitung —
auch ein bloßes Neuspeichern — kann die Konformität brechen, ohne dass die
Datei es noch anzeigt. Deshalb wird sie weder verkleinert noch mit dem
Umschlag zusammengefügt.

Damit PDF/UA gelingt, braucht **jede Abbildung und jede Formel einen
Alternativtext** — auch einzelne Größen im Fließtext (`#mathe($m$, alt: "m")`).
Fehlt er, bricht der Bau mit einer Meldung ab, die die Stelle nennt:

```typst
#figure(abbildung("aufbau.png", alt: "Versuchsstand mit …"),
        caption: [Aufbau des Versuchsstands.])

#numbered-equation($ E = m c^2 $, alt: "E ist gleich m mal c hoch zwei")
```

### 5.4 Abbildungen, Tabellen und Formeln

Abbildungen und Tabellen sind gewöhnliche Typst-`figure`. Die Vorlage
beschriftet sie im Zuschnitt der Reihe: der Bezeichner fett in ISEM-Petrol,
die Nummer kapitelweise gezählt, Abbildungen **unterhalb**, Tabellen
**oberhalb**.

```typst
#figure(
  abbildung("aufbau.png", alt: "Versuchsstand mit …"),
  caption: [Aufbau des Versuchsstands.],
) <abb-aufbau>

#figure(
  table(columns: (1fr, 1fr), [*Merkmal*], [*Wert*], [Masse], [12 kg]),
  caption: [Kenngrößen des Prüflings.],
) <tab-kenngroessen>

#numbered-equation($ E = m c^2 $) <gl-energie>
```

Verwiesen wird mit `@abb-aufbau`; Typst schreibt „Abbildung 2.1" und hält die
Nummer beim Verschieben aktuell. `abbildung(name)` sucht die Datei in
`inhalt/abbildungen/`, skaliert das Bild auf Satzbreite und begrenzt die
Höhe, damit es nicht über den Satzspiegel läuft. Abgesetzte Formeln ohne
`numbered-equation` bleiben ohne Nummer.

**Übernommene Abbildungen brauchen eine Quellenangabe** (das verlangt auch
der TUHH-Leitfaden). Sie gehört mit `#bildquelle(<schlüssel>)` in die
Beschriftung:

```typst
#figure(
  abbildung("systemmodell.png", alt: "…"),
  caption: [Systemmodell nach #autor[Weilkiens].#bildquelle(<weilkiens2014>)],
) <abb-systemmodell>
```

Auf der Seite der Abbildung entsteht daraus die gewohnte Fußnote des
Zitierstils — die Quelle steht also dort, wo die Abbildung steht. Im
Abbildungsverzeichnis hinten wird sie automatisch unterdrückt: dort steht
nur die Beschriftung, keine Quelle und keine Fußnote.

Fachbegriffe lassen sich mit `definitionsbox[…]` hervorheben. Für eine fette
Gliederungszeile, die weder ins Inhaltsverzeichnis noch in die Gliederung
gehört, gibt es `zwischentitel[…]` — eine echte Überschrift wäre dort falsch,
weil sie eine Lücke in die Ebenenfolge risse und PDF/UA abbräche. Formeln, die
nur als Bild vorliegen, setzt `formelbild("pfad", alt: "…")`.

---

## 6. Literatur und Zotero

Die Vorlage zitiert nach dem **ISEM-Zitationsstil**
(`template/ISEM-Zitationsstil.csl`, identisch mit dem Zotero-Stil
„TUHH-ISEM"). Die Quellen stehen in `inhalt/literatur.bib`.

### 6.1 Zotero mit der Vorlage verbinden

Der bequeme Weg ist ein Add-on, das die `.bib`-Datei automatisch aktuell hält:

1. **Better BibTeX installieren**
   [Download](https://retorque.re/zotero-better-bibtex/installation/) →
   in Zotero: *Werkzeuge → Add-ons → Zahnrad → Add-on aus Datei installieren*
   → Zotero neu starten.

2. **Zitierschlüssel festlegen.** In Zotero unter
   *Bearbeiten → Einstellungen → Better BibTeX → Citation keys* das Format
   `auth.lower + year` eintragen. Dann heißt ein Eintrag von Bursac aus 2023
   schlicht `bursac2023` — und genau so zitierst du ihn im Text.

3. **Sammlung exportieren.** Rechtsklick auf deine Sammlung →
   *Export Collection…* → Format **Better BibTeX**, Haken bei
   **Keep updated** → speichern als `inhalt/literatur.bib`.

   Der Haken ist der entscheidende Teil: Zotero schreibt die Datei ab jetzt
   bei jeder Änderung neu. Du musst nie wieder exportieren.

4. **Zitieren.** Im Text:

   ```typst
   Das zeigt sich in mehreren Arbeiten @bursac2023 @mustermann2024.
   ```

### 6.2 Fallstricke bei der Literatur

- **Umlaute:** Better BibTeX schreibt sie korrekt als UTF-8. Wenn du eine
  `.bib` aus einer anderen Quelle nutzt und im PDF `M\"uller` erscheint,
  fehlt die richtige Kodierung.
- **Autorenlisten nicht kürzen.** Die TUHH verbietet „et al." im
  Literaturverzeichnis ausdrücklich. Trage in Zotero alle Autoren ein.
- **DOI entweder überall oder nirgends.** Auch das steht so im TUHH-Leitfaden.
- **Online-Quellen brauchen ein Abrufdatum** (Zotero-Feld *Zugriff*).
- **Keine Insider-Kürzel** für Zeitschriften oder Konferenzen — der volle
  Name muss erkennbar sein.

---

## 7. Was die Prüfskripte machen

`.\bauen.ps1` baut nicht nur, sondern prüft auch. Drei Berichte:

| Skript | prüft |
|---|---|
| `template/cover/tools/pruefen.py` | Umschlagformat, Beschnitt, CMYK, Schrifteinbettung |
| `template/innenteil/tools/pruefen.py` | Innenteilformat, Beschnitt, Sicherheitsabstand, 7 mm Falzkante, Bogenteilung, Bildauflösung, CMYK, reines K, OutputIntent, Lesezeichen |
| `template/innenteil/tools/tuhh_pruefen.py` | die TUHH-Formalia am fertigen PDF |
| `template/innenteil/tools/umbruch_pruefen.py` | Hurenkinder, Schusterjungen, Trennungen über den Seitenumbruch, Trennungsleitern, kurze Schlusszeilen, Bildauflösung |

Für einen aus dem Druck zurückgelesenen Band (siehe `Band000-Bursac/`) kommen
vier weitere Werkzeuge dazu. Sie werden nicht bei jedem Bau aufgerufen,
sondern von Hand, solange der Text noch nachgearbeitet wird:

| Skript | leistet |
|---|---|
| `abgleich.py` | vergleicht den gesetzten Band Wort für Wort mit dem Original-PDF und meldet, was fehlt und was zu viel ist — mit Seitenzahl im Original |
| `textreste_pruefen.py` | findet Narben der Rückwandlung in der Quelle: abgeschnittene Sätze, Bildbeschriftungen im Fließtext, Definitionen ohne Kasten, offene TODO |
| `trennungen_heilen.py` | fügt Wörter zusammen, die ein Absatzumbruch zerrissen hat — mit oder ohne Leerzeichen, je nachdem, was im Original steht |
| `bildreste_entfernen.py` | löscht Absätze, die keine Sätze sind: Beschriftungen aus Grafiken, die im Text gelandet sind |
| `template/tools/umfang_pruefen.py` | ob Cover und Innenteil dieselbe Seitenzahl annehmen |

Dazu kommt `template/innenteil/tools/verkleinern.py`: Es fasst gleiche Bilder zusammen
und begrenzt die Auflösung auf die von der Druckerei geforderten 300 dpi.
Bei einer Arbeit mit vielen Abbildungen macht das den Unterschied zwischen
einer handlichen und einer unverschickbaren Datei — im Testband von
21,5 MB auf 7,4 MB. `.auen.ps1` ruft es selbst auf.

Ein `[!!]` bedeutet: So kann das nicht in den Druck. Ein `[ ?]` ist ein
Hinweis, den du selbst beurteilen musst.

**Wichtig:** Die Skripte prüfen, was maschinell prüfbar ist. Was sie nicht
können, listen sie am Ende ihrer Ausgabe auf — etwa die Lesbarkeit der
Schrift *in* deinen Abbildungen oder die Lückenlosigkeit des Lebenslaufs.
Diese Punkte bleiben deine Aufgabe.

---

## 8. Warum Umschlag und Innenteil getrennte Dateien sind

Das ist die Frage, die am häufigsten kommt. Der Grund liegt in der
Buchherstellung:

**Es sind zwei verschiedene Druckerzeugnisse.** Der Innenteil wird auf
115 g/m² Bilderdruck gedruckt, gefalzt und fadengeheftet. Der Umschlag wird
auf 135 g/m² Papier gedruckt, folienkaschiert und auf 2,2 mm Graupappe
aufgezogen. Zwei Maschinen, zwei Papiere, zwei Dateien — die Druckerei
verlangt sie getrennt.

**Die Formate sind verschieden:**

| | Endformat | Datenformat (mit Beschnitt) |
|---|---|---|
| Innenteil | 148 × 210 mm | 154 × 216 mm (3 mm) |
| Umschlag | (306 mm + Rücken) × 215 mm | (336 mm + Rücken) × 245 mm (15 mm) |

Der Umschlag ist eine einzige breite Seite: Rückseite, Buchrücken und
Titelseite nebeneinander. Der Buchdeckel ist zudem etwas größer als der
Buchblock (153 × 215 statt 148 × 210 mm) — deshalb steht der Umschlag beim
fertigen Buch leicht über.

**Der Umschlag hängt vom Innenteil ab.** Die Rückenstärke ergibt sich aus der
Seitenzahl:

```
Rücken = Seiten / 2 × Blattdicke + 2 × Graupappe
```

Deshalb trägst du die Seitenzahl in `inhalt/buchdaten.typ` ein, und deshalb
prüft `template/tools/umfang_pruefen.py`, ob sie noch stimmt. Solange du schreibst,
wird sie nicht stimmen — das ist normal. Vor dem Druck muss sie stimmen.

**Für online ist es umgekehrt.** Da will niemand zwei Dateien. Deshalb baut
`template/tools/gesamt.py` eine Datei: Titelseite, Innenteil, Rückseite — mit den
Lesezeichen des Innenteils und den richtigen Seitenlabels. Der Buchrücken
entfällt dabei, denn ein PDF hat keinen.

---

## 9. Zum Drucken

Was WirMachenDruck bekommt:

1. `build/Druckversion/umschlag.pdf` — **nicht** `umschlag-kontrolle.pdf`, die hat
   Hilfslinien drin.
2. `build/Druckversion/innenteil.pdf`

Grundlage ist das Datenblatt `buecher_mit_hardcover_dina5_hoch_44_1.pdf`
(Seite 2 beschreibt die Inhaltsseiten). Was dort steht, prüft
`template/innenteil/tools/pruefen.py` Punkt für Punkt: Datenformat 154 × 216 mm,
Endformat 148 × 210 mm, 3 mm Beschnitt, 5 mm Sicherheitsabstand, 7 mm
Falzkante am Bund der ersten und letzten Blätter, CMYK, mindestens 300 dpi,
eingebettete Schriften.

Vorher prüfen:

- [ ] `seiten` in `inhalt/buchdaten.typ` stimmt mit dem Innenteil überein
- [ ] Seitenzahl ist durch 4 teilbar — die Druckdatei füllt selbst auf, im
      Cover muss die aufgefüllte Zahl stehen
- [ ] Alle Prüfskripte laufen ohne `[!!]` durch
- [ ] Die von der Druckerei genannte Bundstärke stimmt mit der berechneten
      überein (sonst in `bund:` direkt eintragen)
- [ ] **Digitale Vorprüfung beim Prüfungsamt** — seit August 2026 verpflichtend
      **vor** dem Druck, verhindert Fehldrucke

> **Fallstrick Rückenstärke:** Die Blattdicke 0,104 mm ist aus der
> Herstellerangabe zurückgerechnet (204 Seiten → 15 mm). Ob WirMachenDruck
> wirklich linear rechnet, ist nicht bestätigt. Nimm die Zahl, die der
> Konfigurator für deine Seitenzahl nennt, und trage sie in `bund:` ein.

---

## 10. Häufige Fehler

| Symptom | Ursache | Lösung |
|---|---|---|
| `typst: command not found` | PowerShell kennt den neuen Pfad nicht | Fenster neu öffnen |
| PDF sieht nach der falschen Schrift aus | Cambria fehlt, Typst nimmt still einen Ersatz | `typst fonts \| Select-String Cambria` |
| `error: unknown variable: definitionsbox` | Kapiteldatei ohne Import-Zeile | erste Zeile `#import "/template/innenteil/isem.typ": *` |
| Literaturverweis erscheint als `@bursac2023` | Schlüssel steht nicht in `literatur.bib` | Zotero-Export prüfen |
| Umschlag passt nicht ums Buch | `seiten` veraltet | `.\bauen.ps1`, Umfangsbericht lesen |
| Änderung wirkt nicht | `typst watch` läuft noch mit alter Datei | Strg+C, neu starten |
| `file access denied` oder Vorlage nicht gefunden | `typst` ohne `--root ..` gestartet | `typst watch --root .. main.typ …` aus `inhalt/` |
| Abbildung wird nicht gefunden | Datei liegt nicht in `inhalt/abbildungen/` | `abbildung("bild.png", alt: "…")` sucht dort; anderer Ort: `"/inhalt/…/bild.png"` |

---

## 11. Der Beispielband

`Band000-Bursac/` ist ein vollständiger Band der Reihe, aus dem gedruckten
Original zurückgelesen: 217 Seiten, 90 Abbildungen, 9 Tabellen, rund 1000
Fußnoten. Er ist das Belegexemplar der Vorlage — was dort durchläuft, läuft
auch in einer neuen Arbeit. Er trägt seine eigene Kopie der Bau- und
Prüfskripte (noch in der älteren Ordnerstruktur mit `Innenteil/` und
`Cover/`) und baut mit seinem eigenen `.\bauen.ps1`.

Er ist zugleich der beste Ort, um zu sehen, wie die Prüfskripte an echtem
Text arbeiten: `umbruch_pruefen.py` meldet dort 143 Stellen — Hurenkinder,
Trennungen am Seitenende und Abbildungen mit 274 statt 300 dpi.

## 12. Ordnerübersicht

```
docs/ANLEITUNG.md             dieses Dokument
docs/AENDERUNGEN-GEGENUEBER-WORD.md  was anders ist als in Word, und warum
bauen.ps1                     baut alles und prüft alles (Windows)
bauen.sh                      dasselbe für macOS und Linux
build/                        die fertigen Dateien

inhalt/                       ← DEINE Arbeit. Nur hier schreibst du.
  angaben.typ                 ← hier trägst du ein (auch PDF-Metadaten)
  buchdaten.typ               ← Angaben für den Umschlag
  main.typ                    Reihenfolge deiner Kapitel und Anhänge
  literatur.bib               Quellen (aus Zotero)
  kapitel/                    ← hier schreibst du
  anhang/  titelei/  abbildungen/

template/                     ← die Vorlage. Wird per git merge aktualisiert.
  bauen.ps1  bauen.sh         die eigentliche Baulogik
  ISEM-Zitationsstil.csl      Zitierstil des Instituts
  ISOcoated_v2_300_eci.icc    Ausgabebedingung für den Druck
  buecher_mit_hardcover_...pdf  Datenblatt der Druckerei
  requirements.txt            Python-Pakete der Skripte
  innenteil/
    isem.typ                  das Layout: Satzspiegel, Raster, Farben, Verzeichnisse
    tuhh.typ                  Deckblätter und Fassungsregeln
    buch.typ                  Zusammenbau: Titelei, Hauptteil, Verzeichnisse
    bezeichner.typ            deutsche und englische Bezeichnungen
    impressum.typ             Schmutztitel und Impressum der Reihe
    tools/                    Druckdatei, Verkleinerung, Umbruch- und Formatprüfung
  cover/
    COVER.md                  Details zum Umschlag
    umschlag.typ  bildschirm.typ
    src/                      Layout, Farben, Logos
    assets/                   Designvorlage, Datenblatt, ISEM-Logo
    tools/
  tools/
    farbprofil.py             trägt die Ausgabebedingung in die Druckdateien ein
    gesamt.py                 Umschlag + Innenteil → eine Online-Datei
    umfang_pruefen.py         gleicht Seitenzahl gegen Cover ab
```

---

## 13. Lizenz

Die Vorlage steht unter **CC0 1.0** — gemeinfrei, so weit das Recht es
zulässt. Du darfst sie kopieren, ändern und weitergeben, auch gewerblich,
ohne uns zu nennen und ohne zu fragen. Der Text deiner Arbeit gehört
selbstverständlich dir; CC0 betrifft nur die Vorlage.

Ausgenommen sind vier Bestandteile, die uns nicht gehören oder eine eigene
Lizenz tragen: der Zitierstil, die Logos von TUHH und ISEM, das Farbprofil
der ECI und die Schrift Cambria. Die Einzelheiten stehen in `NOTICE`.

Das Layout in `template/innenteil/isem.typ` ist für diese Reihe geschrieben. Es
bildet eine ältere, in Word gesetzte Referenzfassung nach: Satzspiegel,
Schriftgrade, Abstände, Kopfzeilen und Beschriftungen sind aus jener Datei
ausgemessen und im Kopf des Moduls dokumentiert.
