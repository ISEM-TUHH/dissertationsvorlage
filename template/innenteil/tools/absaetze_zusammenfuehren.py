# -*- coding: utf-8 -*-
"""Fuegt Absaetze zusammen, die der Seitenumbruch des Originals zerrissen hat.

    python tools/absaetze_zusammenfuehren.py <original.pdf> [--aendern]

Beim Zuruecklesen wurde jede Originalseite fuer sich genommen. Lief ein Satz
ueber den Seitenumbruch, entstanden daraus zwei Absaetze - erkennbar daran,
dass der erste ohne Satzzeichen endet und der zweite klein anfaengt.

Ob die beiden wirklich zusammengehoeren, entscheidet das Original: nur wenn
dort das Ende des einen unmittelbar in den Anfang des anderen uebergeht,
werden sie verbunden.

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
    sys.exit("Aufruf: python tools/absaetze_zusammenfuehren.py <original.pdf> "
             "[--aendern]")
AENDERN = "--aendern" in sys.argv

orig = fitz.open(argumente[0])


def schlicht(t):
    t = (t.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
          .replace("ﬀ", "ff").replace("ﬃ", "ffi"))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(z for z in t if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]", "", t.lower())


def originaltext():
    """Der Flieszttext des Originals als eine Buchstabenfolge."""
    stuecke = []
    for n in range(orig.page_count):
        seite = orig[n]
        hoehe = seite.rect.height
        for b in seite.get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp:
                    continue
                y = max(s["origin"][1] for s in sp)
                if y < hoehe * 0.08 or y > hoehe * 0.86:
                    continue
                stuecke.append("".join(s["text"] for s in sp))
    return schlicht(" ".join(stuecke))


TEXT = originaltext()


def ohne_auszeichnung(s):
    s = re.sub(r"#footnote\[(?:[^][]|\[[^]]*\])*\]", " ", s)
    s = re.sub(r"#quelle\(<[^>]*>\)|#cite\([^)]*\)|#link\(<[^>]*>\)", " ", s)
    s = re.sub(r"#[a-zA-Z-]+(\([^)]*\))?", " ", s)
    s = re.sub(r"<[^>]*>|@[a-zA-Z][\w]*|[\[\]$]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def ist_flieszttext(zeile):
    roh = zeile.strip()
    if not roh or len(ohne_auszeichnung(roh)) < 40:
        return False
    if roh.startswith(("=", "//", "#", "-", "+", ")", "*")):
        return False
    if re.match(r"^(abbildung|caption:|alt:|kind:)", roh):
        return False
    return True


gesamt = 0
for pfad in sorted(glob.glob("kapitel/*.typ")):
    zeilen = io.open(pfad, encoding="utf-8").read().split("\n")
    geaendert = True
    while geaendert:
        geaendert = False
        for i, zeile in enumerate(zeilen):
            if not ist_flieszttext(zeile):
                continue
            ende = ohne_auszeichnung(zeile)
            if ende.rstrip().endswith((".", "!", "?", ":", "“", ";", "”")):
                continue
            # Der naechste Flieszttextabsatz.
            j = next((k for k in range(i + 1, len(zeilen))
                      if ist_flieszttext(zeilen[k])), None)
            if j is None:
                continue
            anfang = ohne_auszeichnung(zeilen[j])
            # Eine nummerierte Aufzaehlung faengt neu an, sie wird nicht
            # angehaengt.
            if re.match(r"\d+\.\s", zeilen[j].strip()):
                continue
            # Eine Zwischenueberschrift steht ohne Satzzeichen fuer sich.
            if len(ende) < 90 and not re.search(r"[.!?,;:]", ende):
                continue
            probe = schlicht(ende[-30:]) + schlicht(anfang[:30])
            if len(probe) < 40 or probe not in TEXT:
                continue
            gesamt += 1
            print("  %-40s Z.%-5d …%s  +  %s…"
                  % (os.path.basename(pfad)[:38], i + 1, ende[-42:],
                     anfang[:42]))
            if AENDERN:
                zeilen[i] = zeile.rstrip() + " " + zeilen[j].lstrip()
                del zeilen[j]
                # Die Leerzeile, die den entfernten Absatz umgab, faellt weg.
                while j < len(zeilen) and not zeilen[j].strip() and \
                        j + 1 < len(zeilen) and not zeilen[j + 1].strip():
                    del zeilen[j]
                geaendert = True
                break
    if AENDERN:
        io.open(pfad, "w", encoding="utf-8", newline="\n").write(
            re.sub(r"\n{3,}", "\n\n", "\n".join(zeilen)))

print()
print("%d zerrissene Absaetze%s."
      % (gesamt, " zusammengefuehrt" if AENDERN else " gefunden"))
