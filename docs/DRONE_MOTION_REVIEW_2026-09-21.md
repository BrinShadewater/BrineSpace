# Drone motion review — September 21

## Installed repair

The live grid uses `scripts/drone_art.gd` for flying fleet drones. Salvage working
art previously split the image at source y=220 and rotated both lower halves,
including the central winch/chassis through y=275. Native phase captures show that
body shearing. Its split now sits at y=280, with pivots at the actual lower arm
joints (60,275) and (300,275). Source art, bob, clocks, phase logic and navigation
are unchanged. Mining rendering is unchanged. Construction was subsequently repaired as below.

## Verification

Eight working poses per kind captured with the runtime drawing function; before
and after sheets inspected. Native regression tests salvage at two sizes/eight
phases: 16 poses, zero failures. It requires the central winch to remain identical
and claws to change. An output-only copy of the old implementation fails 12 checks,
proving the guard detects the repaired shear. The production source was not
reverted for that mutation check.

Evidence: output/drone-motion-review-2026-09-21/working-phases.png,
working-phases-repaired.png, source grids, regression.log and old-regression.log.
Maintained guard: tests/test_salvage_articulation.gd (+ UID and native lane).

## Remaining work

Construction welding-tip attachment is now corrected as described below. Mining's drill-width oscillation was
captured but not judged through a full flight sequence. Docking, bay transitions,
normal-zoom temporal review and matching drone material/detail to the bought art
remain open. A rendered phase sheet does not establish complete flight acceptance.

## Construction articulation installed

The original shared y=220 split also sheared the construction winch. Its rigid upper
halves now end at y=290 (left) and y=260 (right), with source pivots (65,290) and
(310,260). Each distal tool follows its own joint. Atlas pixels, palette, timing,
bob and navigation remain unchanged. Native eight-phase sheet inspected.

Construction regression: 16 poses at two sizes, zero failures; the original
implementation fails 12 checks. Salvage's 16 poses still pass. Mining/salvage rows
in the same native phase capture have zero changed pixels. Evidence:
working-phases-both-repaired.png, construction-both-regression.log,
salvage-both-regression.log and old-construction-regression.log in the same output
folder. Tests have paired UIDs and explicit native lanes. Full flight/docking and
welding attachment acceptance remain open.

## Welding endpoints attached

Construction beams now start at reviewed opaque source tool tips (112,370) and
(226,358), transformed by the same `_manipulator_point` function that positions
the articulated tool geometry. Both receive the same already-bobbed center. The
old independent 4 Hz spread no longer lets beams drift away from the 3.5 Hz arms.
Sparks retain their authored work-point effect; no gameplay target behavior changed.

Eight native working poses inspected in working-phases-attached-tools.png. Both
16-pose chassis/motion guards pass. Mining/salvage rows remain pixel-identical to
the prior sheet; salvage retains its original floating-point operation order to
avoid introducing tiny unrelated rasterization changes. No full flight/docking
acceptance implied. Next: in-game transition review and normal-zoom art matching.

## Hatch scale continuity repaired

Grid flight drawing previously ended launch at 65% scale but began outbound at
100%; returning had the reverse discontinuity at docking. Travel now interpolates
65%-100% over the same first/last 0.30 cell used to blend the hatch position offset.
Fleet phases, durations, routing and bay placement are unchanged.

Native `tests/test_drone_hatch_handoff.gd` calls the actual grid `_draw_drones`
renderer with an isolated fleet and fixed anchors. It checks non-empty drone pixels
and exact launch/outbound and return/docking boundary agreement for all three kinds:
six comparisons pass. An output-only old-grid copy fails all six. Its initial
mutation attempt had a duplicate global class parse error and was discarded; the
final copy removes the duplicate class declaration and runs the intended old path.
Logs: hatch-regression.log and old-hatch-regression.log in the review output folder.

This proves exterior hatch boundary continuity only. Owner bay layout/cradle
registration, whole-flight temporal review and normal-zoom style acceptance remain
separate open checks. Added paired UID and explicit native lane for the guard.

## Current bay layouts checked

