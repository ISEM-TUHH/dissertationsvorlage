# -*- coding: utf-8 -*-
"""Prueft die erzeugten PDF gegen die Vorgaben von WirMachenDruck.

    python tools/pruefen.py

Grundlage ist das Datenblatt "Buch DIN A5, mit geradem Buchruecken,
Inhaltsseiten 4/4-farbig" (buecher_mit_hardcover_dina5_hoch_44_1.pdf):

    Datenformat        154 x 216 mm  (3 mm Beschnitt umlaufend)
    Endformat          148 x 210 mm
    Sicherheitsabstand 5 mm ab Endformat
    Falzkante          ca. 7 mm am Bund der ersten und letzten Blaetter
    Farbmodus          CMYK
    Aufloesung         mindestens 300 dpi
    Dateiformat        PDF, Schriften eingebettet, Transparenzen reduziert
"""
import os
import sys
import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), "inhalt"))

MM = 72.0 / 25.4
ENDFORMAT = (148.0, 210.0)
DATENFORMAT = (154.0, 216.0)
SICHERHEIT = 5.0
FALZKANTE = 7.0      # Bundzugabe der ersten und letzten Blaetter
MINDEST_DPI = 300.0

# farbprofil.py liegt in template/tools, dieses Skript in
# template/innenteil/tools - der Pfad wird von der Datei aus aufgeloest,
# damit das Arbeitsverzeichnis (inhalt/) keine Rolle spielt.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "tools"))
try:
    from farbprofil import hat_outputintent
except ImportError:
    hat_outputintent = None

ok_gesamt = True


def _streams(d, seite, gesehen):
    """Contentstream der Seite und aller darin aufgerufenen Form-XObjects.

    Nach dem Anlegen des Beschnitts liegt der eigentliche Satz in einem
    Form-XObject; wer nur den Seitenstream liest, sieht dort keine Farben.
    """
    yield seite.read_contents()
    for eintrag in d.get_page_xobjects(seite.number):
        xref = eintrag[0]
        if xref in gesehen:
            continue
        gesehen.add(xref)
        try:
            if d.xref_get_key(xref, "Subtype")[1] == "/Form":
                yield d.xref_stream(xref)
        except Exception:
            continue


def farboperatoren(d):
    ops = {}
    gesehen = set()
    for seite in d:
        for stream in _streams(d, seite, gesehen):
            if not stream:
                continue
            for tok in stream.split():
                t = tok.decode("latin-1")
                if t in ("k", "K", "rg", "RG", "g", "G", "sc", "scn", "SC", "SCN"):
                    ops[t] = ops.get(t, 0) + 1
    return ops


def bildfarbraeume(d):
    raeume = set()
    for seite in d:
        for bild in seite.get_images(full=True):
            info = d.extract_image(bild[0])
            raeume.add(info.get("colorspace", 0))
    # PyMuPDF: 1 = Gray, 3 = RGB, 4 = CMYK
    namen = {1: "Grau", 3: "RGB", 4: "CMYK"}
    return {namen.get(r, str(r)) for r in raeume}


def schriften(d):
    alle = {}
    for seite in d:
        for f in seite.get_fonts(full=True):
            alle[f[3]] = f[1] != "n/a"
    return alle


def satzspiegel_pruefen(d, seitenformat):
    """Kleinster Abstand vom Endformat zu bedruckter Flaeche."""
    dx = (seitenformat[0] - ENDFORMAT[0]) / 2
    dy = (seitenformat[1] - ENDFORMAT[1]) / 2
    trim = fitz.Rect(dx * MM, dy * MM,
                     (dx + ENDFORMAT[0]) * MM, (dy + ENDFORMAT[1]) * MM)
    kleinster = None
    schlimmste = None
    for seite in d:
        inhalt = None
        for block in seite.get_text("blocks"):
            r = fitz.Rect(block[:4])
            inhalt = r if inhalt is None else (inhalt | r)
        for bild in seite.get_image_info():
            r = fitz.Rect(bild["bbox"])
            inhalt = r if inhalt is None else (inhalt | r)
        if inhalt is None:
            continue
        abstand = min(inhalt.x0 - trim.x0, trim.x1 - inhalt.x1,
                      inhalt.y0 - trim.y0, trim.y1 - inhalt.y1) / MM
        if kleinster is None or abstand < kleinster:
            kleinster, schlimmste = abstand, seite.number + 1
    return kleinster, schlimmste


