# Second game maintenance handoff

Updated: September 8, 2026 (Vancouver) · BrineSpace · `main`, local and uncommitted.

## Objective and acceptance

Owner requested another game-wide optimization, cleanup, bug-fix and polish pass.
Continued from the first pass, targeting additional defects and repeated work, with
broader comms, crew-save and economy coverage. This is source validation, not an
exhaustive playtest or acceptance of a newly exported binary.

## Accepted decisions and constraints

Normal costs/failures, three-cycle hidden discovery, open-ended expeditions and current
art are unchanged. No architecture split, asset regeneration, personal-save cleanup,
commit or executable rebuild. Earlier uncommitted work is preserved.

## Current state

- `scripts/main.gd`: the selected room inspector now refreshes once after its last
  water or crack disappears. Previously it could retain the old wet reading indefinitely.
  The half-second status cadence remains.
- `scripts/run_save.gd`: reject invalid speed indexes, zero/nonfinite zoom, nonfinite
  animation clocks and invalid cycle timers before offering Continue or changing a
  station. Valid backups still recover invalid primary checkpoints. Successful direct
  restore clears stale error text. `scripts/run_manager.gd` owns the shared speed list
  used by runtime controls and checkpoint validation.
- `scripts/room_content_canvas.gd`: determine supported renderer fields when assigning
  a renderer instead of inspecting object properties for every room submission.
  `scripts/room_layout_store.gd` reports whether it applied a layout;
  `rooms/full-wall-v1/split_wall_prop.gd` skips the redundant final geometry hash when
  nothing changed.
- `rooms/whole-room/nursery_whole_view.gd` and `connected_rooms_view.gd`: share the two
  repeatedly loaded immutable source atlases. Loading still uses raw PNG bytes, with
  no editor import dependency. Source timestamp changes replace cached entries.
- Extended `test_inspector_refresh.gd` and `test_checkpoint_isolation.gd` with reproduced
  failure paths. Added `test_shared_room_sources.gd` with paired `.gd.uid` for sharing,
  native size/pixels, timestamp refresh and bounded cache checks.
- Updated `test_content_cache_parity.gd` to use the current complete architect thaw and
  disable pointer-driven UI animation during comparisons. It and
  `test_layout_performance_guards.gd` now reject headless execution explicitly.
- `playtest_paid_opening.gd` buys its second generator before support rooms in the
  two-generator comparison. This changes the controlled fixture plan, not gameplay
  costs or supplies. It and `test_station_systems.gd` stop and drain audio before freeing
  nodes, using the production shutdown helper.

## Verification

[Summary and full logs](../output/game-maintenance-pass2/verification-summary.json):
21 latest targeted fixture invocations return zero without script/assertion/resource
errors. Coverage includes comms context/archive, crew death/save, cold store/galley/
workshop economy, inspector and checkpoint regressions, Save/Continue, station systems,
flood rendering, all 188 door-layout combinations, Studio workflow/performance, HUD,
wet doors, shared sources, native Save & Quit and paid salvage openings. Godot 4.6.1;
APPDATA and LOCALAPPDATA were isolated per fixture.

All **33 native retained-versus-direct render comparisons are pixel-identical** across
rotations, power/light changes, camera movement, crew animation and construction.
The later shared-source loader also passes direct GPU/source pixel equality checks.
Reviewed the native mixed-station capture. [Pixel results](../output/game-maintenance-pass2/pixel-comparison.json).

The dense 49-room profile is effectively unchanged: **25.205 ms dry / 34.312 ms flooded**,
versus 25.221 / 34.120 ms after the first pass. No additional frame-rate improvement is
claimed. A frame-connection cache experiment was removed because it did not help.
Source sharing removes repeated atlas decoding/allocation; no startup-time or total
memory reduction percentage was established.

The original late-second-generator salvage plan failed to afford that generator.
The revised early-generator plan completes with normal paid costs. Both the one- and
two-generator stations survive five simulated minutes; the native two-generator run
records no wait for stored Power, while the one-generator station waits 282.3 seconds.
This is a controlled-blueprint comparison, not evidence that every draft/order is viable.

Verbose evidence traces the lingering headless economic-fixture shutdown warning to
Ogg music playback. The same updated fixture passes natively without those errors;
the station-system fixture and native Save & Quit also finish cleanly. The headless
driver warning remains a documented limit. Earlier failed attempts and logs are retained.

## Next action

This second maintenance round is complete. A fresh integrated package and sustained
normal-play acceptance remain next, especially early generation choices, multi-crew
traffic and shortages. Dense rendering still exceeds the 60 fps budget. Owner pacing
and visual acceptance remain pending.