Read-only audit used a copy of the owner's saved room layouts. All three bay views
retain non-hidden `_rov` and `_hatch` functional props in all four rotations; the
current layouts do not trigger missing-host center fallback. Native room review:
12 views, 1,920 walking samples, zero failures. Quarter-zero Mining, Construction
and Salvage captures inspected: docks/hatches are present and visibly placed.
Owner-layout bytes match the snapshot after review; no furnishing changed.

Evidence: bay-bindings.json, bay-layout-review.log, bays/ captures and copied
bay-owner-layouts.json under output/drone-motion-review-2026-09-21/. This establishes
static host placement, not a complete timed departure/return. The dock sprite uses
70 room units while flying base width currently uses 0.18*384=69.12, and body bob
begins at deployment; assess that small handoff difference in temporal review before
claiming exact cradle-to-flight continuity. The larger hatch scale jump is repaired.

## Construction trip through the live game

Output-only `construction_trip.gd` pays normal bay operation and advances the real
main process in 0.1-second steps. Observed docked -> launching -> outbound -> working
-> returning -> docking -> docked, with the ordered corridor present on completion.
Final dock reached at step 117 (~11.8 simulated seconds). Native process exits zero.
The first capture placed the work site at the viewport edge; a corrected camera
waits for initial UI layout and requires the working drone's center on screen.
Exterior work and restored dock screenshots inspected in trip-visible/; phases.json
and trip-visible.log record sequence and completion. This is sampled phase evidence,
not continuous video or all drone kinds/rotations.

Under-station invisibility is intentional: grid `_draw_environment_foreground` puts
ROVs below station floors, and tests/playtest_visual_refinement.gd explicitly checks
complete hull occlusion. Preserve that contract rather than putting launch drones
above the floor to make a capture look busier. Existing bay empty/restored behavior
matches the captured deployment. Owner layouts were read from the copied snapshot.
No production code changed in this trip review. Mining/salvage trips, further Bill
motion repair and broader room polish remain open.

## Mining and salvage live cycles

Both native fixtures now complete all phases, battery recharge and clearance, then
return to dock (step 334, ~33.5 simulated seconds). The first return at step 177 is
not completion: a 12-second extraction battery cannot finish 18 seconds of work.
Progress remains at 12 through recharge, reaches 18 on the second trip, and cargo
is present on return and empty after docking. No battery/gameplay rules changed.
Initial fixtures exited 1 because they stopped at the first return; corrected runs
exit zero and preserve the initial logs as evidence of the fixture mistake.

Evidence: mining-trip-complete.log, salvage-trip-complete.log, each trip's phases.json
and native phase captures under output/drone-motion-review-2026-09-21/.
These prove live lifecycle completion, not clear visibility of all working poses.
Mining working and salvage restored-dock captures inspected. The adjacent target's
nearest clear face can put the rendered worker mostly beneath the bay floor:
`underwater_visibility.drone_position` tests wreck obstruction but not occupied
station cells when choosing its work face. Preserve intentional hull occlusion;
review work-face choice separately before claiming visual acceptance. Owner rooms
remain unchanged.

## Exposed work-face selection repaired

`underwater_visibility.drone_position` now prefers an unoccupied, unblocked side of
the clearance target. It retains the closest clear covered side when every exposed
side is unavailable, and does not select outside the map. The offset blends over
the last/first 0.30 cell on outbound/return, avoiding a new work-boundary jump.
This same position feeds the rendered drone, its lamp and silt. Fleet routes,
progress, recharge and owner layouts are unchanged; survey illumination follows
the newly visible work position as intended.

Focused work-face guard passes: occupied-side avoidance, no simulation mutation,
phase-boundary continuity, unchanged distant travel, covered fallback, enclosed
target and map-edge cases. Native mining trip still clears/recharges/returns at
step 334; its working capture now shows the drone outside the bay floor. Native
underwater foundation suite passes zero failures, covering excavation, survey,
lighting and checkpoint state. Evidence: work-face-test.log,
mining-exposed-trip.log, mining-trip-exposed/ and
underwater-foundation-after-work-face.log under the review output folder.
This is one synthetic adjacent-target native case, not every real formation or
all-animation visual acceptance. Tests/test_drone_work_face.gd has its UID and
fleet subsystem registration.
