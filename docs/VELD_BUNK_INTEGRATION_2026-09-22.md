# Veld bought-bunk integration

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Deliver connected entry, rest and exit for the bought lower bunk, preserving
character scale and owner layouts. Veld is installed; broader cast and release
acceptance remain unfinished.

## Accepted decisions and constraints
Use the reviewed unmirrored tileset-mb2-14 bunk at 72.46131 x 73.99651 world units.
Other sizes, flipped placement and blocked approaches are not silently accepted.
No owner layout edits, Higgsfield, commits or publication.

## Current state
- tools/build_veld_bunk.py installs reproducible bare/equipped supplements in
  character/dr-veld-v2/supplemental/bunk-east; rebuild_human_crew_art.py invokes it.
- scripts/veld_npc.gd owns the 1.84s contact profile, sleeping hold, partial reversal
  and typed saved-state validation. run_save.gd uses that validator; bill_npc.gd
  permits a typed transition limit without changing normal human durations.
- crew_room_activity.gd registers only compatible Veld bunk stations. crew_life.gd
  suppresses generic head correction while the explicit contact profile is active.
- tests/test_veld_bunk.gd and its UID are indexed in the native crew lane.

## Verification
Evidence: output/layout-default-audit-2026-09-21/.
- veld-bunk-controller-final.log: normal chooser and exact arrival; fourteen
  bare/equipped disk restores; pause, partial reversal, service-loss interruption,
  completion, invalid saved data and unsuitable station checks; zero failures.
- sleep-interruption-after-veld.log: 507 checks, zero failures.
- marsh-berth-after-veld.log: arrival, five restores, pause, interruption, completion,
  low battery and invalid saves; zero failures.
- veld-bunk-rebuild.json: all 18 catalog/supplement/clearance files identical after
  local rebuild and finalization; movement clearance unchanged.
Native output/crew-activity/veld-bunk captures show the hanging leg in front of the
rail and the sleeping pose inside the lower bunk. This fixture removes the old
blue bunk locally; it does not mutate saved furnishing. Earlier staged motion
and metadata evidence is preserved in the source study README.

## Next action
Extend continuous bought-bunk contact to the remaining cast, beginning with
Branforth's staged compact endpoint. Verify broader autonomous travel and current
Windows/Mac packages separately. Owner visual acceptance remains open.
