# Book Club

Our cozy little book club, in a deliberately mid-2000s-looking site. Built from Game Club:
everyone puts one short book on the shelf, spends 3 🔖 bookmarks on the ones they want to read,
and chats in an old-school chat room.

- `index.html`, `css/`, `js/`: the site (plain HTML/CSS/JS, no build step).
- `supabase/migrations/`: database tables, rules and seed data.
- `supabase/functions/books/`: server function for Open Library search + page counts.
- `scripts/set_codes.py`: gives members new two-word secret codes.
- `scripts/make_share_images.py`: draws the link-preview image and app icons.
- `PLAN.md`: every decision made so far.

Secrets live only in `.env.local` and `member-codes.txt`, which are never committed.

To run it locally: `python -m http.server 8000` in this folder, then open http://localhost:8000.
