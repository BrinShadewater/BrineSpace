# AGENTS.md — 🛰️ working on BrineSpace

A Godot 4.7 passive roguelite station builder. `project.godot` sets
`run/main_scene="res://scenes/title_screen.tscn"`, config name `BrineSpace`, a 1920×1080 design
viewport and a 1600×900 default window.

Start with [`docs/CURRENT_STATUS.md`](docs/CURRENT_STATUS.md) for accepted
direction, the latest recorded acceptance and remaining work. Read the north star
and relevant implementation notes in [`docs/DEVELOPMENT_NOTES.md`](docs/DEVELOPMENT_NOTES.md)
before changing gameplay. [`NOTICE.md`](NOTICE.md) governs rights.

Dated handoffs and archived notes preserve evidence, not a current task list.
Later owner decisions govern intended behavior; current code shows implementation,
and dated test reports establish only the revision and scope they actually tested.
Update CURRENT_STATUS.md at a meaningful change of direction or acceptance milestone.

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

**Name whole `res://` paths. Never a folder prefix joined to a built name.** Two
tools read your source as if it were data, and both get a prefix wrong:

- A rename or a move can only rewrite *whole quoted paths*. The September 18 art move
  (`3d4e0fed9`) relocated 798 files and rewrote 385 source files, and its "zero dangling
  references" was true and useless: 102 paths assembled at runtime — a `const ROOT`
  joined to a filename, `"…/pack/%s.png" % key`, `"…/" + id + "-v1.png"` — were invisible
  to it. The whole seabed and every station foundation drew nothing for two days,
  because a missing PNG is a warning plus a magenta placeholder and nothing asserts on it.
- `tools/build_release_manifest.py` expands a quoted folder prefix into *that entire
  folder*, **including inside a comment**. The rooms root shipped 80 files and 101 MB to
  deliver three `machine.png`.

So: a `const` map of whole paths, not a prefix and a suffix. `tests/test_reliability.gd`
now fails if any `res://` artwork the station loads reaches the placeholder — that is the
cheap guard this class of bug went without.

## 🚫 Prototype state that is deliberate, not broken

The README is explicit that this is mid-prototype. Do not "fix" these:

- **Normal runs spend room costs and enforce resource failure conditions.**
  Timed directives and scenario victory were retired at the owner's request;
  current loops conclude through Conclude Expedition. Do not restore old deadlines.
- **Only dedicated fixtures opt into free building or disabled failures.** Do not
  turn those flags on to make a gameplay or balance test pass.
- **Hidden recipes stay hidden** until functioning rooms discover them. Three
  consecutive functioning cycles stabilize a pattern: its per-cycle bonus doubles in
  every later loop, it pays Archived Data, and its related blueprint costs half.
  Stabilising no longer decrypts a room — blueprints, crew and companions are bought
  with Archived Data on the Meta Progression page (`scripts/meta_shop.gd`).
- **Crew and companions met in a loop play for the rest of it** and must be bought to
  return in later loops. What a profile already owned stays owned and free.
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
| `project.godot`, `scenes/title_screen.tscn` | Project entry point; `scenes/main.tscn` is gameplay |
| `scripts/` | Game logic — `main`, `grid_canvas`, `room_database`, `orbit_manager`, `synergy_manager`, `meta_state` |
| `rooms/` | Room definitions and art |
| `rooms/tileset-library/` | Registry of the bought prop library, floor finishes, and the owner's Studio marks (`favourites`, `retired`, `names`, `categories` — owner data, never reset from git) |
| `assets/new-tilesets/` | Converted bought art, one folder per in-universe set; Git LFS |
| `vendor-art/` | The bought packs exactly as shipped; gitignored. The tileset repair tools read them through `--sources`; do not delete |
| `docs/TILESET_LIBRARY_HANDOFF_2026-09-20.md` | Start here for the bought art library: what exists, how the owner reports problems, the pipeline and what is open |
| `legacy/` | The earlier room and prop art, moved aside: `default/` was live in rooms, `retired/` was not |
| `Brine icons/` | Icon set, multiple sizes, with sprite-sheet sources |
| `brinecore-animation/` | BRINE core room animation study — its own scene and scripts |
| `mining-drone-animation/` | Directional drone animation frames (the deep paths) |
| `brineui/`, `character/` | UI and character art |
| `docs/DEVELOPMENT_NOTES.md` | North star, current focus, known limits |

