# -*- coding: utf-8 -*-
"""Macht aus der gesetzten A5-Datei die Druckdatei fuer WirMachenDruck.

    python tools/druckdatei.py build/_satz-druck.pdf ../build/Druckversion/innenteil.pdf

Zwei Schritte:

1. Farbkonvertierung nach CMYK (Ghostscript). Notwendig, weil Abbildungen als
   RGB-Pixelbilder vorliegen und Typst sie nicht nach CMYK wandeln kann.
   Reine Graustufen bleiben Graustufen - im Vierfarbdruck ist das der
   K-Kanal, also genau das, was fuer Flieszttext gewuenscht ist.

2. Beschnitt anlegen: die Seitenflaeche waechst von 148 x 210 mm auf das
   Datenformat 154 x 216 mm. Die Seiten werden dabei nicht neu aufgebaut,
   sondern nur ihre Boxen verschoben - der gesetzte Inhalt behaelt seine
   Koordinaten und liegt zentriert, Lesezeichen und Querverweise bleiben
   erhalten.

   Das ist zulaessig, solange der Innenteil keine randabfallenden Objekte
   enthaelt: der zusaetzliche Rand ist dann Papierweisz. Andernfalls muss
   direkt im Datenformat gesetzt werden (siehe docs/ANLEITUNG.md).
"""
import os
import shutil
import subprocess
import sys

import fitz

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "tools"))
from farbprofil import ausgabebedingung_eintragen, profilpfad  # noqa: E402

MM = 72.0 / 25.4
ENDFORMAT = (148 * MM, 210 * MM)
DATENFORMAT = (154 * MM, 216 * MM)

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


def nach_cmyk(quelle, ziel):
    gs = finde_ghostscript()
    profil = profilpfad(BASIS)
    if gs is None:
        print("  Ghostscript nicht gefunden - Farbkonvertierung uebersprungen.")
        print("  Die Datei bleibt in RGB. Fuer den Druck Ghostscript installieren.")
        shutil.copyfile(quelle, ziel)
        return False
    befehl = [
        gs, "-dBATCH", "-dNOPAUSE", "-dQUIET", "-sDEVICE=pdfwrite",
        "-dProcessColorModel=/DeviceCMYK",
        "-sColorConversionStrategy=CMYK",
        "-dAutoFilterColorImages=false", "-dColorImageFilter=/FlateEncode",
        "-dAutoFilterGrayImages=false", "-dGrayImageFilter=/FlateEncode",
        # Gleiche Bilder nur einmal speichern und auf die von der Druckerei
        # geforderten 300 dpi begrenzen - darueber bringt Aufloesung nichts.
        "-dDetectDuplicateImages=true",
        "-dDownsampleColorImages=true", "-dColorImageResolution=300",
        "-dDownsampleGrayImages=true", "-dGrayImageResolution=300",
        "-dEmbedAllFonts=true", "-dSubsetFonts=true",
        "-dCompatibilityLevel=1.6",
    ]
    mit_profil = list(befehl)
    kopie = None
    if profil is not None:
        kopie = os.path.abspath(
            os.path.join(os.path.dirname(quelle) or ".", "_farbprofil.icc"))
        shutil.copyfile(profil, kopie)
        # Ghostscript laeuft seit 9.50 im SAFER-Mode und verweigert sonst das
        # Lesen des Profils - mit "Permission denied" und ohne brauchbare
        # Meldung. Die Erlaubnis muss vor der Eingabedatei stehen, aber hinter
        # dem Programmnamen.
        mit_profil.insert(1, "--permit-file-read=" + kopie)
        mit_profil += [
            # Zielprofil der Trennung. Ohne diese Angabe rechnet Ghostscript
            # mit seinem eingebauten Standard - das Petrol der Reihe faellt
            # dann anders aus als in der Ausgabebedingung der Druckerei.
            "-sOutputICCProfile=" + kopie,
            "-dRenderIntent=1",  # relativ farbmetrisch
            "-dBlackPtComp=1",
        ]
    else:
        print("  Farbprofil nicht gefunden - Trennung mit dem Ghostscript-Standard.")

    versuche = [(mit_profil, profil)] if profil is not None else []
    versuche.append((befehl, None))
    for argumente, verwendet in versuche:
        try:
            subprocess.check_call(argumente + ["-sOutputFile=" + ziel, quelle])
        except subprocess.CalledProcessError:
            if verwendet is None:
                raise
            print("  Ghostscript kam mit dem Farbprofil nicht zurecht - "
                  "Trennung mit dem eingebauten Standard.")
            continue
        print("  Farbkonvertierung nach CMYK: %s" % os.path.basename(gs))
        if verwendet is not None:
            print("  Zielprofil: %s" % os.path.basename(verwendet))
        break
    if kopie is not None and os.path.exists(kopie):
        os.remove(kopie)
    return True


