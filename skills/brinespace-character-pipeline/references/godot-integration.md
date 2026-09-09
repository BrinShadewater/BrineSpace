# Godot integration

Use this reference when the requested work changes a character's runtime behavior
or connects an animation pack. Inspect current code; these paths describe the
Bill/Veld prototype, not a requirement to preserve every implementation detail.

| Concern | Existing location |
|---|---|
| Crew update and game integration | `scripts/main.gd` |
| Navigation, geometry cache, needs, local avoidance | `scripts/bill_npc.gd` |
| Science preferences and action meanings | `scripts/veld_npc.gd` |
| Manifest playback and per-character clock | `scripts/crew_sprite_player.gd` |
| Character rendering and doors | `scripts/grid_canvas.gd` |
| Layered prop/crew depth | `rooms/whole-room/nursery_whole_view.gd` |
| Corridor geometry | `rooms/underwater/corridor_geometry.gd` |
| Checkpoint serialization | `scripts/run_save.gd` |

Keep changes narrow. Follow AGENTS.md's limits on refactoring `main.gd`, prototype
economy, hidden discoveries, and player saves. New crew appearance/behavior does
not imply staffing bonuses, research rewards, or resource consumption.

## Integration checks

- Separate shared frame data from each actor's playback clock, needs, destination,
  and random state. A new NPC should not perturb the station's random sequence.
  For reproducible multi-crew fixtures, seed every actor's decision generator,
  not only the station RNG. Record trajectories and compare repeated same-seed
  runs before interpreting different outcomes; keep a varied seed set and retain
  failures rather than choosing only a passing seed. Do not seed normal play.
- Advance locomotion from actual travel with the current stride convention.
  Account for state/direction changes, pause, speed, and position discontinuities.
- Match action duration and controller stage transitions. Check interruption when
  a destination becomes unavailable, including recovery from kneeling.
- Use room-local geometry and actual prop footprints. Preserve connected-door
  routing while allowing reachable interior destinations. Test swept movement,
  not just whether the destination is clear.
  Spaced point samples can miss a short corner intersection that incremental
  movement catches later. Keep planned shortcuts and actual movement consistent;
  test near-tangent wall/prop corners in both directions and retain a safe bend.
  Do not enlarge a door or move furniture to conceal a clearance-test false negative.
  A movement tick can consume a waypoint and turn: its endpoint chord is not
  necessarily the traveled path. On a chord failure, retain the consumed waypoints
  and check each traveled leg before changing geometry or weakening a test.
  The test-only `tests/traced_bill_npc.gd` observes production movement without
  replacing it; its regression checks safe bends, real corner cuts and stopped
  attempts. Use the sum of traveled leg lengths for speed checks. Keep this
  instrumentation in fixtures, not in the shipped controller.
  Record simulation tick size and capture cadence separately. Continuous movement
  assertions with sparse screenshots do not establish full-speed animation
  quality; inspect rear-hull silhouette projection separately from foot clearance.
  Seeded comparisons also require matching scene/controller/geometry revisions;
  a seed alone does not freeze a concurrently edited station.
  For a failed crew detour, inspect the join from the off-grid foot to the graph,
  not only the graph route. The nearest static-clear node can be behind a peer
  while another reachable join is clear. Reproduce recorded positions with and
  without the peer before changing room geometry or increasing retry budgets.
  A clear entry can also be isolated by padded peer-node exclusions. Check that
  it has a complete route before accepting it; a farther safe entry may remain
  connected. Preserve clearance and restore temporary graph exclusions between
  candidate attempts. Keep the recorded stationary-peer probe distinct from a
  replay of the full multi-crew history.
  An exactly tangent planned segment can fail after incremental float movement.
  Replay the recorded full segment with production ticks and compare the stopped
  remainder against the same blockers before moving furniture. If adding a small
  planning margin, retain cell ownership and collision clearance; test the original
  target via a safe bend, reverse/rotated cases and existing crew passing.
- Register drawing and depth at the feet; review whole silhouettes near walls,
  props, and doors. Foot clearance alone cannot certify that a head stays behind
  the correct hull layer. Check layered rooms, corridors, and legacy consumers.
- Doors must respond to the new actor independently. Shared embedded room views
  must clear temporary actor lists so characters do not appear in unrelated rooms.
- Preserve independent clocks and applicable NPC state through save/Continue.
  Validate malformed data before mutation and preserve old checkpoints without
  crew data. Keep fixture saves and display preferences isolated from player data.
  Continue replaces controller instances. Reacquire them from the restored game
  before comparing snapshots or advancing movement; old references can falsely
  report lost paths. For yielding, test an actual mid-retreat disk checkpoint,
  intent restoration and completed travel separately from ordinary idle saves.

Current avoidance maintains 20 canonical units between crew foot centers and
supports local yielding/detours for two characters. It is not a population-scale
crowd system. Adding a third actor requires checking actual multi-peer avoidance;
the existing head-on pair test does not establish that behavior. Existing work
actions face east; choose compatible approaches or
explicitly add the requested directional coverage. Do not shrink collision areas
or disable normal run rules to make a fixture pass.

