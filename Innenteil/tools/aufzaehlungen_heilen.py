# -*- coding: utf-8 -*-
"""Macht aus eingelaufenen Spiegelstrichen wieder Aufzaehlungen.

    python tools/aufzaehlungen_heilen.py [--aendern]

Beim Zuruecklesen aus dem PDF sind Aufzaehlungen in den Flieszttext
geraten: die Punkte stehen hintereinander in einer Zeile, getrennt durch
Spiegelstriche. Im Satz erscheinen sie dann als Fliesztext statt als Liste.

Nicht jeder Spiegelstrich ist ein Aufzaehlungszeichen - "die INCOSE - die
groeszte Organisation fuer Systems Engineering - in Zusammenarbeit" ist ein
Einschub. Unterschieden wird an zwei sicheren Merkmalen:

  A  Der Absatz beginnt mit einem geschuetzten Spiegelstrich (\\-). Dann war
     er im Original schon eine Liste, deren erster Punkt erhalten blieb.
  B  Der Absatz enthaelt einen Doppelpunkt, auf den unmittelbar ein
     Spiegelstrich folgt. Der Doppelpunkt kuendigt die Aufzaehlung an.

In beiden Faellen muessen mindestens zwei Punkte zusammenkommen.

Ohne --aendern wird nur gezeigt, was geschehen wuerde.
"""
import glob
import io
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HIER))

AENDERN = "--aendern" in sys.argv

# Ein Doppelpunkt, dem noch eine Fussnote oder ein Zitat folgen darf.
NACH_DOPPELPUNKT = re.compile(
    r":((?:#footnote\[(?:[^][]|\[[^]]*\])*\]|@[a-zA-Z][\w]*|\s)*)-\s")


def punkte_teilen(rest):
    """Teilt den Aufzaehlungsteil an den Spiegelstrichen."""
    teile = re.split(r"\s+-\s+", rest.strip())
    return [t.strip() for t in teile if t.strip()]


def behandeln(zeile):
    """Gibt die Ersetzung zurueck oder None."""
    roh = zeile.rstrip()

    # A: der Absatz beginnt selbst mit einem Spiegelstrich.
    if roh.lstrip().startswith("\\-"):
        rest = roh.lstrip()[2:]
        punkte = punkte_teilen(rest)
        if len(punkte) < 2:
            return None
        return "\n".join("- " + p for p in punkte)

    # B: ein Doppelpunkt kuendigt die Aufzaehlung an.
    m = NACH_DOPPELPUNKT.search(roh)
    if not m:
        return None
    kopf = roh[:m.start() + 1] + m.group(1).rstrip()
    punkte = punkte_teilen(roh[m.end():])
    if len(punkte) < 2:
        return None
    return kopf + "\n\n" + "\n".join("- " + p for p in punkte)


gesamt = 0
for pfad in sorted(glob.glob("kapitel/*.typ")) + sorted(glob.glob("titelei/*.typ")):
    text = io.open(pfad, encoding="utf-8").read()
    zeilen = text.split("\n")
    geaendert = False
    for i, zeile in enumerate(zeilen):
        if zeile.count(" - ") < 1:
            continue
        neu = behandeln(zeile)
        if neu is None or neu == zeile:
            continue
        anzahl = neu.count("\n- ") + (1 if neu.startswith("- ") else 0)
        print("  %-40s Z.%-5d %d Punkte: %s"
              % (os.path.basename(pfad)[:38], i + 1, anzahl,
                 re.sub(r"\s+", " ", zeile)[:70]))
        zeilen[i] = neu
        geaendert = True
        gesamt += 1
    if geaendert and AENDERN:
        io.open(pfad, "w", encoding="utf-8", newline="\n").write("\n".join(zeilen))

print()
print("%d Aufzaehlung(en)%s." % (gesamt, " hergestellt" if AENDERN else " gefunden"))
