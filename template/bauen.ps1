# Baut alles: Umschlag, Innenteil und die Online-Gesamtdatei.
# Aufgerufen wird ueber ..\bauen.ps1 im Wurzelordner.
#
# Ergebnisse
#   build\Druckversion\umschlag.pdf       Druckdatei Umschlag (CMYK, Beschnitt)
#   build\Druckversion\innenteil.pdf      Druckdatei Innenteil (CMYK, Beschnitt)
#   build\Onlineversion\dissertation.pdf  alles in einer Datei, zum Lesen und Verschicken
#   build\Archivversion\innenteil.pdf     PDF/A + PDF/UA, fuer TORE und die DNB
#   build\Kontrolle\                      Hilfslinien und Vergleichsbilder

$ErrorActionPreference = "Stop"
$wurzel = Split-Path $PSScriptRoot -Parent

Write-Host "`n=== Umschlag ============================================" -ForegroundColor Cyan
& "$PSScriptRoot\cover\bauen.ps1"

Write-Host "`n=== Innenteil ===========================================" -ForegroundColor Cyan
& "$PSScriptRoot\innenteil\bauen.ps1"

Write-Host "`n=== Umfang abgleichen ===================================" -ForegroundColor Cyan
Set-Location $wurzel
# Eine Abweichung ist hier eine Warnung, kein Abbruchgrund: solange der
# Innenteil noch waechst, stimmt die Seitenzahl im Cover naturgemaess nicht.
$alt = $ErrorActionPreference; $ErrorActionPreference = "Continue"
python template/tools/umfang_pruefen.py
$ErrorActionPreference = $alt

Write-Host "`n=== Gesamtdatei fuer online =============================" -ForegroundColor Cyan
python template/tools/gesamt.py

Write-Host "`nFertig." -ForegroundColor Green
