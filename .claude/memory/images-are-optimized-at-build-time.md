---
name: images-are-optimized-at-build-time
description: Both cover and in-body images are downscaled and converted to WebP by Hugo at build time, so commit full-resolution originals.
metadata:
  type: project
---

Commit the full-resolution camera file. Nothing needs pre-processing before a
post goes up, and no external image service is involved.

Two separate mechanisms handle it:

- **Cover images** — PaperMod's `_partials/cover.html` builds a responsive
  `srcset` with WebP variants. Gated on `params.cover.responsiveImages` (set to
  `true` in `hugo.toml`) **and** `params.env == "production"`, so `hugo server`
  deliberately skips it and serves originals for build speed.
- **In-body images** — `layouts/_markup/render-image.html`, a Hugo image render
  hook written for this repo. It turns `![alt](photo.jpg)` into a `srcset` at
  480/720/1080px plus a cap at the original width or 1440px, whichever is
  smaller, all WebP q82, with `loading="lazy"`. It runs in every environment.

The hook only processes **page resources** in JPEG, PNG, or WebP. Remote URLs,
files under `static/`, and formats Hugo cannot decode (SVG, GIF) fall through to
a plain `<img>` untouched — that fallback is intentional, not a gap.

Generated variants land in `resources/_gen/`, which is git-ignored, so CI
regenerates them on every build.

See [[site-renders-via-papermod-submodule]].
