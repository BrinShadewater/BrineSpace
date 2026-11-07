# Normal release expedition and Continue dialogue repair

Updated: September 23, 2026. Project: BrineSpace.

## Objective and acceptance

Review normal progression and crew action presentation in the current release,
including disk Continue. This bounded automated run is not human pacing, listening,
all-character motion acceptance or native Mac validation.

## Accepted decisions and constraints

Normal dealt hand, room costs, failures and comms pauses remain enabled. No injected
resources, free building, manual simulation steps, source-art or owner-layout edits.
Use isolated profiles and preserve the existing executable packages. No Higgsfield,
commit, publication or new package export this pass.

## Current state

- Reviewed actual Windows build `brinespace-7a7cf72066849d92`, `debug=false`.
  Automated legal card/grid choices run for 100 wall-clock seconds before saving
  and another 100 after Continue, excluding loading time. The selected strategy
  builds one of each listed opening room; it does not represent unrestricted play.
- The expedition reached cycle8/seven rooms, survived and displayed its conclusion.
  Disk Continue preserved Bill, rooms, resources and cycle3 exactly, then advanced
  to cycle8. No release engine errors; normal costs/failures remained enabled.
- Observed defect: after Continue, Bill repeated his initial wake line. The opening
  stores `opening/crew`, while the later observer uses `awake/bill`. A restored
  observer had no active-crew baseline and treated him as newly awake despite the
  saved message keys. This also affects the other starting architects.
- `scripts/crew_comms.gd` now initializes its active/completed-activity observations
  from the restored crew. Later inactive-to-active transitions still announce new
  crew. No save schema or dialogue text change.
- `tests/test_comms_archive.gd` now covers all four starters with the real opening
  keys and checks a subsequent newly thawed crewmember still speaks.
- **The source repair is not in the existing Windows/Mac packages.** Their earlier
  acceptance and source identity remain intact; include this fix in the next build.

## Verification and visual review

- The added regression reproduced four failures before the fix and zero afterward.
  Existing archive checks, save/Continue regression and native conversation/input
  regression all pass. A separate staged restore of this run's frozen checkpoint
  confirms `opening/crew` remains seen and no wake message is queued.
- Initial 552 close-up samples had an incorrect coordinate mapping and are not
  motion acceptance. Full-screen captures and progression evidence remain usable.
  The follow-up uses the viewport's final transform and the grid canvas transform:
  1920x1080 logical coordinates map to the captured 1600x900 image.
- A disposable copy of the same checkpoint supplied a further 65-second release
  observation: 289 correctly centered crops, including four walk directions and
  north-facing torch draw/weld/stow. The release still reproduces the old wake-line
  bug; source-fixed checkpoint verification is recorded separately.
- Agent inspected the corrected pose sheet and fitted station view. Sampled limbs
  remain visible and connected; Hydroponics' beds and engineering machinery remain
  distinguishable at their respective room scales. This does not establish foot
  locking, temporal smoothness or approval of every room. No art/layout change was
  justified by these samples. West/north walk GIFs retain measured capture intervals;
  they are excerpts with a repeating boundary, not uninterrupted gameplay recordings.
- No new audio listening or mixing claim. Readback captures are not performance
  benchmarks. Other characters, helmet variants and Mac hardware were not exercised.
- Evidence: `output/normal-release-review-2026-09-23/`: `events.json`, `native.log`,
  `checkpoint-frozen.loop`, `comms-before.log`, `comms-after.log`,
  `save-regression.log`, `conversation-regression.log`, `frozen-checkpoint-comms.log`,
  `motion-contact.png`, `walk-west.gif`, `walk-north.gif` and `closeup/`.

## Next action

Use the new gameplay excerpts for owner motion feedback, then investigate specific
reported defects. Include the Continue dialogue fix in the next maintained export;
do not imply the current archives already contain it. Native Apple Silicon launch
testing and owner listening remain open. Preserve the frozen checkpoint; restore
only disposable copies when a review may save or conclude the expedition.
