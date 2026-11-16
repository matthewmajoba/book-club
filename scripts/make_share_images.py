"""Make the link-preview image (og-image.jpg) and app icons in Book Club's cozy look.
Run: python scripts/make_share_images.py   (needs Pillow; uses Windows' Cooper Black + Verdana)
Everything is drawn here (plaid, wallpaper, fairy lights), no photos needed."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
COOPER = "C:/Windows/Fonts/COOPBL.TTF"
VERDANA_B = "C:/Windows/Fonts/verdanab.ttf"
SYM = "C:/Windows/Fonts/seguisym.ttf"


def vgrad(w, h, stops):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        p = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            (p0, c0), (p1, c1) = stops[i], stops[i + 1]
            if p0 <= p <= p1:
                k = (p - p0) / (p1 - p0 or 1)
                g.putpixel((0, y), tuple(int(c0[j] + (c1[j] - c0[j]) * k) for j in range(3)))
                break
    return g.resize((w, h))


def plaid(w, h, scale=1.0):
    """Red flannel: dark green bands + thin cream lines both ways, like the site's panel borders."""
    im = Image.new("RGBA", (w, h), (154, 42, 36, 255))
    over = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    step = int(30 * scale)
    for x in range(0, w + step, step):
        d.rectangle([x, 0, x + int(9 * scale), h], fill=(18, 44, 28, 120))
        d.rectangle([x + int(20 * scale), 0, x + int(21 * scale), h], fill=(255, 230, 190, 70))
    for y in range(0, h + step, step):
        d.rectangle([0, y, w, y + int(9 * scale)], fill=(18, 44, 28, 120))
        d.rectangle([0, y + int(20 * scale), w, y + int(21 * scale)], fill=(255, 230, 190, 70))
    return Image.alpha_composite(im, over)


def wallpaper(w, h):
    im = Image.new("RGB", (w, h), (43, 19, 22))
    d = ImageDraw.Draw(im)
    s = 64
    for y in range(0, h + s, s):
        for x in range(0, w + s, s):
            cx, cy = x + 32, y + 32
            for ang in range(4):
                a = ang * math.pi / 2
                px, py = cx + math.cos(a) * 9, cy + math.sin(a) * 9
                d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(67, 31, 34))
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(112, 74, 38))
        for x in range(0, w, 64):
            d.rectangle([x, 0, x + 1, h], fill=(36, 15, 18))
    return im


def wordart(text, size):
    """Warm gradient Cooper Black with a stacked brown 3D shadow and a lamp-light glow."""
    font = ImageFont.truetype(COOPER, size)
    l, t, r, b = font.getbbox(text)
    w, h = r - l + 70, b - t + 70
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((35 - l, 35 - t), text, font=font, fill=255)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow = Image.new("RGBA", (w, h), (255, 170, 60, 0))
    glow.putalpha(mask.filter(ImageFilter.GaussianBlur(18)).point(lambda a: int(a * 0.7)))
    layer = Image.alpha_composite(layer, glow)
    for i, col in [(8, (34, 12, 4)), (6, (62, 24, 10)), (4, (106, 42, 18)), (2, (140, 60, 26))]:
        sh = Image.new("RGBA", (w, h), col + (255,))
        a = Image.new("L", (w, h), 0); a.paste(mask, (i, i))
        sh.putalpha(a)
        layer = Image.alpha_composite(layer, sh)
    fill = vgrad(w, h, [(0, (255, 248, 226)), (.32, (255, 224, 160)), (.6, (244, 166, 74)), (.88, (192, 96, 42)), (1, (192, 96, 42))]).convert("RGBA")
    fill.putalpha(mask)
    edge = Image.new("RGBA", (w, h), (255, 243, 208, 255))
    edge.putalpha(mask.filter(ImageFilter.MaxFilter(3)))
    layer = Image.alpha_composite(layer, edge)
    return Image.alpha_composite(layer, fill)


