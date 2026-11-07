# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James crew-traffic turns

## Objective and acceptance
Continue James's full animation and consistency goal. This is agent-verified traffic
coverage, not full-set completion or new owner visual acceptance.

## Accepted decisions and constraints
Keep the selected masters, anatomical density, matte colour grade, equipment and clocks.
Existing reversible-work authorization applies. No runtime art/code, layout, export or
commit changed in this pass; the preceding waypoint/turn-clearance fix remains selected.

## Current state
`character/james-console-water-exit-turn-v1/build_native_traffic.py` derives
`native-traffic.gd` from the preceding next-task fixture. The native main crew update
runs flooding/vitals, safety, peer avoidance, chooser/update and passage yielding.
After normal console service/egress, normal seed17 curiosity selection gives James his
next path. A fixture recovered Bill is placed48 units ahead in a clear adjacent-room
lane, idles naturally and may yield; James's path/facing are not injected. Equal initial
water and disabled fixture pumps isolate traffic from changing flood height.

## Verification
98,686 checks, eight journeys (four rotations, bare breathable.65 and sealed
helmet.95), eight actual detours, peak wait291.7ms in every case, 30 ordinary turns.
All turn starts and finite completions pass, all journeys reach the next task, selected
poses fit their actual swim/tread profiles, and foot separation remains at least32 units.
Current recovered-roster rules exclude unintended Veld/Marsh spawning. Clean native log,
exit0, no timeout and real profile unchanged under scratch APPDATA. Bare/helmet waiting
native screenshots visually reviewed: bodies separated and James turns away from Bill.
These stills are not an exhaustive per-pixel overlap audit of every frame.

Investigation retained in `initial-traffic-*`, `tread-profile-diagnostic-*` and
`legacy-extra-peer-traffic-*`. First fixture wrongly treated a restart after treading
as an ordinary turn and used swim clearance for a stationary tread. Clearing architect
state enabled legacy presence and allowed Veld to respawn during full main update;
the final fixture retains current roster rules and asserts no unintended actors.
Those earlier intervals are diagnostic evidence, not the final scoped proof.

## Next action
Continue other traffic patterns, equipment transitions and complete furniture/meal and
exterior/airlock return journeys. Other seeds/layouts, high-water bare survival and
all-frame pair silhouette overlap remain distinct. Full James goal stays active.
