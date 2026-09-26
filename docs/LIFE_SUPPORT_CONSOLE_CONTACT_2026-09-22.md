# Life Support console contact

Updated September 22, 2026.

## Objective and accepted constraints
Repair the observed floor-kneeling interaction without moving room furniture or
altering character art. Owner layouts and library marks remain untouched.

## Current state
Installed in scripts/crew_room_activity.gd and scripts/bill_npc.gd: the unflipped
bought blue-graph desk in Life Support supplies a south-side keyboard service
point, facing north, with a standing interact action. Contact follows the actual
prop rectangle, including saved placement. The reviewed point is 16 units below
the desk's lower edge. Collision checks reject obstructed or out-of-band contact;
unreviewed flipped variants do not inherit this profile.

This station explicitly permits navigation targets up to 160 units from room
center, instead of the generic 144. Other stations retain their limit. Normal
graph routing, spawn clearance and final segment checks still apply, and the
route ends at the exact service point. No collision margin was reduced.
The shared controller serves the human crew; this does not establish visual
acceptance for every character, prop, or arbitrary layout.

## Verification
- Native controlled paid station: normal chooser with maintenance need seeded,
  route around desk, 114 movement steps, exact arrival (7748.6,8414.1), interact
  north. Inspected desk-contact-candidate.png in
  output/expedition-resume-2026-09-22. Standing pose now meets the keyboard side.
  This is a staged chooser/contact check, not another autonomous expedition.
- Maintained test_crew_room_activity.gd passes 48 room/rotation/human cases,
  including all four Life Support rotations for Bill, Veld and Branforth,
  exact approach, correct facing, snapshot validity, Bill q0 disk restore,
  maintenance benefit and power interruption. Final log: activity-tests-final.log.
- Added blocked/flipped desk negative controls. Corrected reported case count to
  increment for every actor/quarter rather than only Bill q0. Optional --room
  filter added. Initial expanded test incorrectly expected a comms event from
  console work; the final console check tests maintenance benefit instead.
- No new source art, generation call, export, owner-layout write or release claim.

## Next action
The full-cycle follow-up below completes the bounded Bill q0 visual review.
Use comparable evidence to address other generic equipment work.
Do not extrapolate this desk's service side to arbitrary assets. Broader natural
motion, room polish and native Mac release acceptance remain open.

## Native process follow-up
desk-cycle.gd in the same evidence folder captures 28 seconds of the normal game
process after seeding the starting maintenance need and choosing the desk through
the normal controller. Economy timer remains stopped; this is a controlled
interaction observation, not another paid-expedition or performance acceptance.
The camera includes the entire desk and approach/departure path.

239 captured samples include all four walk directions and 171 interact-north
samples. Bill completes three maintenance reductions, then chooses curiosity and
walks away. Maximum recorded contact error while interacting is 0.0225 world
units. Source log exits 0 with no reported script/engine errors. Room-scale contact
sheet inspected across approach, repeated work cycles and departure: connected
limbs, stable foot position and equipment-facing work; no new defect established.
desk-cycle.gif preserves recorded sample timing for owner motion review.
This proves only the observed Bill q0 desk sequence, not all props or characters.

## Power and layout follow-up
The new console exposed a shared-controller omission: curiosity visits did not
use Life Support's service-availability guard during selection or ongoing work.
A focused regression reproduced continued interact after power loss (exit 1,
console-power-before.log). Both guards now include Life Support. Repeated full
activity test passes 48 cases (console-power-after.log, exit 0), with an explicit
curiosity interruption/no-service-reward check. A moved-desk geometry check also
proves the station follows its effective rectangle rather than cached coordinates.
Live navigation rebuilds already clear goal, route, stage and state. This does not
yet establish restore behavior when a saved action predates a furniture change;
that is covered by the subsequent contact check below. No art, owner layout, or
package changed.

## Restore contact correction
Reproduced a structurally valid saved console action standing on safe floor 20
units away from the current keyboard contact. Before the fix it resumed interact
at that stale location (console-restore-before.log, exit 1). Restore now checks
current station contact and facing for this console action. A mismatch cancels
the goal/action/timer, retains the active crew and exact safe position, and gives
no needs benefit. Matching contacts retain their saved action and timer. The save
schema is unchanged. This is scoped to active console work; other historical
actions and queued routes are not certified by this check.

The full activity suite passes 48 cases after the fix (console-restore-after.log,
exit 0, no reported script/engine errors). All 12 Life Support human/quarter cases
exercise stale and matching contact restoration. Existing disk round-trip and
power-interruption coverage remains included. The stale-contact fixture models
old furniture placement through its saved foot; it does not edit owner layouts.
