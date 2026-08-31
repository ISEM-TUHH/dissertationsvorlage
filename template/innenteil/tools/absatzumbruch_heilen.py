# -*- coding: utf-8 -*-
"""Behebt Hurenkinder und Schusterjungen, ohne den Text zu aendern.

    python tools/absatzumbruch_heilen.py [--anzahl N] [--probe]

  Hurenkind      die letzte Zeile eines Absatzes steht allein oben auf einer
                 Seite.
  Schusterjunge  die erste Zeile eines Absatzes steht allein unten auf einer
                 Seite.

Beides regelt Typst ueber Kosten. Global stehen sie schon hoch; hoeher
gedreht wird der Satz insgesamt schlechter, weil die Kosten ueberall wirken
und Typst dann an anderer Stelle nachgibt. Deshalb wird die Kostenstelle
hier nur fuer den einen betroffenen Absatz angehoben: sein Inhalt kommt in
ein #text(costs: ...). Das ist ein reines Satzelement - am Wortlaut, an der
Absatzform und am Raster aendert sich nichts.

Wie bei den Trennungen wird in Runden gearbeitet, weil jede Heilung den
Satz dahinter verschiebt.
"""
import glob
import os
import re
import subprocess
import sys
import unicodedata

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), "inhalt"))

ANZAHL = 25
if "--anzahl" in sys.argv:
    ANZAHL = int(sys.argv[sys.argv.index("--anzahl") + 1])
DATEI = "build/_umbruch.pdf"
KOSTEN = ('#text(costs: (widow: 4000%, orphan: 4000%))[', ']')


def bauen():
    e = subprocess.run(
        ["typst", "compile", "--root", "..", "--input", "ausgabe=druck", "main.typ", DATEI],
        capture_output=True, text=True)
    if e.returncode:
        sys.exit("Satz fehlgeschlagen:\n" + e.stderr[:2000])