def falzkante_pruefen(d, seitenformat):
    """Abstand zum Bund auf den ersten und letzten beiden Blaettern.

    Das erste und das letzte Blatt werden beim Hardcover in den Falz
    geklebt; laut Datenblatt sind dort rund 7 mm am Bund nicht sichtbar.
    Rechte (ungerade) Seiten haben den Bund links, linke Seiten rechts.
    """
    dx = (seitenformat[0] - ENDFORMAT[0]) / 2
    dy = (seitenformat[1] - ENDFORMAT[1]) / 2
    trim = fitz.Rect(dx * MM, dy * MM,
                     (dx + ENDFORMAT[0]) * MM, (dy + ENDFORMAT[1]) * MM)
    betroffen = [0, 1, d.page_count - 2, d.page_count - 1]
    kleinster, schlimmste = None, None
    for nr in betroffen:
        if nr < 0 or nr >= d.page_count:
            continue
        seite = d[nr]
        inhalt = None
        for block in seite.get_text("blocks"):
            r = fitz.Rect(block[:4])
            inhalt = r if inhalt is None else (inhalt | r)
        for bild in seite.get_image_info():
            r = fitz.Rect(bild["bbox"])
            inhalt = r if inhalt is None else (inhalt | r)
        if inhalt is None:
            continue
        # Seite 1 ist eine rechte Seite: Bund links.
        bund_links = (nr % 2) == 0
        abstand = (inhalt.x0 - trim.x0 if bund_links else trim.x1 - inhalt.x1) / MM
        if kleinster is None or abstand < kleinster:
            kleinster, schlimmste = abstand, nr + 1
    return kleinster, schlimmste


def bildaufloesung(d):
    """Kleinste effektive Aufloesung eines platzierten Bildes in dpi."""
    kleinste, seite_nr = None, None
    for seite in d:
        for info in seite.get_image_info(xrefs=True):
            r = fitz.Rect(info["bbox"])
            if r.width <= 0 or r.height <= 0:
                continue
            dpi_x = info["width"] / (r.width / 72.0)
            dpi_y = info["height"] / (r.height / 72.0)
            dpi = min(dpi_x, dpi_y)
            if kleinste is None or dpi < kleinste:
                kleinste, seite_nr = dpi, seite.number + 1
    return kleinste, seite_nr


def nicht_cmyk_farbraeume(d):
    """Seiten mit Farbraeumen, die nicht DeviceCMYK sind."""
    import re
    treffer = []
    for seite in d:
        eintrag = d.xref_get_key(seite.xref, "Resources/ColorSpace")
        if eintrag[0] != "dict":
            continue
        for name, ref in re.findall(r"/(\w+)\s(\d+) 0 R", eintrag[1]):
            objekt = d.xref_object(int(ref))
            m = re.search(r"/ICCBased (\d+) 0 R", objekt)
            if m and d.xref_get_key(int(m.group(1)), "N")[1] != "4":
                treffer.append(seite.number + 1)
                break
    return sorted(set(treffer))


def vierfarbiges_schwarz(d):
    """Seiten, auf denen Schwarz nicht als reines K gesetzt ist.

    Im Buchsatz gehoeren Text und feine Linien in den K-Kanal. Vierfarbiges
    Schwarz zeigt bei der geringsten Passerdifferenz farbige Raender.
    """
    treffer = []
    for seite in d:
        toks = [t.decode("latin-1") for t in seite.read_contents().split()]
        for i, t in enumerate(toks):
            if t not in ("k", "K") or i < 4:
                continue
            try:
                c, m, y, kk = (float(x) for x in toks[i - 4:i])
            except ValueError:
                continue
            if kk > 0.5 and (c > 0.05 or m > 0.05 or y > 0.05):
                treffer.append(seite.number + 1)
                break
    return sorted(set(treffer))


