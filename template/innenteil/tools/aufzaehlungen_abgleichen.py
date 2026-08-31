# -*- coding: utf-8 -*-
"""Prueft die Grenzen der Aufzaehlungen am Original.

    python tools/aufzaehlungen_abgleichen.py <original.pdf> [--aendern]

Beim Herstellen der Aufzaehlungen wurde an den Spiegelstrichen geteilt. Der
Text, der im Original hinter der Liste weitergeht, blieb dabei am letzten
Punkt haengen - er steht jetzt faelschlich mit im Aufzaehlungszeichen.

Das Original weisz es besser: dort beginnt jeder Punkt mit einem
Spiegelstrich am linken Rand, und der Absatz danach beginnt ohne. Hier wird
deshalb zu jedem Punkt der Kapiteldatei die Stelle im Original gesucht und
gelesen, wie weit der Punkt dort reicht. Was darueber hinausgeht, wandert in
einen eigenen Absatz hinter die Liste.

Ohne --aendern wird nur berichtet.
"""
import glob
import io
import os
import re
import sys
import unicodedata

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), "inhalt"))

argumente = [a for a in sys.argv[1:] if not a.startswith("--")]
if not argumente:
    sys.exit("Aufruf: python tools/aufzaehlungen_abgleichen.py <original.pdf> "
             "[--aendern]")
ORIGINAL = argumente[0]
AENDERN = "--aendern" in sys.argv

orig = fitz.open(ORIGINAL)


def schlicht(t):
    t = (t.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
          .replace("ﬀ", "ff").replace("ﬃ", "ffi"))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(z for z in t if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]", "", t.lower())


def original_punkte():
    """Alle Aufzaehlungspunkte des Originals als Buchstabenfolge.

    Erkannt werden sie am Einzug, nicht am Text: im Original stehen die
    Punkte eingerueckt (x rund 90), der Flieszttext am Satzrand (x rund 71).
    Ein Punkt endet, sobald eine Zeile wieder am Satzrand beginnt - dort
    faengt der Absatz hinter der Liste an.
    """
    punkte = []
    laufend = None
    for n in range(orig.page_count):
        seite = orig[n]
        hoehe = seite.rect.height
        zeilen = []
        for b in seite.get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp:
                    continue
                y = max(s["origin"][1] for s in sp)
                # Kolumnentitel, Seitenzahl und Fussnotenapparat stehen
                # ebenfalls eingerueckt und wuerden sonst an den laufenden
                # Punkt angehaengt.
                if y < hoehe * 0.08 or y > hoehe * 0.86:
                    continue
                zeilen.append((l["bbox"][1], l["bbox"][0],
                               "".join(s["text"] for s in sp)))
        if not zeilen:
            continue
        zeilen.sort()
        rand = min(x for _, x, _ in zeilen)
        for _, x, roh in zeilen:
            roh = roh.strip()
            eingerueckt = x > rand + 8
            # Das Leerzeichen hinter dem Strich ist im Original eine
            # Positionierung, kein Zeichen: die Zeile beginnt mit "-Problem".
            if eingerueckt and roh[:1] in ("-", "–", "•"):
                if laufend:
                    punkte.append(laufend)
                laufend = roh[1:].lstrip()
            elif laufend is not None and eingerueckt:
                laufend += " " + roh
            elif laufend is not None:
                punkte.append(laufend)
                laufend = None
    if laufend:
        punkte.append(laufend)
    return [schlicht(p) for p in punkte if len(schlicht(p)) > 25]


PUNKTE = original_punkte()


def echtes_ende(punkt_text):
    """Wie weit reicht dieser Punkt im Original?

    Rueckgabe: Anzahl der Buchstaben, die zum Punkt gehoeren, oder None,
    wenn er im Original nicht gefunden wird.
    """
    kern = schlicht(punkt_text)
    if len(kern) < 25:
        return None
    anfang = kern[:25]
    for p in PUNKTE:
        if p.startswith(anfang):
            return len(p)
    return None


def buchstabenstelle(text, anzahl):
    """Position im Rohtext, an der die anzahl-te Buchstabe endet."""
    gezaehlt = 0
    i = 0
    while i < len(text):
        if gezaehlt >= anzahl:
            return i
        z = text[i]
        if schlicht(z):
            gezaehlt += 1
        i += 1
    return len(text)


gesamt = 0
for pfad in sorted(glob.glob("kapitel/*.typ")):
    text = io.open(pfad, encoding="utf-8").read()
    zeilen = text.split("\n")
    geaendert = False
    for i, zeile in enumerate(zeilen):
        if not zeile.startswith("- "):
            continue
        inhalt = zeile[2:]
        laenge = echtes_ende(inhalt)
        if laenge is None:
            continue
        if len(schlicht(inhalt)) <= laenge + 8:
            continue          # passt
        schnitt = buchstabenstelle(inhalt, laenge)
        # Auf die naechste Satzgrenze aufrunden, damit kein Wort zerfaellt.
        m = re.compile(r"[.!?)\]]\s").search(inhalt, max(0, schnitt - 60))
        if m:
            schnitt = m.end()
        punkt, rest = inhalt[:schnitt].rstrip(), inhalt[schnitt:].strip()
        if len(schlicht(rest)) < 20:
            continue
        gesamt += 1
        print("  %-40s Z.%-5d Rest (%d Zeichen): %s"
              % (os.path.basename(pfad)[:38], i + 1, len(rest),
                 re.sub(r"\s+", " ", rest)[:80]))
        zeilen[i] = "- " + punkt + "\n\n" + rest
        geaendert = True
    if geaendert and AENDERN:
        io.open(pfad, "w", encoding="utf-8", newline="\n").write("\n".join(zeilen))

print()
print("%d Aufzaehlungspunkt(e) mit angehaengtem Flieszttext%s."
      % (gesamt, " getrennt" if AENDERN else " gefunden"))

# ── Gegenprobe: Punkte des Originals, die im Band keine Liste sind ───────
band = ""
for pfad in sorted(glob.glob("kapitel/*.typ")) + sorted(glob.glob("titelei/*.typ")):
    band += io.open(pfad, encoding="utf-8").read() + chr(10)
def ohne_auszeichnung(s):
    s = re.sub(r'#cite\(<[^>]*>[^)]*\)|#quelle\(<[^>]*>\)', ' ', s)
    s = re.sub(r'#footnote\[(?:[^][]|\[[^]]*\])*\]', ' ', s)
    s = re.sub(r'#link\(<[^>]*>\)', ' ', s)
    s = re.sub(r'#[a-zA-Z-]+(\([^)]*\))?', ' ', s)
    return re.sub(r'<[^>]*>|[\[\]]|@[a-zA-Z][\w]*', ' ', s)


listenpunkte = set()
for zeile in band.split(chr(10)):
    if zeile.startswith("- "):
        listenpunkte.add(schlicht(ohne_auszeichnung(zeile[2:]))[:30])
ganzer_band = schlicht(ohne_auszeichnung(band))

print()
fehlend = 0
for punkt in PUNKTE:
    anfang = punkt[:30]
    if anfang in listenpunkte:
        continue
    if anfang not in ganzer_band:
        continue          # steht ueberhaupt nicht im Band - andere Baustelle
    fehlend += 1
    print("  im Band kein Aufzaehlungspunkt: %s" % punkt[:80])
print("%d Punkt(e) des Originals stehen im Band als Flieszttext." % fehlend)
