# -*- coding: utf-8 -*-
"""Traegt die Ausgabebedingung in die Umschlag-Druckdatei ein.

    python tools/ausgabebedingung.py ../build/Druckversion/umschlag.pdf

Der Umschlag wird von Typst bereits in CMYK gesetzt; umgerechnet werden muss
also nichts. Was fehlt, ist die Angabe, fuer welche Druckbedingung diese
CMYK-Werte gelten - genau das traegt dieses Skript nach.
"""
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, os.path.join(WURZEL, "tools"))

from farbprofil import ausgabebedingung_eintragen  # noqa: E402

ziel = sys.argv[1] if len(sys.argv) > 1 else "../build/Druckversion/umschlag.pdf"
if not os.path.exists(ziel):
    raise SystemExit("Datei nicht gefunden: %s" % ziel)
ausgabebedingung_eintragen(ziel)
