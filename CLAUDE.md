# CLAUDE.md

**Read [`AGENTS.md`](AGENTS.md) first.** This file exists so Claude Code finds the
guidance by the name it looks for; the content lives in one place on purpose.

The thing most likely to cost you an hour:

> **On Windows, clone with `git -c core.longpaths=true`.** The
> `mining-drone-animation/…` paths exceed the 260-character limit. Without it the
> clone fails partway, prints `Filename too long`, and *still leaves a
> populated-looking directory* with an empty index — so files look absent when they
> are present, and a commit from that state deletes everything you did not add.
>
> Sanity check any checkout with `git ls-files | wc -l` → **615**. To ask whether a
> file exists, use `git ls-tree -r --name-only origin/main`, not the filesystem.

Also:

- **Raster art is Git LFS.** Pointer files are not corruption; do not "repair" them.
- **Prototype state is deliberate** — failure conditions disabled, free building in
  testing mode, prototype saves at `user://brine_save.json`. Not bugs.
- **Do not refactor `scripts/main.gd` (2,952 lines) unasked.** The project is
  optimising for finding what is fun, not for architecture. Propose, don't perform.
- **Keep `.uid` files paired with their `.gd`.**

Godot 4.6, entry point `res://scenes/main.tscn`. Rights: [`NOTICE.md`](NOTICE.md).
