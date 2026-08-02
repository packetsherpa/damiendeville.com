# Ideas

Staging ground for writing that isn't a draft yet: half-thoughts, links worth returning to, a scene or a line, a claim that needs checking. Nothing here is built or published — `ideas/` sits outside `content/`, so Hugo ignores it entirely. A file here can be as rough as one sentence.

## Layout

- `inbox/` — raw capture. Anything, unsorted, no structure required. Sweep it periodically into a section folder or `archive/`.
- `technology/` — developing technology notes.
- `archive/` — ideas that went nowhere, or whose file was promoted to `content/`. Kept rather than deleted, because dead ideas resurface.

## Flow

1. Capture into `inbox/` without thinking about where it belongs.
2. When an idea has a shape, move it to `technology/` and give it a real filename.
3. When it has a governing idea you can state in one sentence — the bar in `STYLE.md` — promote it: create the real post with `hugo new content technology/my-note.md`, move the thinking across, and drop the idea file in `archive/`.

## Shape of an idea file

No front matter, no schema — these are never rendered. What tends to be worth writing down:

```markdown
# Working title

The claim, or the question, in a sentence or two.

## Why it might hold

## Sources
- url — what it establishes

## Open
- what I'd need to check before publishing
```

Use it or don't. The only rule is that a file here is not a draft, and shouldn't be treated as one.

## Notes

- Committed to the repo on purpose, so ideas sync across machines and are capturable from a phone the same way posts are (see `WRITING.md`).
- Anything genuinely private is better kept out of this repo than kept here.
