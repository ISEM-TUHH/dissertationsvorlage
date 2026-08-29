# -*- coding: utf-8 -*-
"""Vollstaendiger SVG-Path-Parser -> Liste von Subpfaden.

Jeder Subpfad ist eine Liste von Segmenten:
    ('M', (x, y))
    ('L', (x, y))
    ('C', (c1x, c1y), (c2x, c2y), (x, y))
    ('Z',)
Arcs (A/a) werden in kubische Beziers zerlegt.
"""
import re
import math

_TOK = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")


def _nums(tokens, i, n):
    vals = []
    while len(vals) < n:
        vals.append(float(tokens[i]))
        i += 1
    return vals, i


def _arc_to_cubics(x0, y0, rx, ry, phi, large, sweep, x1, y1):
    """SVG-Arc -> Folge kubischer Beziers (Implementation Notes F.6)."""
    if rx == 0 or ry == 0:
        return [('C', (x0, y0), (x1, y1), (x1, y1))]
    phi = math.radians(phi)
    cosp, sinp = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x0 - x1) / 2.0, (y0 - y1) / 2.0
    x1p = cosp * dx2 + sinp * dy2
    y1p = -sinp * dx2 + cosp * dy2
    rx, ry = abs(rx), abs(ry)
    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1:
        s = math.sqrt(lam)
        rx, ry = rx * s, ry * s
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large == sweep:
        co = -co
    cxp = co * rx * y1p / ry
    cyp = -co * ry * x1p / rx
    cx = cosp * cxp - sinp * cyp + (x0 + x1) / 2.0
    cy = sinp * cxp + cosp * cyp + (y0 + y1) / 2.0

    def ang(ux, uy, vx, vy):
        d = math.sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
        c = max(-1.0, min(1.0, (ux * vx + uy * vy) / d)) if d else 1.0
        a = math.acos(c)
        return -a if ux * vy - uy * vx < 0 else a

    th1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dth = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dth > 0:
        dth -= 2 * math.pi
    elif sweep and dth < 0:
        dth += 2 * math.pi

    segs = []
    n = max(1, int(math.ceil(abs(dth) / (math.pi / 2))))
    delta = dth / n
    t = 4.0 / 3.0 * math.tan(delta / 4.0)
    th = th1
    px, py = x0, y0
    for _ in range(n):
        c1, s1 = math.cos(th), math.sin(th)
        th2 = th + delta
        c2, s2 = math.cos(th2), math.sin(th2)

        def pt(c, s):
            return (cosp * rx * c - sinp * ry * s + cx, sinp * rx * c + cosp * ry * s + cy)

        e = pt(c2, s2)
        d1 = (cosp * (-rx * s1) - sinp * (ry * c1), sinp * (-rx * s1) + cosp * (ry * c1))
        d2 = (cosp * (-rx * s2) - sinp * (ry * c2), sinp * (-rx * s2) + cosp * (ry * c2))
        segs.append(('C', (px + t * d1[0], py + t * d1[1]),
                     (e[0] - t * d2[0], e[1] - t * d2[1]), e))
        px, py = e
        th = th2
    return segs


def parse(d):
    tokens = _TOK.findall(d)
    i, n = 0, len(tokens)
    subpaths, cur = [], []
    x = y = sx = sy = 0.0
    prev_c = None   # letzter Bezier-Kontrollpunkt (fuer S/T)
    prev_q = None
    cmd = None
    while i < n:
        t = tokens[i]
        if re.match(r"[A-Za-z]", t):
            cmd = t
            i += 1
            if cmd in "Zz":
                if cur:
                    cur.append(('Z',))
                    subpaths.append(cur)
                    cur = []
                x, y = sx, sy
                continue
        elif cmd is None:
            raise ValueError("Pfad beginnt ohne Kommando: %r" % d[:40])
        elif cmd == 'M':
            cmd = 'L'
        elif cmd == 'm':
            cmd = 'l'

        rel = cmd.islower()
        c = cmd.upper()
        if c == 'M':
            (a, b), i = _nums(tokens, i, 2)
            x, y = (x + a, y + b) if rel else (a, b)
            if cur:
                subpaths.append(cur)
            cur = [('M', (x, y))]
            sx, sy = x, y
            prev_c = prev_q = None
        elif c == 'L':
            (a, b), i = _nums(tokens, i, 2)
            x, y = (x + a, y + b) if rel else (a, b)
            cur.append(('L', (x, y)))
            prev_c = prev_q = None
        elif c == 'H':
            (a,), i = _nums(tokens, i, 1)
            x = x + a if rel else a
            cur.append(('L', (x, y)))
            prev_c = prev_q = None
        elif c == 'V':
            (a,), i = _nums(tokens, i, 1)
            y = y + a if rel else a
            cur.append(('L', (x, y)))
            prev_c = prev_q = None
        elif c == 'C':
            v, i = _nums(tokens, i, 6)
            if rel:
                p1 = (x + v[0], y + v[1]); p2 = (x + v[2], y + v[3]); p3 = (x + v[4], y + v[5])
            else:
                p1 = (v[0], v[1]); p2 = (v[2], v[3]); p3 = (v[4], v[5])
            cur.append(('C', p1, p2, p3))
            prev_c, prev_q = p2, None
            x, y = p3
        elif c == 'S':
            v, i = _nums(tokens, i, 4)
            if rel:
                p2 = (x + v[0], y + v[1]); p3 = (x + v[2], y + v[3])
            else:
                p2 = (v[0], v[1]); p3 = (v[2], v[3])
            p1 = (2 * x - prev_c[0], 2 * y - prev_c[1]) if prev_c else (x, y)
            cur.append(('C', p1, p2, p3))
            prev_c, prev_q = p2, None
            x, y = p3
        elif c in 'QT':
            if c == 'Q':
                v, i = _nums(tokens, i, 4)
                q = (x + v[0], y + v[1]) if rel else (v[0], v[1])
                p3 = (x + v[2], y + v[3]) if rel else (v[2], v[3])
            else:
                v, i = _nums(tokens, i, 2)
                q = (2 * x - prev_q[0], 2 * y - prev_q[1]) if prev_q else (x, y)
                p3 = (x + v[0], y + v[1]) if rel else (v[0], v[1])
            p1 = (x + 2.0 / 3 * (q[0] - x), y + 2.0 / 3 * (q[1] - y))
            p2 = (p3[0] + 2.0 / 3 * (q[0] - p3[0]), p3[1] + 2.0 / 3 * (q[1] - p3[1]))
            cur.append(('C', p1, p2, p3))
            prev_q, prev_c = q, p2
            x, y = p3
        elif c == 'A':
            v, i = _nums(tokens, i, 7)
            p3 = (x + v[5], y + v[6]) if rel else (v[5], v[6])
            cur.extend(_arc_to_cubics(x, y, v[0], v[1], v[2], int(v[3]), int(v[4]), p3[0], p3[1]))
            x, y = p3
            prev_c = prev_q = None
        else:
            raise ValueError("unbekanntes Kommando %r" % cmd)
    if cur:
        subpaths.append(cur)
    return subpaths
