# Marsh bedside integration handoff

Updated September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Replace Marsh's broken berth presentation with connected bed-edge sitting,
leg swing, sleep and rising. The compatible legacy berth is now integrated;
one seeded approach/departure review also passes. Bought-bunk support and packaged
acceptance remain open. The broader animation/furnishing goal is unfinished.

## Accepted decisions and constraints
Marsh only, unmirrored compound bed/cabinet with a clear bedside notch. Preserve
owner room layouts. Other actors and unsupported furniture retain existing clips
and 0.8-second timings. No Higgsfield, new generation, commit or publication in
this integration step. Source generation evidence is in the earlier contact report.

## Current state
- `character/marsh-berth-v1/` preserves raw source, exact prompt and review.
- `tools/build_marsh_berth.py` extracts six registered poses, uses exact canonical
  idle-east, and packages lie/sleep/reversed-rise in Marsh's supplemental catalog.
  Transitions take 1.6s, including an edge-seat hold before the leg swing.
- `scripts/marsh_npc.gd` selects the profile, retains contact anchors in saves,
  controls presentation offset, and reverses from the current pose when interrupted.
  Low battery completes rising before charging travel begins.
- `scripts/crew_life.gd` supports actor-specific transition duration; the shared
  controller retains human limits and validates Marsh's extended saved timer.
- `scripts/crew_room_activity.gd` marks only the compatible close bedside station.
- Canonical rebuild invokes the new builder. Fixed Marsh's stale lookup for the
  archived sprite-polish-v2 source sheets and stabilized carry direction iteration.
  Furniture clips are excluded from Marsh's shared locomotion/swim clearance;
  the resulting clearance file is unchanged from the prior committed version.

## Verification
- Canonical Marsh rebuild passes, reproducing 211 original source frames.
- Supplemental build is deterministic; all six installed PNGs exactly match the
  reviewed 1.6s trial. PNGs are covered by Git LFS attributes.
- `tests/test_marsh_berth.gd` native pass: compatible arrival, matching clip/actor
  timing, five actual disk/staged restores with exact pose pixels and contact,
  simulation pause, reversed partial interruption, real service-loss interruption,
  normal sleep/rise completion, low-battery exit and invalid-save rejection.
- Existing native crew activity test: 36 cases pass. Existing Marsh battery test:
  headless pass, 93 route samples, including charging/expedition and old checkpoints.
  Existing seated-depth Python regression also passes.
- Live restored seat and recline screenshots reviewed at
  `output/crew-activity/marsh-berth/`. The initial camera capture incorrectly showed
  the core because zoom's deferred recenter replaced focus; final fixture supplies
  the berth center to zoom and asserts actual camera position before capture.
- Logs and build parity: `output/layout-default-audit-2026-09-21/`.

## Next action
Resolve saved Crew Hab q3's unregistered bought bunk, continue remaining
animation/furnishing work, and refresh
release packages. Current Windows/Mac packages predate this change; Apple Silicon
native testing and owner visual acceptance remain outstanding.

## Later travel and draw-order verification
The separate `marsh-berth-travel.gd` fixture starts Marsh awake at the core, seeds
needs/RNG once, and uses `_update_test_walker` and the normal goal chooser. It does
not assign a goal, route or arrival position. His controller chooses three rests
before leaving (fatigue, curiosity, fatigue); the fixture does not shorten them.

This exposed two additional installed fixes:
- A compatible bedside station now requests `exact_approach`. Navigation appends
  the final clear segment to its anchor before sitting, checking floor, crew and
  segment clearance. Previously a node inside the 36-unit activity tolerance could
  start the animation well away from the authored contact point.
- Shared room rendering exposes the unchanged default actor-depth calculation.
  Crew Hab overrides it only in the unmirrored compound prop's open notch, placing
  standing/walking crew in front of its shorter cabinet. Both retained and direct
  draw queues use the hook. Source pixels and room layouts are unchanged.

Final v4 run: 1,205 simulation samples (60.25s), 153 native captures, all rest phases,
completion and departure, zero failures. Exact arrival is checked for every lie
sample. Native approach and departure inspected: the cabinet no longer removes
the walking torso before/after the furniture pose. All 36 native crew activity
cases pass again with exact-entry and localized-depth negative controls.

Evidence: `output/layout-default-audit-2026-09-21/marsh-berth-travel-v4/` and
`crew-activity-bedside-depth.log`. The GIF is a live capture excerpt: entry followed
by the final rise/departure, with long sleep/repeated rests omitted. Earlier travel
captures missed the room, and v2 failed its first camera-center assertion; v3/v4
wait for the observable center before capture. Those failures were not acceptance.
