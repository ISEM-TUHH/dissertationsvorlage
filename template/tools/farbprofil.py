# -*- coding: utf-8 -*-
"""Ausgabebedingung (OutputIntent) in eine Druckdatei eintragen.

Die Druckerei erwartet CMYK-Daten. Zahlenwerte allein sagen aber nicht, wie
sie auf Papier aussehen - dazu gehoert die Ausgabebedingung. Fuer den
europaeischen Bogenoffset und fuer den Digitaldruck von WirMachenDruck ist
das ISO Coated v2 300 % (ECI). Das Profil wird in die Datei eingebettet und
im Katalog als /OutputIntents eingetragen, so wie es PDF/X verlangt.

Ohne diesen Eintrag rechnet jede Vorstufe mit ihrer eigenen Annahme - und
das Petrol der Reihe kann dann anders herauskommen als gedacht.
"""
import os

import fitz

PROFIL_DATEI = "ISOcoated_v2_300_eci.icc"
BEDINGUNG = "ISO Coated v2 300% (ECI)"
REGISTRIERUNG = "http://www.color.org"


def profilpfad(start=None):
    """Sucht das ICC-Profil vom angegebenen Ordner aus nach oben.

    Das Profil liegt bei der Vorlage in template/ - deshalb wird auf jeder
    Ebene auch der Unterordner template/ mit angesehen. Zuerst kommt aber
    der Ordner dieses Skripts selbst an die Reihe, denn farbprofil.py liegt
    im selben template/tools-Baum wie das Profil.
    """
    kandidaten = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
    ordner = os.path.abspath(start or os.getcwd())
    for _ in range(5):
        kandidaten.append(ordner)
        eltern = os.path.dirname(ordner)
        if eltern == ordner:
            break
        ordner = eltern
    for basis in kandidaten:
        for kandidat in (os.path.join(basis, PROFIL_DATEI),
                         os.path.join(basis, "template", PROFIL_DATEI)):
            if os.path.exists(kandidat):
                return kandidat
    return None


def lesezeichen_anzeigen(pfad, layout=None):
    """Oeffnet der Reader die Datei, zeigt er die Lesezeichen an
    (/PageMode /UseOutlines). layout setzt zusaetzlich die Seitenansicht:
    "OneColumn" = einseitig fortlaufend (Onlinefassung ohne Vakatseiten),
    "TwoPageRight" = Doppelseiten mit rechter Erstseite (Druckkontrolle).
    """
    d = fitz.open(pfad)
    try:
        d.set_pagemode("UseOutlines")
        if layout:
            d.set_pagelayout(layout)
        d.saveIncr()
    finally:
        d.close()


def hat_outputintent(pfad):
    d = fitz.open(pfad)
    try:
        eintrag = d.xref_get_key(d.pdf_catalog(), "OutputIntents")[1]
        return eintrag not in (None, "null")
    finally:
        d.close()


def ausgabebedingung_eintragen(pfad, profil=None):
    """Traegt ISO Coated v2 300 % (ECI) als Ausgabebedingung ein.

    Gibt True zurueck, wenn das Profil eingebettet wurde.
    """
    profil = profil or profilpfad(os.path.dirname(os.path.abspath(pfad)))
    if profil is None:
        print("  Farbprofil %s nicht gefunden - keine Ausgabebedingung eingetragen."
              % PROFIL_DATEI)
        return False

    with open(profil, "rb") as f:
        icc = f.read()

    d = fitz.open(pfad)
    try:
        icc_xref = d.get_new_xref()
        # N = 4 Farbkanaele; das Profil selbst liegt im Datenstrom.
        d.update_object(icc_xref, "<< /N 4 >>")
        d.update_stream(icc_xref, icc, compress=True)

        oi_xref = d.get_new_xref()
        d.update_object(oi_xref, (
            "<< /Type /OutputIntent /S /GTS_PDFX "
            "/OutputConditionIdentifier (%s) /OutputCondition (%s) /Info (%s) "
            "/RegistryName (%s) /DestOutputProfile %d 0 R >>"
        ) % (BEDINGUNG, BEDINGUNG, BEDINGUNG, REGISTRIERUNG, icc_xref))

        d.xref_set_key(d.pdf_catalog(), "OutputIntents", "[ %d 0 R ]" % oi_xref)

        zwischen = pfad + ".oi.tmp"
        d.save(zwischen, garbage=3, deflate=True)
    finally:
        d.close()
    os.replace(zwischen, pfad)
    print("  Ausgabebedingung eingetragen: %s (%.1f MB Profil eingebettet)"
          % (BEDINGUNG, len(icc) / 1e6))
    return True