## Relevant verification

Locate Godot 4.6 from the environment; do not embed a developer's executable path.
Typical headless invocation from the checkout:

```text
<godot> --headless --path . --script res://tests/test_dr_veld.gd
```

Select tests for affected behavior, adapting/extending them for new crew:

- `tests/test_major_bill_animations.gd`: Bill coverage, timing, transitions.
- `tests/test_dr_veld.gd`: Veld pack plus independent behavior/playback and doors.
- `tests/test_bill_npc.gd`: room navigation and rotation coverage.
- `tests/test_crew_polish.gd`: passing, clearance, saved action restoration.
- `tests/test_run_save.gd`: checkpoint and Continue regressions.
- `tests/playtest_dr_veld.gd`: native rendering and action review fixture.

Run native evidence for changed rendering/motion; headless success is insufficient.
On Windows, wait for a GUI Godot process to finish and read its log rather than
assuming the shell returning means the test completed. Fixtures should set their
isolated preferences before scene initialization. Package/export verification is
separate and needed only when packaging is in the requested scope.

Installation activity: derive operator-side approaches from current prop bounds, allow alternate positions along that edge, and let the existing navigation graph prove reachability. Use a doorway-side start for a doorway approach fixture; arbitrary farthest nodes can be isolated pockets. Preserve authored direction coverage: east interaction is not a four-direction work pack, and standing rest is not seated rest. Save ordinary action fields and check disk restoration plus service interruption. See docs/CREW_ROOM_ACTIVITY_2026-09-08.md.

Portrait comms: keep the panel within station-view bounds rather than over the HUD. Separate session history from persistent speed preferences; replay must not append duplicate history. Gate generic discovery dialogue after accepted discovery and never disclose hidden recipes. Warn on low AND declining reserves, not unused zero stock. Bound ambient cadence and event duplicates. Check both small-window containment and contextual event state. See docs/CREW_COMMS_2026-09-08.md.

Completion dialogue must consume an explicit successful activity event, not infer success from changed status text. Test natural timer completion against a power-interruption negative control. Persistent comms archives use validated bounded entries and temporary-file replacement; preserve malformed originals. Derive fixture archive paths from isolated run-save paths so tests never alter player history.

Interactive comms: distinguish fresh scene startup, Continue, and in-scene loop restart; reset transient dialogue keys on restart while retaining archives. Consume crew clicks before room selection only when no blueprint is selected, using the rendered foot/body scale. Test construction precedence, absent/dead actors, pending-report retention, reply reveal timing, and expanded panel containment at the minimum window size. Read contextual replies from current actor/room and resource forecast state; do not expose hidden recipes.

Contact pickers must refresh available living actors when opened and revalidate on selection. Switching manual contacts should preserve pending reports. Queue priority should preserve arrival order among urgent reports and avoid replacing the message being read; test these independently from the visual urgency cue.

Closing a conversation should distinguish minimizing from discarding queued events. Verify that hidden typewriter progress stays fixed, the inbox respects overlay and viewport bounds, and contextual journal navigation restores the prior pause state. Describe scene-local unread retention separately from persistent displayed history.

Character dialogue: keep authored opinions separate from live resource/activity values. Room flavor must not imply machinery is operational unless that state is checked. Preserve a definition fallback for rooms without authored lines, verify numeric substitution for every speaker, and distinguish writing review from runtime tests.

Room conversations should label observed operation separately from a next-cycle forecast. Snapshot the discussed cell/type for contextual actions, validate it before locating, and do not silently retarget an old reply to the actor's new room. Explain when asking again refreshes status.

Owner-directed compact comms supersedes the expanded popup guidance: visible controls are only Next/X, with side-panel access. Measure auto-dismiss from text completion, not message arrival; test manual reveal, new dialogue after close, queued advance, overlay suspension and the exact visible control count. Do not restore earlier controls merely because their data helpers remain.


## Recovery, androids and recap discoveries

Keep permanent unlocks, current-loop physical recovery and selection independent.
Record first-time successful unlocks for the loop recap; include architects and
companions, avoid duplicates and do not count an already-unlocked starter again.
Save that loop record explicitly. Older checkpoints default to no recorded new
characters, and a new loop clears the record. Exercise recovery, repeat recovery,
Continue, legacy saves and new-loop reset. Derive accepted IDs from current cast
registries when extending the roster; do not silently omit a new companion.

Marsh's approved contract is an android, not a human with invisible helmet art:
no breathing or helmet requirement, powered charging-pod recovery, visible white
fluid in connected tubes, then wake. Battery return/charging replaces oxygen as
his tradeoff. Apply this across survival, routing, expeditions, equipment UI,
forecasts and Save/Continue. Keep battery balance numbers in game data/current
notes rather than treating today's tuning as a pipeline invariant. Preserve
partial charge, prepaid power and outage progress. A docked actor must not also
render as a duplicate floor actor.

For exports, use the checkout's docs/RELEASE_WORKFLOW.md. Native editor success,
PCK asset validation and actual release gameplay are different evidence scopes.
