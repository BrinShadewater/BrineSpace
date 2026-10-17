# Drawing and render submission — October 15, 2026

The private Windows candidate prepares Moonbay water geometry about **0.29–0.40 ms
faster per frame** in the diagnostic workload. Pooled normal idle improves
**51.98→52.86 FPS**, 4× idle **45.47→47.09**, and 4× placement-phase average
**43.46→44.80**. Placement action frames are mixed: **58.738→57.009 ms** forward,
**57.024→57.903 ms** reverse. This is a small CPU gain; it does not establish a
shorter placement hitch or reach 60 FPS.

Keep V2 private. Normal game sources and the shipping candidate were not changed.
Mac/build packaging, broader pacing and native-memory acceptance remain open.
The reference already contains private stable-ID V3 navigation and distant-room /
one-spare configuration. These are **not comparisons against the installed game**.

## Root cause and implementation

Release diagnostics find about 4.7 ms in aggregate live-room drawing and 2.3–2.5 ms
in the 4× exterior pass. These include child callbacks/uploads and cannot be added
to their nested scopes. Detailed exterior tracing finds drone drawing ~2.29 ms,
including atlas work ~2.0 ms. Static harvest is only ~0.11 ms, so proposed harvest
retention was not implemented. Door/light validation is ~0.70 ms, the surface key
~0.40 ms and fog ~0.39 ms.

Moonbay water geometry preparation costs ~1.3 ms/frame. V1 moves individual AA
ribbon packets into an optional native helper. V2 compiles each ordered raw
command group in one native call, reducing repeated script/native calls. It
produces the same owned float32 point/color/strip-count arrays, then uses the
existing topology cache and drawing loop. Other commands and unsupported
polylines keep their command-stream position. Clocks, geometry, colors, blend
order, crew, doors, warnings and navigation are unchanged.

| Diagnostic phase | Reference water CPU | V1 packets | V2 batch |
|---|---:|---:|---:|
| 1× idle | 1.340 ms | 1.015 ms | 0.942 ms |
| 1× placement | 1.335 ms | 1.034 ms | 0.965 ms |
| 4× idle | 1.318 ms | 1.097 ms | 1.028 ms |
| 4× placement | 1.303 ms | 1.084 ms | 0.965 ms |

These are separate instrumented diagnostics, not final FPS lanes. GPU draw counts
remain essentially unchanged: ~2,117–2,196/frame depending on phase. This improves
CPU geometry preparation; reduced GPU submission is not demonstrated. Do not
attribute the full wall-time difference solely to water: process variance and
other drawing/upload work remain.

The helper retains counters only. Geometry/vectors are local to a call; no path,
canvas, texture or clock persists. The canvas-owned script topology/cache policy
is unchanged. Extension absent/reference flag selects the original script. API2
loads before the first water draw; optional helper lookup is cached.

`add_packet` falls back to script when native generation rejects input. The batch
compiler instead passes unsupported lines through as raw polylines. Acceptance
covers normal finite generated 7/25-point water paths; oversized/nonfinite batch
parity is unproven. All live candidate runs have zero rejected packets. Independent
read-only review found no blocker within this domain, checking order, float32
boundaries, ownership, pointer lifetimes and shared topology.

## Guarded release benchmark

Godot 4.7.2 `ed1daf0bf`, actual Windows release executable/PCK, Compatibility /
OpenGL, RTX 4070 Ti, 1920×1080. Maintained `mixed_large` fixture; 180 warm frames
per process, then 120 each of idle/placement at 1×/4×. Serial order: reference →
candidate2 → candidate2 → reference. **1,920 measured frames**, eight exact phase-end
state, camera endpoint and per-frame camera-path pairs. Existing benchmark
observers remain; new detailed profiler wrappers are absent from final lanes.
VSync and frame cap measured disabled. Every guard-valid run retained.

Both lanes load unchanged stable-ID V3 and water V2 binaries; each makes ten
stable-navigation calls. Reference water counters stay zero; each candidate makes
1,320 batches / 105,099 packets, zero rejections. Source/pack/native identities
verified before/after. Process/window guard has no errors/foreign Godot runtime;
the owner's editor was preserved. Each pooled cell below contains 240 frames.
FPS = 1,000 / pooled mean; p95 recomputed over combined samples.

| Phase | Reference FPS | V2 FPS | Reference p95 | V2 p95 |
|---|---:|---:|---:|---:|
| 1× idle | 51.98 | 52.86 | 21.680 ms | 22.798 ms |
| 1× placement | 50.94 | 51.66 | 23.106 ms | 23.717 ms |
| 4× idle | 45.47 | 47.09 | 37.988 ms | 36.339 ms |
| 4× placement | 43.46 | 44.80 | 37.037 ms | 34.867 ms |

