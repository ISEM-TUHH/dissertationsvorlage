#!/usr/bin/env bash
# Erzeugt alle Umschlag-PDF und prueft sie (macOS/Linux).
# Aufruf direkt oder ueber ../bauen.sh (den Gesamtbau).
#
# Die Buchdaten liest der Umschlag aus inhalt/buchdaten.typ - gebaut wird
# darum mit --root auf dem Wurzelordner.

set -euo pipefail
hier="$(cd "$(dirname "$0")" && pwd)"
py="$(command -v python3 || command -v python)"
cd "$hier"

# Zwischendateien bleiben hier, die fertigen Dateien wandern in
# ../../build mit seinen Unterordnern.
mkdir -p build ../../build/Druckversion ../../build/Onlineversion ../../build/Archivversion ../../build/Kontrolle

echo "Logos aus den Quellen erzeugen ..."
"$py" tools/gen_logos.py

echo "Druckdatei Umschlag (CMYK) ..."
typst compile --root ../.. umschlag.typ ../../build/Druckversion/umschlag.pdf

echo "Ausgabebedingung eintragen (ISO Coated v2 300% ECI) ..."
"$py" tools/ausgabebedingung.py ../../build/Druckversion/umschlag.pdf

echo "Kontrollansicht mit Hilfslinien ..."
typst compile --root ../.. --input hilfslinien=ja umschlag.typ ../../build/Kontrolle/umschlag-hilfslinien.pdf

echo "Bildschirmfassung (RGB, Titelseite vorn / Rueckseite hinten) ..."
typst compile --root ../.. --input farbraum=rgb bildschirm.typ ../../build/Onlineversion/umschlag.pdf

echo ""
"$py" tools/pruefen.py
echo ""
"$py" tools/vergleich.py
