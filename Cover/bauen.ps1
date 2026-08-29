# Erzeugt alle PDF und prueft sie. Aufruf aus dem Ordner Cover heraus:
#     .\bauen.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
# Zwischendateien bleiben hier, die fertigen Dateien wandern in
# ..\build mit seinen Unterordnern.
foreach ($o in "build", "..\build\Druckversion", "..\build\Onlineversion", "..\build\Archivversion", "..\build\Kontrolle") {
  if (-not (Test-Path $o)) { New-Item -ItemType Directory $o | Out-Null }
}

Write-Host "Logos aus den Quellen erzeugen ..."
python tools/gen_logos.py

Write-Host "Druckdatei Umschlag (CMYK) ..."
typst compile --root . umschlag.typ ../build/Druckversion/umschlag.pdf

Write-Host "Ausgabebedingung eintragen (ISO Coated v2 300% ECI) ..."
python tools/ausgabebedingung.py ../build/Druckversion/umschlag.pdf

Write-Host "Kontrollansicht mit Hilfslinien ..."
typst compile --root . --input hilfslinien=ja umschlag.typ ../build/Kontrolle/umschlag-hilfslinien.pdf

Write-Host "Bildschirmfassung (RGB, Titelseite vorn / Rueckseite hinten) ..."
typst compile --root . --input farbraum=rgb bildschirm.typ ../build/Onlineversion/umschlag.pdf

Write-Host ""
python tools/pruefen.py
Write-Host ""
python tools/vergleich.py
