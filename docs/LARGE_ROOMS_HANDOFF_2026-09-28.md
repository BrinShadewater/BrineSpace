# Project handoff

Updated: 2026-09-28 · Project: BrineSpace · Task: Four large rooms

## Objective and acceptance
Build four 2×2 rare rooms, one selected per run, with fixed large props and working perimeter doors. Moonbay supports crew-assigned mini-sub survey, recovery, and deep-access missions. Native visual and paid-run gameplay checks are required for acceptance.

## Accepted decisions and constraints
First four runs introduce Farm, Depot, Moonbay, then Tidal Power Plant; later runs select randomly. Colors are green, yellow, cyan, yellow. Large rooms cost more than normal rooms. Moonbay is dry except its sealed launch chamber, requires one ocean-facing side, and has four station doors on the other three walls. Routine sub missions are slow; hazardous sites can damage the sub and force a return. Fixed centerpieces must preserve crew paths.

## Current state
Isolated managed worktree at `C:/Users/Alex/.codex/worktrees/large-rooms/Brine Space`. Written design at `docs/superpowers/specs/2026-09-28-large-rooms-design.md` is owner-approved. Foundation and Moonbay mission implementation plans are written under `docs/superpowers/plans/` and await owner review and execution-method choice. No runtime code or art changed. The main checkout contains extensive unrelated local changes; preserve them.

## Verification
Reviewed current room database, run deck, single-cell placement, and grid renderer assumptions. Git index and HEAD both list 35,317 files in the worktree. Gameplay and visual validation remain pending implementation. Tests must use scratch `APPDATA` and fingerprint the real save folder before and after.

## Next action
Get the owner's review of both implementation plans and execution-method choice. Then build in dependency order: shared footprint/ports, four rooms and draft rules, room effects, Moonbay missions, focused tests and native visual acceptance.
