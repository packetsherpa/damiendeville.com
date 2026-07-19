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
    album: Album title
```

Commentary remains ordinary Markdown below the front matter.

## Parser phase

The SongShift text export uses one seven-field playlist header followed by five-field track rows:

```text
***playlist*** | SongShift | export timestamp | playlist date | status | service | playlist ID
track | artist | album | service | track ID
```

The repository importer preserves track order and album data, detects duplicate service identifiers, and reports malformed rows rather than guessing.

Generate a reviewable draft with:

```sh
python3 scripts/songshift_to_hugo.py path/to/export.txt \
  --output content/music/daily/YYYY-MM-DD.md
```

Optional flags add the description, playlist URL, Threads URL, image path, and image description. The importer always creates a draft so commentary can be reviewed before publication.

When the SongShift export service is `Apple Music` and the header includes a `pl.` playlist identifier, the importer can derive `playlist_url` automatically as `https://music.apple.com/us/playlist/<playlist-id>`. Keep passing `--playlist-url` if you want to override that default or point to another service instead.

Pages CMS remains the recovery and manual-editing interface.

## Automated import and publish

For unattended publishing from a local `~/Documents/playlists` drop folder, the repository now includes two helper scripts:

- `python3 scripts/sync_daily_playlists.py`
- `./scripts/publish_new_playlists.sh`

`sync_daily_playlists.py` watches only date-named SongShift exports such as `2026.07.19.txt`. On its first run it creates `.playlist-sync-state.json` and marks the current folder contents as already seen so the automation can start from "now" without importing the entire historical archive. After that, new or changed exports create `content/music/daily/YYYY-MM-DD.md` when the page does not already exist, and can backfill a blank `playlist_url` on an existing page.

`publish_new_playlists.sh` is the end-to-end publisher. It:

1. Refuses to run if the repository already has local changes.
2. Pulls `main` with `--ff-only`.
3. Runs `sync_daily_playlists.py`.
4. Exits early if no playlist page changed.
5. Runs the playlist tests and the Hugo production build.
6. Commits only the changed files under `content/music/daily/`.
7. Pushes `main`, which triggers the existing GitHub Pages deployment.

You can test the pipeline without publishing by running:

```sh
./scripts/publish_new_playlists.sh --dry-run
```

### Option 1: macOS folder watcher

If you want "as soon as I drop a file in the folder" behavior, use a `launchd` agent with `WatchPaths` pointing at `~/Documents/playlists` and run:

```sh
/Users/damien/Documents/GitHub/damiendeville.com/scripts/publish_new_playlists.sh
```

This is the closest thing to a true file-drop automation on macOS.

### Option 2: Codex scheduled automation

If you prefer an app-managed workflow, create a Codex cron automation that runs every 10 to 15 minutes against this repository and calls:

```sh
./scripts/publish_new_playlists.sh
```

This is simpler to manage inside Codex, but it polls instead of reacting instantly to a new file.
