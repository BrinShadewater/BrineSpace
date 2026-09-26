# Door variant handoff

Updated: September 21, 2026 · Project: BrineSpace

## Objective and acceptance
Reduce repeated door department work without changing selected art.

## Accepted decisions and constraints
Keep this local and reversible; no persistent cache or geometry changes.

## Current state
`rooms/doors/department_door.gd` now evaluates each required department once per
`pair_variant` call. Current Windows/Mac packages predate this edit.

## Verification
All 2,401 ordered pairs, including empty and unknown rooms, match the previous
expression. Native 100-room probe completed with zero failures and 75 connections.
Same-frame mean whole validation was 3.2064 ms before and 3.091625 ms after;
part lookup was 0.810725 ms before and 0.7089 ms after. These are single-run,
overlapping helper measurements, not proof of an FPS improvement.
Evidence: `output/door-state-breakdown-2026-09-21/` and the two corresponding
`output/game-pass/door-state-*` result directories.

## Next action
Prioritize normal expedition and visual acceptance. Further performance work needs
a concrete bottleneck question; the separate adjacency candidate remains uninstalled.
