# -*- coding: utf-8 -*-
"""Findet Abbildungen, die mitten im Satz stehen.

    python tools/bilder_einordnen.py [--aendern]

Beim Zuruecklesen aus dem PDF wurde jede Abbildung dort eingefuegt, wo sie
im Original gesetzt war. Der Satz laeuft dort aber weiter: die Abbildung
steht zwischen zwei Haelften desselben Satzes. Im Band, der anders
umbricht, zerreiszt sie den Text sichtbar.

Erkannt wird das an den beiden Nachbarn: endet der Absatz davor nicht mit
einem Satzzeichen, oder faengt der Absatz danach klein an, gehoert die
Abbildung nicht an diese Stelle. Sie wandert dann hinter den Absatz, der
sie erwaehnt - oder, wenn es den nicht gibt, hinter den naechsten
vollstaendigen Absatz.

Ohne --aendern wird nur berichtet.
"""
import glob
import io
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HIER))

AENDERN = "--aendern" in sys.argv


def bloecke(text):
    """Der Quelltext als Folge von Absaetzen und Abbildungsblocken."""
    zeilen = text.split("\n")
    ergebnis = []
    i = 0
    while i < len(zeilen):
        if zeilen[i].startswith("#figure("):
            j = i
            while j < len(zeilen) and not zeilen[j].startswith(") <"):
                j += 1
            ergebnis.append(("bild", zeilen[i:j + 1]))
            i = j + 1
        else:
            ergebnis.append(("text", [zeilen[i]]))
            i += 1
    return ergebnis


def ist_absatz(zeile):
    roh = zeile.strip()
    return bool(roh) and not roh.startswith(("=", "//", "#let", "#pagebreak",
                                             "#zwischentitel", "#definitionsbox"))


def ohne_auszeichnung(s):
    s = re.sub(r"#footnote\[(?:[^][]|\[[^]]*\])*\]", " ", s)
    s = re.sub(r"#quelle\(<[^>]*>\)|#cite\([^)]*\)", " ", s)
    s = re.sub(r"#link\(<[^>]*>\)", " ", s)
    s = re.sub(r"#[a-zA-Z-]+(\([^)]*\))?", " ", s)
    s = re.sub(r"<[^>]*>|@[a-zA-Z][\w]*|[\[\]$]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def marke_von(bild):
    for zeile in bild:
        m = re.search(r"<((?:abb|tab)-[0-9-]+)>", zeile)
        if m:
            return m.group(1)
    return None


def nummer_von(marke):
    teile = marke.split("-")
    return "%s.%s" % (teile[1], teile[2]) if len(teile) >= 3 else None


gesamt = 0
for pfad in sorted(glob.glob("kapitel/*.typ")):
    text = io.open(pfad, encoding="utf-8").read()
    folge = bloecke(text)
    umgestellt = False

    for stelle, (art, inhalt) in enumerate(folge):
        if art != "bild":
            continue
        # Der letzte Absatz davor und der erste danach.
        davor = next((z[0] for a, z in reversed(folge[:stelle])
                      if a == "text" and ist_absatz(z[0])), "")
        danach_i = next((k for k in range(stelle + 1, len(folge))
                         if folge[k][0] == "text" and ist_absatz(folge[k][1][0])),
                        None)
        danach = folge[danach_i][1][0] if danach_i is not None else ""
        vor_text = ohne_auszeichnung(davor)
        nach_text = ohne_auszeichnung(danach)
        if not vor_text or not nach_text:
            continue
        zerreiszt = (not vor_text.rstrip().endswith((".", "!", "?", ":", "“"))
                     or (nach_text[:1].islower() and not nach_text.startswith("und ")))
        if not zerreiszt:
            continue

        marke = marke_von(inhalt)
        gesamt += 1
        print("  %-40s %-10s nach: …%s"
              % (os.path.basename(pfad)[:38], marke or "?", vor_text[-55:]))
        if not AENDERN:
            continue

        # Die Abbildung hinter den Absatz setzen, der auf sie verweist.
        nummer = nummer_von(marke) if marke else None
        ziel = None
        if nummer:
            for k in range(stelle + 1, len(folge)):
                if folge[k][0] != "text":
                    continue
                if re.search(r"(Abbildung|Abb\.|Tabelle|Tab\.)\D{0,4}%s\b"
                             % re.escape(nummer), folge[k][1][0]):
                    ziel = k
                    break
        if ziel is None:
            ziel = danach_i
        if ziel is None:
            continue
        folge[stelle] = ("leer", [])
        folge[ziel] = (folge[ziel][0], folge[ziel][1] + [""] + inhalt)
        umgestellt = True

    if umgestellt and AENDERN:
        neu = []
        for art, inhalt in folge:
            neu.extend(inhalt)
        io.open(pfad, "w", encoding="utf-8", newline="\n").write(
            re.sub(r"\n{3,}", "\n\n", "\n".join(neu)))

print()
print("%d Abbildung(en) mitten im Satz%s."
      % (gesamt, " umgesetzt" if AENDERN else " gefunden"))
