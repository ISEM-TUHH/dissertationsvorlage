# -*- coding: utf-8 -*-
"""Legt die nachgebaute Titelseite ueber den Originalentwurf.

    python tools/vergleich.py

Erzeugt ../build/Kontrolle/umschlag-vergleich.png: Original in Rot, Nachbau in Gruen, Deckung in
Grau. Meldet den Anteil abweichender Pixel.
"""
import os
import subprocess
import sys
import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
os.chdir(BASIS)

DPI = 150
ORIGINAL = "assets/entwurf-original.pdf"
PRUEFDATEI = "build/_u1-referenzformat.typ"
PRUEF_PDF = "build/_u1-referenzformat.pdf"
AUSGABE = "../build/Kontrolle/umschlag-vergleich.png"

# Titelseite im Format des Originalentwurfs (432 x 648 pt) setzen
open(PRUEFDATEI, "w", encoding="utf-8").write('''#import "../src/design.typ": u1-inhalt
#import "../buchdaten.typ": buch
#set page(width: 432pt, height: 648pt, margin: 0pt, fill: white)
#u1-inhalt(432pt, 648pt,
  titel: buch.titel,
  autor: "Felix Förster, M. Sc.",
  reihe: buch.reihe,
  herausgeber: buch.herausgeber,
  band: buch.band,
)
''')
subprocess.check_call(["typst", "compile", "--root", ".", PRUEFDATEI, PRUEF_PDF])

a = fitz.open(ORIGINAL)[0].get_pixmap(dpi=DPI)
b = fitz.open(PRUEF_PDF)[0].get_pixmap(dpi=DPI)
w, h = min(a.width, b.width), min(a.height, b.height)
sa, sb, na, nb = a.samples, b.samples, a.n, b.n

rows, abw = [], 0
for y in range(h):
    row = bytearray()
    for x in range(w):
        ia, ib = (y * a.width + x) * na, (y * b.width + x) * nb
        ga = (sa[ia] + sa[ia + 1] + sa[ia + 2]) // 3
        gb = (sb[ib] + sb[ib + 1] + sb[ib + 2]) // 3
        if abs(ga - gb) > 40:
            abw += 1
        row += bytes((ga, gb, min(ga, gb)))
    rows.append(bytes(row))
fitz.Pixmap(fitz.csRGB, w, h, b"".join(rows), 0).save(AUSGABE)

anteil = 100.0 * abw / (w * h)
print("Original: %s" % ORIGINAL)
print("Nachbau:  %s (Format des Originalentwurfs)" % PRUEF_PDF)
print("Differenzbild: %s" % AUSGABE)
print("abweichende Pixel: %d von %d (%.2f %%)" % (abw, w * h, anteil))
sys.exit(0 if anteil < 2.0 else 1)
