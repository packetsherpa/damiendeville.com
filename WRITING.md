# Writing and publishing

How to write a post and put it live on https://steady.org/ (the site is named
**Steady**). It is [Hugo](https://gohugo.io/) + the PaperMod theme, deployed to
GitHub Pages. Publishing is nothing more than pushing Markdown to `main`.

## One-time setup (on a computer)

```sh
git clone https://github.com/packetsherpa/steady.org.git
cd steady.org
git submodule update --init --recursive   # pulls the PaperMod theme
```

Install Hugo (`brew install hugo` on macOS). No Node, no Python — just Hugo.

## The everyday loop

1. **Create the post.**

   ```sh
   hugo new content technology/my-note.md   # a technology note
   hugo new content music/a-show.md         # a music / show note
   ```

   This scaffolds the file from the matching archetype with `draft: true`.

2. **Write it.** Edit the front matter and body in Markdown. While
   `draft: true`, it is invisible to the world.

3. **Preview.**

   ```sh
   hugo server -D
   ```

   Open http://localhost:1313/ (`-D` shows drafts; it live-reloads on save).

4. **Publish.** Set `draft: false`, then:

   ```sh
   git add .
   git commit -m "Publish: my note title"
   git push          # to main
   ```

   Pushing to `main` triggers the GitHub Action, which builds and deploys in
   about half a minute. **Pushing to `main` is publishing** — there is no
   separate deploy step.

## Text-only post vs. post with a header image

A **text-only** post is a single `.md` file.

For a **header image**, make the post a *page bundle* — a folder with
`index.md` — and put the image inside it:

```
content/technology/my-note/
├── index.md
└── feature.jpg
```

Then in the front matter:

```yaml
cover:
  image: "feature.jpg"
  alt: "Describe what is visible in the image."
  relative: true          # required — see gotchas
```

For an image **inside the body**, put it in the same folder and reference it
inline:

```markdown
![Alt text describing the photo](photo.jpg)
```

Working examples to copy: `content/technology/it-wasnt-air-gapped/` and
`content/music/death-cab-for-cutie-merriweather-2026-07-21/`.

## Front matter reference

```yaml
---
title: "Your Title"
date: 2026-08-01
draft: true            # flip to false to publish
description: "One-sentence summary; shows on cards and link previews."
tags:
  - security
  - ai
cover:                 # optional; only for bundles that include an image
  image: "feature.jpg"
  alt: ""
  relative: true
---
```

Keep to these fields — standard front matter is what keeps the site portable
and makes a future theme swap a one-line change.

## Gotchas

- **`cover ... relative: true`** is required for a bundle's header image, or the
  social-share preview link 404s. On the page itself it looks fine either way,
  so it is easy to miss.
- **Do not run `hugo --panicOnWarning`.** The current PaperMod release triggers
  two harmless Hugo deprecation warnings that would fail the build under that
  flag. Use `hugo server -D` and `hugo --gc --minify` (what CI runs).
- The About page and section intros are Markdown too: `content/about.md`,
  `content/technology/_index.md`, `content/music/_index.md`.

## Publishing from a phone or tablet

The site is just Markdown files in a git repo, so anything that can edit a file
and push to `main` can publish. Ranked by how well each handles a real post
(including images):

1. **Working Copy (iOS/iPadOS) — best.** A full git client that clones the repo,
   pulls the theme submodule, creates folders (page bundles), adds photos from
   your camera roll, commits, and pushes to `main`. Pair it with iA Writer or
   its built-in editor (iA Writer opens the repo through the Files app). This is
   the only mobile path that cleanly handles a header image + bundle.

2. **GitHub in a browser or the GitHub mobile app — quickest for text.**
   Go to `content/technology/`, "Add file → Create new file", name it
   `my-note.md`, paste front matter + body, commit to `main`. Live in ~30s. To
   include an image without a computer, use "Add file → Upload files" and type a
   path like `content/technology/my-note/index.md` in the filename to create the
   folder, then upload the image into the same folder. Fiddlier than Working
   Copy, but it works.

3. **A browser CMS, if mobile becomes your main way to post.** A form-based
   editor (e.g. Pages CMS or Decap CMS) gives a phone-friendly title/body/image
   flow that commits for you. It adds back a little config that this rebuild
   deliberately cut, but it is the smoothest phone experience.

**Android:** same idea — a git client like Termux + git or MGit, plus any
Markdown editor. The GitHub web flow is identical.

**Previewing on mobile is the weak spot.** There is no easy local Hugo on a
phone. Two realistic options:

- Lean on drafts: keep `draft: true`, flip to `false` only when you are
  confident, and review the live post right after it deploys.
- Or set up deploy previews (Cloudflare Pages / Netlify) so pushing a branch
  gives a preview URL you can open on your phone before merging. Not configured
  today, but a clean add if you want it.

The same gotchas apply on mobile: keep `cover ... relative: true` for header
images, set `draft: false` to publish, and remember that pushing to `main`
publishes.
