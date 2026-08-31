#!/usr/bin/env bash
# Erzeugt Online-, Archiv- und Druckfassung des Innenteils und prueft alle
# (macOS/Linux). Aufruf direkt oder ueber ../bauen.sh (den Gesamtbau).
#
# Gearbeitet wird im Ordner inhalt/ - dort liegen main.typ, die Kapitel und
# die Angaben. Gebaut wird mit --root auf dem Wurzelordner, damit main.typ
# die Vorlage unter /template/ erreicht.

set -euo pipefail
hier="$(cd "$(dirname "$0")" && pwd)"
wurzel="$(cd "$hier/../.." && pwd)"
py="$(command -v python3 || command -v python)"
inhalt="inhalt"
[ -d "$wurzel/inhalt" ] || inhalt="inhalt-vorlage"
cd "$wurzel/$inhalt"

# Zwischendateien bleiben in inhalt/build, die fertigen Dateien wandern in
# ../build mit seinen Unterordnern.
mkdir -p build ../build/Druckversion ../build/Onlineversion ../build/Archivversion ../build/Kontrolle

echo "Onlinefassung (RGB, 148 x 210 mm, ohne Beschnitt) ..."
typst compile --root .. --input "inhalt=$inhalt" main.typ ../build/Onlineversion/innenteil.pdf

echo "Onlinefassung verkleinern ..."
"$py" ../template/innenteil/tools/verkleinern.py ../build/Onlineversion/innenteil.pdf

echo "Archivfassung (PDF/A-2b + PDF/UA-1, fuer TORE und DNB) ..."
typst compile --root .. --input "inhalt=$inhalt" --pdf-standard a-2b,ua-1 main.typ ../build/Archivversion/innenteil.pdf

echo "Satz fuer den Druck (doppelseitig) ..."
typst compile --root .. --input "inhalt=$inhalt" --input ausgabe=druck main.typ build/_satz-druck.pdf

echo "Druckfassung (CMYK, 154 x 216 mm mit 3 mm Beschnitt) ..."
"$py" ../template/innenteil/tools/druckdatei.py build/_satz-druck.pdf ../build/Druckversion/innenteil.pdf

echo ""
"$py" ../template/innenteil/tools/pruefen.py
echo ""
"$py" ../template/innenteil/tools/tuhh_pruefen.py ../build/Onlineversion/innenteil.pdf

echo ""
"$py" ../template/innenteil/tools/umbruch_pruefen.py ../build/Druckversion/innenteil.pdf
