# Codex art handoff - October 13, 2026

Graphical work from the owner's October 13 playtest, for Codex. Claude is taking the code
items from the same reports (listed at the end so the two do not overlap).

Read first: `AGENTS.md`, then the character pipeline skill
(`skills/brinespace-character-pipeline/`). Report screenshots are in
`output/owner-reports-2026-10-13/` (one PNG per report, named by time).

## Ground rules for this batch

1. **Art only.** Do not edit `scripts/`. If a task needs a code change, write down what is
   needed and stop on that task; Claude will make it.
2. **Marsh is helmet-free** by owner decision (`character/marsh-v2/catalog.json` has no
   equipment). Do not add helmet rows for him.
3. **Keep what the game reads.** Marsh's clips are listed in
   `character/marsh-v2/catalog.json`. Most of his water clips come from
   `character/marsh-master-repair-v1/manifest-p92_0-172_0.json` (canvas 184x184, pivot 92,172,
   `standingHeight` 148). New or replaced clips must keep pivot and standing height so he does
   not change size or slide.
4. **Stage, then select.** Put new work in its own versioned folder and switch the catalog
   entry only when it is ready. Never overwrite the frames a manifest already points at.
5. **Whole `res://` paths** in every manifest. Raster art is Git LFS; pointer files are normal.
6. **After any crew art or timing change, rebuild the crew art record** and commit it with the
   art:
   `godot --headless --path . -s tools/build_crew_art_baseline.gd`
   Three tests compare the game with `tests/crew-art-baseline.json` and fail until it is rebuilt.
7. **Run tests with a scratch save folder**, never the owner's:
   `python tools/run_tests.py --only <names>` with `APPDATA` pointed at a short scratch path.
   Add `--native --screen 2` for tests in the native lane.
8. **The owner approves by eye.** Produce a before/after image for each item.

## 1. Marsh: swim cycle looks off

Report 13:30 ("Swimming animation also looks off").

- Marsh's `swim-east/north/south/west` are 4 frames over 720 ms. Bill, Veld and Branforth have
  6 frames. His canvas is 184x184; theirs is 256x256.
- `swim-north` frame 0 appears to show two heads
  (`character/marsh-master-repair-v1/frames/swim-north/000.png`). Check and repair.
- Wanted: a swim cycle of the same quality and frame count as the other crew, at Marsh's
  proportions.

Done when: the owner accepts a side-by-side of Marsh swimming next to Bill in all four
facings, and `test_crew_swim_packs` still passes.

## 2. Marsh: swim turns end on a different painting from the swim cycle

Already in the art queue; do it with item 1, since a new swim cycle changes the target.

- The last frame of each of Marsh's 12 `swim-turn-<from>-<to>` clips has the same outline as
  frame 0 of the swim cycle it hands to, but 3,500 to 4,100 interior pixels differ. The swim
  cycle was repainted and the turn clips were not.
- His `carry-turn-*` and `swim-carry-turn-*` clips match their cycles exactly, and so do all
  turns for the other three crew. Use those as the reference for what "matches" means.
- Comparison: `output/marsh-swim-turn-endpoints-2026-10-12.png`.

Done when: `python tools/run_tests.py --only test_carry_turn_handoff` reports 0 failures
(it reports 12 today, all Marsh swim turns). Do not edit that test.

## 3. Marsh: no transition from standing to swimming

Report 13:30 ("Marsh doesnt transition from standing to swimming"), seen in the Diving
Airlock as it floods (`output/owner-reports-2026-10-13/20261013-133031.png`).

- Marsh has `swim-start-*` and `swim-stop-*` (5 frames, 400 ms), which join tread and swim.
  Nothing joins a dry standing pose to a water pose, so he snaps from one to the other.
- Wanted: a short clip per facing that takes him from his dry stand to his tread or first
  swim frame, and its reverse for draining.
- **Needs code.** Stage the clips and name them; Claude will wire the selection. Not yet
  checked: whether the other three crew have the same gap.

Done when: the clips are staged with a manifest and a contact sheet, and the first and last
frames match Marsh's `stand-*` and `tread-*` frame 0 exactly at the pivot.

## 4. Marsh: salvaging underwater uses a dry standing pose

Report 13:32 (`output/owner-reports-2026-10-13/20261013-133234.png`).

- During the salvage phase of an expedition every crew member plays their `salvage-<facing>`
  clip (`scripts/bill_npc.gd`, `animation_state`).
- Bill's, Veld's and Branforth's `salvage-*` frames are water poses (`crew_water_pose` true).
  Marsh's come from `character/marsh-diagnostics-v7/frames/salvage-*` and are dry standing
  poses (`crew_water_pose` false), so he stands on nothing in open water.
- Wanted: `salvage-east/north/south/west` for Marsh as water poses, 6 frames over 900 ms like
  the current ones, that read as working on wreckage while floating.

Done when: the owner accepts Marsh salvaging beside Bill, and the new frames carry
`"water": true` in their manifest state.

## 5. Bill: helmeted walk north is still the old painting

Already in the art queue.

- Bare `walk-north` is on the 256 canvas (pivot 128,224) from
  `character/bill-walk-north-master-head-v1`. The helmeted `walk-north` frames are still on the
  184 canvas (pivot 92,172). Both declare standing height 148, so they are the same size on
  screen, but the helmeted frames did not get the repaint. Every other walk facing matches.

Done when: helmeted `walk-north` is on the 256 canvas, frame for frame with the bare clip.

## 6. Optional: locked blueprints as a mystery

Report 13:39 ("Not unlocked rooms should be grayed out and more of a mystery before
unlocked").

Claude will grey the locked cards in code first and show the owner. If the owner then wants
painted silhouettes or a "signal obscured" treatment per room, that becomes art work here.
Do not start this until asked.

## What Claude did from the same reports (do not duplicate)

Details are in `docs/CURRENT_STATUS.md`, October 13.

- 13:27 Marsh's head through the airlock wall: fixed in code (aa587633). Crew stand nearer
  the south wall of a chamber that lies east-west. No art needed.
- 13:29 card title text: open, waiting on the owner's choice of hover style.
- 13:31 Marsh stuck on Margot and River: fixed (7a7066e0).
- 13:35 Journal crew roster: portrait fixed (94a183c3); the berth count is the owner's call.
- 13:39 Meta Progression: scroll jump fixed (3270479f); locked blueprints use the Codex's
  "signal obscured" card and a purchase shows the recovered room (c55e8a60). Item 6 above
  stays optional and unrequested.
- 13:40 the 3.4 s frame was the Room Layout Studio opening: fixed (f612f57d).

## When you hand back

List, per item: the folder you staged, the catalog lines you changed, the tests you ran with
their result lines, and the before/after image. Say plainly which items you did not finish.
