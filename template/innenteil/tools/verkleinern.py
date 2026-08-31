# -*- coding: utf-8 -*-
"""Verkleinert die Onlinefassung, ohne die Druckqualität zu unterschreiten.

    python tools/verkleinern.py ../build/Onlineversion/innenteil.pdf

Wozu
----
Jede eingebettete Abbildung bringt ihre eigenen Bilddaten mit. Bei einer
Arbeit mit hundert Abbildungen summiert sich das auf ein Vielfaches dessen,
was nötig wäre: gleiche Bilder liegen mehrfach im Dokument, und die
Auflösung ist höher als der Druck verlangt.

Ghostscript räumt beides auf - doppelte Bilder werden einmal gespeichert,
die Auflösung auf 300 dpi begrenzt. 300 dpi ist die Vorgabe der Druckerei;
darunter geht es nicht, darüber bringt es nichts.

Schriften bleiben vollständig eingebettet, Vektoren bleiben Vektoren.
"""
import os
import shutil
import subprocess
import sys

import fitz

GS_KANDIDATEN = [
    "gswin64c", "gswin32c", "gs",
    r"C:\Program Files\gs\gs10.07.1\bin\gswin64c.exe",
]


def finde_ghostscript():
    for k in GS_KANDIDATEN:
        p = shutil.which(k) if os.sep not in k else (k if os.path.exists(k) else None)
        if p:
            return p
    return None


def main():
    pfad = sys.argv[1] if len(sys.argv) > 1 else "../build/Onlineversion/innenteil.pdf"
    if not os.path.exists(pfad):
        sys.exit("fehlt: " + pfad)

    vorher = os.path.getsize(pfad)
    gs = finde_ghostscript()
    if gs is None:
        print("Ghostscript nicht gefunden - Datei bleibt unverändert (%.1f MB)."
              % (vorher / 1048576))
        return

    # Ghostscript wirft die Seitenlabels (römisch/arabisch) weg - vorher
    # sichern, hinterher zurückschreiben. Die Labels müssen 1:1 dem
    # Aufdruck entsprechen.
    d = fitz.open(pfad)
    labels = d.get_page_labels()
    d.close()
    # PyMuPDF liest aus Typst-Dateien faelschlich "/Type /PageLabel" als
    # Praefix "ageLabel" - das ist keines.
    for l in labels:
        if l.get("prefix") == "ageLabel":
            l["prefix"] = ""

    ziel = pfad + ".tmp"
    subprocess.check_call([
        gs, "-dBATCH", "-dNOPAUSE", "-dQUIET", "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.7",
        "-dDetectDuplicateImages=true",
        "-dDownsampleColorImages=true", "-dColorImageResolution=300",
        "-dDownsampleGrayImages=true", "-dGrayImageResolution=300",
        "-dDownsampleMonoImages=true", "-dMonoImageResolution=600",
        "-dEmbedAllFonts=true", "-dSubsetFonts=true",
        "-sOutputFile=" + ziel, pfad,
    ])
    nachher = os.path.getsize(ziel)

    # Nur übernehmen, wenn es wirklich kleiner geworden ist.
    if nachher < vorher:
        os.replace(ziel, pfad)
        print("verkleinert: %.1f MB -> %.1f MB (%.0f %% gespart)"
              % (vorher / 1048576, nachher / 1048576,
                 100 * (1 - nachher / vorher)))
    else:
        os.remove(ziel)
        print("keine Verkleinerung möglich, Datei bleibt bei %.1f MB"
              % (vorher / 1048576))

    # Seitenlabels zurückschreiben und die Lesezeichen beim Öffnen anzeigen.
    d = fitz.open(pfad)
    if labels:
        d.set_page_labels(labels)
    d.set_pagemode("UseOutlines")
    d.save(pfad, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    d.close()


main()
