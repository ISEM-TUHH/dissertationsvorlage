# -*- coding: utf-8 -*-
"""Zeigt den vollen Wortlaut einzelner Fussnoten aus dem Original.

    python tools/fussnote_original.py <original.pdf> <nummer> [nummer ...]
"""
import re
import sys

import fitz

d = fitz.open(sys.argv[1])
ZIEL = {int(a) for a in sys.argv[2:]}


def grundgrad():
    h = {}
    for n in range(20, min(200, d.page_count)):
        for bl in d[n].get_text("dict")["blocks"]:
            if bl["type"]:
                continue
            for l in bl["lines"]:
                for s in l["spans"]:
                    if s["text"].strip():
                        h[round(s["size"], 1)] = (h.get(round(s["size"], 1), 0)
                                                  + len(s["text"]))
    return max(h, key=h.get)


g = grundgrad()
for n in range(d.page_count):
    p = d[n]
    H = p.rect.height
    zeilen = []
    for bl in p.get_text("dict")["blocks"]:
        if bl["type"]:
            continue
        for l in bl["lines"]:
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp or max(s["size"] for s in sp) >= g - 0.8:
                continue
            if sp[0]["origin"][1] <= H * 0.7:
                continue
            zeilen.append((sp[0]["origin"][1], "".join(s["text"] for s in sp)))
    zeilen.sort()
    lauf, alle = None, []
    for _, t in zeilen:
        m = re.match(r"^(\d{1,3})(\D.*)$", t.strip())
        if m:
            if lauf:
                alle.append(lauf)
            lauf = [int(m.group(1)), m.group(2).strip()]
        elif lauf:
            lauf[1] += " " + t.strip()
    if lauf:
        alle.append(lauf)
    for nr, t in alle:
        if nr in ZIEL:
            t = re.sub(r"\s+", " ", t.replace("\u00ad", ""))
            print("Fn %d (S.%d): %s\n" % (nr, n + 1, t))
