#!/usr/bin/env bash
# Baut alles: Umschlag, Innenteil und die Online-Gesamtdatei (macOS/Linux).
# Aufruf aus dem Wurzelordner:
#     ./template/bauen.sh
#
# Ergebnisse: siehe bauen.ps1 - beide Skripte tun dasselbe.

set -euo pipefail
hier="$(cd "$(dirname "$0")" && pwd)"
wurzel="$(dirname "$hier")"
py="$(command -v python3 || command -v python)"

echo ""
echo "=== Umschlag ============================================"
"$hier/cover/bauen.sh"

echo ""
echo "=== Innenteil ==========================================="
"$hier/innenteil/bauen.sh"

echo ""
echo "=== Umfang abgleichen ==================================="
cd "$wurzel"
# Eine Abweichung ist hier eine Warnung, kein Abbruchgrund: solange der
# Innenteil noch waechst, stimmt die Seitenzahl im Cover naturgemaess nicht.
"$py" template/tools/umfang_pruefen.py || true

echo ""
echo "=== Gesamtdatei fuer online ============================="
"$py" template/tools/gesamt.py

echo ""
echo "Fertig."
