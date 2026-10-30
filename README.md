# External Affairs — staging

A migration of [externalaffairs.northeastern.edu](https://externalaffairs.northeastern.edu/) onto the Northeastern Design System (NUEAC-413), for review. Not the live site; every page is `noindex`.

- `build/build.py` composes the pages from the design system's components (`~/Projects/nu-homepage-prototype/design-system`) and the live site's content (`build/content.json`).
- The page shell (header, footers, Explore sheet, page glue, menu behaviour) comes from the shared kit in `~/Projects/nu-site-kit`.
- `docs/` is the built output that GitHub Pages serves.

```bash
python3 build/build.py
```
