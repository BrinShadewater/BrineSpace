# Diving airlock hatch integration

Updated: September 26, 2026 · BrineSpace · Native airlock pilot

## Objective and acceptance

Install the approved browser hatch artwork and crew sequence in the existing
diving airlock. Review actual departure and return in all four rotations.
Department door families were already installed by the architecture rollout.

## Accepted decisions and constraints

Outside-facing steel depth is 11 units in every rotation. North keeps its raised
frame; other directions use the overhead rim. Inner door uses the airlock family
at 18-unit depth. Crew wait facing the moving outer hatch, cross straight through
the open aperture, and remain swimming until the chamber drains. Beacons rotate
once per 2.5 seconds with 85-unit reach, 1.25-second warning before requested door
travel and 2-second linger. Equalizing/depressurizing provide advance warning for
automatic openings. Existing interlocks, power holds, costs and finite cargo remain.
Expedition endurance admission includes the added wet holds and departure seal.

## Current state

- `rooms/doors/ocean_hatch.gd`: approved rim, connected steel planes, restrained
  wet face tint and foreground frame pass; removes old edge-on face strips.
- `rooms/underwater/airlock-v1/airlock_view.gd`: thick department inner door,
  warning beacons and readable chamber swimming without changing general flood art.
- `rooms/whole-room/painted_shell.gd`: continuous north lintel and exterior cap
  aperture reserved on all rotations, independent of station connection ports.
- `scripts/grid_canvas.gd`, `scripts/room_content_canvas.gd`: frame layering,
  water-aware door invalidation and per-room retained caution state.
- `scripts/airlock_cycle.gd`: saved warning lead/linger with pause and power holds.
- `scripts/crew_expedition.gd`, `scripts/room_flooding.gd`: facing waits outside
  during closure and swimming throughout draining.
- `assets/room-cards-v2/airlock.png`: rebaked with a scratch copy of owner layouts.
- Airlock, exterior-hatch, clearance and diver-mining fixtures updated. The mining
  fixture supports rotation and capture directory arguments for actual journeys.

## Verification

Headless airlock equipment/interlock/save tests and six Marsh expedition journeys
pass. Native exterior-hatch pause, power interruption and save/restore pass.
Bill's native mining journeys cover all four rotations, both aperture crossings,
departure closure waits, drainage, checkpoint restore and exact cargo delivery.
Captured swimming, opening and closing states are reviewed in the native gallery:
`output/airlock-integration-2026-09-26/review.html`. Logs and isolated APPDATA folders
are beside it. Earlier captures revealed faint submerged actors and unsplit side
caps; the final captures supersede those intermediate images.
Before/after owner-folder fingerprints show unchanged save, checkpoint, comms,
preferences and layouts; only the transient `.recovery_mode_lock` disappeared.
Tests all ran with scratch APPDATA. Native evidence contains 20 captures.

## Next action

Owner visual/play acceptance in the source game, then rebuild the playable package
if requested. Existing executables do not contain this change. No release export,
commit, push or publication was performed. The preview's fixed 45-second loop is
not installed as a gameplay timer: actual expeditions drive the existing cycle.
