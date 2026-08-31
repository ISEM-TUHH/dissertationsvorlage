// Druckdatei fuer den Umschlag (U4 | Ruecken | U1) inklusive Beschnitt, CMYK.
// Inhalte werden nicht hier, sondern in inhalt/buchdaten.typ gepflegt.
//
//   typst compile umschlag.typ build/umschlag.pdf
//   typst compile --input hilfslinien=ja umschlag.typ build/umschlag-kontrolle.pdf

#import "src/cover.typ": umschlag
#import "/" + sys.inputs.at("inhalt", default: "inhalt") + "/buchdaten.typ": buch

#show: umschlag.with(
  titel: buch.titel,
  autor: buch.autor,
  reihe: buch.reihe,
  herausgeber: buch.herausgeber,
  band: buch.band,
  ruecken-titel: buch.ruecken-titel,
  ruecken-autor: buch.ruecken-autor,
  u4-text: buch.u4-text,
  isbn: buch.isbn,
  seiten: buch.seiten,
  bund: buch.bund,
  blattdicke: buch.blattdicke,
  pappe: buch.pappe,
  hilfslinien: sys.inputs.at("hilfslinien", default: "") != "",
)
