---
name: source-uses-straight-quotes
description: Markdown source uses straight quotes and apostrophes; Hugo's Goldmark typographer renders them as curly, so never hand-type curly characters.
metadata:
  type: project
---

`STYLE.md` calls for curly quotation marks and apostrophes on the rendered site,
and the site does render them that way. That conversion happens at build time:
Hugo's Goldmark typographer extension is on by default and turns `"` into `"`
and `'` into `'` in the HTML output.

So the convention in `content/**/*.md` is **straight quotes and straight
apostrophes**. Both published technology posts follow it, and hand-typing curly
characters into source produces identical output while making the source
inconsistent with every other file.

Check the rendered result rather than the source when verifying typography:

```sh
grep -o 'wasn[^ ]*t' public/<slug>/index.html
```

See [[site-renders-via-papermod-submodule]] for the rest of the build path.
