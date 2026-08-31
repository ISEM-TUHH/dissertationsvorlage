#!/usr/bin/env bash
# Baut alles: Umschlag, Innenteil und die Online-Gesamtdatei.
#     ./bauen.sh
#
# Diese Datei ist nur der Einstieg. Die eigentliche Baulogik liegt in
# template/bauen.sh und wird mit der Vorlage aktualisiert.
#
# Unter Windows: .\bauen.ps1

set -euo pipefail
exec "$(dirname "$0")/template/bauen.sh"
