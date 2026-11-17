-- The default tagline loses its stars ("like game club but for books"). Only an untouched tagline changes;
-- one the admin wrote stays as it is.
alter table public.club_look alter column tagline set default 'like game club but for books';

update public.club_look set tagline = 'like game club but for books'
where tagline = '★ like game club but for books ★';
