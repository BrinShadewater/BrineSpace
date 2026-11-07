# Project handoff

Updated: September 8, 2026 · Project: BrineSpace · Task: Observation Room

## Objective and acceptance
Create a dead-end room with a three-wall library installation, side bookshelves
and giant round north porthole. Owner requested squarer corners after V1; V2 is
integrated with square backing/returns. Native card and station composition reviewed.

## Accepted decisions and constraints
Preserve the round window, warm materials, three-sided layout and clear south
entrance. Implementation defaults: fixed north-facing blueprint, 6 Metal,
no ongoing resource cost/output or new crew mechanic. Do not infer approval of
future bonuses or alternate directional art.

## Current state
New assets/view, prompts and source ledger live in
`rooms/underwater/observation-room-v1/`. Database, main placement, grid view/card
registries, floor profile, rollout ledger and raw export manifest include it.
Added `tools/register_observation_room.py`, `tools/review_observation_room.gd`
and `tests/test_observation_room.gd`; Godot scripts have paired UIDs.
Existing unrelated working changes were preserved; nothing committed or pushed.

## Verification
Native art bounds/entry/collision check passes. Gameplay v3 passes paid queued
construction, deck, Save/Continue and 168 movement samples into/out of the room.
Three native window sizes captured; final gameplay log contains zero ERROR lines.
V1/V2 gameplay runs encountered concurrent unrelated edits; v3 supersedes them.
PNG LFS attributes verified. Standalone executable/package not rebuilt.

## Next action
Owner visual review of the squared composition; current room is playable from
the checkout. Rotatable variants or functional observation bonuses need a new
design request. Earlier standalone packages do not contain this room.
