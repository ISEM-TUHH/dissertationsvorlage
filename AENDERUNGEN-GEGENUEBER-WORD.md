---
titel: Änderungen gegenüber der Word-Vorlage
zweck: nachvollziehbar machen, was am Satz geändert wurde und warum
stand: 2026-08-29
---

# Vom Word-Satz zum Reihenband

Ausgangspunkt dieser Vorlage war eine Word-Fassung: 185 Seiten, erzeugt mit
Word für Microsoft 365. Sie sah gut aus, war aber zum Lesen am Bildschirm und
zum Ausdrucken gedacht, nicht zum Binden eines Buches.

> **Das Aussehen ist absichtlich geblieben.** Satzspiegel, Schriftgrade und
> Abstände sind aus der Word-Fassung nachgemessen, nicht geschätzt — die
> Grundlinien stimmen auf zwei Hundertstel Millimeter. Geändert haben wir das
> Verfahren dahinter und alles, was für ein gedrucktes Reihenbuch dazugehört.

Sortiert ist die Liste nach Aufwand: oben, was in Word ein Häkchen ist und
sofort etwas bringt — unten das, wofür Word nicht gebaut ist. Wer bei Word
bleiben möchte, kann bei Stufe 1 anfangen und aufhören, wann er will.
Menüpfade nach Word für Microsoft 365, deutsche Oberfläche.

---

## Stufe 1 — sofort

Fünfzehn Punkte, zusammen an einem Nachmittag erledigt. Sie machen den
größten Teil des Unterschieds aus.

### Gegenüberliegende Seitenränder, innen 14 mm, außen 15 mm

Ein gebundenes Buch verschluckt am Bund einige Millimeter. Der Bundsteg muss
deshalb breiter sein als der Außensteg, und beides muss sich seitenweise
spiegeln. Für die Bildschirmfassung setzen wir dagegen symmetrisch — dort
gibt es keinen Bund, und eine wandernde Spalte wirkt beim Blättern am Monitor
nur unruhig.

**In Word:** `Layout → Seitenränder → Benutzerdefinierte Seitenränder`, unter
„Mehrere Seiten“ *Gegenüberliegende Seiten* wählen; die Felder heißen dann
Innen und Außen.

### Erstzeileneinzug statt Absatzabstand

Neue Absätze beginnen mit einem Einzug, statt durch eine Leerzeile getrennt zu
werden. Das ist der klassische Buchsatz: Der Text bleibt eine geschlossene
Fläche, und die Seite füllt sich gleichmäßig bis zum Fuß.

**In Word:** In der Formatvorlage *Standard*
`Absatz → Sondereinzug: Erste Zeile, 0,35 cm`, Abstand vor/nach auf 0. Für den
ersten Absatz nach einer Überschrift eine zweite Formatvorlage ohne Einzug
anlegen — dort ist er unerwünscht.

### Bildkomprimierung abschalten

Die Druckerei verlangt 300 dpi. Word rechnet eingefügte Bilder standardmäßig
herunter — beim Speichern, unbemerkt und unwiederbringlich. Das ist der
häufigste Grund für unscharfe Abbildungen im fertigen Buch.

**In Word:** `Datei → Optionen → Erweitert → Bildgröße und -qualität`, Häkchen
bei *Bilder in Datei nicht komprimieren*, Standardauflösung auf *Hohe
Qualität*. Am besten gleich zu Beginn, denn einmal komprimierte Bilder holt
man nicht zurück.

### Absatzkontrolle und begrenzte Trennstriche

Einzelne Zeilen, die allein am Seitenkopf oder -fuß stehen, stören den
Lesefluss; drei oder vier getrennte Zeilen untereinander bilden eine störende
Treppe am rechten Rand.

**In Word:** `Absatz → Zeilen- und Seitenumbruch → Absatzkontrolle` (meist
schon an) und `Layout → Silbentrennung → Silbentrennungsoptionen`,
aufeinanderfolgende Trennstriche auf 2 begrenzen.

