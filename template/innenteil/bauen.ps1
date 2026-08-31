# Erzeugt Online-, Archiv- und Druckfassung des Innenteils und prueft alle.
# Aufruf direkt oder ueber ..\bauen.ps1 im Wurzelordner.
#
# Gearbeitet wird im Ordner inhalt\ - dort liegen main.typ, die Kapitel und
# die Angaben. Gebaut wird mit --root auf dem Wurzelordner, damit main.typ
# die Vorlage unter /template/ erreicht.

$ErrorActionPreference = "Stop"
$wurzel = (Resolve-Path "$PSScriptRoot\..\..").Path
Set-Location "$wurzel\inhalt"

# Zwischendateien bleiben in inhalt\build, die fertigen Dateien wandern in
# ..\build mit seinen Unterordnern.
foreach ($o in "build", "..\build\Druckversion", "..\build\Onlineversion", "..\build\Archivversion", "..\build\Kontrolle") {
  if (-not (Test-Path $o)) { New-Item -ItemType Directory $o | Out-Null }
}

Write-Host "Onlinefassung (RGB, 148 x 210 mm, ohne Beschnitt) ..."
typst compile --root .. main.typ ../build/Onlineversion/innenteil.pdf

Write-Host "Onlinefassung verkleinern ..."
python ../template/innenteil/tools/verkleinern.py ../build/Onlineversion/innenteil.pdf

Write-Host "Archivfassung (PDF/A-2b + PDF/UA-1, fuer TORE und DNB) ..."
typst compile --root .. --pdf-standard a-2b,ua-1 main.typ ../build/Archivversion/innenteil.pdf

Write-Host "Satz fuer den Druck (doppelseitig) ..."
typst compile --root .. --input ausgabe=druck main.typ build/_satz-druck.pdf

Write-Host "Druckfassung (CMYK, 154 x 216 mm mit 3 mm Beschnitt) ..."
python ../template/innenteil/tools/druckdatei.py build/_satz-druck.pdf ../build/Druckversion/innenteil.pdf

Write-Host ""
python ../template/innenteil/tools/pruefen.py
Write-Host ""
python ../template/innenteil/tools/tuhh_pruefen.py ../build/Onlineversion/innenteil.pdf

Write-Host ""
python ../template/innenteil/tools/umbruch_pruefen.py ../build/Druckversion/innenteil.pdf
