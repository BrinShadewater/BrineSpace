# Water detail handoff — September 29

## Objective
Complete the six additional audited environment drawing groups authorized by owner.

## Accepted decisions
Matte original hardware; neutral transparent water artwork. Existing clocks,
counts, tint, fog, state and fallback behavior remain. Door plate draw preserves
the caller's transform; waves map to the existing animated path.

## Current state
Eight textures in `assets/environment/water-detail-v1/`, three immutable source
sheets (one superseded), prompts, reproducible bake, manifest, README and verifier.
Consumers: `scripts/environment_art.gd`, `station_hardware.gd`, `station_effects.gd`,
`grid_canvas.gd`. Native fixture: `tests/preview_water_detail.gd` plus paired UID.
The permanent environment loader automatically includes all new bindings.

## Verification
86 runtime loader checks; native source/actual-size effect sheet, rotated plate
draws, pause equality, time changes, turbine Reduced Motion and station capture.
Scratch profile isolation and real-profile fingerprints retained. Source raster
hashes and byte-identical rebake checked. Source review corrected neighbouring
atlas filament tails in bubble/fleck crops. No paid-run or release acceptance claim.
Final evidence: `output/water-detail-20260929-235947/summary.json`. Real-profile
deltas were limited to Godot logs; saved progress files did not change.

## Next action
Owner review during regular play. No commit, push or playable export requested.
Concurrent character/card work remains outside this task.
