# -*- coding: utf-8 -*-
"""Prueft die gesetzte Dissertation gegen die formalen TUHH-Anforderungen.

    python tools/tuhh_pruefen.py ../build/Onlineversion/dissertation.pdf

Grundlage
    Promotionsordnung TUHH §§ 6 Abs. 2 und 16
    Deckblattvorlagen 2a (Einreichung) und 4b (Endfassung)
    "Guidelines for Formal Aspects of Ph.D. Theses", Juli 2023
    "Hinweise finale Version der Dissertation", August 2026

Was hier NICHT geprueft werden kann, steht am Ende der Ausgabe. Diese Punkte
bleiben menschliche Aufgabe - das Skript behauptet nicht, sie abzudecken.
"""
import io
import os
import re
import sys

import fitz

HIER = os.path.dirname(os.path.abspath(__file__))
_wurzel = os.path.dirname(os.path.dirname(os.path.dirname(HIER)))
_inhalt = "inhalt" if os.path.isdir(os.path.join(_wurzel, "inhalt")) else "inhalt-vorlage"
BASIS = os.path.join(_wurzel, _inhalt)
os.chdir(BASIS)

pdf = sys.argv[1] if len(sys.argv) > 1 else "../build/Onlineversion/dissertation.pdf"

# --- angaben.typ auslesen ------------------------------------------------
quelle = io.open("angaben.typ", encoding="utf-8").read()


def feld(name, default=None):
    m = re.search(r"^\s*%s:\s*(.+?),\s*(?://.*)?$" % re.escape(name), quelle, re.M)
    if not m:
        return default
    w = m.group(1).strip()
    if w.startswith('"') and w.endswith('"'):
        return w[1:-1]
    if w in ("true", "false"):
        return w == "true"
    if re.fullmatch(r"\d+", w):
        return int(w)
    return w


fassung = feld("fassung")
befunde = []


def pruefe(bedingung, text, quellenangabe, hart=True):
    befunde.append((bool(bedingung), text, quellenangabe, hart))


d = fitz.open(pdf)


def deckblatt_finden(dok):
    """Nummer der Deckblattseite (0-basiert).

    Die Buchausgabe stellt dem Deckblatt einen Schmutztitel voran; das
    Deckblatt ist dann nicht mehr die erste Seite. Erkannt wird es an der
    Formel der TUHH-Vorlagen 2a und 4b.
    """
    for seite in dok:
        text = seite.get_text()
        if "Promotionsausschuss" in text and "Dissertation" in text:
            return seite.number
    return 0


erste = deckblatt_finden(d)
seite1 = d[erste].get_text()
seite2 = d[erste + 1].get_text() if d.page_count > erste + 1 else ""
volltext = "\n".join(s.get_text() for s in d)

print("Prüfung: %s" % pdf)
print("Fassung laut angaben.typ: %s" % fassung)
print("Deckblatt auf Seite %d\n" % (erste + 1))

# ── Deckblatt ────────────────────────────────────────────────────────────
if fassung == "eingereicht":
    pruefe("Dem Promotionsausschuss" in seite1,
           'Deckblatt sagt "Dem Promotionsausschuss ... vorgelegte Dissertation"',
           "Vorlage 2a")
    pruefe("vorgelegte Dissertation" in seite1,
           'Deckblatt nennt die Fassung "vorgelegte Dissertation"', "Vorlage 2a")
    pruefe(feld("betreuung", "") .split(":")[-1].strip()[:12] in seite1,
           "Betreuung ist auf dem Deckblatt genannt", "Vorlage 2a")
else:
    pruefe("Vom Promotionsausschuss" in seite1,
           'Deckblatt sagt "Vom Promotionsausschuss ... genehmigte Dissertation"',
           "Vorlage 4b")
    pruefe("genehmigte Dissertation" in seite1,
           'Deckblatt nennt die Fassung "genehmigte Dissertation"', "Vorlage 4b")
    # Die Vorlage 4b spricht von "Gutachtern"; verbreitet sind auch
    # "Hauptreferent/Korreferent" und "Referent/Korreferent".
    begutachtung = ("Gutachter", "Gutachterin", "Hauptreferent", "Korreferent",
                    "Referent", "Referentin")
    pruefe(any(w in seite2 for w in begutachtung),
           "Rückseite des Deckblatts nennt die Gutachtenden", "PromO § 16 Abs. 3")
    pruefe("mündlichen Prüfung" in seite2,
           "Rückseite nennt den Tag der mündlichen Prüfung", "PromO § 16 Abs. 3")

# Die Hochschulzeile steht in angaben.typ - Fremdbaende der Reihe stammen
# nicht zwingend von der TUHH.
_hs = feld("hochschule", "der Technischen Universität Hamburg")
_hs_kern = re.sub(r"^(der|des|dem)\s+", "", _hs)
pruefe(_hs_kern.split()[0] in seite1,
       "Hochschule genannt (%s)" % _hs_kern, "Vorlagen 2a / 4b")
pruefe(re.search(r"\(Monografie\)|\(kumulativ\)", seite1) is not None,
       "Art der Dissertation ist ausgewählt (Monografie oder kumulativ)",
       "Vorlagen 2a / 4b")
pruefe("(in)" not in seite1 and "(In)" not in seite1,
       "keine Klammer-Genderformen auf dem Deckblatt - Form ist aufgelöst",
       "Leitfaden: Genderformen konkret auflösen")
