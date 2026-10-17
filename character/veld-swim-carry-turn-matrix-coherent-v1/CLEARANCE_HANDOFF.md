# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: Veld cargo clearance

## Objective and acceptance
Complete the full master-matched Veld animation set, then cross-family polish.
This milestone verifies staged cargo envelopes and furnished turn routes only.

## Accepted decisions and constraints
Preserve selected art, timing, physical ruler and existing clearance coverage.
Candidate profile remains scratch-only; no production selections or code changed.
Every Godot run uses scratch APPDATA and fingerprints the owner's real profile.

## Current state
measure_clearance.py and validate_clearance.py measure 48 states/336 references.
candidate-clearance-profile-v1.json expands 24 old bounds conservatively. Correct
actual gates are swim movement, actions salvage, and life cargo-turn. Furnished
route fixture/check_routes.py exercise actual graph, smoothing, movement and grid
frame selection. record_route_evidence.py binds reports/captures and source hashes.

## Verification
778 envelope/hash/no-shrink checks pass. 24 furnished turns pass 2403 checks:
every phase, paused phase, finite completion, exact cargo endpoint and arrival.
One obstructed swept-turn route passes 50 checks: safe early cancellation then
arrival. Engine errors zero, real profile changes zero. Two corrected native room
captures reviewed: east/west bare and north/south helmet. First captures contained
legacy Bill preview and are archived; fixture clears its cell/expedition. First
narrow probe chose clear geometry and failed; archived then corrected to select
an obstructed swept envelope. Evidence: route-evidence-v1.json.

## Next action
Exercise complete outbound/exterior sample/pickup/return/airlock/unload journeys,
normal flooding/traffic and interruption/disk restore before runtime promotion.
Then continue remaining crew-life/distress/recovery/death and full-set polish.
Full goal active; this is not owner motion acceptance or whole-journey proof.
