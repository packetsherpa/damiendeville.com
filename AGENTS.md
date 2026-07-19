# damiendeville.com — Agent Instructions

Hugo source for Damien DeVille's publication on technology, leadership, and music, including the daily playlist intake and publishing workflow.

This file is the single source of truth for any agent working in this repo
(Claude Code, Codex, or others). `CLAUDE.md` is a symlink to this file. Global
conventions live in `~/.claude/CLAUDE.md` — do not restate them here. This file
covers only what is specific to damiendeville.com.

## What This Tool Is

This repository builds and deploys a Hugo site at `https://damiendeville.com/`.
The core content areas are:

- `content/technology/` for technology notes
- `content/music/` for daily playlists, listening notes, and show notes

Important local commands:

- `hugo server --buildDrafts`
- `hugo --gc --minify --panicOnWarning`
- `python3 -m unittest tests.test_songshift_to_hugo tests.test_sync_daily_playlists`
- `python3 scripts/sync_daily_playlists.py`
- `./scripts/publish_new_playlists.sh --dry-run`

Important workflow docs:

- `PUBLISHING.md` for manual writing and publishing
- `PLAYLIST_AUTOMATION.md` for the current playlist automation flow
- `PLAYLIST_EXPANSION_PLAN.md` for the planned Spotify / TIDAL / Threads expansion

Gotchas:

- The public site is deployed from `main` through `.github/workflows/pages.yml`.
- Daily playlist pages are stored as flat files under `content/music/daily/`.
- `playlist_url` currently means the Apple Music playlist URL.
- July 11, 2026 is intentionally missing from the current July daily-playlist archive.

## On Session Start

1. Read `project-context.md` — the authoritative live state (what is in flight, blocked, and the next starting point).
2. Run `git status --short --branch` and `git log --oneline -5`.
3. State the current task before starting; if it is not obvious, ask.

## Coordination with Other Agents

More than one agent may work this repo. To avoid conflict:

- Treat `project-context.md` as the shared handoff document.
- Do not assume the working tree reflects only your prior changes — check `git status` and `git log` before editing.
- Prefer clear task ownership before parallel work; avoid editing the same files as another agent unless explicitly asked.

## Durable Memory

Durable facts, decisions, and landmines live in `.claude/memory/` as one-fact
files (frontmatter: `name`, `description`, `metadata.type`; linked with
`[[slug]]`). When something becomes durable, add a one-fact file and a line in
`.claude/memory/MEMORY.md` — do not bury it in `project-context.md`.

@.claude/memory/MEMORY.md
