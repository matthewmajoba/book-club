-- Short stories from inside a bigger book (e.g. "Best New Horror" from 20th Century Ghosts).
-- The pick's title is the story; from_title is the book it lives in. Open Library doesn't know
-- how long a single story is, so these always wait for a page check by the admin.
alter table public.books add column from_title text check (char_length(from_title) <= 200);

drop function public.add_book_internal(smallint, text, text, text, text, int, text);

create function public.add_book_internal(p_member smallint, p_key text, p_title text, p_author text,
                                         p_cover text, p_pages int, p_status text, p_from text default null)
returns public.books
language plpgsql security definer set search_path = '' as $$
declare r public.rounds := private.open_round(); b public.books; what text;
begin
  begin
    insert into public.books (round_id, member_id, ol_key, title, author, cover_url, pages, pages_source, status, from_title)
    values (r.id, p_member, p_key, private.clean(p_title, 200), nullif(left(trim(coalesce(p_author,'')), 200), ''),
            p_cover, p_pages, case when p_pages is null then null else 'openlibrary' end, p_status,
            nullif(left(trim(coalesce(p_from,'')), 200), ''))
    returning * into b;
  exception when unique_violation then
    raise exception 'You already have a book on the shelf. Return it first (late fee!).';
  end;
  what := case when b.from_title is null then b.title else format('"%s" (from %s)', b.title, b.from_title) end;
  if p_status = 'pending' then
    perform private.add_log(p_member, 'suggest', format('%s suggested %s (needs a page count check)', private.member_name(p_member), what));
    perform private.sys_msg(p_member, format('📖 %s suggested %s. It needs a quick page count check first.', private.member_name(p_member), what));
  else
    perform private.add_log(p_member, 'suggest', format('%s put %s on the shelf (~%s pages)', private.member_name(p_member), what, b.pages));
    perform private.sys_msg(p_member, format('📖 %s put %s on the shelf!', private.member_name(p_member), what));
  end if;
  return b;
end $$;

revoke execute on function public.add_book_internal(smallint,text,text,text,text,int,text,text) from public, anon, authenticated;
grant execute on function public.add_book_internal(smallint,text,text,text,text,int,text,text) to service_role;
