# Bug-report and performance pass — October 4, 2026

## Objective and acceptance
Review the owner's saved reports; make measured, focused performance and reliability fixes without changing gameplay rules, selected character art, or owner saves.

## Accepted decisions and constraints
Source changes only. All Godot runs use scratch APPDATA. Native rendering and pixel comparisons establish visual parity; simulation timings do not stand in for rendering. Preserve concurrent work and avoid a main-script refactor.

## Current state
- Indexed all 289 saved reports. Triage concentrated on the newest 65 (September 29–October 4); older archives are retained as historical evidence, not declared fixed.
- Latest manual lag report: `20261004-015752`, 12-room live station. Replayed the exact snapshot with its saved zoom/scroll at 2560×1440, then exercised panning and cycle updates.
- `grid_canvas.gd`: register lazy room instances before adding them to the tree, preventing `_ready`/image-pump reentry from constructing the same room recursively. Addresses the stack-overflow path recorded September 30. Regression fixture deliberately re-enters during `_ready`.
- `title_archive.gd`: remove unchecked second-line indexing from Credits. The normal current build string did not reproduce the old exception; the display now also tolerates a one-line value instead of aborting the rest of the page.
- Upright kelp only rebuilds animated polygons whose complete sway envelope can intersect the visible station area. No change to placements, timing, art or animation. Optional viewport flows through `seabed_background.gd` from the grid; other consumers retain the uncropped default.
- `tools/soak_test.gd`: reset autosave target after restoring an input checkpoint, so the tool cannot overwrite its source snapshot.
- `tests/test_report_regressions.gd` (+UID, registered in performance-diagnostics): loading reentry, complete Credits and native kelp parity.
- `CURRENT_STATUS.md`: collapsed repeated blank lines, 581,569,255 → 2,617,435 bytes. Hash of newline-normalized nonblank content matches. A concurrent status update was detected on the first attempt; cleanup was retried against the newer document, preserving that update.

## Verification
Evidence: `output/performance-bug-pass-2026-10-04/` (report index, copied snapshots, isolated profiles, logs, pixel checks, before/after timings, cleanup digest).

Same-input native replay, 300 measured frames after warm-up; vsync disabled in both runs:

| Metric | Before | After |
| --- | ---: | ---: |
| Mean frame | 21.94 ms | 20.32 ms |
| p95 frame | 30.53 ms | 27.76 ms |
| Mean grid drawing | 6.78 ms | 6.09 ms |
| Mean seabed drawing | 1.91 ms | 1.25 ms |
| Worst frame | 49.46 ms | 56.26 ms |

The repeatable reduction is in seabed work (~34%); the single worst frame did not improve. These are focused development-build measurements, not a universal FPS guarantee. No static floor rebuild occurred during either measured sample. The historic 150–200 ms multi-layer redraw bursts were not reproduced in this replay.

- Native report regressions: **112 checks, zero failures**, including 108 exact pixel comparisons across zooms, screen edges, sway phases, reduced motion and disabled effects.
- Headless simulation budget: **40 cycles / 800 frames PASS**, mean 1.64 ms, worst 21.8 ms.
- Native menu recovery: **PASS**.
- Native loading transition: **PASS**.
- September 30 Margot/Marsh snapshot replay: 60 simulated seconds; Margot gives way, Marsh reaches his workplace by 10 seconds, maximum sampled traffic waits 0.291 / 0.035 seconds. Current passage logic clears this report; no navigation rewrite was needed.
- Owner profile: **2,936 non-log files unchanged** after final validation.
- Native diagnostic reporting: **PASS, zero failures** after fixture correction. Its old assertion directly paused the SceneTree, conflicting with the existing overlay-ownership fix; it now tests main's real gameplay pause and both report/Studio close orders. F9 is intentionally blocked behind the report. The first headless invocation was stopped because this fixture requires rendering; intermediate failed fixture logs are retained separately.
- Older nil drone-dock state error already has a current-source guard in `room_asset_library.gd`. The September 30 screenshot's unidentified old floor graphic is partially obscured by the diagnostics overlay; no asset was deleted on that evidence.

## Startup continuation — October 4

Owner asked to continue. Changes in `scripts/image_prefetch.gd` and `scripts/safe_image.gd`:
- Keep successful PNG decodes in a startup-only LRU cache capped at **16 MiB / 128 images**. Return independent images so a raw-image consumer cannot mutate another caller's pixels. Cold launches benefit too. Release the cache when startup ends.
- Skip obsolete prefixes when the previous manifest order jumps forward; retain at most one worker window behind and one ahead. A regression test jumps eight windows and verifies only the requested slot is submitted.
- Reset per-launch diagnostics; expose worker submissions and peak pending count. `reuse_recent_images` is a diagnostic comparison switch set before `begin()`; ordinary startup enables reuse.
- Expanded `tests/test_image_prefetch.gd` with copy isolation, warm/cold repeats, entry/byte eviction, release and bounded scheduling checks; registered in performance-diagnostics. No character manifests or image assets changed.

Verification: prefetch regression **PASS** (one intentionally missing-image warning), native new-run/Continue loading transition **PASS**, no unexpected errors. Scratch APPDATA and **2,936 owner non-log files unchanged**.

Initial full-source baseline: 15.431 s building/restoring the latest 12-room station; after change: 12.853 s. A subsequent controlled comparison using the same current code, snapshot, viewport, previous-launch manifest and warm filesystem measured **13.885 s cache disabled → 11.695 s cache enabled (15.8% reduction)**. Both requested 32,169 images, submitted 25,676 worker jobs and peaked at 96 pending jobs. Cache served 3,291 repeats; final texture memory was identical (5,249.95 MiB). Startup captures are byte-identical in pixels. These are development-build measurements excluding the narrative typing interval, not release timing or a claim that all loading stalls are gone.

The old floor-graphic snapshot was restored at its original zoom/scroll and cycle 10. Review waited for camera and drone-image jobs to settle; the initial freeze-before-render capture was replaced. The visible little figure near the north doorway matches active Margot at canonical foot `(8220.004, 7465.602)`, walking south. Asked the owner whether this is the reported object; no answer yet, so no intended prop/companion was removed. Final review: `output/startup-pass-2026-10-04/floor-prop-current.png`.

Evidence: `output/startup-pass-2026-10-04/verification.json`, controlled timing logs/captures, expanded prefetch test log, loading-test log and owner fingerprints. The first raw before/after image comparison was also identical, but the controlled pair supplies the clearer timing comparison.

## Next action
Continuation complete in source. Startup still loads a large animation bank and takes roughly 12 seconds in this case; deeper loading changes need the same selected-frame and Continue checks. The floor report needs owner confirmation if they meant a different object from Margot. No executable export, commit or upload was made.
