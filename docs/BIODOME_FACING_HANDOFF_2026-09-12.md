# Biodome facing handoff

Updated: September 12, 2026. Project: BrineSpace.

## Objective and acceptance
Continue all rooms including missing directional art. South banks use overhead camera and inward access, preserving room identity and functioning equipment.

## Accepted decisions and constraints
Preserve tree canopy, mixed fern habitat, closed aquatic enclosure, nursery and three nutrient dispensers. Keep separate tree/aquatic units at original sizes. No export requested.

## Current state
assets/biodome-directional-v1 contains new south source, prompt and provenance. Added side-biodome-habitat-wall-south registration. full_wall_prop.gd selects the companion for q3; biodome_view.gd retains independent tree/aquatic units and moves them north. Coverage, bible, status, rollout and maintained/installed guidance updated. No q0 card change.

## Verification
Native q3 static/powered views reviewed. output/biodome-directional-2026-09-12/comparison.json shows unchanged prop inventory and q0/q1/q2 RGB; independent machinery sizes explicitly checked. 176 furnished routes and 20 existing side variants pass. state-checks.json isolates OFF/two-time changes to each relocated live unit. These checks do not establish full catalog acceptance. Owner review pending.

## Next action
Continue missing companions and unreviewed directions, including Biodome north/east/west. Full catalog remains active.
