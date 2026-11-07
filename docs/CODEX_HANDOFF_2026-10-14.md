# Codex handoff - October 14, 2026

Project: `C:/Users/Alex/Documents/Brine Space` · Godot 4.7.2, gl_compatibility · `origin/main`
at `fb1072a6` when written.

Claude took over from your [October 11 performance handoff](CLAUDE_PERFORMANCE_HANDOFF_2026-10-11.md)
and the owner is handing the game back to you. This document covers everything since then:
65 commits from October 11 to 14. The detail for each item is in
[`CURRENT_STATUS.md`](CURRENT_STATUS.md) (newest first, dated); this is the map.

Also open for you: the [art handoff of October 13](CODEX_ART_HANDOFF_2026-10-13.md). Its items
are unchanged and none were started.

## Read first

1. `AGENTS.md`, then this file, then the top of `docs/CURRENT_STATUS.md` down to October 11.
2. Owner decisions below are settled. Do not reopen them without the owner.
3. The working tree holds other people's uncommitted work: about 55 modified tracked files
   (mostly `character/veld-identity-correction-v1/`, `skills/brinespace-*`, two
   `rooms/underwater/*/render_completed_room.gd`, `export_presets.cfg`, `.gitattributes`) and
   about 16,000 untracked files. None of it is Claude's. Stage by explicit path only, never
   `git add -A` or `commit -a`; check `git diff --cached --name-only` before every commit.
4. The tileset library JSON carries the owner's Studio marks (stars, retirements, renames)
   uncommitted. Never `git checkout` those files.

## Where things stand

- **Repository.** Everything the game ships is now on `origin/main`: code, data and all
  27,532 shipped PNGs (Git LFS, three batches), plus 4,268 tools, tests and documents. A
  shallow fresh clone matched the release manifest file for file and started a new game.
  Git LFS storage was about 7.7 GB before the art and an expected 9.1 GB after, on the free
  plan; the 10 GB limit was not confirmed. Check the quota before adding a lot of art.
- **Release candidate:** `brinespace-6d97d875cd6b9d23` in `C:/bs-release-20261013c/windows`,
  built from `a64e18f9`. It passed pack audit (35,790 checked, 0 missing or changed),
  new-game smoke, Continue timing (12.7 s first launch, 7.0-7.2 s ordinary), save/quit/
  relaunch, 40 of 40 starts and a clean 30-minute soak. Benchmark at 1920x1080: fresh station
  24/24; the reported 12-room save 20-21/24, with only zoom over (accepted, below).
  **It predates the October 14 changes** (Studio ocean, Studio warm-up, crew roster, berth
  rules, Clone Lab). Rebuild before any release. Publishing is the owner's decision alone.
- **Rebuild recipe:** the stage drivers in `output/renderdoc-tools-2026-10-08/`
  (freeze, import, build, audit, smoke) reused with a new output folder; about 22 minutes.
  The freeze copies the working tree, so do not edit files while it runs. D: lacks the
  roughly 40 GB of headroom a freeze wants; C: has been used.
- **Mac:** an unsigned Universal 2 build only. Signing uses the owner's individual Apple
  account and must never be done without them.
- **Owner's save folder** `%APPDATA%/Godot/app_userdata/BrineSpace/` held 2,948 files and was
  unchanged by every check. The owner plays from source, so that folder changes while they
  play; that is not a test leak.

## What changed since October 11

### Performance and release work (from your handoff's next actions)

- Your private effect storage went in, Windows-guarded: lossless two-channel drone effect
  sheets with a generator and test (`2d81f289`, `643b2959`), and cropped mining cargo
  storage (`42be16c7`). The topology cache and `test_crew_topology_signature` from your
  handoff are committed (`5a469aaa`, `6773994d`).
- Loading no longer trips the stall report (`adb3403a`).
- Crew passage stand-off: the sweep is bounded and pauses after a failure (`217edff9`).
- Exit crash: worker-thread image jobs still pending at quit crashed the process
  (0xC0000005). Hand-image and drone jobs now finish on `tree_exiting`, whoever started them
  (`3094c2b5`). Any new worker task must do the same; `scripts/studio_warmup.gd` is the
  smallest example.
