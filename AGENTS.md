# damiendeville.com — Agent Instructions

Hugo source for Damien DeVille's writing on technology, life, and music.

This file is the single source of truth for any agent working in this repo
(Claude Code, Codex, or others). `CLAUDE.md` and `GEMINI.md` are symlinks to
this file. Global conventions live in `~/.claude/CLAUDE.md` — do not restate
them here. This file covers only what is specific to damiendeville.com.

## What This Tool Is

This repository builds and deploys a Hugo site at `https://damiendeville.com/`.
It is a writing-first personal publication. The content areas are:

- `content/technology/` for technology notes
- `content/music/` for listening notes and live-show notes
- `content/about.md` for the about page

The site renders through the [PaperMod](https://github.com/adityatelange/hugo-PaperMod)
theme, which is vendored as a git submodule under `themes/PaperMod`.

Important local commands:

- `git submodule update --init --recursive` — fetch the theme after a fresh clone
- `hugo server -D` — local preview at `http://localhost:1313/`, including drafts
- `hugo --gc --minify` — production build (matches CI)

Workflow docs:

- `README.md` for the writing, preview, and publishing workflow.

## Writing Style

`STYLE.md` is the writing standard for all reader-facing site content. Read and
apply it whenever creating or substantively editing technology notes, music
writing, show notes, or personal posts.

@STYLE.md

## Content conventions

- A post is a draft (`draft: true`) until you set `draft: false`; publishing is
  pushing a non-draft post to `main`.
- For a post with a header image, make it a page bundle (a folder with
  `index.md`) and set `cover.image` in front matter. See
  `content/technology/it-wasnt-air-gapped/` for a working example.
- In-body images use `![alt text](photo.jpg)` with the file in the post's
  bundle folder.

Gotchas:

- The public site is deployed from `main` through `.github/workflows/pages.yml`,
  which checks out submodules so the theme is present at build time.
- The theme is a submodule: after a fresh clone run
  `git submodule update --init --recursive`, or the build has no layouts.
- Do not use `hugo --panicOnWarning`: the current PaperMod release triggers two
  Hugo deprecation warnings (`LanguageDirection`, `LanguageCode`) that are
  theme-internal and harmless. CI does not use that flag.

## On Session Start

1. Read `project-context.md` — the authoritative live state (what is in flight,
   blocked, and the next starting point).
2. Run `git status --short --branch` and `git log --oneline -5`.
3. State the current task before starting; if it is not obvious, ask.

## Coordination with Other Agents

More than one agent may work this repo. To avoid conflict:

- Treat `project-context.md` as the shared handoff document.
- Do not assume the working tree reflects only your prior changes — check
  `git status` and `git log` before editing.
- Prefer clear task ownership before parallel work; avoid editing the same files
  as another agent unless explicitly asked.

## Durable Memory

Durable facts, decisions, and landmines live in `.claude/memory/` as one-fact
files (frontmatter: `name`, `description`, `metadata.type`; linked with
`[[slug]]`). When something becomes durable, add a one-fact file and a line in
`.claude/memory/MEMORY.md` — do not bury it in `project-context.md`.

@.claude/memory/MEMORY.md
