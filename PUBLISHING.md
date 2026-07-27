# Publishing guide

This site is a collection of Markdown files built by Hugo and published by GitHub Pages. Pages CMS is the primary publishing interface for all posts, GitHub is the source of truth, and GitHub performs the Hugo production build automatically.

## Publish from Pages CMS

Open <https://app.pagescms.org/>, sign in with GitHub, and select this repository. Pages CMS commits directly to `main`; GitHub Actions then builds and deploys the site.

Use the collection that matches the post:

- **Technology Notes** for technology, security, AI, and leadership writing.
- **Listening Notes** for albums, artists, and other focused music writing.
- **Live Shows** for concert reports.
- **Daily Playlists** for the daily playlist archive.

New Technology Notes, Listening Notes, and Live Shows begin as drafts. Clear **Draft** only when the entry is ready for the public site.

## Daily playlists

Use Pages CMS for routine playlist creation and editing. Select **Daily Playlists**. The form manages filenames, metadata, tracks, and image paths and commits changes directly to GitHub.

The export-assisted workflow is documented in [PLAYLIST_AUTOMATION.md](PLAYLIST_AUTOMATION.md).

## One-time Obsidian setup

Open the repository folder as the `damiendeville.com` vault. Enable Obsidian's core **Templates** plugin, then set its template folder location to:

```text
_templates
```

The repository ignores `.obsidian/`, so each device keeps its own private workspace settings while sharing the same writing templates.

Use ordinary Markdown links and images in published content. Obsidian wiki links such as `[[Another note]]` are not rendered by this Hugo site.

## 1. Start with the latest site

### Mac

Open a terminal and run:

```sh
cd ~/Documents/GitHub/damiendeville.com
git pull --ff-only
```

Then open or return to the repository's Obsidian vault.

### iPhone or iPad

Close or leave Obsidian, open the linked repository in Working Copy, and pull. Reopen the vault in Obsidian after the pull completes.

## 2. Create an entry

For longer writing, create the file at the path shown below, open the command palette, choose **Templates: Insert template**, and select the matching template. Every template starts as a draft.

### Daily playlist

Pages CMS is the recommended interface. The Obsidian template remains available as an emergency fallback, but daily entries are stored as single files such as `content/music/daily/2026-07-18.md`.

### Listening note

```text
content/music/listening/artist-album/index.md
```

Insert **Listening Note**.

### Live show

Pages CMS is recommended. Select **Live Shows**, choose **New**, and complete the form. It creates a date-and-title Markdown file under `content/music/shows/`. Upload photographs through the Header image field or the editor's image control; Pages CMS stores them under `static/images/music/` and inserts a Hugo-ready image path.

### Technology note

```text
content/technology/note-title.md
```

Pages CMS is recommended. Select **Technology Notes**, choose **New**, and complete the form. Use the same form for short observations and longer, more developed pieces; the writing no longer needs to be classified before you begin.

Use lowercase, hyphenated folder and file names. The human-readable title comes from the `title` field inside the note.

## 3. Understand the front matter

The block between the `---` lines controls the page:

```yaml
---
title: "The title readers see"
date: 2026-07-18T21:00:00-04:00
draft: true
description: "A one-sentence summary."
tags:
  - ambient
  - electronic
---
```

- `title` appears on the page and in lists.
- `date` controls chronology.
- `draft: true` prevents production publication.
- `description` appears in list views and search previews.
- `tags` connect related entries.
- Music templates include additional self-explanatory fields such as `artist`, `venue`, `playlist_url`, and `threads_url`.

## 4. Write and preview

Obsidian provides a Markdown preview on every device. On the Mac, you can also preview the exact Hugo site by running:

Run:

```sh
hugo server --buildDrafts
```

Open <http://localhost:1313/>. Hugo refreshes the preview when you save a file. Stop the preview with `Control-C` in the terminal.

Drafts appear in the local Hugo preview because of `--buildDrafts`, but they do not appear on the public site. An exact Hugo preview is optional and is not required to publish from iOS.

## 5. Publish

When an entry is ready, change:

```yaml
draft: true
```

to:

```yaml
draft: false
```

On the Mac, optionally verify the production build:

```sh
hugo --gc --minify --panicOnWarning
```

### Publish from the Mac

Review and publish the change in the terminal:

```sh
git status --short
git diff
git add path/to/the/files-you-changed
git commit -m "Publish descriptive entry title"
git push origin main
```

GitHub Actions deploys `main` automatically. The workflow is visible in the repository's **Actions** tab, and the updated site normally appears within a few minutes.

### Publish from iPhone or iPad

1. Save the note in Obsidian.
2. Open Working Copy and review the modified files.
3. Commit with a descriptive message.
4. Push to `main`.
5. GitHub Actions builds and deploys the site automatically.

Pull before starting on another device, and avoid editing the same entry on two devices simultaneously.

## 6. Correct or update an entry

Edit its `index.md` or Markdown file, preview it, run the production build, and repeat the Git commands above. Git preserves the history of every published revision.

## Useful checks

```sh
git status --short --branch
hugo --gc --minify --panicOnWarning
```

If the production build fails, do not push. Read the first Hugo error, correct the referenced file, and run the build again.
