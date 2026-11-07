# Project handoff

Updated: September27,2026 · Task: view new crew walking in Layout Studio

## Objective and acceptance
Owner requested an interactive engine view of the new crew walking around Studio rooms.

## Accepted decisions and constraints
Use existing Studio preview/pathfinding, copied owner layouts and isolated APPDATA. No generation, save restoration or gameplay changes.

## Current state
`scripts/room_scale_preview.gd` now appends the same explicit bare idle/walk overrides used by gameplay for Bill, Veld and Branforth, including after full-art loading. Existing companions and other activities unchanged.

`tools/preview_crew_layout_studio.gd` opens Research Lab with all three walking; user can switch rooms and rotations normally. Autosave disabled in this launcher; manual edits affect its scratch profile. Interactive GUI launched; process record/log in output/crew-layout-studio-preview. Close the Godot window to stop it.

## Verification
Native verify run exited0, confirmed all three travelled, exact latest north-frame counts (19/36/28), and no furnishing changes. Screenshot reviewed. Copied room_layouts.json and Studio preferences into output/crew-layout-studio-preview/profile before launching. Real-profile fingerprint changed only last_session.json during verification; cause not established, no restoration attempted. Real room_layouts.json unchanged. Do not claim complete live-profile immutability.

## Next action
Owner reviews walking across chosen rooms. Studio actors navigate independently; this preview does not establish live multi-crew avoidance. No credits spent; last confirmed56. Launcher and loader edit retain paired UIDs.
