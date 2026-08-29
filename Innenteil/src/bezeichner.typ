// Sprachabhängige Überschriften und Bezeichner.
// Die TUHH lässt Deutsch oder Englisch zu, keine dritte Sprache.

#let texte = (
  de: (
    inhalt: "Inhaltsverzeichnis",
    abbildungen: "Abbildungsverzeichnis",
    tabellen: "Tabellenverzeichnis",
    abkuerzungen: "Abkürzungsverzeichnis",
    formelzeichen: "Formelzeichen",
    glossar: "Glossar",
    zusammenfassung: "Kurzfassung",
    abstract: "Abstract",
    herausgebervorwort: "Vorwort des Herausgebers",
    vorwort: "Vorwort zum Band",
    danksagung: "Danksagung",
    literatur: "Literaturverzeichnis",
    studentische_arbeiten: "Studentische Arbeiten im Rahmen dieser Arbeit",
    anhang: "Anhang",
    ki_erklaerung: "KI-Erklärung",
    eidesstattlich: "Eidesstattliche Erklärung",
    lebenslauf: "Lebenslauf",
    abbildung: "Abbildung",
    tabelle: "Tabelle",
  ),
  en: (
    inhalt: "Contents",
    abbildungen: "List of Figures",
    tabellen: "List of Tables",
    abkuerzungen: "Abbreviations",
    formelzeichen: "Nomenclature",
    glossar: "Glossary",
    zusammenfassung: "Abstract",
    abstract: "Kurzfassung",
    herausgebervorwort: "Editor's Preface",
    vorwort: "Preface to this Volume",
    danksagung: "Acknowledgements",
    literatur: "References",
    studentische_arbeiten: "Student Theses Supervised in the Course of this Work",
    anhang: "Appendix",
    ki_erklaerung: "Declaration on the Use of AI Tools",
    eidesstattlich: "Declaration on Oath",
    lebenslauf: "Curriculum Vitae",
    abbildung: "Figure",
    tabelle: "Table",
  ),
)

/// Liefert die Bezeichner für die eingestellte Sprache.
#let bezeichner(sprache) = texte.at(sprache)
