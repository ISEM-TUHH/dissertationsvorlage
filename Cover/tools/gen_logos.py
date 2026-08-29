# -*- coding: utf-8 -*-
"""Erzeugt src/logos.typ: Logos als echte Typst-Vektorpfade mit CMYK-Farben.

    python tools/gen_logos.py          (aus dem Ordner Cover/ heraus)

Quellen:
  ISEM : assets/isem-logo.svg          (Druckfreigabe, Illustrator-Export)
  TUHH : assets/entwurf-original.pdf   (Vektorpfade aus dem Originallayout)
         -> sobald das TUHH-SVG vorliegt, TUHH_SVG unten setzen; dann wird
            derselbe SVG-Weg wie fuer ISEM benutzt.

Warum nicht image("logo.svg")? SVG kennt nur RGB. Ein importiertes SVG landet
als DeviceRGB im PDF. Durch die Umwandlung in Typst-curve() mit Farben aus
farben.typ bleibt die Druckdatei durchgaengig CMYK.
"""
import io
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
sys.path.insert(0, HIER)
import svgpath  # noqa: E402

ISEM_SVG = os.path.join(BASIS, "assets", "isem-logo.svg")
TUHH_SVG = None  # <- Pfad zum TUHH-SVG eintragen, sobald vorhanden
ENTWURF = os.path.join(BASIS, "assets", "entwurf-original.pdf")
TUHH_PFADE = [11, 12, 13, 14]  # Indizes der TUHH-Buchstaben im Entwurf
OUT = os.path.join(BASIS, "src", "logos.typ")

# Fuellfarbe der Quelle -> Farbname aus farben.typ
FARBEN = {
    "#1cb9d9": "isem-cyan",
    "#2bb9ce": "isem-cyan2",
    "#7c93ad": "isem-grau",
    "#00c1d4": "tuhh-cyan",
}


def _bezier_bbox(p0, p1, p2, p3):
    """Exakte Bounding-Box einer kubischen Bezierkurve (Extrema der Ableitung)."""
    xs, ys = [p0[0], p3[0]], [p0[1], p3[1]]
    for k in (0, 1):
        a = -p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]
        b = 2 * (p0[k] - 2 * p1[k] + p2[k])
        c = -p0[k] + p1[k]
        ts = []
        if abs(a) < 1e-12:
            if abs(b) > 1e-12:
                ts.append(-c / b)
        else:
            disc = b * b - 4 * a * c
            if disc >= 0:
                r = disc ** 0.5
                ts += [(-b + r) / (2 * a), (-b - r) / (2 * a)]
        for t in ts:
            if 0 < t < 1:
                u = 1 - t
                v = (u ** 3 * p0[k] + 3 * u * u * t * p1[k]
                     + 3 * u * t * t * p2[k] + t ** 3 * p3[k])
                (xs if k == 0 else ys).append(v)
    return min(xs), min(ys), max(xs), max(ys)


def ink_bbox(formen):
    """Bounding-Box aller gezeichneten Pfade (ohne viewBox-Weissraum)."""
    x0 = y0 = float("inf")
    x1 = y1 = float("-inf")
    for _f, _s, _w, subs in formen:
        for sub in subs:
            cur = None
            for seg in sub:
                if seg[0] in ("M", "L"):
                    pts = [seg[1]]
                    cur = seg[1]
                elif seg[0] == "C":
                    bx = _bezier_bbox(cur, seg[1], seg[2], seg[3])
                    pts = [(bx[0], bx[1]), (bx[2], bx[3])]
                    cur = seg[3]
                else:
                    continue
                for px, py in pts:
                    x0, y0 = min(x0, px), min(y0, py)
                    x1, y1 = max(x1, px), max(y1, py)
    return x0, y0, x1, y1


def svg_klassen(text):
    """CSS-Klassen aus dem <style>-Block: .stN { fill: #xxxxxx; stroke: ... }"""
    out = {}
    for m in re.finditer(r"\.(st\d+)\s*\{([^}]*)\}", text):
        body = m.group(2)
        f = re.search(r"fill:\s*([^;\s]+)", body)
        s = re.search(r"stroke:\s*([^;\s]+)", body)
        w = re.search(r"stroke-width:\s*([\d.]+)", body)
        out[m.group(1)] = {
            "fill": f.group(1).lower() if f else None,
            "stroke": s.group(1).lower() if s else None,
            "stroke_width": float(w.group(1)) if w else 1.0,
        }
    return out


