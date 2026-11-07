# Marsh loaded-swimming turn matrix

Updated: September 22, 2026. Project: BrineSpace. Task: complete cargo-swimming turns.

## Objective and acceptance

All twelve directed loaded-swimming turns are installed and technically checked.
This completes Marsh's three turn families: twelve swimming, twelve dry carrying,
twelve swimming with cargo. Full expedition and owner motion acceptance remain open.

## Accepted decisions and constraints

No Higgsfield, mirroring, gameplay/controller changes or existing sprite edits.
Cargo stays in both hands ahead of the swimmer, with rear-view body occlusion.
Use the selected four loaded-loop endpoints, not the old empty-handed originals.

## Current state

- `character/marsh-swim-carry-turns-v1/`: four independent source sheets, two angle
  correction sheets, exact prompts, frozen loaded endpoints and review media.
  East/north and east/south use source01 first/middle and source02 third poses;
  unselected poses are retained. Explicit registration accommodates actual source
  dimensions2170x725 and2172x724. North pairs use .24 scale; south pairs .22.
- `tools/build_marsh_swim_carry_turns.py`: four adjacent pairs, five frames per
  directed clip,400ms duration. Return clips reverse the same registered poses.
- `tools/build_marsh_opposite_swim_carry_turns.py`: two opposite pairs, nine frames
  per directed clip,800ms duration. East/west passes north; north/south passes east.
  Shared cardinal frame is stored once with combined120ms timing.
- Runtime: six `character/marsh-v2/supplemental/swim-carry-turn-*` folders,
  twelve clips/76 frame references,224x208,pivot112,172,standingHeight148.
  All poses are water transitions. Catalog, supplemental source contract and
  clearance updated; existing PNG hashes unchanged.
- Canonical `tools/rebuild_marsh_art.py` reapplies adjacent and opposite loaded
  turns after the loaded base states. No generation service is needed to rebuild.
- `tests/test_marsh_swim_carry_turns.py` checks reproduction, exact current joins,
  reversal, binary alpha and borders. `tests/test_carry_turn_handoff.gd` now requires
  all Marsh turns in all three families instead of skipping missing loaded turns.

## Verification

- All76 new frames reproduce exactly. No alpha/border defects.
- Validator:196 body states/1002 frame references, no errors;211 original source
  frames and one source manifest unchanged. No Marsh helmet pack is intended.
- Native turn handoff:72 actor/body/equipment cases, zero failures. Checks exact
  endpoint pose, destination restart, subsequent playback clock and serialized
  pause/restore. Other humans retain the fixture's east/west coverage; Marsh is
  checked in all twelve directions for all three families.
- Native rendering: twelve directions,72 rendered samples each, zero missing
  textures. Agent inspected all four contact sheets, half-turn contact and native
  intermediate captures. Preview preserves captured timing to GIF precision.
- Complete packs:21,263 checks, zero failures. Existing fixture source-image
  warnings are not release compatibility evidence.
- Native battery/route gate:PASS,93 route samples with updated clearance.
- Evidence: `output/marsh-swim-carry-turns-2026-09-22/`; inline preview is
  `corner-turns-native.gif`. Review sheets deliberately hold endpoints longer.
- No full canonical rebuild, export, commit or publication this pass.

## Next action

Review a full normal expedition: underwater pickup, loaded return turns, recall,
water-to-dry handoff and unloading. Check room/prop occlusion at gameplay scale.
Address observed defects before fresh Windows/Mac builds and Apple Silicon testing.
