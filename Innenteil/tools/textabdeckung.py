# -*- coding: utf-8 -*-
"""Misst, wieviel Text des Originals im Band tatsaechlich steht.

    python tools/textabdeckung.py <original.pdf> [kapitel ...]

Der Satzabgleich stolpert ueber Abbildungen, die einen Satz zerteilen, und
meldet dann Luecken, die keine sind. Hier wird deshalb nicht nach Saetzen
gesucht, sondern nach Textfenstern: aus dem Original werden alle 200
Buchstaben 70 Buchstaben lang Proben genommen und im Band gesucht. Fehlt
eine Probe, fehlt an dieser Stelle Text - unabhaengig davon, wie der Band
umbricht.

Ausgegeben wird die Abdeckung je Kapitel und die Fundstelle jeder Luecke.
"""
import os
import re
import sys
import unicodedata

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HIER))

if len(sys.argv) < 2:
    sys.exit("Aufruf: python tools/textabdeckung.py <original.pdf> [kapitel ...]")
ORIGINAL = sys.argv[1]
KAPITEL = [int(a) for a in sys.argv[2:]] or list(range(1, 8))

SCHRITT = 200        # Abstand der Proben
PROBE = 70           # Laenge einer Probe

orig = fitz.open(ORIGINAL)
band = fitz.open("../build/Onlineversion/innenteil.pdf")


def kapitelbereich(dok, nr):
    alle = [e for e in dok.get_toc() if e[0] == 1]
    for e in alle:
        if re.match(r"^%d\s" % nr, e[1].strip()):
            spaeter = [x[2] for x in alle if x[2] > e[2]]
            return e[2], (min(spaeter) - 1 if spaeter else dok.page_count)
    return None, None


def buchstaben(t):
    t = (t.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
          .replace("ﬀ", "ff").replace("ﬃ", "ffi"))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(z for z in t if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]", "", t.lower())


def volltext(dok, von, bis):
    """Nur der Flieszttext: ohne Kolumnentitel, Seitenzahl, Fussnotenapparat
    und ohne die hochgestellten Verweisziffern.

    Diese Bestandteile stehen in Original und Band an verschiedenen Stellen
    und in verschiedener Form. Bleiben sie stehen, meldet der Vergleich
    Luecken, wo in Wahrheit nur die Verweisziffer anders gesetzt ist.
    """
    grad = grundgrad(dok, von, bis)
    stuecke = []
    for n in range(von, bis + 1):
        seite = dok[n - 1]
        hoehe = seite.rect.height
        for b in seite.get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp:
                    continue
                grundlinie = max(s["origin"][1] for s in sp)
                if grundlinie < hoehe * 0.08 or grundlinie > hoehe * 0.86:
                    continue
                gross = max(s["size"] for s in sp)
                if gross < grad - 0.8:
                    continue          # Fussnotenapparat und Beschriftungen
                for s in sp:
                    hoch = (s["size"] < gross - 1.0
                            and s["origin"][1] < grundlinie - 1.0)
                    if hoch and re.fullmatch(r"\d{1,3}", s["text"].strip()):
                        continue      # Verweisziffer
                    stuecke.append(s["text"])
    return buchstaben(" ".join(stuecke))


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


def seite_zu(dok, von, bis, anteil):
    """Grobe Seitenangabe zu einer Position im Volltext."""
    laenge = 0
    ziel = anteil
    for n in range(von, bis + 1):
        laenge += len(volltext(dok, n, n))
        if laenge >= ziel:
            return n
    return bis


gesamt_proben = gesamt_fehlend = 0
for kap in KAPITEL:
    ov, ob = kapitelbereich(orig, kap)
    bv, bb = kapitelbereich(band, kap)
    if ov is None or bv is None:
        continue
    otext = volltext(orig, ov, ob)
    btext = volltext(band, bv, bb)

    proben = fehlend = 0
    luecken = []
    for pos in range(0, len(otext) - PROBE, SCHRITT):
        stueck = otext[pos:pos + PROBE]
        proben += 1
        if stueck in btext:
            continue
        # Eine Probe kann auch dann fehlen, wenn nur ihre Mitte anders
        # zusammengesetzt ist: an einer Ueberschrift, an einer Abbildung
        # oder wo der Band die Trennung anders aufloest. Erst wenn auch
        # beide Haelften fehlen, fehlt hier wirklich Text.
        halb = PROBE // 2
        if stueck[:halb] in btext or stueck[halb:] in btext:
            continue
        fehlend += 1
        luecken.append((pos, stueck))

    # Benachbarte Fehlstellen zu einer Luecke zusammenfassen.
    gebuendelt = []
    for pos, stueck in luecken:
        if gebuendelt and pos - gebuendelt[-1][1] <= SCHRITT:
            gebuendelt[-1][1] = pos
        else:
            gebuendelt.append([pos, pos, stueck])

    abdeckung = 100.0 * (proben - fehlend) / proben if proben else 100.0
    print("── Kapitel %d ── %d Proben, %.1f %% gefunden, %d Luecke(n)"
          % (kap, proben, abdeckung, len(gebuendelt)))
    for anfang, ende, stueck in gebuendelt:
        zeichen = ende - anfang + PROBE
        print("   ~%4d Zeichen ab Originalseite %d: %s"
              % (zeichen, seite_zu(orig, ov, ob, anfang), stueck[:60]))
    gesamt_proben += proben
    gesamt_fehlend += fehlend
    print()

if gesamt_proben:
    print("Insgesamt %.1f %% des Originaltextes im Band gefunden (%d von %d "
          "Proben)." % (100.0 * (gesamt_proben - gesamt_fehlend) / gesamt_proben,
                        gesamt_proben - gesamt_fehlend, gesamt_proben))
