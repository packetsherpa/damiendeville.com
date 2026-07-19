# Playlist Expansion Plan

This document captures the next implementation step after the current uncommitted daily-playlist automation work. It is intentionally a design and execution plan only; it does not describe code that has already been shipped beyond the files currently modified in the working tree.

## Current working tree baseline

The repository already has the following local, uncommitted playlist automation work:

- `scripts/songshift_to_hugo.py`
  - Parses SongShift exports.
  - Derives Apple Music `playlist_url` values automatically when the export contains a `pl.` Apple Music playlist identifier.
- `scripts/sync_daily_playlists.py`
  - Watches date-named SongShift exports in `~/Documents/playlists`.
  - Creates published Hugo daily playlist pages for newly seen exports.
  - Maintains local state in `.playlist-sync-state.json`.
- `scripts/publish_new_playlists.sh`
  - Refuses to auto-publish from a dirty worktree.
  - Pulls, syncs, validates, commits playlist-page changes, and pushes.
- `content/music/daily/2026-07-01.md` through `content/music/daily/2026-07-19.md`
  - July 11, 2026 is intentionally absent.
- `PLAYLIST_AUTOMATION.md`
  - Documents the current SongShift-to-Hugo automation flow.
- `.gitignore`
  - Ignores Python cache files and local playlist sync state.

## Goal

Extend the current Apple Music-first workflow so that a newly dropped SongShift export can eventually:

1. Create or update the Apple Music-backed Hugo page.
2. Create corresponding Spotify and TIDAL playlists.
3. Store all playlist URLs in the page front matter.
4. Publish the site.
5. Create a Threads post linking to the site page.
6. Create three reply posts linking to the Apple Music, Spotify, and TIDAL playlists.
7. Store the Threads permalink and reply identifiers back in the page.

## Recommended rollout order

Implement this in three phases rather than all at once.

### Phase 1: Spotify support

Add Spotify playlist creation and URL capture while keeping Apple Music as the source of truth.

Why first:

- Spotify has a verified official API path for search, playlist creation, and playlist population.
- It is the lowest-risk next step.
- It exercises the cross-service matching model without forcing Threads or TIDAL to be solved in the same change.

### Phase 2: Threads posting

Add Threads publishing after the site page is live.

Why second:

- The Threads post should link to the final site page, so it belongs after the page has been pushed and deployed.
- The root post plus reply chain can be designed to be idempotent if we store returned Threads identifiers in front matter.

### Phase 3: TIDAL support

Add TIDAL only after confirming whether the account and developer app have reliable playlist-write capability through the official API.

Why third:

- Spotify and Threads can be built confidently now.
- TIDAL documentation clearly supports app registration and user authorization, but playlist-write availability for this specific use case still needs confirmation before implementation.
- If official playlist creation proves unavailable or impractical, browser automation can remain a contained fallback for TIDAL only.

## Target content model

Keep the current `playlist_url` field as the canonical Apple Music link for backward compatibility, and extend the flat front matter model rather than introducing a nested object.

Target additional fields:

```yaml
playlist_url: https://music.apple.com/us/playlist/...
spotify_url: https://open.spotify.com/playlist/...
tidal_url: https://tidal.com/browse/playlist/...
threads_url: https://www.threads.com/@.../post/...
threads_root_id: "..."
threads_apple_reply_id: "..."
threads_spotify_reply_id: "..."
threads_tidal_reply_id: "..."
```

Rationale:

- Matches the existing front matter style.
- Minimizes Hugo template complexity.
- Keeps Pages CMS form fields straightforward.
- Makes reruns and repair tasks easier because identifiers live with the content entry they belong to.

## File-by-file implementation plan

### `layouts/_default/single.html`

Current state:

- Renders `playlist_url`, `threads_url`, and `setlist_url`.

Planned change:

- Replace the single generic playlist link with service-specific links.
- Suggested rendering order:
  - `Apple Music` from `playlist_url`
  - `Spotify` from `spotify_url`
  - `TIDAL` from `tidal_url`
  - `Threads` from `threads_url`
