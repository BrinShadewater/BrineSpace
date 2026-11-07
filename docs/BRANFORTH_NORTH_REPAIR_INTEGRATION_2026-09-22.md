# Branforth north repair handoff

Updated September 22, 2026. Project: Brine Space.

## Objective and acceptance

Continue the crew animation polish with a detailed, connected Branforth north
repair chain. Preserve character identity, exact idle/action joins and equipment
fit. Native rendering and reproducible pixels are separate from owner acceptance.

## Decisions and constraints

No Higgsfield, publication or room-layout edits. Existing source art is preserved.
Use one anatomical scale per source sheet, never stretch crouched poses to idle
height. The planted left boot is screen-left in this view and is not the pivot.

## Current state

Installed 36 PNGs in `character/chief-engineer-branforth-v2/frames/`: six frames
each for kneel-north, repair-north and stand-north, bare and helmet variants.
Timing, manifests, pivots and clearance remain byte-identical. The previous south
integration is unchanged. Current playable exports predate both integrations.

`tools/prepare_branforth_north_repair_chain.py` builds from preserved sources in
`character/crew-repair-polish-v1/sources/`: repair-north-01, kneel-north-02 and
frozen bare/helmet idle endpoints. It removes disconnected alpha debris, uses
fixed 0.25 scale, registers the planted boot at x111/y224, and reuses the canonical
north helmet head. Stand reverses kneel; idle endpoints and action joins are exact.
`tools/branforth_repair_revision.py` selects these states explicitly during the
canonical crew rebuild. The existing regression test now covers south and north.

Rejected sources remain preserved with exact prompts: kneel-north-01 lacks early
descent and has oversized anatomy. West repair-01 and kneel-01 make Branforth too
broad and young-looking; neither is selected or installed. All generation used
the built-in OpenAI image tool. PNG source paths have Git LFS coverage.

Preview: `character/crew-repair-polish-v1/review/branforth-north-chain-02/chain.gif`.

## Verification

- Python repair-chain regression: 3 tests pass, covering 72 selected south/north
  frames, binary alpha and exact idle/action joins.
- Human crew validator: zero errors or border touches; 669 original source frames
  and 108 source manifests unchanged.
- Native Godot production-player audition: 111 captures with both equipment
  variants, no missing frames or logged errors; inspected descent and work frames.
- Complete crew packs: 19,475 checks, zero failures. Existing raw-image fixture
  warnings remain; they are not packaged-release evidence.
- Frozen north baseline: exactly 36 of 2,203 runtime PNG/JSON files changed;
  2,167 unchanged, zero added. Only selected north PNG paths changed.

Evidence: `output/branforth-north-chain-2026-09-22/` (before/changed JSON, native
captures/log, validation, rebuild-check and pack logs). This is a bounded player
rendering check, not an autonomous station repair or owner acceptance. No new
playable package was exported.

## Next action

Re-author west from the canonical slender mature profile, with a standing-scale
ruler and preserved face; do not build further on the rejected younger/broader
source. Then review Marsh repair readability and missing transition coverage.