def buchblock_schlieszen(pfad, teiler=4):
    """Haengt leere Seiten an, bis die Seitenzahl durch `teiler` teilbar ist.

    Ein Buchblock entsteht aus gefalzten Bogen - die Seitenzahl muss deshalb
    durch vier teilbar sein. Das Datenblatt zeigt auszerdem die letzte
    Inhaltsseite als linke Seite; auch das ist damit erfuellt. Die Seiten
    werden hier angehaengt und nicht im Satz erzeugt, weil eine im Satz
    berechnete Seitenzahl den Umbruch nicht konvergieren laesst.
    """
    d = fitz.open(pfad)
    fehlend = (-d.page_count) % teiler
    if fehlend:
        breite, hoehe = d[-1].rect.width, d[-1].rect.height
        for _ in range(fehlend):
            d.new_page(width=breite, height=hoehe)
        gesamt = d.page_count
        zwischen = pfad + ".vakat.tmp"
        d.save(zwischen, garbage=3, deflate=True)
        d.close()
        os.replace(zwischen, pfad)
        print("  Buchblock geschlossen: %d Vakatseite(n) angehaengt" % fehlend)
    else:
        gesamt = d.page_count
        d.close()
    print("  Umfang des Buchblocks: %d Seiten (durch %d teilbar)" % (gesamt, teiler))


def beschnitt_anlegen(pfad):
    dx = (DATENFORMAT[0] - ENDFORMAT[0]) / 2
    dy = (DATENFORMAT[1] - ENDFORMAT[1]) / 2
    d = fitz.open(pfad)
    media = "[%g %g %g %g]" % (-dx, -dy, ENDFORMAT[0] + dx, ENDFORMAT[1] + dy)
    trim = "[0 0 %g %g]" % ENDFORMAT
    for seite in d:
        d.xref_set_key(seite.xref, "MediaBox", media)
        d.xref_set_key(seite.xref, "CropBox", media)
        d.xref_set_key(seite.xref, "BleedBox", media)
        d.xref_set_key(seite.xref, "TrimBox", trim)
    # Vollstaendig neu schreiben statt inkrementell anzuhaengen: Ghostscript
    # legt komprimierte Querverweistabellen an, und ein inkrementeller Anhang
    # darauf kann die Datei unbrauchbar machen - sie endet dann mitten im
    # Datenstrom, ohne dass ein Fehler gemeldet wird.
    lesezeichen = len(d.get_toc())
    zwischen = pfad + ".tmp"
    d.save(zwischen, garbage=3, deflate=True)
    d.close()
    os.replace(zwischen, pfad)

    # Gegenprobe: die Datei muss danach lesbar sein und Seiten enthalten.
    kontrolle = fitz.open(pfad)
    if kontrolle.page_count == 0:
        kontrolle.close()
        raise SystemExit("Die Druckdatei %s enthaelt keine Seiten." % pfad)
    kontrolle.close()
    print("  Beschnitt angelegt: 154 x 216 mm, TrimBox 148 x 210 mm")
    print("  Lesezeichen erhalten: %d" % lesezeichen)


def main():
    quelle, ziel = sys.argv[1], sys.argv[2]
    print("Druckdatei erzeugen aus %s" % quelle)
    nach_cmyk(quelle, ziel)
    buchblock_schlieszen(ziel)
    beschnitt_anlegen(ziel)
    ausgabebedingung_eintragen(ziel)
    print("  geschrieben: %s" % ziel)


main()
