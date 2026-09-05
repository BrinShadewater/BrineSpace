# AGENTS.md — 🛰️ working on BrineSpace

A Godot 4.6 passive roguelite station builder. `project.godot` sets
`run/main_scene="res://scenes/main.tscn"`, config name `BRINE`, a 1920×1080 design
viewport and a 1600×900 default window.

Read [`docs/DEVELOPMENT_NOTES.md`](docs/DEVELOPMENT_NOTES.md) before changing
gameplay — it holds the north star, the current focus, and the known prototype
limits. [`NOTICE.md`](NOTICE.md) governs rights.

## ⚠️ Clone this repo correctly or you will get a broken checkout

**On Windows, clone with long paths enabled:**

```bash
git -c core.longpaths=true clone https://github.com/BrinShadewater/BrineSpace.git
```

`mining-drone-animation/animations/…` nests deeper than the 260-character Windows
path limit. Without `core.longpaths`, the clone **fails partway, prints
`Filename too long`, and still leaves a populated-looking directory** with an empty
index. That failure mode is vicious: the folder looks fine, so a `find` over it
reports files as absent that are in fact present, and a `git add` + `commit` from
that state records a tree containing only the files you added — i.e. a commit that
deletes everything else.

**Verify before trusting a checkout:** compare `git ls-files` with the checked-out
commit's `git ls-tree -r --name-only HEAD`; the index must not be empty or partial.
And when you want to know whether a file exists, ask git rather than the filesystem:

```bash
git ls-tree -r --name-only origin/main | grep project.godot
```

**Raster art is stored in Git LFS.** Without LFS installed you get pointer files
rather than images. A pointer file is not a corrupt image — do not "repair" one, and
never commit a large binary in a way that bypasses LFS.

## 🚫 Prototype state that is deliberate, not broken

The README is explicit that this is mid-prototype. Do not "fix" these:

- **Normal runs spend room costs and enforce failure/deadline conditions.**
- **Only dedicated fixtures opt into free building or disabled failures.** Do not
  turn those flags on to make a gameplay or balance test pass.
- **Hidden recipes stay hidden** until functioning rooms discover them. Three
  consecutive functioning cycles stabilize a pattern and unlock its reward.
- **Saves and unlocks are prototype-level**, written to `user://brine_save.json`
  and deliberately not versioned.

Each looks like a bug and is a decision. If one genuinely needs to change, that is a
gameplay call for the owner, not a tidy-up.

## 🧠 Before refactoring anything

`scripts/main.gd` is a large monolith, supported by the grid renderer and
data-driven room, run and discovery modules. The urge to split it is understandable.

Resist it unless asked. The stated north star is *discovering which placement
decisions become satisfying* — the project is optimising for learning what is fun,
not for architecture, and a large refactor mid-prototype costs the thing it is
actually trying to buy. Bring it up as a proposal; do not do it in passing.

`.uid` files sit beside each `.gd`. They are Godot's resource UIDs — **keep them
paired**, do not delete or regenerate them casually, and commit them with their
script.

## 🗺️ Layout

| Path | What it is |
|---|---|
| `project.godot`, `scenes/main.tscn` | Entry point |
| `scripts/` | Game logic — `main`, `grid_canvas`, `room_database`, `orbit_manager`, `synergy_manager`, `meta_state` |
| `rooms/` | Room definitions and art |
| `Brine icons/` | Icon set, multiple sizes, with sprite-sheet sources |
| `brinecore-animation/` | BRINE core room animation study — its own scene and scripts |
| `mining-drone-animation/` | Directional drone animation frames (the deep paths) |
| `brineui/`, `character/` | UI and character art |
| `docs/DEVELOPMENT_NOTES.md` | North star, current focus, known limits |

Icons ship at several sizes with sources alongside — regenerate from the source
rather than upscaling a smaller export. Room art and card thumbnails load from PNG at
runtime so new assets need no editor import step; preserve that if you touch loading.

## 🗣️ BRINE's voice

BRINE is a damaged AI core with opinions, and they are *not always comforting*. Dry,
a little haunted, never chirpy:

> *"I have mapped thirty-seven ways to run out of oxygen. I recommend none of them."*

If you write user-facing text, match that. Do not make BRINE friendly or helpful.
