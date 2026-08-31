# -*- coding: utf-8 -*-
"""Setzt die Online-Gesamtdatei zusammen: Titelseite, Innenteil, Rückseite.

    python tools/gesamt.py

Nur für die Onlinefassung. Die Druckerei bekommt Umschlag und Innenteil
getrennt - warum, steht in docs/ANLEITUNG.md.

Was das Skript leistet:
  - hängt die Titelseite (U1) vorn und die Rückseite (U4) hinten an
  - übernimmt die Lesezeichen des Innenteils und verschiebt sie um die
    vorangestellte Seite
  - setzt Dokumentsprache, Doppelseiten-Ansicht und Titelanzeige
  - setzt PDF-Seitenlabels, damit der Reader dieselbe Seitenzahl anzeigt,
    die auch gedruckt auf der Seite steht: Umschlag ohne Nummer, Titelei
    römisch, Hauptteil arabisch ab 1
"""
import os
import sys

import fitz

BASIS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(BASIS)

COVER = "build/Onlineversion/umschlag.pdf"
INNEN = "build/Onlineversion/innenteil.pdf"
ZIEL = "build/Onlineversion/dissertation.pdf"


def main():
    for pfad in (COVER, INNEN):
        if not os.path.exists(pfad):
            sys.exit("fehlt: %s - zuerst .\\template\\bauen.ps1 ausführen." % pfad)

    cover = fitz.open(COVER)
    innen = fitz.open(INNEN)
    if cover.page_count != 2:
        sys.exit("%s muss genau zwei Seiten haben (Titelseite, Rückseite)." % COVER)

    toc = innen.get_toc()
    erste_kapitelseite = next((e[2] for e in toc if e[0] == 1), None)

    ziel = fitz.open()
    ziel.insert_pdf(cover, from_page=0, to_page=0)   # U1
    ziel.insert_pdf(innen)                            # Innenteil
    ziel.insert_pdf(cover, from_page=1, to_page=1)   # U4

    # Lesezeichen: um die vorangestellte Titelseite verschieben, davor ein
    # Eintrag für den Umschlag und dahinter einer für die Rückseite.
    neu = [[1, "Titelseite", 1]]
    neu += [[e[0], e[1], e[2] + 1] for e in toc]
    neu += [[1, "Rückseite", ziel.page_count]]
    ziel.set_toc(neu)

    # Seitenlabels
    #   Seite 1                      Umschlag, ohne Nummer
    #   Titelei                      römisch, beginnt bei i
    #   ab der ersten Kapitelseite   arabisch, beginnt bei 1
    #   letzte Seite                 Umschlag, ohne Nummer
    labels = [{"startpage": 0, "prefix": "U", "style": "D", "firstpagenum": 1}]
    labels.append({"startpage": 1, "style": "r", "firstpagenum": 1})
    if erste_kapitelseite is not None:
        labels.append({"startpage": erste_kapitelseite, "style": "D", "firstpagenum": 1})
    labels.append({"startpage": ziel.page_count - 1, "prefix": "U", "style": "D",
                   "firstpagenum": 4})
    ziel.set_page_labels(labels)

    ziel.set_metadata({
        "title": innen.metadata.get("title", ""),
        "author": innen.metadata.get("author", ""),
        "subject": innen.metadata.get("subject", ""),
        "keywords": innen.metadata.get("keywords", ""),
        "producer": "Typst",
    })

    # Dokumentsprache und Leseansicht. `TwoPageRight` oeffnet die Datei als
    # Doppelseiten mit ungerader Seite rechts - so, wie das Buch aufgeschlagen
    # daliegt. `DisplayDocTitle` zeigt den Titel in der Fensterleiste statt
    # des Dateinamens.
    katalog = ziel.pdf_catalog()
    sprache = innen.xref_get_key(innen.pdf_catalog(), "Lang")
    if sprache[0] != "null":
        ziel.xref_set_key(katalog, "Lang", sprache[1])
    else:
        ziel.xref_set_key(katalog, "Lang", "(de-DE)")
    ziel.xref_set_key(katalog, "PageLayout", "/TwoPageRight")
    ziel.xref_set_key(katalog, "PageMode", "/UseOutlines")
    ziel.xref_set_key(katalog, "ViewerPreferences", "<< /DisplayDocTitle true >>")

    os.makedirs("build", exist_ok=True)
    ziel.save(ZIEL, garbage=4, deflate=True)

    print("geschrieben: %s" % ZIEL)
    print("  %d Seiten (1 Titelseite + %d Innenteil + 1 Rückseite)"
          % (ziel.page_count, innen.page_count))
    print("  %d Lesezeichen" % len(neu))
    print("  Seitenlabels: Umschlag ohne Nummer, Titelei römisch, "
          "Hauptteil arabisch ab PDF-Seite %s" % (erste_kapitelseite + 1))


main()
