# Memory

Durable facts, decisions, and landmines for Packet Sherpa (packetsherpa.org).
One file per fact. Live/churning state lives in `project-context.md`, not here.

- [Split out of steady.org](split-from-steady-org.md) — this repo took the technology writing on 2026-08-02; music stays at steady.org, and git history before the split is shared between the two repos.
- [Posts publish at the site root](posts-publish-at-site-root.md) — `content/technology/` maps to `/:slug/`; `/technology/` is the Archive listing.
- [Images are optimized at build time](images-are-optimized-at-build-time.md) — commit full-resolution originals; PaperMod and a render hook produce WebP srcsets.
- [Site deploys from main via GitHub Pages](site-deploys-from-main.md) — production deploys come from pushes to `main` through the Pages workflow.
- [Site renders via the PaperMod theme submodule](site-renders-via-papermod-submodule.md) — layouts come from `themes/PaperMod`, vendored as a git submodule; fetch it with `git submodule update --init --recursive`.
- [Markdown source uses straight quotes](source-uses-straight-quotes.md) — Goldmark's typographer converts them to curly at build time, so never hand-type curly characters into content.
