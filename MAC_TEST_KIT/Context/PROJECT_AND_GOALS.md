# Project context and accepted direction

## What BrineSpace is

A Godot 4.7 passive roguelite underwater station builder. Current local builds use
official **Godot 4.7.2**. The north star is restoring a silent station: build a
little, watch interlocking systems settle, discover an unexpected connection,
decide whether to risk another room. Placement decisions and discovery should
create pressure; rapid clicking should not. Older orbital fiction and prototype
implementation names do not override the underwater direction.

The immediate objective is an Early Access candidate for **Windows and macOS**,
with reliable saves, readable visuals, correct crew/doors/lights and acceptable
frame pacing. The repeated performance constraint is **no change to how the game
looks or crew behave**. We want closer to 60 FPS on large stations, including 4×
simulation, zoom and room placement. A short 12-room VSync-limited 60 FPS result
does not meet the separate 40-room large-station target.

The owner has already spent many sessions measuring CPU work, render submission,
draw calls, texture uploads, room setup, navigation and rare stalls. Do not restart
from a generic "Godot optimization checklist" or propose turning off the artwork.
Use the included evidence map and frozen code to choose a measured target.

## Deliberate gameplay, not bugs to tidy up

- Ordinary runs pay room costs and enforce resource failures. Dedicated fixtures
  alone may opt into free building/disabled failures. Do not enable these to make
  a normal-play test pass.
- Timed directives/scenario victory were retired by the owner. A loop is banked
  with **Conclude Expedition**. Do not restore deadlines.
- Hidden recipes are discovered by functioning rooms. Three consecutive functioning
  cycles stabilize a pattern: its per-cycle bonus doubles in later loops, it pays
  Archived Data and its related blueprint costs half. Stabilizing does not decrypt
  a room. Blueprints, crew and companions are bought in Meta Progression with
  Archived Data. Already owned profile content remains owned/free.
- Crew/companions met in a loop remain for that loop; buying them determines their
  return in later loops. Follow the current code/owner instructions rather than
  an obsolete unlock description.
- Saves/unlocks remain prototype-level and deliberately unversioned. Preserve the
  existing packet admission, asset bindings, write/backup semantics and sidecars.
- No new survivor content or promises of future survivors in descriptions without
  an owner decision. Existing frozen recovery/progression remains intact.
- **Marsh animation polish is parked for its own session.** Platform validation
  does not reopen animation, room art or gameplay balance work.

BRINE is a damaged AI with dry, haunted opinions, not a cheerful assistant. User
text should preserve that voice. UI uses bundled Barlow Semi Condensed; station
logs retain a monospace face. Card zero readability, frame-over-outline layering
and angled coloured line clarity were addressed earlier; inspect them on Retina
without changing the accepted design merely for Mac.

## Code and content map

| Location in optional source | Responsibility |
| --- | --- |
| `project.godot`, `scenes/title_screen.tscn` | Title entry; gameplay is `scenes/main.tscn` |
| `scripts/main.gd` | Large game/UI/simulation coordinator; do not split it in passing |
| `scripts/grid_canvas.gd` | Station drawing, room setup, actor/source loading, retained rendering |
| `scripts/room_database.gd`, room/run/discovery modules | Definitions, colours, loop/recipe/progression rules |
| `scripts/run_save.gd`, `scripts/james_cargo_checkpoint.gd` | Checkpoint capture/validation/write/restore and live cargo binding |
| `scripts/crew_storage/` | Lossless compressed CPU frames and private draw routing/presentation lifetime |
| Crew/companion NPC scripts | Navigation, jobs, paths, movement and survival; inspect actual selected factories |
| `scripts/drone_animation.gd`, drone effect/storage modules | Exterior animations, uploads, lossless storage/fallback paths |
| `rooms/whole-room/`, `rooms/` | Room surfaces, doors/water/props, authored definitions and art |
| `rooms/tileset-library/` | Owner's Studio library marks/layout data; never reset from Git |
| `assets/`, `character/`, `brineui/`, `legacy/` | Runtime/authoring assets; legacy/retired paths can still be live |
| `tests/index.json`, `tools/run_tests.py` | Subsystem/lane-aware tests; native and headless acceptance differ |
| `docs/CURRENT_STATUS.md`, `docs/DEVELOPMENT_NOTES.md` | Direction and dated acceptance; newer owner decisions govern |

The design viewport is 1920×1080; default desktop window 1600×900. Record both
logical viewport and actual pixels/Retina scale in Mac results. Renderer settings
are part of the candidate: keep the current default for first acceptance.

## Content and engineering constraints

Keep `.gd` and `.uid` paired. Raster art is Git LFS in the repository; pointer
files are not broken PNGs. The optional source archive contains actual file bytes.
Runtime PNG loading must remain available without an editor import dependency.
Use whole quoted `res://` paths; path prefixes assembled with filenames evade
renames and can accidentally expand release manifests to entire folders.

Do not delete `legacy/`, `retired/` assets or bought source packs by their names.
Some remain dynamically loaded. Vendor packs, owner Studio marks and source
generations are not generic cleanup targets. `NOTICE.md` governs rights.

Department colours come from `RoomDatabase.room_color(id)`; corridors stay grey
and the BRINE core AI white. Studio free placement and filtering differ from live
rooms: some dressing/common decorations are intentionally hidden, wall decoration
is paused, and free-placement `issues()` can be empty. Do not label every Studio
test difference a gameplay regression. Read original AGENTS.md for the full rules.

## What this Mac session should deliver

Validate the frozen app natively, produce a reproducible report and preserve
progress/artwork. Establish actual backend, hardware, memory and frame distributions
before suggesting further optimizations. Fix a demonstrated Mac blocker in a
separate source/build lane if appropriate; keep the original candidate for comparison.
No automatic upload, publication, merge or broad refactor is requested.
