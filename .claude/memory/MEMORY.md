# Memory

Durable facts, decisions, and landmines for damiendeville.com. One file per
fact. Live/churning state lives in `project-context.md`, not here.

- [Site deploys from main via GitHub Pages](site-deploys-from-main.md) — production deploys come from pushes to `main` through the Pages workflow.
- [Daily playlists are flat markdown files](daily-playlists-are-flat-markdown-files.md) — daily entries live directly under `content/music/daily/` rather than bundle directories.
- [Apple Music playlist URL is derived from SongShift export](apple-music-playlist-url-derived-from-songshift-export.md) — the importer treats `playlist_url` as the Apple Music URL when a `pl.` identifier is present.
