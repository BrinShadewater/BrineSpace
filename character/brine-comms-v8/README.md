# BRINE submerged portrait

Updated: September 8, 2026

## Objective and acceptance
Make BRINE look like she is floating in water inside her tube.

## Accepted decisions and constraints
Preserve her composed smile, crew pixel style, spacious glass tube and small
animated bubbles. No bottom rim or exterior room.

## Current state
Built-in imagegen edit adds buoyant hair locks, cool underwater lighting and
refracted light on the suit. Exact prompt and hashed source retained here.
crew_comms.gd loads v8. brine_comms_bubbles.gd masks the wider floating hair;
test_brine_comms_bubbles.gd checks its occlusion. Previous art retained.

## Verification
Native comms checks pass at both sizes (output/brine-v8-comms.log).
Bubble mask checks pass (output/brine-v8-bubbles.log). Agent reviewed full artwork
and native small portrait, saved as review-960.png. Hair buoyancy is painted;
bubbles remain the animated element.

## Next action
Owner review of the submerged appearance.
