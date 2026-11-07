# Codex handoff — art paths, room layouts and the camera, September 20, 2026

Read [`AGENTS.md`](../AGENTS.md) first, then
[`TILESET_LIBRARY_HANDOFF_2026-09-20.md`](TILESET_LIBRARY_HANDOFF_2026-09-20.md) for the bought
art library. This file covers what changed on the evening of September 20 and, more
importantly, **why the art works the way it does now** — because the shape of it is not
obvious from the code, and getting it wrong is how two days of blank seabed happened.

Everything below was measured on this machine on September 20 with Godot 4.7.2. Where a
number is quoted, it came from a run, not an estimate.

---

## 1. The one thing to understand before you touch art

**Name whole `res://` paths. Never a folder prefix joined to a built name.**

Two separate tools read your source as if it were data, and a prefix defeats both:

1. **A rename or a move can only rewrite whole quoted paths.** Commit `3d4e0fed9`
   (September 18) relocated 798 art files into `legacy/` and rewrote the literals in 385
   source files. It reported "zero dangling references", which was true and useless: any
   path the code *assembles at runtime* was invisible to it. A `const ROOT` joined to a
   filename. `"…/pack/%s.png" % key`. `"…/" + id + "-v1.png"`. **102 paths** had been
   loading nothing for two days.
2. **`tools/build_release_manifest.py` expands a quoted folder prefix into that entire
   folder — including inside a comment.** The rooms root shipped 80 files and 101 MB to
   deliver three `machine.png`. This is what cut the release pack from 5.8 GB to 1.2 GB,
   so it matters.

The fix pattern, used throughout now, is a `const` map of whole paths:

```gdscript
const FOUNDATION_ART := {
    "silt": "res://legacy/default/rooms/foundation-v1/foundation-silt-v1.png",
    "reef": "res://legacy/retired/rooms/foundation-v1/foundation-reef-v1.png",
    ...
}
```

**Why nobody noticed for two days:** a missing PNG is a `push_warning` plus a magenta
placeholder, and the only assertion on `SafeImage.failures` lived in
`release_new_game_smoke.gd`, which runs only against an actual release build.
`tests/test_reliability.gd` now fails if any `res://` artwork the station loads reaches the
placeholder. That is the cheap guard this whole class of bug went without. It was proved
non-vacuous by disabling the fix and watching it fail.

---

## 2. Where the art actually lives

`legacy/` is **load-bearing**. It looks like a cleanup candidate and is not: 102 live art
paths point into it, plus 73 that predate this session.

| Root | What is in it | Live code points here? |
|---|---|---|
| `assets/`, `rooms/` | Floors, risers, wall surfaces, corridors, room cards, icons, UI, character art, the bought tileset library | Yes |
| `legacy/default/` | 445 files the September 18 move classified as "the game was still referencing" | **Yes** — the seabed, foundations, several rooms |
| `legacy/retired/` | 353 files it classified as "nothing referenced at all" — often wrong, because the reference was dynamic | **Yes** — the command centre, construction bay, tidal condenser, observation room, galley, salvage workshop |

A single pack can be **split across all three**. The observation room is the worst case:
`riser.png` stayed in `assets/`, `shelves-down.png` went to `legacy/default/`, and the other
21 files went to `legacy/retired/`. Do not assume a folder moved as a unit.

To find where a file went: `git ls-tree -r --name-only HEAD | grep <basename>`. Ask git, not
the filesystem — see the clone warning in AGENTS.md.

**Do not move the art back.** The owner's copy stays where they put it; adapt the code.

---

## 3. What was broken and is now fixed

### 3.1 The seabed and the foundations
21 environment view scripts under `assets/environment/*/` had `const ROOT := "res://assets/…"`.
All now point at `legacy/default/`. The station's four foundation piles were assembled from
`"foundation-" + variant + "-v1.png"` and drew nothing; `grid_canvas.gd` has the explicit
`FOUNDATION_ART` map above.

### 3.2 A per-frame disk read, and why the fix made the game *faster*
Eleven environment views guarded `prepare()` with `if not textures.is_empty(): return`. A
failed load leaves the dictionary empty, so they re-read from disk **on every `_draw`** —
560 attempts at one anemone PNG in a single test run, and **3,122 asset errors** in that one
run. They latch the attempt with a `prepared` flag now.

Measured on a 78-room station, before and after:

