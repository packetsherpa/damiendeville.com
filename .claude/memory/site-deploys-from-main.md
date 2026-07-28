---
name: site-deploys-from-main
description: Production deploys come from pushes to main through the GitHub Pages workflow.
metadata:
  type: project
---

The production site at `https://steady.org/` is built and deployed by
`.github/workflows/pages.yml` whenever `main` is updated. The custom domain is
pinned by `static/CNAME`.
