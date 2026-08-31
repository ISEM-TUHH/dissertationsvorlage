# -*- coding: utf-8 -*-
"""Findet Fussnoten, in denen der falsche Literatureintrag zitiert wird.

    python tools/zitate_richtigstellen.py <original.pdf> <kapitel> [--aendern]

Bei der Uebernahme aus dem Word-Original sind Zitierschluessel eingeebnet
worden: wo die Arbeit "Albers & Wintergerst, 2013" nachweist, steht im Band
"Albers, Behrendt, Schroeter, Ott & Klingler, 2013". Beide Eintraege gibt es,
beide tragen dasselbe Jahr - der Unterschied faellt nur auf, wenn man die
Namen liest.

Zugeordnet wird ueber den Text davor, nicht ueber die Reihenfolge: zu jeder
Verweisziffer im Original werden die letzten Buchstaben des Satzes davor
gemerkt. Dieselben Buchstaben stehen im Quelltext des Bandes vor dem Zitat.
Damit findet jede Zitierstelle ihre Fussnote im Original, auch wenn davor
oder danach Fussnoten fehlen.

Ohne --aendern wird nur berichtet.
"""
import difflib
import glob
import os
import re
import sys
import unicodedata

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), "inhalt"))

argumente = [a for a in sys.argv[1:] if not a.startswith("--")]
AENDERN = "--aendern" in sys.argv
if len(argumente) < 2:
    sys.exit("Aufruf: python tools/zitate_richtigstellen.py <original.pdf> "
             "<kapitel> [--aendern]")
ORIGINAL, KAPITEL = argumente[0], int(argumente[1])
ANKER = 45          # Buchstaben vor der Verweisziffer

orig = fitz.open(ORIGINAL)


# ── Literaturverzeichnis ────────────────────────────────────────────────
def schlicht(wort):
    wort = unicodedata.normalize("NFKD", wort)
    wort = "".join(z for z in wort if not unicodedata.combining(z))
    return re.sub(r"[^a-z]", "", wort.lower())


def nachnamen(feld):
    namen = []
    for teil in re.split(r"\s+and\s+", feld):
        teil = teil.strip().strip("{}")
        if not teil:
            continue
        namen.append(teil.split(",")[0].strip() if "," in teil
                     else teil.split()[-1])
    return namen


EINTRAEGE = {}
for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}",
                     open("literatur.bib", encoding="utf-8").read(), re.S):
    a = re.search(r"author\s*=\s*\{(.*?)\}\s*,\s*\n", m.group(2), re.S)
    j = re.search(r"year\s*=\s*\{(\d{4})\}", m.group(2))
    if a and j:
        EINTRAEGE[m.group(1).strip()] = (
            [schlicht(n) for n in nachnamen(a.group(1))], j.group(1))


def passender_eintrag(namen, jahr, buchstabe=""):
    """Schluessel zu einer Autor-Jahr-Angabe.

    Das Original unterscheidet mehrere Arbeiten desselben Jahres durch einen
    angehaengten Buchstaben ("2015b"). Gibt es mehrere Eintraege mit gleicher
    Autorenliste, entscheidet dieser Buchstabe.
    """
    gesucht = [schlicht(n) for n in namen]
    genau = [k for k, (ns, y) in EINTRAEGE.items() if y == jahr and ns == gesucht]
    if len(genau) > 1 and buchstabe:
        passend = [k for k in genau if k.endswith(jahr + buchstabe)]
        if len(passend) == 1:
            return passend[0]
    if len(genau) == 1:
        return genau[0]
    anfang = [k for k, (ns, y) in EINTRAEGE.items()
              if y == jahr and ns[:len(gesucht)] == gesucht]
    return anfang[0] if len(anfang) == 1 else None