### Formeln in Cambria Math

Der Fließtext steht in Cambria; die zugehörige Formelschrift ist Cambria Math.
Passen die beiden nicht zusammen, fallen die Ziffern in der Formel gegenüber
denen im Text auf.

**In Word:** Nichts zu tun — der Formeleditor setzt von Haus aus in Cambria
Math. Einzelne Größen im Fließtext über `Einfügen → Formel` setzen, damit sie
kursiv und in derselben Schrift stehen.

### Kapitälchen für Autornamen

Zitierte Autornamen im Fließtext stehen in Kapitälchen. Das hebt sie ruhig
heraus, ohne dass Fettung oder Kursive den Lesefluss unterbrechen.

**In Word:** `Start → Schriftart → Effekte: Kapitälchen`, am besten als eigene
Zeichenformatvorlage. Kleine Einschränkung: Word rechnet Kapitälchen aus
Großbuchstaben herunter, statt die echten der Schrift zu nehmen — sie geraten
dadurch etwas zu dünn. Für den Alltag reicht es.

### Bildunterschriften eigenständig setzen

Beschriftungen stehen in 9 pt mit farbiger Kennung und Abstand nach unten. Sie
sollen sich vom Fließtext unterscheiden, damit man beim Blättern sofort sieht,
was Bildlegende ist und was Text.

**In Word:** Die Formatvorlage *Beschriftung* gibt es bereits; sie einmal
anpassen genügt. Beschriftungen immer über `Verweise → Beschriftung einfügen`
setzen, nie von Hand — sonst zählt Word nicht mit.

### Aufzählungszeichen in der Hausfarbe

Punkte und Nummern stehen in ISEM-Petrol, der Text bleibt schwarz. Das
gliedert die Seite, ohne den Lesefluss zu stören, und nimmt die Farbe des
Umschlags auf.

**In Word:**
`Start → Aufzählungszeichen → Neues Aufzählungszeichen definieren → Schriftart → Farbe`.
Bei Nummerierungen erbt die Zahl die Formatierung der Absatzmarke: Absatzmarke
markieren, einfärben. Die Hausfarbe vorher unter
`Entwurf → Farben → Farben anpassen` als Designfarbe hinterlegen.

### Querverweise als Feld statt als Text

„vgl. Abbildung 2.21“ soll im PDF an die richtige Stelle springen — und die
Nummer soll stimmen, auch wenn vorne eine Abbildung dazukommt.

**In Word:** `Verweise → Querverweis`. Das ist in Word sogar bequemer als in
einem Satzprogramm, und beim PDF-Export entsteht daraus automatisch ein
Sprungziel.

### Glossar aus den Definitionen

Nummerierte Definitionen gehören mit Seitenzahl in ein Verzeichnis. Von Hand
gepflegt, stimmt es nach der zweiten Überarbeitung nicht mehr.

**In Word:** `Verweise → Beschriftung einfügen → Neue Bezeichnung: „Definition“`.
Danach erzeugt `Verweise → Abbildungsverzeichnis` mit der Beschriftungskategorie
*Definition* das fertige Glossar. Ein Punkt, den Word wirklich gut kann.

### Impressum auf einer linken Seite

Das Impressum steht auf der Rückseite des Schmutztitels — dort sucht man es in
Verlagsreihen. Nebenbei spart das zwei Leerseiten, weil die Rückseite ohnehin
frei wäre.

**In Word:** `Layout → Umbrüche → Abschnittswechsel: Gerade Seite`. Word fügt
bei Bedarf selbst eine Leerseite ein.

### Schmutztitel, Kolophon, ISSN und DOI

Vor dem Deckblatt steht ein Schmutztitel mit Reihe, Band und Herausgeber. Im
Impressum stehen Coverdesign, Druckerei, Papiersorte, Rechtevorbehalt und der
Hinweis auf die Deutsche Nationalbibliothek. Die Reihe bekommt eine ISSN je
Ausgabe, die Bände statt einer ISBN jeweils einen DOI — so ist jeder Band
dauerhaft zitierbar, ohne dass für jeden eine ISBN beschafft werden muss.

