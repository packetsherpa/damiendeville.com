---
name: posts-publish-at-site-root
description: Posts live in content/technology/ but publish at /:contentbasename/, so the bundle folder name is the URL; /technology/ is the Archive listing.
metadata:
  type: project
---

Every post on this site is a technology note, so nesting them under
`/technology/` in the URL is redundant. `hugo.toml` carries:

```toml
[permalinks]
  technology = "/:contentbasename/"
```

So `content/technology/my-note/index.md` is served at
`https://packetsherpa.org/my-note/`, while `/technology/` remains the section
listing — presented as the **Archive** page and linked from the main menu.

**Use `:contentbasename`, not `:slug`.** This started as `/:slug/`, and on
2026-08-02 retitling a post silently changed its live URL: Hugo's `:slug` token
falls back to the **title** when no `slug:` is set in front matter, not to the
filename or bundle folder. `:contentbasename` resolves to the bundle folder name
for page bundles, so the URL is whatever the directory is called and a retitle
cannot move it. Do not switch back.

Consequences:

- The bundle folder name is the URL. Choose it deliberately, and renaming a
  folder is what changes a published URL — there is no redirect mechanism on
  GitHub Pages.
- A new top-level page (`content/whatever.md`) shares the root namespace with
  every post URL. Check for a collision before adding one; `about` is the only
  such page today.
- `mainSections = ["technology"]` still drives the home page listing, so the
  section name matters even though it is invisible in URLs.
- Renaming the `content/technology/` directory would silently change every post
  URL unless the `[permalinks]` key is renamed with it.

See [[split-from-steady-org]].
