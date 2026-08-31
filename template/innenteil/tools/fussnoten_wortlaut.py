# -*- coding: utf-8 -*-
"""Vergleicht den Wortlaut jeder Fussnote mit dem Original.

    python tools/fussnoten_wortlaut.py <original.pdf> [kapitel ...]

Die bisherigen Werkzeuge suchen nur, ob eine Fussnote ueberhaupt vorhanden
ist. Das uebersieht den haeufigsten Fehler der Uebernahme: der Zitierschluessel
wurde eingeebnet. Wo das Original "Albers & Gausemeier, 2012 und Albers &
Lohmeyer, 2012" schreibt, steht im Band zweimal dieselbe Quelle - vorhanden,
aber falsch.

Deshalb werden hier Original und Band Fussnote fuer Fussnote der Reihe nach
gegenuebergestellt und der Wortlaut verglichen.
"""
import os
import re
import sys

import difflib

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), "inhalt"))

if len(sys.argv) < 2:
    sys.exit("Aufruf: python tools/fussnoten_wortlaut.py <original.pdf> [kapitel ...]")
ORIGINAL = sys.argv[1]
KAPITEL = [int(a) for a in sys.argv[2:]] or list(range(1, 9))
BAND = "../build/Onlineversion/innenteil.pdf"

orig = fitz.open(ORIGINAL)
band = fitz.open(BAND)


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
    """Fussnoten des Bereichs als (Nummer, Wortlaut, Seite)."""
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
    # Achsenbeschriftungen von Diagrammen stehen ebenfalls klein und im
    # unteren Seitendrittel ("0", "-20", "%", "TN"). Sie sehen wie eine
    # Fussnote mit Nummer aus und werden hier verworfen.
    def echte_fussnote(text):
        # Zu kurz: Achsenteilungen wie "0", "-20", "%".
        if len(re.sub(r"[^A-Za-zÄÖÜäöüß]", "", text)) < 6:
            return False
        # Enthaelt eine Bildunterschrift: dann ist die Zeile in Wahrheit
        # Diagramminhalt, den der Seitenfusz mit aufgesammelt hat.
        if re.search(r"(Abbildung|Tabelle)\s+\d+[.\-]\d+:", text):
            return False
        return True

    return [f for f in gefunden if echte_fussnote(f[1])]


def normal(t):
    """Wortlaut auf das Vergleichbare reduzieren."""
    t = (t.replace("\u00ad", "").replace("\u202f", " ")
          .replace("\u2019", "'").replace("\u201e", '"').replace("\u201c", '"')
          .replace("\u2013", "-").replace("\u2014", "-")
          .replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff"))
    t = re.sub(r"\s+", " ", t)
    return t.strip(" .;")


def kern(t):
    return re.sub(r"[^a-z0-9äöüß]", "", normal(t).lower())


def aehnlich(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def ausrichten(links, rechts):
    """Ordnet zwei Fussnotenfolgen einander zu.

    Die Nummerierung des Bandes laeuft gegenueber dem Original versetzt,
    sobald eine Fussnote fehlt. Zugeordnet wird deshalb ueber die
    Reihenfolge: eine Ausrichtung nach Needleman-Wunsch, bewertet mit der
    Aehnlichkeit des Wortlauts. Luecken auf einer Seite kosten Punkte, so
    dass fehlende und zusaetzliche Fussnoten sichtbar werden.
    """
    n, m = len(links), len(rechts)
    LUECKE = -0.55
    punkte = [[0.0] * (m + 1) for _ in range(n + 1)]
    weg = [[""] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        punkte[i][0] = i * LUECKE
        weg[i][0] = "o"
    for j in range(1, m + 1):
        punkte[0][j] = j * LUECKE
        weg[0][j] = "b"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            paar = punkte[i - 1][j - 1] + 2 * aehnlich(links[i - 1], rechts[j - 1]) - 1
            oben = punkte[i - 1][j] + LUECKE
            link = punkte[i][j - 1] + LUECKE
            besser = max(paar, oben, link)
            punkte[i][j] = besser
            weg[i][j] = "p" if besser == paar else ("o" if besser == oben else "b")
    i, j, paare = n, m, []
    while i > 0 or j > 0:
        z = weg[i][j]
        if z == "p":
            paare.append((i - 1, j - 1)); i -= 1; j -= 1
        elif z == "o":
            paare.append((i - 1, None)); i -= 1
        else:
            paare.append((None, j - 1)); j -= 1
    paare.reverse()
    return paare


gesamt = 0
for kap in KAPITEL:
    ov, ob = kapitelbereich(orig, kap)
    bv, bb = kapitelbereich(band, kap)
    if ov is None or bv is None:
        continue
    of = fussnoten(orig, ov, ob)
    bf = fussnoten(band, bv, bb)
    paare = ausrichten([kern(t) for _, t, _ in of], [kern(t) for _, t, _ in bf])

    # Eine Fussnote an einer Bildunterschrift steht im Satzfluss je nach
    # Umbruch vor oder hinter der benachbarten Fussnote des Flieszttextes.
    # Solche Paare sind nur verschoben, nicht falsch - sie werden hier
    # zusammengefuehrt, bevor gemeldet wird.
    frei_o = [i for i, j in paare if j is None and i is not None]
    frei_b = [j for i, j in paare if i is None and j is not None]
    verschoben = set()
    for i in frei_o:
        for j in frei_b:
            if j in verschoben:
                continue
            if aehnlich(kern(of[i][1]), kern(bf[j][1])) > 0.9:
                verschoben.add(i + 10000)
                verschoben.add(j)
                break

    meldungen = []
    for io_, ib in paare:
        if ib is None and io_ is not None and io_ + 10000 in verschoben:
            continue
        if io_ is None and ib in verschoben:
            continue
        if io_ is None:
            nr, t, s = bf[ib]
            meldungen.append(("Fn %d im Band hat im Original keine Entsprechung"
                              % nr, None, normal(t)))
            continue
        onr, ot, os_ = of[io_]
        if ib is None:
            meldungen.append(("Fn %d (Original S.%d) fehlt im Band" % (onr, os_),
                              normal(ot), None))
            continue
        bnr, bt, bs = bf[ib]
        g = aehnlich(kern(ot), kern(bt))
        if g > 0.985:
            continue
        jo = sorted(set(re.findall(r"(\d{4})", normal(ot))))
        jb = sorted(set(re.findall(r"(\d{4})", normal(bt))))
        if jo != jb:
            grund = "Jahresangaben %s statt %s" % (",".join(jb), ",".join(jo))
        elif g > 0.9:
            continue          # nur Satzzeichen der Zitierweise
        else:
            grund = "Wortlaut weicht ab (%.0f%% gleich)" % (g * 100)
        meldungen.append(("Fn %d (Original S.%d, Band S.%d): %s"
                          % (onr, os_, bs, grund), normal(ot), normal(bt)))

    print("── Kapitel %d ── Original %d Fussnoten, Band %d, %d zu pruefen"
          % (kap, len(of), len(bf), len(meldungen)))
    for kopfzeile, o, b in meldungen:
        print("   " + kopfzeile)
        if o:
            print("      Original : %s" % o[:160])
        if b:
            print("      Band     : %s" % b[:160])
    gesamt += len(meldungen)
    print()

print("%d Stelle(n) zu pruefen." % gesamt)