- **Light fades no longer repaint every floor** (`a64e18f9`): while a room fades, its light
  pools (or a hallway's hull) are a `FadeSlot` child of the floor layer, drawn once at full
  light, and the fade changes its opacity or tint. Floors repaint when a fade starts and when
  it settles; settled rooms are pixel-identical to the old drawing.
  `--repaint-floors-with-light-fades` restores the old path. Fade frames went from 18.2 to
  13.2 ms on the 12-room save, and the lighting gate passes.
- **Zoom gate: cause found, miss accepted by the owner.** Each zoom causes 3-5 frames of
  18-26 ms while retained layers repaint at the new size, one group per frame (floors;
  walls, doors and lights; the environment group with 274 rock and wreck cell slots). Passing
  would need floors as per-room nodes. The owner declined that and a partial seabed split.
- **Studio opening:** 3.2 s to 0.41 s. The cast decodes each frame when first drawn
  (`lazy_art`, `f612f57d`), and the art catalogue plus the first room's script now load on a
  worker thread two seconds after the title settles (`scripts/studio_warmup.gd`, `95cd9f64`).
  Later openings take 0.32 s; the rest is the Studio building its panels.
- Meta Progression's Blueprints tab adds cards a few per frame instead of all at once
  (`9604bcd3`) and keeps its scroll position after a purchase (`3270479f`).
- **Object count growth: partly traced and parked** by the owner, possibly for you. Soaks
  gain about 80 objects a minute with flat memory. The prop mesh cache (cap 256) and the crew
  path caches (cap 60,000) are bounded. A steady 55-80 a minute remains untraced: it is not in
  any reachable script container, node metadata, signal or tween, and not a leak at exit.
  Recommended next step: a two-hour soak; if memory drifts, Godot's ObjectDB snapshot from
  the editor debugger.

### Fixes from the owner's playtest reports (October 13)

- Large rooms: no legacy door stamped over their own port doors (`388978bf`); outer walls,
  riser edges, corners and port doors at the ordinary 16 px depth with their original art
  (`4d7255d9`); added to the riser catalog's departments (`7e8e959d`).
- Marsh could stand "waiting for passage" for good behind River and Margot: his east start
  clip restarted on each blocked attempt, so blocked time counted one frame in seven
  (`7a7066e0`, test `test_marsh_blocked_wait`).
- Diving Airlock: in a chamber lying east-west, crew stood on the centre line and their head
  crossed the far wall; they now stand 38 units nearer the south wall
  (`aa587633`, `test_airlock_chamber_stand`).
- Meta Progression: locked blueprints show department and rarity behind the Codex's "signal
  obscured" card; buying one shows the recovered room until Continue or Escape (`c55e8a60`).
- Hand cards: every card is exactly `CARD_SIZE` (`ac54ebb1`); long value rows wrap
  (`7c89eb83`); a hovered card lifts without growing and lands on whole screen pixels,
  because the 5 percent enlargement resampled its text (`b4c0d1f0`).
- Journal: the core architect's row shows their own portrait (`94a183c3`); the roster lists
  the real crew only (`b2e3f97c`).
- Room Layout Studio: the ocean is always shown, on the game's own seabed tile, aligned with
  the room at the Studio's pan and zoom and clipped to the canvas (`d5386ab3`).

### Gameplay rules changed by the owner (October 14)

- **Berths are housing for characters only.** Two to start, two more per Crew Hab, plus the
  research bonus; companions take none. A Crew Hab no longer adds an unnamed survivor.
  Food and oxygen upkeep count only the characters aboard. Old checkpoints reset their crew
  count from the characters recorded alive (`dac6a2a2`, `test_berths_real_crew`).
- **Safe Wake Protocol** no longer adds survivors; while it runs, cryopods thaw 50% faster
  (`cryo_recovery.safe_wake_rate`).
- **Clone Lab** no longer makes clone crew; for now it makes 3 Data for 2 Power and 1 Biomass
  and stays in the draft deck (`fb1072a6`). Its real job is parked; the owner liked "bring
  back a crew member who died this run". Do not build that unasked.

### Tests and the test runner

- Crew loaders work on a grid outside the scene tree; old-save fixtures added (`fe4f8577`).
- The crew art record `tests/crew-art-baseline.json` (2,002 clips, 19,604 frames) is built by
  `tools/build_crew_art_baseline.gd`. Rebuild and commit it with any approved crew art or
  timing change; three tests compare against it.
- `tools/run_tests.py`: a stall guard stops a test that printed a script error and went
  quiet (`c2761de1`); fixtures get the scratch folder they name (`7d2c4180`); lanes come from
  the source plus overrides in `tests/index.json` (headless 347, native 525, skip 48 when
  counted). 81 pixel-readback tests moved to the native lane (`a7926b9a`).
- Twelve candidate fixtures overtaken by selection are skipped, not deleted (`1e5ffb7f`).
- Remaining failures are pre-existing and listed in `output/full-suite-2026-10-12/`
  (about 20 headless, 45 native when counted). Mostly Bill art pins waiting on art; also
  `test_carry_turn_handoff` (12 Marsh swim-turn mismatches, art item 2),
  `test_veld_death_water_*_candidate`, `test_content_cache_parity`,
  `test_retained_lights_parity`, `test_environment_cache_parity`, `test_branforth_bunk`,
  `test_hull_ui`, `test_site_runtime`, `test_veld_sofa_contact_probe`.
- `test_ui_live_components` fails on a reused scratch profile (its meta save remembers the
  purchase) and passes on a clean one. Start long runs with a fresh scratch folder.

## Owner decisions (settled)

1. Helmet changes may restart a clip.
2. Large rooms are rare: the existing one-per-run rule covers it.
3. Hand defaults: no frame, fan layout. All hand cards one size; hover lifts, never grows.
4. Large-room walls at 16 px with their original art; the department cap art was rejected.
5. Locked blueprints: "signal obscured", with the purchase popup.
6. The light-fade overlay is approved; the zoom miss is accepted for this release.
7. Studio: the ocean is always on (no switch), on seabed tiles. The warm-up is approved.
8. Crew roster and berths: real characters only (above). Clone Lab revival is parked.
9. Object-count growth is parked.
10. Marsh is helmet-free.

## How to work here without breaking things

- **Never run anything against the owner's save folder.** Point `APPDATA` at a short scratch
  path (for example `D:/BrineSpace-performance/scratch/<name>`), fingerprint the owner folder
  before and after, and copy any report or save into a scratch folder before reading it.
- Windowed tests: `--native --screen 2`, muted (`BRINE_SILENT=1`, `--audio-driver Dummy` for
  probes).
- Owner layouts change results. Before calling a layout or route failure a regression, run
  it with an empty scratch profile and with a scratch copy of `room_layouts.json`.
- `scripts/main.gd`: no refactors unasked. Keep `.uid` files paired with their `.gd`. Name
  whole `res://` paths; a rename rewrites only whole literals.
- `ImageTexture.get_image()` returns null headless; tests reading pixels belong in the native
  lane.
- Benchmark p95 drifts about 1 ms with machine state. Compare candidates back to back in the
  same hour; one run misleads.
- `get_property_list()` reads can trigger lazy art loads (Josh's frames, texture pools). A
  probe that walks the scene inflates object counts by itself.

## Suggested next steps (owner to choose)

1. The art handoff: Marsh's swim cycle and swim-turn end frames, stand-to-swim clips (code
   follows), underwater salvage pose, and Bill's helmeted walk north. Rebuild the crew art
   record with the art.
2. Rebuild the Windows candidate from current `main` and rerun the release checks, so the
   October 14 changes are in a certified build.
3. If asked: the object-count trace, or the Clone Lab's revival job.
4. Mac signing and the GTX 1650 / M1 measurements need the owner or that hardware.
