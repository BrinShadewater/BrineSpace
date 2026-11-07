# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: real-map performance validation

## Objective and acceptance

Validate the installed template-link bounds fix beyond the current station, with
matched native performance and full gameplay/camera/UI state comparisons.
Full release gates remain open; this comparison is not Mac or target-GPU certification.

## Accepted decisions and constraints

Muted secondary display, isolated profiles, owner fingerprints. Existing debug=false
release runtime plus small script overlays; no asset/runtime copies or screenshots.
Same fixture-only deterministic survey/notification clocks in both lanes. The original
template sweep is restored only in the reference overlay; installed source is unchanged.
No automatic quality changes, route deferral or gameplay changes.

## Current state

No production edits this milestone. New scoped runners/comparator:
`output/renderdoc-tools-2026-10-08/run-template-bounds-other-maps.py` and
`compare-template-bounds-other-maps.py`. Evidence:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/template-bounds-other-maps/`.
Includes identities, comparison, slow-frame audit, owner guard and storage summary.

## Verification

Twelve native runs, three alternating pairs per map, idle/pan/selection/zoom-selection
at 1x/2x/4x, 90 measured frames per phase: 12,960 frames. Reported 12-room save and
deterministic 40-room fixture with active production/crew/drones. All 72 full paired
phase states/cameras and 324 UI snapshots exact. No engine errors/missing runtime art.

| Map/metric | Pre-fix | Installed |
|---|---:|---:|
| Reported mean ms | 12.295 | 11.925 |
| Reported p95 / p99 ms | 17.911 / 34.811 | 17.641 / 34.235 |
| Reported max ms | 41.878 | 40.872 |
| Large mean ms | 25.545 | 25.586 |
| Large p95 / p99 ms | 38.383 / 63.437 | 37.483 / 64.377 |
| Large max ms | 102.528 | 98.906 |
| Large >50 / >100 ms | 66 / 1 | 68 / 0 |

Reported mean -3.01%, with two pairs better and one slightly worse; not universal.
Large +0.16% and mixed tails: effectively neutral, no broad gain. Texture peaks
unchanged, 1559.506 / 3028.686 MiB. Installed fix's stronger acceptance remains the
previous current-map construction spike, not overall FPS.

All 134 large >50 ms frames audited: 113 zoom-selection, 17 selection, 3 idle, 1 pan.
49 have sampled uploads and 85 do not. Repeated 2x zoom-selection frame 78 reaches
95.820–102.528 ms across all six runs: drawing-command work ~47.756–53.327 ms,
sampled texture creation ~19.461–21.724 ms, crew ~1.554–1.619 ms. Nested profiler
timings overlap; do not add them. The >100 ms reference frame has the same trigger
as near-100 ms installed frames, so the fix does not close this rendering stall.

Owner guard: 2938 unchanged. Native jobs terminal; runner restores override. Evidence
37.25 MiB plus 33.87 MiB short-path scratch profiles. Tool safety policy blocked their
removal; profiles retained, no alternative deletion attempted. C 122.95 / D 69.67 GiB
free. No art batches or full runtime copies created.

## Next action

Attribute zoom-triggered drawing-command rebuilds by stage/layer and invalidation
cause on these same logical frames. Separate texture-creation frames from the 85
no-upload slow frames. Preserve complete rooms and selected visual quality when
reducing redraw work. Separate non-rebuild passage spike remains open; loading,
endurance, broader bugs/visuals and PC/Mac certification remain unfinished.
