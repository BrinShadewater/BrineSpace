# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James underwater cargo integration

## Objective and acceptance
Continue full James animation replacement and cross-family polish. This milestone
installs cargo/activity/turn families; owner visual acceptance remains pending.

## Accepted decisions and constraints
Matte masters, fixed source skull rulers, sensible compact limbs, rigid case in
both hands, wrench on belt, forward blowtorch for salvage. Exact destination carry
seams and retained gameplay clocks. No per-pose height fitting or mirrored yaw.

## Current state
character/james-water-cargo-family-v1 and james-water-cargo-turn-family-v1 installed
through scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json. Clearance action
cargo/salvage envelopes and life cargo-turn profiles union actual selected alpha;
ordinary swim/tread/transition profiles preserved.24states/328refs in both modes.
ES/WN bodyv2 preservev1 helmets, SW/NE fullv2 correct yaw. Reviewed configs/builders
protected against accidental regeneration/reset. Source revisions and prompts retained.
Pipeline,bible,continuation and maintained/installed crew-consistency skill updated.

## Verification
712 cargo and1162 turn package checks PASS;1580 cargo and2780 turn installed player
checks PASS;2916 staged/2918 installed moving route checks PASS,24 authored two-leg
flooded-room paths,184turn refs,456 alpha samples.182 installed controlled exterior
salvage/pickup/recall checks PASS,32 reviewed captures; real owner profile unchanged.
Native82px contacts and four fresh installed route boards reviewed. Not all layouts,
pathfinder/traffic/exterior-turn proof, dispatch or full airlock delivery proof.

## Next action
Replace16 remaining states:swim-distress,recover-air,death-ground,death-water each
four directions, then cross-family material/anatomy/timing/readability polish.
Revisit cargo680ms halves versus800ms quarters, water arrival stop-facing snap,
flooded tint, helmet/case occlusion, compact legs and prior furniture journey limits.
Coverage173bare3196slots/171helmet3172slots,16retained; full goal remains active.
No jobs running, commit, export or full-set acceptance.


Latest polish supersedes the pending North dry recovery, cargo half-clock and disk-restored death-phase items here. See JAMES_CONSISTENCY_HANDOFF_2026-09-30.md; prior checks retain their dated scope.
