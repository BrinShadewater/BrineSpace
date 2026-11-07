# Windows build handoff

Historical build: superseded by the later fixed and optimized releases. Its editor/PCK smoke and short release launch did not certify release-only decoding; see TEEGLY_PR_INTEGRATION_2026-09-09.md and RELIABILITY_PERFORMANCE_2026-09-09.md for subsequent actual-release acceptance. Use RELEASE_WORKFLOW.md for future builds.

Updated: 2026-09-09 - BrineSpace

## Objective and acceptance
Quick verification followed by a playable Windows build from the current local game.

## Accepted decisions and constraints
Build includes current uncommitted project work. Normal title-screen entry point and normal gameplay rules; no validation feature flags. Player saves are not bundled.

## Current state
Release build: builds/BrineSpace-2026-09-09/BrineSpace.exe and BrineSpace.pck (keep together). README, rights notice and SHA256SUMS included. Godot 4.6.1 Windows x64, approximately 5.7 GiB total.
Added Windows Game export preset and ignored local builds directory. Export includes tools/modular_room_geometry.gd because gameplay and Room Layout Studio depend on it.
Fixed startup camera cancellation in scripts/main.gd: changing zoom-slider minimum emitted an unintended user zoom, invalidating the pending core centering. Block slider signals while updating its range. Extended native navigation startup coverage to allow ordinary camera processing.

## Verification
Import and final release export complete successfully. Companion regression passes including Margot. Native navigation/camera checks pass at 1600x900 and 960x540. Final release executable starts normally and exits cleanly after 120 frames, without script/errors.
Final PCK mounted with the matching Godot 4.6.1 engine passes the external smoke fixture: title, gameplay startup, automatically visible station and all architect/companion portraits. Screenshots reviewed. This separately verifies package assets; release templates do not execute the external --script fixture themselves.
Evidence: output/build-export-final.log, output/build-camera-final.log, output/build-companions.log, output/build-release-final-errors.log, output/build-pack-final.log, output/build-gameplay.png, output/build-title.png. Raw-image warnings from the editor-engine fixture are expected; raw PNGs are included by the export plugin.

## Next action
Owner can run the executable. This is a startup and focused regression check, not a long balance/performance acceptance run. No commit or external publication requested.
