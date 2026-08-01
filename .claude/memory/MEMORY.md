# Memory

Durable facts, decisions, and landmines for Steady (steady.org). One file per
fact. Live/churning state lives in `project-context.md`, not here.

- [Site deploys from main via GitHub Pages](site-deploys-from-main.md) — production deploys come from pushes to `main` through the Pages workflow.
- [Site renders via the PaperMod theme submodule](site-renders-via-papermod-submodule.md) — layouts come from `themes/PaperMod`, vendored as a git submodule; fetch it with `git submodule update --init --recursive`.
- [Markdown source uses straight quotes](source-uses-straight-quotes.md) — Goldmark's typographer converts them to curly at build time, so never hand-type curly characters into content.
