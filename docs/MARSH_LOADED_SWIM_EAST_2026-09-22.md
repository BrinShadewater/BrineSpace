# Marsh east loaded-swimming repair

Updated: September 22, 2026. Project: BrineSpace. Task: repair cargo presentation.

## Objective and acceptance

Make east-facing underwater cargo pickup and transport visibly carry the case.
Installed and technically verified; normal expedition and owner motion review open.

## Accepted decisions and constraints

No Higgsfield. New authored pickup sheet plus preserved loop candidate. No economy,
cargo-credit, pickup-controller timing or dry-unload changes. Other directions preserved.

## Current state

Audit of all24 old swim-carry frames confirms empty-handed upright art in all four
directions. Pickup endpoints also empty-handed. Dry carrying/unloading has cargo.
Contact evidence: `output/marsh-loaded-swim-audit-2026-09-22/`.

`tools/build_marsh_loaded_swim.py` installs two replacement states under
`character/marsh-v2/supplemental/loaded-swim-east/`, removing their old manifest
entries without deleting original PNGs. Canonical rebuild reapplies the selection.
Six pickup frames use exact salvage frame zero, four new intermediates and exact
loaded-loop frame zero. Six loop slots reuse four poses in0,1,2,3,2,1 order.
Pickup150ms/frame (mapped by existing renderer to0.52s controller); loop180ms/frame.
Pickup now non-looping. Canvas224x208,pivot112,172,standingHeight148; explicit water
metadata. Transparent horizontal padding preserves uncut boots and case.

Source/prompt: `character/marsh-swim-cargo-v1/sources/east-pickup-01.*` plus existing
east loop source. Detached case preserved during extraction; hand-measured cell
edges prevent neighboring boot contamination. Review chain GIF/contact:
`character/marsh-swim-cargo-v1/review/east-chain-01/`.

Catalog, clearance and supplemental contract updated. Original PNGs unchanged.
Complete-pack test counts the union of baseline/replacement states and respects
explicit replacement loop/metadata contracts instead of stale baseline values.

## Verification

- Twelve selected frames reproduce exactly; pickup starts on exact registered
  salvage endpoint and ends on exact loaded-loop frame zero.
- Native fixture:90 samples using0.52s pickup mapping; endpoint and paused-pose
  restore checks pass. Agent inspected contact and loaded native capture. This is
  a player fixture, not proof of a full economy/expedition lifecycle.
- Complete packs:20,631 checks, zero failures; fixture source-loading warnings remain.
- Validator:184 states/926 references, zero errors/border touches;211 original
  source frames and one source manifest unchanged.
- Native battery/route gate:PASS,93 samples with recalculated clearance.
- No release export, commit or publication.

## Next action

Repair west/north/south loaded swimming and underwater pickup, then twelve cargo
swim turns. Check normal expedition pickup/return, recall interruption and water
to dry presentation before owner acceptance and updated releases.
