# Airlock shelf helmet fit

Updated September 22, 2026. Broad goal remains active.

## Objective and constraints
Match the shelf helmet to current crew equipment sizes through the locker handoff.
No generated art, owner-layout changes, controller timing changes or publication.

## Current state
scripts/airlock_service.gd supplies actor-specific visible world dimensions from
current fitted shell bounds: Bill 39x48, Veld 28x28, Branforth 38x40 source pixels,
converted using 65.28/148. The old shelf was 20x25 world units for both men and
12x15 for Veld. Existing empty-shell texture is reused.
The servicing/reserved actor selects the fit; a human remaining at the interaction
point retains it after completion. An unattended spare defaults to Bill's fit.
Marsh is excluded. No serialized state or persistent reservation was introduced.
The room view and grid assignment now use dimensions rather than one scale factor.
The maintained baker refreshed only assets/room-cards-v2/airlock.png; reviewed,
LFS verified, previous card preserved in the evidence folder.

## Verification
Evidence: output/airlock-shelf-fit-2026-09-22/ and adjacent native log.
- Native continuous actions: all three humans in all four quarters, 2217 travel
  samples, completed equip/remove actions, fixed feet and inspector UI pass;
  exit 0 and no engine/script errors. Source animations were unchanged.
- Native three-actor shelf comparison and refreshed card inspected.
- Final lazy geometry lookup guard passes an independent headless probe:
  10 checks cover dimensions measured from actual canonical bare/equipped idle
  pixels, pending reservations, retained return sizes and no lookup in an empty
  airlock. The guard avoids extra work when no human is present; no FPS claim.
- Native run preceded only that lookup guard; the final probe verifies its actor
  selection and dimensions. The card bake ran with final code.

These controlled captures do not establish unforced expedition or packaged/Mac
acceptance. Matching visible fitted dimensions is not a claim of pixel-identical
carried, shelf and worn textures. Owner visual acceptance remains open.

## Next action
Return to ordinary expedition/transition review and remaining furnishing work.
Refresh the test packages at a release milestone; c0508d641e858e5e predates this
shelf adjustment and the two installed locker-action repairs.