def fairy_lights(img, y, amp, step, phase=0):
    """A drooping wire with warm and pink bulbs."""
    d = ImageDraw.Draw(img)
    w = img.width
    pts = [(x, y + amp * abs(math.sin((x + phase) / step * math.pi))) for x in range(0, w + 1, 4)]
    d.line(pts, fill=(26, 14, 8, 255), width=3)
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    bulbs = []
    for i, x in enumerate(range(step // 2 - phase % step, w, step)):
        by = y + amp * abs(math.sin((x + phase) / step * math.pi)) + 8
        col = (255, 196, 90) if i % 2 == 0 else (255, 140, 190)
        gd.ellipse([x - 16, by - 16, x + 16, by + 16], fill=col + (110,))
        bulbs.append((x, by, col))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(img)
    for x, by, col in bulbs:
        d.ellipse([x - 6, by - 7, x + 6, by + 7], fill=col + (255,))
        d.ellipse([x - 3, by - 4, x + 2, by + 1], fill=(255, 250, 230, 255))


def framed(w, h, border, inner):
    base = plaid(w, h, scale=border / 22)
    d = ImageDraw.Draw(base)
    d.rectangle([border, border, w - border - 1, h - border - 1], fill=inner + (255,))
    d.rectangle([border - 2, border - 2, w - border + 1, h - border + 1], outline=(18, 8, 6, 255), width=2)
    return base


def og():
    W, H = 1200, 630
    out = wallpaper(W, H).convert("RGBA")
    card_w, card_h = 1040, 470
    card = framed(card_w, card_h, 24, (28, 17, 12))
    lamp = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    ImageDraw.Draw(lamp).ellipse([card_w * .08, -card_h * .7, card_w * .92, card_h * .6], fill=(120, 66, 30, 150))
    card = Image.alpha_composite(card, lamp.filter(ImageFilter.GaussianBlur(70)))
    inner = Image.new("RGBA", (card_w - 48, 70), (0, 0, 0, 0))
    fairy_lights(inner, 6, 22, 92)
    card.alpha_composite(inner, (24, 24))
    logo = wordart("BOOK CLUB", 138)
    card.alpha_composite(logo, ((card_w - logo.width) // 2, 108))
    d = ImageDraw.Draw(card)
    f = ImageFont.truetype(VERDANA_B, 28)
    tag = "CURL UP  ·  READ  ·  GOSSIP ABOUT IT"
    tw = d.textlength(tag, font=f)
    d.text(((card_w - tw) / 2, card_h - 128), tag, font=f, fill=(255, 217, 138))
    f2 = ImageFont.truetype(VERDANA_B, 21)
    sub = "pick a book  ·  vote with your 3 bookmarks  ·  chat  ·  read"
    sw = d.textlength(sub, font=f2)
    d.text(((card_w - sw) / 2, card_h - 76), sub, font=f2, fill=(201, 184, 154))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([(W - card_w) // 2 + 10, (H - card_h) // 2 + 14, (W + card_w) // 2 + 10, (H + card_h) // 2 + 14], fill=(0, 0, 0, 170))
    out = Image.alpha_composite(out, shadow.filter(ImageFilter.GaussianBlur(14)))
    out.alpha_composite(card, ((W - card_w) // 2, (H - card_h) // 2))
    out.convert("RGB").save(IMG / "og-image.jpg", quality=86, optimize=True, progressive=True)


def book_stack(s):
    """Three chunky books stacked up, for the app icon."""
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    books = [((139, 35, 35), 0.70, -0.02), ((46, 78, 56), 0.62, 0.05), ((192, 96, 42), 0.66, -0.04)]
    hgt = s * 0.17
    y = s * 0.80
    for col, wid, off in books:
        x0 = s * (0.5 - wid / 2 + off)
        x1 = x0 + s * wid
        d.rounded_rectangle([x0, y - hgt, x1, y], radius=int(s * 0.03), fill=col, outline=(26, 14, 8), width=max(2, s // 80))
        d.rectangle([x1 - s * 0.05, y - hgt + s * 0.025, x1 - s * 0.015, y - s * 0.025], fill=(243, 232, 208))
        d.rectangle([x0 + s * 0.08, y - hgt * 0.62, x0 + s * 0.30, y - hgt * 0.42], fill=(242, 207, 120))
        y -= hgt - s * 0.005
    return im


def icon(size, path):
    s = 512
    base = framed(s, s, 40, (28, 17, 12))
    lamp = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(lamp).ellipse([s * .1, -s * .2, s * .9, s * .7], fill=(120, 66, 30, 170))
    base = Image.alpha_composite(base, lamp.filter(ImageFilter.GaussianBlur(50)))
    stack = book_stack(s - 80)
    base.alpha_composite(stack, (40, 26))
    base.convert("RGB").resize((size, size), Image.LANCZOS).save(path, optimize=True)


if __name__ == "__main__":
    IMG.mkdir(exist_ok=True)
    og()
    icon(180, IMG / "apple-touch-icon.png")
    icon(192, IMG / "icon-192.png")
    icon(512, IMG / "icon-512.png")
    icon(32, IMG / "favicon-32.png")
    print("made og-image.jpg + icons in img/")
