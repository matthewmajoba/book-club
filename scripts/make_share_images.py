"""Make the link-preview image (og-image.jpg) and app icons in Book Club's granny-square look:
the real granny-square afghan photo as wallpaper, a cream card crocheted round and round, the name in
chunky '70s type with stacked yarn-colored shadows, and grandma's WIP polaroid (the site's default
look, see js/look.js). The icons are a granny square.
Run: python scripts/make_wallpapers.py first, then python scripts/make_share_images.py
(needs Pillow; uses Windows' Cooper Black + Segoe UI Bold)"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
F = "C:/Windows/Fonts/"
COOPER, SEGOE_B, SYM = F + "COOPBL.TTF", F + "segoeuib.ttf", F + "seguisym.ttf"

# the "Rainbow scraps" yarn
ACCENT, EDGE, PAPER, INK = (214, 51, 108), (27, 27, 27), (255, 250, 240), (38, 32, 28)
R1, R2, R3 = (232, 89, 12), (252, 196, 25), (16, 152, 173)
K = 2  # draw at 2x, shrink at the end for smooth edges


def rounds(d, box, rings):
    """Nested rectangles, outside in: rings = [(color, width), ...]"""
    x0, y0, x1, y1 = box
    for col, w in rings:
        d.rectangle([x0, y0, x1, y1], fill=col)
        x0, y0, x1, y1 = x0 + w, y0 + w, x1 - w, y1 - w
    return x0, y0, x1, y1


def spaced(d, xy, text, font, fill, spacing):
    """Centered text with letter spacing."""
    widths = [d.textlength(ch, font=font) for ch in text]
    x = xy[0] - (sum(widths) + spacing * (len(text) - 1)) / 2
    for ch, w in zip(text, widths):
        d.text((x, xy[1]), ch, font=font, fill=fill, anchor="lm")
        x += w + spacing


def og():
    W, H = 1200 * K, 630 * K
    out = Image.new("RGBA", (W, H))
    tile = Image.open(IMG / "wall" / "granny.jpg").convert("RGBA")
    tile = tile.resize((300 * K, round(300 * K * tile.height / tile.width)), Image.LANCZOS)
    for y in range(0, H, tile.height):
        for x in range(0, W, tile.width):
            out.paste(tile, (x, y))
    # the card, with a soft shadow under it
    box = (110 * K, 92 * K, 1090 * K, 548 * K)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([box[0] + 8 * K, box[1] + 22 * K, box[2] + 8 * K, box[3] + 26 * K], fill=(0, 0, 0, 150))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18 * K)))
    d = ImageDraw.Draw(out)
    rounds(d, box, [(EDGE, 9 * K), (R3, 8 * K), (R2, 8 * K), (R1, 8 * K), (PAPER, 0)])
    cx = (box[0] + box[2]) // 2
    spaced(d, (cx, 175 * K), "MADE WITH LOVE BY", ImageFont.truetype(SEGOE_B, 19 * K), (95, 88, 82), 6 * K)
    big = ImageFont.truetype(COOPER, 150 * K)
    for off, col in [(15, EDGE), (10, R3), (5, R2), (0, ACCENT)]:
        d.text((cx + off * K - 8 * K, 300 * K + off * K), "Book Club", font=big, fill=col, anchor="mm")
    tf, sf = ImageFont.truetype(SEGOE_B, 30 * K), ImageFont.truetype(SYM, 26 * K)
    tag, gap = "like game club but for books", 18 * K
    tw = d.textlength(tag, font=tf)
    d.text((cx, 452 * K), tag, font=tf, fill=INK, anchor="mm")
    for x in (cx - tw / 2 - gap, cx + tw / 2 + gap):  # Segoe UI has no star, so they come from Segoe UI Symbol
        d.text((x, 454 * K), "\u2605", font=sf, fill=INK, anchor="mm")
    # grandma's WIP polaroid, taped to the corner
    ph = Image.open(IMG / "grandmas-wip.jpg").convert("RGBA")
    pw = 210 * K
    ph = ph.resize((pw, round(pw * ph.height / ph.width)), Image.LANCZOS)
    pol = Image.new("RGBA", (pw + 20 * K, ph.height + 52 * K), (255, 255, 255, 255))
    pol.paste(ph, (10 * K, 10 * K))
    ImageDraw.Draw(pol).text((pol.width // 2, ph.height + 32 * K), "Grandma's WIP", font=ImageFont.truetype(COOPER, 19 * K), fill=(70, 70, 70), anchor="mm")
    pol = pol.rotate(-8, resample=Image.BICUBIC, expand=True)
    psh = Image.new("RGBA", pol.size, (0, 0, 0, 0))
    psh.putalpha(pol.getchannel("A").point(lambda a: a * 0.55))
    at = (box[2] - pol.width + 70 * K, box[1] - 70 * K)
    out.alpha_composite(psh.filter(ImageFilter.GaussianBlur(9 * K)), (at[0] + 4 * K, at[1] + 14 * K))
    out.alpha_composite(pol, at)
    out.convert("RGB").resize((1200, 630), Image.LANCZOS).save(IMG / "og-image.jpg", quality=88, optimize=True, progressive=True)


def granny_square(s, rings):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = rounds(d, (0, 0, s - 1, s - 1), rings)
    return im, (x0, y0, x1, y1), d


def icon(size, path):
    """A granny square: dark edge, three rounds, a pink middle."""
    s = 512
    edge = 48 if size <= 48 else 34
    im, _, d = granny_square(s, [(EDGE, edge), (R3, 54), (R2, 54), (R1, 54), (ACCENT, 0)])
    if size > 48:  # the dark chain stitch between rounds
        for inset in (edge + 54, edge + 108, edge + 162):
            d.rectangle([inset, inset, s - 1 - inset, s - 1 - inset], outline=(70, 45, 35, 255), width=4)
    im.resize((size, size), Image.LANCZOS).save(path, optimize=True)


if __name__ == "__main__":
    IMG.mkdir(exist_ok=True)
    og()
    icon(180, IMG / "apple-touch-icon.png")
    icon(192, IMG / "icon-192.png")
    icon(512, IMG / "icon-512.png")
    icon(32, IMG / "favicon-32.png")
    print("made og-image.jpg + icons in img/")
