# -*- coding: utf-8 -*-
"""Behebt Trennungen am Seitenende, ohne den Text zu aendern.

    python tools/umbruch_heilen.py [--anzahl N] [--auch-verso] [--probe]

Eine Worttrennung am Fusz einer rechten Seite zwingt den Leser, mit einem
halben Wort im Kopf umzublaettern. Der Buchsatz vermeidet sie. Typst kennt
dafuer keine eigene Kostenstelle: Trennungskosten wirken auf jede Trennung,
nicht nur auf die am Seitenende - das macht den Flattersatz schlechter, ohne
das eigentliche Problem zu loesen.

Deshalb wird hier genau das eine Wort behandelt, das umbricht: es kommt in
eine #box[...]. Eine Box wird nicht getrennt, also wandert das Wort ganz auf
die naechste Seite. Am Wortlaut aendert sich nichts - im Druck ist der
Eingriff unsichtbar.

Weil jede Heilung den Satz dahinter verschiebt, arbeitet das Werkzeug in
Runden: bauen, die vorderste Trennung heilen, neu bauen. Standardmaeszig
werden nur rechte Seiten behandelt; mit --auch-verso auch linke.
"""
import glob
import os
import re
import subprocess
import sys
import unicodedata

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HIER))

ANZAHL = 40
if "--anzahl" in sys.argv:
    ANZAHL = int(sys.argv[sys.argv.index("--anzahl") + 1])
AUCH_VERSO = "--auch-verso" in sys.argv
PROBE = "--probe" in sys.argv
DATEI = "build/_umbruch.pdf"


def bauen():
    ergebnis = subprocess.run(
        ["typst", "compile", "--input", "ausgabe=druck", "main.typ", DATEI],
        capture_output=True, text=True)
    if ergebnis.returncode:
        sys.exit("Satz fehlgeschlagen:\n" + ergebnis.stderr[:2000])


def zeilen_der_seite(seite):
    """Textzeilen des Satzspiegels, von oben nach unten."""
    hoehe = seite.rect.height
    gesammelt = []
    for b in seite.get_text("dict")["blocks"]:
        if b["type"]:
            continue
        for l in b["lines"]:
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp:
                continue
            y = max(s["origin"][1] for s in sp)
            if y < hoehe * 0.08 or y > hoehe * 0.90:
                continue          # Kolumnentitel und Seitenzahl
            gesammelt.append((y, max(s["size"] for s in sp),
                              "".join(s["text"] for s in sp)))
    gesammelt.sort()
    return gesammelt


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


def schlicht(t):
    t = (t.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
          .replace("ﬀ", "ff").replace("ﬃ", "ffi"))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(z for z in t if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]", "", t.lower())


def trennungen(dok):
    """(Seite, Wortanfang, Wortende, Text davor) je Trennung am Seitenende."""
    erste, letzte = 1, dok.page_count
    grad = grundgrad(dok, max(1, dok.page_count // 3),
                     min(dok.page_count, dok.page_count // 3 + 20))
    gefunden = []
    for n in range(erste, letzte):
        # Nur Zeilen der Grundschrift zaehlen: unter dem Flieszttext steht
        # der Fussnotenapparat, und der ist nie die letzte Textzeile im
        # Sinne des Umbruchs.
        oben = [z for z in zeilen_der_seite(dok[n - 1])
                if abs(z[1] - grad) <= 0.6]
        unten = [z for z in zeilen_der_seite(dok[n])
                 if abs(z[1] - grad) <= 0.6]
        if not oben or not unten:
            continue
        _, _, letzte_zeile = oben[-1]
        if not letzte_zeile.rstrip().endswith(("­", "-", "‐")):
            continue
        _, _, erste_zeile = unten[0]
        anfang = re.search(r"([\wäöüÄÖÜß]+)[­\-‐]\s*$",
                           letzte_zeile.rstrip())
        ende = re.match(r"([\wäöüÄÖÜß]+)", erste_zeile.lstrip())
        if not anfang or not ende:
            continue
        davor = letzte_zeile[:anfang.start(1)]
        gefunden.append((n, anfang.group(1), ende.group(1), davor))
    return gefunden


def kapiteldateien():
    return sorted(glob.glob("kapitel/*.typ"))


def heilen(wortanfang, wortende, davor):
    """Setzt das umbrechende Wort in eine Box. Gibt die Datei zurueck."""
    wort = wortanfang + wortende
    ziel = schlicht(davor)[-30:]
    for pfad in kapiteldateien():
        text = open(pfad, encoding="utf-8").read()
        for m in re.finditer(r"(?<![\w#\[])" + re.escape(wort)
                             + r"(?![\wäöüÄÖÜß])", text):
            if "#box[" + wort in text[max(0, m.start() - 6):m.end() + 1]:
                continue
            vorher = schlicht(re.sub(r"#[a-zA-Z-]+(\([^)]*\))?|<[^>]*>|[\[\]]",
                                     " ", text[max(0, m.start() - 400):m.start()]))
            if len(ziel) >= 12 and not vorher.endswith(ziel[-12:]):
                continue
            neu = text[:m.start()] + "#box[" + wort + "]" + text[m.end():]
            open(pfad, "w", encoding="utf-8", newline="\n").write(neu)
            return pfad
    return None


print("Trennungen am Seitenende heilen (%s)"
      % ("nur rechte Seiten" if not AUCH_VERSO else "rechte und linke Seiten"))
geheilt, aufgegeben = [], []
for runde in range(ANZAHL):
    bauen()
    dok = fitz.open(DATEI)
    offen = [t for t in trennungen(dok)
             if (AUCH_VERSO or t[0] % 2 == 1)
             and (t[0], t[1] + t[2]) not in aufgegeben]
    dok.close()
    if not offen:
        break
    seite, a, b, davor = offen[0]
    pfad = heilen(a, b, davor)
    if pfad:
        geheilt.append((seite, a + "-" + b, pfad))
        print("  + S.%-4d %s%s  ->  #box[%s]  in %s"
              % (seite, a, "­" + b, a + b, os.path.basename(pfad)))
    else:
        aufgegeben.append((seite, a + b))
        print("  ! S.%-4d %s%s  Stelle im Quelltext nicht eindeutig"
              % (seite, a, "­" + b))

bauen()
dok = fitz.open(DATEI)
rest = trennungen(dok)
print()
print("%d Trennung(en) geheilt, %d offen (%d davon auf linken Seiten)."
      % (len(geheilt), len(rest), sum(1 for t in rest if t[0] % 2 == 0)))
for n, a, b, _ in rest:
    print("   S.%-4d %s%s%s" % (n, a, "­", b))
