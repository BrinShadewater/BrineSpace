# Marsh carrying half-turns and crew coverage

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Finish Marsh's four carrying half-turns and verify which characters still lack
turn coverage. Integrated and technically checked; ordinary transport review
and owner visual acceptance remain open.

## Accepted decisions and constraints

Reuse authored adjacent poses, without mirroring or new generation. No Higgsfield,
gameplay/room changes, export or publication.

## Current state

`tools/build_marsh_opposite_carry_turns.py` joins east/west through north and
north/south through east; reverse clips reverse the poses. Shared cardinal frame
is exact and stored once with120ms combined duration. Four800ms clips, nine frames
each,184x184, pivot92,172, standingHeight148, explicit dry metadata.
Canonical rebuild, catalog and hash contract include both runtime pair folders
under `character/marsh-v2/supplemental/carry-turn-*/`.
Review GIFs/contact sheets: `character/marsh-carry-turns-v1/review/east-west-01/`
and `north-south-01/`. Earlier PNGs and clearance are unchanged.

## Verification

- Catalog audit: Bill, Veld, Branforth each have12 swim,12 carry,12 swim-carry
  turns in both body and helmet catalogs. These counts establish turn coverage,
  not complete artistic acceptance of every animation.
- Marsh now has12 swim and12 carry turns;12 swim-carry turns remain absent.
  Previous count was16, not14; this pass removes four.
- All76 carry-turn frames reproduce exactly, including original endpoints and
  binary alpha. Shared middle-frame identity is asserted by the builder.
- Two native fixtures,120 rendered samples each: four selected clips and exact
  destination handoffs, zero failures. Agent inspected contact sheets and native
  midpoint capture. Normal transport/interruption visual review remains pending.
- Maintained handoff:60 cases, zero failures, including pause/restore. All twelve
  Marsh carrying turns are now mandatory.
- Complete packs:20,563 checks, zero failures. Existing fixture source-loading
  warnings are not release-export evidence.
- Validator:184 body states/926 references, zero errors/border touches;
  211 original source frames and one original manifest unchanged.
- Evidence: `output/marsh-carry-half-turns-2026-09-22/`, including crew catalog audit.

## Next action

Marsh's twelve swimming-with-cargo turns. Then normal-play animation/cargo review,
fresh stable builds and Apple Silicon testing. No updated export yet.