**In Word:** Reiner Text auf zwei zusätzlichen Seiten. Der Aufwand liegt nicht
im Satz, sondern darin, die Angaben einmal vollständig zusammenzutragen.

### Lange Überschriften im Inhaltsverzeichnis umbrechen

Eine lange Kapitelüberschrift soll umbrechen, statt die Punktführung zu
verdrängen. Sonst steht die Seitenzahl irgendwo im Nichts.

**In Word:** Formatvorlagen *Verzeichnis 1* bis *Verzeichnis 3* anpassen,
hängender Einzug in Höhe der Nummernbreite, danach das Verzeichnis einmal
aktualisieren.

### Getaggtes PDF mit Alternativtexten

Ein getaggtes PDF hat eine Lesereihenfolge, die ein Screenreader auswerten
kann; jede Abbildung braucht dafür einen Alternativtext. Nachträglich lässt
sich das kaum reparieren.

**In Word:** Beim Export
`Optionen → Dokumentstrukturtags für Barrierefreiheit` anhaken; Alternativtexte
über Rechtsklick auf das Bild. `Überprüfen → Barrierefreiheit prüfen` findet,
was fehlt.

### Getrennte Ordner für fertige Dateien

Es muss jederzeit klar sein, welche Datei an die Druckerei geht. Wir legen die
fertigen Dateien nach `Druckversion`, `Onlineversion`, `Archivversion` und
`Kontrolle`; Zwischenstände bleiben davon getrennt.

**In Word:** Reine Dateiablage — dieselbe Ordnung lässt sich mit jedem
Schreibprogramm halten.

---

## Stufe 2 — mit Aufwand

Erreichbar in Word, hält sich aber nicht von selbst. Diese Punkte müssen nach
jeder größeren Überarbeitung nachgezogen werden und lohnen deshalb vor allem
kurz vor der Abgabe.

### Registerhaltiger Satz

Alle Zeilen liegen auf einem Raster von 12,9 pt, sodass Vorder- und Rückseite
eines Blattes auf gleicher Höhe stehen. Im Buch scheint das Papier durch; ohne
Register sieht man ein leichtes Zittern hinter dem Text.

| Maß | Wert |
|---|---|
| Rasterschritt | 12,9 pt |
| Satzspiegel | 119 × 173 mm |
| Zeilen je Seite | 38 |
| Zeichen je Zeile | ≈ 74 |

**In Word:** Ein echtes Raster kennt Word nicht, aber man kommt nah heran: in
allen Formatvorlagen `Zeilenabstand: Genau, 12,9 pt` und jeden Abstand
vor/nach als Vielfaches davon. Der Haken: Abbildungen und Formeln müssen von
Hand auf ein Vielfaches der Zeilenhöhe gebracht werden, sonst verrutscht alles
Folgende.

### Schmales geschütztes Leerzeichen

„z. B.“, „Abb. 2.3“, „12. Januar“, „§ 4“ und „75 %“ bekommen ein schmales
geschütztes Leerzeichen. Das hält die Teile zusammen — sonst rutscht das „B.“
allein in die nächste Zeile — und der Abstand ist enger als ein normales
Wortleerzeichen, wie der Duden es vorsieht.

**In Word:** Das Zeichen tippt man als `202F` gefolgt von `Alt + C`. Für die
häufigsten Fälle lohnen AutoKorrektur-Einträge; den Rest erledigt kurz vor der
Abgabe ein Durchgang mit Suchen & Ersetzen. Das normale geschützte
Leerzeichen hält zwar zusammen, ist aber zu breit.

### Mehr Luft unter dem Fußnotenstrich

In der Word-Fassung klebte der Trennstrich am ersten Fußnoteneintrag und
wirkte wie ein Unterstrich der letzten Textzeile.

