# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: isolate urgent changes from size-only zoom rebuilds

## Objective and acceptance
Continue full PC/Mac performance/release readiness. Reduce measured zoom redraw bursts without changing pixels, timing, gameplay, input or quality. Whole release gates remain open.

## Accepted decisions and constraints
Muted secondary display, isolated profiles, owner fingerprints, shared debug=false runtime; no screenshots/runtime/art copies. No automatic quality changes, global downscaling, owner-data writes, UID regeneration or monolith refactor.

## Current state
Installed measured scheduling change in scripts/grid_canvas.gd `_flush_retained_layers`. An urgent pending door or terrain layer used to promote every due layer in its group, including unrelated size-only layers. While settling, after a group has already queued, pending real changes still repaint immediately but unrelated size-only layers wait with complete scaled commands. Deferred groups contribute to backlog; the queued group index advances only if work was queued. Existing preparing/structural/flood rules remain.

Added maintained regression to tests/test_live_surface_retention.gd (same UID): urgent door/terrain update is immediate, unrelated size-only wall waits, deferred layers drain exactly once, ordinary structural wall update remains immediate. Installed source bytes equal measured candidate. Original pre-change SHA 9913350b3f991d90802ee6e733eabe1f58e289d512f93920b1cca2d4543fd4d4; installed SHA e4bdb79b4413bfdd21f4b0c3c9af51a8c8835cb158e8254d8cbb98d33fe966cf.

## Verification
Existing three-repeat installed large traces: 35 frames >50 ms, 19 with sampled uploads and 16 without; every non-upload slow frame is zoom-selection. Correlation, not driver bus or disjoint decomposition. Focused native layer and cause probes each match 12 full phase states/cameras and 54 UI snapshots. Slow zoom frames rebuild 80 wall slots plus floors/terrain. Dry station rules out flood-overlay hypothesis. Cause trace shows size-only wall dependencies sharing an urgent door group and size-only environment dependencies sharing selection-changed terrain. GPU line batching shortcut rejected before an experiment: Godot 4.7.2 positive-width multiline dispatches separate line commands internally.

Regression RED corrected runtime exit1: door/floor/terrain each draw once, unrelated wall also draws (failure). Initial private class-name collision emitted parse errors; specific stalled process stopped, guards restored; corrected private copy omits global class declaration. This parse failure is not the behavioral RED. GREEN exit0: wall stays zero while required updates draw, all deferred layers drain exactly once. Initial native visual fixture passes. Fresh installed maintained test also passes with zero failures/errors: includes new scheduling regression, exact selection/settled forced-rebuild pixels, reveal zero strongly differing sampled pixels /27232, Fit glide 28 frames/one hold/no simultaneous floor-wall frame.

Three alternating before/after 40-room pairs, six actual debug=false runs /6480 frames. All 36 full phase states/cameras and 162 UI snapshots exact. Workload idle/pan/selection/zoom-selection at 1x/2x/4x, 90 frames each.

| Metric | Before | Installed |
|---|---:|---:|
| Whole mean ms | 23.940 | 23.929 |
| Whole p95 ms | 34.571 | 35.071 |
| Whole p99 ms | 45.674 | 45.406 |
| Whole max ms | 85.412 | 67.867 |
| Whole >50 / >100 | 27 / 0 | 17 / 0 |
| Zoom mean ms | 26.229 | 26.315 |
| Zoom p95 ms | 41.308 | 41.150 |
| Zoom p99 ms | 67.103 | 52.020 |
| Zoom maximum ms | 85.412 | 58.386 |
| Zoom >50 ms | 19 | 10 |
| Texture peak MiB | 3028.686 | 3028.686 |

Whole mean -0.044%, mixed pairs; zoom mean +0.33%, two pairs worse. No sustained FPS gain. Accept as targeted zoom-stutter reduction: zoom p99 -22.5%, >50 count -47.4%; 24/27 preselected logical landing frames better, mean 59.297→48.663 ms (-17.9%). Whole p95 slightly worse. Frame gates remain failed. Renderer/upload risks remain; no target hardware/Mac certification.

All owner guards 2938 unchanged; tests terminal and runtime override restored. New evidence 34.88 MiB plus scratch 24.75 MiB retained; C122.29/D69.11 GiB free. UIDs have no diff. No screenshots or full runtime copies.

Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation/: render-spike-attribution/analysis.json, zoom-layer-spike-attribution/analysis.json, zoom-flush-cause/analysis.json, zoom-group-scheduling-trial/{verify-red.log,verify-green.log}, zoom-group-scheduling-native/native.log, zoom-group-scheduling-workloads/{comparison.json,zoom-comparison.json,identity.json,owner.json}. Corresponding private scripts in output/renderdoc-tools-2026-10-08.

## Next action
Run prepared run-zoom-group-scheduling-other-maps.py and analyzer for three pairs each on reported and current owner-copy stations. Frozen baseline-grid.gd hash exactly matches original workload identity. Keep the real improvements scoped to zoom pacing; reject broad FPS claims. Next address repeated drone image uploads with an actually new measured remedy; do not repeat unchanged larger-cache/indexed/page-cropping trials. All release loading/endurance/bug/UI/GTX1650/M1/Mac signing and certification requirements remain open.

Engine reference: https://github.com/godotengine/godot/blob/4.7.2-stable/servers/rendering/renderer_canvas_cull.cpp (canvas_item_add_multiline positive-width branch).
