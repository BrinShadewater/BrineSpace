# Margot settles beside resting crew

Updated: October 20, 2026 · Project: BrineSpace · Task: natural companion company

## Objective and acceptance

Owner approved Margot settling beside resting crew with her existing animations,
no extra UI and no resource bonuses. Make her company more intentional while
preserving independent behavior, physical movement, safety and personal space.

## Accepted decisions and constraints

At an ordinary personality decision, Margot has a 50% chance to try nearby resting
crew before falling back to her existing independent actions. Eligible crew are
stationary, alive, dry, seated/asleep or taking an idle fatigue rest. No helmet,
expedition, fire, flooded or suspended destination; locked doors prevent approaches.
Search radius is 1.5 room widths, with at most three route attempts per choice.

She walks to a clear floor node 60–145 world units away, outside the room's doorway
margins. Sleeping crew invite her existing nap; seated/simple rest invites her
existing sit. If the crew get up or leave while she approaches, she abandons the
approach. Once settled she may finish naturally. Existing giving-way, petting,
fire evacuation, flooding and animation clocks remain in charge. No needs/resource
changes, forced crew interactions, new artwork, UI, camera movement or reward.

## Current state

- `scripts/companion_npc.gd`: bounded rest-target/route selection and approach
  revalidation. Existing personality save fields retain the queued sit/nap;
  validation now admits those queued actions for Margot only via species checks.
- `tests/test_margot_company.gd` and paired UID: physical approach, personal space,
  doorway margins, save during approach/nap, pause, crew departure, petting, safety,
  unchanged resources/needs and both independent/company choices.
- `tests/test_margot_company_native.gd` and paired UID: native berth/nap review.
- `tests/index.json`: focused subsystem/native lane; `docs/CURRENT_STATUS.md`:
  milestone and remaining human acceptance.

## Verification

Focused headless fixture: 26 checks pass. Native fixture: 27 checks pass. Existing
companion personality, water and fire-save tests pass. The real habitation fixture
routes Margot to a floor spot in 6.2 seconds, within the 10.4-second sleeping stage;
crew sleep is held in this controlled fixture, so this is not natural-run frequency
evidence. Native 1600x900 image reviewed: Margot curls up beside Bill's berth with
clear floor separation and no doorway occupation. Nap duration remains 18 seconds.

Initial test exposed the old queued-action whitelist rejecting Margot's approach;
fixed without adding save fields or admitting other species' sit/nap. Disk Continue
now preserves approach and settled action. Seeded 24-choice test produces both
company and independent actions (9/15), not a measured population distribution.

Evidence: `D:/bs-margot-company-20261020`; screenshot:
`output/margot-company-20261020/resting-together.png`. All Godot tests used scratch
APPDATA. All 2,971 owner files hash-equal; signed ZIP stat unchanged. Source only;
no export or publication.

## Next action

Observe a normal opening with both companions: Josh's restoration assistance and
Margot's occasional company. Judge frequency and emotional payoff in actual play;
this controlled test does not establish human acceptance or all-room visual fit.
