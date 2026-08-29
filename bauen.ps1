# Baut alles: Umschlag, Innenteil und die Online-Gesamtdatei.
#     .\bauen.ps1
#
# Ergebnisse
#   Cover\build\umschlag.pdf              Druckdatei Umschlag (CMYK, Beschnitt)
#   Cover\build\umschlag-kontrolle.pdf    dieselbe mit Hilfslinien, nur zur Ansicht
#   Innenteil\build\innenteil-druck.pdf   Druckdatei Innenteil (CMYK, Beschnitt)
#   Innenteil\build\innenteil-online.pdf  Innenteil zum Lesen am Bildschirm
#   build\dissertation-online.pdf         alles in einer Datei, zum Lesen und Verschicken

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "`n=== Umschlag ============================================" -ForegroundColor Cyan
& "$PSScriptRoot\Cover\bauen.ps1"

Write-Host "`n=== Innenteil ===========================================" -ForegroundColor Cyan
& "$PSScriptRoot\Innenteil\bauen.ps1"

Write-Host "`n=== Umfang abgleichen ===================================" -ForegroundColor Cyan
Set-Location $PSScriptRoot
# Eine Abweichung ist hier eine Warnung, kein Abbruchgrund: solange der
# Innenteil noch waechst, stimmt die Seitenzahl im Cover naturgemaess nicht.
$alt = $ErrorActionPreference; $ErrorActionPreference = "Continue"
python tools/umfang_pruefen.py
$ErrorActionPreference = $alt

Write-Host "`n=== Gesamtdatei fuer online =============================" -ForegroundColor Cyan
python tools/gesamt.py

Write-Host "`nFertig." -ForegroundColor Green
