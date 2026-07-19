# damiendeville.com

The source for Damien DeVille's technology-focused publication, built with Hugo and deployed to GitHub Pages.

See [PUBLISHING.md](PUBLISHING.md) for the complete manual writing, preview, and publishing workflow.

## Local development

```sh
hugo server --buildDrafts
```

The local site is available at `http://localhost:1313/`.

## Create content

Evergreen article:

```sh
hugo new content articles/my-article.md --kind article
```

Chronological note:

```sh
hugo new content notes/my-note.md --kind note
```

Daily playlist:

```sh
hugo new content music/daily/2026-07-18/index.md --kind daily-playlist
```

New content is a draft until `draft: false` is set in its front matter.

## Production build

```sh
hugo --gc --minify
```

The generated `public/` directory is intentionally ignored. GitHub Actions builds and deploys it on every push to `main`.
