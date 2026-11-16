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
  - **Short stories from inside a bigger book** (e.g. "Best New Horror" from 20th Century Ghosts): search the
    book, pick it, open "Just reading one story from this book?" (opens by itself when the book is too long) and type
    the story's title. It goes on the shelf as the story with the book's cover, labeled "from <book>"
    (`books.from_title`), after the admin types its page count (Open Library has no per-story lengths or
    tables of contents to read them from). "Can't find it?" also has an optional "the book it's in" box.
  - Open Library has no page count (or the book isn't there): goes to "page check" until the
    admin types the page count.
- 3 🔖 bookmarks per person to vote with; 2 in one book = a big vote.
- Returning your pick early = +1 late fee (`members.late_fees`), a "tsk tsk tsk" librarian, and a
  slip with a LATE stamp in the **Book Drop**.
- Admin crowns the most-bookmarked book; it goes to **📚 Books We've Read** and the shelf clears.

## Look (redesigned 2026-11-16 for pitching to bookstores)
- Early-2000s website bones (one centered page on tiled wallpaper, framed boxes, a marquee,
  plain-word nav, 80x15 footer badges) set like a literary magazine: Cormorant Garamond italic
  headings, Georgia text, Verdana small-caps labels, Courier Prime for typed bits, "Nothing You
  Could Do" for handwriting. No fake wood, plaid or fairy lights.
- **The admin picks the look** (Admin → The look): club name, tagline, colors (8), wallpaper (10)
  and frame (9). Clicking previews it only for the admin; Save writes `club_look` (one row,
  `set_look` RPC) and everyone's page switches live. Patterns are SVGs drawn in `js/look.js` from
  the chosen colors, so any combo works; frames are 36px border-images sliced at 12px. A small
  script in `index.html` puts the last-seen look back before first paint.
- Masthead: dateline (date · Vol. I · No. <round> · now reading), the club name huge in italic,
  botanical sprigs either side, handwritten tagline, a double rule with a wax seal monogram
  (initials of the club name), then the nav.
- Ticker: BOOK FACTS typed on a strip of paper (~140 stupid-but-true facts in `facts`).
- Shelf: books faced out on a shelf drawn with two ink rules; each vote is a bookmark ribbon
  poking out of the top in the voter's color (big votes stand taller); bookseller shelf-talker
  cards under each book; "Still choosing: ..." line for everyone without a pick.
- Book Drop: a library date-due card with LATE stamps.
- Bookmark tiers (share of all bookmarks): DUSTY · SKIMMING · INTRIGUED · PAGE TURNER ·
  CAN'T PUT IT DOWN (shown as words on the shelf-talker).
- Names: each member's font, in a darkened shade of their color with a highlighter swipe of it.
- Chat: a 2000s messenger window in the club's colors; a shop bell rings when someone comes in.
- **Daily Reading** (under the chat) and the **🔮 Crystal Ball of Encouragement and Love** archive
  work exactly like Game Club's (`js/pep.js` is a straight copy), with 30 book-flavored sayings.
  Love Notes start on 2026-11-15.

## Re-deploy after changes
- New migration file: `npx supabase db push`.
- Function: `npx supabase functions deploy books --no-verify-jwt --use-api`.
- Preview image + icons: `python scripts/make_share_images.py` (draws the default Claret look).
