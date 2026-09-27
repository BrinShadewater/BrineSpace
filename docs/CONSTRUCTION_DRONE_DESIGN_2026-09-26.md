# Exterior construction drone: design and future NPC contract

Updated: 2026-09-26 · BrineSpace · Concept redesign

## Objective and accepted direction
The owner requested a construction drone that leaves the underwater base to build
and repair its exterior, designed with a future moving NPC in mind.

## Current state
The revised palette uses a dark-gray pressure hull, charcoal joints, dull steel,
muted cyan highlights and a recessed cyan camera, two side ducted marine thrusters and rear maneuvering
pods. Two articulated arms carry a gripper (image-left in the front reference)
and repair/welding tool (image-right). It has no walking legs.

The owner subsequently removed all yellow accents. The current reference and
bay use the shared Drone/AI cyan-and-metal palette; ochre originals are history.

Updated master and 295 x 287 native export:
`C:/Users/Alex/Desktop/BrineSpace Clean Prop Exports/masters/sp-construction_drone_bay-1.png`
and the matching file under `game-size`.
Standalone transparent identity reference:
`C:/Users/Alex/Desktop/BrineSpace Clean Prop Exports/npc-references/construction-drone-v1.png`.
Original bay exports, exact prompts, raw generation paths and save script are
under `provenance/construction-drone-redesign-2026-09-26` in that export folder.
Generated using the built-in image tool. Baseline reference hashes are preserved
by pointing the original catalog entry at its backed-up PNGs.

## Future NPC requirements
- Separate the mobile drone from the stationary dock. Create a matching empty
  dock for departure; the present occupied bay is a static concept export.
- Use the central hull as a stable registration anchor. Thrusters and articulated
  arms move independently. Establish actual scale and pivot against the runtime
  consumer before producing an animation pack.
- Author directional views consistently; do not mirror opposite directions and
  accidentally swap the gripper and welding tool.
- Prove hover, travel and hull-repair motion first. Later coverage should include
  turning, construction/material handling, docking and undocking as behavior needs.
- Keep travel tools tucked and extend them for work. Separate sparks, bubbles and
  tool effects from the base sprite. Preserve the silhouette at gameplay scale.
- Keep docked and free-swimming identity identical. Validate exterior depth,
  occlusion, tool contact and navigation during eventual integration.

## Verification and next action
Agent visually reviewed both masters and the bay at native size. Alpha checks
passed for all deliverables; native canvas remains 295 x 287. Owner visual review
is pending. This is concept work: no animation frames, layered rig, empty dock or
NPC runtime integration are claimed. No gameplay code or owner layouts changed.
