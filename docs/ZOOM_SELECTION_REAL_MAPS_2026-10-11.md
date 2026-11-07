# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: real-map zoom validation

## Objective and acceptance

Verify installed zoom cache fix on the reported and owner-current stations.
Matched native frame measurements and exact gameplay/camera/UI comparisons,
without touching owner saves. Full PC/Mac release requirements remain open.

## Accepted decisions and constraints

Muted secondary display, scratch profiles, owner fingerprints; reused physical
debug=false runtime plus small script overlays. No screenshot/art batches.
Same deterministic fixture-only survey and notification clocks in both lanes.
Compare installed source against an overlay restoring only the old selection
cache condition; navigation and other accepted improvements remain in both lanes.

## Current state

No new production changes. Runners/comparator in
`output/renderdoc-tools-2026-10-08/run-zoom-selection-real-maps.py` and
`compare-zoom-selection-real-maps.py`. Evidence under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/zoom-selection-real-maps/`.
Input saves/source identities preserved; all identities unchanged after runs.

## Verification

Twelve native runs, three alternating matched pairs per map, idle/pan/selection/
zoom-selection at 1x/2x/4x, 90 measured frames per phase: 12,960 frames.
All 72 full paired phase states/cameras and 324 UI snapshots exact.

| Metric | Pre-fix | Installed |
|---|---:|---:|
| Reported mean ms | 12.151 | 12.038 |
| Reported p95 / p99 ms | 17.761 / 34.898 | 17.669 / 26.337 |
| Reported max ms | 45.265 | 37.233 |
| Current mean ms | 11.964 | 11.794 |
| Current p95 / p99 ms | 19.546 / 31.589 | 19.312 / 29.004 |
| Current max ms | 45.355 | 45.396 |

Reported mean -0.93%, mixed pairs. Current -1.42%, all three pair means better.
No frames >50 ms in either lane on these maps. Texture peaks unchanged:
1559.506 MiB reported, 1945.262 MiB current; upload counts and decoded bytes
unchanged. These real maps still exceed p95 16.7 / p99 25 ms gates; this does not
certify target GTX1650/M1 hardware, 1440p/Retina, cold loading or endurance.
Native visual acceptance remains the preceding zoom-fix milestone's recorded scope.

No engine errors/missing runtime art. Owner guard 2938 unchanged; native jobs
terminal and runtime override restored. Evidence 33.88 MiB plus 33.83 MiB scratch;
C 122.95 / D 69.55 GiB free. No cleanup-policy bypass attempted.

## Next action

Measure actor preparation in static floor/wall passes before removing it.
`_draw_nursery` prepares actor frames for those passes; painted-shell renderer
returns before crew drawing, and floor rendering has its separate path. Frame
getters already cache, and calls may affect playback snapshots, so this is an
unmeasured hypothesis, not an accepted optimization.

Residual large-map upload-heavy examples include 96,337,920 / 144,506,880 decoded
bytes for mining-rover collect/effects sheets (~92 / 138 MiB). These are creation
diagnostics, not confirmed bus traffic or simultaneous allocation. Preserve prior
rejected 512 MiB cache, row-strip pixel mismatch and indexed lease trials; do not
repeat them unchanged. Full memory/loading/endurance/bug/visual and PC/Mac release
certification remains unfinished. Indexed lossless provider stays private.