| | HEAD (blank seabed) | now (art restored) |
|---|---|---|
| 100 rooms, fit view | 64.73 ms | **62.19 ms** |
| 100 rooms, close | 23.68 ms | **20.30 ms** |
| draw calls | 10,085 | 10,564 |
| `env_seabed` draw stage | 4.728 ms | not in the top eight |

**Drawing the seabed is cheaper than failing to draw it was.** Do not "optimise" by
removing art before you check what the broken path costs.

### 3.3 Navigation ignored the library's own floor data
Every one of the 10,507 library props records a `footprint` — the part of the art that
stands on the floor — and the equipment shadow already draws only that. But
`Geometry.prop_collision_rects()` blocked with the **whole art box**, including the part
drawn up the wall. A tall incubator whose feet were 12 units inside the room walled off the
doorway behind it. It honours `footprint` now when a prop has no explicit `collision_boxes`.

### 3.4 The Isolation Vault rendered empty
`rooms/underwater/rare-dead-ends/isolation_vault_view.gd` filtered props to "dressing only"
on **every** `configure_embedded`, which threw away the wall bank the previous call had
installed — and the bank only reinstalls off a fresh rebuild. Props went **8 → 0 → 0 → 0**
and never recovered. Behind it, the view ran "place the dressing" with no dressing left, and
`Dressing.place()` ends in a room-wide `keep_props_inside_walls()` that clamps to a flat 360
interior, dragging the wall-mounted bank 16 px off its wall. Both fixed;
`test_embedded_geometry` passes all 188 room/rotation cases for the first time in a while.

---

## 4. Room layouts — the rules that are easy to break

The owner's layouts live in `%APPDATA%\Godot\app_userdata\BrineSpace\room_layouts.json`,
keyed `<asset>/<quarter>`, merged over the committed defaults in
`rooms/full-wall-v1/default-layouts.json`. **A `null` entry deletes an authored prop.**

### 4.1 The furnishing script strips a room before it places
`tools/room_decorating/furnish_groups.gd` nulls every authored default prop, keeping a
removal only if `issues()` stays clean. On the BRINE Core that deleted all five authored
props — including `brine_chamber`, which the tank, the water, the reflections and BRINE's
floating body all key off, so **she was not drawn in her own core room**. All five are
restored. If a room has authored furniture worth keeping, place into it without that step.

### 4.2 "Copy to other rotations" pins a prop while the door moves
Five doorways were blocked by props and crew could not path through them. One was the
footprint bug in 3.3. The rest were the owner's own placements sitting at **identical
coordinates in all four rotations** — the door moves with the rotation, the prop does not.
Watch for that button.

Resolved on the owner's call: the Mycelium Nursery's cultivation bank came out (240 units
wide in a 348-wide room — it cannot share a wall with a 72-unit door lane, at any offset),
and Pressure Control lost its wall installation plus the pump standing in its only door at
q2. Its other 14 hand-placed props were left alone.

### 4.3 Furnish the room, not its name
`tools/room_decorating/plan_groups.py` had the Emergency Isolation Vault down as a
strongroom — strongbox, hard case, crate, cot, locker — when `room_database.gd` calls it
*"Reserve power and emergency branch isolation controls"*, Engineering. It asks for
switchgear, a fuse box, a transformer, a power coupling and a battery rack now. The
Mycelium Nursery had no entry at all and now has one. **Read a room's `description` and
`category` before writing its group list.**

### 4.4 The lint, and what each check is actually worth
`tools/lint_room_layouts.gd` — headless, all 188 room/rotations in about a minute, writes
`output/layout-lint.json`, exits non-zero on findings, never writes the layout store.

```
godot --headless --path . -s res://tools/lint_room_layouts.gd
godot --headless --path . -s res://tools/lint_room_layouts.gd -- --rooms=research_lab
```

- **blocked-door — rigorous.** It is the rule `bill_npc.gd` uses to build the navigation
  graph, so a finding means crew genuinely cannot walk through that door. **Currently zero.**
- **overlap — advisory.** Only compares props that record their floor contact. An authored
  prop falls back to its whole art box, and in a top-down room a console standing *in front
  of* a machine overlaps that box and is drawn correctly by `sort_y`. The first version of
  this check reported 90 findings; **48 of them were depth, not collision**, and acting on
  them would have meant moving the owner's props to fix nothing.
- **off-hull — advisory and cosmetic.** Free placement is the Studio's default and the
  owner's to use.

Current state: **188 room/rotations, 0 blocked doors, 25 off-hull, 1 overlap** — all the
owner's art, all cosmetic. Not a CI gate.

---

## 5. The camera

