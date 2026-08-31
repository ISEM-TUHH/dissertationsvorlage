# -*- coding: utf-8 -*-
"""Vergleicht Original und Band als Menge von Fussnoten, nicht als Folge.

    python tools/fussnoten_mengen.py <original.pdf> [kapitel ...]

Die Ausrichtung nach Reihenfolge meldet eine verschobene Fussnote zweimal:
einmal als fehlend, einmal als ueberzaehlig. Das verdeckt die Faelle, die
wirklich zaehlen - eine Fussnote, die doppelt gesetzt wurde, oder eine, die
tatsaechlich fehlt. Hier wird deshalb nur gezaehlt, wie oft ein Wortlaut auf
beiden Seiten vorkommt.
"""
import os
import re
import sys
from collections import Counter

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), "inhalt"))

if len(sys.argv) < 2:
    sys.exit("Aufruf: python tools/fussnoten_mengen.py <original.pdf> "
             "[kapitel ...]")
ORIGINAL = sys.argv[1]
KAPITEL = [int(a) for a in sys.argv[2:]] or list(range(1, 9))

orig = fitz.open(ORIGINAL)
band = fitz.open("../build/Onlineversion/innenteil.pdf")


def kapitelbereich(dok, nr):
    alle = [e for e in dok.get_toc() if e[0] == 1]
    for e in alle:
        if re.match(r"^%d\s" % nr, e[1].strip()):
            spaeter = [x[2] for x in alle if x[2] > e[2]]
            return e[2], (min(spaeter) - 1 if spaeter else dok.page_count)
    return None, None


def grundgrad(dok, von, bis):
    h = {}
    for n in range(von, bis + 1):
        for b in dok[n - 1].get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    if s["text"].strip():
                        h[round(s["size"], 1)] = (h.get(round(s["size"], 1), 0)
                                                  + len(s["text"]))
    return max(h, key=h.get)


def fussnoten(dok, von, bis):
    grad = grundgrad(dok, von, bis)
    gefunden = []
    for n in range(von, bis + 1):
        seite = dok[n - 1]
        hoehe = seite.rect.height
        zeilen = []
        for b in seite.get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp or max(s["size"] for s in sp) >= grad - 0.8:
                    continue
                if sp[0]["origin"][1] <= hoehe * 0.7:
                    continue
                zeilen.append((sp[0]["origin"][1],
                               "".join(s["text"] for s in sp)))
        zeilen.sort()
        laufend = None
        for _, t in zeilen:
            m = re.match(r"^(\d{1,3})(\D.*)$", t.strip())
            if m:
                if laufend:
                    gefunden.append(laufend)
                laufend = [int(m.group(1)), m.group(2).strip(), n]
            elif laufend:
                laufend[1] += " " + t.strip()
        if laufend:
            gefunden.append(laufend)

    def echte_fussnote(text):
        if len(re.sub(r"[^A-Za-zÄÖÜäöüß]", "", text)) < 6:
            return False
        if re.search(r"(Abbildung|Tabelle)\s+\d+[.\-]\d+:", text):
            return False
        return True

    return [f for f in gefunden if echte_fussnote(f[1])]


def kern(t):
    t = (t.replace("­", "").replace(" ", " ")
          .replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff"))
    return re.sub(r"[^a-z0-9äöüß]", "", t.lower())


gesamt = 0
for kap in KAPITEL:
    ov, ob = kapitelbereich(orig, kap)
    bv, bb = kapitelbereich(band, kap)
    if ov is None or bv is None:
        continue
    of = fussnoten(orig, ov, ob)
    bf = fussnoten(band, bv, bb)
    zo = Counter(kern(t) for _, t, _ in of)
    zb = Counter(kern(t) for _, t, _ in bf)

    doppelt, fehlend = [], []
    for k, n in zb.items():
        if n > zo.get(k, 0):
            beispiel = next(t for _, t, _ in bf if kern(t) == k)
            doppelt.append((n - zo.get(k, 0), beispiel))
    for k, n in zo.items():
        if n > zb.get(k, 0):
            beispiel = next(t for _, t, _ in of if kern(t) == k)
            fehlend.append((n - zb.get(k, 0), beispiel))

    print("── Kapitel %d ── Original %d, Band %d" % (kap, len(of), len(bf)))
    for n, t in sorted(doppelt, key=lambda x: -x[0]):
        print("   %dx zu viel im Band : %s" % (n, re.sub(r"\s+", " ", t)[:120]))
    for n, t in sorted(fehlend, key=lambda x: -x[0]):
        print("   %dx zu wenig im Band: %s" % (n, re.sub(r"\s+", " ", t)[:120]))
    gesamt += len(doppelt) + len(fehlend)
    print()

print("%d Abweichung(en) im Bestand." % gesamt)
