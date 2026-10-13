# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: deferred camera scene lifetime

## Objective and accepted constraints
Cancel queued camera work after scene exit or queued deletion. Preserve normal
centering, user camera overrides and visual quality. Tests use verified scratch
profiles; no renderer admission, zoom math, frame-cap or engine change.

## Current state
`scripts/main.gd`: guards before/after next-frame waits in `_center_grid_on_station`,
`_center_grid_on_core` and `_restore_grid_view_center_deferred`; existing revision
checks remain. Permanent `tests/test_camera_scene_lifetime.gd` and paired UID test
actual Main methods through a lightweight subclass that skips startup/artwork.
Registered in render-perf and save groups. Unrelated dirty Main/index changes remain.

## Verification
The reduced recovery/fast-title control exposed queued station-centering work
running after scene exit: null `get_tree()` and invalid `process_frame` access.
This is a real source lifetime error, not a reason to loosen save validation.

Regression before: exit 1, five checks/two failures, ten error lines. After:
exit zero, five checks/zero failures/errors. Attached callbacks still apply;
camera revision changes cancel obsolete work; detached entry, resumed/queued
callbacks and queued deletion safely stop. All 2,936 owner fingerprints unchanged.

Recovered/no-gameplay native control with only the three guarded methods updated:
zero failures/errors and no anonymous warning. Full Studio, simulation and two
save/title/Continue cycles with only those methods updated: zero failures/errors,
clean exit, anonymous warning absent. Earlier evidence remains preserved.
Startup-only context also exits cleanly. The original recovered-stage warning
included camera errors and is not a clean constructor comparison.

Evidence: `output/compressed-crew-2026-10-06/camera-regression/`,
`bounds-cache/context-stage-recovered-safe/`, `bounds-cache/full-safe-camera/`.

## Next action
Repeat guarded combined ten-transition Studio coverage before closing the warning
completely. The camera error is reproduced/fixed in current source; the warning is
eliminated in the shorter native lanes. Continue loading/frame/memory work afterward.
Compressed backend remains experimental. Long soak, simultaneous spills, original
bug closure and actual Windows/Mac release gates remain. No FPS gain claimed.

Ten-cycle follow-up: 826 checks/zero behavioral or engine errors, old resources
release, title texture 182.795→186.555 MiB and static 222.645→229.936 MiB remain
within 5%. **The anonymous exit warning returned once.** Short clean controls did
not prove a durable warning fix; do not close it or blame it solely on the camera
callback error. The source camera fix remains verified independently. Evidence:
`bounds-cache/full-safe-camera/ten-cycle/`. Owner fingerprints unchanged.
