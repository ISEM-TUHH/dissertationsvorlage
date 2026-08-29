---
titel: ISEM-Buchumschlag in Typst
zweck: Druckfertiger Hardcover-Umschlag und Bildschirmfassung für die Reihe „Forschungsberichte des ISEM“
quelle_design: assets/entwurf-original.pdf
quelle_spezifikation: assets/datenblatt-wirmachendruck.pdf
druckerei: WirMachenDruck
produkt: Buch DIN A5 hoch, Hardcover, gerader Buchrücken, Umschlag 4/0-farbig
einzige_eingabedatei: buchdaten.typ
stand: 2026-08-26
---

# ISEM-Buchumschlag

Nachbau des Entwurfs `assets/entwurf-original.pdf` als parametrisches
Typst-Projekt. Zwei Ausgaben aus derselben Quelle:

| Ausgabe | Datei | Farbraum | Format |
|---|---|---|---|
| Druckdatei Umschlag | `build/umschlag.pdf` | CMYK | (336 mm + B) × 245 mm, eine Seite: U4 \| Rücken \| U1 |
| Kontrollansicht | `build/umschlag-kontrolle.pdf` | CMYK | wie oben, mit Endformat-, Sicherheits- und Falzlinien |
| Bildschirmfassung | `build/cover-bildschirm.pdf` | RGB | 148 × 210 mm, zwei Seiten: Titelseite, Rückseite |

## Bedienung

Alle Angaben stehen in **`buchdaten.typ`**: Titel, Verfasser, Bandnummer,
Seitenzahl, Reihe, Rückentext. Sonst ist nichts anzufassen.

```powershell
.\bauen.ps1              # alle drei PDF erzeugen und prüfen
```

Einzeln:

```bash
typst compile umschlag.typ build/umschlag.pdf
typst compile --input hilfslinien=ja umschlag.typ build/umschlag-kontrolle.pdf
typst compile --input farbraum=rgb bildschirm.typ build/cover-bildschirm.pdf

python tools/pruefen.py      # Maße, Farbraum, Schrifteinbettung
python tools/vergleich.py    # Differenzbild gegen den Originalentwurf
```

Die Kontrollansicht ist **nicht** die Druckdatei — die Hilfslinien dürfen
nicht mitgedruckt werden.

## Maße

Angaben der Druckerei (`assets/datenblatt-wirmachendruck.pdf`, Seite 1, und
`assets/cover-informationen-druckerei.md`), B = Bundstärke:

| Größe | Wert | Herkunft |
|---|---|---|
| Datenformat Umschlag | (336 mm + B) × 245 mm | Datenblatt |
| Endformat Umschlag | (306 mm + B) × 215 mm | Datenblatt |
| Beschnitt umlaufend | 15 mm | Datenblatt |
| Sicherheitsabstand | 5 mm ab Endformat | Datenblatt |
| Falzkante | ca. 7 mm beidseits des Rückens | Datenblatt |
| Rücken-Toleranz | 10 % | Cover-Informationen |
| Deckel je Seite | 153 × 215 mm | = (306 mm) / 2 |
| Buchblock | 148 × 210 mm, Datenformat 154 × 216 mm | Datenblatt, Seite 2 |
| Bundstärke bei 204 Seiten | 15 mm | Cover-Informationen |
| Graupappe | 2,2 mm je Deckel | Cover-Informationen |

### Bundstärke aus der Seitenzahl

```
B = seiten / 2 · Blattdicke + 2 · Graupappe
  = seiten / 2 · 0,104 mm   + 2 · 2,2 mm
```

204 Seiten → 15,01 mm, also exakt die genannten 1,5 cm.

> **Nicht von der Druckerei bestätigt:** Die Blattdicke 0,104 mm ist aus der
> einen Herstellerangabe (204 Seiten → 15 mm) zurückgerechnet; dass
> WirMachenDruck linear rechnet, ist nicht belegt. Nennt der Konfigurator für
> die endgültige Seitenzahl eine andere Bundstärke, diese in `buchdaten.typ`
> unter `bund:` eintragen — sie hat dann Vorrang vor der Rechnung.

Die schräge Petrolfläche läuft mit der Steigung des Originalentwurfs über U4,
Rücken und U1 durch und passt sich damit jeder Rückenstärke von selbst an.
Auf dem Rücken steht nur mittig gesetzter Text, keine Farbkante — wegen der
10 % Toleranz.

## Farben

Die Druckdatei ist durchgängig **DeviceCMYK**, ohne einen einzigen RGB- oder
Graustufenwert; `tools/pruefen.py` verifiziert das. Zentral in
`src/farben.typ`:

