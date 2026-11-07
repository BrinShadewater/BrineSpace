# Bill remaining action review

Updated: September 21, 2026 · Project: BrineSpace

## Objective and acceptance
Identify remaining directional action mismatches after installing the south repair.
Scope is source-boundary comparison and one isolated native direction review.

## Accepted decisions and constraints
No art, owner layouts or gameplay changed. Preserve the installed south and side-walk
repairs. Opposite directions must retain independently authored identity and equipment.

## Current state
`output/bill-other-action-review-2026-09-21/source-boundaries.png` aligns east,
west and north idle/walk/kneel/repair at their declared foot pivots. bounds.json
records endpoint extents. East kneel/repair is visually coherent with its current
idle and shares a -99-pixel relative top. West and north still show the older soft
face/suit surfaces and green edging. In each, kneel ends at relative top -116 but
repair starts at -138: a 22-source-pixel height increase (about 9.7 world units at
65.28/148 scale). Equal standing-height metadata does not correct the pose mismatch.

## Verification
`output/bill-north-action-review-2026-09-21/` contains 198 consecutive native frames,
state JSON, boundary.png and log. Direction is forced north to isolate rendering;
this is not evidence of autonomous facing or a north-side equipment interaction.
Process exited zero. Foot coordinates remain identical through kneel/repair/stand.
Agent boundary-board inspection confirms visible rising at kneel-to-repair and
dropping at repair-to-stand. No owner motion approval is claimed.

## Next action
Repair north and west action sources as coherent kneel/work/stand families using
their current idle/walk identities. Match adjacent endpoints and retain head/torso
construction through the work loop. Do not stretch a whole repair sprite to conceal
the mismatch. East does not need source replacement on this evidence; full-loop
motion acceptance remains separate.

## North source candidate
Two built-in generated source sheets, exact prompts, registration scripts and
source hashes are preserved in `output/bill-north-actions-source-2026-09-21/`.
The kneel sheet uses current north idle/walk as identity reference and old action
poses only as motion reference. Six poses share one scale with a 148-pixel standing
height. The repair sheet contributes only two arm regions; head, backpack, legs and
boots remain from the settled kneel frame. Work endpoints equal the settled pose
exactly, and stand reverses kneel. This removes the 22-pixel endpoint height jump
without vertically stretching a repair sprite.

`output/bill-north-action-candidate-2026-09-21/` contains 198 native candidate frames,
state JSON, log and boundary-comparison.png (old above, candidate below). Isolated
north direction, exit zero/zero failures/no logged errors. Agent boundary inspection
confirms the kneel/work/rise height pop is removed. Raw sources remain outside live
art; no generation used Higgsfield.

Candidate remains uninstalled. contact-check.json finds the viewer-left boot's
bottom-band alpha centroid moves from x110.78 standing to x103.47 kneeling. Correct
and visually review that planted-foot drift, then fit the existing rear helmet
and check the full approach/action sequence before canonical integration. West
source repair remains open. South integration and east source selection are unchanged.
