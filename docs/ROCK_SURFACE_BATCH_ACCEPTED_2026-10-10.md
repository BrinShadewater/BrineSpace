# Rock surface batching: real-station verification

Updated: October 10, 2026 · Project: BrineSpace · PC/Mac release performance work

## Objective and acceptance

Reduce measured rendering overhead without changing selected art, layering,
animation or gameplay. This accepts one source optimization; the full release
performance and platform gates remain open.

## Accepted decisions and constraints

Two scene-owned immutable meshes combine the disjoint rock backing and textured
top surfaces. Mineral overlays, cliffs, ridges, excavation and selection retain
their existing draws. No texture changes, atlases, downscaling, quality reductions
or permanent cache were introduced. Geometry is rebuilt when cell size, rock
membership or neighbour connections change. Current and last-drawn mesh sets are
retained until commands update, then released with the terrain scene.

Tests remain muted on secondary screen 2, with isolated profiles, disabled physical
benchmark input and a 20 GiB storage floor. The owner profile is unchanged.

## Current state

Changed source:

- `scripts/rock_surface_batch.gd` and its new paired UID: immutable surface geometry.
- `scripts/terrain_content_canvas.gd`: retained surface node, invalidation and slot order.
- `assets/environment/rock-blockers-v1/rock_view.gd`: optional surface omission for
  the retained path; direct/reference draws keep their previous default.

The maintained terrain test already exercises the new normal path. No release
package, upload, Mac certification, owner layout or gameplay decision changed.

## Verification

Real reported 12-room save and deterministic 40-room expansion, Windows RTX 4070 Ti,
1920×1080. Actual `debug=false` runtime with small source overlays, shared original
PCK SHA-256 `e9d3f8460270b78b8eba5d29300349f1639ebd405965223e2b88f1be1ba6d297`.
Three reference/candidate pairs per map, alternating lane order, idle/pan/zoom/
lighting at 1×/2×/4×, 90 frames per phase: 12,960 measured gameplay frames total.

| Map | Mean before → after | Change | p95 before → after | p99 before → after | Frames >50 ms |
|---|---|---|---|---|---|
| 12 rooms | 14.984 → 14.700 ms | 1.89% shorter | 21.153 → 20.964 ms | 25.115 → 24.883 ms | 0 → 0 |
| 40 rooms | 27.313 → 26.855 ms | 1.68% shorter | 43.730 → 43.567 ms | 55.893 → 54.851 ms | 59 → 60 |

All three small-map means improve; large-map pairs are mixed. This is a modest
rendering benefit, not stutter closure or 60 FPS acceptance. Texture budgets and
the larger simulation/animation preparation costs still require separate work.

Attribution: rocks account for 491 of 512 terrain calls; wreck sprites 20 and plants
1. Frozen full-map batching reduces total calls by 164 on both scenes (12-room
2021→1857; 40-room 3428→3264). Delayed GPU query reductions are approximately
0.6–0.8 ms and 0.7–1.5 ms respectively; these cannot be added to gameplay times.

Quality and behavior:

- 36 native synthetic surface comparisons: exact, including transparency/filtering.
- Six frozen full-map candidate/reference comparisons and restoration checks: exact.
- 48 real-map comparisons: exact across excavation stages, clearance, three scales
  and nearest/linear filtering; restored gameplay state matches.
- Installed existing `test_terrain_cell_retention.gd`: **296 checks, zero failures**,
  including 272 exact images, first draw, selection, visibility, added/removed cells,
  camera transforms, empty field, invalidation and scene cleanup.
- All physical gameplay state matches in all 72 phase pairs. Exact serialized
  playback state matches in 71/72: one final 4× lighting phase differs only in
  Branfort's phase/last-time/motion-started by one simulation step (0.0667 s).
  Unchanged baseline runs 1/2 versus 3 show the identical three-value variation.
  A render-completion barrier repeat also reproduces it. It also occurs without batch
  draws; this establishes reference-lane observation variability, not a distinct
  candidate gameplay regression. Do not
  silently normalize or claim these clock snapshots are deterministic; follow up
  with direct animation-output sampling.

The installed test launcher initially had two wrapper failures (helper extraction,
then duplicate `run`); the owned failed process was stopped, configuration restored
and the corrected V3 test passed. They were not terrain test failures.

Every native run ended; runtime override configuration restored. All 2,938 owner
files unchanged. Focused source whitespace check passes. Including the attribution
runs and failed wrapper evidence, outputs are approximately 62.2 MiB plus 67.6 MiB
scratch, using shared PCKs rather than full copies. C: 126.98 GiB and D: 78.90 GiB
free at completion. No recursive cleanup retry.

Evidence root: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`;
`rock-gameplay-pairs/summary.json`, `playback-clock-comparison.json`,
`rock-gameplay-render-settled/`, `rock-real-map-mutations/`, and
`rock-installed-retention-v3/`. Focused runners remain in
`output/renderdoc-tools-2026-10-08/`.

## Next action

Investigate the larger active large-map CPU/preparation costs and directly sample
animation output at fixed simulation times, including 30/60/120 FPS. The new rock
key currently performs a second neighbour scan: measure whether reusing the
existing per-cell mask removes worthwhile CPU work before changing it.

Repeat the complete workload and loading matrix on a newly frozen packaged
candidate; endurance, release bugs, target GTX 1650/M1 hardware and native Mac
signing/notarization/gameplay remain outstanding. Keep latest accepted visual
quality and bounded test storage. Do not upload or change itch.io visibility.
