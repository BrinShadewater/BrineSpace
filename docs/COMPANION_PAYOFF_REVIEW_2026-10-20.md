# Companion rescue payoff review

Updated: October 20, 2026 · Project: BrineSpace · Task: investigate Josh/Margot payoff without more UI

## Objective and acceptance

Identify a small, visible contribution that makes rescue worthwhile. This is a
source review and proposal, not an accepted gameplay change or live playtest.

## Accepted decisions and constraints

No additional UI. Preserve existing art and animation timing, normal recovery
costs, physical access and safety rules. Owner has requested investigation;
the behavior proposals below have not been approved for implementation.

## Current state

Josh already provides +25% hull-repair work rate while his torch is lit beside an
architect actively welding an already-paid hull job. Travel, deployment/retraction,
distance, dry footing and worker state gate the benefit. His target search only
considers jobs within 384 world units. He otherwise watches repairs/crew, turns or
powers down. He does not currently contribute to normal construction or ward
restoration. See `scripts/companion_repair.gd`, `scripts/companion_npc.gd`.

Margot already follows the nearest available crew member's room, then chooses a
clear random destination. Sit/groom/nap/stretch/yawn are random personality actions;
petting has a visible reaction and cooldown. Merely adding crew-following would
duplicate existing behavior. No production/rest bonus was found in these behavior
paths. See `scripts/companions.gd`, `scripts/companion_npc.gd`.

Recommendation: first extend Josh's existing physical torch assistance to paid
derelict restoration. This gives him a constructive opening role, including helping
rescue Margot, without requiring a hull emergency. Keep architect ownership and
normal cost; only actual assisting time gets the existing 25% rate bonus. Do not
promise a fixed total recovery saving: travel, torch phases and powered thaw remain.

For Margot, a separate smaller character proposal is to deliberately settle near
resting crew using existing sit/nap animations and safe floor nodes. This would
make existing company behavior feel relational rather than random. No automatic
resource or fatigue bonus proposed; emotional payoff needs visual/human judgment.

## Verification

Read current companion/repair/ward code and existing companion repair/personality
tests, plus the retained normal-cost Josh/Margot opening report. No game launched,
no new tests run, no player saves touched, no gameplay/art/build edits. Existing
test source describes coverage, not a fresh acceptance result.

## Next action

Agree on the first behavior change. For Josh, verify reachable adjacent work
positions, ward-specific targeting, loss of helper/worker/access, pause and
Save/Continue, unchanged payment and boot duration. Review actual paired welding
visually and compare ordinary paid recovery with/without assistance. Margot's
resting-crew behavior is a separate optional follow-up.