- Preserve existing `setlist_url` behavior for show pages.

### `.pages.yml`

Current state:

- Exposes `playlist_url` and `threads_url` only.

Planned change:

- Add editable string fields for:
  - `spotify_url`
  - `tidal_url`
- Keep `threads_url` editable for manual repair.
- Do not expose `threads_root_id` or reply IDs in the CMS form unless operationally necessary.

### `archetypes/daily-playlist.md`

Current state:

- Contains Apple Music-era playlist fields only.

Planned change:

- Add empty placeholders for:
  - `spotify_url`
  - `tidal_url`
  - `threads_root_id`
  - `threads_apple_reply_id`
  - `threads_spotify_reply_id`
  - `threads_tidal_reply_id`

### `_templates/Daily Playlist.md`

Current state:

- Mirrors the current playlist fields for manual writing workflows.

Planned change:

- Keep it aligned with the updated daily-playlist archetype.

### `scripts/songshift_to_hugo.py`

Current state:

- Converts SongShift exports into Hugo entries.
- Derives Apple Music `playlist_url`.

Planned change:

- Leave Apple Music derivation as-is.
- Do not add Spotify or TIDAL creation logic here.

Reason:

- This script should remain a pure parser/renderer.
- Cross-service publishing belongs in orchestration scripts, not in the basic importer.

### `scripts/sync_daily_playlists.py`

Current state:

- Creates new daily playlist pages or backfills Apple Music URLs for existing entries.

Planned change:

- Continue to own page creation only.
- Optionally add support for preserving any later-added cross-service URLs if a page is regenerated, but avoid turning this into the main orchestration layer.

### `scripts/publish_new_playlists.sh`

Current state:

- Syncs new pages, validates, commits changed `content/music/daily/*`, and pushes.

Planned change:

- Evolve this from "page publisher" into a coordinator that calls smaller steps in sequence.
- Likely split responsibilities into helper scripts instead of making this shell file too large.

Suggested end-state sequence:

1. `git pull --ff-only`
2. `python3 scripts/sync_daily_playlists.py`
3. Detect newly created or changed playlist pages
4. `python3 scripts/enrich_playlists_with_spotify.py`
5. `python3 scripts/enrich_playlists_with_tidal.py`
6. Run tests and Hugo build
7. Commit and push page updates
8. Wait for deployed page availability
9. `python3 scripts/post_playlists_to_threads.py`
10. Commit and push Threads URL / reply ID updates

This means the future workflow should use two commits:

- Commit A: content + service playlist URLs
- Commit B: Threads permalink and reply identifiers

### New script: `scripts/enrich_playlists_with_spotify.py`

Purpose:

- Read one or more daily playlist pages.
- Match tracks against Spotify.
- Create or update the Spotify playlist for each page.
- Write `spotify_url` back into front matter.

Expected inputs:

- Hugo page path(s)
- Spotify credentials via environment variables or a local secret file not committed to Git

Expected outputs:

- Updated page front matter
- Structured log of matched, ambiguous, and missing tracks

Matching strategy:

- Search with track + artist + album.
- Prefer exact artist matches.
- Prefer album matches when available.
- Allow a conservative fallback when title and primary artist match but album differs because of remasters, deluxe editions, or singles.

Safety rules:

- If too many tracks fail matching, stop and report instead of publishing a partial playlist silently.
- If the playlist already exists, replace its contents rather than creating duplicates with the same date.

### New script: `scripts/enrich_playlists_with_tidal.py`

Purpose:

- Same shape as the Spotify enrichment script, but for TIDAL.

Implementation note:

- Build this only after validating the preferred official API path.
- If official playlist-write support is not viable, isolate browser automation behind the same script interface so the rest of the pipeline does not need to change.

### New script: `scripts/post_playlists_to_threads.py`

Purpose:

