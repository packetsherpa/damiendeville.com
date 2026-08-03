# This repo is a mirror

Everything outside `.github/` in this repo is a copy of
[packetsherpa/packetsherpa.org](https://github.com/packetsherpa/packetsherpa.org),
overwritten hourly by `.github/workflows/pages.yml`. The `README.md`,
`AGENTS.md`, `CLAUDE.md`, and `project-context.md` you see here are upstream's
files describing upstream's repo — they are not about this repo.

**Do not write posts here.** Any change you commit outside `.github/` is
discarded at the next sync. Write in `packetsherpa.org` and push to its `main`;
this site picks the change up within the hour, or immediately if you run the
workflow by hand:

```
gh workflow run pages.yml --repo packetsherpa/damiendeville.com
```

## Why this exists

`packetsherpa.org` was registered in late July 2026 and some DNS filtering
services block newly registered domains on principle, so a share of readers
could not resolve it. `damiendeville.com` is an established domain and serves
the same site.

Both domains are live and serve identical content. Which one search engines
treat as the original is decided by `params.canonicalBaseURL` in upstream's
`hugo.toml` — a single value, honored by both builds through the local
`layouts/_partials/head.html` override. As of 2026-08-03 it points here, at
`https://damiendeville.com/`.

## Flipping canonical back

Once `packetsherpa.org` has aged out of the newly-registered-domain filters
(target: mid-September 2026, roughly 4–6 weeks after 2026-08-03), verify it
resolves on the filtering resolvers that were blocking it, then in the
**upstream** repo set:

```toml
canonicalBaseURL = "https://packetsherpa.org/"
```

Nothing in this repo changes. This site keeps serving the same content at
`damiendeville.com`; it just stops being the canonical origin.

## What is native to this repo

Only `.github/`. The sync deliberately drops upstream's `.github/` rather than
merging it, so a workflow added upstream never leaks in — `GITHUB_TOKEN` is not
permitted to push new workflow files, and such a leak would break every sync.
