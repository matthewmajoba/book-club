-- Picks can be books, novellas or short stories, under 150 pages.
-- The "just this once cause I love you" grace is now 20% over the limit (151-180 pages at 150)
-- instead of a flat +60, so it scales with whatever the limit is.
alter table public.rounds alter column max_pages set default 150;
update public.rounds set max_pages = 150 where status = 'open';

create or replace function public.approve_book(p_token text, p_book_id bigint, p_pages int) returns void
language plpgsql security definer set search_path = '' as $$
declare v smallint := private.require_admin(p_token); r public.rounds := private.open_round(); b public.books;
begin
  select * into b from public.books where id = p_book_id and status = 'pending';
  if not found then raise exception 'That book is not waiting for a check.'; end if;
  if p_pages is null or p_pages <= 0 then raise exception 'Enter how many pages it has.'; end if;
  if p_pages > r.max_pages + round(r.max_pages * 0.2) then
    update public.books set status = 'pulled', pages = p_pages, pages_source = 'admin', ended_at = now() where id = b.id;
    perform private.add_log(v, 'pull', format('%s is too long (%s pages), back to the library it goes', b.title, p_pages));
    perform private.sys_msg(v, format('🚫 %s is too long (%s pages). Pick something else!', b.title, p_pages));
  else
    update public.books set status = 'active', pages = p_pages, pages_source = 'admin' where id = b.id;
    perform private.add_log(v, 'approve', format('%s passed the page check (%s pages)', b.title, p_pages));
    perform private.sys_msg(v, format('✅ %s passed the page check and is on the shelf!', b.title));
  end if;
end $$;
