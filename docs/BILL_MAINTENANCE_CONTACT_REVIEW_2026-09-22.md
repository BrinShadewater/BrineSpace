# Bill maintenance contact review

Updated September 22, 2026.

## Objective and constraints
Continue natural crew motion and equipment contact without changing owner layouts.
No Higgsfield or source-art changes in this investigation.

## Current state
The paid observation's south repair at 40.246 seconds has foot (7760,8272),
Life Support cell (20,21), local foot (-112,16). A current-engine geometry probe
identifies exactly one matching maintenance target: library/tileset-srb2-35,
Computer desk, blue graph, rect (-174,42,101.2,100.1). The chosen south facing
is consistent with that target; the north tanks are not the target.

The wider native reconstruction shows Bill kneeling on clear floor short of the
desk. Generic equipment_facing accepts a 10-34 world-unit gap outside the entire
prop rectangle; this sample has a 26-unit gap. It does not establish hand/tool
contact or select a prop-specific service side/action. This is an interaction
placement/presentation issue, not evidence of another disconnected-limb defect.

## Verification
Evidence: output/expedition-resume-2026-09-22/work-target.json, work-target.log,
work-context.log and work-room-context.png. Headless geometry probe and native
reconstruction both exit 0 without reported engine errors. Wider screenshot
visually inspected. Reconstruction explicitly places Bill at the recorded foot
and repair state; it is context evidence, not another autonomous run. The earlier
autonomous crop omitted the desk below Bill and cannot alone certify contact.
No production code, art, room layouts or library marks changed.

## Next action
Implement a reviewed maintenance service-point/action contract using live prop
geometry and reachable approaches. Start with this desk and compare contact at
native scale before broadening to other equipment or rotations. Preserve collision
clearance; do not simply shrink safety margins or move owner furniture. Distinguish
standing console operation from low maintenance work. Then exercise ordinary goal
selection, approach, work and departure with the equipment visible throughout.