- **Zoom-out is capped.** `ZOOM_OUT_EXTENT := 0.75` in `main.gd`: the furthest view shows 30
  of the 40 cells across, not all of them. A station is a block in the middle of the grid, so
  it still fits whole. **This is readability, not speed** — the same rooms are drawn at
  either limit and the frame costs the same (60.6 ms against 61.0).
- **Wheel zoom holds the grid point under the pointer.** It used to preserve the view
  *centre*, which the scroll container clamps at the grid edge, so zooming out far pulled
  the centre toward the middle of the map and zooming back in returned you there instead of
  to what you were looking at: **5.81 cells of drift over three notches, now 0.01**. The
  pointer is read fresh each notch, a pointer outside the grid frame falls back to the
  centre, and `_request_grid_zoom` drops any anchor so the slider and Fit Station View
  cannot inherit a stale one.
- `tests/test_grid_zoom.gd` covers both, headless in 24 s, and was proved non-vacuous.

---

## 6. Performance: the facts, and the only lever that matters

Measured with and without the draw profiler — **the profiler is free** (61.08 ms vs 61.29),
so the numbers in `tests/profile_large_station.gd` are real and not self-inflicted.

Frame cost at a fixed far zoom is **dead linear**:

| rooms | 2 | 20 | 40 | 60 | 78 |
|---|---|---|---|---|---|
| frame | 15.3 ms | 25.8 ms | 37.4 ms | 48.2 ms | 58.8 ms |

That is **~15 ms fixed plus 0.57 ms per room**. No superlinear blowup, no missing cache.
The fixed part decomposes as: wreck field 4.1 ms, seabed 1.7 ms, HUD 1.1 ms, ~8.4 ms base.

So **0.57 ms × 78 rooms = 44 of the 61 ms** is `_draw_room` doing genuine work — every room
rendering full prop detail even when it is 62 px across. `cull_props` only culls what is
*off-screen*, so at fit view it does nothing.

The project renders through `gl_compatibility` (section 10), which is worth knowing before
reasoning about batching.

**The only lever that touches that 44 ms is level of detail**: below some zoom, draw a
simplified room instead of every prop. There is no LOD mechanism in the codebase today, so
it is a new feature that changes what the player sees, not a tidy-up — an owner decision.
The question to ask first is: *at fit view, what should a room look like?*

Do not bother re-doing the obvious optimisations. `_crew_feet` is already cached per frame,
static room content is already retained, and the close view is 19.7 ms (~50 FPS) and fine.
This is specifically a zoomed-out problem.

---

## 7. Test state

Measured September 20. Run a group with
`python tools/run_tests.py --subsystem <name>`, add `--native` for the render-bound lane.

| suite | headless | native |
|---|---|---|
| gameplay (57) | 48 pass, 0 fail | — |
| crew (29) | 27 pass | — |
| ui (16) | 10 pass (incl. `test_grid_zoom`) | — |
| fire (4) | 3 pass | `test_fire_gameplay` pass |
| flood-water (12) | 9 pass | 3 pass |
| room-art (29) | 16 pass | — |
| render-perf (18) | 2 pass | 14 pass, **1 fail** |

Zero `res://` artwork misses across 48 logs (was 102). Fire and flooding were also driven
live: ignition 0.120 → 0.264 unsuppressed then sprinklers to 0.000; a hull crack to 0.531 in
8 s; pumps losing to an open breach and winning once sealed (0.999 → 0.523); station water
conserved with pumps off, because it equalises through doorways rather than draining.

**Two traps in the test lanes:**
- The tests share one Godot executable and one cursor. Running a second Godot against the
  display makes a native render test hang — `test_retained_lights_parity` timed out at 400 s
  that way and passes in 62.3 s alone. Do not blame the code before you check.
- Several tests are render-bound and *skip* headless. A green headless run is not a green
  lane; four fire and flood tests had never actually executed until they were run natively.

---

## 8. Open, and not for an agent to decide

1. **The opening economy is two Metal short.** `playtest_drone_economy` was measuring
   nothing — it never woke an architect, and crew build the rooms now, so the station it paid
   for was never constructed (0 metal over 300 s, twice). Fixed, it builds in a sensible
   order, finds free cells and names any build it cannot make. With solar, life support and
   hydroponics the station **survives all 300 seconds** and is then two Metal short of the
   drone bay — and never makes it up, because nothing on a station without a drone bay
   produces Metal (37 cycles later it still held 4). Without life support the crew are dead
   by cycle 12, `"Crew population reached 0."` So the paid opening cannot buy both life
   support and the bay that earns its keep. That is the opening grant, a room cost or a
   starter bay — **not** a flag to switch off. The test fails saying exactly this.
