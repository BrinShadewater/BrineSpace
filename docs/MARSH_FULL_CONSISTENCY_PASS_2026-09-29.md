# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: complete Marsh consistency pass 3

## Objective and acceptance

Owner requested all Marsh animations checked for loops, perspective, size and smooth motion. Complete current selection reviewed: 204 states / 1,058 frame slots, including accepted crew-chat v2. New diagnostic corrections are installed for owner visual review; do not call mechanical tests owner approval.

## Accepted decisions and constraints

Preserve approved android identity, right-temple hardware, white-fluid injury, dry ordinary shutdown and crew interaction. Common anatomical calibration remains 148 source pixels per 65.28 world units. Foreshortening and crouching/seated/prone height changes are intentional. Existing action/loop timings and gameplay rules remain. No interpolation, pose-height normalization or global palette simplification.

## Current state

- `character/marsh-quality-pass-v3/`: immutable pre-pass contract, 60 complete pose boards, 204 authored-timing GIFs, per-state measurements, current viewer, four timed before/after diagnostic chains and frozen installation/scope records.
- Corrected 24 states / 120 slots: standing interact, repair, inspect, salvage and paired diagnostic entry/exit. Existing arm/tool art is retained on exact approved idle anatomy outside complete-arm masks; the broader head/torso/legs no longer switch in and out. Matching entry/repair/exit endpoints stay exact. New exports override sibling manifests; 180 other states, all timings and all calibration metadata remain unchanged.
- New preparation/publishing tools, source/provenance/join tests, catalogue selection, canonical rebaker override and colour guards. Existing audit tool now accepts a versioned output directory and fits all artwork into contact-board cells, including below-pivot swimming/welding art. Playback test decodes PNG bytes explicitly, removing four development-only image-load warnings.
- Current consolidated review includes fresh 27 native phase previews. No generation, NPC behavior change, commit or executable export in this pass.

## Verification

- 22,504 actual-player continuous 60Hz playback, gait transition, pause/Continue and registered tread checks: zero failures, no warnings.
- Fresh native selected-player review: 204 states / 1,058 source/elapsed checks / 432 captures / zero failures.
- Three anatomy/provenance/diagnostic-join/calibration/margin tests pass. Colour lock: 8,811 PNG paths, 1,031 previously approved corrections, zero errors. Six changed Python files compile; viewer JavaScript syntax and links pass. New PNG/GIF paths use LFS attributes.
- Complete directional matrices and seven native phase summary boards inspected. Loop seam ratios have no large outliers (largest ~1.36 times median ordinary pose change); no artwork touches canvas edges. Short authored run/swimming pose cadence remains visible at close zoom. Native snapshots and metrics do not certify subjective perfection; current timed viewer is the motion-review artifact. Browser controls were not exercised.
- Godot runs used scratch APPDATA. Real-profile comparison: 2,728 unchanged, six changed (`large_revision.meta`, backup, `last_session.json`, `room_layouts.json`, recovery and Studio config), two added (bug-report zip and prop probe recovery), none removed. The shared session was active; origin of these external deltas is not established here. Preserve them; no restoration attempted. See `output/marsh-animation-audit/profile-quality-v3-comparison.json`.

## Next action

Owner visual review at `character/marsh-quality-pass-v3/index.html`, especially the diagnostic before/after chains. Accepted crew-chat v2 remains selected. No further mechanical failure is open in this scope.


## Diagnostic correction supersedes pass 3

Owner rejected the diagnostic animation: pass 3 masks clipped raised gloves and the scanner. Current selection and review are revision 4; see [diagnostic repair handoff](MARSH_DIAGNOSTIC_REPAIR_2026-09-29.md). Earlier successful mechanical checks did not cover scanner retention.
