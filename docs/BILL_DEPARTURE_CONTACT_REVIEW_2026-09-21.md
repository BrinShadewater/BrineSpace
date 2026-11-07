# Bill departure and contact review

Updated: September 21, 2026. Project: Brine Space. Broad goal remains active.

## Objective and acceptance
Review the connected walk in actual paid gameplay, including approach, work and
departure. Connected contours alone do not establish foot planting or body continuity.

## Decisions and constraints
Preserve all owner layouts and source art. No generation or Higgsfield used.
No gait timing, movement speed, cost, failure or release-package changes.

## Current state
scripts/bill_npc.gd now leaves a newly selected service route in idle until move()
selects walking and the actual travel direction together. Previously the first
stationary frame after standing used walk in the old work direction, followed by
a facing change on the next update. This applies to the shared normal goal-selection
path; locker and workshop route entry paths were not changed in this patch.
tests/test_bill_npc.gd guards the queued-route state. Existing unrelated controller
changes in the worktree were preserved. Script UID remains unchanged.

Evidence: output/bill-contact-review-2026-09-21, with separate after/ captures.
The capture scripts load installed production tables without candidate overrides.
summarize.py verifies the recorded state/position sequence and produces the GIFs.
The two openings choose different autonomous work targets; they are NOT matched
trajectories or pixel-parity evidence.

## Verification
- Before: 256 native samples, west approach, north kneel/work/stand, then east
  departure. Sample211 is a stationary north walk frame before east movement.
- After: 258 native samples, south approach/action, idle then east departure.
  No stationary walk sample. Costs and failures enabled in both controlled openings.
- Both action sequences retain an identical actor root through kneel/work/stand.
  This verifies controller position, not anatomical boot contact or full foot lock.
- Agent inspected transition sheets and room context. Crops are contained in the
  viewport. GIFs sample every second30Hz frame with60/70/70ms timing.
- Veld and Branforth behavior tests PASS (exit0). Bill test's new route check and
  movement/activity/pause checks pass, but the full test exits1 for the existing
  Research Lab q2 door0 clearance issue.188room/rotation cases exercised; that
  protected-layout finding is already tracked in CURRENT_STATUS. No test bypass.
- No new full-library or release export run: art unchanged. Current Windows/Mac
  build2601720e53d908cc predates this controller patch.

## Remaining work and next action
South stand-to-idle at after/frames212-213 visibly changes torso/suit bulk even
though the root stays fixed. Review those installed poses at shared pivot/scale,
then repair their source continuity while retaining connected limbs. Native action
capture is evidence, not owner acceptance. Complete anatomical gait/hold review
remains open; the six-pose walk still has within-pose travel. Do not reinstate the
rejected mixed-boot limb rig or treat added frames alone as a repair.
