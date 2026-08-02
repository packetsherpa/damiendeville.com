---
name: site-deploys-from-main
description: Production deploys come from pushes to main through the GitHub Pages workflow.
metadata:
  type: project
---

The production site at `https://packetsherpa.org/` is built and deployed by
`.github/workflows/pages.yml` whenever `main` is updated. The custom domain is
pinned by `static/CNAME`.

DNS lives at Hover: four apex `A` records to `185.199.108.153`,
`185.199.109.153`, `185.199.110.153`, and `185.199.111.153`, plus
`CNAME www → packetsherpa.github.io`. The custom domain and Enforce HTTPS are
set in the repo's Settings → Pages.

This is a **project** Pages site, not the user site. `packetsherpa.github.io` is
a separate repo serving separate content, and putting a custom domain on that
one would redirect every project site under the account beneath it.

See [[split-from-steady-org]].
