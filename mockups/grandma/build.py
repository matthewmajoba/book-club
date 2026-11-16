"""Builds the 10 grandma-style Book Club mockups + a gallery page (mockups/grandma/index.html).
Run: python mockups/grandma/build.py   Photos in img/ come from Wikimedia Commons (see CREDITS.md)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEMBER_FONTS = "family=Lobster&family=UnifrakturMaguntia&family=Homemade+Apple&family=Henny+Penny&family=Courier+Prime:wght@400;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400"

BOOKS = [
    ("https://covers.openlibrary.org/b/id/4942829-L.jpg", "Best New Horror", "from 20th Century Ghosts", "Matt", "#ff9f43", "UnifrakturMaguntia", 1.05, "28 pp", "page turner", [("#8fa8ff", 2), ("#7bd88f", 1)], False),
    ("https://covers.openlibrary.org/b/id/2547013-L.jpg", "The Stinky Cheese Man", "", "Sarah", "#b99cff", "Homemade Apple", .8, "52 pp", "intrigued", [("#ff9f43", 1)], False),
    ("https://covers.openlibrary.org/b/isbn/9780156012195-L.jpg", "The Little Prince", "", "Kalon", "#7bd88f", "Lobster", 1, "96 pp", "can't put it down", [("#ff9f43", 1), ("#b99cff", 2), ("#ff6b6b", 1)], False),
    ("https://covers.openlibrary.org/b/isbn/9780140177398-L.jpg", "Of Mice and Men", "", "Hannah", "#ff6b6b", "Henny Penny", .92, "? pp", "", [], True),
]
FACTS = ["Agatha Christie learned about poisons working in a hospital pharmacy.", "The Little Prince has been translated into over 500 languages.",
         "Dr. Seuss wrote Green Eggs and Ham on a bet that he couldn't use only 50 words.", "Libraries in the 1800s often charged a membership fee."]


def nm(name, color, font, fs):
    return f'<span class="nm" style="--mc:{color};--mf:\'{font}\';--fs:{fs}">{name}</span>'


def page(t):
    books = []
    for cover, title, frm, who, col, font, fs, pp, tier, votes, pending in BOOKS:
        rib = "".join(f'<i style="--c:{c}"{" class=big" if p == 2 else ""}></i>' for c, p in votes)
        books.append(f'''<div class="book"><div class="cover">{f'<span class="ribbons">{rib}</span>' if rib else ""}<img src="{cover}" alt="Cover of {title}" >{'<span class="pending">awaiting page count</span>' if pending else ""}</div>
      <div class="card"><span class="by">picked by</span>{nm(who, col, font, fs)}<span class="ti">{title}</span>{f"<small>{frm}</small>" if frm else ""}<span class="meta">{pp}{f" · <b>{tier}</b>" if tier else ""}</span></div></div>''')
    facts = "<em>❦</em>".join(FACTS)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["n"]}. {t["name"]} · Book Club look</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{t["fonts"]}&{MEMBER_FONTS}&display=swap">
<link rel="stylesheet" href="base.css">
<style>{t["css"]}</style></head>
<body class="t{t["n"]}">
<a class="back" href="index.html">&larr; all 10 looks</a>
<main class="page">
  <header class="mast">{t.get("before", "")}
    <div class="mast-in"><p class="hello">{t.get("hello", "Welcome to")}</p><h1 class="name">Book Club</h1><p class="tag">&#9733; like game club but for books &#9733;</p></div>{t.get("after", "")}
  </header>
  <nav class="nav">
    <button class="gb">The Log</button><button class="gb">Books We've Read</button><button class="gb">Crystal Ball of Encouragement &amp; Love</button>
    <button class="gb">Rules</button><button class="gb">Admin</button><button class="gb go">Sign out, Matt</button>
  </nav>
  <div class="ticker"><b>Book Facts</b><div class="run"><span>{facts}</span></div></div>
  <div class="cols">
    <section class="box shelfbox">
      <div class="sec"><h2>Book Picks</h2><span class="limit">under 150 pages</span></div>
      <div class="budget">Your bookmarks <span class="tok"><i></i><i></i><i class="u"></i></span> <b>2 of 3 left</b><button class="gb small">+ Put a book on the shelf</button></div>
      <div class="shelf">{"".join(books)}</div>
      <p class="still"><span>Still choosing</span> {nm("Giselle", "#4fd1c5", "Lobster", 1)} &amp; {nm("Junior", "#ffd166", "Henny Penny", .92)}</p>
      <div class="drop"><div class="hd"><b>The Book Drop</b><small>returned early · one late fee each</small></div>
        <div class="row"><span>NOV 12</span><span>{nm("Anthony", "#6ec6ff", "Lobster", 1)}</span><span>Wuthering Heights</span><span class="late">LATE</span></div></div>
    </section>
    <aside class="side">
      <div class="box chat">
        <div class="tb"><span class="tbi">&#10086;</span><span>Book Club Chat Room</span></div>
        <div class="here"><span class="lbl">here now (3/10):</span> {nm("Matt", "#ff9f43", "UnifrakturMaguntia", 1.05)} {nm("Kalon", "#7bd88f", "Lobster", 1)} {nm("Sarah", "#b99cff", "Homemade Apple", .8)}</div>
        <div class="log">
          <p><span class="ts">(8:10 AM)</span>{nm("Kalon", "#7bd88f", "Lobster", 1)}: under 150 pages? what are we reading, chapter books? lol</p>
          <p class="sys"><span class="ts">(8:19 AM)</span>Sarah put The Stinky Cheese Man on the shelf!</p>
          <p><span class="ts">(8:21 AM)</span>{nm("Sarah", "#b99cff", "Homemade Apple", .8)}: Kids books</p>
          <p><span class="ts">(8:24 AM)</span>{nm("Matt", "#ff9f43", "UnifrakturMaguntia", 1.05)}: grandma would be so proud of us</p>
        </div>
        <div class="send"><input type="text" placeholder="type a message..." aria-label="Message"><button class="gb small">Send</button></div>
      </div>
      <div class="box daily">
        <h3>Daily Reading</h3>
        <q>You have the energy of a brand-new library card.</q>
        <div class="orbrow"><span class="orb" aria-hidden="true"></span><span class="count"><span>000168</span><small>likes</small></span></div>
      </div>
    </aside>
  </div>
  <footer class="foot"><p class="colo">Book Club · a small reading society · est. 2026</p>
    <div class="badges"><span class="badge"><b>BEST VIEWED</b><i>1024x768</i></span><span class="badge"><b>MADE W/</b><i>LOVE</i></span><span class="badge"><b>BOOKS BY</b><i>OPEN LIBRARY</i></span><span class="badge"><b>ASK</b><i>GRANDMA</i></span></div>
  </footer>
</main>
</body></html>'''


# ---------------------------------------------------------------- the ten looks
T = []

T.append(dict(n=1, slug="doily-parlor", name="The Doily Parlor",
  blurb="Real crocheted doilies on red velvet, a cameo plaque masthead, cameo-brooch buttons, books standing on doilies.",
  fonts="family=Pinyon+Script&family=Cormorant+SC:wght@500;700&family=Cormorant+Garamond:ital,wght@1,500",
  hello="Grandma's",
  before='<img class="dly" src="img/doily.png" alt="">',
  css="""