**In Word:** Die Trennlinie ist nur in der Entwurfsansicht erreichbar:
`Ansicht → Entwurf`, dann `Verweise → Notizen anzeigen` und im Auswahlfeld
*Fußnotentrennlinie*. Dort einen leeren Absatz mit fester Höhe anfügen.

### Motto und Widmung auf fester Höhe

Beide beginnen im oberen Drittel der Seite, unabhängig davon, wie lang der
Text ist und was davor steht. Beim Blättern liegen sie damit an derselben
Stelle.

**In Word:** Am verlässlichsten mit einem Textfeld ohne Rahmen und absoluter
Position. Ein Absatz mit festem Abstand davor tut es auch, wandert aber mit,
sobald sich der Text davor ändert.

### Falzkante auf dem ersten und letzten Blatt

Dort wird der Buchblock in den Deckel geklebt. Alles, was näher als 7 mm am
Bund steht, verschwindet im Falz.

**In Word:** Eigener Abschnitt für die betroffenen Blätter mit größerem
Bundsteg. Funktioniert, muss aber überlebt werden, wenn sich der Umfang
ändert.

### Seitenzahl durch vier teilbar

Ein Buchblock besteht aus gefalzten Bogen. Geht die Seitenzahl nicht auf,
füllt die Druckerei selbst auf — an einer Stelle, die sie aussucht.

**In Word:** Leerseiten am Ende anfügen und die Seitenzahl in der Statusleiste
im Blick behalten. Muss nach der allerletzten Änderung noch einmal geprüft
werden.

### Zitieren im Notenstil

Ein Zitat im Text erzeugt die Fußnote selbst, und das Literaturverzeichnis
entsteht aus derselben Quelle. Werden beide getrennt gepflegt, laufen sie mit
jeder Überarbeitung weiter auseinander.

**In Word:** Die eingebaute Quellenverwaltung kennt nur Autor-Jahr-Stile. Für
Fußnotenzitate braucht es *Zotero* oder *Citavi* mit einem CSL-Notenstil. Der
ISEM-Zitationsstil liegt als CSL-Datei bei und lässt sich dort direkt
einhängen.

### Trennungen über den Seitenumbruch vermeiden

Ein Trennstrich am Fuß einer rechten Seite zwingt zum Umblättern mit einem
halben Wort im Kopf.

**In Word:** Es gibt keine Einstellung dafür — man findet die Stellen nur beim
Durchsehen. Der Eingriff ist dann klein: die automatische Silbentrennung für
diesen einen Absatz abschalten.

---

## Stufe 3 — anderes Werkzeug

Word ist ein Textverarbeitungsprogramm und kennt nur RGB. Alles, was mit der
Druckvorstufe zu tun hat, muss danach passieren — mit Acrobat Pro oder über
die Druckerei.

### CMYK-Ausgabe und Schwarz nur im K-Kanal

Fließtext wird als `0/0/0/100` gesetzt. Wird Schwarz über ein Farbprofil
umgerechnet, entsteht vierfarbiges Schwarz — und schon eine geringe
Passerdifferenz der Druckmaschine lässt die Schrift unscharf und farbig
gesäumt erscheinen. Deshalb ist in dieser Vorlage jede Farbe in beiden
Farbräumen verbindlich hinterlegt und wird nie umgerechnet.

**Nicht in Word.** Die Umwandlung macht anschließend
`Acrobat Pro → Druckproduktion → Farben konvertieren`, dort mit der
Einstellung, die reines Schwarz erhält.

### Beschnittzugabe und TrimBox

Die Druckdatei ist ringsum 3 mm größer als das Endformat und trägt eine
TrimBox. Ohne Zugabe entsteht am Rand ein weißer Blitzer, sobald der Schnitt
um einen Zehntelmillimeter wandert.

**Nicht in Word.** Seitengröße lässt sich auf 154 × 216 mm stellen, die
TrimBox setzt danach `Acrobat Pro → Druckproduktion → Seitenrahmen festlegen`.

