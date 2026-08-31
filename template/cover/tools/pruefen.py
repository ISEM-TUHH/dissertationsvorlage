# -*- coding: utf-8 -*-
"""Prueft die erzeugten PDF gegen die Vorgaben.

    python tools/pruefen.py                      alles pruefen
    python tools/pruefen.py ../build/Druckversion/umschlag.pdf 204
"""
import os
import sys
import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)

BLATTDICKE, PAPPE = 0.104, 2.2
ok_gesamt = True


def farboperatoren(d):
    ops = {}
    for seite in d:
        for tok in seite.read_contents().split():
            t = tok.decode("latin-1")
            if t in ("k", "K", "rg", "RG", "g", "G", "sc", "scn", "SC", "SCN"):
                ops[t] = ops.get(t, 0) + 1
    return {
        "cmyk": ops.get("k", 0) + ops.get("K", 0),
        "rgb": ops.get("rg", 0) + ops.get("RG", 0),
        "gray": ops.get("g", 0) + ops.get("G", 0),
        "andere": sum(ops.get(x, 0) for x in ("sc", "scn", "SC", "SCN")),
    }


def farbraeume(d):
    """Welche Farbraeume deklariert das PDF? Typst schreibt RGB als ICCBased
    (sRGB) und spricht es mit scn an, CMYK dagegen direkt mit k/K."""
    gefunden = set()
    for xref in range(1, d.xref_length()):
        try:
            obj = d.xref_object(xref, compressed=True)
        except Exception:
            continue
        for name in ("DeviceCMYK", "DeviceRGB", "DeviceGray", "ICCBased",
                     "CalRGB", "Separation", "Lab"):
            if "/" + name in obj:
                gefunden.add(name)
    return gefunden


def gemeinsam(d, erwartet):
    """Schriften, Pixelbilder, Farbraum. erwartet: 'cmyk' oder 'rgb'."""
    global ok_gesamt
    ok = True
    f = farboperatoren(d)
    cs = farbraeume(d)
    print("  Operatoren CMYK %-4d RGB %-4d Grau %-4d benannt %d"
          % (f["cmyk"], f["rgb"], f["gray"], f["andere"]))
    print("  Farbraeume %s" % (", ".join(sorted(cs)) if cs else "keine deklariert"))

    if erwartet == "cmyk":
        # Reine Druckdatei: alle Farben ueber k/K, keine RGB- oder Grauwerte
        # und kein RGB-Farbraum im Dokument.
        if f["rgb"] or f["gray"] or f["andere"]:
            print("    !! Druckdatei enthaelt Nicht-CMYK-Farboperatoren")
            ok = False
        if cs & {"DeviceRGB", "ICCBased", "CalRGB", "DeviceGray"}:
            print("    !! Druckdatei deklariert einen RGB-/Graufarbraum")
            ok = False
        if not f["cmyk"]:
            print("    !! keine CMYK-Farben gefunden")
            ok = False
    else:
        # Bildschirmfassung: RGB, entweder DeviceRGB oder ICCBased (sRGB).
        if f["cmyk"] or "DeviceCMYK" in cs:
            print("    !! Bildschirmfassung enthaelt CMYK")
            ok = False
        if not (f["rgb"] or f["andere"]):
            print("    !! keine RGB-Farben gefunden")
            ok = False

    for fo in d[0].get_fonts(full=True):
        eingebettet = fo[1] != "n/a"
        print("  Schrift    %-24s %-8s %s"
              % (fo[3], fo[2], "eingebettet" if eingebettet else "NICHT EINGEBETTET"))
        if not eingebettet:
            ok = False

    bilder = sum(len(p.get_images(full=True)) for p in d)
    print("  Pixelbilder %d %s" % (bilder, "(alles Vektor)" if not bilder else "<-- pruefen"))
    if bilder:
        ok = False
    ok_gesamt = ok_gesamt and ok
    return ok


def pruefe_umschlag(pfad, seiten):
    global ok_gesamt
    d = fitz.open(pfad)
    p = d[0]
    mm = lambda v: v / 72 * 25.4
    W, H = mm(p.rect.width), mm(p.rect.height)
    B = seiten / 2 * BLATTDICKE + 2 * PAPPE
    print("\n=== %s  (%d Seiten Buchblock) ===" % (pfad, seiten))
    ok = True
    for name, ist, soll in (
        ("Datenformat Breite", W, 336 + B),
        ("Datenformat Hoehe", H, 245.0),
        ("Endformat Breite", W - 30, 306 + B),
        ("Endformat Hoehe", H - 30, 215.0),
    ):
        gut = abs(ist - soll) <= 0.05
        ok = ok and gut
        print("  [%s] %-20s %8.2f mm  (soll %.2f mm)"
              % ("OK" if gut else "!!", name, ist, soll))
    print("  Bundstaerke              %8.2f mm  (Beschnitt 15 mm, Sicherheit 5 mm, Falz 7 mm)" % B)
    ok_gesamt = ok_gesamt and ok
    gemeinsam(d, "cmyk")


def pruefe_bildschirm(pfad):
    global ok_gesamt
    d = fitz.open(pfad)
    mm = lambda v: v / 72 * 25.4
    print("\n=== %s ===" % pfad)
    ok = d.page_count == 2
    print("  [%s] Seitenzahl %d (soll 2: Titelseite, Rueckseite)"
          % ("OK" if ok else "!!", d.page_count))
    for i, p in enumerate(d):
        print("       Seite %d  %.1f x %.1f mm" % (i + 1, mm(p.rect.width), mm(p.rect.height)))
    ok_gesamt = ok_gesamt and ok
    gemeinsam(d, "rgb")


def main():
    if len(sys.argv) > 1:
        pfad = sys.argv[1]
        if "bildschirm" in pfad:
            pruefe_bildschirm(pfad)
        else:
            pruefe_umschlag(pfad, int(sys.argv[2]) if len(sys.argv) > 2 else 204)
    else:
        os.chdir(BASIS)
        import re
        _inhalt = "../../inhalt" if os.path.isdir("../../inhalt") else "../../inhalt-vorlage"
        quelle = open(_inhalt + "/buchdaten.typ", encoding="utf-8").read()
        seiten = int(re.search(r"seiten:\s*(\d+)", quelle).group(1))
        pruefe_umschlag("../../build/Druckversion/umschlag.pdf", seiten)
        pruefe_bildschirm("../../build/Onlineversion/umschlag.pdf")
    print("\nErgebnis:", "alles in Ordnung" if ok_gesamt else "Abweichungen gefunden")
    sys.exit(0 if ok_gesamt else 1)


main()
