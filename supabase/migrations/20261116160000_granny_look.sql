-- The granny-square redesign renamed the look choices (js/look.js): colorway is now the yarn
-- (rainbow, harvest, ...), wallpaper is a real photo (granny, doilies, ...), frame is a crochet border
-- (rounds, shell, ...). Old names still work (the site falls back to the defaults), but point the
-- defaults and an untouched row at the new ones.
alter table public.club_look alter column colorway set default 'rainbow';
alter table public.club_look alter column wallpaper set default 'granny';
alter table public.club_look alter column frame set default 'rounds';

update public.club_look set colorway = 'rainbow', wallpaper = 'granny', frame = 'rounds'
where colorway = 'claret' and wallpaper = 'floral' and frame = 'rule';
