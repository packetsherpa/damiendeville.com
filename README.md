# Default Deny

Source for **Default Deny** — Damien DeVille's writing on security, artificial
intelligence, complex systems, and technical leadership, published at
[packetsherpa.org](https://packetsherpa.org/). Built with
[Hugo](https://gohugo.io/) and the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed to
GitHub Pages.

Music and personal writing live separately, at
[steady.org](https://steady.org/) ([repo](https://github.com/packetsherpa/steady.org)).

## Setup

The theme is a git submodule, so after cloning fetch it once:

```sh
git submodule update --init --recursive
```

## Local development

```sh
hugo server -D
```

The local site is available at `http://localhost:1313/`. `-D` includes drafts.

## Writing a post

```sh
hugo new content technology/my-note.md
```

`technology` matches its archetype (`archetypes/technology.md`) by section name
automatically. New content is a draft (`draft: true`) until you set
`draft: false`.

Posts live under `content/technology/` but publish at the site root — a post in
`content/technology/my-note/` is served at `https://packetsherpa.org/my-note/`.
The `/technology/` URL is the Archive listing.

See **[WRITING.md](WRITING.md)** for the full guide, including page bundles,
front matter, gotchas, and publishing from a phone or tablet.

### Images

- **Header image:** set `cover.image` in front matter. For a per-post image,
  make the post a page bundle (a folder with `index.md`) and drop the image in
  it — see `content/technology/it-wasnt-air-gapped/` for a working example.
  PaperMod generates a responsive `srcset` and WebP variants at build time
  (`cover.responsiveImages = true` in `hugo.toml`).
- **In-body image:** `![Descriptive alt text](photo.jpg)` with the file in the
  post's bundle folder. `layouts/_markup/render-image.html` resizes it, converts
  it to WebP, and emits a `srcset`, so a full-resolution camera file is fine to
  commit.

## Publishing

Set `draft: false`, commit, and push to `main`. GitHub Actions builds and
deploys the site. That is the whole flow.

## Production build

```sh
hugo --gc --minify
```

The generated `public/` directory is git-ignored; CI builds it on every push to
`main`.
