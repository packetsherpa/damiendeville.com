# Daily playlist automation

The normal daily workflow should not require direct Hugo, Git, folder, or image-path management.

## Manual fallback

Pages CMS provides a form backed by the `daily_playlists` collection in `.pages.yml`. It writes one Markdown file per day to `content/music/daily/`, stores uploaded images under `static/images/music/daily/`, commits the files to GitHub, and triggers the existing Pages deployment.

## Codex-assisted workflow

The intended routine is:

1. Send Codex a playlist export.
2. State the playlist date, or say that it is today's or tomorrow's playlist.
3. Optionally attach an image and provide the Threads or playlist URL.
4. Add any short context you want reflected in the introduction or commentary.
5. Codex normalizes the export into ordered `tracks` data, creates the dated Markdown file, places media correctly, validates the Hugo build, and presents the result for review.
6. After approval, Codex commits and pushes. GitHub Actions publishes the update.

The minimum input is the playlist export and intended date. Description, image, links, tags, and commentary can be added during review.

## Stable entry contract

Each entry is stored as `content/music/daily/YYYY-MM-DD.md` and contains:

```yaml
title: Daily Playlist — Month D, YYYY
date: YYYY-MM-DD
publishDate: YYYY-MM-DD
draft: false
description: A one-sentence summary.
music_kind: Daily playlist
playlist_url: https://...
threads_url: https://...
image: /images/music/daily/YYYY-MM-DD.jpeg
image_alt: A useful description of the image.
tags: []
tracks:
  - title: Track title
    artist: Artist name
```

Commentary remains ordinary Markdown below the front matter.

## Parser phase

Do not build an export parser until at least one representative raw export has been inspected. The parser should preserve track order, normalize artist and title fields without changing their meaning, detect duplicates, and report ambiguous rows rather than guessing.

Once the export format is known, the parser can become a small repository script invoked by Codex. Pages CMS remains the recovery and manual-editing interface.