:root{--bg:#8f0f12;--tile:url(img/doily-bg.jpg);--tile-size:170px;--panel:#fff8f1;--ink:#3b1418;--muted:#8d5a5a;--accent:#9d1424;--title:"Pinyon Script",cursive;--display:"Cormorant Garamond",serif}
.mast{padding:10px 0 4px}
.dly{position:absolute;left:50%;top:50%;width:min(560px,96vw);transform:translate(-50%,-50%) rotate(8deg);filter:drop-shadow(0 6px 10px rgba(0,0,0,.45));pointer-events:none}
.mast-in{background:radial-gradient(ellipse at 50% 40%,#fffdf8,#f7e9dc);border-radius:50%;padding:46px 70px 44px;margin:46px 0;
  box-shadow:0 0 0 4px #e7c66a,0 0 0 6px #8a6420,0 0 0 9px #f3dc9a,0 0 0 11px #8a6420,0 14px 30px rgba(0,0,0,.55),inset 0 0 30px rgba(140,90,60,.18)}
.hello{font:500 14px "Cormorant SC",serif;letter-spacing:.35em;color:#8a6420}
.tag{font:italic 500 22px "Cormorant Garamond",serif}
.gb{font:700 15px/1 "Cormorant SC",serif;letter-spacing:.06em;color:#5a1620;padding:11px 22px 12px;border-radius:999px;
  background:radial-gradient(ellipse at 50% 30%,#fff4ef,#f6cdbf 70%,#e9aa98);
  box-shadow:inset 0 0 0 2px #fff7e6,inset 0 -3px 6px rgba(140,60,50,.25),0 0 0 3px #d9b257,0 0 0 4px #7d5a18,0 4px 0 4px #6b4a12,0 9px 14px 2px rgba(0,0,0,.45);text-shadow:0 1px 0 #fff}
.gb:hover{background:radial-gradient(ellipse at 50% 30%,#fff,#ffd9cc 70%,#f2b3a2)}
.gb:active{transform:translateY(3px);box-shadow:inset 0 0 0 2px #fff7e6,0 0 0 3px #d9b257,0 0 0 4px #7d5a18,0 1px 0 4px #6b4a12}
.gb.go{background:radial-gradient(ellipse at 50% 30%,#d33c4c,#9d1424 75%);color:#fff4ee;text-shadow:0 1px 1px #4a0008}
.gb.small{font-size:13px;padding:8px 16px}
.ticker{background:#fde5ea;border:2px solid #d9b257;border-radius:999px;box-shadow:0 0 0 4px #fff7f0,0 6px 14px rgba(0,0,0,.45)}
.ticker b{font:400 24px "Pinyon Script";color:#fff;background:#9d1424;border-radius:999px 0 0 999px;padding:0 22px}
.ticker .run{font:italic 500 18px "Cormorant Garamond",serif;color:#5a1620}.ticker em{color:#9d1424}
.box{border-radius:18px;box-shadow:0 0 0 4px #f7d6dd,0 0 0 6px #d9b257,0 0 0 7px #7d5a18,0 14px 30px rgba(0,0,0,.55)}
.box::before{content:"";position:absolute;inset:7px;border:1.5px dashed #e3a6b2;border-radius:13px;pointer-events:none}
.limit{font:500 17px "Cormorant SC",serif;border:1.5px solid #d9b257;border-radius:999px;background:#fff1ea}
.cover::before{content:"";position:absolute;left:50%;top:50%;width:150%;aspect-ratio:1;transform:translate(-50%,-30%) rotate(-12deg);background:url(img/doily.png) center/contain no-repeat;z-index:-2;filter:drop-shadow(0 3px 3px rgba(0,0,0,.25))}
.card{position:relative;z-index:1}
.card{background:#fff;border-radius:10px;box-shadow:0 0 0 1px #e9c3c9,0 3px 6px rgba(0,0,0,.12)}
.pending{background:#9d1424;color:#fff}
.chat .tb{background:linear-gradient(#c8324a,#9d1424);color:#fff;font:700 15px "Cormorant SC",serif;letter-spacing:.06em;border-radius:18px 18px 0 0}
.tbi{width:20px;height:20px;border-radius:50%;background:#fff;color:#9d1424;display:grid;place-items:center}
.chat .here{background:#fdeef0;border-bottom:1px solid #f0c8cf}
.daily{background:radial-gradient(circle at 50% 0,#4a1028,#200814);color:#ffeef2}
.daily::before{border-color:#d9b257}
.daily h3{font:400 32px "Pinyon Script";color:#f3dc9a}
.count span{background:#200814;color:#f3dc9a;border:2px solid #d9b257;border-radius:6px}
.foot{font:italic 500 18px "Cormorant Garamond",serif}.foot .colo{background:#fff8f1;padding:4px 20px;border-radius:999px;box-shadow:0 0 0 3px #d9b257}
"""))

T.append(dict(n=2, slug="candy-dish", name="Grandma's Candy Dish",
  blurb="Real strawberry hard candies on pink gingham, peppermint-stripe frames, and buttons that are wrapped candies.",
  fonts="family=Leckerli+One&family=Fredoka:wght@500;700",
  hello="Grab a candy, sweetie",
  before='<img class="cnd l" src="img/candy.png" alt=""><img class="cnd r" src="img/candy.png" alt="">',
  css="""
:root{--bg:#ffe3ea;--tile:url(img/candy-bg.jpg);--tile-size:340px;--panel:#fffdfd;--ink:#4a1420;--muted:#a05a6a;--accent:#d3203f;--title:"Leckerli One",cursive;--display:"Fredoka",sans-serif;--body:"Fredoka",sans-serif}
.mast{padding:34px 20px 30px;background:#fff;border-radius:44px;box-shadow:0 0 0 12px #fff,0 0 0 12px #fff,0 18px 34px rgba(160,30,60,.35);
  border:14px solid transparent;background:linear-gradient(#fffafb,#fff0f4) padding-box,repeating-linear-gradient(45deg,#e01f3d 0 14px,#fff 14px 28px) border-box}
.cnd{position:absolute;width:min(230px,26vw);top:50%;filter:drop-shadow(0 8px 8px rgba(0,0,0,.25))}
.cnd.l{left:-36px;transform:translateY(-50%) rotate(-24deg)}.cnd.r{right:-36px;transform:translateY(-50%) rotate(160deg) scaleY(-1)}
.name{color:#e01f3d;text-shadow:3px 3px 0 #fff,6px 6px 0 #1f8a4c,7px 7px 0 #0d5a2c;font-size:clamp(56px,11vw,124px)}
.hello{font:700 13px "Fredoka";letter-spacing:.25em;color:#1f8a4c}
.tag{font:500 19px "Fredoka";background:#1f8a4c;color:#fff;padding:5px 18px;border-radius:999px;margin-top:12px}
.gb{position:relative;margin:0 22px;font:700 14px/1 "Fredoka";color:#fff;padding:12px 18px;border-radius:22px;text-shadow:0 1px 1px #6a0010;
  background:radial-gradient(circle at 20% 30%,#ffe36b 0 1.4px,transparent 2px) 0 0/14px 12px,radial-gradient(circle at 70% 75%,#ffe36b 0 1.4px,transparent 2px) 0 0/14px 12px,radial-gradient(ellipse at 40% 25%,#ff8a9a,#e01f3d 55%,#9a0a22);
  box-shadow:inset 0 3px 3px rgba(255,255,255,.55),inset 0 -4px 6px rgba(80,0,10,.4),0 6px 10px rgba(120,0,30,.35)}
.gb::before,.gb::after{content:"";position:absolute;top:50%;width:26px;height:34px;margin-top:-17px;background:linear-gradient(135deg,#0e6a35,#3fd47e 35%,#0b5a2b 55%,#55e292 75%,#0e6a35);z-index:-1}
.gb::before{left:-22px;clip-path:polygon(100% 30%,0 0,18% 30%,0 50%,18% 70%,0 100%,100% 70%)}
.gb::after{right:-22px;clip-path:polygon(0 30%,100% 0,82% 30%,100% 50%,82% 70%,100% 100%,0 70%)}
.gb:hover{filter:brightness(1.08)}.gb:active{transform:translateY(2px) scale(.98)}
.gb.go{background:radial-gradient(ellipse at 40% 25%,#7cf0aa,#1f8a4c 55%,#0b4a24)}
.gb.go::before,.gb.go::after{background:linear-gradient(135deg,#a3001c,#ff6a80 35%,#a3001c 55%,#ff8a9a 75%,#a3001c)}
.gb.small{font-size:12.5px;padding:9px 14px}
.ticker{background:#fff;border-radius:999px;border:4px solid #1f8a4c;box-shadow:0 6px 0 #0d5a2c}
.ticker b{background:#1f8a4c;color:#fff;font:400 20px "Leckerli One"}
.ticker .run{font:500 16px "Fredoka";color:#4a1420}.ticker em{color:#e01f3d}
.box{border-radius:28px;border:12px solid transparent;background:linear-gradient(#fffdfd,#fff6f8) padding-box,repeating-linear-gradient(45deg,#e01f3d 0 12px,#fff 12px 24px) border-box;box-shadow:0 14px 28px rgba(160,30,60,.3)}
.limit{background:#ffe3ea;border-radius:999px;font:700 14px "Fredoka";color:#e01f3d}
.card{background:#fff;border-radius:14px;border:3px solid #ffd0db;border-top:10px solid transparent;background:linear-gradient(#fff,#fff) padding-box,repeating-linear-gradient(90deg,#ffd0db 0 8px,#fff 8px 16px) border-box}
.cover img{border-radius:6px}
.pending{background:#1f8a4c;color:#fff;border-radius:6px}
.chat{padding:0}.chat .tb{background:repeating-linear-gradient(90deg,#ffd0db 0 14px,#fff 14px 28px);color:#e01f3d;font:400 20px "Leckerli One"}
.tbi{color:#1f8a4c}.chat .here{border-bottom:2px dotted #ffc0cf}
.daily{background:radial-gradient(circle at 50% 10%,#ffe3ea,#ffc9d6) padding-box,repeating-linear-gradient(45deg,#e01f3d 0 12px,#fff 12px 24px) border-box}
.daily h3{font:400 30px "Leckerli One";color:#e01f3d}
.count span{background:#fff;border:3px solid #e01f3d;border-radius:12px;color:#e01f3d}
.foot{font:500 16px "Fredoka";color:#4a1420}.foot .colo{background:#fff;padding:4px 16px;border-radius:999px}
"""))

T.append(dict(n=3, slug="sunday-china", name="Sunday China",
  blurb="Real Blue Willow plates on a blue gingham tablecloth, porcelain panels with cobalt and gold rims, china-plate buttons.",
  fonts="family=Great+Vibes&family=Cormorant+SC:wght@500;700&family=Cormorant+Garamond:ital,wght@0,500;1,500",
  hello="Sunday dinner at",
  before='<img class="plate l" src="img/willow.png" alt=""><img class="plate r" src="img/willow.png" alt="">',
  css="""
:root{--bg:#eef3fb;--tile:url(img/willow-bg.jpg);--tile-size:420px;--panel:#fdfdfb;--ink:#14244f;--muted:#5a6a92;--accent:#1d3f94;--title:"Great Vibes",cursive;--display:"Cormorant Garamond",serif}
.mast{padding:30px 150px;background:#fdfdfb;border-radius:50% / 26%;box-shadow:inset 0 0 0 10px #fdfdfb,inset 0 0 0 13px #1d3f94,inset 0 0 0 16px #fdfdfb,inset 0 0 0 18px #c9a24a,0 16px 34px rgba(20,36,79,.4)}
.plate{position:absolute;top:50%;width:min(170px,20vw);transform:translateY(-50%)}.plate.l{left:-10px;transform:translateY(-50%) rotate(-12deg)}.plate.r{right:-10px;transform:translateY(-50%) rotate(14deg)}
.hello{font:500 14px "Cormorant SC";letter-spacing:.32em;color:#c9a24a}
.name{color:#1d3f94;text-shadow:0 2px 0 #c9d7f2}
.tag{font:italic 500 22px "Cormorant Garamond"}
@media (max-width:700px){.mast{padding:30px 24px}.plate{display:none}}
.gb{font:700 14px/1 "Cormorant SC";letter-spacing:.08em;color:#1d3f94;padding:13px 24px;border-radius:999px;background:radial-gradient(ellipse at 50% 20%,#fff,#eef2fa 70%,#dbe3f3);
  box-shadow:inset 0 0 0 3px #fff,inset 0 0 0 5px #1d3f94,inset 0 0 0 6px #fff,inset 0 0 0 7.5px #6f8ccc,0 0 0 2px #c9a24a,0 4px 0 2px #9c7a2a,0 9px 14px rgba(20,36,79,.35)}
.gb:hover{background:radial-gradient(ellipse at 50% 20%,#fff,#f6f8fd)}.gb:active{transform:translateY(3px);box-shadow:inset 0 0 0 3px #fff,inset 0 0 0 5px #1d3f94,0 0 0 2px #c9a24a,0 1px 0 2px #9c7a2a}
.gb.go{background:radial-gradient(ellipse at 50% 20%,#3b66c9,#1d3f94 70%);color:#fff;box-shadow:inset 0 0 0 3px #1d3f94,inset 0 0 0 4.5px #fff,0 0 0 2px #c9a24a,0 4px 0 2px #9c7a2a,0 9px 14px rgba(20,36,79,.35)}
.gb.small{padding:10px 18px;font-size:13px}
.ticker{background:#1d3f94;color:#fff;border-radius:6px;box-shadow:0 0 0 3px #fff,0 0 0 5px #c9a24a,0 8px 16px rgba(20,36,79,.35)}
.ticker b{font:400 28px "Great Vibes";color:#f3dc9a}.ticker .run{font:italic 500 18px "Cormorant Garamond"}.ticker em{color:#f3dc9a}
.box{border-radius:26px;box-shadow:inset 0 0 0 8px #fdfdfb,inset 0 0 0 10px #1d3f94,inset 0 0 0 13px #fdfdfb,inset 0 0 0 14px #6f8ccc,0 0 0 3px #c9a24a,0 16px 30px rgba(20,36,79,.38);padding:24px}
.limit{font:500 16px "Cormorant SC";border:1.5px solid #1d3f94;border-radius:999px}
.cover::before{content:"";position:absolute;left:50%;bottom:-22px;width:150%;aspect-ratio:3/1;transform:translateX(-50%);border-radius:50%;background:radial-gradient(ellipse,#fff 40%,#e3e9f6 62%,#1d3f94 64% 66%,#fff 67%,#c9a24a 70% 71%,transparent 72%);z-index:-2;filter:drop-shadow(0 3px 3px rgba(20,36,79,.3))}
.card{position:relative;z-index:1}
.card{background:#fff;border:1.5px solid #1d3f94;border-radius:12px;box-shadow:inset 0 0 0 3px #fff,inset 0 0 0 4px #6f8ccc}
.pending{background:#1d3f94;color:#fff}
.chat .tb{background:#1d3f94;color:#fff;font:700 15px "Cormorant SC";letter-spacing:.08em;border-radius:26px 26px 0 0}
.chat{padding:0;box-shadow:0 0 0 3px #c9a24a,0 16px 30px rgba(20,36,79,.38)}
.tbi{color:#f3dc9a}
.daily h3{font:400 34px "Great Vibes";color:#1d3f94}
.count span{border:2px solid #1d3f94;border-radius:8px;color:#1d3f94}
.foot{font:italic 500 19px "Cormorant Garamond";color:#14244f}.foot .colo{background:#fff;padding:4px 18px;border-radius:999px;box-shadow:0 0 0 2px #1d3f94}
"""))

T.append(dict(n=4, slug="rose-teatime", name="Rose Teatime",
  blurb="Real rose-painted porcelain repeated as wallpaper, framed tea-set photos in the header, gilded pink enamel buttons.",
  fonts="family=Parisienne&family=Playfair+Display:ital,wght@0,600;1,500&family=Lora:ital@0;1",
  hello="Time for tea at",
  before='<figure class="oval l"><img src="img/teacup.jpg" alt=""></figure><figure class="oval r"><img src="img/roseset.jpg" alt=""></figure>',
  css="""
:root{--bg:#fff;--tile:url(img/rose-bg.jpg);--tile-size:300px;--panel:#fff9fa;--ink:#4b1d2b;--muted:#a3687a;--accent:#c23a64;--title:"Parisienne",cursive;--display:"Playfair Display",serif;--body:"Lora",Georgia,serif}
.mast{padding:30px 200px 34px;background:linear-gradient(#fff6f8,#ffe8ee);border-radius:20px;box-shadow:inset 0 0 0 6px #fff6f8,inset 0 0 0 8px #d4ad57,inset 0 0 0 10px #fff6f8,inset 0 0 0 11px #d4ad57,0 18px 36px rgba(120,40,70,.35)}
.oval{position:absolute;top:50%;margin:0;width:150px;height:186px;border-radius:50%;overflow:hidden;transform:translateY(-50%);box-shadow:0 0 0 5px #e8c773,0 0 0 7px #8a6420,0 0 0 10px #f6e3a8,0 0 0 12px #8a6420,0 10px 18px rgba(0,0,0,.4)}
.oval.l{left:34px}.oval.r{right:34px}.oval img{width:100%;height:100%;object-fit:cover}
@media (max-width:760px){.mast{padding:30px 20px}.oval{display:none}}
.hello{font:italic 500 16px "Playfair Display";letter-spacing:.06em;text-transform:none;color:#a07a2a}
.name{color:#c23a64;text-shadow:0 2px 0 #fff,0 3px 0 #e8c773}
.tag{font:italic 500 21px "Playfair Display"}
.gb{font:600 14px/1 "Playfair Display";color:#fff;padding:12px 22px 12px 38px;border-radius:999px;position:relative;text-shadow:0 1px 1px #6a0a2a;
  background:linear-gradient(#f590ad,#d94d79 60%,#b93460);box-shadow:inset 0 2px 1px rgba(255,255,255,.6),inset 0 -3px 5px rgba(90,0,30,.35),0 0 0 3px #f2d58a,0 0 0 4.5px #8a6420,0 4px 0 4px #6e4e14,0 9px 14px rgba(90,20,50,.4)}
.gb::before{content:"\\273F";position:absolute;left:14px;top:50%;transform:translateY(-52%);font-size:15px;color:#fff3c4;text-shadow:0 0 3px #b93460}
.gb:hover{filter:brightness(1.07)}.gb:active{transform:translateY(3px);box-shadow:inset 0 2px 1px rgba(255,255,255,.6),0 0 0 3px #f2d58a,0 0 0 4.5px #8a6420,0 1px 0 4px #6e4e14}
.gb.go{background:linear-gradient(#fff,#ffeef3 60%,#f8d6e1);color:#c23a64;text-shadow:none}.gb.go::before{color:#c23a64;text-shadow:none}
.gb.small{font-size:12.5px;padding:9px 16px 9px 32px}.gb.small::before{left:11px}
.ticker{background:#fff;border-radius:999px;box-shadow:0 0 0 3px #d4ad57,0 0 0 6px #fff,0 0 0 7px #d4ad57,0 8px 16px rgba(120,40,70,.3)}
.ticker b{background:#c23a64;color:#fff;font:400 26px "Parisienne";border-radius:999px 0 0 999px}.ticker .run{font:italic 17px "Lora";color:#4b1d2b}.ticker em{color:#c23a64}
.box{border-radius:20px;box-shadow:inset 0 0 0 5px #fff9fa,inset 0 0 0 7px #d4ad57,0 0 0 4px #ffe1ea,0 0 0 5px #d4ad57,0 16px 30px rgba(120,40,70,.3);padding:22px}
.limit{font:italic 500 16px "Playfair Display";border:1.5px solid #d4ad57;border-radius:999px;background:#fff}
.card{background:#fff;border-radius:50% 50% 12px 12px / 22px 22px 12px 12px;box-shadow:0 0 0 1.5px #e8c773,0 4px 8px rgba(120,40,70,.15);padding-top:14px}
.pending{background:#c23a64;color:#fff}
.chat .tb{background:linear-gradient(#e0608a,#c23a64);color:#fff;font:600 15px "Playfair Display";border-radius:20px 20px 0 0}
.chat{padding:0}.tbi{color:#f2d58a}
.daily{background:radial-gradient(circle at 50% 0,#5a1c36,#2c0c1c);color:#ffeef3}
.daily h3{font:400 34px "Parisienne";color:#f2d58a}
.count span{border:2px solid #d4ad57;border-radius:8px;color:#f2d58a;background:#2c0c1c}
.foot{font:italic 18px "Lora";color:#4b1d2b}.foot .colo{background:#fff;padding:4px 18px;border-radius:999px;box-shadow:0 0 0 2px #d4ad57}
"""))

T.append(dict(n=5, slug="sewing-tin", name="The Sewing Tin",
  blurb="A real tin of sewing buttons as the wallpaper, tape-measure trim, pinked-edge fabric panels, and buttons that are actual sewing buttons.",
  fonts="family=Cookie&family=Special+Elite&family=Nunito:wght@600;800",
  hello="Lovingly handmade by",
  after='<img class="spool" src="img/buttons-spool.png" alt="">',
  css="""
:root{--bg:#3a2216;--tile:url(img/buttons-bg.jpg);--tile-size:420px;--panel:#fbf4e6;--ink:#2e2018;--muted:#8a6d55;--accent:#c0392b;--title:"Cookie",cursive;--display:"Special Elite",monospace;--body:"Nunito",sans-serif}
.mast{padding:34px 40px 70px;background:#fbf4e6;border-radius:6px;box-shadow:0 0 0 6px #fbf4e6,0 0 0 8px #c0392b,0 18px 34px rgba(0,0,0,.6);outline:2px dashed #c0392b;outline-offset:-16px}
.mast::before{content:"";position:absolute;left:0;right:0;top:-6px;height:28px;background:repeating-linear-gradient(90deg,#2e2018 0 1px,transparent 1px 9px) 0 100%/100% 9px no-repeat,repeating-linear-gradient(90deg,#2e2018 0 1.5px,transparent 1.5px 45px) 0 100%/100% 16px no-repeat,#f5d547;border-bottom:1px solid #b0901a}
.spool{position:absolute;bottom:-42px;right:24px;width:min(300px,40vw);transform:rotate(-4deg);z-index:3}
.hello{font:400 14px "Special Elite";letter-spacing:.2em;color:#c0392b;margin-top:18px}
.name{color:#2c4a7a;font-size:clamp(66px,12vw,140px)}
.tag{font:400 17px "Special Elite"}
.gb{font:800 14px/1 "Nunito";color:#2e2018;padding:12px 18px 12px 46px;border-radius:999px;position:relative;background:var(--c,#f9c9d4);
  box-shadow:inset 0 0 0 4px rgba(255,255,255,.35),inset 0 -5px 8px rgba(0,0,0,.18),inset 0 4px 6px rgba(255,255,255,.5),0 4px 0 rgba(0,0,0,.25),0 8px 12px rgba(0,0,0,.35)}
.gb::before{content:"";position:absolute;left:12px;top:50%;width:24px;height:24px;margin-top:-12px;border-radius:50%;
  background:radial-gradient(circle at 35% 35%,#2e2018 0 2.3px,transparent 2.8px),radial-gradient(circle at 65% 35%,#2e2018 0 2.3px,transparent 2.8px),radial-gradient(circle at 35% 65%,#2e2018 0 2.3px,transparent 2.8px),radial-gradient(circle at 65% 65%,#2e2018 0 2.3px,transparent 2.8px),rgba(0,0,0,.08);
  box-shadow:inset 0 1px 2px rgba(0,0,0,.25)}
.gb::after{content:"";position:absolute;left:18px;top:50%;width:12px;height:12px;margin-top:-6px;background:linear-gradient(45deg,transparent 44%,#c0392b 44% 56%,transparent 56%),linear-gradient(-45deg,transparent 44%,#c0392b 44% 56%,transparent 56%)}
.nav .gb:nth-child(6n+1){--c:#f9c9d4}.nav .gb:nth-child(6n+2){--c:#bfe3d0}.nav .gb:nth-child(6n+3){--c:#fbe39a}.nav .gb:nth-child(6n+4){--c:#cfd8f6}.nav .gb:nth-child(6n+5){--c:#f6c9a4}
.gb.go{--c:#c0392b;color:#fff}.gb.go::after{background:linear-gradient(45deg,transparent 44%,#fff 44% 56%,transparent 56%),linear-gradient(-45deg,transparent 44%,#fff 44% 56%,transparent 56%)}
.gb:active{transform:translateY(3px)}.gb.small{--c:#fbe39a;font-size:12.5px;padding:9px 14px 9px 40px}.gb.small::before{width:20px;height:20px;margin-top:-10px;left:11px}.gb.small::after{left:16px}
.ticker{background:#f5d547;border-block:2px solid #b0901a;box-shadow:0 6px 12px rgba(0,0,0,.5)}
.ticker::after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,#2e2018 0 1px,transparent 1px 9px) 0 0/100% 7px no-repeat;pointer-events:none}
.ticker b{background:#c0392b;color:#fff;font:400 26px "Cookie"}.ticker .run{font:400 15px "Special Elite";color:#2e2018;padding-top:12px}.ticker em{color:#c0392b}
.box{--z:10px;background:#fbf4e6;padding:24px 20px;box-shadow:0 14px 28px rgba(0,0,0,.6);
  -webkit-mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/var(--z) 100%;mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/var(--z) 100%;padding-bottom:28px}
.box::before{content:"";position:absolute;inset:9px 9px 16px;border:2px dashed #c0392b;pointer-events:none}
.side .box{filter:drop-shadow(0 10px 14px rgba(0,0,0,.5))}
.sec h2{color:#2c4a7a}.limit{font:400 15px "Special Elite";background:#f5d547;transform:rotate(-2deg)}
.card{background:#fff;border:1px solid #d9c7a8;box-shadow:2px 3px 0 rgba(0,0,0,.08)}
.card::before{content:"";width:20px;height:20px;margin-top:-20px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 2px,#e74c3c 3px,#a3261a);box-shadow:0 2px 2px rgba(0,0,0,.4)}
.pending{background:#f5d547;color:#2e2018;border:1px solid #b0901a}
.chat .tb{background:#2c4a7a;color:#fff;font:400 15px "Special Elite"}.tbi{color:#f5d547}
.chat .log{background:repeating-linear-gradient(#fbf4e6 0 27px,#d6e2f2 27px 28px)}
.daily{background:#2c4a7a;color:#fff}.daily::before{border-color:#f5d547}
.daily h3{font:400 38px "Cookie";color:#f5d547}
.count span{background:#fbf4e6;color:#2c4a7a;border-radius:6px}
.foot{font:400 15px "Special Elite"}.foot .colo{background:#f5d547;color:#2e2018;padding:5px 16px;border:1px solid #b0901a;box-shadow:0 4px 8px rgba(0,0,0,.5)}
"""))

T.append(dict(n=6, slug="granny-square", name="Granny Square Afghan",
  blurb="A real granny-square afghan as the wallpaper, crochet-round borders on every panel, buttons that are little granny squares.",
  fonts="family=Grandstander:wght@700;900&family=Nunito:wght@600;800",
  hello="Made with love by",
  before='<figure class="snap"><img src="img/granny-hooks.jpg" alt=""><figcaption>Grandma\'s WIP</figcaption></figure>',
  css="""
:root{--bg:#222;--tile:url(img/granny-bg.jpg);--tile-size:360px;--panel:#fffaf0;--ink:#26201c;--muted:#7a6a5a;--accent:#d6336c;--title:"Grandstander",cursive;--display:"Grandstander",cursive;--body:"Nunito",sans-serif}
.rounds{box-shadow:0 0 0 6px #fffaf0,0 0 0 12px #e8590c,0 0 0 18px #fcc419,0 0 0 24px #1098ad,0 0 0 31px #1b1b1b,0 20px 34px 22px rgba(0,0,0,.45)}
.mast{margin:30px;padding:34px 30px;background:#fffaf0;box-shadow:0 0 0 6px #fffaf0,0 0 0 12px #e8590c,0 0 0 18px #fcc419,0 0 0 24px #1098ad,0 0 0 31px #1b1b1b,0 20px 34px 22px rgba(0,0,0,.45)}
.snap{position:absolute;right:-6px;top:-14px;margin:0;width:180px;background:#fff;padding:8px 8px 26px;transform:rotate(7deg);box-shadow:0 8px 16px rgba(0,0,0,.4);z-index:3}
.snap img{width:100%;display:block}.snap figcaption{font:700 13px "Grandstander";text-align:center;margin-top:6px;color:#444}
@media (max-width:760px){.snap{display:none}}
.hello{font:800 13px "Nunito";color:#1098ad}
.name{font:900 clamp(58px,11vw,124px)/1 "Grandstander";color:#d6336c;text-shadow:4px 4px 0 #fcc419,8px 8px 0 #1098ad,12px 12px 0 #1b1b1b;letter-spacing:.01em}
.tag{font:800 18px "Nunito";margin-top:16px}
.nav{gap:20px}
.gb{font:900 14px/1.1 "Grandstander";color:#1b1b1b;padding:14px 16px;border-radius:4px;background:var(--c,#fcc419);
  box-shadow:inset 0 0 0 4px #fff3,0 0 0 4px var(--c2,#e8590c),0 0 0 8px var(--c3,#1098ad),0 0 0 12px #1b1b1b,0 14px 14px rgba(0,0,0,.45);
  background-image:radial-gradient(circle,rgba(255,255,255,.3) 1px,transparent 1.5px);background-size:5px 5px}
.nav .gb:nth-child(2){--c:#ff8fb1;--c2:#7950f2;--c3:#fcc419}.nav .gb:nth-child(3){--c:#96f2d7;--c2:#d6336c;--c3:#fd7e14}.nav .gb:nth-child(4){--c:#ffd8a8;--c2:#2b8a3e;--c3:#d6336c}.nav .gb:nth-child(5){--c:#d0bfff;--c2:#fcc419;--c3:#e8590c}
.gb.go{--c:#d6336c;--c2:#fcc419;--c3:#1098ad;color:#fff}
.gb:hover{transform:rotate(-2deg) scale(1.03)}.gb:active{transform:translateY(3px)}
.gb.small{font-size:12.5px;padding:10px 12px;margin-right:12px}
.ticker{background:#1b1b1b;margin:8px 12px;box-shadow:0 0 0 5px #fcc419,0 0 0 10px #1b1b1b}
.ticker b{background:#d6336c;color:#fff;font:900 18px "Grandstander"}.ticker .run{font:800 15px "Nunito";color:#fff}.ticker em{color:#fcc419}
.box{margin:31px;background:#fffaf0;box-shadow:0 0 0 6px #fffaf0,0 0 0 12px #e8590c,0 0 0 18px #fcc419,0 0 0 24px #1098ad,0 0 0 31px #1b1b1b,0 20px 34px 22px rgba(0,0,0,.45)}
.side{gap:62px}.cols{gap:30px}
.side .box:nth-child(2){box-shadow:0 0 0 6px #fffaf0,0 0 0 12px #7950f2,0 0 0 18px #ff8fb1,0 0 0 24px #fcc419,0 0 0 31px #1b1b1b,0 20px 34px 22px rgba(0,0,0,.45)}
.sec h2{font:900 40px "Grandstander";color:#d6336c}
.limit{font:900 14px "Grandstander";background:#fcc419;border-radius:4px;box-shadow:0 0 0 3px #1b1b1b}
.card{background:#fff;box-shadow:0 0 0 3px #96f2d7,0 0 0 6px #1b1b1b;margin-top:6px}
.book:nth-child(2) .card{box-shadow:0 0 0 3px #ff8fb1,0 0 0 6px #1b1b1b}.book:nth-child(3) .card{box-shadow:0 0 0 3px #fcc419,0 0 0 6px #1b1b1b}.book:nth-child(4) .card{box-shadow:0 0 0 3px #d0bfff,0 0 0 6px #1b1b1b}
.pending{background:#1b1b1b;color:#fcc419}
.chat .tb{background:#1098ad;color:#fff;font:900 16px "Grandstander"}.tbi{color:#fcc419}
.daily h3{font:900 26px "Grandstander";color:#7950f2}
.count span{background:#1b1b1b;color:#fcc419}
.foot{color:#fff;font:800 16px "Nunito"}.foot .colo{background:#1b1b1b;padding:6px 16px;box-shadow:0 0 0 4px #fcc419}
"""))

T.append(dict(n=7, slug="formal-parlor", name="The Formal Parlor",
  blurb="Real red toile on the walls, the masthead hung in a real carved gilt frame, engraved brass-plate buttons.",
  fonts="family=Cinzel+Decorative:wght@700;900&family=Cinzel:wght@700;800&family=IM+Fell+English:ital@0;1",
  hello="The family of",
  css="""
:root{--bg:#f1e3d6;--tile:url(img/toile-bg.jpg);--tile-size:300px;--panel:#fffaf2;--ink:#3c1712;--muted:#8a5b4f;--accent:#8e1d27;--title:"Cinzel Decorative",serif;--display:"IM Fell English",serif;--body:"IM Fell English",Georgia,serif}
.mast{border:76px solid transparent;border-image:url(img/gilt-frame.png) 182 181 168 177 / 76px 76px 70px 74px round;background:radial-gradient(ellipse at 50% 35%,#5a1c22,#2a0a0e 75%) padding-box;padding:26px 30px 30px;
  filter:drop-shadow(0 18px 18px rgba(40,10,5,.55));max-width:860px;width:100%;justify-self:center}
.hello{font:600 13px "Cinzel";letter-spacing:.35em;color:#e9c97a}
.name{font:900 clamp(44px,8vw,96px)/1.05 "Cinzel Decorative";color:#f6dc92;background:linear-gradient(#fff3c4,#e9c06a 45%,#a0731f 55%,#f3d58a);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 0 #3c0e10)}
.tag{font:italic 21px "IM Fell English";color:#f3e2c4}
.gb{font:800 13.5px/1 "Cinzel";letter-spacing:.08em;color:#2a1600;padding:13px 22px;border-radius:4px;text-shadow:0 1px 0 #fff3c8;
  background:linear-gradient(#fff2bf,#e6bd5c 30%,#b5862c 55%,#e9c56c 80%,#9e7322);box-shadow:inset 0 0 0 1px #fff4c8,inset 0 0 0 3px #a7781e,inset 0 0 0 4px #f8dd8f,0 3px 0 #6a4a10,0 8px 14px rgba(40,10,5,.45)}
.gb::before,.gb::after{content:"";position:absolute;width:5px;height:5px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff7d0,#8a6414);top:50%;margin-top:-2.5px}
.gb{position:relative}.gb::before{left:7px}.gb::after{right:7px}
.gb:hover{filter:brightness(1.08)}.gb:active{transform:translateY(2px);box-shadow:inset 0 0 0 1px #fff4c8,inset 0 0 0 3px #a7781e,0 1px 0 #6a4a10}
.gb.go{background:linear-gradient(#b5303b,#8e1d27 60%,#5e0f17);color:#f6dc92;text-shadow:0 1px 0 #3c0e10;box-shadow:inset 0 0 0 1px #e9a3a8,inset 0 0 0 3px #e6bd5c,0 3px 0 #6a4a10,0 8px 14px rgba(40,10,5,.45)}
.gb.small{padding:10px 18px;font-size:12px}
.ticker{background:#2a0a0e;color:#f3e2c4;box-shadow:0 0 0 3px #e6bd5c,0 0 0 5px #6a4a10,0 10px 18px rgba(40,10,5,.45)}
.ticker b{background:linear-gradient(#f6dc92,#c9973a);color:#2a1600;font:800 15px "Cinzel"}.ticker .run{font:italic 18px "IM Fell English"}.ticker em{color:#e6bd5c}
.box{border:16px solid transparent;background:linear-gradient(#fffaf2,#f8ecdc) padding-box,linear-gradient(135deg,#fff2bf,#c9973a 20%,#7d5715 40%,#f2d07c 55%,#9e7322 75%,#f6e19c) border-box;box-shadow:inset 0 0 0 2px #8e6a22,0 0 0 2px #5a3e0c,0 16px 30px rgba(40,10,5,.5);padding:20px}
.box::before{content:"";position:absolute;inset:-9px;border:1px solid rgba(255,250,220,.7);pointer-events:none}
.sec h2{font:700 34px "Cinzel Decorative";color:#8e1d27}
.limit{font:italic 17px "IM Fell English";border-bottom:1px solid #8e1d27;border-radius:0}
.card{background:#fffaf2;border:1px solid #c9a24a;box-shadow:0 0 0 3px #fffaf2,0 0 0 4px #c9a24a}
.cover img{box-shadow:0 0 0 4px #e6bd5c,0 0 0 5px #6a4a10,0 12px 16px -6px rgba(0,0,0,.6)}
.pending{background:#2a0a0e;color:#f6dc92}
.chat{padding:0}.chat .tb{background:#2a0a0e;color:#f6dc92;font:700 13px "Cinzel";letter-spacing:.1em}.tbi{color:#e6bd5c}
.daily{background:radial-gradient(ellipse at 50% 0,#5a1c22,#2a0a0e 80%) padding-box,linear-gradient(135deg,#fff2bf,#c9973a 20%,#7d5715 40%,#f2d07c 55%,#9e7322 75%,#f6e19c) border-box;color:#f3e2c4}
.daily h3{font:700 22px "Cinzel Decorative";color:#f6dc92}
.count span{background:#2a0a0e;color:#f6dc92;border:2px solid #e6bd5c}
.foot{font:italic 18px "IM Fell English";color:#3c1712}.foot .colo{background:#fffaf2;padding:4px 18px;box-shadow:0 0 0 2px #c9a24a}
"""))

T.append(dict(n=8, slug="chenille-violets", name="Chenille & African Violets",
  blurb="Real green chenille bedspread as the wallpaper, panels framed in real bobbin lace, Grandma's African violets on the windowsill.",
  fonts="family=Berkshire+Swash&family=Quicksand:wght@600;700&family=Lora:ital@0;1",
  hello="From the windowsill of",
  after='<div class="sill"><span class="pot"><img src="img/violet1.png" alt=""></span><span class="pot"><img src="img/violet2.png" alt=""></span><span class="pot"><img src="img/violet3.png" alt=""></span></div>',
  css="""
:root{--bg:#6a7a2a;--tile:url(img/chenille-bg.jpg);--tile-size:260px;--panel:#fbf6ff;--ink:#2e1f3e;--muted:#7a6890;--accent:#7b3fa8;--title:"Berkshire Swash",cursive;--display:"Lora",serif;--body:"Lora",Georgia,serif}
.mast{border:46px solid transparent;border-image:url(img/lace-frame.png) 109 152 134 132 / 46px 50px 46px 50px round;background:radial-gradient(ellipse at 50% 30%,#fbf6ff,#ecdcf6) padding-box;padding:18px 20px 0}
.hello{font:700 13px "Quicksand";color:#5d8a3a;letter-spacing:.24em}
.name{font:400 clamp(56px,10vw,112px)/1.05 "Berkshire Swash";color:#7b3fa8;text-shadow:0 3px 0 #e1c8f2}
.tag{font:italic 20px "Lora"}
.sill{display:flex;gap:clamp(14px,5vw,60px);justify-content:center;margin-top:16px;padding:0 20px;border-bottom:12px solid #e9e3d8;box-shadow:0 10px 0 -4px #cfc6b6;width:100%}
.pot{position:relative;display:grid;justify-items:center;width:clamp(82px,12vw,128px)}
.pot img{width:100%;border-radius:50%;filter:drop-shadow(0 4px 4px rgba(0,0,0,.3));position:relative;z-index:1;margin-bottom:-22%}
.pot::after{content:"";width:72%;height:clamp(40px,6vw,62px);background:linear-gradient(90deg,#b8553a,#d9774f 30%,#e58d64 45%,#c25f40 75%,#9c4430);clip-path:polygon(0 0,100% 0,88% 100%,12% 100%);border-top:8px solid #d26a46;box-shadow:inset 0 6px 0 rgba(0,0,0,.15)}
.gb{font:700 14px/1 "Quicksand";color:#fff;padding:12px 20px;border-radius:999px;text-shadow:0 1px 1px #3e1a5e;
  background:radial-gradient(circle,rgba(255,255,255,.35) 1.2px,transparent 1.6px) 0 0/7px 7px,linear-gradient(#a571d0,#7b3fa8 60%,#5e2a86);
  box-shadow:inset 0 2px 1px rgba(255,255,255,.4),inset 0 -3px 4px rgba(40,0,60,.35),0 0 0 3px #fbf6ff,0 0 0 5px #5d8a3a,0 6px 0 5px #3f6a22,0 10px 14px rgba(0,0,0,.4)}
.gb:hover{filter:brightness(1.08)}.gb:active{transform:translateY(4px);box-shadow:inset 0 2px 1px rgba(255,255,255,.4),0 0 0 3px #fbf6ff,0 0 0 5px #5d8a3a,0 2px 0 5px #3f6a22}
.gb.go{background:radial-gradient(circle,rgba(255,255,255,.35) 1.2px,transparent 1.6px) 0 0/7px 7px,linear-gradient(#ff8ac2,#e0559c 60%,#b8337a)}
.gb.small{font-size:12.5px;padding:9px 15px}
.ticker{background:#fbf6ff;border-radius:999px;box-shadow:0 0 0 4px #7b3fa8,0 8px 16px rgba(0,0,0,.45)}
.ticker b{background:#7b3fa8;color:#fff;font:400 19px "Berkshire Swash";border-radius:999px 0 0 999px}.ticker .run{font:italic 17px "Lora"}.ticker em{color:#5d8a3a}
.box{border:30px solid transparent;border-image:url(img/lace-frame.png) 109 152 134 132 / 30px 32px 30px 32px round;background:#fbf6ff padding-box;padding:14px}
.sec h2{font:400 40px "Berkshire Swash";color:#7b3fa8}
.limit{font:700 14px "Quicksand";background:#efe1f8;border-radius:999px;color:#5e2a86}
.card{background:#fff;border-radius:14px;border:2px dotted #b88ad8}
.pending{background:#5d8a3a;color:#fff;border-radius:999px}
.chat .tb{background:#7b3fa8;color:#fff;font:400 17px "Berkshire Swash";border-radius:10px 10px 0 0}.tbi{color:#ffd1ec}
.daily{background:#2e1f3e padding-box;color:#f3e8ff}.daily h3{font:400 28px "Berkshire Swash";color:#e1c8f2}
.count span{background:#fbf6ff;color:#7b3fa8;border-radius:999px}
.foot{color:#fff;font:italic 18px "Lora";text-shadow:0 1px 3px #000}
"""))

T.append(dict(n=9, slug="cross-stitch", name="Bless This Book Club",
  blurb="Real red cross-stitch on linen as the wallpaper, a stitched sampler masthead trimmed with a real embroidered floral band, stitched-patch buttons.",
  fonts="family=Jacquard+24&family=Pixelify+Sans:wght@500;700&family=Lora:ital@0;1",
  hello="Bless this",
  css="""
:root{--bg:#f4eee2;--tile:url(img/xstitch-bg.jpg);--tile-size:300px;--panel:#fffdf8;--ink:#2a1a14;--muted:#8a6f60;--accent:#c4262e;--title:"Jacquard 24",serif;--display:"Lora",serif;--body:"Lora",Georgia,serif;
  --aida:repeating-linear-gradient(0deg,rgba(0,0,0,.06) 0 1px,transparent 1px 5px),repeating-linear-gradient(90deg,rgba(0,0,0,.06) 0 1px,transparent 1px 5px),#fffdf6}
.mast{background:var(--aida);padding:84px 30px 84px;box-shadow:0 0 0 10px #fffdf6,0 0 0 12px #c4262e,0 18px 30px rgba(60,20,10,.4);border:3px dashed #c4262e;outline:8px solid #fffdf6}
.mast::before,.mast::after{content:"";position:absolute;left:0;right:0;height:62px;background:url(img/xstitch-band.jpg) 0 0/auto 62px repeat-x}
.mast::before{top:0}.mast::after{bottom:0;transform:scaleY(-1)}
.hello{font:400 34px "Jacquard 24";letter-spacing:.06em;text-transform:none;color:#2f6b3a}
.name{font:400 clamp(66px,12vw,140px)/.95 "Jacquard 24";color:#c4262e;text-shadow:3px 3px 0 rgba(196,38,46,.2)}
.tag{font:500 18px "Pixelify Sans";color:#2f6b3a}
.gb{font:700 14px/1 "Pixelify Sans";color:#c4262e;padding:13px 20px;background:var(--aida);border:2px dashed #c4262e;outline:5px solid #fffdf6;box-shadow:0 0 0 7px #2f6b3a,0 4px 0 7px #1d4a26,0 10px 14px 6px rgba(60,20,10,.3)}
.gb:hover{background:#fff1ec}.gb:active{transform:translateY(3px);box-shadow:0 0 0 7px #2f6b3a,0 1px 0 7px #1d4a26}
.gb.go{color:#fffdf6;background:repeating-linear-gradient(0deg,rgba(255,255,255,.12) 0 1px,transparent 1px 5px),repeating-linear-gradient(90deg,rgba(255,255,255,.12) 0 1px,transparent 1px 5px),#c4262e;border-color:#fffdf6;outline-color:#c4262e}
.nav{gap:22px}.gb.small{font-size:12px;padding:10px 14px;margin-right:8px}
.ticker{background:#2a1a14;box-shadow:0 0 0 4px #fffdf6,0 0 0 6px #c4262e,0 10px 18px rgba(60,20,10,.35);margin:0 7px}
.ticker b{background:#c4262e;color:#fff;font:400 26px "Jacquard 24"}.ticker .run{font:500 15px "Pixelify Sans";color:#fffdf6}.ticker em{color:#f2b53a}
.box{background:var(--aida);border:2px dashed #c4262e;box-shadow:0 0 0 8px #fffdf6,0 0 0 10px #2f6b3a,0 16px 28px 6px rgba(60,20,10,.35);margin:10px;padding:20px}
.side{gap:36px}
.sec h2{font:400 46px "Jacquard 24";color:#c4262e}
.limit{font:italic 15px "Lora";border:2px dashed #2f6b3a;color:#2f6b3a}
.card{background:#fffdf6;border:2px dashed #c4262e}
.cover img{box-shadow:0 0 0 3px #fffdf6,0 0 0 5px #2f6b3a,0 12px 16px -6px rgba(0,0,0,.5)}
.pending{background:#2f6b3a;color:#fff}
.chat{padding:0}.chat .tb{background:#c4262e;color:#fff;font:400 22px "Jacquard 24"}.tbi{color:#f2b53a}
.daily{background:#2a1a14;color:#fffdf6;border-color:#f2b53a}.daily h3{font:400 34px "Jacquard 24";color:#f2b53a}
.count span{font-family:"Pixelify Sans";background:#fffdf6;color:#c4262e}
.foot{font:500 15px "Pixelify Sans";color:#2a1a14}.foot .colo{background:#fffdf6;padding:6px 16px;border:2px dashed #c4262e}
"""))

T.append(dict(n=10, slug="good-room", name="The Good Room",
  blurb="Grandma's real Persian rug underfoot, rosebud-stripe wallpaper with real collector plates, and everything covered in clear plastic. Do not sit.",
  fonts="family=Yesteryear&family=Playfair+Display:ital,wght@0,700;1,500&family=Lora:ital@0;1",
  hello="Please wipe your feet",
  before='<img class="cplate l" src="img/roseplate.png" alt=""><img class="cplate r" src="img/willow.png" alt="">',
  after='<p class="sign">PLEASE DO NOT SIT ON THE GOOD COUCH</p>',
  css="""
:root{--bg:#7a2418;--tile:url(img/carpet-bg.jpg);--tile-size:420px;--panel:#fffaf4;--ink:#3a1810;--muted:#8a5a4a;--accent:#8e2440;--title:"Yesteryear",cursive;--display:"Playfair Display",serif;--body:"Lora",Georgia,serif;
  --plastic:linear-gradient(115deg,rgba(255,255,255,0) 18%,rgba(255,255,255,.55) 22%,rgba(255,255,255,0) 30%,rgba(255,255,255,0) 62%,rgba(255,255,255,.35) 66%,rgba(255,255,255,0) 72%)}
.mast{padding:30px 190px 26px;background:url(img/rosestripe-bg.jpg) 0 0/200px;box-shadow:inset 0 -26px 0 #e9dccb,inset 0 -30px 0 #b89a78,0 0 0 8px #fff7ec,0 0 0 10px #b89a78,0 18px 34px rgba(0,0,0,.6)}
.mast-in{background:rgba(255,250,244,.92);padding:16px 34px 18px;border-radius:12px;box-shadow:0 0 0 2px #b89a78}
.cplate{position:absolute;top:44%;width:min(160px,17vw);transform:translateY(-50%)}.cplate.l{left:20px}.cplate.r{right:20px}
.cplate::after{content:""}
@media (max-width:760px){.mast{padding:24px 16px 26px}.cplate{display:none}}
.hello{font:500 italic 15px "Playfair Display";text-transform:none;letter-spacing:.04em;color:#8a5a4a}
.name{font:400 clamp(60px,11vw,124px)/1 "Yesteryear";color:#8e2440;text-shadow:2px 2px 0 #f1c7cf}
.tag{font:italic 500 21px "Playfair Display"}
.sign{position:relative;z-index:2;margin:14px 0 0;background:#fff;border:2px solid #3a1810;font:700 11px "Playfair Display";letter-spacing:.2em;padding:5px 12px;transform:rotate(-1.5deg);box-shadow:2px 2px 0 rgba(0,0,0,.3)}
.gb{position:relative;font:700 14px/1 "Playfair Display";color:#fff;padding:14px 22px;border-radius:14px;text-shadow:0 1px 1px #3a0010;
  background:var(--plastic),radial-gradient(circle at 50% 50%,rgba(0,0,0,.28) 0 2px,transparent 3px) 50% 50%/28px 28px,radial-gradient(ellipse at 50% 20%,#c4526e,#8e2440 70%,#6a1830);
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.55),inset 0 3px 2px rgba(255,255,255,.6),inset 0 -6px 10px rgba(40,0,10,.35),0 0 0 1px rgba(255,255,255,.8),0 5px 0 #4a1020,0 10px 16px rgba(0,0,0,.5)}
.gb:hover{filter:brightness(1.1)}.gb:active{transform:translateY(4px);box-shadow:inset 0 0 0 2px rgba(255,255,255,.55),0 1px 0 #4a1020}
.gb.go{background:var(--plastic),radial-gradient(circle at 50% 50%,rgba(0,0,0,.2) 0 2px,transparent 3px) 50% 50%/28px 28px,radial-gradient(ellipse at 50% 20%,#d9c48a,#a8873a 70%,#7a5c1a);color:#2a1a04;text-shadow:0 1px 0 rgba(255,255,255,.5)}
.gb.small{font-size:12.5px;padding:10px 16px}
.ticker{background:var(--plastic),#fffaf4;border:6px solid transparent;border-image:url(img/chintz-bg.jpg) 30 round;box-shadow:0 10px 18px rgba(0,0,0,.5)}
.ticker b{background:#8e2440;color:#fff;font:400 26px "Yesteryear"}.ticker .run{font:italic 17px "Lora"}.ticker em{color:#8e2440}
.box{border:18px solid transparent;background:linear-gradient(#fffaf4,#fffaf4) padding-box,url(img/chintz-bg.jpg) 0 0/180px border-box;border-radius:16px;box-shadow:0 18px 30px rgba(0,0,0,.55);padding:20px}
.box::after{content:"";position:absolute;inset:-18px;border-radius:16px;background:var(--plastic);box-shadow:inset 0 0 0 2px rgba(255,255,255,.7),inset 0 0 22px rgba(255,255,255,.35);pointer-events:none}
.sec h2{font:400 42px "Yesteryear";color:#8e2440}
.limit{font:italic 500 16px "Playfair Display";background:#fff;border:2px solid #3a1810;transform:rotate(1deg)}
.card{background:#fff;border-radius:10px;box-shadow:0 0 0 1px #d8c2a8,0 3px 6px rgba(0,0,0,.12)}
.pending{background:#3a1810;color:#fff}
.chat{padding:0}.chat .tb{background:#8e2440;color:#fff;font:700 14px "Playfair Display";border-radius:0}.tbi{color:#f1c7cf}
.daily{background:linear-gradient(#2a0a14,#2a0a14) padding-box,url(img/chintz-bg.jpg) 0 0/180px border-box;color:#ffeef2}
.daily h3{font:400 32px "Yesteryear";color:#f1c7cf}
.count span{background:#fffaf4;color:#8e2440;border-radius:8px}
.foot{color:#fff;font:italic 18px "Lora";text-shadow:0 1px 3px #000}.foot .colo{background:rgba(58,24,16,.85);padding:4px 16px;border-radius:999px}
"""))

for t in T:
    (HERE / f"{t['n']:02d}-{t['slug']}.html").write_text(page(t), encoding="utf-8")

cards = "\n".join(f'''<a class="opt" href="{t['n']:02d}-{t['slug']}.html"><div class="pv"><img src="shots/{t['n']:02d}-{t['slug']}-thumb.jpg" alt="{t['name']} preview" loading="lazy"></div>
  <div class="lb"><span class="no">Look {t['n']}</span><b>{t['name']}</b><p>{t['blurb']}</p></div></a>''' for t in T)
(HERE / "index.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Book Club · 10 grandma looks</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pinyon+Script&family=Lora:ital@0;1&display=swap">
<style>
body{{margin:0;background:url(img/doily-bg.jpg) 0 0/150px,#8f0f12;font:15px/1.5 Lora,Georgia,serif;color:#2b1a1a}}
header{{text-align:center;margin:30px auto 6px;max-width:720px;padding:18px 24px 20px;background:#fffaf2;color:#9d1424;border-radius:999px;box-shadow:0 0 0 4px #f3dc9a,0 0 0 6px #7d5a18,0 14px 28px rgba(0,0,0,.5)}}
h1{{margin:0;font:400 clamp(44px,8vw,80px)/1 "Pinyon Script",cursive}}
header p{{margin:6px 0 0;font-style:italic;color:#3b1418}}
.grid{{max-width:1240px;margin:0 auto;padding:20px 16px 60px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}}
.opt{{display:block;background:#fffaf2;color:inherit;text-decoration:none;border-radius:14px;overflow:hidden;box-shadow:0 0 0 4px #f3dc9a,0 14px 28px rgba(0,0,0,.55);transition:transform .15s}}
.opt:hover{{transform:translateY(-4px)}}
.pv{{border-bottom:3px solid #f3dc9a}}.pv img{{display:block;width:100%;height:auto}}
.lb{{padding:12px 16px 16px}}.no{{display:block;font:700 11px Verdana,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#9d1424}}
.lb b{{display:block;font:400 30px/1.1 "Pinyon Script",cursive;color:#9d1424;margin:2px 0 4px}}.lb p{{margin:0;font-size:14px}}
footer{{text-align:center;padding:0 16px 40px}} footer span{{display:inline-block;background:#fffaf2;padding:6px 16px;border-radius:999px;font-size:13px}} footer a{{color:#9d1424}}
</style></head><body>
<header><h1>Pick Grandma's Look</h1><p>Ten full-page looks for Book Club, all built from real photos. Click one to see it full size.</p></header>
<main class="grid">{cards}</main>
<footer><span>Photos from Wikimedia Commons under CC0 / public domain / Creative Commons licenses &middot; <a href="CREDITS.md">credits</a></span></footer>
</body></html>''', encoding="utf-8")
print("built", len(T), "looks")
