---
name: site-renders-via-papermod-submodule
description: The site's layouts come from the PaperMod theme, vendored as a git submodule under themes/PaperMod.
metadata:
  type: project
---

The site has no bespoke layouts. All rendering comes from the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, vendored as a
git submodule at `themes/PaperMod` and selected via `theme = "PaperMod"` in
`hugo.toml`.

Consequences:

- A fresh clone must run `git submodule update --init --recursive` before the
  site will build, and `.github/workflows/pages.yml` checks out submodules.
- Per-post header images use PaperMod's `cover.image` front matter; posts with
  images are page bundles (a folder with `index.md`).
- Swapping themes later is a one-line `theme` change in `hugo.toml` plus
  reconciling a few `[params]` values, because content uses standard Hugo front
  matter with no layout overrides.
