---
name: split-from-steady-org
description: This repo was split out of steady.org on 2026-08-02; technology writing lives here, music and personal writing stay at steady.org.
metadata:
  type: project
---

On 2026-08-02 the single `steady.org` site was split in two. This repo
(`packetsherpa.org`) took the technology writing; `steady.org` kept music and
personal writing. Both are Hugo + PaperMod on GitHub Pages, one repo each.

This repo was created by cloning `steady.org` rather than starting empty, so
**git history before the split is shared between the two repos**. Commits
touching music content appear in this repo's log even though those files are
gone, and vice versa. That is expected — do not treat it as a mistake or try to
rewrite it.

Consequences:

- Technology notes belong here. Music, show, and personal notes belong in
  `steady.org`. Neither repo should grow the other's section back.
- `STYLE.md` was forked at the split: this copy covers technology writing only,
  and the music and personal-post guidance lives in the `steady.org` copy. A
  change to shared voice guidance has to be applied to both.
- Damien explicitly deferred redirects from the old `steady.org/technology/*`
  URLs on 2026-08-02 — readership was negligible and GitHub Pages cannot issue a
  301 without putting Cloudflare in front. Those URLs are expected to 404 once
  `steady.org` drops its technology section.

See [[posts-publish-at-site-root]] and [[site-deploys-from-main]].
