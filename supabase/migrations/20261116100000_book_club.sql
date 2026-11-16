-- Book Club schema (built from Game Club's, with books instead of games).
-- Everyone (even logged-out visitors) can READ the public tables.
-- Nobody can write to tables directly: every change goes through the functions below,
-- which check the member's session token and the club rules.

create extension if not exists pgcrypto with schema extensions;
create schema if not exists private;

-- ---------- tables ----------
create table public.members (
  id smallint generated always as identity primary key,
  name text not null unique,
  color text unique,
  font text,
  late_fees int not null default 0,          -- +1 every time you return your pick early
  is_admin boolean not null default false,
  setup_done boolean not null default false,
  created_at timestamptz not null default now()
);

-- secret codes + lockout state: never readable from the browser
create table private.member_secrets (
  member_id smallint primary key references public.members(id) on delete cascade,
  code_hash text,
  failed_attempts int not null default 0,
  locked_until timestamptz
);

create table private.sessions (
  token_hash text primary key,
  member_id smallint not null references public.members(id) on delete cascade,
  created_at timestamptz not null default now()
);

-- a "round" is one fill-up of the shelf; members never see the word
create table public.rounds (
  id int generated always as identity primary key,
  name text not null,
  max_pages int not null default 300,
  status text not null default 'open' check (status in ('open','closed')),
  winner_book_id bigint,
  created_at timestamptz not null default now(),
  closed_at timestamptz
);
create unique index rounds_one_open on public.rounds ((status)) where status = 'open';

create table public.books (
  id bigint generated always as identity primary key,
  round_id int not null references public.rounds(id),
  member_id smallint not null references public.members(id) on delete cascade,
  ol_key text,                                  -- Open Library work key, e.g. /works/OL27482W
  title text not null check (char_length(title) between 1 and 200),
  author text check (char_length(author) <= 200),
  cover_url text,
  pages int,
  pages_source text check (pages_source in ('openlibrary','admin')),
  status text not null default 'active'
    check (status in ('active','pending','withdrawn','pulled','won','lost')),
  created_at timestamptz not null default now(),
  ended_at timestamptz
);
-- one live pick per person per round
create unique index books_one_live_pick on public.books (round_id, member_id)
  where status in ('active','pending');

create table public.votes (
  round_id int not null references public.rounds(id),
  member_id smallint not null references public.members(id) on delete cascade,
  book_id bigint not null references public.books(id) on delete cascade,
  points smallint not null check (points between 1 and 2),
  primary key (member_id, book_id)
);

create table public.notes (
  id bigint generated always as identity primary key,
  book_id bigint not null references public.books(id) on delete cascade,
  member_id smallint not null references public.members(id) on delete cascade,
  body text not null check (char_length(body) between 1 and 500),
  created_at timestamptz not null default now()
);

create table public.messages (
  id bigint generated always as identity primary key,
  member_id smallint references public.members(id) on delete cascade,
  kind text not null default 'chat' check (kind in ('chat','system')),
  body text not null check (char_length(body) between 1 and 500),
  created_at timestamptz not null default now()
);

create table public.log (
  id bigint generated always as identity primary key,
  member_id smallint references public.members(id) on delete cascade,
  kind text not null,
  text text not null,
  created_at timestamptz not null default now()
);

create table public.facts (
  id int generated always as identity primary key,
  body text not null
);

-- Daily Reading: sayings rotate one per day (Pacific time); likes pile up in one shared pool per day
create table public.sayings (
  id int primary key,
  body text not null check (char_length(body) between 1 and 200)
);

create table public.saying_likes (
  day date not null,
  member_id smallint not null references public.members(id) on delete cascade,
  n int not null default 0 check (n >= 0),
  primary key (day, member_id)
);

-- Crystal Ball of Encouragement and Love: every finished day's saying + its likes, saved for good
create table public.love_notes (
  day date primary key,
  body text not null,
  likes int not null default 0
);

-- ---------- read-only access for everyone ----------
do $$
declare t text;
begin
  foreach t in array array['members','rounds','books','votes','notes','messages','log','facts',
                           'sayings','saying_likes','love_notes'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('create policy "anyone can read" on public.%I for select to anon, authenticated using (true)', t);
    execute format('revoke insert, update, delete, truncate on public.%I from anon, authenticated', t);
  end loop;
end $$;
revoke all on schema private from anon, authenticated;

-- live updates
alter publication supabase_realtime add table
  public.members, public.books, public.votes, public.notes, public.messages, public.log, public.rounds,
  public.saying_likes;

-- ---------- helpers ----------
create function private.norm_code(p text) returns text
language sql immutable as $$
  select trim(regexp_replace(lower(coalesce(p,'')), '[^a-z]+', ' ', 'g'))
$$;

create function private.member_id_for(p_token text) returns smallint
language plpgsql security definer set search_path = '' as $$
declare v smallint;
begin
  select s.member_id into v from private.sessions s
   where s.token_hash = encode(extensions.digest(coalesce(p_token,''), 'sha256'), 'hex');
  if v is null then raise exception 'You need to sign in first.'; end if;
  return v;
end $$;

create function private.open_round() returns public.rounds
language plpgsql security definer set search_path = '' as $$
declare r public.rounds;
begin
  select * into r from public.rounds where status = 'open';
  if not found then raise exception 'The shelf is closed right now.'; end if;
  return r;
end $$;

create function private.clean(p text, p_max int default 500) returns text
language plpgsql immutable as $$
declare v text := trim(coalesce(p,''));
begin
  if v = '' then raise exception 'Type something first.'; end if;
  if char_length(v) > p_max then raise exception 'That is too long (max % characters).', p_max; end if;
  return v;
end $$;

create function private.add_log(p_member smallint, p_kind text, p_text text) returns void
language sql security definer set search_path = '' as $$
  insert into public.log (member_id, kind, text) values (p_member, p_kind, p_text);
$$;

create function private.sys_msg(p_member smallint, p_text text) returns void
language sql security definer set search_path = '' as $$
  insert into public.messages (member_id, kind, body) values (p_member, 'system', left(p_text, 500));
$$;

create function private.member_name(p_id smallint) returns text
language sql stable security definer set search_path = '' as $$
  select name from public.members where id = p_id;
$$;

create function private.require_admin(p_token text) returns smallint
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.member_id_for(p_token);
begin
  if not (select is_admin from public.members where id = v) then raise exception 'That''s an admin thing.'; end if;
  return v;
end $$;

-- ---------- login ----------
-- Returns {ok, token, member} or {ok:false, error}. Never raises on a wrong code,
-- so the failed-attempt counter is saved.
create function public.login(p_name text, p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare m public.members; s private.member_secrets; tok text;
begin
  select * into m from public.members where lower(name) = lower(trim(coalesce(p_name,'')));
  if not found then return jsonb_build_object('ok', false, 'error', 'Who are you?'); end if;
  select * into s from private.member_secrets where member_id = m.id for update;
  if not found or s.code_hash is null then
    return jsonb_build_object('ok', false, 'error', 'You don''t have a code yet.');
  end if;
  if s.locked_until is not null and s.locked_until > now() then
    return jsonb_build_object('ok', false, 'error', 'Too many wrong guesses. Try again in a few minutes.');
  end if;
  if s.code_hash <> extensions.crypt(private.norm_code(p_code), s.code_hash) then
    update private.member_secrets
       set failed_attempts = case when failed_attempts + 1 >= 5 then 0 else failed_attempts + 1 end,
           locked_until   = case when failed_attempts + 1 >= 5 then now() + interval '10 minutes' else null end
     where member_id = m.id;
    return jsonb_build_object('ok', false, 'error', format('Nope. The real %s would know that.', m.name));
  end if;
  update private.member_secrets set failed_attempts = 0, locked_until = null where member_id = m.id;
  tok := encode(extensions.gen_random_bytes(32), 'hex');
  insert into private.sessions (token_hash, member_id)
       values (encode(extensions.digest(tok, 'sha256'), 'hex'), m.id);
  return jsonb_build_object('ok', true, 'token', tok, 'member', to_jsonb(m));
end $$;

create function public.me(p_token text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare v smallint;
begin
  select s.member_id into v from private.sessions s
   where s.token_hash = encode(extensions.digest(coalesce(p_token,''), 'sha256'), 'hex');
  if v is null then return null; end if;
  return (select to_jsonb(m) from public.members m where m.id = v);
end $$;

create function public.logout(p_token text) returns void
language sql security definer set search_path = '' as $$
  delete from private.sessions
   where token_hash = encode(extensions.digest(coalesce(p_token,''), 'sha256'), 'hex');
$$;

-- ---------- first-time setup: color + font ----------
create function public.setup_profile(p_token text, p_color text, p_font text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.member_id_for(p_token); was_done boolean; m public.members;
begin
  if p_color not in ('#ff6b6b','#ff9f43','#ffd166','#c5e063','#7bd88f','#4fd1c5','#6ec6ff',
                     '#8fa8ff','#b99cff','#e58cff','#ff8fb8','#ffb38a','#f4e1b0','#d9b38c') then
    raise exception 'Pick one of the colors on the list.';
  end if;
  if p_font not in ('Lobster','Special Elite','IM Fell English SC','UnifrakturMaguntia','Henny Penny',
                    'Fredericka the Great','Homemade Apple','Amatic SC','Mountains of Christmas','Creepster') then
    raise exception 'Pick one of the fonts on the list.';
  end if;
  select setup_done into was_done from public.members where id = v;
  begin
    update public.members set color = p_color, font = p_font, setup_done = true where id = v
      returning * into m;
  exception when unique_violation then
    raise exception 'Someone just grabbed that color. Pick another!';
  end;
  if not was_done then
    perform private.add_log(v, 'join', format('%s joined Book Club', m.name));
  end if;
  return to_jsonb(m);
end $$;

-- ---------- voting: 3 bookmarks per person, max 2 on one book ----------
create function public.set_vote(p_token text, p_book_id bigint, p_points int) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.member_id_for(p_token); r public.rounds := private.open_round();
        b public.books; used int; old int;
begin
  if p_points < 0 or p_points > 2 then raise exception 'You can put 0, 1 or 2 🔖 on a book.'; end if;
  select * into b from public.books where id = p_book_id;
  if not found or b.round_id <> r.id or b.status <> 'active' then
    raise exception 'That book is not up for votes right now.';
  end if;
  select coalesce(sum(points),0) into used from public.votes
   where member_id = v and round_id = r.id and book_id <> p_book_id;
  if used + p_points > 3 then
    raise exception 'You only get 3 🔖. Take one back from another book first.';
  end if;
  select points into old from public.votes where member_id = v and book_id = p_book_id;
  if p_points = 0 then
    delete from public.votes where member_id = v and book_id = p_book_id;
  else
    insert into public.votes (round_id, member_id, book_id, points) values (r.id, v, p_book_id, p_points)
    on conflict (member_id, book_id) do update set points = excluded.points;
  end if;
  if coalesce(old,0) <> p_points then
    perform private.add_log(v, 'vote', case
      when p_points = 0 then format('%s took their bookmark out of %s', private.member_name(v), b.title)
      when p_points = 2 then format('%s put a BIG VOTE (🔖🔖) in %s', private.member_name(v), b.title)
      else format('%s put a 🔖 in %s', private.member_name(v), b.title) end);
  end if;
end $$;

-- ---------- notes + chat ----------
create function public.add_note(p_token text, p_book_id bigint, p_body text) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.member_id_for(p_token);
begin
  if not exists (select 1 from public.books where id = p_book_id) then raise exception 'No such book.'; end if;
  insert into public.notes (book_id, member_id, body) values (p_book_id, v, private.clean(p_body));
end $$;

create function public.send_message(p_token text, p_body text) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.member_id_for(p_token);
begin
  insert into public.messages (member_id, body) values (v, private.clean(p_body));
end $$;

-- ---------- returning your pick early ----------
create function public.withdraw_book(p_token text) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.member_id_for(p_token); r public.rounds := private.open_round(); b public.books;
begin
  select * into b from public.books where round_id = r.id and member_id = v and status in ('active','pending');
  if not found then raise exception 'You have nothing on the shelf to return.'; end if;
  update public.books set status = 'withdrawn', ended_at = now() where id = b.id;
  delete from public.votes where book_id = b.id;
  update public.members set late_fees = late_fees + 1 where id = v;
  perform private.add_log(v, 'withdraw', format('%s returned %s early (+1 late fee)', private.member_name(v), b.title));
  perform private.sys_msg(v, format('📕 %s returned %s early. Tsk tsk. +1 late fee.', private.member_name(v), b.title));
end $$;

-- ---------- called only by the server function after it looks the book up on Open Library ----------
create function public.member_for_token(p_token text) returns smallint
language sql security definer set search_path = '' as $$
  select private.member_id_for(p_token);
$$;

create function public.add_book_internal(p_member smallint, p_key text, p_title text, p_author text,
                                         p_cover text, p_pages int, p_status text) returns public.books
language plpgsql security definer set search_path = '' as $$
declare r public.rounds := private.open_round(); b public.books;
begin
  begin
    insert into public.books (round_id, member_id, ol_key, title, author, cover_url, pages, pages_source, status)
    values (r.id, p_member, p_key, private.clean(p_title, 200), nullif(left(trim(coalesce(p_author,'')), 200), ''),
            p_cover, p_pages, case when p_pages is null then null else 'openlibrary' end, p_status)
    returning * into b;
  exception when unique_violation then
    raise exception 'You already have a book on the shelf. Return it first (late fee!).';
  end;
  if p_status = 'pending' then
    perform private.add_log(p_member, 'suggest', format('%s suggested %s (needs a page count check)', private.member_name(p_member), b.title));
    perform private.sys_msg(p_member, format('📖 %s suggested %s. It needs a quick page count check first.', private.member_name(p_member), b.title));
  else
    perform private.add_log(p_member, 'suggest', format('%s put %s on the shelf (~%s pages)', private.member_name(p_member), b.title, b.pages));
    perform private.sys_msg(p_member, format('📖 %s put %s on the shelf!', private.member_name(p_member), b.title));
  end if;
  return b;
end $$;

-- ---------- admin ----------
create function public.approve_book(p_token text, p_book_id bigint, p_pages int) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.require_admin(p_token); r public.rounds := private.open_round(); b public.books;
begin
  select * into b from public.books where id = p_book_id and status = 'pending';
  if not found then raise exception 'That book is not waiting for a check.'; end if;
  if p_pages is null or p_pages <= 0 then raise exception 'Enter how many pages it has.'; end if;
  if p_pages > r.max_pages + 60 then
    update public.books set status = 'pulled', pages = p_pages, pages_source = 'admin', ended_at = now() where id = b.id;
    perform private.add_log(v, 'pull', format('%s is too long (%s pages), back to the library it goes', b.title, p_pages));
    perform private.sys_msg(v, format('🚫 %s is too long (%s pages). Pick something else!', b.title, p_pages));
  else
    update public.books set status = 'active', pages = p_pages, pages_source = 'admin' where id = b.id;
    perform private.add_log(v, 'approve', format('%s passed the page check (%s pages)', b.title, p_pages));
    perform private.sys_msg(v, format('✅ %s passed the page check and is on the shelf!', b.title));
  end if;
end $$;

create function public.pull_book(p_token text, p_book_id bigint) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.require_admin(p_token); b public.books;
begin
  select * into b from public.books where id = p_book_id and status in ('active','pending');
  if not found then raise exception 'That book is not on the shelf.'; end if;
  update public.books set status = 'pulled', ended_at = now() where id = b.id;
  delete from public.votes where book_id = b.id;
  perform private.add_log(v, 'pull', format('%s was taken off the shelf', b.title));
end $$;

create function public.close_round(p_token text) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.require_admin(p_token); r public.rounds := private.open_round(); w record;
begin
  select b.id, b.title, b.member_id, coalesce(sum(vt.points),0) marks into w
    from public.books b left join public.votes vt on vt.book_id = b.id
   where b.round_id = r.id and b.status = 'active'
   group by b.id order by marks desc, b.created_at asc limit 1;
  if w.id is null then raise exception 'There are no books on the shelf to pick from.'; end if;
  update public.books set status = 'won', ended_at = now() where id = w.id;
  update public.books set status = 'lost', ended_at = now() where round_id = r.id and status in ('active','pending');
  update public.rounds set status = 'closed', closed_at = now(), winner_book_id = w.id where id = r.id;
  insert into public.rounds (name, max_pages) values (format('Shelf %s', r.id + 1), r.max_pages);
  perform private.add_log(v, 'round', format('We''re reading %s (picked by %s) 📚', w.title, private.member_name(w.member_id)));
  perform private.sys_msg(v, format('📚 WE HAVE A WINNER: %s! The shelf is cleared, start picking again.', w.title));
end $$;

-- set a member's secret code (run by the setup script with the service key only)
create function public.set_member_code(p_name text, p_code text) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint;
begin
  select id into v from public.members where name = p_name;
  if v is null then raise exception 'No member named %', p_name; end if;
  insert into private.member_secrets (member_id, code_hash)
       values (v, extensions.crypt(private.norm_code(p_code), extensions.gen_salt('bf', 8)))
  on conflict (member_id) do update set code_hash = excluded.code_hash, failed_attempts = 0, locked_until = null;
  delete from private.sessions where member_id = v;
end $$;

-- ---------- Daily Reading likes ----------
create function private.club_today() returns date
language sql stable set search_path = '' as $$
  select (now() at time zone 'America/Los_Angeles')::date
$$;

-- Add a batch of taps for today. The browser batches them: never more than 40 per call,
-- and nobody can pile on more than 5000 a day.
create function public.smash_like(p_token text, p_count int) returns int
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.member_id_for(p_token);
        d date := private.club_today();
        c int := least(greatest(coalesce(p_count, 0), 0), 40);
        total int;
begin
  if c > 0 then
    insert into public.saying_likes (day, member_id, n) values (d, v, c)
    on conflict (day, member_id) do update set n = least(public.saying_likes.n + excluded.n, 5000);
  end if;
  select coalesce(sum(n), 0) into total from public.saying_likes where day = d;
  return total;
end $$;

-- same rotation the page uses: days since 1970-01-01, mod the number of sayings, by id order
create function private.saying_for(d date) returns text
language sql stable set search_path = '' as $$
  select body from public.sayings order by id
  offset ((d - date '1970-01-01') % greatest((select count(*) from public.sayings), 1)) limit 1
$$;

-- files every finished day (launch day up to yesterday) that isn't saved yet;
-- a finished day's likes can't change anymore, so saving late is still exact
create function public.archive_love_notes() returns void
language sql security definer set search_path = '' as $$
  insert into public.love_notes (day, body, likes)
  select g::date, private.saying_for(g::date),
         coalesce((select sum(n) from public.saying_likes l where l.day = g::date), 0)
    from generate_series(date '2026-11-15', private.club_today() - 1, interval '1 day') g
  on conflict (day) do nothing
$$;

-- ---------- who can call what ----------
revoke execute on all functions in schema public from public, anon, authenticated;
revoke execute on all functions in schema private from public, anon, authenticated;
grant execute on function
  public.login(text,text), public.me(text), public.logout(text),
  public.setup_profile(text,text,text), public.set_vote(text,bigint,int),
  public.add_note(text,bigint,text), public.send_message(text,text), public.withdraw_book(text),
  public.approve_book(text,bigint,int), public.pull_book(text,bigint), public.close_round(text),
  public.smash_like(text,int), public.archive_love_notes()
to anon, authenticated;
grant execute on function
  public.member_for_token(text),
  public.add_book_internal(smallint,text,text,text,text,int,text),
  public.set_member_code(text,text)
to service_role;

-- ---------- seed ----------
insert into public.members (name, is_admin) values
  ('Hannah',false),('Junior',false),('Katie',false),('Sarah',false),('Anthony',false),
  ('Giselle',false),('Michael',false),('Kat',false),('Kalon',false),('Matt',true);

insert into public.rounds (name, max_pages) values ('Shelf 1', 300);

insert into public.sayings (id, body) values
(1,  $s$I will always believe in you. Even when you pick a 600-page book.$s$),
(2,  $s$You are the main character. Everyone else is just a side character who thinks you're cool.$s$),
(3,  $s$If you were a book, I would never dog-ear your pages.$s$),
(4,  $s$You're not behind. You're just reading the footnotes.$s$),
(5,  $s$You're my favorite plot twist.$s$),
(6,  $s$I'd lend you my favorite book. And I don't lend that one to anybody.$s$),
(7,  $s$You're the reason the group chat is worth opening.$s$),
(8,  $s$Even in the sad chapters, you've got this.$s$),
(9,  $s$You're doing great, sweetie. The next chapter is a good one.$s$),
(10, $s$If life were a book club, I'd want you to pick every book.$s$),
(11, $s$You are a five-star read. No notes.$s$),
(12, $s$Somebody out there brags about knowing you. It's me. I'm somebody.$s$),
(13, $s$You don't need the SparkNotes. You're figuring it out beautifully.$s$),
(14, $s$You have the energy of a brand-new library card.$s$),
(15, $s$You're a first edition. Signed. Extremely rare.$s$),
(16, $s$It's okay to put the book down for a while. The story will wait for you. So will we.$s$),
(17, $s$Today's forecast: 100% chance you crush it.$s$),
(18, $s$I'm proud of you. Embarrassing-mom-at-the-recital proud.$s$),
(19, $s$You make the whole world feel like a cozy reading nook.$s$),
(20, $s$Drink some water. Main characters stay hydrated.$s$),
(21, $s$You've survived 100% of your worst chapters so far. That's a perfect record.$s$),
(22, $s$You're not a typo. You're the best line on the page.$s$),
(23, $s$You're the kind of friend people write whole books about.$s$),
(24, $s$You deserve a confetti cannon just for showing up today.$s$),
(25, $s$Remember: you're the hero of this story.$s$),
(26, $s$Even your late fees are kind of adorable.$s$),
(27, $s$You're the happy ending I didn't see coming.$s$),
(28, $s$Bad days are just slow chapters. It picks up, I promise.$s$),
(29, $s$If you were a book, I'd give you five stars and buy the special edition.$s$),
(30, $s$You are loved more than a bookstore cat on a rainy afternoon.$s$);
