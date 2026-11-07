# Bill action sequence review

Updated: September 21, 2026 · Project: BrineSpace

## Objective and acceptance
Review consecutive native frames at kneel, repair, stand and walk transitions.
This checks a south-facing maintenance action, not every direction or owner approval.

## Accepted decisions and constraints
No source art or owner room layouts changed. Existing Storage furnishing used in
an isolated, free-built fixture. Normal expedition and full gait acceptance remain open.

## Current state
External fixture and evidence: `output/bill-action-sequence-2026-09-21/`.
198 native room crops at 30 simulation samples per second, state/phase JSON,
transition-board.png and sequence.gif. The fixture starts recording on kneel;
it does not capture the preceding walk-to-kneel boundary.

## Verification
Native process exited zero, zero fixture failures and no logged engine errors.
Transitions occur at frames 0 kneel, 31 repair, 152 stand, 183 walk. Each new
animation key starts at phase zero. All kneel/repair/stand samples share the same
foot position. Agent inspected frame 31 and the endpoint board; GIF available for
motion review, not claimed as human-reviewed motion.

The stand-to-walk boundary visibly changes torso width and facial treatment.
Source metadata uses standingHeight 148 for both; stand's final opaque bounds are
86x148, versus walk's first 77x147. Thus this is not established as a global height
or pivot defect. Registration is stable, but the authored silhouettes differ.

## Next action
Compare the south stand endpoint against canonical idle/walk source layers and
prepare a targeted candidate preserving foot registration and the kneeling arc.
Review repair-to-stand endpoints too. Do not apply blanket scale changes to mask
body/face inconsistency. Preserve source provenance and test adjacent frames before
integration. East/west limb repairs remain installed and untouched.

## Source candidate follow-up
Traced south kneel/stand to `character/crew-actions-v1/bill/kneel-south` in the
frozen source contract; stand reverses kneel. Idle/walk come from major-bill-v2.
Aligned source comparison shows the action sheet's softer face, broader suit and
green edging. Existing equal standing-height metadata cannot correct those differences.

Built-in image generation produced a six-pose replacement source candidate using
current idle/walk identity and old poses as separate reference roles. No Higgsfield.
Raw source, exact prompt, source comparison and registration JSON are preserved in
`output/bill-action-source-2026-09-21/`. Raw output is 2170x725 RGBA with transparent
background despite the requested magenta; actual alpha was inspected. Six column
components were extracted with binary alpha threshold 128 and one common scale
anchored to a 148-pixel standing height, on 256x256 canvases with pivot (128,224).

Registered candidate review shows cleaner edges and improved facial consistency,
but altered hand/tool motion. It is **uninstalled**. The existing repair loop still
uses the old action style, so replacing kneel/stand alone would preserve an internal
mismatch. Next prepare the matching work-loop pose and review all boundaries;
bounding-box centering is provisional, not proof of anatomical foot registration.

## Matching work-loop and native candidate
A second built-in generated source provides restrained tool-hand poses. Its raw
RGBA source and exact prompt are preserved as repair-source.png and repair-prompt.txt
in the same candidate folder. build_kneel_candidate.py reproduces all six kneel
frames exactly from the recorded source hash/registration. build_repair_candidate.py
registers the work source and replaces only (88,154)-(140,187), retaining the established
face, supporting hand, legs and boots outside that region. Work endpoints exactly
equal the settled kneel pose. Reverse kneel provides stand; production timings remain.

`output/bill-action-candidate-native-2026-09-21/review.gd` injects these three bare
south clips into the fixture only. It captured 198 consecutive native frames,
exited zero, reported zero failures and logged no engine errors. comparison.png
shows existing above/candidate below; sequence.gif preserves the candidate sequence.
Agent endpoint-board review finds more consistent facial/suit treatment and reduced
stand-to-walk discrepancy. This is not owner motion acceptance.

Candidate remains uninstalled. Next gates are anatomical foot contact during
lowering, corresponding helmet fitting, and the preceding walk-to-kneel boundary.
Other directions were not regenerated. Production source contract and live frames
remain unchanged; no broad library rebuild was performed.

## Foot contact and helmet follow-up
Measured the viewer-left boot in the six registered kneel candidates. Pose 1 shifted
its bottom-band alpha centroid from 107.35 to 114.12 source pixels before returning
near 109 in pose 2. build_footlock_candidate.py corrects only pose 1's lower-left
leg, ramping a seven-pixel horizontal correction from y187 to y216. New centroid
107.12; other five frames unchanged. 840 pixels changed in the candidate; the
original source and first registration are preserved. footlock-check.json records
the measurements. This metric supports the targeted correction, not complete gait
acceptance or every anatomical contact point.

build_helmet_candidate.py uses the canonical front overlay through HelmetRebaker
and the existing tilted compositor. It writes six footlock-candidate-helmet and six
repair-candidate-helmet frames; head anchors are recorded in helmet-registration.json.
No new helmet art was generated. Stand reverses the fitted kneel frames.

`output/bill-action-helmet-native-2026-09-21/` contains a native 198-frame equipped
candidate capture, state JSON, log and endpoint board. The fixture forces helmet
equipment to isolate visual fitting; it does not test locker/donning behavior.
Process exited zero with zero failures/no logged errors. Agent inspected frame31
and the endpoint board: helmet follows the lowering/rising head and the planted
foot no longer shows the large pose1 shift. All work remains uninstalled.

Next capture the preceding walk-to-kneel boundary, then integrate the selected
south bare/equipped recipes into the canonical rebuild with scoped output checks.
