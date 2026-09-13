# Marsh south-idle integration

Updated September 13, 2026.

## Objective and constraints
Complete Marsh cardinal idle identity continuity alongside the whole-body walks. Preserve blond male android identity, anatomical-right implant, gloves, no helmet and existing two-frame timing.

## Current state
Source `character/marsh-motion-polish-v1/sources/idle-south-video-01.mp4` completed (946,909 bytes; 97 frames, 24fps, 1248x1664). Exact prompt and completed provider job retained; no active request. Recipe `idle-south-cycle-recipe.json` selects frames 8/43, fixed scale 147/1533 and position 68/68 on canvas 256x256, pivot 128/224; durations 650/650 ms. Temporal source contact and idle/walk comparison reviewed. `tools/veld_scanner_revision.py` now selects all four Marsh cardinal idles. Rebuilt `character/marsh-v2` retains supplemental east start/stop/short-step states.

## Verification
All logs under `output/crew-replacement-2026-09-12/marsh/`: `south-idle-validation.log` reports 143 body states, 691 references, zero errors/border touches, 211 original frames and original manifest unchanged. `south-idle-selected-final.log` passes native exact-source and state coverage checks. `south-idle-live-after.log` passes 51 samples; `live-idle-transition-south-production-01/state-transition-00.png` reviewed at both idle/walk boundaries. Older baseline retained separately. Ledger has 811 selected clips; only changed south-idle row advanced, yielding four reviewed Marsh cardinal idles. These are bounded agent reviews, not owner acceptance or exported gameplay validation.

## Next action
Continue missing directional starts/stops and short-route motion, then older Marsh action/run/carry continuity. Veld carry/seated and Branforth older kneel/carry remain open. All 20 targeted walk variants have prior bounded native/live review; broader replacement goal is incomplete.
