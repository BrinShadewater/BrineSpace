# Bug-fix session — September 10, 2026

Track 1 of the audited plan: gameplay bugs found by code inspection and test-sweep
triage, fixed with focused tests. Source checkout only; no executable rebuild, no
commit or push from this session. Owner visual/pacing review of the behavior
changes remains pending.

## Gameplay fixes

1. **Companion water hysteresis** — `scripts/companion_water.gd` mode thresholds
   gained a 0.03 release band (mirroring `flood_alerts.gd`), so a water level
   oscillating at 20/25/50% no longer flips modes every frame and permanently
   starves Margot/River personality actions via the 12s cooldown reset. Josh's
   nav-graph cell blocking uses the same band. Waking from offline now plays the
   recorded `powerdown-exit` clip instead of snapping to the dry sprite.
   Evidence: `tests/test_companion_water.gd` (three new band assertions + wake
   clip check) PASS; `tests/test_companion_personality.gd` PASS.
2. **Flood alerts on resume** — `flood_alerts.acknowledge_existing(game)` seeds
   announced stages during `run_save` restore, so loading a checkpoint no longer
   re-announces every pre-save flood as urgent; stage *increases* after restore
   still announce. Evidence: `tests/test_flood_alerts.gd` (two new assertions)
   PASS; `tests/test_run_save.gd` PASS.
3. **Flood-retreat re-validation** — `scripts/flood_safety.gd` re-checks the
   chosen refuge on a 1s cadence during the retreat (the swimmer's own transit
   spreads water forward) and re-routes if it flooded or cracked. Evidence:
   `tests/test_flood_retreat.gd` second-scenario assertions PASS.
4. **Journal pet refusal reason** — `Companions.pet_refusal()` reports the actual
   `can_pet` failure ("wait for the water to recede" / "give her a moment" /
   "she is out of reach") instead of always "resume expedition first".
   Evidence: swimming-Margot journal assertion in `test_companion_water.gd`.
5. **Crew rest regression (rotation 2)** — `scripts/crew_room_activity.gd`:
   a berth authored against the west wall now approaches from the east side
   (the west approach fell outside choose_goal's ±144 service band), and a
   lounge quarter whose authored layout replaces the games table with a sofa
   now offers the sofa as the rest station. Both honor the authored layouts
   rather than moving furniture. Evidence: `tests/test_crew_life_rooms.gd`
   0 failures / 72 cases (was 12/69; matches the Sept 8 baseline again).
6. **Rotated-door wall bug** — `rooms/whole-room/nursery_south_facing.gd`
   `configure_embedded` now treats the game's `open_sides` (database door mask at
   the actual rotation) as authoritative instead of re-checking the view's
   pinned-rotation port mask, which walled over rotated doorways in navigation
   for views that pin `rotation:0` (cold store, galley, observation, salvage).
   Unreachable in current gameplay (those rooms are `fixed_rotation:0`), but the
   blockers were wrong and any future rotation unlock would have shipped sealed
   rooms. No behavior change at rotation 0; `test_preferred_room_layouts` (176
   furnished orientations, all ports connected) PASS.

## Robustness and test-infrastructure fixes

7. **MetaState isolation** — reassigning `meta.save_path` (the standard fixture
   isolation step) now resets the in-memory profile and loads the new path, so
   the developer's real unlocks can no longer leak into tests. New
   `tests/test_meta_isolation.gd` PASS; `tests/test_marsh_unlock.gd` now fully
   PASSES with no other change (its four failures were all profile leakage).
8. **Josh swim-clearance guard** — `bill_npc.swim_segment_clear`'s lazy loader
   refuses companion scripts instead of silently handing Josh Bill's human diver
   silhouette.
9. **Settings panel crash guard** — `settings_panel._rebuild` returns when the
   deferred call fires after the panel left the tree.
10. **`tests/test_bill_npc.gd` modernized** — records the post-thaw crew state
    (awake-start was retired Sept 8), places Bill on a spawn-clear standable
    node, and honors `fixed_rotation` in the per-room navigation sweep. PASS
    (176 room/rotation checks).

## Verification

Full regression batch on affected systems, all PASS: companion water,
companion personality, flood alerts, flood retreat, run save, meta isolation,
marsh unlock, crew life rooms, bill NPC, room catalog cards (47), NPC segment
clearance, layout free placement, preferred room layouts (176 orientations).

## Limits and open items

- `art_variant` was confirmed texture-only (corridor dressing + card variant
  selection); its absence from the room-geometry cache key is benign.
- The rotated-door conflicts for the four `fixed_rotation` rooms (pinned aisle/
  office furniture vs. rotated doors) become relevant only if those rooms ever
  unlock rotation — an owner design decision, recorded here, not changed.
- Headless test sweep results and triage: 84/165 pass headless; ~54 timeouts are
  environmental (unguarded `await RenderingServer.frame_post_draw` or
  `get_texture().get_image()` under the dummy driver); remaining stale tests
  (construction queueing, ward recovery, retired doctrines, dressing-aware
  registration counts) are catalogued in the session plan for modernization.
- No native visual captures were taken this session; the changes are logic-side
  (navigation blockers, thresholds, messages). The wall-edge change alters no
  reachable rendering state, but a native spot check of the four fixed-rotation
  rooms at q0 is cheap insurance during the next art session.
