// Book Club server function: search Open Library, look up page counts, add a pick.
// Page counts are always looked up here on the server, never trusted from the browser.
import { createClient } from "jsr:@supabase/supabase-js@2";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, {
  auth: { persistSession: false },
});

const OL = "https://openlibrary.org/search.json";
const FIELDS = "key,title,author_name,cover_i,number_of_pages_median,first_publish_year";
const UA = { "User-Agent": "BookClubSite/1.0 (small private reading club)" };
const cover = (id?: number, size = "L") => (id ? `https://covers.openlibrary.org/b/id/${id}-${size}.jpg?default=false` : null);

type Doc = { key: string; title: string; author_name?: string[]; cover_i?: number; number_of_pages_median?: number; first_publish_year?: number };
const shape = (d: Doc) => ({
  key: d.key, title: d.title, author: (d.author_name ?? []).slice(0, 2).join(", ") || null,
  year: d.first_publish_year ?? null, pages: d.number_of_pages_median ?? null,
  thumb: cover(d.cover_i, "S"), cover: cover(d.cover_i, "L"),
});

async function lookup(key: string): Promise<Doc | null> {
  const r = await fetch(`${OL}?q=${encodeURIComponent(`key:"${key}"`)}&fields=${FIELDS}&limit=1`, { headers: UA });
  if (!r.ok) return null;
  const d = await r.json().catch(() => null);
  return d?.docs?.[0] ?? null;
}

async function maxPages(): Promise<number> {
  const { data } = await db.from("rounds").select("max_pages").eq("status", "open").maybeSingle();
  return Number(data?.max_pages ?? 150);
}

// same rule shape as Game Club: up to the max is fine, up to 20% over is "just this once", more is a no
function verdict(p: number | null, max: number) {
  if (p == null) return { kind: "nodata", ok: true, msg: "Open Library doesn't know how long this one is, so it needs a quick page count check before it goes on the shelf." };
  if (p <= max) return { kind: "ok", ok: true, msg: `About ${p} pages. Perfect!` };
  if (p <= max + Math.round(max * 0.2)) return { kind: "love", ok: true, msg: `About ${p} pages... ok but just this once cause I love you!` };
  return { kind: "blocked", ok: false, msg: `This one is about ${p} pages. That's way over ${max}. Try a shorter book, a novella or a short story!` };
}

const validKey = (k: unknown) => typeof k === "string" && /^\/works\/OL\d+W$/.test(k);

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  try {
    const p = await req.json();
    const action = String(p.action ?? "");

    if (action === "search") {
      const q = String(p.q ?? "").trim().slice(0, 80);
      if (q.length < 2) return json({ results: [] });
      const r = await fetch(`${OL}?q=${encodeURIComponent(q)}&fields=${FIELDS}&limit=12`, { headers: UA });
      if (!r.ok) return json({ error: "The library catalog isn't answering. Try again in a sec." }, 502);
      const d = await r.json();
      return json({ results: (d.docs ?? []).map(shape) });
    }

    if (action === "info") {
      if (!validKey(p.key)) return json({ error: "Bad book id." }, 400);
      const doc = await lookup(p.key);
      if (!doc) return json({ error: "Open Library doesn't know that book." }, 400);
      const pages = doc.number_of_pages_median ?? null;
      return json({ book: shape(doc), verdict: verdict(pages, await maxPages()) });
    }

    if (action === "add" || action === "add_manual") {
      const { data: member, error: authErr } = await db.rpc("member_for_token", { p_token: String(p.token ?? "") });
      if (authErr || !member) return json({ error: "You need to sign in first." }, 401);

      if (action === "add_manual") {
        const title = String(p.title ?? "").trim().slice(0, 200);
        const author = String(p.author ?? "").trim().slice(0, 200);
        if (!title) return json({ error: "Type the book's title." }, 400);
        const { data, error } = await db.rpc("add_book_internal", {
          p_member: member, p_key: null, p_title: title, p_author: author || null, p_cover: null, p_pages: null, p_status: "pending",
        });
        if (error) return json({ error: error.message }, 400);
        return json({ book: data, verdict: verdict(null, await maxPages()) });
      }

      if (!validKey(p.key)) return json({ error: "Bad book id." }, 400);
      const doc = await lookup(p.key);
      if (!doc) return json({ error: "Open Library doesn't know that book." }, 400);
      const b = shape(doc);
      const v = verdict(b.pages, await maxPages());
      if (!v.ok) return json({ error: v.msg, verdict: v }, 400);
      const { data, error } = await db.rpc("add_book_internal", {
        p_member: member, p_key: b.key, p_title: String(b.title).slice(0, 200), p_author: b.author, p_cover: b.cover,
        p_pages: b.pages, p_status: b.pages == null ? "pending" : "active",
      });
      if (error) return json({ error: error.message }, 400);
      return json({ book: data, verdict: v });
    }

    return json({ error: "Unknown action." }, 400);
  } catch (e) {
    return json({ error: "Something broke: " + (e instanceof Error ? e.message : String(e)) }, 500);
  }
});
