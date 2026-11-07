# Project handoff

Updated: September 21, 2026 · Project: BrineSpace · Task: Observation seating

## Objective and acceptance
Make reading follow the bought sofa and align the sit/read/rise animation, preserving
owner furnishings and the wider animation/room/polish objective.

## Accepted decisions and constraints
No owner layout changes or Higgsfield. Keep existing service preferences: Observation
Room is reached through curiosity, not a new fatigue destination. Preserve legacy
desk/chair behavior for layouts that still use it.

## Current state
`scripts/crew_room_activity.gd` recognizes the mat-116 sofa and its copies, chooses
a nearby clear approach, faces south and registers the left cushion rest position.
`scripts/bill_npc.gd` interpolates the observation visual offset to that rest point
through sit/read/rise; the former eight-unit offset remains for legacy stations.
Added `tests/test_observation_sofa.gd` and UID to the crew group; updated current status.

## Verification
Four room rotations, collision clearance and start/mid/read/end offset checks pass.
Native Bill standing, sitting and reading poses inspected against the actual saved
sofa. A headless gameplay fixture selected Observation through bounded repeated
curiosity choices, then completed 149 clear movement steps and entered reading at
(-144,-64), facing south. The initial fatigue fixture failed because its assumed
service preference was wrong; game rules were not changed to accommodate it.

Evidence: `output/observation-seat-review-2026-09-21/`. This proves one Bill journey
and the reviewed sofa pose; other cast poses and mirrored/modified sofa variants
have not received equivalent native visual review. Legacy behavior has a focused
compatibility check, not a repeated full legacy playthrough.

## Next action
Continue Bill joint refinement and remaining furniture interactions, especially
Cold Store's fixed service anchors. Review other cast seating before calling the
shared observation change visually accepted for every crew member.

## Shared-cast follow-up

Veld and Branforth seated south poses were inspected on the same cushion. Marsh
vanished behind it: his seated depth offsets were zero, unlike the human packs.
Updated only south sit-down/sit-rise/sit-idle/read-seated depth metadata in
character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json. The canonical writer
in tools/rebuild_human_crew_art.py now reproduces the 0-to-40 transition, reversed
for rising, and depth 40 while seated. No PNG, timing, pivot or other metadata edits.
Native Marsh seated and mid-sit views now show him correctly in front of the sofa.
tests/test_marsh_seated_depth.py passes; non-depth manifest fields compare exactly
to the preserved baseline. This is south-facing evidence, not all seated directions
or all-cast route acceptance. Preview files share the evidence directory above.
