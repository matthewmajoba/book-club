"""Copies the photo wallpapers from mockups/grandma/img into img/wall/ (plus small thumbnails for the
admin's look picker) and prints each one's average color, which js/look.js uses as the color behind
the photo while it loads. Run: python scripts/make_wallpapers.py
Every photo is from Wikimedia Commons; img/wall/CREDITS.md and credits.html list them."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "mockups" / "grandma" / "img"
OUT = ROOT / "img" / "wall"
OUT.mkdir(parents=True, exist_ok=True)

# site id -> mockup file
WALLS = {
    "granny": "granny-bg.jpg", "afghan": "granny2-bg.jpg", "quilt": "quilt-bg.jpg", "doilies": "doilies-bg.jpg",
    "doily": "doily-bg.jpg", "candy": "candy-bg.jpg", "willow": "willow-bg.jpg", "roses": "rose-bg.jpg",
    "rosebud": "rosestripe-bg.jpg", "calico": "chintz-bg.jpg", "toile": "toile-bg.jpg", "chenille": "chenille-bg.jpg",
    "rug": "carpet-bg.jpg", "buttons": "buttons-bg.jpg", "xstitch": "xstitch-bg.jpg",
}

for wid, name in WALLS.items():
    im = Image.open(SRC / name).convert("RGB")
    im.save(OUT / f"{wid}.jpg", quality=84, optimize=True, progressive=True)
    t = im.copy()
    t.thumbnail((240, 240), Image.LANCZOS)
    t.save(OUT / f"{wid}-t.jpg", quality=78, optimize=True)
    r, g, b = im.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    print(f"{wid:9} #{r:02x}{g:02x}{b:02x}  {im.size}  {(OUT / f'{wid}.jpg').stat().st_size // 1024} KB")

# the polaroid in the masthead
Image.open(SRC / "granny-hooks.jpg").convert("RGB").save(ROOT / "img" / "grandmas-wip.jpg", quality=84, optimize=True)

# ---- credits.html: who took each photo (CC BY / CC BY-SA need this) ----
import html, re
SOURCE = {  # what's on the site -> the Commons file it was made from (keys in mockups/grandma/CREDITS.md)
    "Granny squares": "granny", "'70s afghan": "granny2", "Irish chain quilt": "quilt", "Doilies on velvet": "doilies",
    "Big red doily": "doily_red", "Candy dish": "candy", "Blue willow": "willow", "Rose china": "rosechina",
    "Rosebud stripe": "rosestripe", "Calico": "chintz", "Red toile": "toile2", "Chenille bedspread": "chenille",
    "The good rug": "carpet", "Button tin": "buttons", "Cross-stitch": "xstitch2", "Grandma's WIP (the polaroid)": "granny3",
}
md = (ROOT / "mockups" / "grandma" / "CREDITS.md").read_text(encoding="utf-8")
src = {m[0]: m[1:] for m in re.findall(r"^- \*\*(\w+)\*\*: \[(.+?)\]\((.+?)\) by (.+) \((.+?)\)$", md, re.M)}
rows = []
for shown, key in SOURCE.items():
    title, url, who, lic = src[key]
    who = re.sub(r"(Unknown (author|artist))\1", r"\1", who)
    rows.append(f'<li><b>{html.escape(shown)}</b>: <a href="{html.escape(url)}">{html.escape(title)}</a> by {html.escape(who)} '
                f'<span>({html.escape(lic)})</span></li>')
(ROOT / "credits.html").write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Photo credits · Book Club</title><meta name="robots" content="noindex">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<style>
body{{margin:0;background:#8f7b7a url(img/wall/granny.jpg) 0 0/360px auto;font:600 15px/1.55 "Trebuchet MS",Verdana,sans-serif;color:#26201c}}
main{{max-width:760px;margin:40px auto;padding:26px 30px;background:#fffaf0;border:6px solid #1b1b1b;box-shadow:inset 0 0 0 6px #e8590c,inset 0 0 0 12px #fcc419,inset 0 0 0 18px #1098ad,0 18px 30px rgba(0,0,0,.5)}}
h1{{margin:10px 0 6px;color:#d6336c;font-size:32px}} ul{{padding-left:20px}} li{{margin:8px 0}} span{{color:#76685c}} a{{color:#1c4b8f}}
p.back a{{display:inline-block;margin-top:8px;color:#1b1b1b;background:#fcc419;border:3px solid #1b1b1b;padding:6px 12px;text-decoration:none;font-weight:800}}
</style></head><body><main>
<h1>Photo credits</h1>
<p>Every wallpaper on this site is a real photo from <a href="https://commons.wikimedia.org/">Wikimedia Commons</a>,
cropped and mirrored into a repeating tile (the candy and willow plate are cut out and set on gingham we drew).
Thank you to the people who shared them. Licenses: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY</a>,
<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA</a> (our tiles made from these are shared under the same license),
CC0 and public domain.</p>
<ul>
{chr(10).join(rows)}
</ul>
<p class="back"><a href="./">&larr; back to the club</a></p>
</main></body></html>
''', encoding="utf-8")
print("credits.html:", len(rows), "photos")
