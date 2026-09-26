# Bill west work helmet continuity

Updated: 2026-09-21. Broad animation, furnishing and release goal remains open.

## Objective and decision

Resolve a measured equipment-size discontinuity without deforming Bill's connected
body/feet. Idle and walking use the canonical west48x56 helmet, while the recently
rebuilt work actions used34x40. Keep the physical helmet size across the transition.
No image generation, Higgsfield or owner-room changes.

## Installed change

`tools/build_bill_west_actions.py` reads explicit overlay_size48x56 and
overlay_anchor_offset23,25 from the west action helmet registration. Head anchors
and body sources are unchanged. Kneel, repair and reversed stand use the same fit.
The complete rebuild changes18equipped west-action PNGs and the registration only;
all other captured art/metadata hashes remain identical. Bare artwork is unchanged.

Evidence: output/bill-west-helmet-size-2026-09-21. Includes source-size comparison,
staged frame board, before hashes, canonical diff, exact staged comparisons and logs.

## Verification

- Complete2214-frame validator: zero errors, zero border touches;780original frames
  and113original source manifests preserved.
- All18installed frames match the inspected candidate. Action endpoints and stand
  reversal remain pixel-identical; pixels below the helmet region are unchanged.
- tests/test_bill_work_helmet_scale.py verifies standing helmet dimensions and
  opaque shell pixels directly in every installed west kneel/repair frame; passes.
- Native isolated station fixture:198frames per equipment state, zero failures;
 31kneel,121repair,31stand,15walk samples. Equipped working capture inspected.
  Direction/equipment selection is forced and free building is fixture-only;
  this is rendering/state-sequence evidence, not autonomous facing/donning.

## Remaining work

North and south repaired work actions also use34x40 while standing uses48x56;
review their fitted poses before changing them. West action body proportions and
shading still differ from idle/walk and require a separate coherent-source pass.
Owner motion acceptance and full expedition testing remain open. Current release
packages predate this correction and the connected-walk installation.
