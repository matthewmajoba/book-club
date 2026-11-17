"""Make the link-preview image (og-granny.jpg) and app icons in Book Club's granny-square look:
the real granny-square afghan photo as wallpaper, a cream card crocheted round and round, the name in
chunky '70s type with stacked yarn-colored shadows (the site's default
look, see js/look.js). The icons are a granny square.
Run: python scripts/make_wallpapers.py first, then python scripts/make_share_images.py
(needs Pillow; uses Windows' Cooper Black + Segoe UI Bold)"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
F = "C:/Windows/Fonts/"
COOPER, SEGOE_B = F + "COOPBL.TTF", F + "segoeuib.ttf"

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
    big = ImageFont.truetype(COOPER, 150 * K)
    for off, col in [(15, EDGE), (10, R3), (5, R2), (0, ACCENT)]:
        d.text((cx + off * K - 8 * K, 278 * K + off * K), "Book Club", font=big, fill=col, anchor="mm")
    d.text((cx, 432 * K), "like game club but for books", font=ImageFont.truetype(SEGOE_B, 32 * K), fill=INK, anchor="mm")
    img = out.convert("RGB").resize((1200, 630), Image.LANCZOS)
    # index.html points at og-granny.jpg; change that name whenever the picture changes, because
    # iMessage, Discord, Facebook etc. cache link previews by image address. og-image.jpg (the old
    # name) gets the same picture so anything still pointing there shows the new one too.
    for name in ("og-granny.jpg", "og-image.jpg"):
        img.save(IMG / name, quality=88, optimize=True, progressive=True)


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
    print("made og-granny.jpg + icons in img/")
