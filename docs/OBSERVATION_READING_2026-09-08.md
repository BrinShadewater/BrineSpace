# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: furnished observation room and crew visits

## Objective and acceptance
Owner authorized rear-facing chair, lamp/open book, live furniture installation and crew reading/window visits after the completed-room preview.

## Accepted decisions and constraints
Retain the darker squared library, north porthole, south entrance and six-Metal construction. Activities use existing curiosity needs; no new resource bonus. This supersedes the earlier observation handoff's no-crew-mechanic scope.

## Current state
`assets/observation-office-v1/` contains retained sources, alpha furniture, registrations, prompts and completed-room.png. The live observation view now has five collision props and a tabletop reading set. `crew_room_activity.gd`, `bill_npc.gd` and `grid_canvas.gd` support reading and window visits for all three crew. Visits alternate; occupied stations are skipped. Seated presentation lowers existing north idle art behind the chair, with timed sit/read/rise transitions. No new full-body seated animation sheet. Card, component hashes and floor notes updated. Unrelated working changes preserved; no commit or push.

## Verification
Godot 4.6.1: observation gameplay passes paid construction, Save/Continue, 242 continuous route samples, all three crew's reading/watch approaches, sit/read/rise, snapshot restore, frozen simulation time and suspension interruption; three viewport sizes captured. Native card bounds/collision and completed-room window route pass. Existing crew activity regression passes 36 room/rotation/actor combinations. Final logs: output/observation-reading-test.log, observation-card-furnished.log, observation-furnished.log, observation-crew-regression.log; no ERROR lines. Focused native seated screenshot visually reviewed. Unrelated wreck image-loading warnings remain in gameplay logs.

## Next action
Requested source work is complete. Owner can review the new composition in-game. Standalone packages predate these additions and were not rebuilt.
