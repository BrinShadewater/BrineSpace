# Companion artwork reuse during restore

Updated: 2026-09-21 - BrineSpace

## Objective and accepted constraints
Remove redundant work from checkpoint restoration without changing saved behavior,
crew routes, playback, art or owner layouts. Keep fresh actor state and loaded art
separate. No first-load speed or whole-game FPS claim.

## Current state
scripts/companion_npc.gd accepts an optional same-identity art source. It copies
clip/timing/stride/equipment containers and clearance dictionaries while sharing
existing Texture2D resources; all actor and playback objects remain fresh.
scripts/companions.gd passes previous actors during restore, including legacy/null
checkpoints. Missing or mismatched identity still loads its own art normally.
Added tests/test_companion_art_reuse.gd and paired UID to companions subsystem.
No sprite edits, owner layout changes or executable export in this milestone.

## Evidence
External instrumentation under output/restore-breakdown-2026-09-21 found companion
restore dominated finalization:300018us before,582us after. Same100-room synchronous
probe: load CPU373.836ms ->74.522ms; first frame410.391ms ->109.474ms. These timings
are scoped instrumented measurements, not FPS or normal Continue latency.
Normal Continue uses restore_staged; the old profile fixture calls synchronous
restore. Both paths share companion finalization. Initial decode is still required.

812texture reference checks pass, plus independent clocks, behavior, mutable rows,
durations, clearance, and cross-identity fallback. Existing companions test passes
including saved/legacy/partial recovery flows. Native staged restore passes with
5loading frames,78.321ms total,44.739ms longest observed interval; overlay inspected.
Logs have no engine errors/warnings. Updated companion skill reference and mirror.

## Remaining work
Current Windows/Mac e7c1ea935b573fd2 packages predate this optimization. Refresh only
at the next release milestone. Bill east foot-bounds-v2 remains uninstalled and
west repair/whole-loop review remain open; owner treatment question is optional.
Continue room polish and measured optimization without broad refactoring.

## Related selected-clearance loading cleanup
scripts/bill_npc.gd and scripts/crew_life.gd no longer read legacy clearance JSON
immediately before replacing every used human profile with selected-revision data.
The selected swim source retains its dictionary guard. No envelopes, path rules,
character art or companion/Marsh special handling changed.
Temporary selected-clearance probe passes336clear/blocked cases across Bill, Veld,
Branforth, both equipment variants, swimming/treading/work/everyday poses; loaded
dictionaries equal selected sources. Existing near-tangent doorway and smoothing
regression passes. Evidence: output/selected-clearance-2026-09-21/.
This removes redundant reads/dependencies, not a claimed measured FPS improvement.
Legacy sources remain on disk for other consumers and historical tooling.
