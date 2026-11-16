# Book Club — Build Plan

A copy of Game Club (`../Game Club`), re-themed as a cozy mid-2000s book club. Same members, same
secret words, same features; books instead of games.

## Members
Hannah, Junior, Katie, Sarah, Anthony, Giselle, Michael, Kat, Kalon, Matt (admin).
Secret words are the same as Game Club's: the bcrypt hashes were copied over from Game Club's
database when Book Club was set up (2026-11-15). After that the two are separate, so a new code
from `scripts/set_codes.py` here only changes Book Club. Everyone picks a new color + font on
their first Book Club sign-in (the palette and fonts are cozier than Game Club's).

## Stack
- **Database / backend:** Supabase (free tier), project `book-club`, ref `jpykodpgyrwybapgnbrv`,
  region us-east-1, created 2026-11-15 via CLI. Keys + DB password live only in `.env.local`.
  Free projects pause after ~1 week of no activity; restore with one click.
- **Hosting:** Vercel, live at https://book-club-liart-six.vercel.app (Open Graph tags in `index.html` use this address; update them if the domain changes), imported from GitHub (github.com/matthewmajoba/book-club, public, no secrets).
  `.vercelignore` keeps secrets, scripts and supabase/ off the live site.
- **Book data:** Open Library (no account or key). Search + page counts via the `books` Edge
  Function (`number_of_pages_median` across editions). Covers from `covers.openlibrary.org`.
  Page counts are looked up on the server, never trusted from the browser.

## Rules
- One pick each on the shelf: a book, novella or short story **under 150 pages** (`rounds.max_pages`).
  - ≤ 150: fine. 151–180 (up to 20% over): "ok but just this once cause I love you!" Over 180: blocked.
  - Short stories usually aren't in Open Library on their own: use "Can't find it?" and the admin types the page count.
  - Open Library has no page count (or the book isn't there): goes to "page check" until the
    admin types the page count.
- 3 🔖 bookmarks per person to vote with; 2 in one book = a big vote.
- Returning your pick early = +1 late fee (`members.late_fees`), a "tsk tsk tsk" librarian, and a
  slip with a LATE stamp in the **Book Drop**.
- Admin crowns the most-bookmarked book; it goes to **📚 Books We've Read** and the shelf clears.

## Look
- Vintage floral wallpaper background, red flannel plaid frames on every panel (all CSS, no photos).
- Header: fairy lights, "BOOK CLUB" WordArt in Ultra (warm gold gradient, brown 3D shadow).
- Ticker: BOOK FACTS typed on a strip of old paper (~140 stupid-but-true facts in `facts`).
- Shelf: chalkboard sign, wooden bookcase with fairy lights, books faced out with page edges,
  wooden shelf planks, handwritten shelf-talker cards taped on.
- Bookmark tiers (share of all bookmarks): DUSTY 🕸️ · SKIMMING 😐 · INTRIGUED 🤔 · PAGE TURNER 😍 ·
  CAN'T PUT IT DOWN 🤩.
- Chat: warm 2000s messenger window on cocoa with fairy-light sparkles; a shop bell rings when
  someone comes in.
- **Daily Reading** (under the chat) and the **🔮 Crystal Ball of Encouragement and Love** archive
  work exactly like Game Club's (`js/pep.js` is a straight copy), with 30 book-flavored sayings.
  Love Notes start on 2026-11-15.

## Re-deploy after changes
- New migration file: `npx supabase db push`.
- Function: `npx supabase functions deploy books --no-verify-jwt --use-api`.
- Preview image + icons: `python scripts/make_share_images.py`.