4× FPS improves in both orders: idle 44.845→46.813 / 46.110→47.371; placement
43.610→44.701 / 43.314→44.905. Normal reverse order worsens: idle 52.098→51.878,
placement 51.129→50.596. Forward gains produce the pooled improvement. Normal
pooled p95 worsens in both phases. **0/8 candidate phases pass the mean-and-p95
≤16.667 ms 60 FPS gate.**

## Placement and following frames

Action = fixture frame 30; following window = frames 31–90, excluding action.

| Speed/order | Action reference→V2 | Next frame reference→V2 | Following 60 mean | Following 60 p95 | Following 60 >50 ms |
|---|---:|---:|---:|---:|---:|
| 1× forward | 49.749→45.833 ms | 23.106→23.674 ms | 19.688→18.759 ms | 23.106→23.674 ms | 0→0 |
| 1× reverse | 46.404→49.003 ms | 23.562→23.717 ms | 19.610→19.759 ms | 23.213→23.717 ms | 0→0 |
| 4× forward | 58.738→57.009 ms | 24.124→23.296 ms | 23.199→22.727 ms | 34.556→34.395 ms | 1→1 |
| 4× reverse | 57.024→57.903 ms | 24.190→22.907 ms | 23.568→22.466 ms | 37.037→34.867 ms | 1→1 |

Mean 4× action 57.881→57.456 ms has opposite per-order signs. Following 4× mean /
p95 improve in both orders; each still has one >50 ms frame, two including action.
Full 4× placement maxima are 58.738→57.321 ms forward, 57.666→57.903 ms reverse.
No sampled frame exceeds 100 ms. Remaining placement stalls are not solved.

## Correctness, visuals and profile protection

- V1 and V2 packet oracles each pass **21,079 assertions**, comparing exact point,
  color and strip-count bytes to the independent original strip algorithm.
  Randomized magnitudes, duplicate/closed paths, widths and rounding boundaries
  covered. Expected failing feature checks observed before implementation.
- V2 batch oracle: **1,565 assertions across 109 compiler calls** (108 water cases
  plus one synthetic mixed sequence); order, passthrough boundaries, three
  extents, six depths, three clocks and pumping covered.
- Native animated water: **494 checks / 244 exact raster pairs**, including scales,
  cache eviction, pause/activity and lifetime; 134 batches / 6,157 packets,
  zero rejections. Extension-absent script fallback: **21,076 assertions**.
- **Seventeen cross-process station/first-placement pairs** exact at 1920×1080,
  plus twelve repeat pairs. Three zooms, lighting on/off, and five first-placement
  frames with matching state/camera/readiness/activation. Representative zoom-0.5
  image visually inspected.
- All **26 owner guards** preserve initial/prior protected **2,948 files**. Normal
  selected source/UID/test hashes unchanged. Twelve stable-native and ten
  water-native guards clean. Final audit passes.

Engine memory counters equal across all four timing processes: 2,026.62 MB start,
2,044.11 MB end, 2,776.91 MB peak texture counter. These do not measure native
transient allocations/RSS; no broad memory/long-soak acceptance claimed. Earlier
`TEST_PROFILE_INCIDENT_2026-10-15.md` recovery caveat remains unchanged.

## Evidence and next action

Evidence: `C:/bs-draw-submit-20261015/`; helpers:
`output/draw-submit-20261015/`. Reference's 22 scripts/PCK match prior stable-ID V3.
V2 changes only frozen `moonbay.gd` and `water_stroke_triangles.gd`. Native V1/V2
source/build/DLL manifests preserved separately under `water-native/`.

V2 DLL SHA-256 `4e3dc0516744ac04d0599de5d8a5cd7c76e867ff349bd68c135a4a8d9c6cad74`
(343,552 bytes). Stable V3 DLL unchanged:
`ccc5debfd91df60c9940ac217e1859841363c265ccd343f9c1c19643f783a23d`.
MSVC 14.44.35207, release/speed/single, `/fp:precise`; godot-cpp pin
`1e7926375b62b445fa79db6851f7105b644831f2`; exact API dump SHA
`d0e4c08c03b165156dabe6bfb6a906baf0069189f62035341230a246c86d6986`.
Godot/godot-cpp licenses copied alongside. No dependency/native installation,
export, Mac package, commit or upload.

Primary evidence: `draw1-analysis.json`, four timing reports, process guard,
`final-audit.json`, `visual-parity.json`, `first-paint-parity.json`, water oracle
logs and scratch pixel `context.json`. Diagnostic profile analyses explain scope
attribution; do not pool their timings with acceptance lanes.

Next trace the surviving ~2,100–2,200 draw calls and CPU submission separately,
then test a bounded retained-command/resource change preserving blend order.
Drone atlas/upload bursts remain a large 4× cost. Before native integration:
Mac/build/package, fallback lifecycle, longer pacing and transient/working-set
checks. Keep water and stable-ID changes independently reviewable.
