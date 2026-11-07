# Shared monitor waveform calculations

Updated: October 10, 2026 · Project: BrineSpace · PC/Mac performance work

## Objective and acceptance

Reduce repeated room-effect calculations while preserving every draw, animation
time, source image and selected quality. One source optimization is accepted;
the complete release performance and platform gates remain open.

## Accepted decisions and constraints

Normalized 25-point monitor traces depend only on the exact animation clock and
screen index. Share their calculation within a scene. Every monitor still applies
its original geometry and submits its original commands at its original clock.
The cache clears when its clock changes, caps at 64 traces, owns no images and
releases with the scene. Special/custom/flipped artwork keeps existing fallbacks.

Continue isolated, muted secondary-screen tests with disabled physical benchmark
input and a 20 GiB storage floor. No art changes, quality reduction, engine update,
atlas conversion, gameplay change, full package copies or cleanup retry.

## Current state

- `scripts/prepared_library_screens.gd`: bounded read-only normalized waveform cache.
- `scripts/room_content_canvas.gd`: supply the cache to the existing monitor path.
- `scripts/grid_canvas.gd`: share one cache among scene-owned room canvases.
- `tests/test_library_live_context.gd`: verify shared reuse, bounds, scene release
  and animation-clock samples for 30/60/120 FPS at 1×/2×/4×.

Existing UID sidecars and test-index registration preserved. Release packages and
Mac certification have not changed.

## Verification

Investigated current-source saved 40-room native `debug=false` gameplay first:

- Simulation approximately 2 ms/frame in prior reports; it was not the largest
  measured component. Do not label all unaccounted frame time as simulation.
- Door/light diagnostic: connectivity plus port enumeration approximately 0.27 ms,
  door-frame calculation approximately 0.20 ms. Instrumented helper costs can nest;
  instrumentation has overhead and these are not workload improvement measurements.
- Content-paint diagnostic: 110 ordinary library-effect paints/frame approximately
  1.54 ms, roughly two-thirds of content painting in the sampled 1× idle phase.
  Renderer-field binding/restoration was a comparatively small component.

Three matched reference/candidate 40-room pairs on Windows RTX 4070 Ti, 1080p,
alternating lane order, idle/pan/lighting at 1×/2×/4×, 90 frames/phase. Shared actual
release executable/PCK with small source overlays; 4,860 measured frames total.

| Metric | Reference | Candidate |
|---|---:|---:|
| Average frame time | 27.715 ms | 27.514 ms |
| p95 | 43.975 ms | 43.920 ms |
| p99 | 53.742 ms | 52.471 ms |
| Frames >50 ms | 41 | 38 |
| Mean content painting | 2,485.7 µs | 2,402.6 µs |

Average frame time is 0.72% shorter; content painting is 3.34% shorter. All three
pair means favor the cache, but the gain is small and release gates still fail.
Do not add this percentage to gains from differently scoped earlier workloads.

Quality/behavior checks:

- Initial native library regression: 512 checks/406 exact raster pairs across 179
  actual registrations, wet materials, filters, transforms, flips, operating states,
  Reduced Motion, clocks and fallback behavior.
- Shared scene cache: 515 checks, including reuse, 64-entry bound and scene release.
- Extended and installed native regression: **569 checks, zero failures**, including
  460 exact raster pairs and the 54 new FPS/speed/clock samples.
- All physical gameplay snapshots match across all 27 measured phase pairs.
  26/27 complete serialized snapshots match. One final 4× lighting snapshot differs
  only in Branfort's cached last-rendered position, phase, last-time and motion-start.
- A separate actual native matched pair requested Branfort's frame at the same
  current simulation clock after the workload. Position, full playback snapshot,
  184×184 RGBA image size/format and SHA-256 all match exactly. The prior cached
  snapshot was approximately 0.933 seconds behind that current clock on both lanes.
  Cached render observations are not a deterministic current-time simulation gate.
  This does not certify all crew animation at every FPS or close the broader
  animation-timing release work.

The initial native runner checked an incorrect terminal string after a passing
test; its isolated `context.json`, zero-failure log and owner guard were separately
validated. The string was corrected; subsequent shared/clock/installed runs passed.

Every job is terminal; runtime override restored; all 2,938 owner files unchanged;
focused whitespace check passes. Approximately 44.1 MiB evidence and 35.3 MiB
scratch for this pass; no full PCK copies. At completion C:126.93 GiB/D:78.82 GiB free.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`door-validation-attribution/attribution.json`, `content-paint-attribution/attribution.json`,
`screen-wave-gameplay-pairs/summary.json`,
`screen-wave-canonical-pose/canonical-comparison.json`, and
`screen-wave-installed-native/`. Focused runners remain in
`output/renderdoc-tools-2026-10-08/`.

## Next action

The canonical-pose run also recorded a 101.042 ms 1× lighting frame (frame 73).
Its sampled-frame drone events are complete: 289,013,764 decoded/uploaded bytes
(289.0 MB decimal/275.6 MiB), four synchronous texture creation/upload calls totaling
39.056 ms. They include collect-south-cargo (96.3 MB), wheel-layer-north (48.2 MB),
mine-north-effects (144.5 MB), and a 1×1 empty image. Exterior-actor drawing totals
55.845 ms and includes those calls; floor passes also total 12.314 ms. Do not add
nested totals or delayed GPU queries as independent costs.

Investigate the request/eviction sequence and predictably prepare required drone
layers before their first visible use, within the current memory budget. Avoid
incomplete drones or altered animation timing. Prior larger-cache and cropped/row
upload trials failed their respective performance/quality gates; do not repeat
them unchanged. Reproduce whether the >100 ms stall is consistent and account for
every >50 ms event. Then complete the full packaged workload, loading, endurance,
bug, GTX 1650 and native M1/Mac release-certification matrix. No itch.io publication.
