# Erzeugt Online- und Druckfassung des Innenteils und prueft beide.
#     .\bauen.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
# Zwischendateien bleiben hier, die fertigen Dateien wandern in
# ..\build mit seinen Unterordnern.
foreach ($o in "build", "..\build\Druckversion", "..\build\Onlineversion", "..\build\Archivversion", "..\build\Kontrolle") {
  if (-not (Test-Path $o)) { New-Item -ItemType Directory $o | Out-Null }
}

Write-Host "Onlinefassung (RGB, 148 x 210 mm, ohne Beschnitt) ..."
typst compile main.typ ../build/Onlineversion/innenteil.pdf

Write-Host "Onlinefassung verkleinern ..."
python tools/verkleinern.py ../build/Onlineversion/innenteil.pdf

Write-Host "Archivfassung (PDF/A-2b + PDF/UA-1, fuer TORE und DNB) ..."
typst compile --pdf-standard a-2b,ua-1 main.typ ../build/Archivversion/innenteil.pdf

Write-Host "Satz fuer den Druck (doppelseitig) ..."
typst compile --input ausgabe=druck main.typ build/_satz-druck.pdf

Write-Host "Druckfassung (CMYK, 154 x 216 mm mit 3 mm Beschnitt) ..."
python tools/druckdatei.py build/_satz-druck.pdf ../build/Druckversion/innenteil.pdf

Write-Host ""
python tools/pruefen.py
Write-Host ""
python tools/tuhh_pruefen.py ../build/Onlineversion/innenteil.pdf

Write-Host ""
python tools/umbruch_pruefen.py ../build/Druckversion/innenteil.pdf
