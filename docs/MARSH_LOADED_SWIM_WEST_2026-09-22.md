# Marsh west loaded-swimming repair

Updated: September 22, 2026. Project: BrineSpace. Task: continue cargo presentation.

## Objective and acceptance

Repair west underwater pickup and cargo swimming with connected case/hand contact
and exact endpoint joins. Integrated; normal expedition and owner motion review open.

## Accepted decisions and constraints

No Higgsfield. Independently authored west sheets, no mirroring. Cargo credit,
controller timing, dry unloading and east repair preserved. No release export.

## Current state

Frozen source/prompts: `character/marsh-swim-cargo-v1/sources/west-loop-01.*` and
`west-pickup-01.*`. Direction-aware preparation and installation use explicit
west shoulder anchors; loop scale .32, pickup .30. Detached case in the reach
pose survives extraction. First reach registration moved right12px after detecting
case clipping at the original position. No scale reduction to hide the clipping.

Runtime replacement: `character/marsh-v2/supplemental/loaded-swim-west/`.
Two states, twelve frames,224x208,pivot112,172,standingHeight148. Six150ms pickup
slots map to the unchanged0.52s controller; six180ms loop slots use four poses in
0,1,2,3,2,1 order. Pickup starts on exact salvage frame zero and ends on exact
loaded-loop frame zero. Canonical rebuild now includes east and west.
Catalog, source contract and clearance updated; earlier PNGs, including selected
east repair, remain unchanged. Old west files retained, removed from active manifest.

Review GIF/contact: `character/marsh-swim-cargo-v1/review/west-chain-01/`.

## Verification

- All24 selected east/west frames reproduce exactly, with both endpoint joins.
- Validator:184 body states/926 references, zero errors/border touches;211 original
  source frames and one original manifest unchanged.
- Native player:90 rendered samples,0.52s pickup mapping, exact endpoint and paused
  pose restore, zero failures. Agent inspected contact and native loaded capture.
- Complete packs:20,699 checks, zero failures. Existing fixture source-loading
  warnings do not establish release compatibility.
- Native battery/route check:PASS,93 route samples with the updated clearance.
- Evidence: `output/marsh-west-loaded-swim-2026-09-22/`.

## Next action

Repair north/south underwater pickup and loaded swimming, then twelve swimming
with cargo turns. Normal expedition/recall and water-to-dry visual checks remain;
fresh releases and Apple Silicon validation are still pending.
