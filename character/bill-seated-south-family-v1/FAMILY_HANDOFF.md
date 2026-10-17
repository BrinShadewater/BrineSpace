# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill south sitting and reading

## Objective and acceptance
Continue the full master-consistent Bill animation set and final consistency
polish. This milestone selects south sitting, breathing, reading and tablet
entry/exit in both gear states. Owner visual acceptance remains separate.

## Accepted decisions and constraints
Preserve the selected matte master, native helmet and 256px figure plane
(pivot 128,224; standing height 148). Keep the nominal 12-second reading budget:
0.48 take-out, 11.04 reading, 0.48 put-away. Sit/rise remain 0.65 seconds in
the observation service. Tool stages retain the full seated furniture offset.

## Current state and changed files
The consolidated manifests select 12 gear states and 72 source references.
`scripts/grid_canvas.gd` loads this family and rebuilds retained cosmetic arrays;
`character/ACTIVE_ASSETS.json` records the selection. Source packs retain their
historical staging metadata; this family is the current selection authority.

`scripts/bill_npc.gd` and `scripts/crew_life.gd` wire Bill's south tablet stages,
timers, saved cached pose and service-loss cleanup. Actual Bill uses
`major_bill_npc.gd`; the new tablet sequence is restricted to Bill's classes.
The first 60ms exit slot retains the currently displayed whole reading pose,
including its hands and prop, across restores. Partial entry reverses only
performed motion. Partial observation sitting now retains its reverse pose and
furniture translation; that helper is inherited, while this evidence tests Bill.

## Verification
90 family hash/registry/whole-path/timing checks pass. Normal-loader native
fixture `tests/test_bill_seated_south_family_selected.gd` passes 559 checks in
45.59 seconds: 72 frame bindings, real sofa approach/stages, 64 scene captures,
28 partial sit/tool entry interruptions, 12 arbitrary reading-phase interruptions
and ten actual disk checkpoint restores. Fresh bare/equipped sofa captures were
visually reviewed. Scratch APPDATA isolated every run; all 2,914 real non-log
profile files remained unchanged.

The fixture explicitly selects the real reading station, then uses Bill's real
route and activity stages; autonomous goal selection is outside this evidence.
Rejected expanded run: 28 failures, including boundary ticks consuming newly
reversed motion and a fixture that discarded required recovery wards. Runtime
cleanup now returns before consuming that tick; the fixture preserves wards.
Previous 305-check normal sequence pass and candidate reports are narrower
historical evidence, not this final expanded proof.

## Remaining work and next action
Other directional seated/reading and life/rest families, broader world journeys
and final cross-animation material/join polish remain. Later cached-to-authored
exit joins merit the full-set visual pass. Full goal remains active.

