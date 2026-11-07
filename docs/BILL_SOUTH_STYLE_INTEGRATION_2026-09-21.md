# Bill south standing continuity integration

Updated September 21, 2026. Brine Space. Broad goal remains active.

## Objective and acceptance
Repair the south-facing body/style pop observed at stand-to-idle in the paid
contact review. Preserve identity, connected limbs, existing timings and pivots.
Owner full-motion acceptance and anatomical walk contact remain open.

## Decisions and sources
The installed old action source had a broader torso/larger face than canonical
idle when placed at the same pivot. A new lowering source uses canonical idle
alone. A separate work source contributes hand/tool pixels only. Both used the
built-in image_gen tool, never Higgsfield or CLI/API fallback.
Sources, exact prompt.txt/work-prompt.txt, raw output names and registrations are
under character/major-bill-v3/sources/south-actions-style-2026-09-21/.
Raw lowering: exec-c342acd3-c514-4d10-84cc-d69e0b9df6af.png.
Raw work: exec-67b93d95-3026-42ad-80fc-621179da30a4.png.
Source SHA256s are frozen in candidate-registration.json; integration.json records
current installation separately from historical authoring-stage labels.

## Current implementation
- New tools/build_bill_south_style_actions.py selected by rebuild_bill_art.py.
  The old south helper and sources remain historical, not deleted.
- Common146-pixel actual standing extent, matching canonical idle; manifest
  standingHeight148,256canvas and128/224pivot remain unchanged.
- Whole connected lower poses, small whole-frame contact registration; no mixed
  boot/leg rig. First kneel/final stand use exact canonical idle pixels translated
  by36/52 into the action canvas, bare and helmeted. This removes endpoint redesign.
- Work endpoints match settled kneel; only a recorded hand polygon changes during
  tool work. Standing reverses lowering.48x56helmets retained; first uses exact idle.
- Exactly36south action PNGs changed;4424other runtime files/metadata/sidecars are
  unchanged against the pre-integration snapshot. No owner layouts edited.

## Verification
Evidence: output/bill-south-endpoint-review-2026-09-21/.
- Helper reproduces36candidate images exactly; installed outputs match all36.
- New south endpoint/body tests and existing west continuity tests:4pass.
  Three-direction helmet shell test passes. The first south fit uses canonical
  idle registration rather than an approximate generated head anchor.
- Full validator:2214frames, zero errors/border touches;780originalframes and
  113source manifests unchanged. Actual production consumer:11773checks,0failures.
- Candidate native and independent installed-loader native runs each capture198
  frames per equipment state,0failures. Installed run removes all candidate
  overrides and checks the actual selected dry table. Agent inspected bare/helmet
  room captures and registered sequence sheets. Crops are contained.
- installed/south-actions.gif: every second30Hz frame,60/70/70ms,6.6seconds;
  two equipment variants shown. Isolated room, forced south facing/equipment,
  fixture-only free building/failures disabled. Not autonomous expedition evidence.

## Remaining work and next action
Continue normal paid expedition transitions and anatomical gait review. Matching
standing endpoints does not prove foot planting throughout the six-pose walk or
all-direction stylistic continuity. Check north/east against canonical idle before
requesting more source art. Existing2601720e53d908cc Windows/Mac exports predate this
south art integration and the preceding controller departure fix; no export rerun.
No commit, push, publication or owner-room mutation.
