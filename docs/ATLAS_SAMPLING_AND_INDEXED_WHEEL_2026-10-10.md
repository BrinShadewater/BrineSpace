# Project handoff — atlas sampling isolated; additional wheel encoding tested privately

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Continue reducing measured drone upload pressure without changing selected pixels.
Previous turn was progress: fresh traces confirmed repeated large uploads/evictions and
rejected plain RGBA paging on native pixels. This turn isolates that failure and verifies
a new lossless full-dimension source, then measures it. Complete release goal remains open.

## Accepted decisions and constraints
Muted secondary Windows display, isolated resolved APPDATA, owner fingerprints,20GiB
storage floor, reused runtime/small overlays. No production rendering, art, filtering or
cache-budget change. Keep all failed candidates private. Native standalone checks and
actual debug=false gameplay comparisons have distinct scopes.

## Current state: paging diagnostics
Control using the original texture on both views passes all84 rendered comparisons.
The same native controls/scales/mirrors/frame boundaries therefore support differential
testing. A1×1 owned texture proxy reports original atlas dimensions for the canvas
draw command while a separate shader reads the small page.

Matching-build [Godot canvas shader source](https://github.com/godotengine/godot/blob/ed1daf0bf/drivers/gles3/shaders/canvas.glsl)
shows normalized-coordinate interpolation and half-texel region clamping;
[renderer implementation](https://github.com/godotengine/godot/blob/master/drivers/gles3/rasterizer_canvas_gles3.cpp)
provides the source rectangle from pixel coordinates and inverse texture size. These
references guide the experiment; they do not certify a remedy on another platform.

Native proxy diagnostic compares all32 bits of both UV components over336 combinations
(seven frames, three scales, mirror, filter and component/byte-plane):675checks/zero failures.
The original command-coordinate values are preserved in this tested fixture. That alone
does not preserve texture sampling after remapping to a smaller physical texture.

Observed exact nearest results out of42:
- Plain smaller-page draw:9 (preceding turn).
- Original-coordinate proxy with integer texel fetch:12.
- Added hypothetical sampling quantization bias:6; reject this hypothesis.
- Proxy with normal GPU sampler and page remapping:15.
- Same sampler/proxy reading the full original texture:42.

The sampler diagnostics deliberately bind a nearest sampler; their linear-reference
comparisons are not a test of a linear paging implementation. Diagnostic execution
messages only cover execution/core checks; report.cases supplies the actual pixel result.
Original standalone paging did test actual linear filtering and failed42/42. No paging
implementation is accepted. Texture-dimension remapping remains a fidelity barrier;
the exact hardware sampling mechanism is not fully established. Avoid further arbitrary
bias tuning or pretending successful coordinate checks prove final pixel equality.

## Additional indexed source
Fresh trace coverage: existing private20-source indexed catalog covers39.65% of decoded
upload bytes (39/193 events), leaving substantial pressure in ordinary sources.
New private encoding: steer-right-west.png, observed ten uploads in the earlier trace.
Original2688×4480 RGBA atlas:48,168,960bytes.39,660unique RGBA values fit RG8 indices
plus a256×155RGBA palette:24,243,200bytes (~49.7% reduction), unchanged dimensions.
Every reconstructed byte matches, including transparent RGB. Original PNG/hash unchanged;
private PNG outputs total~2.04MiB. No lossy quantization or frame removal.

Native standalone172checks/zero failures,84 exact rendered pairs: seven frames,
three scales and mirrors;42 nearest pairs use indexed storage,42 linear pairs use
the original RGBA fallback. Full texture dimensions and native coordinate sampling are
retained. Scope is one atlas and white modulation, not full-station motion/lighting.

## Incremental gameplay measurement
Updated private grid restores current prewarm_station_views from normal source, so both
lanes retain the accepted pending-room/layout fixes. Current Solar source is explicitly
overlaid too. Do not reuse the old private grid against current source: it predates the
construction fixes. Existing historical reports remain scoped to their tested revision.

Three alternating matched debug=false40-room pairs compare private indexed20 versus21,
not normal RGBA versus candidate.6,480frames, idle/pan/zoom/lighting1×/2×/4×.

| Metric | Indexed20 | Indexed21 |
|---|---:|---:|
| Mean ms |29.168|29.048|
| p95 ms |47.399|47.828|
| p99 ms |61.491|59.194|
| Max ms |101.130|98.191|
| >50 / >100 frames |118 /2|122 /0|
| Peak sampled texture MiB |2629.355|2629.355|

Mean improves0.41%, mixed pair means. No scene-peak memory reduction; p95 and >50 count
worsen slightly. All36full gameplay/camera pairs exact. Backend20/21source checks,
missing-image/runtime/mute/input/coverage and no ordinary duplicate guards pass.
Useful private data point, not normal-game FPS acceptance or a release certification.
Keep the entire indexed provider and this extension private pending broader checks.

## Changed artifacts and verification
No production code changes. Private evidence under
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/rgba-page-*,
indexed-steer-west-feasibility and indexed-steer-west-incremental. New source PNGs,
encoding/hash proof, refreshed private grid/catalog/resource lists, native reports,
six gameplay reports/logs, comparison and source/storage identities retained.
Focused runners in output/renderdoc-tools-2026-10-08/run-rgba-page-*.py,
run-indexed-steer-west-*.py and incremental comparator. All jobs terminal; runtime
configuration restored; original art/source identities unchanged. Every owner guard
2938files before/after, no changes.87.98MiB evidence+profiles; C125.00/D73.91GiB free.

## Next action
Test the refreshed full-dimension indexed candidate in whole-station same-clock motion,
loading/fallback and scene lifetime, then profile its added renderer/CPU work and compare
against current normal source. Prioritize measured high-byte fallback sources rather
than extending the catalog indiscriminately. Paging remains deferred on failed pixel
checks. Normal gameplay, all performance targets and PC/Mac release gates remain open.
