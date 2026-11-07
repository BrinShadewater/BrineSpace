# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: BRINE start focus and cryopod occupancy

## Objective and acceptance
New Loop and Continue center the camera on BRINE. Frozen occupants represent only characters not already acquired in the current playthrough.

## Accepted decisions and constraints
The selected starter begins awake with an empty pod; this supersedes the former seven-second initial wake. Other architects retain their recruitment thaw. Continue keeps saved zoom and crew state. Older saves during the initial wake complete it once. Previously acquired identities remain absent from occupied pods, including deceased crew.

## Current state
Changed scripts/main.gd and scripts/run_save.gd for exact core-cell camera focus and starter initialization; scripts/architects.gd for idempotent starter wake and nonmutating pod display filtering; scripts/grid_canvas.gd applies filtering to core, derelict and restored cryo views. Updated tests/test_architect_recovery.gd for the awake starter. No asset edits or export.

## Verification
Native output/check_core_start_v2.gd passes for all three starters, expanded station New/Continue focus, saved zoom, one awake starter, only other pods occupied, disk restore, old wake-save migration and nonmutating display. Evidence: output/core-start-v2.log; visually reviewed output/core-start-v1/branforth.png. tests/test_run_save.gd passes including title Continue. Architect recovery assertions pass, with a remaining headless shutdown warning about two resources still in use. An initial native fixture used a blocked basalt cell and was corrected to a valid construction cell before the passing run.

## Next action
Ready for owner review in the running game. Packaged acceptance was not run. Unrelated concurrent checkout changes remain untouched.
