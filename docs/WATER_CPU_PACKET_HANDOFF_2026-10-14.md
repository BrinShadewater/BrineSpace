# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: remaining CPU/render costs

## Objective and acceptance

Owner requested the largest remaining CPU/render-submission improvements toward
60 FPS with unchanged appearance. Admit a measured local CPU improvement only
after exact geometry/native pixels and bounded ownership checks. Whole-frame
timings need an otherwise quiet machine; component results do not establish FPS.

## Accepted decisions and constraints

Install the contained Moonbay water CPU change. Keep animation clocks, ribbon
positions/colours, antialiasing, command order, crew, doors and warnings intact.
The room-raster prototypes remain private. Neither rejected drone experiment is
part of this candidate. No export, commit, publication or Mac acceptance implied.

## Current state

Changed normal files:

- `scripts/water_stroke_triangles.gd`: use native `Vector2.angle_to()` for the
  existing cross/dot/atan2 calculation; hoist unchanged rounded half-width.
  Optional packet mode assembles/reuses complete ordered index buffers instead
  of hundreds of per-strip dictionary lookups/appends. Cache capped at 64 layouts;
  inserted layout keys and returned indices are independent snapshots.
- `rooms/large-rooms/moonbay.gd`: water command packets opt into that mode.
- `tests/test_water_stroke_triangles.gd`: permanent ordered geometry, cache
  eviction and caller-mutation coverage. Existing UIDs/index lane retained.

Evidence: `C:/bs-frame-cpu-20261014/`; drivers: `output/frame-cpu-20261014/`.
Final private PCK SHA256:
`084ca0c0f8e0f2a1b706b3ace5d2f2eac8bd538dbfd300de35842170a071a965`.
It overlays the existing private LOD/reuse baseline plus accepted companion fix.
Normal helper equals that measured helper except comments; Moonbay is identical.
`production-source.json` and `production-verification.json` record source hashes.

## Verification

Fresh attribution: live-room scope ~6.3 ms, Moonbay base ~1.93 ms, door/light
validation ~1.5 ms with diagnostic wrappers (~1.3 ms without), delayed render CPU
~5.6–6 ms. Moonbay water consumes ~1.62 ms, of which stroke preparation ~1.17 ms.
These nested scopes overlap. Door helper costs are spread across topology,
light sampling and key construction; there is no single comparable shortcut.

Final buffer stress: 49,250 checks / 5,000 packets, exact points/colours/indices,
varying lengths/counts, tiny through large finite coordinates, degeneracy,
eviction and mutation isolation. Zero failures. Native water fixture: 493 checks /
244 exact pixel pairs, zero failures. Final continuous native sweep: 720 exact
pixel pairs with full animated water and continuous filling/pumping, both drawing
orders, zero failures. Representative native water image reviewed.

Paired in-process water CPU means, reference -> candidate (microseconds):

| Drawing order | Full water | Filling/pumping |
|---|---:|---:|
| Forward | 1900.861 -> 1568.744 | 1174.417 -> 946.717 |
| Reverse | 1879.483 -> 1540.544 | 1151.017 -> 936.633 |

This supports a **17–20% water-CPU saving**, about 0.21–0.34 ms in these cases.
P95 improves in all four scopes; one reverse pumping maximum is 2077 -> 2231 us,
so no universal maximum-frame improvement is claimed. Full-water indices remain
92,400 bytes; pumping retains 22 layouts / 975,000 index bytes versus the original
227,232 bytes. These are index storage measurements, not total process RAM.
Station uses two layouts / 95,400 index bytes. No new textures are allocated.

Installed normal-source tests, maintained native runner, scratch APPDATA with owner
layouts: stroke 7,960 cache/scalar checks / 180 visible exact pixel pairs; water
493 checks / 244 pairs; complete large-room composition 135 checks / 80 pairs.
All three pass, no logged errors/warnings/leaks. Runner evidence:
`output/test-runs/20261014-224339-native/`. Final source review finds no actionable
issue. Scoped whitespace checks pass. Seven other runtime files match their
pre-task normal references. All 31 completed owner guards preserve 2,948 files,
including the four quiet follow-up runs below.
No task-owned QA game/editor process remains.

### Whole-station timing limitation

Final actual debug=false QA runs cover idle/pan/zoom/lighting at 1x/4x: 3,840
frames, all 16 gameplay-state/camera pairs exact. Texture peaks match at
2784.653 MiB. Raw means are 29.845 -> 27.664 and 26.270 -> 25.402 ms; p95 improves
7/8 and 3/8, and all 16 candidate 60 FPS phase gates still fail.

**Do not accept these as an FPS improvement.** Another native Godot worker was
observed during timing; the active “Complete Krusher Dom animations” chat confirms
concurrent native verification and browser playback. Its exact contribution to
the exploratory full-frame variation is unknown.
`analysis.json` preserves raw observations, not a release performance acceptance.
The owner subsequently confirmed other runs were paused; the follow-up is below.

Exploratory failures remain excluded: endpoint-direction reuse failed duplicate/
underflow review and was removed; stress found shared index values and mutable
layout keys, both fixed with explicit snapshots. Two native bootstrap attempts did
not start the fixture and were terminated; direct frozen-script invocation passes.
Earlier packet2/packet3 timing lanes are superseded and unsuitable for admission.

### Quiet follow-up after owner paused other runs

Completed the unchanged frozen reference/candidate in both orders with fresh
scratch profiles. No source, pack, workload or fixture-setting changes. A native
Windows process-snapshot guard sampled every0.5 seconds; only the pre-existing
idle editor (PID46624) was allowed. No foreign Godot worker, duplicate game or
monitor error was recorded. This guard covers Godot processes, not every possible
background workload. Evidence: `quiet1-process-guard.json`, `quiet-analysis.json`
and the four `quiet1-*-identity.json` records. All immutable pack hashes verify.

| Run order | Reference mean | Candidate mean | P95 improved | Candidate gates |
|---|---:|---:|---:|---:|
| Reference then candidate | 24.437 ms | 24.628 ms | 4/8 | 0/8 |
| Candidate then reference | 27.677 ms | 24.358 ms | 7/8 | 0/8 |

All3,840 measured frames complete; all16 state/camera pairs match. Texture peaks
remain identical at2784.653 MiB. Normal-speed idle21.478->21.387 and
21.734->21.354 ms (candidate46.76/46.83 FPS). First-order large-base CPU drops
147–219 us across phases; normal-speed idle/pan drops202/205 us. Draw calls are
unchanged, and first-order render CPU stays essentially flat at1x. Whole-frame
results remain mixed: first order0.78% slower, reverse11.99% faster, with a broad
slowdown across several reverse-reference systems beyond this small water scope.
No causal12% improvement, general FPS gain or removal of stutters is established.
Worst frames78.216->74.393 and108.402->70.898 ms; over50-ms samples4->3 and31->4.
All16 candidate60 FPS phase gates still fail. The repeatable admission remains
the verified local CPU saving; the requested quiet comparison is now complete.

## Next action

No further water benchmark or source/visual matrix is pending. Keep FPS reporting
separate from the local CPU admission. Remaining large costs include live room preparation/drawing,
door/light validation and ~6 ms render submission; the water change reduces CPU
preparation, not draw-call count. Windows delivery is unchanged; actual PC/Mac,
endurance, save/relaunch and 60 FPS release acceptance remain open.
