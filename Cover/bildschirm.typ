// Bildschirmfassung: zweiseitiges PDF ohne Beschnitt, Titelseite vorn,
// Rueckseite hinten. Zum Voran- und Nachstellen an die digitale Fassung.
//
//   typst compile --input farbraum=rgb bildschirm.typ build/cover-bildschirm.pdf
//
// Der Schalter --input farbraum=rgb rechnet die Palette aus src/farben.typ
// nach RGB um. Ohne ihn entsteht dieselbe Datei in CMYK.

#import "src/cover.typ": bildschirm
#import "buchdaten.typ": buch

#show: bildschirm.with(
  titel: buch.titel,
  autor: buch.autor,
  reihe: buch.reihe,
  herausgeber: buch.herausgeber,
  band: buch.band,
  u4-text: buch.u4-text,
  isbn: buch.isbn,
  breite: buch.bildschirm-breite,
  hoehe: buch.bildschirm-hoehe,
)
