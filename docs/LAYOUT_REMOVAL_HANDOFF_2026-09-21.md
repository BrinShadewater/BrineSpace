# Project handoff

Updated: September 21, 2026 · Project: BrineSpace · Task: Layout cache removal guard

## Objective and acceptance
Preserve saved furnishing through repeated setup without discarding the existing
unchanged-room fast path. Continue the wider art, animation and polish objective.

## Accepted decisions and constraints
Explicit saved prop deletions remain authoritative. Do not restore unwanted legacy
furniture or edit owner layouts. No broad renderer refactor or unrelated benchmark.

## Current state
`scripts/room_layout_store.gd` records applied prop count alongside its signature.
The stamped-survivor check alone previously accepted shortened and empty arrays.
Count changes now reapply the layout, restoring its requested library props.
Added `tests/test_layout_cache_removal.gd`/UID to layout-studio and updated status.

## Verification
Before: five failures for partial/empty removal. After: zero failures, including
unique restoration, stable fast path/render serial, and respecting a newly saved
deletion. The existing Isolation Vault guard also passes all 15 repeated/rotated
setups. Evidence: `output/layout-removal-guard-2026-09-21/`.
This verifies cache correctness for those cases, not a measured FPS improvement.

## Next action
Continue remaining Bill gait and artwork work; reconcile local/default furnishing
before the stable-build release refresh.
