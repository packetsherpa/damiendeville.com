# damiendeville.com — Live State

> Live state only: what is in flight, blocked, and next. Durable facts live in
> `.claude/memory/` (see `.claude/memory/MEMORY.md`). Changelog lives in git
> history.

## Goal

Maintain and publish Damien DeVille's Hugo site, with an emphasis on the daily playlist workflow and the next-stage expansion into multi-service playlists and Threads posting.

## Active Work

- Daily playlist automation for Apple Music-backed SongShift exports is now in the repo.
- July 1-19, 2026 playlist pages have been generated, with July 11 intentionally absent.
- A concrete expansion design exists for Spotify, TIDAL, and Threads in `PLAYLIST_EXPANSION_PLAN.md`.
- The repo is being retrofitted to match the `tool-template` agent-config and memory standard.

## Blockers

- The Spotify / TIDAL / Threads expansion is designed but not implemented yet.
- TIDAL playlist-write capability still needs verification before implementation.

## Next

- Decide whether playlist automation should be triggered by a macOS folder watcher or a Codex cron job.
- When ready, implement the expansion plan in phases:
  1. Spotify playlist creation and URL persistence
  2. Threads posting after deploy
  3. TIDAL integration after API capability is confirmed
