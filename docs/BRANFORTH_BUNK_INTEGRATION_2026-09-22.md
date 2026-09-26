# Branforth bought-bunk integration

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Connected entry, sleeping hold and exit for the reviewed lower bunk, with existing
helmet and preserved body scale. Installed in the working tree; full expedition,
owner visual acceptance and release packages remain open.

## Accepted decisions and constraints
Same reviewed unmirrored bunk dimensions and approach as Veld. Preserve owner
layouts and ordinary movement clearance. No Higgsfield, new generation, commits
or publication in this integration step.

## Current state
- build_branforth_equipment.py fits the existing 34x36 east helmet to authored head
  centers and rotations; recorded head boxes constrain hair cleanup. Bare art is
  unchanged and equipped idle is exact canonical art.
- tools/build_branforth_bunk.py installs the supplement; the canonical human rebuild
  invokes it. Catalog and files live in chief-engineer-branforth-v2/supplemental/bunk-east.
- scripts/branforth_npc.gd owns contact timing, partial reversal and typed snapshot
  validation. crew_room_activity.gd registers the correct actor-specific station;
  run_save.gd uses Branforth's validator.
- tests/test_branforth_bunk.gd is indexed in the native crew lane with generated UID
  bb6dmkyeud4ea. No owner layout edits.

## Verification
Evidence: output/layout-default-audit-2026-09-21/.
- branforth-bunk-controller-final.log: normal chooser/arrival, fourteen bare/equipped
  disk restores, pause, reverse/service interruption, completion and invalid saves;
  zero failures. Each rendered contact sample also equals its Branforth source PNG.
- veld-bunk-after-branforth.log: existing Veld native controller checks pass.
- sleep-interruption-after-branforth.log: 507 checks, zero failures.
- branforth-bunk-rebuild.json: all 18 installed catalog/supplement/clearance files
  unchanged by rebuild/finalization, including movement clearance.
- 47 native equipped study captures reviewed; exact first/last pixels. Equipment
  validation confirms deterministic rebuild, binary alpha, clear borders, exact
  idle and unchanged bare frames. Native restored resting capture also inspected.
This controlled fixture evidence does not establish a full unbiased expedition.

## Next action
Complete Bill/Marsh bought-bunk contact profiles, review multi-crew autonomous use
and continue room polish/performance work. Refresh and test release packages only
with their own evidence; Apple Silicon runtime acceptance remains pending.
