#import "/template/innenteil/isem.typ": *


== Ausgangslage

Dieses Dokument ist die Demofassung der ISEM-Dissertationsvorlage. Es ist
zugleich ihre eigene Bedienungsanleitung: Jede Seite zeigt, was die Vorlage
kann, und der Text daneben erklärt, wie es aufgerufen wird. Wer das PDF liest
und die zugehörigen Dateien in `inhalt/kapitel/` daneben legt, sieht zu
jedem Ergebnis den Befehl, der es erzeugt hat.

Der Satz folgt den Formalia der Technischen Universität Hamburg und den
Gepflogenheiten des Buchdrucks. Beides zusammen ergibt eine Reihe von
Entscheidungen, die man im fertigen Buch kaum bemerkt, solange sie richtig
getroffen sind — und die sofort auffallen, wenn sie fehlen. Ein Absatz
beginnt deshalb mit einem Einzug und nicht mit einer Leerzeile, alle Zeilen
liegen auf einem festen Raster, und der Bundsteg ist schmaler als der
Außensteg, weil ein gebundenes Buch am Bund einige Millimeter verschluckt.

#lorem(60)

Ein Literaturverweis sieht so aus @beispiel2024, mehrere
so @beispiel2024 @beispiel2023. Der Zitierstil der Reihe ist ein Notenstil:
Aus dem Verweis im Text entsteht die Fußnote von selbst, und dieselbe Angabe
erscheint später im Literaturverzeichnis. Beides wird aus einer Quelle
gespeist, `inhalt/literatur.bib`, und kann deshalb nicht auseinanderlaufen.

=== Eine Ebene tiefer

Auf jeder Gliederungsebene muss es mindestens zwei Abschnitte geben — ein
1.1.1 ohne 1.1.2 ist nach dem TUHH-Leitfaden unzulässig. Die Vorlage prüft
das nicht für dich, aber sie macht es sichtbar: Wer nur einen
Unterabschnitt anlegt, sieht ihn im Inhaltsverzeichnis allein stehen.

#lorem(50)

Überschriften gibt es in vier Ebenen. Die erste beginnt immer auf einer
rechten Seite und trägt die Kapitelnummer groß über dem Titel; die zweite und
dritte stehen im laufenden Text. Für eine vierte Ebene, die nicht ins
Inhaltsverzeichnis soll, gibt es `#zwischentitel[…]`:

#zwischentitel[So sieht ein Zwischentitel aus]

Er ist fett und etwas kleiner als der Fließtext, wird nicht nummeriert und
taucht in keinem Verzeichnis auf. Für die Gliederung innerhalb eines längeren
Abschnitts ist er das richtige Mittel — eine echte vierte Ebene würde das
Inhaltsverzeichnis überladen.

=== Und die zweite auf gleicher Ebene

Aufzählungen tragen die Hausfarbe. Der Punkt ist petrolfarben, der Text
bleibt schwarz:

- Ein erster Punkt, der lang genug ist, um über die Zeile hinauszugehen und
  zu zeigen, wie die Folgezeile eines Aufzählungspunktes eingezogen wird.
- Ein zweiter Punkt.
- Ein dritter.

Dasselbe gilt für nummerierte Aufzählungen:

+ Der erste Schritt.
+ Der zweite Schritt.
+ Der dritte Schritt.

== Zielsetzung

#lorem(70)

Mikrotypografie kommt von selbst: z.B. und z. B. werden beide zu
„z.#h(0pt)B.“, ebenso u.a., d.h. und i.d.R. Vor Bezugsgrößen steht ein
schmales geschütztes Leerzeichen: Abb. 3, Kap. 2, Nr. 5, § 6, 15 %, 230 V,
12,5 kg und 1. Januar 2026. Du musst dafür nichts tun — schreib die
Abkürzung so, wie sie dir aus der Feder fließt, und die Vorlage setzt den
richtigen Abstand.

Zitierte Personen stehen in Kapitälchen: #autor[Albers] beschreibt das
Modell der SGE, #autor[Ropohl] das systemische Denken. Der Aufruf lautet
`#autor[Name]` und nutzt die echten Kapitälchen der Schrift, keine
verkleinerten Großbuchstaben.

Formeln stehen in Cambria Math, der zur Grundschrift gehörenden
Formelschrift. Das gilt auch für einzelne Größen im Fließtext: Die Masse
#mathe($m$, alt: "m") und die Lichtgeschwindigkeit #mathe($c$, alt: "c")
werden mit `#mathe($m$, alt: "m")` gesetzt und erscheinen dadurch kursiv und
in derselben Schrift wie die abgesetzte Formel. Das `alt` ist die
Textalternative für Screenreader — ohne sie lässt sich die barrierefreie
Archivfassung (PDF/UA) nicht bauen.

== Aufbau der Arbeit

#lorem(45)

Der Vorspann umfasst Schmutztitel, Deckblatt, Impressum, die Vorworte, die
Danksagung, Kurzfassung und Abstract sowie das Inhaltsverzeichnis. Er wird
römisch gezählt. Danach beginnt der Hauptteil mit arabischer Zählung; jedes
Kapitel fängt auf einer rechten Seite an.

Hinten folgen Anhang, Literaturverzeichnis und die Verzeichnisse der
Abbildungen, Tabellen, Formelzeichen, Abkürzungen und Definitionen. Welche
davon mitkommen, steht in `inhalt/angaben.typ` — jeder Teil hat dort einen
eigenen Schalter, und keiner muss von Hand gepflegt werden.