def pruefe(pfad, art):
    """art: 'druck' oder 'online'."""
    global ok_gesamt
    if not os.path.exists(pfad):
        print("\n=== %s === fehlt" % pfad)
        ok_gesamt = False
        return
    d = fitz.open(pfad)
    soll = DATENFORMAT if art == "druck" else ENDFORMAT
    print("\n=== %s  (%d Seiten) ===" % (pfad, d.page_count))
    ok = True

    formate = {(round(p.rect.width / MM, 1), round(p.rect.height / MM, 1)) for p in d}
    for fmt in sorted(formate):
        gut = abs(fmt[0] - soll[0]) <= 0.1 and abs(fmt[1] - soll[1]) <= 0.1
        ok = ok and gut
        print("  [%s] Seitenformat %.1f x %.1f mm  (soll %.1f x %.1f mm)"
              % ("OK" if gut else "!!", fmt[0], fmt[1], soll[0], soll[1]))

    if art == "druck":
        tb = d.xref_get_key(d[0].xref, "TrimBox")[1]
        vorhanden = tb not in ("null", None)
        ok = ok and vorhanden
        print("  [%s] TrimBox %s" % ("OK" if vorhanden else "!!", tb))
        print("       Beschnitt 3 mm umlaufend (Datenformat minus Endformat)")

    abstand, seite = satzspiegel_pruefen(d, soll)
    if abstand is not None:
        gut = abstand >= SICHERHEIT  # keine Toleranz - 5 mm sind das Minimum
        ok = ok and gut
        print("  [%s] geringster Abstand zum Endformat %.1f mm auf Seite %d  (soll >= %.0f mm)"
              % ("OK" if gut else "!!", abstand, seite, SICHERHEIT))

    falz, falzseite = falzkante_pruefen(d, soll)
    if falz is not None:
        gut = falz >= FALZKANTE
        ok = ok and gut
        print("  [%s] Bundabstand auf den ersten/letzten Blaettern %.1f mm auf Seite %d  (soll >= %.0f mm Falzkante)"
              % ("OK" if gut else "!!", falz, falzseite, FALZKANTE))

    dpi, dpiseite = bildaufloesung(d)
    if dpi is not None:
        # Das Datenblatt sagt "sollte mindestens 300 dpi betragen" - das ist
        # eine Empfehlung zur Bildqualitaet, kein Formatfehler. Deshalb ein
        # Hinweis; welche Seiten betroffen sind, sagt umbruch_pruefen.py.
        gut = dpi >= MINDEST_DPI - 1
        print("  [%s] kleinste Bildaufloesung %.0f dpi auf Seite %d  (soll >= %.0f dpi)"
              % ("OK" if gut else " ?", dpi, dpiseite, MINDEST_DPI))

    if art == "druck":
        gerade = d.page_count % 2 == 0
        vierer = d.page_count % 4 == 0
        ok = ok and gerade
        print("  [%s] Seitenzahl gerade (%d) - die letzte Inhaltsseite ist eine linke Seite"
              % ("OK" if gerade else "!!", d.page_count))
        print("  [%s] Seitenzahl durch 4 teilbar (%d)  (Bogenteilung)"
              % ("OK" if vierer else " ?", d.page_count))

    f = farboperatoren(d)
    cmyk = f.get("k", 0) + f.get("K", 0)
    rgb = f.get("rg", 0) + f.get("RG", 0)
    grau = f.get("g", 0) + f.get("G", 0)
    print("  Farboperatoren  CMYK %d, RGB %d, Grau %d, benannt %d"
          % (cmyk, rgb, grau, sum(f.get(x, 0) for x in ("sc", "scn", "SC", "SCN"))))
    bilder = bildfarbraeume(d)
    print("  Bildfarbraeume  %s" % (", ".join(sorted(bilder)) if bilder else "keine Bilder"))
    if art == "druck":
        if rgb:
            print("    !! Druckdatei enthaelt RGB-Farboperatoren")
            ok = False
        if "RGB" in bilder:
            print("    !! Druckdatei enthaelt RGB-Bilder")
            ok = False

    fehlend = [n for n, e in schriften(d).items() if not e]
    print("  Schriften       %d, alle eingebettet: %s"
          % (len(schriften(d)), "ja" if not fehlend else "NEIN: " + ", ".join(fehlend)))
    if fehlend:
        ok = False

    toc = d.get_toc()
    tiefe = max([e[0] for e in toc], default=0)
    gut = len(toc) > 0 and tiefe <= 3
    ok = ok and gut
    print("  [%s] Lesezeichen     %d Eintraege, tiefste Ebene %d  (soll <= 3)"
          % ("OK" if gut else "!!", len(toc), tiefe))

    if art == "druck":
        fremd = nicht_cmyk_farbraeume(d)
        gut = not fremd
        ok = ok and gut
        print("  [%s] alle Farben in DeviceCMYK%s"
              % ("OK" if gut else "!!",
                 "" if gut else " - nicht auf Seite " + ", ".join(map(str, fremd[:8]))))

        reich = vierfarbiges_schwarz(d)
        gut = not reich
        ok = ok and gut
        print("  [%s] Schwarz steht im K-Kanal%s"
              % ("OK" if gut else "!!",
                 "" if gut else " - vierfarbig auf Seite " + ", ".join(map(str, reich[:8]))
                 + " (im Satz `schwarz` statt `black` verwenden)"))

    if art == "druck" and hat_outputintent is not None:
        d.close()
        vorhanden = hat_outputintent(pfad)
        d = fitz.open(pfad)
        ok = ok and vorhanden
        print("  [%s] Ausgabebedingung ISO Coated v2 300%% (ECI) eingebettet"
              % ("OK" if vorhanden else "!!"))

    if art == "druck":
        # Kapitel und Verzeichnisse muessen auf einer rechten Seite beginnen.
        dx = (DATENFORMAT[0] - ENDFORMAT[0]) / 2 * MM
        dy = (DATENFORMAT[1] - ENDFORMAT[1]) / 2 * MM
        links = [e for e in toc if e[0] == 1 and e[2] % 2 == 0]
        gut = len(links) == 0
        ok = ok and gut
        print("  [%s] Kapitelanfaenge auf rechter Seite: %s"
              % ("OK" if gut else "!!",
                 "alle" if gut else "links beginnen " + ", ".join(
                     "%s (S. %d)" % (e[1], e[2]) for e in links)))

    ok_gesamt = ok_gesamt and ok


