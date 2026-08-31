# -*- coding: utf-8 -*-
"""Design-Treuecheck: legt die nachgebaute Titelseite ueber den
Originalentwurf des Reihen-Designs.

    python tools/vergleich.py

Erzeugt ../build/Kontrolle/umschlag-vergleich.png: Original in Rot, Nachbau
in Gruen, Deckung in Grau. Meldet den Anteil abweichender Pixel.

Der Check prueft das DESIGN der Vorlage, nicht den Umschlag eines Bandes:
Als Nachbau werden fest die Angaben des Originalentwurfs gesetzt und mit
dessen PDF verglichen. Er ist deshalb nur fuer die Vorlagenentwicklung
relevant und wird uebersprungen, sobald ein eigener Band in inhalt/ liegt -
sonst laege in jedem Fork ein Kontrollbild mit dem fremden Entwurfscover.
"""
import os
import subprocess
import sys
import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
os.chdir(BASIS)

if os.path.isdir("../../inhalt"):
    print("Designvergleich uebersprungen: er prueft das Reihen-Design gegen")
    print("den Originalentwurf und ist nur fuer die Vorlagenentwicklung")
    print("relevant, nicht fuer den Umschlag deines Bandes.")
    sys.exit(0)

DPI = 150
ORIGINAL = "assets/entwurf-original.pdf"
PRUEFDATEI = "build/_u1-referenzformat.typ"
PRUEF_PDF = "build/_u1-referenzformat.pdf"
AUSGABE = "../../build/Kontrolle/umschlag-vergleich.png"

# Titelseite im Format des Originalentwurfs (432 x 648 pt) setzen.
# Titel und Autor sind fest die Angaben des Originalentwurfs - verglichen
# wird das Design, nicht der Inhalt von inhalt/buchdaten.typ.
open(PRUEFDATEI, "w", encoding="utf-8").write('''#import "../src/design.typ": u1-inhalt
#set page(width: 432pt, height: 648pt, margin: 0pt, fill: white)
#u1-inhalt(432pt, 648pt,
  titel: "Intuitive und stakeholder-gerechte Sichten im MBSE zur Steigerung von Veränderlichkeit und Akzeptanz",
  autor: "Felix Förster, M. Sc.",
  reihe: "Forschungsberichte des ISEM",
  herausgeber: "Prof. Dr.-Ing. Nikola Bursac (Hrsg.)",
  band: "Band 005",
)
''')
# Wurzel ist das Repositorium: die Pruefdatei liest inhalt/buchdaten.typ.
subprocess.check_call(["typst", "compile", "--root", "../..", PRUEFDATEI, PRUEF_PDF])

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
