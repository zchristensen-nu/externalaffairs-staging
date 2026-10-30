# External Affairs — staging

A migration of [externalaffairs.northeastern.edu](https://externalaffairs.northeastern.edu/) onto the Northeastern Design System (NUEAC-413), for review. Not the live site; every page is `noindex`.

- `build/build.py` composes the pages from the design system's components (`~/Projects/nu-homepage-prototype/design-system`) and the live site's content (`build/content.json`).
- `build/site.css` and `build/site.js` are page glue only: placement of components and the open/close behaviour of menus.
- `docs/` is the built output that GitHub Pages serves.

```bash
python3 build/build.py
```
