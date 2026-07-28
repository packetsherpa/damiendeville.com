# damiendeville.com

Source for Damien DeVille's writing on technology, life, and music. Built with
[Hugo](https://gohugo.io/) and the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed to
GitHub Pages.

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
hugo new content music/a-show.md
```

New content is a draft (`draft: true`) until you set `draft: false`.

See **[WRITING.md](WRITING.md)** for the full guide, including page bundles,
front matter, gotchas, and publishing from a phone or tablet.

### Images

- **Header image:** set `cover.image` in front matter. For a per-post image,
  make the post a page bundle (a folder with `index.md`) and drop the image in
  it — see `content/technology/it-wasnt-air-gapped/` for a working example.
- **In-body image:** `![Descriptive alt text](photo.jpg)` with the file in the
  post's bundle folder.

## Publishing

Set `draft: false`, commit, and push to `main`. GitHub Actions builds and
deploys the site. That is the whole flow.

## Production build

```sh
hugo --gc --minify
```

The generated `public/` directory is git-ignored; CI builds it on every push to
`main`.
