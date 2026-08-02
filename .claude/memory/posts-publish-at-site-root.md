---
name: posts-publish-at-site-root
description: Posts live in content/technology/ but publish at /:slug/; the /technology/ URL is the Archive listing.
metadata:
  type: project
---

Every post on this site is a technology note, so nesting them under
`/technology/` in the URL is redundant. `hugo.toml` carries:

```toml
[permalinks]
  technology = "/:slug/"
```

So `content/technology/my-note/index.md` is served at
`https://packetsherpa.org/my-note/`, while `/technology/` remains the section
listing — presented as the **Archive** page and linked from the main menu.

Consequences:

- A new top-level page (`content/whatever.md`) shares the root namespace with
  every post slug. Check for a collision before adding one; `about` is the only
  such page today.
- `mainSections = ["technology"]` still drives the home page listing, so the
  section name matters even though it is invisible in URLs.
- Renaming the `content/technology/` directory would silently change every post
  URL unless the `[permalinks]` key is renamed with it.

See [[split-from-steady-org]].