| Farbe | CMYK | RGB | Verwendung | Status |
|---|---|---|---|---|
| Türkis | 70 / 0 / 13 / 0 | 0 / 193 / 212 | TUHH- und ISEM-Logo | verbindlich |
| Petrol | 100 / 18 / 0 / 49 | 0 / 106 / 129 | Fläche unten, Rücken | verbindlich |
| ISEM-Grau | 28 / 15 / 0 / 32 | 124 / 147 / 173 | ISEM-Logo, Buchstaben I und S | RGB aus `#7c93ad`, **CMYK offen** |
| Schwarz | 0 / 0 / 0 / 100 | 0 / 0 / 0 | Text | gesetzt |

CMYK und RGB sind **getrennt hinterlegte Vorgaben**, keine Umrechnung
voneinander — eine Konvertierung würde die Vorgabewerte verfehlen.

Der Schalter `--input farbraum=rgb` waehlt die RGB-Spalte; die
Bildschirmfassung nutzt ihn.

## Logos

Beide Logos sind **echte Vektorpfade mit Farben aus `farben.typ`** — keine
Pixelbilder und kein SVG-Import (ein importiertes SVG würde als DeviceRGB im
PDF landen und den CMYK-Workflow brechen).

`tools/gen_logos.py` erzeugt `src/logos.typ` aus:

* **ISEM** — `assets/isem-logo.svg` (Druckfreigabe)
* **TUHH** — vorläufig aus den Vektorpfaden von `assets/entwurf-original.pdf`

> **Offen:** Sobald das TUHH-SVG vorliegt, in `tools/gen_logos.py` bei
> `TUHH_SVG` den Pfad eintragen und `python tools/gen_logos.py` ausführen.

## Treue zum Original

Die Titelseite ist aus dem Entwurf vermessen: Grundlinien, Logohöhen, Steigung
der Fläche und Zeilenabstände stehen als Zahlenwerte in `src/design.typ` unter
`A`. Das Differenzbild gegen das Original zeigt **0,49 % abweichende Pixel**,
im Wesentlichen Subpixel-Ränder an Glyphenkanten.

Zwei bewusste Abweichungen:

1. Der Entwurf ist 152,4 × 228,6 mm groß, der Hardcover-Deckel 153 × 215 mm.
   Das Layout wird proportional auf das Endformat abgebildet.
2. Die kleine Petrol-Stufe an der Bundkante des Entwurfs entfällt auf der
   Doppelseite — dort liefe sie als Absatz genau in die Falzkante. In der
   Einzelseitenansicht (Bildschirmfassung) ist sie erhalten.

Schrift: **Bahnschrift**, wie im Entwurf; wird beim Kompilieren eingebettet.

## Dateien

```
buchdaten.typ            <- hier wird gepflegt
umschlag.typ             Einstiegspunkt Druckdatei (CMYK, mit Beschnitt)
bildschirm.typ           Einstiegspunkt Bildschirmfassung (RGB, 2 Seiten)
bauen.ps1                erzeugt alle PDF und prüft sie
COVER.md                 dieses Dokument

src/farben.typ           Palette in CMYK und RGB, Farbraumumschaltung
src/logos.typ            erzeugt — nicht von Hand ändern
src/design.typ           Layout U1 und U4, aus dem Original vermessen
src/cover.typ            Druckgeometrie, Rücken, Hilfslinien, Bildschirmfassung

tools/gen_logos.py       SVG/PDF -> Typst-Vektorpfade
tools/svgpath.py         SVG-Pfadparser
tools/pruefen.py         Prüfung der fertigen PDF
tools/vergleich.py       Differenzbild gegen den Originalentwurf

assets/entwurf-original.pdf              Designvorlage
assets/datenblatt-wirmachendruck.pdf     Spezifikation der Druckerei
assets/cover-informationen-druckerei.md  Bestellangaben
assets/isem-logo.svg                     ISEM-Logo, Druckfreigabe

build/                   Ausgaben
```

## Offene Punkte

1. TUHH-Logo als SVG einsetzen (siehe oben).
2. CMYK-Wert für das ISEM-Grau bestätigen (RGB ist gesetzt).
3. Endgültige Seitenzahl in `buchdaten.typ` eintragen und die von
   WirMachenDruck genannte Bundstärke gegen die berechnete prüfen.
4. U4 ist bewusst ruhig gehalten — Klappentext und ISBN sind in
   `buchdaten.typ` vorbereitet, aber noch leer.