def grundgrad(dok):
    h = {}
    for n in range(dok.page_count // 3, min(dok.page_count, dok.page_count // 3 + 20)):
        for b in dok[n].get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    if s["text"].strip():
                        h[round(s["size"], 1)] = (h.get(round(s["size"], 1), 0)
                                                  + len(s["text"]))
    return max(h, key=h.get)


def zeilen(seite, grad):
    """Zeilen der Grundschrift mit Angabe, ob sie einen Absatz beginnen."""
    hoehe = seite.rect.height
    roh = []
    for b in seite.get_text("dict")["blocks"]:
        if b["type"]:
            continue
        for l in b["lines"]:
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp:
                continue
            y = max(s["origin"][1] for s in sp)
            if y < hoehe * 0.08 or y > hoehe * 0.90:
                continue
            if abs(max(s["size"] for s in sp) - grad) > 0.6:
                continue
            roh.append((y, min(s["origin"][0] for s in sp),
                        "".join(s["text"] for s in sp)))
    roh.sort()
    if not roh:
        return []
    linker_rand = min(x for _, x, _ in roh)
    return [{"text": t, "absatzanfang": x > linker_rand + 3}
            for _, x, t in roh]


def schlicht(t):
    t = (t.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
          .replace("ﬀ", "ff").replace("ﬃ", "ffi"))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(z for z in t if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]", "", t.lower())


def flieszttext_bereich(dok):
    """Erste und letzte Seite des Flieszttextes, aus den Lesezeichen.

    Nur dort gilt der Erstzeileneinzug als Kennzeichen des Absatzanfangs.
    Im Literaturverzeichnis ist der Einzug haengend, also umgekehrt - dort
    wuerde jede Fortsetzungszeile als Absatzanfang gelten.
    """
    toc = dok.get_toc()
    if not toc:
        return 1, dok.page_count
    schluss = ("literaturverzeichnis", "references", "anhang", "appendix")
    anfang, ende = None, dok.page_count
    for ebene, titel, seite in toc:
        if ebene != 1:
            continue
        klein = titel.strip().lower()
        if anfang is None and klein not in (
            "inhaltsverzeichnis", "contents", "kurzfassung", "abstract",
            "danksagung", "vorwort", "vorwort zum band",
            "vorwort des herausgebers",
        ):
            anfang = seite
        if anfang is not None and klein.startswith(schluss):
            ende = seite - 1
            break
    return (anfang or 1), ende


def faelle(dok):
    """(Art, Seite, Zeilentext) fuer jedes Hurenkind und jeden Schusterjungen."""
    grad = grundgrad(dok)
    von, bis = flieszttext_bereich(dok)
    gefunden = []
    for n in range(von, bis + 1):
        z = zeilen(dok[n - 1], grad)
        if len(z) < 5:
            continue          # Abbildungsseite
        if len(z) >= 2 and not z[0]["absatzanfang"] and z[1]["absatzanfang"]:
            gefunden.append(("Hurenkind", n, z[0]["text"]))
        if z[-1]["absatzanfang"] and len(z) > 1:
            gefunden.append(("Schusterjunge", n, z[-1]["text"]))
    return gefunden


def absaetze(text):
    """(Anfang, Ende) jedes Flieszttext-Absatzes einer Kapiteldatei."""
    ergebnis = []
    pos = 0
    for stueck in text.split("\n\n"):
        anfang, ende = pos, pos + len(stueck)
        pos = ende + 2
        roh = stueck.strip()
        if not roh or roh.startswith(("=", "#figure", "#let", "//", ")",
                                      "#definitionsbox", "#zwischentitel",
                                      "-", "+", "#box(", "#pagebreak")):
            continue
        if len(schlicht(roh)) < 60:
            continue
        ergebnis.append((anfang + (len(stueck) - len(stueck.lstrip())),
                         ende - (len(stueck) - len(stueck.rstrip()))))
    return ergebnis


def heilen(art, zeilentext):
    """Hebt die Kosten fuer den betroffenen Absatz an."""
    marke = schlicht(zeilentext)[:40] if art == "Schusterjunge" \
        else schlicht(zeilentext)[-40:]
    if len(marke) < 15:
        return None
    for pfad in sorted(glob.glob("kapitel/*.typ")):
        text = open(pfad, encoding="utf-8").read()
        for a, e in absaetze(text):
            roh = text[a:e]
            if "#text(costs:" in roh:
                continue
            sauber = schlicht(re.sub(
                r'#cite\([^)]*\)|#[a-zA-Z-]+(\([^)]*\))?|<[^>]*>|[\[\]]',
                " ", roh))
            passt = (sauber.startswith(marke) if art == "Schusterjunge"
                     else sauber.endswith(marke))
            if not passt:
                continue
            neu = text[:a] + KOSTEN[0] + roh + KOSTEN[1] + text[e:]
            open(pfad, "w", encoding="utf-8", newline="\n").write(neu)
            return pfad
    return None


print("Hurenkinder und Schusterjungen heilen")
geheilt, aufgegeben = [], []
for runde in range(ANZAHL):
    bauen()
    dok = fitz.open(DATEI)
    offen = [f for f in faelle(dok) if (f[0], f[1]) not in aufgegeben]
    dok.close()
    if not offen:
        break
    art, seite, zeilentext = offen[0]
    pfad = heilen(art, zeilentext)
    if pfad:
        geheilt.append((art, seite))
        print("  + %-14s S.%-4d %-42s in %s"
              % (art, seite, re.sub(r"\s+", " ", zeilentext)[:42],
                 os.path.basename(pfad)))
    else:
        aufgegeben.append((art, seite))
        print("  ! %-14s S.%-4d %-42s Absatz nicht eindeutig"
              % (art, seite, re.sub(r"\s+", " ", zeilentext)[:42]))

bauen()
dok = fitz.open(DATEI)
rest = faelle(dok)
print()
print("%d geheilt, %d offen." % (len(geheilt), len(rest)))
for art, n, t in rest:
    print("   %-14s S.%-4d %s" % (art, n, re.sub(r"\s+", " ", t)[:50]))