2. **`test_content_cache_parity`** — the one red test, predates this session, reproduces
   identically on HEAD. Exactly **one pixel in 1.44 million**, stale by one animation tick,
   in the mining drone bay's dock status lamp (a 4×3-unit lens that renders sub-pixel at fit
   view). An attempt to fix it by skipping sub-pixel drawing made it **worse — 10 failures
   to 27** — and was reverted. That strongly suggests the retained and direct passes see
   different `view_scale` values, which is a render-architecture question, not a one-liner.
3. **26 lint findings** in the owner's art (section 4.4), all cosmetic.
4. **BRINE's four other props** are restored; nothing outstanding there.

---

## 9. Do not

- `git add -A`. Other sessions write to this working copy constantly — currently 42 modified
  art files and an untracked capture folder that are not yours. Stage explicit pathspecs.
- Delete `legacy/`. It is load-bearing (section 2).
- Delete `output/`. It is 108 GB across 891 folders and **642 of them, 106.7 GB, are cited by
  a doc, tool or test** — including 107 test-run folders named in handoff docs as evidence.
  Only 1.7 GB is cited nowhere, scattered across 249 small folders. If space is needed, the
  honest levers are `builds/` (18 GB) and `.godot/` (9.4 GB), both regenerable, both the
  owner's call.
- Restore art the owner moved, or nudge a prop they placed. Adapt the code. The one exception
  is a prop standing in a doorway where no code change can work — and then you ask.
- Turn on free build or disable failure conditions to make a balance test pass.
- Refactor `scripts/main.gd` unasked.

---

## 10. `project.godot` — no instructions in it, and don't add any

It carries Godot's stock header and nothing project-specific. **Do not put guidance there:**
the editor rewrites that file from its own state whenever it saves, so hand-written comments
do not survive. Guidance belongs in `AGENTS.md`; `CLAUDE.md` is a pointer at it.

Four settings in it are worth knowing, because they are not obvious and two of them bear on
work described above:

- **`renderer/rendering_method="gl_compatibility"`.** The game runs on the OpenGL 3.3
  compatibility renderer, not Forward+. Anyone attacking the 10,564 draw calls in section 6
  should know that before reasoning about batching or measuring against another renderer's
  numbers. Changing it is a project-wide rendering decision, not a tuning knob.
- **`run/main_scene="res://scenes/title_screen.tscn"`.** The title screen is the entry point;
  `scenes/main.tscn` is gameplay and is what most fixtures instantiate directly. (`CLAUDE.md`
  claimed `main.tscn` was the entry point until September 20; it did not match the project
  file and is corrected.)
- **A 1920×1080 base viewport with a 1600×900 window override and `stretch/mode="canvas_items"`.**
  This is the whole of the open "blurry UI" item: the interface is laid out at 1920×1080 and
  resampled to whatever the window is, so at any other size every panel is softened. The
  turned cards in fan mode only make it easy to see. Fixing it means changing the base
  viewport, the stretch mode, or moving to distance-field fonts — an owner call, recorded in
  `CURRENT_STATUS.md`.
- **`run/main_scene.<feature>` overrides** — `menu_validation`, `environment_validation` and
  `room_validation` point at generated scenes under `tests/runtime_generated/`. They are how a
  validation export boots something other than the title screen. Keep those checks separate
  from actual release gameplay, as AGENTS.md says.

One autoload: `BugReport` (`scripts/bug_report.gd`), which is what F8 writes through.

## 11. Where to look

| Path | What |
|---|---|
| `scripts/safe_image.gd` | Every raw PNG load; `failures` is what `test_reliability` asserts on |
| `scripts/grid_canvas.gd` | The renderer, `FOUNDATION_ART`, the retained-layer machinery |
| `tools/modular_room_geometry.gd` | `prop_collision_rects()` — the navigation blocker, now footprint-aware |
| `tools/lint_room_layouts.gd` | The layout lint (section 4.4) |
| `tools/room_decorating/` | `plan_groups.py` (room group lists) and `furnish_groups.gd` (the placer) |
| `skills/brinespace-room-pipeline/references/room-decorating.md` | How the owner decorates, measured, and what a furnishing script must check |
| `tests/test_grid_zoom.gd` | Camera limits and anchoring |
| `tests/profile_large_station.gd` | The render profile used for section 6 |