# ── Original: Fussnoten und Verweisziffern ──────────────────────────────
def kapitelbereich(nr):
    alle = [e for e in orig.get_toc() if e[0] == 1]
    for e in alle:
        if re.match(r"^%d\s" % nr, e[1].strip()):
            spaeter = [x[2] for x in alle if x[2] > e[2]]
            return e[2], (min(spaeter) - 1 if spaeter else orig.page_count)
    return None, None


def grundgrad(von, bis):
    h = {}
    for n in range(von, bis + 1):
        for b in orig[n - 1].get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    if s["text"].strip():
                        h[round(s["size"], 1)] = (h.get(round(s["size"], 1), 0)
                                                  + len(s["text"]))
    return max(h, key=h.get)


def buchstaben(t):
    t = (t.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
          .replace("ﬀ", "ff"))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(z for z in t if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]", "", t.lower())


def fussnoten(von, bis):
    grad = grundgrad(von, bis)
    gefunden = []
    for n in range(von, bis + 1):
        seite = orig[n - 1]
        hoehe = seite.rect.height
        zeilen = []
        for b in seite.get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp or max(s["size"] for s in sp) >= grad - 0.8:
                    continue
                if sp[0]["origin"][1] <= hoehe * 0.7:
                    continue
                zeilen.append((sp[0]["origin"][1],
                               "".join(s["text"] for s in sp)))
        zeilen.sort()
        laufend = None
        for _, t in zeilen:
            m = re.match(r"^(\d{1,3})(\D.*)$", t.strip())
            if m:
                if laufend:
                    gefunden.append(laufend)
                laufend = [int(m.group(1)), m.group(2).strip(), n]
            elif laufend:
                laufend[1] += " " + t.strip()
        if laufend:
            gefunden.append(laufend)
    return {nr: (txt, seite) for nr, txt, seite in gefunden}


def originaltext(von, bis):
    """Fortlaufender Buchstabentext des Kapitels und die Marken darin.

    Rueckgabe: (Text, [(Position, Fussnotennummer), ...]). Ueber die Position
    laesst sich zu jeder Textstelle die naechste Verweisziffer finden - auch
    dann, wenn im Band davor eine Fussnote fehlt oder eine Abbildung anders
    umbricht.
    """
    grad = grundgrad(von, bis)
    lauf, marken = [], []
    laenge = 0
    for n in range(von, bis + 1):
        seite = orig[n - 1]
        hoehe = seite.rect.height
        for b in seite.get_text("dict")["blocks"]:
            if b["type"]:
                continue
            for l in b["lines"]:
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp:
                    continue
                grundlinie = max(s["origin"][1] for s in sp)
                if grundlinie < hoehe * 0.07 or grundlinie > hoehe * 0.88:
                    continue
                gross = max(s["size"] for s in sp)
                ist_beschriftung = bool(re.match(
                    r"\s*(Abbildung|Tabelle)\s+\d+[.\-]\d+", 
                    "".join(s["text"] for s in sp)))
                if abs(gross - grad) > 0.6 and not ist_beschriftung:
                    continue
                for s in sp:
                    text = s["text"].strip()
                    hoch = (s["size"] < gross - 1.0
                            and s["origin"][1] < grundlinie - 1.0)
                    if hoch and re.fullmatch(r"\d{1,3}", text):
                        marken.append((laenge, int(text)))
                    else:
                        stueck = buchstaben(s["text"])
                        lauf.append(stueck)
                        laenge += len(stueck)
    return "".join(lauf), marken


