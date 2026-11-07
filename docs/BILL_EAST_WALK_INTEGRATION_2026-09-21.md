# Bill alternating east walk integration

Updated September 21, 2026. Project: BrineSpace. Broad goal remains unfinished.

## Objective and accepted decisions
Repair Bill's repeated/disjointed side-walk poses with independently authored,
connected alternating poses. Preserve directional gear, existing timing/stride,
other actions, owner rooms and library marks. No Higgsfield or publication.

## Current state
The canonical rebuild selects tools/build_bill_alternating_east_walk.py.
The shared side-walk review CLI exports both selected directional recipes;
tests/test_bill_walk_surface.py covers both. Exactly 12 east bare/helmet PNGs
changed; 4448 other inventoried runtime art/metadata/import files are unchanged.
Six poses retain the 184x184 canvas, pivot (92,172), standing height 148,
900ms cycle and existing stride. East helmets remain 46x56.

Sources and all three built-in generation prompts are preserved under
character/major-bill-v3/sources/east-walk-alternation-2026-09-21/.
The first sheet repeated the first contact and wrong passing support leg;
separate contact-b and passing-b sources replace those cells. Raw rejected cells
are retained. Source alpha is thresholded before uniform recorded scaling;
head registration, final binary alpha and per-pose canonical helmets reproduce
frozen decoded hashes. East is not a mirror of west. Integration required no
additional generation. Frozen recipe status describes its earlier staging point;
integration.json records current selection.

## Verification
Evidence: output/bill-east-walk-integration-2026-09-21/.
- Complete canonical rebuild passed; exact 12-file change boundary verified.
- Four surface/review parity tests pass, including all 24 selected side-walk
  exports, frozen decoded pixels, binary alpha and helmet/body preservation.
- Full validator: 2214 frames, zero errors/border touches; 780 original frames
  and 113 original manifests unchanged.
- Production consumer: 11773 checks, zero failures.
- Installed native paid station fixture exited zero: 480 captures, 251 unpaused
  east-walk samples, actual getter membership checked each east walking frame.
  No candidate manifest, table, timing or metadata overrides. Costs and failures
  remain enabled. Controlled room setup/manual 30Hz simulation is not a human
  playtest or full expedition acceptance.
- Separate production-player native capture: 27 frames each for bare/helmet,
  zero missing textures; source and game-scale render inspected. Inline GIF is
  a crop of those installed native renders, 27 frames over 900ms.
- Character pipeline reference updated and installed copy synchronized.

## Next action
Review complete gait/contact consistency, including north/south and transitions,
and obtain owner visual feedback. Native checks do not establish anatomical
world-space foot locking or final appearance acceptance. Continue room polish
while preserving owner layouts. Windows/Mac 1fe9515ad1c5f4c5 packages predate
both alternating side-walk integrations; refresh at the next release milestone.
