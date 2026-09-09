# Crew life animation handoff

Updated: September 8, 2026 · Project: BrineSpace · Task: all eight remaining animation categories

## Objective and acceptance
Owner requested the full proposed set for Bill, Veld and Branforth: sitting/rising, meals, sleep, oxygen distress/recovery, pickup, reading/inspection, carrying turns and additional death directions. Implemented and available for owner visual review.

## Accepted decisions and constraints
Use original character proportions and asymmetric equipment, preserve authored sources and existing helmet fitting. No gameplay economy or oxygen-rate changes. Retain legacy saves. No commit or deployment requested.

## Current state
`character/crew-life-v1/` contains 1,044 frames and 174 manifests. Runtime creates 86 new clips per architect plus helmet variants. `crew_life.gd`, crew loading/playback, NPC stages, room activity anchors, flooding cues and expedition pickup connect them to play. Pickup precedes cargo extraction; recall cancels extraction. Existing east deaths are retained; other facings now persist on death. Seated/bed draw depth and safe approach offsets keep actors visible on furniture.

New review tools: `tests/preview_crew_life.gd`, `tests/test_crew_life_rooms.gd`, pack/review builders. Affected existing room, expedition and flooding tests include new checkpoints and activity phases. Unknown concurrent room/art changes were preserved.

## Verification
Godot native pack review: 0 failures, 86 clips each. Native room review: 72 room/rotation/actor cases, safe furniture approaches, save/restore and interruptions. Existing 36 room activity cases, station expedition/interlock/cargo, flooding, swimming packs, hull repair and construction pass. Native images inspected; local moving gallery and GIF generated from actual runtime-fitted textures. Existing station test reports two resources still in use at process exit after passing.

## Next action
Owner review: [moving gallery](../output/crew-life-review.html), [showcase](../output/crew-life-preview.gif), and native `crew-life-room-*-q*.png` captures. Visual acceptance remains pending. Local browser automation was blocked by URL security policy, so no browser-run success is claimed.
