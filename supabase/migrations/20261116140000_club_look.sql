-- The club's look: name, tagline, colors, wallpaper and border pattern.
-- One row, readable by everyone, changed only by the admin through set_look().
-- The pattern ids are drawn by the front end (js/look.js); unknown ids fall back to the defaults there.

create table public.club_look (
  id smallint primary key default 1 check (id = 1),
  club_name text not null default 'Book Club' check (char_length(club_name) between 1 and 40),
  tagline text not null default '★ like game club but for books ★' check (char_length(tagline) <= 80),
  colorway text not null default 'claret' check (colorway ~ '^[a-z0-9-]{1,24}$'),
  wallpaper text not null default 'floral' check (wallpaper ~ '^[a-z0-9-]{1,24}$'),
  frame text not null default 'rule' check (frame ~ '^[a-z0-9-]{1,24}$'),
  updated_at timestamptz not null default now()
);
insert into public.club_look default values;

alter table public.club_look enable row level security;
create policy "anyone can read" on public.club_look for select to anon, authenticated using (true);
revoke insert, update, delete, truncate on public.club_look from anon, authenticated;
alter publication supabase_realtime add table public.club_look;

create function public.set_look(p_token text, p_name text, p_tagline text,
                                 p_colorway text, p_wallpaper text, p_frame text) returns public.club_look
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.require_admin(p_token); r public.club_look;
begin
  update public.club_look set
    club_name = private.clean(p_name, 40),
    tagline   = left(trim(coalesce(p_tagline, '')), 80),
    colorway  = lower(trim(p_colorway)),
    wallpaper = lower(trim(p_wallpaper)),
    frame     = lower(trim(p_frame)),
    updated_at = now()
  where id = 1
  returning * into r;
  return r;
end $$;

revoke execute on function public.set_look(text,text,text,text,text,text) from public;
grant execute on function public.set_look(text,text,text,text,text,text) to anon, authenticated;
