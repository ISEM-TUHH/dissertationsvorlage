# Baut alles: Umschlag, Innenteil und die Online-Gesamtdatei.
#     .\bauen.ps1
#
# Diese Datei ist nur der Einstieg. Die eigentliche Baulogik liegt in
# template\bauen.ps1 und wird mit der Vorlage aktualisiert - so bekommst du
# Verbesserungen am Bau mit jedem "git merge vorlage/main" von selbst.
#
# Unter macOS und Linux: ./bauen.sh

$ErrorActionPreference = "Stop"
& "$PSScriptRoot\template\bauen.ps1"
