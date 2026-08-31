# ISEM-Dissertationsvorlage

Satzvorlage für die Reihe **Forschungsberichte des ISEM** — Institut für Smarte
Entwicklung und Maschinenelemente, Technische Universität Hamburg.

Aus einer Quelle entstehen drei Dateien:

| Was | Datei | wofür |
|---|---|---|
| Druckfassung | `build/Druckversion/innenteil.pdf` + `umschlag.pdf` | an die Druckerei |
| Onlinefassung | `build/Onlineversion/dissertation.pdf` | zum Lesen und Verschicken |
| Archivfassung | `build/Archivversion/innenteil.pdf` | für TORE und die DNB |

| Kapitelanfang und Folgeseite | Umschlag |
|---|---|
| ![Zwei Seiten aus dem Satz](docs/vorschau-satz.png) | ![Titelseite des Umschlags](docs/vorschau-umschlag.png) |

Beides stammt aus dem Demoband, den `.\bauen.ps1` erzeugt. Er liegt auch
fertig bei den [Releases](../../releases) — ein Klick statt einer
Installation.

Gesetzt wird mit [Typst](https://typst.app). Wenn du noch nie damit gearbeitet
hast: Das ist kein Hindernis. Du schreibst in gewöhnlichen Textdateien, und
ein Befehl baut daraus das fertige Buch.

---

## Zwei Ordner, klare Rollen

Das Repositorium ist so geschnitten, dass sich deine Arbeit und die Vorlage
nicht in die Quere kommen:

```
inhalt/      ← DEINE Dissertation: Kapitel, Bilder, Literatur, Angaben.
              Nur hier schreibst du.
template/    ← die Vorlage: Satz, Umschlag, Prüfskripte.
              Hier änderst du nichts - dieser Ordner wird aktualisiert.
```

**So bleibst du während der Schreibzeit aktuell:** Du forkst dieses
Repositorium und schreibst in `inhalt/`. Wird die Vorlage verbessert, holst
du dir den neuen Stand — deine Kapitel bleiben unberührt, weil die Vorlage
nur `template/` ändert:

```powershell
git remote add vorlage https://github.com/ISEM-TUHH/dissertationsvorlage.git   # einmalig
git fetch vorlage
git merge vorlage/main
```

Beim nächsten `.\bauen.ps1` ist deine Arbeit im neuen Satz.

---

## In fünf Minuten zum ersten PDF

```powershell
git clone https://github.com/ISEM-TUHH/dissertationsvorlage.git
cd dissertationsvorlage
.\bauen.ps1          # unter macOS/Linux: ./bauen.sh
```

Danach liegt alles in `build/`. Wenn etwas fehlt, sagt dir das Skript, was.

Für den Alltag reicht:

```powershell
cd inhalt
typst watch --root .. main.typ ../build/Onlineversion/innenteil.pdf
```

Typst baut dann bei jedem Speichern neu — meist in unter einer Sekunde.
Das `--root ..` gehört dazu: Es erlaubt der Hauptdatei den Zugriff auf die
Vorlage unter `template/`.

---

## Was du brauchst

| | wofür | woher |
|---|---|---|
| **Typst** ab 0.13 | der Satz selbst | `winget install Typst.Typst` |
| **Python** ab 3.10 | Prüfskripte und Druckdateien | [python.org](https://www.python.org) |
| **Ghostscript** | CMYK-Wandlung des Innenteils | [ghostscript.com](https://www.ghostscript.com) |
| **Cambria** | die Schrift der Reihe | liegt jedem Windows und jedem Office bei |
| PyMuPDF, Pillow | für die Skripte | `pip install -r requirements.txt` |

Das Farbprofil `template/ISOcoated_v2_300_eci.icc` liegt bei. Es stammt vom
[European Color Initiative](https://www.eci.org) und darf frei verwendet
werden.

---

## Wo du was einträgst

Im Alltag brauchst du zwei Dateien, beide in `inhalt/`:

- **`inhalt/angaben.typ`** — Titel, Name, Gutachter, Datum, Schlagworte für
  die PDF-Metadaten, welche Teile mitkommen sollen. Ganz oben steht die
  wichtigste Zeile:

  ```typst
  fassung: "eingereicht",   // oder "genehmigt"
  ```

  Sie schaltet zwischen der Fassung für den Promotionsausschuss und der
  gedruckten Fassung für die Reihe um — mit allem, was daran hängt:
  Deckblatt, Erklärungen, Lebenslauf.

- **`inhalt/buchdaten.typ`** — Angaben für den Umschlag, vor allem die
  Seitenzahl des Buchblocks. Aus ihr rechnet die Vorlage die Rückenstärke.

Deine Kapitel liegen als einzelne Dateien in `inhalt/kapitel/`, deine
Bilder in `inhalt/abbildungen/`. Ein neues Kapitel ist eine neue Datei plus
eine Zeile in `inhalt/main.typ`.

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
- **Bildquellen am richtigen Ort**: `#bildquelle(<schlüssel>)` in der
  Beschriftung setzt die Quelle als Fußnote auf die Seite der Abbildung —
  im Abbildungsverzeichnis hinten erscheint sie nicht.
- **PDF-Metadaten**: Titel, Verfasser und Schlagworte aus `inhalt/angaben.typ`
  stehen in jeder erzeugten PDF.
- **Mikrotypografie**: schmale geschützte Leerzeichen, echte Kapitälchen,
  Cambria Math für Formeln, Aufzählungszeichen in der Hausfarbe.

Warum das so eingerichtet ist, steht in
**[AENDERUNGEN-GEGENUEBER-WORD.md](AENDERUNGEN-GEGENUEBER-WORD.md)** — dort
ist auch beschrieben, welche dieser Punkte sich in Word nachbauen lassen und
wie.

---

## Prüfskripte

Nach jedem `.\bauen.ps1` laufen die Prüfungen automatisch mit. Einzeln
aufrufen lassen sie sich auch — Arbeitsverzeichnis ist `inhalt/`:

```powershell
cd inhalt
python ../template/innenteil/tools/pruefen.py           # Druckvorgaben: Format, Beschnitt, Farbe, Schriften
python ../template/innenteil/tools/tuhh_pruefen.py      # Formalia der TUHH
python ../template/innenteil/tools/umbruch_pruefen.py   # Hurenkinder, Schusterjungen, Trennungen
```

### Werkzeuge für die Übernahme einer bestehenden Arbeit

Acht der Skripte erwarten als Argument ein Original-PDF. Sie werden nur
gebraucht, wenn eine bereits gesetzte Arbeit in die Reihe übernommen wird —
so ist Band 000 entstanden. Für eine neu geschriebene Dissertation sind sie
ohne Bedeutung:

```powershell
python ../template/innenteil/tools/textabdeckung.py <original.pdf>            # fehlt Text?
python ../template/innenteil/tools/fussnoten_wortlaut.py <original.pdf>       # stimmt jede Fußnote?
python ../template/innenteil/tools/fussnoten_mengen.py <original.pdf>         # fehlt oder doppelt?
python ../template/innenteil/tools/fussnote_original.py <original.pdf> 42     # Wortlaut einer Fußnote
python ../template/innenteil/tools/zitate_richtigstellen.py <original.pdf> 2  # richtige Quelle zitiert?
python ../template/innenteil/tools/abbildungen_pruefen.py <original.pdf>      # Abbildung abgeschnitten?
python ../template/innenteil/tools/aufzaehlungen_abgleichen.py <original.pdf> # Aufzählung abgegrenzt?
python ../template/innenteil/tools/absaetze_zusammenfuehren.py <original.pdf> # Absatz zerrissen?
```

### Umbruch beheben, ohne den Text zu ändern

Zwei Werkzeuge beheben Umbruchprobleme selbst, **ohne den Text zu ändern** —
über eine unsichtbare Klammer um das umbrechende Wort oder über lokal
erhöhte Satzkosten:

```powershell
python ../template/innenteil/tools/umbruch_heilen.py --auch-verso
python ../template/innenteil/tools/absatzumbruch_heilen.py
```

Der Wortlaut der Autorin oder des Autors bleibt dabei unangetastet.

---

## Ordner

```
inhalt/          ← deine Arbeit. Nur hier schreibst du.
  angaben.typ      alle Angaben zur Arbeit (auch PDF-Metadaten)
  buchdaten.typ    Angaben für den Umschlag
  main.typ         Reihenfolge deiner Kapitel und Anhänge
  literatur.bib    Quellen (aus Zotero)
  kapitel/         deine Kapitel, eine Datei je Kapitel
  anhang/          deine Anhänge
  titelei/         Vorwort, Danksagung, Kurzfassung, Abstract …
  abbildungen/     deine Bilddateien
template/        ← die Vorlage. Wird per git merge aktualisiert.
  innenteil/       der Satz: Satzspiegel, Raster, Verzeichnisse, Deckblätter
    tools/         Druckdatei, Verkleinerung, Umbruch- und Formatprüfung
  cover/           der Umschlag: Layout, Farben, Logos, Prüfskripte
  tools/           Gesamtdatei, Umfangsabgleich, Farbprofil
  ISEM-Zitationsstil.csl   Zitierstil des Instituts
  ISOcoated_v2_300_eci.icc Ausgabebedingung für den Druck
bauen.ps1        baut alles und prüft alles (Windows)
bauen.sh         dasselbe für macOS und Linux
build/           die fertigen Dateien
```

---

## Ein vollständiges Beispiel

Band 000 der Reihe — die Dissertation von Nikola Bursać — ist mit dieser
Vorlage gesetzt und dient als Belegexemplar: alles, was dort läuft, läuft
auch in einer neuen Arbeit. Der Band liegt in einem eigenen, nicht
öffentlichen Repository; wer hineinsehen möchte, meldet sich beim Institut.

---

## Fassungen

Was sich von Fassung zu Fassung ändert, steht in
**[CHANGELOG.md](CHANGELOG.md)**. Notiere dir, mit welcher Fassung du
begonnen hast — dann ist später nachvollziehbar, warum ein älterer Band
anders aussieht als ein neuer.

---

## Lizenz

**[CC0 1.0](LICENSE)** — gemeinfrei, so weit das Recht es zulässt. Nimm sie,
ändere sie, gib sie weiter, auch gewerblich. Du musst uns nicht nennen und
nicht fragen. Wenn du magst, sag uns trotzdem Bescheid — wir freuen uns.

Vier Bestandteile sind davon ausgenommen, weil sie uns nicht gehören oder
eine eigene Lizenz tragen: der Zitierstil (CC BY-SA 3.0, abgeleitet vom
APA-Stil), die Logos von TUHH und ISEM, das Farbprofil der ECI und die
Schrift Cambria. Die Einzelheiten stehen in **[NOTICE](NOTICE)**.

---

## Mitmachen

Fehler und Wünsche gern als Issue. Wenn dir beim Schreiben etwas auffällt,
das die Vorlage übernehmen sollte, ist das die richtige Stelle dafür — jede
Arbeit macht die Vorlage für die nächste besser.
