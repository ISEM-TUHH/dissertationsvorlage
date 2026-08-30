# -*- coding: utf-8 -*-
"""Erzeugt die Vorschaubilder fuer die README.

    python tools/vorschau.py

Vorher .auen.ps1 laufen lassen - das Skript liest die fertigen PDF.

Zwei Bilder: der Umschlag und eine Doppelseite aus dem Satz. Beide auf
hellem Grund mit einer feinen Kante, damit die weisse Seite sich vom
Hintergrund der README abhebt - auch im dunklen Erscheinungsbild.
"""
import os

import fitz
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HIER))
os.makedirs("docs", exist_ok=True)

DPI = 150
GRUND = (232, 236, 237)      # heller Grund, leicht ins Petrol gezogen
KANTE = (203, 213, 216)
RAND = 26
SPALT = 18


def seite(dok, nummer):
    bild = dok[nummer].get_pixmap(dpi=DPI)
    return Image.frombytes("RGB", (bild.width, bild.height), bild.samples)


def rahmen(bilder, name):
    """Legt die Bilder nebeneinander auf einen Grund und speichert."""
    hoehe = max(b.height for b in bilder)
    breite = sum(b.width for b in bilder) + SPALT * (len(bilder) - 1)
    blatt = Image.new("RGB", (breite + 2 * RAND, hoehe + 2 * RAND), GRUND)
    x = RAND
    for b in bilder:
        # feine Kante um die Seite
        kante = Image.new("RGB", (b.width + 2, b.height + 2), KANTE)
        kante.paste(b, (1, 1))
        blatt.paste(kante, (x - 1, RAND - 1))
        x += b.width + SPALT
    blatt.save(name, optimize=True)
    print("  %-34s %d x %d" % (name, blatt.width, blatt.height))


innen = fitz.open("build/Onlineversion/innenteil.pdf")
umschlag = fitz.open("build/Onlineversion/umschlag.pdf")

print("Vorschaubilder:")
# Kapitelanfang und Folgeseite: Definitionskasten, Abbildung, Fussnoten.
rahmen([seite(innen, 20), seite(innen, 21)], "docs/vorschau-satz.png")
# Umschlag: Titelseite.
rahmen([seite(umschlag, 0)], "docs/vorschau-umschlag.png")

innen.close()
umschlag.close()
