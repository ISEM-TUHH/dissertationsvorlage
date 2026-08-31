# -*- coding: utf-8 -*-
"""Prueft, ob die Abbildungen vollstaendig aus dem Original geholt wurden.

    python tools/abbildungen_pruefen.py <original.pdf> [--neu]

Der Extraktor sucht die Abbildung ueber zusammenhaengende Grafikelemente.
Wo eine Abbildung aus mehreren Teilen besteht, findet er manchmal nur einen
Streifen: das Bild im Band ist dann breit und flach statt vollstaendig.

Hier wird andersherum gerechnet. Die Bildunterschrift steht fest - sie ist
im Text zu finden. Ueber ihr liegt die Abbildung, darueber die letzte Zeile
Flieszttext. Aus diesen beiden Kanten ergibt sich die Hoehe, aus dem
Satzspiegel die Breite. Weicht das Seitenverhaeltnis des gespeicherten
Bildes davon deutlich ab, fehlt etwas.

Mit --neu werden die abweichenden Abbildungen neu aufgenommen.
"""
import os
import re
import sys

import fitz
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), "inhalt"))

argumente = [a for a in sys.argv[1:] if not a.startswith("--")]
if not argumente:
    sys.exit("Aufruf: python tools/abbildungen_pruefen.py <original.pdf> [--neu]")
ORIGINAL = argumente[0]
NEU = "--neu" in sys.argv
ABB = "abbildungen"
DPI = 300
TOLERANZ = 0.18          # zulaessige Abweichung des Seitenverhaeltnisses

orig = fitz.open(ORIGINAL)


def zeilen(seite):
    ergebnis = []
    for b in seite.get_text("dict")["blocks"]:
        if b["type"]:
            continue
        for l in b["lines"]:
            sp = [s for s in l["spans"] if s["text"].strip()]
            if sp:
                ergebnis.append((l["bbox"], "".join(s["text"] for s in sp)))
    return ergebnis


def satzspiegel(seite):
    """Linke und rechte Kante des Textes auf dieser Seite."""
    kanten = [b for b, t in zeilen(seite)]
    if not kanten:
        return seite.rect.x0 + 70, seite.rect.x1 - 70
    return min(k[0] for k in kanten), max(k[2] for k in kanten)


def bereich(seite, kopf_y, boden_y=None):
    """Der Kasten der Abbildung ueber ihrer Beschriftung.

    Massgeblich sind die Grafikelemente, nicht der Text: eine Abbildung
    enthaelt oft selbst Beschriftungen, und die stehen dem Textvergleich im
    Weg. Zuerst wird die Ausdehnung aller Grafikelemente ueber der
    Beschriftung genommen, dann werden die Textzeilen hinzugenommen, die in
    diesem Band liegen - das sind die Beschriftungen innerhalb des Bildes.
    """
    seiten_oben = seite.rect.y0 + seite.rect.height * 0.09
    if boden_y is not None:
        seiten_oben = max(seiten_oben, boden_y + 2)
    # Flieszttext oberhalb der Abbildung begrenzt sie ebenfalls nach oben.
    # Erkannt wird er an der Zeilenbreite: eine Zeile des Satzspiegels ist
    # lang, eine Beschriftung innerhalb des Bildes kurz.
    breiteste = max((b[2] - b[0] for b, _ in zeilen(seite)), default=0)
    for bbox, _ in zeilen(seite):
        if bbox[3] < kopf_y - 4 and bbox[3] > seiten_oben                 and (bbox[2] - bbox[0]) > breiteste * 0.75:
            seiten_oben = bbox[3]
    teile = []
    for b in seite.get_text("dict")["blocks"]:
        if b["type"] != 1:
            continue
        x0, y0, x1, y1 = b["bbox"]
        if y1 <= kopf_y and y0 >= seiten_oben:
            teile.append((x0, y0, x1, y1))
    for z in seite.get_drawings():
        x0, y0, x1, y1 = z["rect"]
        if y1 <= kopf_y and y0 >= seiten_oben and (x1 - x0) > 3 and (y1 - y0) > 3:
            teile.append((x0, y0, x1, y1))
    if not teile:
        return None
    oben = min(t[1] for t in teile)
    links = min(t[0] for t in teile)
    rechts = max(t[2] for t in teile)

    # Beschriftungen innerhalb der Abbildung erweitern sie zur Seite. Die
    # Oberkante bleibt bei den Grafikelementen: sonst wandert der Kasten
    # Zeile fuer Zeile in den Flieszttext darueber hinein.
    for bbox, _ in zeilen(seite):
        if bbox[1] >= oben - 2 and bbox[3] <= kopf_y - 1:
            links, rechts = min(links, bbox[0]), max(rechts, bbox[2])
    return fitz.Rect(links - 3, oben - 3, rechts + 3, kopf_y - 2)


BESCHRIFTUNG = re.compile(r"^\s*(?:Abbildung|Tabelle)\s+(\d+)[.\-](\d+)\s*:")
NUR_ABBILDUNG = re.compile(r"^\s*Abbildung\s+(\d+)[.\-](\d+)\s*:")

geprueft = abweichend = neugemacht = 0
for n in range(orig.page_count):
    seite = orig[n]
    # Die Unterkante der vorigen Beschriftung derselben Seite begrenzt die
    # naechste Abbildung nach oben - sonst wird die davor mitgenommen.
    voriges_ende = None
    for bbox, text in sorted(zeilen(seite), key=lambda x: x[0][1]):
        if BESCHRIFTUNG.match(text) and not NUR_ABBILDUNG.match(text):
            voriges_ende = bbox[3]
            continue
        m = NUR_ABBILDUNG.match(text)
        if not m:
            continue
        name = "abbildung_%s_%s.png" % (m.group(1), m.group(2))
        pfad = os.path.join(ABB, name)
        if not os.path.exists(pfad):
            print("  ! %-24s fehlt im Ordner" % name)
            continue
        kasten = bereich(seite, bbox[1], voriges_ende)
        voriges_ende = bbox[3]
        if kasten is None or kasten.height < 20 or kasten.width < 20:
            continue
        soll = kasten.width / kasten.height
        with Image.open(pfad) as bild:
            ist = bild.width / bild.height
        geprueft += 1
        if abs(ist - soll) / soll <= TOLERANZ:
            continue
        abweichend += 1
        print("  %-24s S.%-4d gespeichert %5.1f:1, im Original %5.1f:1"
              % (name, n + 1, ist, soll))
        if NEU:
            neu = seite.get_pixmap(dpi=DPI, clip=kasten)
            neu.save(pfad)
            neugemacht += 1
            print("      neu aufgenommen: %d x %d" % (neu.width, neu.height))

print()
print("%d Abbildungen geprueft, %d abweichend%s."
      % (geprueft, abweichend,
         ", %d neu aufgenommen" % neugemacht if NEU else ""))
