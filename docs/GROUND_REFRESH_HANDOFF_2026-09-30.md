# Ground refresh handoff — September 30

## Objective
Continue replacing older environment art, prioritizing visible seabed materials.

## Accepted decisions
Neutral matte painted materials; retain gameplay placement, blocker geometry,
world UV scale, tint and fog. Tube worms stay bound to existing legacy scenery.

## Current state
Three immutable masters and three runtime PNGs in `assets/environment/ground-refresh-v1/`,
plus prompts, bake, manifest, README and isolated verifier. Explicit paths added to
`scripts/environment_art.gd`. Selected bindings in `seabed_background.gd` and
`rock_view.gd` retain original fallbacks. Silt tiles retain world bounds with explicit
mirror UVs. New fixture `tests/preview_ground_refresh.gd` has a paired resource UID.
Concurrent character/card changes are outside this task; no commit/push/export.

## Verification
89 runtime loader checks, native old/source/tint comparisons and reflected join
review, selected binding checks, unchanged scenery data, read-only drawing and
paused repeat-frame equality. Actual fogged station capture uses free solar arrays
only in its dedicated art fixture. Source audit and byte-identical rebake recorded.
All Godot runs use scratch profiles and fingerprint the real profile before/after.
Passing evidence: `output/ground-refresh-20260930-000926/summary.json`; all 2,774
real profile files unchanged. Source audit: three identities / six rasters, no
unregistered candidates. All three runtime exports rebuild byte-identically.

## Next action
Owner review in ordinary play; remaining older habitat materials and bought site
scenery can be addressed in later batches. Packaged gameplay remains untested.
