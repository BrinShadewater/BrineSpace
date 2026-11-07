# Terrain cell retention integration

Updated: October 5, 2026 · BrineSpace · R5

## Objective and acceptance

Reduce terrain rebuilding during excavation while preserving exact progress,
artwork, ordering, selection, neighbor edges, visibility and camera transforms.

## Accepted decisions and constraints

Enabled by default; `--reference-terrain-cells` restores the original whole-field
terrain pass. Each grid owns its terrain host; no global node/image cache. Keep
original rock/selection/wreck/plant order, exact progress and full-field neighbor
queries. No animation/frame/quality reduction or gameplay timing changes.

## Current state

- `scripts/terrain_content_canvas.gd` and UID: retained cells in ordered groups,
  keys for scale, kind, progress, clearing, visibility and neighbor connections.
  Removes missing cells, preserves dictionary insertion order, shares existing
  renderer textures and records deferred drawing in grid diagnostics.
- `scripts/grid_canvas.gd`: terrain host integration and reference switch;
  buried-state changes now invalidate the terrain key as drawing requires.
- Rock/wreck renderer scripts: optional cell subset; original full-field calls
  retain their behavior. Rock selection uses the same extracted draw function.
- `tests/test_terrain_cell_retention.gd` and UID; native performance registration.
  Existing source UIDs and selected art remain unchanged.

## Verification

Final enabled source: **296 checks, zero failures**, including **272 byte-exact
comparisons** using the actual grid terrain pass. Coverage: first rendered frame,
progress, rock/wreck selection, clearing, buried-site reveal, buried-state key,
insertion/removal, field replacement, scale/translation, plants, reference-mode
switching and scene deletion. Two scales, offsets and filters. Deferred deletion
is checked through observable weak-reference release; the initial fixed-frame
cleanup check was corrected. Initial fixture parse typing error also corrected.
Final native logs have no engine errors. Integrated terrain and station captures
visually inspected. Full moving station/zoom pixel certification remains open.

Three reference and three candidate 40-room 1080p native runs, 60 samples per
action/speed. Workload: idle, excavation and zoom at 1x/2x/4x. Dedicated fixture
seeds an already-arrived mining drone, resetting its rock per excavation phase;
normal fleet/clearance updates advance progress. It is a deterministic fixture,
not a player arrival/recovery test. Both variants retain earlier accepted changes.

Median of three phase measurements:

| Excavation | Reference terrain CPU | Retained terrain CPU | Reference p95 | Retained p95 |
| --- | ---: | ---: | ---: | ---: |
| 1x | 5.669 ms | 0.787 ms | 63.670 ms | 51.948 ms |
| 2x | 5.772 ms | 0.757 ms | 50.618 ms | 42.493 ms |
| 4x | 5.856 ms | 0.773 ms | 60.313 ms | 51.153 ms |

Terrain CPU includes parent preparation and deferred cell drawing. Mean of nine
phase mean-frame-time medians improves **46.555 to 41.602 ms**. Idle 2x and zoom
4x tails worsen; stalls remain (maximum sampled 958 ms reference / 937 ms
candidate). Do not claim universally improved pacing or release-gate success.
Station draw-call counts also decrease in these runs; the earlier small fixture's
counts were equal, so that result does not predict every scene. Report fields are
additive and collection is limited to the existing profiling path.

Texture counters remain roughly **4,404 MiB** in settled comparisons. No texture
memory remedy or measured node-memory budget is claimed. No minimum-hardware,
1440p, packaged, Mac or endurance acceptance. All **2,936 owner non-log files
unchanged** across validation and benchmark groups; six runs have zero engine
errors/missing-art reports. Scoped diff whitespace and test-index checks pass.

Evidence: `output/terrain-retention-2026-10-05/`: scripts, logs, input/final source
hashes, images, six raw reports and `station-comparison.json`. Earlier prototype
evidence remains separately scoped. No exports, uploads or commits this interval.

## Next action

R6: profile large-room prop submission before adding retention/culling there.
Keep the full-roster memory remedy mandatory and track long stalls separately.
Carry R5 into packaged/platform benchmarks and full scene-transition/endurance
coverage; the PC/Mac release remains blocked on the existing gates.
