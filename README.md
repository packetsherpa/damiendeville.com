# damiendeville.com

The source for Damien DeVille's publication on technology, life, and music, built with Hugo and deployed to GitHub Pages.

See [PUBLISHING.md](PUBLISHING.md) for the complete manual writing, preview, and publishing workflow.
See [PLAYLIST_AUTOMATION.md](PLAYLIST_AUTOMATION.md) for the daily playlist intake and automation design.

## Local development

```sh
hugo server --buildDrafts
```

The local site is available at `http://localhost:1313/`.

## Create content

Technology note:

```sh
hugo new content technology/my-note.md --kind technology
```

Daily playlist fallback:

```sh
hugo new content music/daily/2026-07-18.md --kind daily-playlist
```

New content is a draft until `draft: false` is set in its front matter.

## Production build

```sh
hugo --gc --minify
```

The generated `public/` directory is intentionally ignored. GitHub Actions builds and deploys it on every push to `main`.
