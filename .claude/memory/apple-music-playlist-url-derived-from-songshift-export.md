---
name: apple-music-playlist-url-derived-from-songshift-export
description: The importer derives the Apple Music playlist URL from SongShift pl.* identifiers and stores it in playlist_url.
metadata:
  type: project
---

When a SongShift export is for Apple Music and includes a `pl.` playlist
identifier, `scripts/songshift_to_hugo.py` derives
`https://music.apple.com/us/playlist/<playlist-id>` and stores it in
`playlist_url`.
