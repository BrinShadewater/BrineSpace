# Project handoff

Updated: September 8, 2026 · Project: BrineSpace · Task: Studio, lighting and BRINE portrait

## Objective and acceptance
Session closed at owner request after Studio simplification, riser/exterior
lighting changes and iterative BRINE comms portrait refinement. V8 is the selected
session result; no further changes requested at closeout.

## Accepted decisions and constraints
- Studio: WASD camera, direct object editing without coordinates, whole-floor
  tileset choices, visible doors, no saved arrangements, new props at 50%, corner
  resize and visible drag between room and tray. Room Default reflects the room;
  Common offers neutral props. Later sessions may refine the live controls.
- Decorations/lights belong on the riser, not the low north strip. Fixtures remain
  when riser geometry is hidden. Exterior lighting is brighter and points outward.
- BRINE: crew-style matte pixels, brown bob, blue eyes, navy suit, faint composed
  smile. Spacious glass tube fills the background, with pale cropped framing and
  no lower rim/outside room. V8 adds buoyant hair and underwater refraction.
  Small bubbles animate behind her; hair/light cues are painted, not animated.

## Current state
Selected art: character/brine-comms-v8/portrait.png, with prompt, manifest/hash
and review-960.png. Earlier versions retained. Runtime: scripts/crew_comms.gd;
effect/mask: scripts/brine_comms_bubbles.gd. Relevant prior handoffs:
ROOM_STUDIO_SIMPLIFICATION_2026-09-08.md, ROOM_STUDIO_USABILITY_2026-09-08.md,
RISER_LIGHTING_2026-09-08.md. Skill portrait guidance and visual bible updated.
Installed character skill mirrored. Working tree contains other sessions' work;
this closeout does not commit, export or alter those tasks.

## Verification
Latest native playtest_crew_comms.gd passes at 1600x900 and 960x540;
test_brine_comms_bubbles.gd passes the updated floating-hair mask checks.
Logs: output/brine-v8-comms.log and output/brine-v8-bubbles.log.
Full source and small native portrait visually reviewed by agent. Earlier Studio
and lighting check scope is recorded in the linked handoffs, not rerun at closeout.
No packaged build was validated for these final portrait revisions.

## Next action
Resume from CURRENT_STATUS.md and live selected assets. No pending work in this
session; further visual refinements or packaging require the next task's scope.
