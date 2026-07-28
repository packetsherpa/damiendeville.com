# Steady (steady.org) — Live State

> Live state only: what is in flight, blocked, and next. Durable facts live in
> `.claude/memory/` (see `.claude/memory/MEMORY.md`). Changelog lives in git
> history.

## Goal

Maintain and publish **Steady** (steady.org), Damien DeVille's writing-first
Hugo site — technology notes, music writing, and personal posts — with a
low-friction "write markdown locally, push to `main`" workflow.

## Active Work

- The site was rebuilt writing-first: the daily-playlist archive, the SongShift
  automation, the browser CMS, and the bespoke layouts were removed. Rendering
  now comes from the PaperMod theme (git submodule under `themes/PaperMod`).
- Surviving content: one technology note (`it-wasnt-air-gapped`), one live-show
  note (Death Cab for Cutie at Merriweather), and the about page.
- Renaming the site to **Steady** at **steady.org**. Repo changes done
  (`static/CNAME`, `baseURL`, site title, docs). Going live still needs DNS for
  steady.org pointed at GitHub Pages and the custom domain set in Pages
  settings. The old damiendeville.com is being retired (no redirect).

## Blockers

- None.

## Next

- Write posts. New technology notes and music/show notes are the main work.
- Optional polish: a favicon and site OpenGraph image, and a short bio block on
  the home page if desired (PaperMod `homeInfoParams`).
