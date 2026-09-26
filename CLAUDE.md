# CLAUDE.md

**Read [`AGENTS.md`](AGENTS.md) first.** This file exists so Claude Code finds the
guidance by the name it looks for; the content lives in one place on purpose.

Before cloning or trusting a fresh checkout, read the long-paths warning in
AGENTS.md — a bad Windows clone looks complete but has an empty index.

Also:

- **Raster art is Git LFS.** Pointer files are not corruption; do not "repair" them.
- **Name whole `res://` paths, never a folder prefix plus a built name.** A rename can
  only rewrite whole literals, and the release manifest expands a quoted folder into the
  whole folder — even in a comment. Both bit hard; see AGENTS.md.
- **Normal runs spend costs and enforce failures.** Free builds and disabled
  failures are isolated fixture options; saves remain at `user://brine_save.json`.
- **Do not refactor `scripts/main.gd` unasked.** The project is
  optimising for finding what is fun, not for architecture. Propose, don't perform.
- **Keep `.uid` files paired with their `.gd`.**

Godot 4.7 (tested with 4.7.2). `project.godot` runs `res://scenes/title_screen.tscn`;
`res://scenes/main.tscn` is gameplay, which most fixtures instantiate directly.
Rights: [`NOTICE.md`](NOTICE.md).
