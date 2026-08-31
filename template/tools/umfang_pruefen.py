# -*- coding: utf-8 -*-
"""Gleicht den tatsächlichen Umfang des Innenteils gegen die Cover-Angaben ab.

    python tools/umfang_pruefen.py

Der häufigste Fehler bei einem Buch: Der Umschlag wird mit einer anderen
Seitenzahl gerechnet als der Innenteil tatsächlich hat. Dann stimmt die
Rückenstärke nicht, und der Umschlag passt nicht um den Buchblock.
"""
import os
import re
import sys

import fitz

BASIS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(BASIS)

INNEN = "build/Druckversion/innenteil.pdf"
INHALT = "inhalt" if os.path.isdir("inhalt") else "inhalt-vorlage"
BUCHDATEN = INHALT + "/buchdaten.typ"

fehler = 0


def melde(ok, text, hinweis=""):
    global fehler
    if not ok:
        fehler += 1
    print("  [%s] %s" % ("OK" if ok else "!!", text))
    if hinweis and not ok:
        print("       %s" % hinweis)


if not os.path.exists(INNEN):
    sys.exit("fehlt: %s - zuerst .\\template\\bauen.ps1 (bzw. ./template/bauen.sh) ausführen." % INNEN)

ist = fitz.open(INNEN).page_count
quelle = open(BUCHDATEN, encoding="utf-8").read()
soll = int(re.search(r"^\s*seiten:\s*(\d+)", quelle, re.M).group(1))

print("Umfang des Buchblocks")
print("  Innenteil (%s): %d Seiten" % (INNEN, ist))
print("  Cover rechnet mit:      %d Seiten\n" % soll)

melde(ist == soll,
      "Seitenzahl in %s stimmt mit dem Innenteil überein" % BUCHDATEN,
      "seiten: %d in inhalt/buchdaten.typ eintragen und neu bauen - "
      "sonst passt die Rückenstärke nicht." % ist)

melde(ist % 4 == 0,
      "Seitenzahl ist durch 4 teilbar (%d)" % ist,
      "Ein Buchblock wird aus gefalzten Bogen gebunden. %d Seiten gehen nicht "
      "auf; die nächste passende Zahl ist %d. Leerseiten am Ende ergänzen "
      "oder die Druckerei fragen." % (ist, ist + (4 - ist % 4)))

# Rückenstärke zur Information. Die Stützstellen stammen aus dem
# WirMachenDruck-Konfigurator (Fadenheftung, 115 g/m² Bilderdruck matt,
# Stand 2026-08-31) und müssen zu template/cover/src/cover.typ passen.
WMD_RUECKEN = [
    (48, 6.0), (52, 7.0), (64, 7.0), (76, 8.0), (80, 8.0), (96, 9.0),
    (100, 10.0), (112, 10.0), (128, 11.0), (144, 12.0), (148, 12.0),
    (160, 13.0), (176, 14.0), (192, 14.0), (204, 15.0), (208, 15.0),
    (224, 16.0), (240, 16.0), (252, 17.0), (256, 17.0), (272, 18.0),
    (288, 19.0), (300, 20.0), (304, 20.0), (320, 21.0), (336, 22.0),
    (352, 22.0), (356, 22.0), (368, 23.0), (384, 24.0), (400, 25.0),
    (416, 25.0), (432, 26.0), (448, 27.0), (464, 28.0), (480, 28.0),
    (496, 29.0), (500, 29.0), (512, 30.0), (528, 31.0), (544, 31.0),
    (560, 32.0), (576, 33.0), (592, 34.0), (600, 34.0)]


def bundstaerke(seiten):
    t = WMD_RUECKEN
    if seiten <= t[0][0]:
        return t[0][1]
    for (n0, b0), (n1, b1) in zip(t, t[1:]):
        if seiten <= n1:
            return b0 + (seiten - n0) / (n1 - n0) * (b1 - b0)
    (n0, b0), (n1, b1) = t[-2], t[-1]
    return b1 + (seiten - n1) * (b1 - b0) / (n1 - n0)


print("\n  Rückenstärke bei %d Seiten: %.2f mm" % (ist, bundstaerke(ist)))
print("  (Fadenheftung, 115 g/m² Bilderdruck matt - Konfigurator-Tabelle)")
print("  Die Druckerei nennt 10 % Fertigungstoleranz auf den Rücken.")

print("\nErgebnis:", "Umfang passt" if fehler == 0 else "%d Abweichung(en)" % fehler)
sys.exit(0 if fehler == 0 else 1)