def pruefe_archiv(pfad):
    """Die Archivfassung fuer TORE und DNB: PDF/A-2b und PDF/UA-1.

    Diese Datei darf nach dem Satz nicht mehr nachbearbeitet werden - jede
    Nachbearbeitung kann die Konformitaet brechen, ohne dass die Datei es
    noch merkt. Deshalb kommt sie direkt aus Typst.
    """
    global ok_gesamt
    if not os.path.exists(pfad):
        print("\n=== %s === fehlt" % pfad)
        ok_gesamt = False
        return
    d = fitz.open(pfad)
    print("\n=== %s  (%d Seiten) ===" % (pfad, d.page_count))
    katalog = d.pdf_catalog()
    ok = True
    for schluessel, name in (
        ("Lang", "Dokumentsprache"),
        ("MarkInfo", "als getaggt gekennzeichnet"),
        ("StructTreeRoot", "Strukturbaum (Screenreader)"),
        ("OutputIntents", "Ausgabebedingung"),
        ("Metadata", "XMP-Metadaten"),
    ):
        vorhanden = d.xref_get_key(katalog, schluessel)[0] != "null"
        ok = ok and vorhanden
        print("  [%s] %s" % ("OK" if vorhanden else "!!", name))

    xmp = d.xref_get_key(katalog, "Metadata")
    inhalt = ""
    if xmp[0] == "xref":
        try:
            inhalt = d.xref_stream(int(xmp[1].split()[0])).decode("utf-8", "ignore")
        except Exception:
            inhalt = ""
    for muster, name in (("pdfaid", "PDF/A-2b ausgewiesen"),
                         ("pdfuaid", "PDF/UA-1 ausgewiesen")):
        gut = muster in inhalt
        ok = ok and gut
        print("  [%s] %s" % ("OK" if gut else "!!", name))

    fehlend = [n for n, e in schriften(d).items() if not e]
    print("  Schriften       %d, alle eingebettet: %s"
          % (len(schriften(d)), "ja" if not fehlend else "NEIN"))
    ok = ok and not fehlend
    ok_gesamt = ok_gesamt and ok


pruefe("../build/Druckversion/innenteil.pdf", "druck")
pruefe("../build/Onlineversion/innenteil.pdf", "online")
pruefe_archiv("../build/Archivversion/innenteil.pdf")
print("\nErgebnis:", "alles in Ordnung" if ok_gesamt else "Abweichungen gefunden")
sys.exit(0 if ok_gesamt else 1)