pruefe(str(feld("jahr")) in seite1,
       "Jahreszahl steht auf dem Deckblatt (%s)" % (
           "Jahr der Einreichung" if fassung == "eingereicht"
           else "Jahr der Veröffentlichung, nicht der mündlichen Prüfung"),
       "Vorlagen 2a / 4b")
ort = feld("geburtsort", "")
pruefe(ort in seite1, "Geburtsort steht auf dem Deckblatt (%s)" % ort,
       "Vorlagen 2a / 4b")
if "," not in ort:
    pruefe(True, "Geburtsort ohne Landangabe - nur zulässig bei Geburt in Deutschland",
           "Leitfaden", hart=False)

# ── Vorspann je Fassung ──────────────────────────────────────────────────
if fassung == "eingereicht":
    pruefe(not feld("mit_vorwort"), "kein Vorwort", "Leitfaden: kein persönlicher Vorspann")
    pruefe(not feld("mit_danksagung"), "keine Danksagung", "Leitfaden")
    pruefe(not feld("mit_widmung"), "keine Widmung", "Leitfaden")
    pruefe(feld("mit_zusammenfassung"), "Zusammenfassung enthalten", "PromO § 6 Abs. 2")
    pruefe(feld("mit_lebenslauf"), "Lebenslauf enthalten", "PromO § 6 Abs. 2, Muster 1d_b")
else:
    pruefe(True, "Vorwort, Danksagung und Widmung sind zulässig", "PromO § 16")

# ── Layout ───────────────────────────────────────────────────────────────
mm = 72.0 / 25.4
formate = {(round(p.rect.width / mm), round(p.rect.height / mm)) for p in d}
pruefe(formate == {(148, 210)} or formate == {(154, 216)},
       "einheitliches Seitenformat %s" % ", ".join("%dx%d mm" % f for f in sorted(formate)),
       "Leitfaden: Lesbarkeit auch bei A5-Druck")

toc = d.get_toc()
pruefe(len(toc) > 0, "PDF enthält Lesezeichen (%d)" % len(toc), "Lesbarkeit der PDF-Fassung")
pruefe(max([e[0] for e in toc], default=0) <= 3,
       "Lesezeichen bis zur dritten Gliederungsebene", "Vorgabe des Instituts")

# Gliederungslogik: kein 1.1 ohne 1.2
nummern = [e[1].split()[0] for e in toc if e[0] >= 2 and re.match(r"^\d", e[1])]
eltern = {}
for n in nummern:
    teile = n.rstrip(".").split(".")
    if len(teile) >= 2:
        eltern.setdefault(".".join(teile[:-1]), []).append(n)
einzelkinder = [k for k, v in eltern.items() if len(v) == 1]
pruefe(not einzelkinder,
       "Gliederungslogik: kein Abschnitt steht allein auf seiner Ebene"
       + ("" if not einzelkinder else " - allein: " + ", ".join(einzelkinder)),
       "Leitfaden: kein 1.1 ohne 1.2")

schriften = set()
for s in d:
    for f in s.get_fonts(full=True):
        schriften.add((f[3], f[1] != "n/a"))
pruefe(all(e for _, e in schriften),
       "alle Schriften eingebettet (%d)" % len(schriften), "Druckfähigkeit")

# Dezimaltrennzeichen sprachrichtig
sprache = feld("sprache")
if sprache == "de":
    # DOI, URL und Gliederungsnummern zuvor entfernen - dort ist der Punkt
    # kein Dezimaltrennzeichen.
    text = re.sub(r"10\.\d{4,9}/\S+", " ", volltext)       # DOI
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)       # URL
    text = re.sub(r"(?m)^\s*\d+(\.\d+)*\.?\s", " ", text)  # Gliederungsnummern
    treffer = re.findall(r"(?<![\w./])\d+\.\d+(?![\w./])", text)
    treffer = [t for t in treffer if not re.match(r"^[1-9]\.\d{1,2}$", t)]
    pruefe(len(treffer) == 0,
           "Dezimaltrennzeichen deutsch (Komma)"
           + ("" if not treffer else " - Punkt gefunden bei: " + ", ".join(sorted(set(treffer))[:6])),
           "Leitfaden: deutsch 1,0 / englisch 1.0", hart=False)

# ── Ausgabe ──────────────────────────────────────────────────────────────
fehler = 0
for ok, text, q, hart in befunde:
    marke = "OK" if ok else ("!!" if hart else " ?")
    if not ok and hart:
        fehler += 1
    print("  [%s] %-62s %s" % (marke, text, q))

print("""
Nicht maschinell prüfbar - bleibt menschliche Aufgabe:
  - Lückenlosigkeit und Aktualität des Lebenslaufs (Lücken über 2-3 Monate
    müssen benannt sein)
  - Lesbarkeit der Schrift IN den Abbildungen beim A5-Druck, beschriftete
    Achsen, keine unscharfen Abbildungen
  - Quellenangabe für alle übernommenen Abbildungen
  - Vollständigkeit und Einheitlichkeit des Literaturverzeichnisses:
    keine Insider-Kürzel, Autorenlisten ungekürzt (kein "et al."),
    DOI entweder überall oder nirgends, Online-Quellen mit Abrufdatum
  - Kennzeichnung von Textrecycling, Hinweis im Vorwort
  - Dauerhafte Verfügbarkeit verlinkter Materialien
  - Digitale Vorprüfung beim Prüfungsamt VOR dem Druck (neu seit 08/2026)""")

print("\nErgebnis: %s" % ("alle prüfbaren Punkte erfüllt" if fehler == 0
                          else "%d Punkt(e) nicht erfüllt" % fehler))
sys.exit(0 if fehler == 0 else 1)