# ── Quelltext des Bandes ────────────────────────────────────────────────
def bloecke(text):
    """Fussnotenbloecke und freistehende Zitate des Quelltextes.

    Eine Zitierstelle findet ihre Fussnote im Original auf zwei Wegen. Steht
    sie in einem #footnote[...], wird der Wortlaut des Blocks mit den
    Fussnoten des Originals verglichen. Steht ein blosses @schluessel im
    Flieszttext, erzeugt der Zitierstil daraus selbst eine Fussnote - dann
    weist der Text davor den Weg.
    """
    ergebnis = []
    i = 0
    while i < len(text):
        if text.startswith("#footnote[", i):
            tiefe, j = 0, i + len("#footnote")
            while j < len(text):
                if text[j] == "[":
                    tiefe += 1
                elif text[j] == "]":
                    tiefe -= 1
                    if tiefe == 0:
                        break
                j += 1
            ergebnis.append(("note", i, j + 1, text[i + len("#footnote["):j]))
            i = j + 1
            continue
        m = re.match(r"@([a-zA-Z][\w]*)", text[i:])
        if m and m.group(1) in EINTRAEGE:
            ergebnis.append(("frei", i, i + m.end(), m.group(1)))
            i += m.end()
            continue
        i += 1
    return ergebnis


def klartext(inhalt_fn):
    """Fussnotentext ohne Auszeichnung, mit den Autoren der Zitate."""
    def ersetze(m):
        namen, jahr = EINTRAEGE[m.group(1)]
        return " ".join(namen) + " " + jahr

    t = re.sub(r'#cite\(<([a-zA-Z][\w]*)>[^)]*\)',
               lambda m: ersetze(m) if m.group(1) in EINTRAEGE else " ",
               inhalt_fn)
    t = re.sub(r'#[a-zA-Z-]+(\([^)]*\))?', " ", t)
    return re.sub(r'<[^>]*>|[\[\]]', " ", t)


def anker_davor(text, stelle):
    davor = text[max(0, stelle - 900):stelle]
    davor = re.sub(r'#cite\([^)]*\)', " ", davor)
    davor = re.sub(r'#footnote\[', " ", davor)
    davor = re.sub(r'#[a-zA-Z-]+(\([^)]*\))?', " ", davor)
    davor = re.sub(r'<[^>]*>|[\[\]]|//.*', " ", davor)
    return buchstaben(davor)[-45:]


NAME = r"[A-ZÄÖÜ][\wäöüßÄÖÜ'’-]+"
ANGABE = re.compile(r"(" + NAME + r"(?:\s*(?:,|&|und)\s*" + NAME + r"){0,10})"
                    r"\s*,?\s*(\d{4})([a-z]?)\b")
KEIN_NAME = {"Siehe", "Vgl", "Nach", "Der", "Die", "Das", "In", "Im", "Bild",
             "Weitere", "Informationen", "Dabei", "Kapitel", "Tabelle",
             "Abbildung", "Anhang", "Band", "Seite", "Teilnehmer", "Zur",
             "Zum", "Mehr", "Details", "Publikation", "Publikationen",
             "Rahmen", "Betreute", "Abschlussarbeit", "Verein", "Deutscher",
             "Ingenieure", "Bundesministerium", "Darstellung", "Darstellungsform",
             "Anlehnung", "Ein", "Eine", "Review", "Keynote", "Symposium",
             "Produktentwicklung", "Vorwort", "Herausgebers"}


def angaben(text):
    treffer = []
    for m in ANGABE.finditer(text):
        namen = [n.strip() for n in re.split(r"\s*(?:,|&|und)\s*", m.group(1))
                 if n.strip()]
        namen = [n for n in namen
                 if n not in KEIN_NAME and len(n) > 2 and not n.endswith(".")]
        if namen:
            treffer.append((namen, m.group(2), m.group(3)))
    return treffer


ov, ob = kapitelbereich(KAPITEL)
if ov is None:
    sys.exit("Kapitel %d im Original nicht gefunden" % KAPITEL)
NOTEN = fussnoten(ov, ob)
TEXT, MARKEN = originaltext(ov, ob)


def fussnote_bei(schwanz):
    """Nummer der Verweisziffer, die im Original auf diesen Text folgt."""
    for laenge in (45, 36, 28, 22, 18):
        stueck = schwanz[-laenge:]
        if len(stueck) < laenge:
            continue
        stelle = TEXT.find(stueck)
        if stelle < 0 or TEXT.find(stueck, stelle + 1) >= 0:
            continue          # nicht gefunden oder nicht eindeutig
        ende = stelle + len(stueck)
        nach = [nr for pos, nr in MARKEN if 0 <= pos - ende <= 3]
        if nach:
            return nach[0]
    return None

