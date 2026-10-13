# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: zoom redraw stutters

## Objective and acceptance

Reduce verified large-station zoom drawing bursts without changing gameplay or
selected visual quality. Matched workloads and native pixels/zoom behavior support
the installed narrow change; full PC/Mac release certification remains open.

## Accepted decisions and constraints

Muted secondary display, isolated profiles, owner fingerprints, input disabled.
Reuse debug=false physical runtime and small overlays; no screenshots, art copies
or automatic quality reduction. Maintain independent selection-sensitive terrain,
derelict and UI layers, structural invalidation, and existing settling schedule.

## Current state

`scripts/grid_canvas.gd` `_surface_state` now preserves cached selection during
preparation/reuse/settling as well as steady rendering. It never changes floor/wall
pixels. Previously selection made those keys appear structurally changed, so the
flush deliberately bypassed its staged size-only schedule and repainted all groups.
`tests/test_live_surface_retention.gd` replaces the obsolete selection-forces-rebuild
assertion with static key independence during settling; other checks remain.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`zoom-key-attribution`, `zoom-selection-retention-trial`, `zoom-selection-native`.
Scoped runners in `output/renderdoc-tools-2026-10-08/`.

## Verification

One 1080-frame private key diagnostic matches the preceding installed control's
12 full phase states/cameras and 54 UI snapshots. Of 270 zoom frames, all 16 >50 ms
frames change selection: ten also change size. No flood surfaces; all 40 rooms
visible. At 2x frames 17/78, selection changes force pending groups to flush together.
Instrumented frame times are attribution, not independent performance acceptance.

Three alternating large-map native debug=false pairs / 6480 measured frames:
idle/pan/selection/zoom-selection at 1x/2x/4x, 90 frames per phase. Both lanes use
the same deterministic survey/notification fixture clocks. All 36 full paired phase
states/cameras and 162 UI snapshots exact.

| Metric | Installed before | Candidate now installed |
|---|---:|---:|
| Mean frame ms | 24.942 | 24.501 |
| Zoom-selection mean ms | 28.570 | 26.755 |
| p95 ms | 37.207 | 35.385 |
| p99 ms | 63.023 | 49.088 |
| Max ms | 99.743 | 94.708 |
| Frames >50 / >100 ms | 62 / 0 | 29 / 0 |
| Texture peak MiB | 3028.686 | 3028.686 |

Whole-run mean -1.77% with mixed pair means; zoom-selection -6.35%. Zoom slow
frames 52→20. Remaining candidate >50 ms frames: 20 zoom-selection, 7 selection,
2 idle; 14 with sampled uploads and 15 without. No broad 60 FPS acceptance.

Native live-surface adapter PASS, zero failures/errors: settled selection pixels
and settled zoom pixels match forced rebuild, live hatch/fire counters remain
cached, chamber water/rotation invalidate, newly revealed room crop has zero
strongly differing sampled pixels out of 27,232, Fit glide passes. Comparisons stay
in memory; no PNGs. Private adapter uses maintained test with the new selection
assertion, unchanged coverage otherwise. Not exhaustive motion/animation certification.
Installed source equals measured candidate excluding explanatory comments; UIDs
unchanged. Three owner guards each 2938 unchanged. Jobs terminal/override restored.

Evidence 26.93 MiB plus 20.95 MiB scratch profiles. C 122.96 / D 69.62 GiB free.
Previous disposable-profile removal was blocked by tool policy; no bypass attempted.

## Next action

Verify installed fix on reported/current real maps. Attribute remaining room-setup,
wall-slot and terrain rebuilding at fixed workload frames, and texture-creation
overlap. Separate non-rebuild companion passage spike remains open. Loading,
endurance, broad bug/visual coverage, target GPUs and PC/Mac certification remain
unfinished; indexed lossless provider remains private.
