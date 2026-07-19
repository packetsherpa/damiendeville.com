# damiendeville.com

The source for Damien DeVille's technology-focused publication, built with Hugo and deployed to GitHub Pages.

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

New content is a draft until `draft: false` is set in its front matter.

## Production build

```sh
hugo --gc --minify
```

The generated `public/` directory is intentionally ignored. GitHub Actions builds and deploys it on every push to `main`.

## Earlier writing

The preserved *Walking in Sober Boots* archive remains at <https://packetsherpa.github.io/soberboots/>.
