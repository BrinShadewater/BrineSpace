# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: drone animation continuation and bible audit

## Objective and acceptance
Continue accepted-v10 drones into moving NPC animation. Owner additionally asked
to check cyan, pixel density, theme, perspective and the bible. This turn produced
a Construction south-facing review pilot; neither scale nor new poses are owner accepted.

## Accepted decisions and constraints
Approved-v10 remains authoritative and unchanged. Preserve asymmetric tools,
status meanings, underwater roles, palette and separate dock effects. No gameplay
or owner-layout modifications. Do not mistake old installed fleet art for the art lock.

## Current state
`assets/drone-npc-pilot-2026-09-26/` contains source references, two generated pose
sheets, builder, style audit, 53 frames/three clips, manifests and review boards/GIF.
`tools/capture_drone_v10_scale.gd` and paired UID provide the production-room scale
fixture. Isolated logs/fingerprints are in `output/drone-npc-pilot-2026-09-26/`.
69.12 world-unit width is provisional. Exports use .34 world units/library pixel.
v1 cyan was too saturated; v2 is slightly grayer than accepted v10. New poses remain
smoother/more outlined than locked machinery. Full batch paused at this quality gate.

## Verification
Sprite validator zero errors/warnings; alpha/border checks passed. Two canonical
machinery reference hashes verified. Native room/Bill scale capture succeeded.
Owner save recursive metadata fingerprints unchanged; scratch APPDATA used.
Light/dark style boards and pose keys inspected. Continuous motion acceptance,
collision/occlusion and integration unverified. No broad game tests warranted.

## Next action
Refine painted material and cyan before further poses. Then add intermediate arm
keys, real propulsion motion and directional coverage; keep handed tools intact.
User has not selected a different pilot drone or accepted final world size.
