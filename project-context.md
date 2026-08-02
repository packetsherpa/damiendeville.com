# Packet Sherpa (packetsherpa.org) — Live State

> Live state only: what is in flight, blocked, and next. Durable facts live in
> `.claude/memory/` (see `.claude/memory/MEMORY.md`). Changelog lives in git
> history.

## Goal

Maintain and publish **Packet Sherpa** (packetsherpa.org), Damien DeVille's
technology writing — security, artificial intelligence, complex systems, and
technical leadership — with a low-friction "write markdown locally, push to
`main`" workflow.

## Active Work

- This repo was split out of `steady.org` on 2026-08-02, cloned with full git
  history so the three existing technology notes keep their commits. `steady.org`
  keeps music and personal writing; this repo takes technology. See
  [[split-from-steady-org]].
- Carried over: three technology notes (`it-wasnt-air-gapped`,
  `shadow-ai-is-a-demand-signal-not-a-policy-failure`,
  `egress-filtering-is-the-control-we-never-implemented`), the about page, the
  PaperMod submodule, the Pages workflow, and the `ideas/` staging tree.
- Posts publish at the site root (`/:slug/`) rather than `/technology/:slug/`;
  `/technology/` is now the Archive listing.
- Image optimization added: `cover.responsiveImages = true` plus a new in-body
  image render hook at `layouts/_markup/render-image.html`.

## Blockers

- **Not live yet.** Going live needs two manual steps outside this repo:
  1. DNS at Hover for `packetsherpa.org` — four apex `A` records to
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`,
     plus `CNAME www → packetsherpa.github.io`.
  2. GitHub repo Settings → Pages → set the custom domain to `packetsherpa.org`
     and enable Enforce HTTPS once the certificate is issued.
- `steady.org` still contains the technology section. It has not been cut down
  yet — that is a separate change in that repo.

## Next

- Land the DNS and Pages settings above, then confirm the live site.
- Cut `steady.org` down to music: delete `content/technology/`,
  `archetypes/technology.md`, `ideas/technology/`, fix its `hugo.toml`, and
  rewrite its about/home copy. No redirects — readership is negligible and
  Damien explicitly deferred them on 2026-08-02.
- Optional: add the same image render hook to `steady.org`.
- Write posts.
