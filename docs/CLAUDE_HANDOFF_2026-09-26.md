# Claude handoff — September 26, 2026

Session "Brinespace development". Nineteen commits on `main`, all pushed (5c1999b59 to
8d79a021b). The owner is redoing the art in Codex, and the next sessions integrate it.
`CURRENT_STATUS.md` records the morning's work; the afternoon's work (from 45e21eb7e on)
is recorded only here, because the Codex session had uncommitted edits to that file.
Merge this into it once those edits land.

## Next: new art integration (in this order)

1. **Run `python tools/art_consistency_check.py` on the new art first.** It flags crew
   clips that drift from the character's typical clip in the same facing, and props or
   crew at a pixel density far from the prop median. Current baseline: the walk cycles
   are the flattest clips (Veld x0.66 contrast), and crew are painted at 0.76x the
   props' density (2.27 against 2.96 source px per world unit). Once the Codex art docs
   settle (`docs/BRINESPACE_ART_REFERENCE_LOCK_2026-09-26.json`,
   `docs/ART_BIBLE_HANDOFF_2026-09-26.md`), align the checker's targets to them.
2. **Then run the full suite and the native lanes** to see what the art breaks, before
   fixing anything by hand: `python tools/run_tests.py`, then `--native --screen 2` per
   subsystem, with `APPDATA` isolated (see Safety).
3. Raster art is Git LFS: check new images are pointers.
4. Props and cards: re-cut them with `build_catalog.py`, then rebake the cards with
   `tools/bake_room_cards_v2.gd`.
5. **Owner Studio layouts key on prop ids.** If the ids change, decide with the owner
   whether to migrate the layouts or re-lay the rooms before any furniture is placed.
6. Crew:
   - `BUNK_SEAT_ROWS` in each crew script was measured from the current bunk frame 2
     (the seat row above the foot pivot). Re-measure it from the new art.
   - If the crew are painted nearer their on-screen size, `standingHeight` in the
     manifests changes. Crew currently draw at about 37% of painted size with nearest
     sampling, which causes the speckle.
7. Drones: new sprites go in the REGIONS table in `scripts/drone_art.gd`. The hatch
   opening is drawn in code.
8. Navigation: new furniture changes the walk graph. Rerun the crew and navigation tests
   and the spike probe against the baseline (below).
9. Corridors: if the outlines change, `test_corridor_swim_shortcut` re-proves the
   swim shortcut's inner rectangles automatically.

## What changed today

### Crew routing and frame spikes

Baseline: a copy of `output/procedural-sites-2026-09-23/expedition-73-progressed-known-recipe-final/latest.loop`,
headless, with `APPDATA` pointed at a scratch folder holding a copy of the owner's `room_layouts.json`.

| Change | Commit | Result |
|---|---|---|
| Swim smoothing retries keeping the search's facings | 30c12e6e1 | Sept 23 doorway report: escape found in ~25 ms (was none; 740 ms worst update) |
| Shortcut reach capped at two rooms; heap swim A*; per-choice unreachable skip | 60b887ec5 | 30-cycle worst frame 389 → 143 ms |
| Corridor swim clearance skips sampling inside a proven floor rectangle | d7b0314bf | Cold failing swim search 820 → 481 ms, all 23,444 answers unchanged |
| Swimmers plan dry rooms with the walking check (`swim_cells`) | f08632878 | Branforth leaves a flooded reactor for a bunk in 17 s; worst frame 115 ms |
| Stand-off detour: a flood fill predicts reachable starts | d1144b031 | Doorway stand-off 1,018 → 53-79 ms (0 mismatches at 26 stand-offs) |
| One crew navigation rebuild per frame (`defer_navigation_rebuild`) | c0098db92 | Room completion 141-176 → 33-64 ms |

Still open: about 115 ms once, right after loading a save (cold caches).

### Economy and room scrapping (owner decisions)

