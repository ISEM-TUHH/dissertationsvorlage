# -*- coding: utf-8 -*-
"""Macht Verweise im Flieszttext anklickbar.

    python tools/verweise_verknuepfen.py [--aendern]

"vgl. Abbildung 2.21" oder "siehe Kapitel 2.1.2" sind im Satz bisher nur
Text. Im Bildschirm-PDF gehoert dort ein Sprung hin - der Leser will die
Abbildung sehen, ohne zu blaettern.

Der Wortlaut bleibt dabei unangetastet: die Stelle wird lediglich in ein
#link(<marke>)[...] gefasst. Typsts eigene Referenz @marke wuerde den Text
neu erzeugen und dabei die Schreibweise des Originals ("Abb." gegenueber
"Abbildung") einebnen.

Verknuepft wird nur, wenn es die Marke wirklich gibt.
"""
import glob
import io
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HIER))

AENDERN = "--aendern" in sys.argv

DATEIEN = sorted(glob.glob("kapitel/*.typ")) + sorted(glob.glob("titelei/*.typ"))

# Alle vorhandenen Marken einsammeln.
MARKEN = set()
for pfad in DATEIEN:
    MARKEN.update(re.findall(r"<([a-z]+-[0-9-]+)>",
                             io.open(pfad, encoding="utf-8").read()))

# Schreibweise im Text -> Bauart der Marke
ARTEN = [
    (r"Abbildungen?|Abb\.", "abb"),
    (r"Tabellen?|Tab\.", "tab"),
    (r"Kapitel|Abschnitt(?:e|s)?", "abschn"),
    (r"Gleichung(?:en)?|Gl\.", "gl"),
]
MUSTER = re.compile(
    r"(?<![\[<#])\b(%s)(\s| | )(\d+(?:\.\d+)*)\b"
    % "|".join(a for a, _ in ARTEN))


def art_zu(wort):
    for muster, kuerzel in ARTEN:
        if re.fullmatch(muster, wort):
            return kuerzel
    return None


def schon_verknuepft(text, stelle):
    """Steht die Fundstelle bereits in einem #link(...)?"""
    auf = text.rfind("#link(", max(0, stelle - 200), stelle)
    if auf < 0:
        return False
    return text.find("]", auf, stelle) < 0


gesamt = 0
for pfad in DATEIEN:
    text = io.open(pfad, encoding="utf-8").read()
    ersetzungen = []
    for m in MUSTER.finditer(text):
        wort, trenner, nummer = m.group(1), m.group(2), m.group(3)
        kuerzel = art_zu(wort)
        if kuerzel is None:
            continue
        marke = "%s-%s" % (kuerzel, nummer.replace(".", "-"))
        if marke not in MARKEN:
            continue
        if schon_verknuepft(text, m.start()):
            continue
        # Die Beschriftung der Abbildung selbst wird nicht verknuepft.
        zeilenanfang = text.rfind("\n", 0, m.start()) + 1
        if text[zeilenanfang:m.start()].lstrip().startswith(("caption:", "alt:")):
            continue
        ersetzungen.append((m.start(), m.end(), marke, m.group(0)))

    if not ersetzungen:
        continue
    print("  %-46s %d Verweise" % (os.path.basename(pfad)[:44],
                                   len(ersetzungen)))
    gesamt += len(ersetzungen)
    if AENDERN:
        for a, e, marke, roh in reversed(ersetzungen):
            text = text[:a] + "#link(<%s>)[%s]" % (marke, roh) + text[e:]
        io.open(pfad, "w", encoding="utf-8", newline="\n").write(text)

print()
print("%d Verweise%s." % (gesamt, " verknuepft" if AENDERN else " gefunden"))