Icons ship at several sizes with sources alongside — regenerate from the source
rather than upscaling a smaller export. Room art and card thumbnails load from PNG at
runtime so new assets need no editor import step; preserve that if you touch loading.

## 🔍 Diagnostics when something is slow or wrong

F7 draws the performance overlay: frame graph, per-system times (crew, drones, cryo,
airlocks, interface, grid draw), path-search counts and the session's error count.
F8 saves a report. A stall (a frame over 400 ms, or under 20 FPS for two seconds)
saves its own report with the seconds before it, at most three a session — and only
in a real play session: anything started with `-s` (tests, tools, probes) has
automatic capture and breadcrumbs off, so runs never write into the player's folders.

- `scripts/error_watch.gd` groups logged errors; every report lists them.
- `scripts/stuck_watch.gd` warns when crew, drones or build orders stop progressing.
- `user://last_session.json` holds breadcrumbs a hard crash cannot erase;
  `user://session_stats.csv` gets one line per finished loop.
- `tools/soak_test.gd` runs a save headless for N cycles and reports where the time
  went; `tests/test_soak_budget.gd` is the gate that fails on a slow frame.
- `tools/bake_room_cards_v2.gd` re-renders card art from the current room designs
  (including the owner's saved Studio layouts) into `assets/room-cards-v2`.
- `tools/lint_room_layouts.gd` checks what the Layout Studio does not. Free placement is
  the Studio's default and `issues()` returns nothing in that mode, so a prop can be saved
  standing in a doorway, on top of another prop or off the hull with no warning — five
  doorways were blocked that way before anyone noticed, and crew simply could not walk
  through them. It sweeps all 188 room/rotations headless using the same rule the
  navigation graph uses, writes `output/layout-lint.json` and exits non-zero on findings.
  Its blocked-door check is rigorous - it is the rule the navigation graph uses. Its
  overlap and off-hull checks only compare props that record their floor contact, and are
  cosmetic: 25 off-hull placements and one overlap remain, all the owner's, all theirs to
  judge. Not a CI gate. `--rooms=a,b` narrows it.

Department colours live in `RoomDatabase.CATEGORY_COLORS` with per-room overrides in
`ROOM_COLORS`; use `RoomDatabase.room_color(id)` so corridors stay grey and BRINE's
core stays AI white. Interface text uses the bundled Barlow Semi Condensed
(`scripts/ui_fonts.gd`, SIL OFL in `assets/fonts/OFL.txt`); the station log keeps a
monospace face.

## 🗣️ BRINE's voice

BRINE is a damaged AI core with opinions, and they are *not always comforting*. Dry,
a little haunted, never chirpy:

> *"I have mapped thirty-seven ways to run out of oxygen. I recommend none of them."*

If you write user-facing text, match that. Do not make BRINE friendly or helpful.

## Run and validate relevant work

Follow README.md's Run locally section: open project.godot with Godot 4.7
(locally tested with 4.7.2), complete imports, and use F5 for the configured title
scene. Choose tests or audit tools for the changed subsystem from tests/ and tools/;
`python tools/run_tests.py --subsystem <name>` runs a group from tests/index.json
with native-only tests routed correctly (`--list` classifies; `--native` runs the
render-bound lane on a real display). Scope searches to `scripts/ rooms/ tests/
tools/ docs/ assets/`: `output/` holds hundreds of thousands of generated snapshot
files, including stale copies of the source tree, and walking it times searches out. Do not equate a headless or
manifest check with visual acceptance, and do not run unrelated full asset batches
merely for a documentation change.

Before treating a failing layout or Studio test as a regression, check the owner
decisions that make the Studio show what the live game hides: dressing and
`library/common-` decorations are filtered from live rooms, free placement is the
Studio default (so `issues()` reports nothing until the toggle is off), and wall
decorations are paused in `rooms/whole-room/decoration_props.gd`. Guard coverage of
a paused feature behind the same flag instead of deleting it. In fixtures, wait for
observable state rather than a fixed delay — a fixed wait after a scene swap is the
known flake pattern — and when a failure is unexplained, print the real per-frame
state with a temporary probe before editing the test.

For playable exports, follow [docs/RELEASE_WORKFLOW.md](docs/RELEASE_WORKFLOW.md) and
use the maintained release exporter. Keep editor/PCK checks separate from actual
release gameplay; release assertions must never contain required side effects.
