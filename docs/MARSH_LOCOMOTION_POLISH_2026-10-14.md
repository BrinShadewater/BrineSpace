# Project handoff

Updated: October 14, 2026 · Project: Brine Space · Task: Marsh locomotion polish

## Objective and acceptance

Owner approved starting the next visual pass with four-direction walking/running,
starts and stops. Review current selection and actual controller playback; correct
visible transitions, retain accepted swimming and avoid speculative redraws.

## Accepted decisions and constraints

Selected walk/run cycles remain. Existing accepted small crown/shading residuals
are retained. No pose regeneration, anatomy patches, mirrors or gait normalization.
Preserve standing height148, pivots, original canvases, timing, strides and root
curves. Whole selected drawings may be shared at adjoining animation boundaries.
Source installation only; no release rebuild, publication or owner acceptance claim.

## Current state

`character/marsh-locomotion-joins-v1` supplies seven states / nine revised holds:
East/West start entry, stop exit and both short-step endpoints share selected idle;
North start's final hold shares selected gait slot1, matching the controller's .23s
handoff. Three complete drawings are copied with transparent registration padding.
All interiors remain original. Two manifests append to Marsh's ordered catalog.
The maintained rebuilder calls `tools/polish_marsh_locomotion_joins.py --install`.
The crew art baseline is refreshed; the new nine-boundary regression and paired
UID are registered in the crew subsystem.

Review inventory:34selected locomotion states /170holds, original hashes frozen in
`character/marsh-locomotion-review-2026-10-14/selected-before.json`.
[Review gallery](../character/marsh-locomotion-review-2026-10-14/review/index.html):
12native route videos with playback/scrubbing controls, nine enlarged boundary
comparisons and34current source replays. Eight walk/run videos pair before/after;
four short-step videos show the installed version. All12native chronology boards
and all34complete source rows reviewed. No new major limb-cycle defect identified
in this bounded review. Replays and sampled native movies are distinct from a
continuously watched real-time play session or universal planted-foot certification.

Native capture tool: `tools/review_marsh_locomotion_2026_10_14.gd` plus paired UID.
Local publisher: `tools/publish_marsh_locomotion_review.py`. Source boundaries are
lossless WebP; native H264 videos are viewing copies of retained PNG evidence.

## Verification

- Boundary regression:9failures before repair ->9checks /zero failures after.
- Corrected baseline:4,970checks /zero; eight96-unit walk/168-unit run routes.
  Installed:5,946checks /zero; same eight routes plus four dedicated short steps.
  All intended gait/step source holds observed, all routes arrive and all sampled
  actor snapshots validate. Each viewport capture observes its rendered marker.
-706paired native samples match keys, slots, physical feet, canvas positions,
  camera regions, player phase, pause and run classification.20paired samples show
  the targeted source changes. No changed physical trajectory or arrival behavior.
- Full baseline scope:only seven Marsh transition states /nine holds change.
  Timing, canvas, pivots, water/depth semantics and every unrelated actor/state,
  including accepted swimming, match. Derived alpha-extent metadata updates for
  all nine changed drawings; it is not claimed unchanged.
- Crew complete packs, walking, Marsh battery (92route samples), and North start
  runtime regressions pass: `output/test-runs/20261014-204458-headless`.
- Narrow rebuild byte-identical; all170original held source hashes preserved.
  All12videos decode at25fps with exact captured frame counts; nine boundary
  comparisons readable. All2,948real non-log owner files match before/after under
  scratch APPDATA. All task Godot processes terminal; owner's existing app left.

Evidence: `output/marsh-locomotion-2026-10-14/`. The initial capture reports36
conservative framing-margin failures on long vertical routes; preserved separately
from corrected `before-native/` and `after-native/`. Moving the review crop upward
fixes those margins without changing art or movement. Two publisher attempts used
overlarge actor-follow subcrops; their failed logs remain. Final published boards
use contained crops and were reviewed. Initial scope audit also correctly rejected
an overbroad metadata-equality assertion; final receipt exempts only derived alpha
extents and verifies all other metadata. No production validator was weakened.

## Next action

Locomotion review and demonstrated transition repairs are complete for this scope;
owner accepted the transition improvements but flagged east-run jumpiness. See
[east-run registration follow-up](MARSH_EAST_RUN_REGISTRATION_2026-10-14.md).
Cargo/work is the next proposed animation family,
then furniture/hazards. Natural jobs/traffic, every stop phase in-world, continuous
2D foot lock, new disk Continue and a refreshed release remain separate scopes.
