# Bill paid approach/work/departure review

September 21, 2026. Broad objective remains active.

## Objective and constraints
Extend the paid gait capture to include the approach before an autonomous work
sequence. Preserve normal building costs/failure rules and all source art. No
Higgsfield, sprite/timing change, owner-layout edit or publication.

## Evidence and findings
The current native fixture builds the controlled paid opening, steps normal game
processing at 30 Hz, handles queued dialogue through its normal minimize method,
and follows Bill's room with the camera. A rolling 15-image buffer retains 1.5
seconds of approach at 10 Hz before the first kneel. It then captures the complete
north-facing Life Support action and one second of departure, 86 images total.

Recorded states: 45 walk samples (15 approach plus 30 departure), 31 kneel,
121 repair, 31 stand. Approach samples are 10 Hz; action samples are 30 Hz. Do not
sum their counts as equal-duration samples. The final approach-to-kneel movement
is 2.16748 controller units over the sparse approach interval. Kneel-to-repair,
repair-to-stand and stand-to-walk boundaries have zero controller displacement.
The complete kneel/repair/stand sequence has zero foot-coordinate spread.

The full station work screenshot and a twelve-image native-pixel transition
contact sheet were inspected: actor/work area visible, no missing limbs or obvious
body jump in sampled poses. The GIF crops screenshots only, without scaling or
modifying sprite artwork, at the captured 100 ms interval. Continuous subjective
smoothness and anatomical foot lock are not proven by controller position or the
contact sheet. No speculative timing/source change was made.

Fixture complete=true, exit 0; free_build=false and failures_disabled=false;
no engine/script errors. Evidence: output/bill-work-transition-review-2026-09-21.
Action animation metadata in this inherited fixture is logged before rendering;
use its states/positions and actual captures, not those fields for same-frame
phase assertions. The earlier paid-gait fixture samples phase after rendering.

## Changed artifacts and next action
Only output evidence and current documentation/pipeline guidance changed.
Review the west-facing walk in gameplay and gather owner natural-motion feedback.
Keep full expedition, room refinement and native Apple Silicon acceptance open.
