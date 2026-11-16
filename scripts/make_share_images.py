"""Make the link-preview image (og-image.jpg) and app icons in Book Club's look:
claret ditsy-floral wallpaper, a paper card with a double rule, an italic Garamond masthead,
botanical sprigs and a wax seal (the site's default look, see js/look.js).
Run: python scripts/make_share_images.py   (needs Pillow; uses Windows' Garamond + Verdana)"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
F = "C:/Windows/Fonts/"
GARA_I, GARA, VERDANA, SYM = F + "GARAIT.TTF", F + "GARA.TTF", F + "verdana.ttf", F + "seguisym.ttf"

# the "Claret" colorway
GROUND, MOTIF, SOFT, ACCENT, PAPER, INK, MUTED = (239, 230, 216), (142, 37, 52), (125, 138, 99), (122, 29, 43), (255, 251, 244), (43, 35, 32), (131, 118, 106)
K = 2  # draw at 2x, shrink at the end for smooth edges


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def flower(d, cx, cy, r, petal, middle):
    for k in range(5):
        a = math.radians(k * 72 - 90)
        px, py, pr = cx + math.cos(a) * r, cy + math.sin(a) * r, r * 0.78
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=petal)
    m = r * 0.5
    d.ellipse([cx - m, cy - m, cx + m, cy + m], fill=middle)


def leaf_poly(x, y, length, width, angle):
    """An almond-shaped leaf starting at (x, y), pointing along angle (degrees)."""
    a = math.radians(angle)
    pts = []
    for i in range(21):
        t = i / 20
        pts.append((t * length, math.sin(t * math.pi) * width))
    pts += [(t, -w) for t, w in reversed(pts)]
    return [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]


def wallpaper(w, h):
    """The ditsy floral from js/look.js, at 50% strength on the linen ground."""
    tile = 128 * K
    im = Image.new("RGB", (w, h), GROUND)
    d = ImageDraw.Draw(im)
    m, s, = mix(GROUND, MOTIF, 0.5), mix(GROUND, SOFT, 0.5)
    for oy in range(0, h + tile, tile):
        for ox in range(0, w + tile, tile):
            def X(v): return ox + v * K
            def Y(v): return oy + v * K
            for (lx, ly, rot) in [(30, 33, 40), (15, 34, -30 + 180), (95, 82, 120), (86, 93, 20), (50, 112, -60)]:
                d.polygon(leaf_poly(X(lx) - 3.6 * K * math.cos(math.radians(rot)), Y(ly) - 3.6 * K * math.sin(math.radians(rot)), 7.2 * K, 1.5 * K, rot), fill=s)
            flower(d, X(23), Y(26), 3.5 * K, m, GROUND)
            flower(d, X(90), Y(76), 3.5 * K, m, GROUND)
            flower(d, X(44), Y(106), 2.6 * K, m, GROUND)
            for (fx, fy) in [(96, 20), (18, 86), (62, 56)]:
                flower(d, X(fx), Y(fy), 2.1 * K, s, GROUND)
            for (dx, dy) in [(64, 14), (118, 50), (34, 64), (112, 112)]:
                d.ellipse([X(dx) - K, Y(dy) - K, X(dx) + K, Y(dy) + K], fill=m)
    return im


def spaced(d, xy, text, font, fill, spacing, anchor="l"):
    """Letter-spaced small caps, like the site's labels."""
    widths = [d.textlength(c, font=font) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x, y = xy
    if anchor == "m": x -= total / 2
    if anchor == "r": x -= total
    for c, wd in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill)
        x += wd + spacing


def sprig(d, x, y, s, flip=False):
    """A botanical sprig (stem, leaves, buds) like the masthead's, s = height."""
    def P(px, py):
        px = 70 - px if flip else px
        return (x + px / 110 * s, y + py / 110 * s)
    def bez(p0, p1, p2, p3):  # the same two curves as the masthead's SVG stem
        return [tuple((1 - t) ** 3 * p0[i] + 3 * (1 - t) ** 2 * t * p1[i] + 3 * (1 - t) * t * t * p2[i] + t ** 3 * p3[i] for i in (0, 1)) for t in [j / 20 for j in range(21)]]
    stem = [P(*q) for q in bez((40, 108), (37, 84), (33, 58), (40, 30)) + bez((40, 30), (43, 18), (48, 9), (55, 2))]
    d.line(stem, fill=SOFT, width=max(2, round(s / 70)))
    d.line([P(36, 64), P(28, 58), P(22, 50), P(20, 40)], fill=SOFT, width=max(2, round(s / 80)))
    for (lx, ly, rot, ln) in [(38, 94, -160, 15), (37, 82, -28, 15), (35, 70, -150, 13), (35, 55, -36, 13), (37, 43, -138, 11), (25, 52, -118, 9)]:
        px, py = P(lx, ly)
        ang = (180 - rot) if flip else rot
        d.polygon(leaf_poly(px, py, ln / 110 * s, 3 / 110 * s, ang), fill=SOFT)
    for (bx, by, r) in [(43, 25, 2.6), (48.5, 17, 2.4), (45, 15, 2.1), (52.5, 9.5, 2.2), (50, 7, 1.8), (55.5, 2.5, 1.5), (19.5, 38.5, 1.9), (22.8, 37.2, 1.5), (18.2, 35, 1.4)]:
        cx, cy = P(bx, by)
        rr = r / 110 * s
        d.ellipse([cx - rr * .8, cy - rr * 1.2, cx + rr * .8, cy + rr * 1.2], fill=ACCENT)


