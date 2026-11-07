# Room flooding and crew survival

Updated: September 8, 2026 · BrineSpace · Flooding implementation

## Objective and acceptance

Rooms accumulate water from hull cracks and open connected doors, drain through
powered pumps, and expose crew to staged movement and survival consequences.
Focused logic, expedition/locker integration, disk checkpoint and native stage
checks pass. Owner pacing and visual acceptance remain pending.

## Accepted decisions and constraints

Owner rules: low water preserves walking speed; medium slows walking; high uses
swimming; critical water permits drowning. Breath lasts 15 simulation seconds;
helmet tanks last 60. Exterior exposure without a helmet kills immediately.
Empty Food starts starvation, rather than the former instant cycle casualty.

Provisional tuning: medium 25%, high 55%, critical 85%; walking multipliers
1 / 0.65 / 0.55. Full crack severity admits 4% compartment volume per second;
powered, unsuspended room pumps remove 0.8% per second. Actual animated door
aperture and level difference determine inter-room flow. Closed doors seal it.
Normal containment faults create 35% crack severity, worsening on recurrence.
Containment repair or the inspector's 2-Metal hull repair seals the crack without
removing accumulated water. The existing PUMPS control also retains its previous
water-production role. Airlock pressure-chamber water stays separate from the dry
preparation compartment and follows the same breathing thresholds during transit.

Starvation kills after 90 seconds without Food; restored supplies reverse accrued
starvation at twice that rate. Dry breathable air restores bare breath; tank air
refills only at a powered diving locker, at 12 seconds of air per second. The
REFILL OXYGEN button sends a helmeted crew member along the real locker route.
Expeditions reject routes beyond tank range and recall at 25 seconds remaining;
power outages and obstructed returns can still exhaust oxygen. Existing paid
construction, room economy, station failure conditions and discovery remain.

## Current state

New simulation/render module: scripts/room_flooding.gd. Integration touches main,
bill_npc (shared by the other architects), grid_canvas, airlock service/panel,
crew_expedition, hardware_panel, local_incidents and run_save. Crew oxygen,
starvation, room water and cracks persist; older saves receive defaults. Room
inspector shows stage, repair and nearby crew air; roster also reports timers.
Water tint, ripples, crack jets and a depth gauge use the live foreground. Narrow
corridor overlays use the existing rotated floor polygons.

Tests added: tests/test_room_flooding.gd and tests/playtest_room_flooding.gd,
with paired UIDs. tests/test_station_systems.gd now clears the fixture's long
exterior detour and performs an actual locker refill before its second trip.
No commit or build publication. Earlier unrelated working-tree edits preserved.

## Verification

Godot 4.6.1:
- test_room_flooding.gd: PASS, leak severity, conserved open-door transfer,
  closed doors, power/pump/pause, movement stages, exact air deadlines, exposure,
  starvation/recovery, roster death, damage/paid repair and invalid water saves.
- test_station_systems.gd: PASS, full expedition and recall, actual refill route,
  interlocks, checkpoint and existing station controls. Its shutdown still reports
  two resources in use; this also appeared in the initial regression run.
- playtest_room_flooding.gd: PASS, real disk write/read/restore of water/cracks and
  individual survival clocks; native 1600x900 stages captured and visually reviewed.
- Scoped git diff --check: clean. Full logs: output/flood-unit.log,
  output/flood-systems.log, output/flood-native.log.

Native images: output/flood-stage-12.png, flood-stage-35.png,
flood-stage-65.png and flood-stage-93.png. These establish bounded stage rendering,
not prolonged play balance or all corridor/room layouts. No new raster art.

## Next action

Play a normal expedition with a containment leak. Review water readability,
thresholds, drain rate, starvation pacing and return reserves. Tune those constants
from owner feedback; do not treat this bounded pass as full-game acceptance.

## Follow-up: continuous flooded transit demonstration

Owner requested a visible test of swimming between rooms. The new
`tests/playtest_flooded_transit.gd` stages Bill, Veld and Branforth in a flooded
Storage Bay, through a shallow corridor and into a nearly dry Storage Bay.
Initial levels are 82%, 35%, 2%; pumps are off and real animated door apertures
transfer water. The fixture uses production geometry, swimming route planning,
crew movement, avoidance and water simulation. Only the test layout and initial
crew placements are staged; normal expeditions and user saves are untouched.

Headless and native traces pass all three complete routes and swimming-to-walking
transitions. Native evidence reviewed at startup, first doorway, second doorway
and completion. Replay: output/flooded-transit.mp4, 35.4 seconds, 15 fps, 1160x480;
531 contiguous native frames encoded and the complete MP4 decoded without errors.
Caption overlay describes the stages; gameplay pixels are the native capture.
The right room starts at 2% and reaches 29% through door flow, so it eventually
requires wading too. This is a continuous controlled demonstration, not a normal
paid survival run. Logs: output/flood-transit-check.log and
output/flood-transit-native.log. The final poster is output/flooded-transit-poster.png. Run the script with `-- --live` for a visible test
that remains open, or `-- --record` to capture 15-fps frames under
`output/flood-transit-frames`. No gameplay code changed for this demonstration.
