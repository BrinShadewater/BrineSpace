# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill east seated renderer selection

## Objective and acceptance
Continue the full master-consistent Bill set and final cross-animation polish.
Select all six authored east seated actions, preserving exact source pixels.
This milestone establishes normal renderer selection; the full goal stays active.

## Accepted decisions and constraints
Use independent east sources and native east helmet, master matte grade,
shared256px plane/pivot128,224/standingHeight148, planted sole223. No new room
activity or furniture geometry is introduced to manufacture directional coverage.

## Current state
Twelve gear states/72refs: sit-down, sit-rise, sit-idle, read-seated, tablet entry
and exit. Consolidated bare/helmet manifests use whole literal res paths to the
three authored source packs. Build/verification/source-bindings retain hashes.
scripts/grid_canvas.gd loads both manifests before rebuilding animation arrays;
character/ACTIVE_ASSETS.json records bill-east-sitting-family in both overrides.
tests/test_bill_seated_east_selected_renderer.gd and paired UID test the normal
loader without candidate injection. Actor/controller behavior is unchanged.
index.html shows the complete sequence, with gear and station-scale controls.

## Verification
90 package checks and320 native checks PASS10.49sec. All72 loaded references
match source pixels; plane, dry pose, elapsed selection, finite terminal hold and
eight paired stage joins pass. Fresh native82px full-family contact reviewed.
All2,914 real non-log profile files unchanged under scratch APPDATA.
This does not establish autonomous east seated/reading service, real furniture
contact, interruption or checkpoint behavior. Actor reading snapshots continue
to support north/south only. Candidate source evidence remains in each pack.

## Next action
Audit existing east furniture/activity consumers before adding controller support;
do not infer chair facing from room rotation. Complete west seated source coverage
and remaining life/rest coverage, then cross-animation material/proportion/pacing
polish. Retain the tablet lift-and-settle gesture for motion review.