def seal(size, letters="BC"):
    """The club's wax seal: a slightly lumpy claret disc, a pressed ring and the monogram."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, R = size / 2, size * 0.47
    pts = [(c + math.cos(a) * R * (1 + 0.025 * math.sin(a * 5) + 0.015 * math.sin(a * 9 + 1)),
            c + math.sin(a) * R * (1 + 0.025 * math.sin(a * 5) + 0.015 * math.sin(a * 9 + 1))) for a in [i / 120 * math.tau for i in range(120)]]
    d.polygon(pts, fill=ACCENT)
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([size * .18, size * .12, size * .6, size * .5], fill=(255, 255, 255, 60))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    im.alpha_composite(Image.composite(glow.filter(ImageFilter.GaussianBlur(size / 14)), Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask))
    r2 = R * 0.8
    d.ellipse([c - r2, c - r2, c + r2, c + r2], outline=mix(ACCENT, (255, 255, 255), .3), width=max(1, size // 70))
    font = ImageFont.truetype(GARA_I, int(size * 0.42))
    d.text((c, c + size * 0.02), letters, font=font, fill=mix(PAPER, ACCENT, .12), anchor="mm")
    return im


def og():
    W, H = 1200 * K, 630 * K
    out = wallpaper(W, H).convert("RGBA")
    cw, ch = 1010 * K, 482 * K
    x0, y0 = (W - cw) // 2, (H - ch) // 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([x0 + 4 * K, y0 + 14 * K, x0 + cw - 4 * K, y0 + ch + 10 * K], fill=(40, 15, 10, 90))
    out = Image.alpha_composite(out, shadow.filter(ImageFilter.GaussianBlur(18 * K)))
    d = ImageDraw.Draw(out)
    d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=PAPER)
    # the double rule (thin, thick, thin), like the site's default frame
    for inset, t in [(1, 1), (4, 3), (9, 1)]:
        d.rectangle([x0 + inset * K * 2, y0 + inset * K * 2, x0 + cw - inset * K * 2, y0 + ch - inset * K * 2], outline=ACCENT, width=t * K)
    small = ImageFont.truetype(VERDANA, 13 * K)
    top = y0 + 48 * K
    spaced(d, (x0 + 62 * K, top), "A SMALL READING SOCIETY", small, MUTED, 3.2 * K)
    spaced(d, (x0 + cw - 62 * K, top), "EST. MMXXVI", small, MUTED, 3.2 * K, "r")
    d.text((x0 + cw / 2, top + 7 * K), "Vol. I", font=ImageFont.truetype(GARA_I, 24 * K), fill=ACCENT, anchor="mm")
    d.line([x0 + 60 * K, top + 30 * K, x0 + cw - 60 * K, top + 30 * K], fill=mix(PAPER, INK, .3), width=K)
    logo = ImageFont.truetype(GARA_I, 172 * K)
    ly = y0 + 196 * K
    d.text((x0 + cw / 2, ly), "Book Club", font=logo, fill=ACCENT, anchor="mm")
    lw = d.textlength("Book Club", font=logo)
    sprig(d, x0 + cw / 2 - lw / 2 - 118 * K, ly - 74 * K, 140 * K)
    sprig(d, x0 + cw / 2 + lw / 2 + 30 * K, ly - 74 * K, 140 * K, flip=True)
    tag_f, star_f = ImageFont.truetype(GARA_I, 36 * K), ImageFont.truetype(SYM, 22 * K)
    tag = "like game club but for books"
    ty, tw = y0 + 318 * K, d.textlength(tag, font=tag_f)
    d.text((x0 + cw / 2, ty), tag, font=tag_f, fill=mix(ACCENT, INK, .2), anchor="mm")
    for sx in (x0 + cw / 2 - tw / 2 - 30 * K, x0 + cw / 2 + tw / 2 + 30 * K):
        d.text((sx, ty + 2 * K), "★", font=star_f, fill=ACCENT, anchor="mm")
    ry = y0 + 384 * K
    for dy in (-3, 3):
        d.line([x0 + 60 * K, ry + dy * K, x0 + cw - 60 * K, ry + dy * K], fill=mix(PAPER, ACCENT, .75), width=K)
    sz = 66 * K
    d.ellipse([x0 + cw / 2 - sz / 2 - 8 * K, ry - sz / 2 - 8 * K, x0 + cw / 2 + sz / 2 + 8 * K, ry + sz / 2 + 8 * K], fill=PAPER)
    out.alpha_composite(seal(sz), (int(x0 + cw / 2 - sz / 2), int(ry - sz / 2)))
    spaced(d, (x0 + cw / 2, y0 + ch - 58 * K), "PICK A BOOK  ·  VOTE WITH THREE BOOKMARKS  ·  CHAT  ·  READ", small, INK, 3 * K, "m")
    out.convert("RGB").resize((1200, 630), Image.LANCZOS).save(IMG / "og-image.jpg", quality=88, optimize=True, progressive=True)


def icon(size, path):
    s = 512
    base = Image.new("RGBA", (s, s), PAPER + (255,))
    d = ImageDraw.Draw(base)
    for inset, t in [(18, 3), (30, 8), (46, 3)]:
        d.rectangle([inset, inset, s - inset, s - inset], outline=ACCENT, width=t)
    sz = 360
    base.alpha_composite(seal(sz), ((s - sz) // 2, (s - sz) // 2))
    if size <= 48:  # tiny favicon: just the seal, as big as it can be
        base = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        base.alpha_composite(seal(s), (0, 0))
    base.resize((size, size), Image.LANCZOS).save(path, optimize=True)


if __name__ == "__main__":
    IMG.mkdir(exist_ok=True)
    og()
    icon(180, IMG / "apple-touch-icon.png")
    icon(192, IMG / "icon-192.png")
    icon(512, IMG / "icon-512.png")
    icon(32, IMG / "favicon-32.png")
    print("made og-image.jpg + icons in img/")
