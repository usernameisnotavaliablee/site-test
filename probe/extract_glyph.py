"""Extract stroke centerlines of one glyph from MacintoshSkeletalVariable.otf (same method as test-animation/build.py).

usage: /Users/mac/Desktop/site/probe/.venv/bin/python -I probe/extract_glyph.py questionmark [KEEP]
Output JSON: {"glyph", "paths": [svg d...], "advance", "width"}; font units, y flipped for SVG, contour order kept.
KEEP: keep only the first KEEP cubic segments of the first stroke. The cursive glyphs end in an exit stroke
meant to join the next letter; questionmark uses 55 to drop the tail that curls up to the right.
"""
import sys, json, math
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

FONT = "/Users/mac/Documents/test-animation/MacintoshSkeletalVariable.otf"
GLYPH = sys.argv[1] if len(sys.argv) > 1 else "questionmark"
f = TTFont(FONT)

def contours(g, w):
    p = RecordingPen(); f.getGlyphSet(location={"wght": w})[g].draw(p)
    cs = []
    for op, a in p.value:
        if op == "moveTo": cs.append([a[0]])
        elif op == "lineTo": cs[-1] += [cs[-1][-1], a[0], a[0]]
        elif op == "curveTo": cs[-1] += list(a)
    return cs

def width(w):
    ys = [p[1] for p in contours("t", w)[1]]
    return max(ys) - min(ys)

W100, W500 = width(100), width(500)
T0 = -W100 / (W500 - W100)

def seglen(p0, c1, c2, p3, n=16):
    pts = [tuple((1-s)**3*a + 3*(1-s)**2*s*b + 3*(1-s)*s*s*c + s**3*d
                 for a, b, c, d in zip(p0, c1, c2, p3)) for s in (i / n for i in range(n + 1))]
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(n))

def centerline(pts):
    segs = [pts[i:i + 4] for i in range(0, len(pts) - 1, 3)]
    lens = [seglen(*s) for s in segs]
    acc, cut, best = 0, 0, 1e9
    for i, L in enumerate(lens):
        acc += L
        if abs(acc - sum(lens) / 2) < best: best, cut = abs(acc - sum(lens) / 2), i
    keep = cut + 1
    while keep > 1 and lens[keep - 1] < 1: keep -= 1
    return pts[:keep * 3 + 1]

strokes = []
for a, b in zip(contours(GLYPH, 100), contours(GLYPH, 500)):
    sk = [(p[0] + (q[0] - p[0]) * T0, p[1] + (q[1] - p[1]) * T0) for p, q in zip(a, b)]
    strokes.append(centerline(sk))

if len(sys.argv) > 2:
    strokes[0] = strokes[0][:int(sys.argv[2]) * 3 + 1]

def d(s):
    r = lambda p: f"{p[0]:.0f} {-p[1]:.0f}"
    return f"M{r(s[0])}" + "".join("C" + " ".join(r(p) for p in s[i:i + 3]) for i in range(1, len(s), 3))

print(json.dumps({"glyph": GLYPH, "paths": [d(s) for s in strokes], "advance": f["hmtx"][GLYPH][0], "width": round(W500)}))
