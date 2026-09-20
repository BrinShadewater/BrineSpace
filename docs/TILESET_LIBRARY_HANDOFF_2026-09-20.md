# Tileset library handoff - September 20, 2026

For whoever picks this up next (Codex, another agent, or the owner in six months).
The work landed on `main` on September 20 through
[PR #12](https://github.com/BrinShadewater/BrineSpace/pull/12) and #13; section 9 lists what
changed after this was first written. Read [`AGENTS.md`](../AGENTS.md) first; this file only covers the bought
art library and the Studio changes that came with it.

The rules of the work live in
[`skills/brinespace-room-pipeline/references/tileset-library.md`](../skills/brinespace-room-pipeline/references/tileset-library.md).
This file says what exists, why, and what is left. Where they disagree, the reference wins.

## 1. What changed, in one paragraph

The owner (Alex, publishes as Brin Shadewater) bought about forty pixel-art packs and now
decorates rooms by hand in the in-game **Room Layout Studio** instead of having agents
paint rooms. The packs were converted to the station's tone, scanned into props, merged,
named, categorised, pruned and repaired. The result is a library of **10,506 props in 42
in-universe sets on 269 sheets**, every prop named for what it is, browsable in the
Studio by category, set, search, favourites and "in this room". The earlier room and prop
art moved to `legacy/`; existing floors and riser walls stay live.

## 2. Where everything is

| Path | What |
|---|---|
| `assets/new-tilesets/<set>/` | Converted sheets (Git LFS). `fixes.png` in a set holds props lifted off a vendor sheet by `isolate.py`. |
| `vendor-art/` | The packs exactly as bought. **Gitignored** (licensed, 350 MB) and **needed**: the repair tools rebuild from them through `--sources`. They were on the owner's Desktop until today. A fresh clone does not have them; ask the owner. |
| `rooms/tileset-library/props.json` | The registry. One entry per prop: `id` (never changes), `label` ("Storage 041"), `title` ("Locker, grey, tall"), `category`, `tileset`, `source`, `region`, `pieces`, `display_width`, `footprint`. |
| `rooms/tileset-library/{favourites,retired,names,categories}.json` | **The owner's marks, written live by the Studio.** Tracked, but between commits they are newer than HEAD. Read them, commit them, never `git checkout` them. |
| `rooms/tileset-library/merged.json` | Alias map: an id that was merged, rejoined or deduplicated points at its survivor. The game follows it (`Library.base_id`), so placed copies keep drawing. |
| `rooms/tileset-library/removed.json` | Every removal with its reason. `sweep.py --restore <id>` undoes one. |
| `rooms/tileset-library/variants.json` | Families of look-alikes the tray folds into one tile. |
| `rooms/tileset-library/hole-patches.json`, `isolate.json`, `hole-report.json`, `floors.json` | Hand-chosen repairs, lifted props, known key holes, the 29 floor finishes. |
| `rooms/full-wall-v1/common-assets.json` | The owner's 45 earlier painted props. Each now has a `theme`, so the sixteen category filters list them beside the bought props. |
| `tools/tileset_library/` | The pipeline. Every tool's docstring says what it does and how it was proved. |
| `%APPDATA%\Godot\app_userdata\BrineSpace\room_layouts.json` | The owner's saved layouts, keyed `<asset>/<quarter>`. Not in the repo. Tests must never write here. |

## 3. The Studio, as the owner uses it now

Start -> Layout Studio. New since this work began:

- Tray filters: sixteen categories, a set filter, search by name, **Favourites**,
  **In this room**, **Marked for removal**; paging (280 per page) with a progress bar;
  hover preview; look-alike families folded into one tile with a **Variants** button.
- Per prop: **Star**, **Mark for removal** (same button restores), **Move to category**,
  **Rename**, **Split in two** (reads **Rejoin parts** on a split prop). Ctrl/Shift-click
  selects several.
- Room: crew picker (Bill, Marsh, Branforth, Veld) for judging scale; placement size;
  **Copy to other rotations**; floor **Finish strength** slider; 29 new floor finishes.
- Shadows shade a prop's floor footprint instead of its whole box.

How the owner reports problems: a **star means "fix this"**, and the **Rename field is a
bug report** ("remove table next to arm"). Read `names.json`, fix, delete the note.
A prop both starred and marked for removal has meant "remove" every time it was asked.

## 4. The pipeline, in the order it is used

`convert` -> `scan` -> `register` -> `merge` -> `tone repair` -> `titles`/`intake`
(review by numbered pages) -> `sweep` -> `refit` -> `cut` -> `isolate` -> `patch_holes`
-> `variants`. After any of them: `register.py --validate`, then the tests below.

What each stage taught us is in the reference. The short list that will save you a day:

1. **Owner data is sacred.** Commit the four mark files before a tool rewrites them.
   Anything the owner starred, renamed or moved is never removed by a reviewer.
2. **Ids are forever.** Never reuse one that was an alias or a removal (`free_id`).
3. **Repairs are pure functions of the vendor's sheet.** Run twice, compare hashes.
   Fill colours are sampled only from pixels that survive in the source.
4. **Judge cut-outs over magenta**, never over the floor grey.
5. **Never run `refit.py` on a piece cut from a scene tile**: connected art regrows the box.
6. **Look before writing.** Every cutting and patching tool has `--preview`/`--dry-run`.
7. **The Studio and the tests share one Godot executable and one cursor.** If the owner
   force-quits the game, a test run dies with it. The native drag-and-drop tests take
   focus and check the cursor; if the desk is busy they say so instead of failing.
8. Automatic key-hole repair (`unkey.py`) failed three times. It is kept for detection only.

## 5. Tests

```
python tools/tileset_library/register.py --validate
python tools/run_tests.py --only test_tileset_registry
python tools/run_tests.py --native --only test_tileset_library_tools,test_room_layout_editor,test_layout_performance_guards,test_simple_room_studio,test_room_studio_usability
```

`test_tileset_registry` (headless, 5 s) checks the contract on the sheets themselves:
trimmed regions, absolute pieces, footprints, unique ids/labels/boxes, marks, aliases,
removals, variants, floors. It has caught every registry mistake made so far; run it
before every commit. The native lane needs a real display.

All of the above passed at the last commit on this branch.

## 6. Numbers

- 10,506 props, 42 sets, 269 sheets, 1,273 look-alike families.
- 1,539 removals logged with reasons (owner's marks, the exclusion list, duplicates).
- 779 aliases. 63 props with hand patches. 16 props lifted onto `fixes.png` sheets.
- Largest categories: Storage 1,583; Industrial & workshop 1,277; Derelict & damaged
  1,099; Screens & computers 961; Lab & science 872.
- The owner's exclusion list: mechs, outdoor vehicles other than forklifts, spaceships,
  outdoor buildings, shipwrecks, medieval chests, pirate cannons, lifeboats, oars,
  crashed aircraft, futuristic guns and armour, spacemen (corpses are kept), solar
  panels, giant mining vehicles, helicopters, tents, ticket booths.

## 7. Open items

1. ~~Merge PR #12.~~ Done, with #13 (CI green again). Work from `main`.
2. ~~Two props still starred.~~ The owner approved both; favourites and notes are empty.
3. `hole-report.json` lists about 400 props with vendor key holes that nobody has
   patched. Patch what the owner stars; do not attempt a library-wide repair.
4. Whites are lifted only on props the owner uses. A library-wide pass is the owner's call.
5. The packs are less saturated than the owner's painted art. Accepted; repainting is a
   separate decision.
6. Suggested, not done: make **Rejoin parts** ask before merging (it replaces the Split
   button on any split piece and was once pressed by accident), and ask the owner for
   example labels of props that look too low-resolution.
7. Working-tree changes under `assets/marsh-charging-v1/review/` and `character/` are
   written by the native test lane and other sessions. They are not part of this work;
   stage explicit paths.

## 8. Do not

- `git add -A`, or restore the owner's mark files from git.
- Delete `vendor-art/`.
- Refactor `scripts/main.gd` or the Studio beyond what a task needs. Propose instead.
- Sign a Mac build, or put keys in code. See the project memory and `AGENTS.md`.

## 9. Later on September 20

- **PR #12 and #13 are merged; `main`'s CI is green again.** Four old breakages hid behind
  each other (CI stops at the first): a stale card-path test, 48 dead default-layout keys,
  five new music tracks missing from CI's LFS fetch, and a 15-minute job limit the art
  import had outgrown. The parse check now runs in batches of 100 scripts per engine
  launch (`tests/ci_parse_all.gd`) and names the script if the engine dies on one.
- **Rejoin parts asks first**: one press says how many props it will merge, a second press
  within four seconds does it.
- **`sweep.py` never removes a prop standing in the owner's rooms.** It reads the owner's
  saved layouts (read only). A reviewer's removal is refused; the owner's own marks are
  listed and need `--even-if-placed`.
- **The agent furnished the rooms the owner had not decorated** (34 rooms and the three
  hallway pieces, four rotations each) by driving the real Studio from a probe script.
  The layouts are in the owner's user folder, not the repo; a backup from before sits
  beside them as `room_layouts.backup-2026-09-20.json`. Two things learned: the Studio's
  validation does not stop library props overlapping each other or standing off a
  hallway's floor, so a furnishing script must check both itself
  (`Corridor.contains_foot`); and a hallway floor is about 94 units wide with a 72-unit
  door lane, so hallway props must be small (about 22 units) and touch the hull.
