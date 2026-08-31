# Änderungen

Diese Datei hält fest, was sich von Fassung zu Fassung ändert. Wer eine
Arbeit setzt, sollte in `inhalt/angaben.typ` notieren, mit welcher Fassung
er begonnen hat — dann lässt sich später nachvollziehen, warum ein alter Band
anders aussieht als ein neuer.

Die Nummern folgen [SemVer](https://semver.org): Die erste Stelle steigt,
wenn eine bestehende Arbeit nach dem Umstieg anders umbricht; die zweite bei
neuen Möglichkeiten, die nichts kaputtmachen; die dritte bei Korrekturen.

## [1.0.1] — 2026-08-31

Umbau für den Fork-Arbeitsablauf: Die Vorlage lebt jetzt vollständig in
`template/`, die Arbeit vollständig in `inhalt/`. Wer die Vorlage forkt und
schreibt, holt sich Verbesserungen mit `git merge vorlage/main` — die
eigenen Kapitel bleiben dabei unberührt, weil Vorlagen-Updates nur
`template/` ändern.

### Geändert

- **Neue Ordnerstruktur.** `Innenteil/src` → `template/innenteil`,
  `Innenteil/tools` → `template/innenteil/tools`, `Cover` → `template/cover`,
  `tools` → `template/tools`. Kapitel, Titelei, Anhänge, `angaben.typ`,
  `literatur.bib` und neu auch `buchdaten.typ` liegen in `inhalt/`.
- **Schlanke `main.typ`.** Der komplette Zusammenbau (Titelei, Hauptteil,
  Verzeichnisse, Erklärungen) ist nach `template/innenteil/buch.typ`
  gewandert. In `inhalt/main.typ` stehen nur noch die Kapitel- und
  Anhangliste — mehr muss beim Schreiben nicht angefasst werden.
- **Kapiteldateien ohne Gerüst.** Das `#let inhalt = [ … ]` entfällt;
  Kapitel sind gewöhnliche Typst-Dateien und werden per `include`
  eingebunden. Erste Zeile: `#import "/template/innenteil/isem.typ": *`.
- **`abbildung("name.png")`** sucht Bilder in `inhalt/abbildungen/` —
  der Pfad `../abbildungen/…` entfällt. Gebaut wird immer mit `--root` auf
  dem Repositorium; die Bau-Skripte und die Anleitung sind entsprechend
  angepasst.

### Neu

- **Bildquellen bei der Abbildung.** `#bildquelle(<schlüssel>)` in der
  Beschriftung setzt die Quelle als Fußnote auf die Seite der Abbildung.
  Im Abbildungsverzeichnis wird sie unterdrückt — dort stehen keine
  Quellen und keine Fußnoten mehr.
- **PDF-Metadaten.** Titel, Verfasser und die neuen `schlagworte` aus
  `inhalt/angaben.typ` stehen in den Metadaten aller erzeugten PDF.
- **macOS/Linux.** Zu jedem `bauen.ps1` gibt es ein gleichwertiges
  `bauen.sh`.

## [1.0.0] — 2026-08-30

Erste veröffentlichte Fassung. Sie ist an Band 000 der Reihe erprobt: eine
vollständige Dissertation mit 232 Druckseiten, 92 Abbildungen, 13 Tabellen
und 380 Fußnoten.

### Satz

- Registerhaltiger Satz auf einem Raster von 12,9 pt.
- Gespiegelte Stege im Druck (Bund 14 mm, außen 15 mm), symmetrisch am
  Bildschirm.
- Erstzeileneinzug statt Absatzabstand.
- Erhöhte Kosten für Schusterjungen, Hurenkinder und Restzeilen.
- Vier Überschriftenebenen, dazu `#zwischentitel[…]` für eine fünfte, die
  nicht ins Inhaltsverzeichnis kommt.

### Mikrotypografie

- Schmales geschütztes Leerzeichen für Abkürzungen, Bezugsgrößen, Einheiten,
  Paragrafen und Datumsangaben — von selbst, ohne Zutun.
- Echte Kapitälchen für Autornamen über `#autor[…]`.
- Cambria Math für abgesetzte Formeln und für einzelne Größen im Fließtext.
- Aufzählungszeichen und Nummern in der Hausfarbe.

### Druckvorstufe

- Drei Ausgaben aus einer Quelle: Druck (CMYK, 154 × 216 mm mit 3 mm
  Beschnitt), Bildschirm (RGB, 148 × 210 mm) und Archiv (PDF/A-2b +
  PDF/UA-1).
- TrimBox, Sicherheitsabstand, Falzkante auf dem ersten und letzten Blatt.
- Seitenzahl wird auf ein Vielfaches von vier aufgefüllt.
- Schwarz ausschließlich im K-Kanal; ISO Coated v2 300 % als eingebettete
  Ausgabebedingung.
- Umschlag mit aus der Seitenzahl gerechneter Rückenstärke; Logos als
  Vektorpfade in CMYK.

### Aufbau

- Schmutztitel, Impressum auf dessen Rückseite, Kolophon mit ISSN und DOI.
- Umschaltung zwischen eingereichter und genehmigter Fassung über eine
  einzige Zeile in `angaben.typ`.
- Verzeichnisse für Abbildungen, Tabellen, Formelzeichen, Abkürzungen und
  Definitionen — alle aus dem Text erzeugt.
- Klickbare Querverweise auf Kapitel, Abbildungen, Tabellen und Gleichungen.

### Werkzeuge

- 26 Prüfskripte für Druckvorgaben, TUHH-Formalia und Umbruch.
- Zwei Werkzeuge, die Umbruchprobleme beheben, ohne den Text zu ändern.
- Acht weitere für die Übernahme einer bereits gesetzten Arbeit aus einem
  PDF.

### Bekannt und offen

- ISSN und DOI stehen als Platzhalter in `Innenteil/angaben.typ`.
- Hurenkinder und Schusterjungen lassen sich nicht restlos beseitigen, ohne
  einzelne Seiten eine Zeile kürzer laufen zu lassen. Das bleibt eine
  Entscheidung des Setzenden.