### Eingebettete Ausgabebedingung

Das ICC-Profil ISO Coated v2 300 % steckt in Innenteil und Umschlag. Damit
weiß die Druckerei, auf welches Papier und welchen Farbauftrag die Datei
gerechnet ist.

**Nicht in Word.** `Acrobat Pro → Druckproduktion → Preflight` kann sie
eintragen; alternativ übernimmt die Druckerei das — dann sollte man ihr das
gewünschte Profil ausdrücklich nennen.

### PDF/A-2b und PDF/UA-1

TORE und die Deutsche Nationalbibliothek nehmen Langzeitarchivfassungen.
PDF/A sichert die Lesbarkeit in zwanzig Jahren, PDF/UA die Zugänglichkeit für
Screenreader.

**Nur teilweise in Word.** Beim Export gibt es
`Optionen → ISO 19005-1-kompatibel (PDF/A)` — das ist allerdings PDF/A-1a, die
ältere Stufe. PDF/A-2b und die PDF/UA-Kennzeichnung setzt erst Acrobat Pro.
Die Vorarbeit — Tags und Alternativtexte — leistet Word aber schon.

### Drei Ausgaben aus einer Quelle

| Fassung | Format | Farbe |
|---|---|---|
| Druck | 154 × 216 mm | CMYK |
| Online | 148 × 210 mm | RGB |
| Archiv | 148 × 210 mm | PDF/A + UA |

**Nicht in Word.** Word kennt einen Satz Seiteneinstellungen je Dokument. Drei
Fassungen hieße drei Dateien — und damit die Gefahr, dass eine davon eine
Korrektur nicht mitbekommt.

### Umschlag mit gerechneter Rückenstärke

Die Rückenbreite hängt an der Seitenzahl: 0,104 mm je Blatt plus 2,2 mm
Graupappe je Deckel. Der Verfassername steht über dem Titel, damit er bei
jedem Band der Reihe auf gleicher Höhe liegt — unter dem Titel wanderte er mit
dessen Länge nach unten. Die Logos sind Vektorpfade in CMYK; ein Pixelbild
würde an den Kanten ausfransen.

**Nicht in Word.** Der Umschlag ist eine Grafikaufgabe. Wichtig ist die
Verbindung: Ändert sich der Umfang, ändert sich der Rücken. Ein Skript
vergleicht nach jedem Bauen beides.

### Prüfskripte nach jedem Bauen

26 kleine Skripte prüfen Seitenformat, Beschnitt, Sicherheitsabstand,
Falzkante, Bogenteilung, Farbraum, K-Schwarz, Ausgabebedingung,
Schrifteinbettung, Lesezeichen, Kapitelanfänge auf der rechten Seite,
Bildauflösung und den Umbruch.

**Teilweise ersetzbar.** `Acrobat Pro → Druckproduktion → Preflight` prüft die
drucktechnischen Punkte sehr gut. Was es dort nicht gibt, sind die
inhaltlichen Prüfungen — ob eine Abbildung mitten im Satz steht, ob eine
Aufzählung abbricht, ob ein Kapitel auf einer linken Seite beginnt.

---

## Kurz gefasst

Wer in Word bleiben will und nur **Stufe 1** umsetzt, hat den größten Teil
gewonnen: gespiegelte Ränder, Einzug statt Abstand, unkomprimierte Bilder,
saubere Beschriftungen, Querverweise und ein automatisches Glossar. Das ist
ein Nachmittag Arbeit und der Unterschied zwischen einem Ausdruck und einem
Buch.

**Stufe 2** lohnt sich, wenn der Text steht — Register und Schmalleerzeichen
sollte man nicht während des Schreibens pflegen, sondern am Ende in einem
Durchgang.

**Stufe 3** braucht Acrobat Pro. Wer den nicht hat, sollte mit der Druckerei
sprechen, bevor die Datei fertig ist — Beschnitt und Farbraum nachträglich zu
retten ist teurer, als sie vorher richtig anzulegen.
