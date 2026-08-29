# ISEM-Dissertationsvorlage

Satzvorlage für die Reihe **Forschungsberichte des ISEM** — Institut für Smarte
Entwicklung und Maschinenelemente, Technische Universität Hamburg.

Aus einer Quelle entstehen drei Dateien:

| Was | Datei | wofür |
|---|---|---|
| Druckfassung | `build/Druckversion/innenteil.pdf` + `umschlag.pdf` | an die Druckerei |
| Onlinefassung | `build/Onlineversion/dissertation.pdf` | zum Lesen und Verschicken |
| Archivfassung | `build/Archivversion/innenteil.pdf` | für TORE und die DNB |

Gesetzt wird mit [Typst](https://typst.app). Wenn du noch nie damit gearbeitet
hast: Das ist kein Hindernis. Du schreibst in gewöhnlichen Textdateien, und
ein Befehl baut daraus das fertige Buch.

---

## In fünf Minuten zum ersten PDF

```powershell
git clone https://github.com/ISEM-TUHH/dissertationsvorlage.git
cd dissertationsvorlage
.\bauen.ps1
```

Danach liegt alles in `build/`. Wenn etwas fehlt, sagt dir das Skript, was.

Für den Alltag reicht:

```powershell
cd Innenteil
typst watch main.typ ../build/Onlineversion/innenteil.pdf
```

Typst baut dann bei jedem Speichern neu — meist in unter einer Sekunde.

---

## Was du brauchst

| | wofür | woher |
|---|---|---|
| **Typst** ab 0.13 | der Satz selbst | `winget install Typst.Typst` |
| **Python** ab 3.10 | Prüfskripte und Druckdateien | [python.org](https://www.python.org) |
| **Ghostscript** | CMYK-Wandlung des Innenteils | [ghostscript.com](https://www.ghostscript.com) |
| **Cambria** | die Schrift der Reihe | liegt jedem Windows und jedem Office bei |
| PyMuPDF, Pillow | für die Skripte | `pip install pymupdf pillow` |

Das Farbprofil `ISOcoated_v2_300_eci.icc` liegt bei. Es stammt vom
[European Color Initiative](https://www.eci.org) und darf frei verwendet
werden.

---

## Wo du was einträgst

Im Alltag brauchst du zwei Dateien:

- **`Innenteil/angaben.typ`** — Titel, Name, Gutachter, Datum, welche Teile
  mitkommen sollen. Ganz oben steht die wichtigste Zeile:

  ```typst
  fassung: "eingereicht",   // oder "genehmigt"
  ```

  Sie schaltet zwischen der Fassung für den Promotionsausschuss und der
  gedruckten Fassung für die Reihe um — mit allem, was daran hängt:
  Deckblatt, Erklärungen, Lebenslauf.

- **`Cover/buchdaten.typ`** — Angaben für den Umschlag, vor allem die
  Seitenzahl des Buchblocks. Aus ihr rechnet die Vorlage die Rückenstärke.

Deine Kapitel liegen als einzelne Dateien in `Innenteil/kapitel/`.

Alles Weitere steht ausführlich in **[ANLEITUNG.md](ANLEITUNG.md)** — von der
Installation über Zotero bis zur Übergabe an die Druckerei.

---

## Was die Vorlage von selbst tut

- **Registerhaltiger Satz.** Alle Zeilen liegen auf einem Raster von 12,9 pt,
  Vorder- und Rückseite eines Blattes stehen auf gleicher Höhe.
- **Gespiegelte Stege im Druck** (Bund 14 mm, außen 15 mm), symmetrisch am
  Bildschirm.
- **Druckfertige Dateien**: Beschnittzugabe, TrimBox, CMYK, Schwarz nur im
  K-Kanal, eingebettete Ausgabebedingung, Seitenzahl durch vier teilbar.
- **Verzeichnisse** für Abbildungen, Tabellen, Formelzeichen, Abkürzungen und
  Definitionen — alle aus dem Text erzeugt, keines von Hand gepflegt.
- **Mikrotypografie**: schmale geschützte Leerzeichen, echte Kapitälchen,
  Cambria Math für Formeln, Aufzählungszeichen in der Hausfarbe.

Warum das so eingerichtet ist, steht in
**[AENDERUNGEN-GEGENUEBER-WORD.md](AENDERUNGEN-GEGENUEBER-WORD.md)** — dort
ist auch beschrieben, welche dieser Punkte sich in Word nachbauen lassen und
wie.

---

## Prüfskripte

Nach jedem `.\bauen.ps1` laufen die Prüfungen automatisch mit. Einzeln
aufrufen lassen sie sich auch:

```powershell
cd Innenteil
python tools/pruefen.py           # Druckvorgaben: Format, Beschnitt, Farbe, Schriften
python tools/tuhh_pruefen.py      # Formalia der TUHH
python tools/umbruch_pruefen.py   # Hurenkinder, Schusterjungen, Trennungen
```

Zwei Werkzeuge beheben Umbruchprobleme selbst, **ohne den Text zu ändern** —
über eine unsichtbare Klammer um das umbrechende Wort oder über lokal
erhöhte Satzkosten:

```powershell
python tools/umbruch_heilen.py --auch-verso
python tools/absatzumbruch_heilen.py
```

Der Wortlaut der Autorin oder des Autors bleibt dabei unangetastet.

---

## Ordner

```
Innenteil/       Text, Literatur, Titelei
  angaben.typ      alle Angaben zur Arbeit
  main.typ         Reihenfolge der Bestandteile
  kapitel/         deine Kapitel
  titelei/         Vorwort, Danksagung, Kurzfassung, Abstract …
  src/             der Satz selbst - hier musst du nichts ändern
  tools/           Prüfskripte
Cover/           Umschlag
  buchdaten.typ    Titel, Verfasser, Seitenzahl
build/           die fertigen Dateien
```

---

## Ein vollständiges Beispiel

Band 000 der Reihe — die Dissertation von Nikola Bursać — ist mit dieser
Vorlage gesetzt und dient als Belegexemplar: alles, was dort läuft, läuft
auch in einer neuen Arbeit. Der Band liegt in einem eigenen, nicht
öffentlichen Repository; wer hineinsehen möchte, meldet sich beim Institut.

---

## Mitmachen

Fehler und Wünsche gern als Issue. Wenn dir beim Schreiben etwas auffällt,
das die Vorlage übernehmen sollte, ist das die richtige Stelle dafür — jede
Arbeit macht die Vorlage für die nächste besser.