def lies_svg(pfad):
    """-> [(fill, stroke, stroke_width, subpaths), ...]"""
    text = io.open(pfad, encoding="utf-8").read()
    klassen = svg_klassen(text)
    formen = []
    for m in re.finditer(r"<path\b([^>]*)>", text):
        attrs = m.group(1)
        d = re.search(r'\sd="([^"]+)"', attrs)
        if not d:
            continue
        kl = re.search(r'class="([^"]+)"', attrs)
        stil = klassen.get(kl.group(1).strip(), {}) if kl else {}
        f = re.search(r'fill="([^"]+)"', attrs)
        fill = (f.group(1) if f else stil.get("fill") or "#000000").lower()
        st = re.search(r'stroke="([^"]+)"', attrs)
        stroke = (st.group(1) if st else stil.get("stroke") or "none").lower()
        formen.append((fill, stroke, stil.get("stroke_width", 1.0), svgpath.parse(d.group(1))))
    return formen


def lies_tuhh_aus_pdf():
    """TUHH-Buchstaben aus dem Originalentwurf, im selben Format wie lies_svg()."""
    import fitz
    dr = fitz.open(ENTWURF)[0].get_drawings()
    formen = []
    for p in (dr[i] for i in TUHH_PFADE):
        subs, cur, last = [], [], None
        for it in p["items"]:
            if it[0] == "l":
                a, b = it[1], it[2]
                if last is None or abs(last.x - a.x) > 1e-6 or abs(last.y - a.y) > 1e-6:
                    if cur:
                        cur.append(("Z",)); subs.append(cur)
                    cur = [("M", (a.x, a.y))]
                cur.append(("L", (b.x, b.y)))
                last = b
            elif it[0] == "c":
                a, c1, c2, b = it[1], it[2], it[3], it[4]
                if last is None or abs(last.x - a.x) > 1e-6 or abs(last.y - a.y) > 1e-6:
                    if cur:
                        cur.append(("Z",)); subs.append(cur)
                    cur = [("M", (a.x, a.y))]
                cur.append(("C", (c1.x, c1.y), (c2.x, c2.y), (b.x, b.y)))
                last = b
        if cur:
            cur.append(("Z",)); subs.append(cur)
        formen.append(("#00c1d4", "none", 0.0, subs))
    return formen


def typst_logo(name, formen):
    """Rendert eine Typst-Funktion <name>-logo(height: ..).

    Bezugsrahmen ist die Ink-Bounding-Box, nicht die viewBox: nur so trifft das
    Logo im Layout exakt die Flaeche, die es im Originalentwurf einnimmt.
    """
    bx0, by0, bx1, by1 = ink_bbox(formen)
    vw, vh = bx1 - bx0, by1 - by0

    def P(p):
        return "(%.5f * s, %.5f * s)" % ((p[0] - bx0) / vh, (p[1] - by0) / vh)

    z = ["// %s-Logo - Vektorpfade, Fuellung aus farben.typ." % name.upper(),
         "#let %s-ratio = %.5f" % (name, vw / vh),
         "#let %s-logo(height: 10mm) = {" % name,
         "  let s = height",
         "  box(width: %s-ratio * height, height: height, {" % name]
    for fill, stroke, sw, subs in formen:
        cname = FARBEN.get(fill)
        if cname is None:
            raise SystemExit("Unbekannte Farbe %s in %s - in FARBEN ergaenzen." % (fill, name))
        args = ["fill: %s" % cname]
        if stroke not in (None, "none"):
            col = "weiss" if stroke in ("#fff", "#ffffff", "white") else FARBEN.get(stroke, "weiss")
            args.append("stroke: %.5f * s + %s" % (sw / vh, col))
        z.append("    place(top + left, curve(%s," % ", ".join(args))
        for sub in subs:
            for seg in sub:
                if seg[0] == "M":
                    z.append("      curve.move(%s)," % P(seg[1]))
                elif seg[0] == "L":
                    z.append("      curve.line(%s)," % P(seg[1]))
                elif seg[0] == "C":
                    z.append("      curve.cubic(%s, %s, %s)," % (P(seg[1]), P(seg[2]), P(seg[3])))
                elif seg[0] == "Z":
                    z.append("      curve.close(),")
            if sub and sub[-1][0] != "Z":
                z.append("      curve.close(),")
        z.append("    ))")
    z += ["  })", "}", ""]
    return z


def main():
    zeilen = ["// AUTOMATISCH GENERIERT von tools/gen_logos.py - nicht von Hand aendern.",
              '#import "farben.typ": *', ""]
    zeilen += typst_logo("tuhh", lies_svg(TUHH_SVG) if TUHH_SVG else lies_tuhh_aus_pdf())
    zeilen += typst_logo("isem", lies_svg(ISEM_SVG))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(zeilen))
    print("geschrieben:", OUT)


main()