- Zero-metal softlock (found by the seed-101 review run): once surveyed deposits were
  gone and Metal fell below 2, nothing was affordable again. The owner chose two fixes
  (9bd084473):
  - `scripts/metal_trickle.gd`: BRINE Core adds +1 Metal every 3 cycles while Metal < 2
    and no bay can harvest.
  - `scripts/room_scrap.gd`: an inspector SCRAP button refunds half a room's Metal
    (press twice to confirm).
- Scrap refuses:
  - the core, rescue wards and crew habs;
  - occupied rooms, and rooms others need to reach the core;
  - an away expedition's airlock;
  - a room next to queued construction, or a builder's work spot;
  - storage whose loss would drop stock over capacity.

  A queued hull repair on the room is cancelled first, which refunds its unused Metal
  (45e21eb7e). Flooded or cracked rooms can be scrapped: their water and leak go with
  them ("jettison").

### Saves and diagnostics

- `RunSave.problem()` names every rejection. `write()` refuses a checkpoint the loader
  would reject and keeps the previous file; a backup fallback records
  `_primary_problem` (f9199d430).
- Hitch and stall reports carry `crew_usec`: per-crew update time, activity, goal and
  navigation rebuild. The stuck watcher raises one advice line after 120 s with nothing
  affordable and no harvest (5f1ae729f).

### Tests and fixtures

- `test_marsh_expedition_presentation` flake (7b0eac3b1): its route clearing erased
  unidentified "recovery" wards, so the saved site was invalid. Seeds 1, 6 and 11
  reproduced it; 8 of 8 random runs pass now.
- `test_owner_report_regressions` passed only with the owner's layouts. It now starts
  where the swimmer fits (db1cdcfa1).
- Expedition test player: rerolls unaffordable cards when no bay can harvest, and
  rerolls the whole hand when stranded with nothing affordable (essential support
  cards are kept). Seed 101: builds after cycle 29 went from 4 to 10, and the station
  reached the next ward (7f1550634, 8cb44b73c).
- New tests:
  - `test_swim_smoothing_facing`, `test_corridor_swim_shortcut`, `test_swim_walk_routing`
  - `test_detour_start_filter`, `test_navigation_rebuild_stagger`
  - `test_metal_trickle`, `test_room_scrap`, `test_save_integrity`
- Last full run: 171 headless passes, 0 failures; native crew, owner and procedural
  lanes pass.

### Bunk and crew art (owner's Codex queue)

- The seated bunk frame sits on the mattress edge (d0170abf2).
- Tried and reverted at the owner's call:
  - colour-matching the bunk clips to the walk cycle (it looked worse; the walk cycle
    is itself the odd one out);
  - mipmapped crew smoothing (it blurred faces).
- Crew suits read too blue beside the warm bunk. In-game pixels match the source art,
  so this is an art question. Details are in the Open list of
  `STATION_PROPS_V2_2026-09-25.md`.

## Automated review runs

Fresh seed-101 runs (900 s, all crew, paid rules) are in
`output/procedural-sites-2026-09-23/expedition-101-sept26-*`: `-review`, `-rerun`,
`-trickle`, `-tuned` and `-tuned2`. They reach cycle ~173 with Veld rescued. Rescuing
all three crew within 900 s is still not reached. The `-review` run's `final.loop` was
deleted by a probe (see Safety).

## Safety (read before running anything)

- Run every Godot test or probe with `APPDATA` pointed at a scratch folder, and
  fingerprint `%APPDATA%/Godot/app_userdata/BrineSpace/` before and after
  (now in `AGENTS.md`, ef6e2f905).
- On Sept 26, the Codex session's unisolated portrait tests overwrote the owner's
  `brine_loop.save.comms.json`. It was restored byte-exact from the Sept 25 F8
  bug-report zip; the overwritten copy is kept in this session's scratchpad.
- `RunSave.restore` points autosave at the loaded file. Probes must restore a scratch
  copy and reset `run_save_path`.
- Other sessions share this checkout. Stage with explicit paths, never `git add -A`.

## Waiting on the owner

- Release continuation check: play to mid-game and save.
- Reviews of motion, scenery, room coherence and music, and a native Mac test.
