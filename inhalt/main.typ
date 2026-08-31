// ===========================================================================
//  Hauptdatei des Innenteils - hier stehen NUR deine Kapitel und Anhaenge.
//
//  Alle Angaben zur Arbeit stehen in angaben.typ, der Satz selbst liegt in
//  ../template/ und wird hier nur aufgerufen. Gebaut wird mit ..\bauen.ps1
//  (oder ../bauen.sh) - siehe ../docs/ANLEITUNG.md.
//
//  Ein neues Kapitel: Datei in kapitel/ anlegen und unten eine Zeile in die
//  Liste eintragen. Die Reihenfolge hier ist die Reihenfolge im Buch.
// ===========================================================================

#import "/template/innenteil/buch.typ": buch
#import "angaben.typ": diss, abkuerzungen, formelzeichen

#show: buch.with(
  diss,
  abkuerzungen: abkuerzungen,
  formelzeichen: formelzeichen,
  // Die Quellen. Die .bib-Datei liegt neben dieser Datei und wird von
  // Zotero gepflegt - siehe docs/ANLEITUNG.md, Kapitel "Literatur und Zotero".
  literatur: bibliography(
    "literatur.bib",
    title: none,
    style: "/template/ISEM-Zitationsstil.csl",
  ),
  kapitel: (
    (
      titel: "Einleitung",
      kennung: "kap-einleitung",
      inhalt: include "kapitel/01_einleitung.typ",
    ),
    (
      titel: "Stand der Forschung",
      kennung: "kap-stand",
      inhalt: include "kapitel/02_stand.typ",
    ),
    (
      titel: "Zusammenfassung und Ausblick",
      kennung: "kap-fazit",
      inhalt: include "kapitel/03_zusammenfassung.typ",
    ),
  ),
  anhaenge: (
    (
      titel: "Erster Anhang",
      kennung: "anh-a",
      inhalt: include "anhang/A_ergaenzungen.typ",
    ),
    (
      titel: "Zweiter Anhang",
      kennung: "anh-b",
      inhalt: include "anhang/B_weiteres.typ",
    ),
  ),
)
