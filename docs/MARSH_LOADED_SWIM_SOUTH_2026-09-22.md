# Marsh south loaded swimming

Updated: September 22, 2026. Project: BrineSpace. Task: continue cargo presentation.

## Objective and acceptance

Complete south-facing pickup/loaded swimming and compare all four directions.
Integrated and technically checked; full expedition and owner motion acceptance
remain open. Twelve swimming-with-cargo turns still need art.

## Accepted decisions and constraints

No Higgsfield. Independent front-facing source, no mirroring. Both hands hold the
case ahead of a foreshortened prone body. Preserve controller timing, cargo credit,
dry unloading, owner layouts and earlier selected art.

## Current state

Raw sources and exact prompts: `character/marsh-swim-cargo-v1/sources/south-*`.
Selected runtime: `character/marsh-v2/supplemental/loaded-swim-south/`.
Preview: `character/marsh-swim-cargo-v1/review/south-chain-01/motion.gif`.

`tools/prepare_marsh_swim_cargo.py` registers the four loop poses at .25 scale.
`tools/build_marsh_loaded_swim.py` registers pickup intermediates at .24 with
measured shoulders. The lifted-case pose was moved upward after a border check
caught a clipped boot. Canvas224x208, pivot112,172, standingHeight148 are unchanged.
Pickup uses exact salvage/loaded endpoints and six150ms slots mapped to existing
0.52s controller time; loop uses six180ms slots, four poses in0,1,2,3,2,1 order.

The canonical rebuild direction list now includes south. Catalog and supplemental
source contract select the replacement keys without duplicates. No existing PNG
or clearance changed during installation. Original source frames are retained.

## Verification

- All48 selected loaded-swim/pickup frames reproduce exactly across four directions.
- Validator:184 states/926 references; no errors or border touches;211 original
  source frames and one source manifest unchanged.
- Native player:90 rendered samples, endpoint equality and serialized paused-pose
  restore, zero failures. Contact sheet and native loaded capture visually inspected.
- Four-direction comparison shows forward case grips, rear body occlusion and
  compact axial poses. This is agent review, not owner motion acceptance.
- Complete packs:20,835 checks, zero failures. Fixture source-loading warnings
  do not establish packaged compatibility.
- Native battery/route gate:PASS,93 route samples.
- Evidence: `output/marsh-south-loaded-swim-2026-09-22/`.
- No full canonical rebuild, export, commit or publication this pass.

## Next action

Author adjacent loaded-swimming turns using these selected endpoints, then compose
the four half-turns. Review normal expedition pickup, recall and water-to-dry joins
before fresh playable builds and Apple Silicon testing.