- Publish the site-linked Threads root post and three service-link replies.
- Store the resulting Threads URL and post IDs in the corresponding Hugo page.

Inputs:

- Hugo page path
- Final page URL, derived from:
  - `baseURL` in `hugo.toml`
  - the page date / section path
- Threads API credentials and user token

Suggested post shape:

- Root post:
  - short daily copy
  - link to the site page
- Reply 1:
  - Apple Music link
- Reply 2:
  - Spotify link
- Reply 3:
  - TIDAL link

Idempotency rules:

- If `threads_root_id` already exists, do not create a second root post.
- If reply IDs exist, skip recreating them unless an explicit repair mode is requested.
- If only `threads_url` is missing but `threads_root_id` exists, fetch or reconstruct the permalink if the API supports it.

### New optional script: `scripts/wait_for_playlist_page.py`

Purpose:

- Poll the public site URL after push and before Threads posting.

Reason:

- Threads should link to a live page, not a soon-to-be-live page.
- This keeps the deploy-wait logic separate from playlist creation logic.

## Secrets and credential design

Do not commit credentials.

Recommended local environment variables:

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REFRESH_TOKEN`
- `SPOTIFY_USER_ID`
- `TIDAL_CLIENT_ID`
- `TIDAL_CLIENT_SECRET`
- `TIDAL_REFRESH_TOKEN`
- `THREADS_APP_ID`
- `THREADS_APP_SECRET`
- `THREADS_USER_ACCESS_TOKEN`
- `THREADS_USER_ID`

If the Threads integration requires longer-lived refresh handling, add:

- `THREADS_REFRESH_TOKEN`

If a local file is preferred instead of shell environment variables, use an ignored `.env.local` or equivalent repo-external secret source.

## Automation choice impact

This plan works with either automation model currently under consideration.

### `launchd` watcher

Best for:

- Near-immediate reaction when a file lands in `~/Documents/playlists`

Tradeoff:

- More operating-system-specific setup

### Codex cron automation

Best for:

- Easier operational management inside Codex

Tradeoff:

- Polling delay rather than immediate reaction

Important note:

- The automation trigger should stay separate from the orchestration design.
- The same repo scripts should work no matter how they are invoked.

## Failure handling design

Treat the pipeline as resumable rather than all-or-nothing.

Suggested checkpoints:

1. Page created
2. Spotify URL written
3. TIDAL URL written
4. Page pushed
5. Threads root post created
6. Threads replies created

On rerun:

- Skip completed checkpoints based on front matter.
- Repair only the missing or failed portion.

Examples:

- If Spotify succeeds and TIDAL fails, keep the page and retry TIDAL later.
- If the site is pushed but Threads posting fails, retry only Threads.
- If the root Threads post succeeds and one reply fails, retry only the missing reply.

## Suggested implementation checkpoints

### Checkpoint 1

Implement and ship:

- `spotify_url` front matter field
- Spotify enrichment script
- Template and CMS updates for Spotify link rendering

### Checkpoint 2

Implement and ship:

- Threads posting script
- `threads_root_id` and reply ID persistence
- deploy wait/poll script

### Checkpoint 3

Implement and ship:

- TIDAL integration through verified API or browser automation fallback
- `tidal_url` rendering and persistence

## Open questions to resolve before implementation

1. Should Spotify and TIDAL playlists be public by default?
2. Should reruns replace playlist contents or create a fresh dated playlist if one already exists?
3. What exact Threads copy should the root post use by default?
4. Should reply order always be Apple Music, Spotify, TIDAL?
5. Do we want the automation to stop if one service is unavailable, or publish what is ready and mark the rest for repair?
6. If TIDAL remains API-uncertain, is browser automation acceptable for production use on this Mac?

## Recommendation

Start implementation with Spotify and Threads, using the current uncommitted repo work as the base. Treat TIDAL as a separate validation track before code is written for it. That approach gives the project a working multi-service publishing pipeline quickly, while containing the only uncertain integration behind a later decision.
