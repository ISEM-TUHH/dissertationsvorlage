# -*- coding: utf-8 -*-
"""Prueft den Umbruch des fertigen Satzes - die Dinge, die man erst am
echten Text sehen kann.

    python tools/umbruch_pruefen.py [../build/Druckversion/innenteil.pdf]

Geprueft wird, was im Buchsatz als Fehler gilt:

  Hurenkind      die letzte Zeile eines Absatzes steht allein oben auf einer
                 Seite. Der Leser faengt die Seite mit einem Rest an.
  Schusterjunge  die erste Zeile eines Absatzes steht allein unten auf einer
                 Seite. Der Absatz beginnt und ist sofort zu Ende.
  Trennung ueber den Seitenumbruch
                 die letzte Zeile einer Seite endet mit einem Trennstrich.
                 Zum Weiterlesen muss umgeblaettert werden.
  Trennungshaeufung
                 mehr als drei Zeilen untereinander enden mit Trennstrich -
                 am rechten Rand entsteht eine "Trennungsleiter".
  Kurze Schlusszeile
                 die letzte Zeile eines Absatzes ist kuerzer als der Einzug.
                 Sie wirkt wie ein Schreibfehler.
  Bildaufloesung unter 300 dpi laut Datenblatt.

Die Erkennung stuetzt sich auf den Erstzeileneinzug: eine Zeile, die weiter
rechts beginnt als der Satzrand, ist ein Absatzanfang. Das funktioniert nur,
solange der Satz mit Einzug arbeitet - siehe src/isem.typ.

Geprueft wird nur der Flieszttext der Kapitel. Verzeichnisse, Tabellen und
das Literaturverzeichnis haben eigene Umbruchregeln; dort waeren die
Befunde nur Rauschen.

Nichts davon ist ein Abbruchgrund. Es sind Stellen, an denen ein Mensch den
Text um ein Wort kuerzen oder laengen sollte.
"""
import os
import sys

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
_wurzel = os.path.dirname(os.path.dirname(os.path.dirname(HIER)))
_inhalt = "inhalt" if os.path.isdir(os.path.join(_wurzel, "inhalt")) else "inhalt-vorlage"
os.chdir(os.path.join(_wurzel, _inhalt))

MM = 72.0 / 25.4
GRUNDSCHRIFT = 10.0
EINZUG = 10.0            # 1 em bei 10 pt
MINDEST_DPI = 300.0
MAX_TRENNUNGEN = 3       # Zeilen mit Trennstrich untereinander

pfad = sys.argv[1] if len(sys.argv) > 1 else "../build/Druckversion/innenteil.pdf"
if not os.path.exists(pfad):
    raise SystemExit("Datei nicht gefunden: %s" % pfad)

befunde = []


def flieszttext_bereich(d):
    """Erste und letzte Seite des Flieszttextes, aus den Lesezeichen.

    Vom ersten nummerierten Kapitel bis zur Seite vor dem
    Literaturverzeichnis. Findet sich nichts, wird das ganze Dokument
    geprueft.
    """
    toc = d.get_toc()
    if not toc:
        return 1, d.page_count
    schluss = ("literaturverzeichnis", "references", "anhang", "appendix")
    anfang, ende = None, d.page_count
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


def melde(art, seite, text):
    befunde.append((art, seite, text))


def zeilen_der_seite(seite):
    """Flieszttextzeilen einer Seite, von oben nach unten.

    Fusznoten (9 pt) und Kolumnentitel (8 pt) bleiben auszen vor; ebenso
    Ueberschriften, die groeszer als die Grundschrift sind.
    """
    roh = []
    for block in seite.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for zeile in block["lines"]:
            spans = [s for s in zeile["spans"] if s["text"].strip()]
            if not spans:
                continue
            groesze = max(s["size"] for s in spans)
            if abs(groesze - GRUNDSCHRIFT) > 0.3:
                continue
            text = "".join(s["text"] for s in spans).rstrip()
            roh.append({
                "x0": min(s["bbox"][0] for s in spans),
                "x1": max(s["bbox"][2] for s in spans),
                "y": spans[0]["origin"][1],
                "text": text,
            })
    roh.sort(key=lambda z: z["y"])

    # Zeilen, die sich eine Grundlinie teilen, gehoeren zu einer Tabelle oder
    # einem Raster - dort gibt es keine Absaetze im Sinne dieser Pruefung.
    gefiltert = []
    for i, z in enumerate(roh):
        nachbar = any(
            j != i and abs(roh[j]["y"] - z["y"]) < 1.0 for j in range(len(roh))
        )
        if not nachbar:
            gefiltert.append(z)
    return gefiltert