pfad = glob.glob("kapitel/%02d_*.typ" % KAPITEL)[0]
inhalt = open(pfad, encoding="utf-8").read()

print("Kapitel %d: %d Fussnoten und %d Verweisziffern im Original"
      % (KAPITEL, len(NOTEN), len(MARKEN)))
print()

aenderungen, ungeklaert = [], 0
verbraucht = {}


def schluessel_der_note(nummer, rang):
    """Der rang-te Literatureintrag, den die Original-Fussnote nennt."""
    text = NOTEN.get(nummer, ("", 0))[0]
    soll = []
    for namen, jahr, buchstabe in angaben(text):
        k = passender_eintrag(namen, jahr, buchstabe)
        if k:
            soll.append(k)
    return (soll[rang] if rang < len(soll) else None), text


for art, a, e, inhalt_block in bloecke(inhalt):
    if art == "note":
        # Passende Fussnote des Originals ueber den Wortlaut suchen.
        eigen = buchstaben(klartext(inhalt_block))
        beste, guete = None, 0.0
        for nr, (otext, _) in NOTEN.items():
            g = difflib.SequenceMatcher(None, eigen, buchstaben(otext)).ratio()
            if g > guete:
                beste, guete = nr, g
        if guete < 0.45:
            ungeklaert += 1
            continue
        nummer = beste
        zitate = list(re.finditer(r'#cite\(<([a-zA-Z][\w]*)>', inhalt_block))
        # Sammelnachweise nennen bis zu neun Quellen in einer Fussnote. Wenn
        # die Namensauswertung des Originals weniger findet als der Quelltext
        # zitiert, ist die Reihenfolge nicht verlaesslich - dann wird die
        # Fussnote uebergangen statt falsch berichtigt.
        erkannt, _ = schluessel_der_note(nummer, 0), None
        anzahl = len([1 for namen, jahr, bu in angaben(NOTEN[nummer][0])
                      if passender_eintrag(namen, jahr, bu)])
        if anzahl < len(zitate):
            ungeklaert += 1
            continue
        for rang, m in enumerate(zitate):
            soll, otext = schluessel_der_note(nummer, rang)
            if soll and soll != m.group(1):
                versatz = a + len("#footnote[") + m.start(1)
                aenderungen.append((versatz, versatz + len(m.group(1)),
                                    m.group(1), soll, nummer, otext))
    else:
        nummer = fussnote_bei(anker_davor(inhalt, a))
        if not nummer:
            ungeklaert += 1
            continue
        rang = verbraucht.get(nummer, 0)
        verbraucht[nummer] = rang + 1
        soll, otext = schluessel_der_note(nummer, rang)
        if soll and soll != inhalt_block:
            aenderungen.append((a + 1, e, inhalt_block, soll, nummer, otext))

print("%d Zitierstelle(n) konnten nicht zugeordnet werden." % ungeklaert)
print("%d falsche Zitierschluessel:" % len(aenderungen))
for a, e, alt, neu, nummer, otext in aenderungen:
    print("   Z.%-5d Fn %-4d %-17s -> %-17s  %s"
          % (inhalt.count(chr(10), 0, a) + 1, nummer, alt, neu,
             re.sub(r"\s+", " ", otext)[:70]))

if AENDERN and aenderungen:
    neu_text = inhalt
    for a, e, alt, neu, *_ in sorted(aenderungen, key=lambda x: -x[0]):
        assert neu_text[a:e] == alt, (neu_text[a:e], alt)
        neu_text = neu_text[:a] + neu + neu_text[e:]
    open(pfad, "w", encoding="utf-8", newline="\n").write(neu_text)
    print()
    print("%d Schluessel in %s berichtigt." % (len(aenderungen), pfad))
