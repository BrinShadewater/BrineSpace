# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: riser redesign study

## Objective and acceptance
Redesign risers to match accepted painted props, overhead perspective and underwater station construction. Match the existing room perimeter top edges.

## Accepted decisions and constraints
Owner now requests a slightly higher riser, superseding the initial keep-height choice. Proposed implementation target is 66 world units versus current 60; this numerical choice is provisional. Preserve deck and door geometry and owner layouts.

## Current state
engineering-v1.png and engineering-v2.png are preserved concept masters. V2 uses the previous concept as subject and legacy/default/assets/rooms/reactor/source/overhead.png as perimeter-cap reference. Exact v2 prompt is preserved. No production runtime changes.

Native interactive preview: tools/preview_riser_room.ps1 launches tools/preview_riser_room.gd with a unique scratch APPDATA/LOCALAPPDATA, a copy of owner room layouts, and before/after owner-save fingerprints. Uses the existing reactor room and four accepted clean prop exports copied to props/ with source hashes in prop-provenance.json. Face is registered at 66 units, with 16-unit skirt; the actual reactor draw_wall/draw_cap methods supply top surfaces and ends. Existing door textures supply four preview doors. Bill and the other Studio scale actors use current animation, collision routing and depth sorting.

Controls: Tab compares original/revised; D opens/closes doors; Space pauses walking; S saves a screenshot; dropdown changes crew. Escape closes. The north doorway is a preview fixture; this is not a connected gameplay station or a production port-mask change.

## Verification
Native Godot 4.7.2 preview verification passed: 4 current props, 279 navigation nodes, 160.5 world units walked without a clearance failure, pause holds position. Visually inspected revised-closed.png, revised-open.png and walking.png in output/riser-room-preview; original-closed.png also captured. Revised cap shares the real room's material, corners remain closed, character sorts behind/in front of machinery, and door skins retract. No script errors. Owner save fingerprint unchanged after verification. Exact 66-unit face is now rendered in the fixture; owner acceptance remains pending. Index and HEAD both contained 34,567 files before new preview files. A preview process left open is isolated; its launcher checks the real folder again on exit.

## Next action
Owner reviews the playable study. Production integration and other departments remain future work, including their perimeter material references and normal connected-door behavior. Launcher: pwsh -NoProfile -File tools/preview_riser_room.ps1; add -Verify for automatic captures and movement checks. Use PowerShell 7: Windows PowerShell inherited this session's module path and failed to resolve Get-FileHash before launching. No full game export or rollout has been made.