def auswerten(d, von, bis):
    seiten = []
    for seite in d:
        if not (von <= seite.number + 1 <= bis):
            seiten.append(None)
            continue
        zeilen = zeilen_der_seite(seite)
        if not zeilen:
            seiten.append(None)
            continue
        rand = min(z["x0"] for z in zeilen)
        for z in zeilen:
            z["absatzanfang"] = z["x0"] > rand + EINZUG * 0.5
            z["breite"] = z["x1"] - z["x0"]
            z["trennung"] = z["text"].endswith("-") or z["text"].endswith("­")
        seiten.append({"nr": seite.number + 1, "zeilen": zeilen, "rand": rand})

    for eintrag in seiten:
        if eintrag is None:
            continue
        nr, zeilen = eintrag["nr"], eintrag["zeilen"]
        # Eine Seite mit wenigen Zeilen ist ein Kapitelanfang oder eine
        # Abbildungsseite - dort sagt die Zeilenlage nichts aus.
        if len(zeilen) < 5:
            continue

        # Hurenkind: erste Zeile setzt einen Absatz der Vorseite fort und ist
        # zugleich dessen letzte.
        if len(zeilen) >= 2 and not zeilen[0]["absatzanfang"] and zeilen[1]["absatzanfang"]:
            melde("Hurenkind", nr, zeilen[0]["text"][:60])

        # Schusterjunge: letzte Zeile beginnt einen Absatz.
        if zeilen[-1]["absatzanfang"] and len(zeilen) > 1:
            melde("Schusterjunge", nr, zeilen[-1]["text"][:60])

        # Trennung ueber den Seitenumbruch.
        if zeilen[-1]["trennung"]:
            melde("Trennung am Seitenende", nr, zeilen[-1]["text"][-40:])

        # Trennungsleiter.
        lauf = 0
        for z in zeilen:
            lauf = lauf + 1 if z["trennung"] else 0
            if lauf == MAX_TRENNUNGEN + 1:
                melde("%d Trennungen untereinander" % lauf, nr, z["text"][-40:])

        # Kurze Absatzschlusszeile.
        for i, z in enumerate(zeilen):
            letzte_des_absatzes = (i + 1 == len(zeilen)) or zeilen[i + 1]["absatzanfang"]
            if letzte_des_absatzes and i + 1 < len(zeilen) and z["breite"] < 2 * EINZUG:
                melde("kurze Schlusszeile", nr, z["text"][:40])

    # Bildaufloesung - hier ueber das ganze Dokument.
    for seite in d:
        for info in seite.get_image_info(xrefs=True):
            r = fitz.Rect(info["bbox"])
            if r.width <= 0 or r.height <= 0:
                continue
            dpi = min(info["width"] / (r.width / 72.0),
                      info["height"] / (r.height / 72.0))
            if dpi < MINDEST_DPI - 1:
                melde("Bild unter 300 dpi", seite.number + 1, "%.0f dpi" % dpi)


d = fitz.open(pfad)
von, bis = flieszttext_bereich(d)
print("Umbruchpruefung: %s  (%d Seiten)" % (pfad, d.page_count))
print("Flieszttext: Seite %d bis %d" % (von, bis))
auswerten(d, von, bis)

if not befunde:
    print("\n  Keine Auffaelligkeiten.")
else:
    breite = max(len(a) for a, _, _ in befunde)
    art_vorher = None
    for art, seite, text in sorted(befunde, key=lambda b: (b[0], b[1])):
        if art != art_vorher:
            print()
            art_vorher = art
        print("  [ ?] %-*s Seite %3d  %s" % (breite, art, seite, text))

print("\n%d Hinweis(e). Keiner davon ist ein Abbruchgrund - jeder ist eine "
      "Stelle,\nan der ein Wort mehr oder weniger den Umbruch rettet."
      % len(befunde))
