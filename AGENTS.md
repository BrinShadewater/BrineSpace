# AGENTS.md — 🛰️ working on BrineSpace

A code-and-documentation snapshot of the Godot 4.7 passive roguelite station builder. `project.godot` sets
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

## Code-only GitHub snapshot

This repository contains code and documentation only. Media files and binary
resources used by the game remain in the owner's full local project. A fresh
GitHub clone is **not runnable** and cannot be used for export or visual
acceptance. Historical paths below describe the complete project, not a promise
that those art files exist here. Do not treat absent art as a game defect.

Never commit media, generated captures, player saves or local working snapshots
to this repository. `.gitignore` excludes common media formats, but inspect the
staged file list before each push. Keep `.gd` and `.uid` pairs together and
preserve text data that the full project loads at runtime.
GitHub CI checks the source-only policy, not the game build.

For actual gameplay and native tests, use a complete local project with the
matching assets and follow the save-isolation rules below. Do not run tests
against the owner's real save folder.

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
| `assets/new-tilesets/` | Converted bought art in the full local project; media is absent from this GitHub snapshot |
| `vendor-art/` | The bought packs exactly as shipped; gitignored. The tileset repair tools read them through `--sources`; do not delete |
| `docs/TILESET_LIBRARY_HANDOFF_2026-09-20.md` | Start here for the bought art library: what exists, how the owner reports problems, the pipeline and what is open |
| [`docs/CODEX_HANDOFF_2026-09-20.md`](docs/CODEX_HANDOFF_2026-09-20.md) | Where the art actually lives after the September 18 move, the room-layout rules that are easy to break, the camera, and what the renderer costs and why |
| `legacy/` | The earlier room and prop art, moved aside. **Load-bearing, not a cleanup candidate:** live code loads from `default/` *and* from `retired/` — that split was decided by whether a literal path named the file, so a dynamic reference landed art in `retired/` that the game still draws. A single pack can be split across `assets/`, `default/` and `retired/` |
| `Brine icons/` | Icon set in the full local project; media is absent here |
| `brinecore-animation/` | BRINE core room animation study — its own scene and scripts |
| `brineui/`, `character/` | UI and character code, metadata and local-only art |
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

In a complete local project with matching media, open project.godot with Godot 4.7
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

**Never run tests or probes against the owner's real save folder.** `project.godot`
pins `user://` to `%APPDATA%/Godot/app_userdata/BrineSpace/`, which holds their
progress save, loop checkpoint, comms sidecar and Studio layouts. Run every Godot test
or probe with `APPDATA` set to a scratch folder (copy `room_layouts.json` in if the
test needs the owner's layouts), and fingerprint the real folder before and after.
On 2026-09-26 unisolated portrait tests overwrote the checkpoint's
`brine_loop.save.comms.json`; it was restored from an F8 bug-report zip. A probe
that restores a checkpoint from `output/` must restore a scratch copy and reset
`run_save_path`: `RunSave.restore` retargets autosave at the loaded file.

For playable exports, follow [docs/RELEASE_WORKFLOW.md](docs/RELEASE_WORKFLOW.md) and
use the maintained release exporter. Keep editor/PCK checks separate from actual
release gameplay; release assertions must never contain required side effects.
