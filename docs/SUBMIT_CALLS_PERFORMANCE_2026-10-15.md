# Submission and draw-call trial — October 15, 2026

An exact-pixel waveform packet reduces real draw calls, but **does not establish
an FPS or placement-hitch improvement** on the large station. Keep it private;
normal game source and playable exports remain unchanged.

| Pooled phase | Reference FPS | Candidate FPS | Reference p95 | Candidate p95 |
|---|---:|---:|---:|---:|
| Normal idle | 55.93 | 55.71 | 19.853 ms | 19.570 ms |
| Normal placement | 54.73 | 54.91 | 22.662 ms | 22.198 ms |
| 4× idle | 49.11 | 48.98 | 34.235 ms | 35.276 ms |
| 4× placement | 45.68 | 45.91 | 35.882 ms | 33.418 ms |

4× action frames: **56.857→55.660 ms** forward, **55.758→56.726 ms** reverse.
Following-window pacing is mixed. **0/8** candidate phases meet mean and p95
≤16.667 ms. This reference already includes the private water V2, stable-ID V3,
distant LOD and one-spare cohort. These are fresh within-study comparisons, not
gains against the installed game or the preceding study's different process times.

## What the draw-call investigation found

After warm-up, freeze simulation and existing commands, then hide one subtree
through its RenderingServer RID and restore it. Every accepted probe restores
the **same 2,114 root-canvas calls**. These are marginal differences, not an
additive partition or frame-time estimate.

| Hidden subtree | Marginal fewer calls |
|---|---:|
| Whole station grid | 1,842 |
| LiveContents | 442 |
| Walls | 200 |
| Terrain | 156 |
| Floors | 148 |
| Foundations | 143 |
| Foreground | 125 |
| Remaining floor pass | 120 |
| Rear doors | 117 |
| Front doors | 74 |

The deeper probe finds 24 visible eligible live effect/prop-pass slots. Their
individual marginal differences sum to only 47 calls; most LiveContents calls
therefore lie outside those animated effect paths. No visible selected slot has
a `specimen_glow` effect, so its proposed nine-circle packet was **not implemented**
or benchmarked. Further generic animation batching would miss this fixture's
larger static prop/structural submission cost.

The initial `calls1` diagnostic used Node hide/show. Visibility notifications
changed retained commands: restored count fell from 2,114 to 691. Those results
were discarded. `calls2` and `calls3` use raw RID visibility, verify restoration
for every node and leave no game source change.

## Bounded implementation

Only the waveform branch in `prepared_library_screens.gd` changes. Its original
25-point open AA polyline becomes one existing ordered stroke packet: same core
and fringe triangles, colors, clock, point math, CanvasItem, material, transform
and prop/crew depth boundary. Screen rectangles, grid lines, radar primitives and
bar graphs remain verbatim. A Prepared instance owns the bounded topology;
geometry is call-local, with no prior-clock history or new nodes.

Godot's pinned GLES3 path starts a new batch for each polygon, and its AA polyline
uses core and fringe polygon commands. Joining only that polygon geometry avoids
changing the distinct color precision of rectangle/line primitives.
[Pinned GLES3 source](https://raw.githubusercontent.com/godotengine/godot/ed1daf0bf/drivers/gles3/rasterizer_canvas_gles3.cpp),
[pinned geometry source](https://raw.githubusercontent.com/godotengine/godot/ed1daf0bf/servers/rendering/renderer_canvas_cull.cpp).

The candidate is Windows gated and has `--reference-screen-traces`. It uses the
unchanged optional water API2 packet helper when present, script packets when
absent, and original polyline submission if geometry is rejected. The pinned
polyline geometry uses fixed 1.25 feather size, independent of viewport/text
oversampling; no StyleBox oversampling restriction was transferred to this path.
Acceptance is for ordinary finite generated traces, not arbitrary nonfinite input
or another platform/engine's math.

## Measured submission cost

Focused test: two waveforms reduce **18→14 canvas draw calls** with exact pixels.
In the fitted large-station view, distant-room caching already removes most
monitors. Steady idle saves only about **eight calls / 0.4%**:

| Phase | Reference mean calls | Candidate mean calls | Reported viewport CPU reference→candidate |
|---|---:|---:|---:|
| Normal idle | 2,116.73 | 2,108.75 | 4.787→4.783 ms |
| Normal placement | 2,137.42 | 2,129.38 | 4.847→4.814 ms |
| 4× idle | 2,120.34 | 2,112.26 | 4.912→4.914 ms |
| 4× placement | 2,199.50 | 2,186.66 | 5.089→5.062 ms |

Placement includes other changing rendering work; do not attribute the full pooled
12.84-call difference to waveform batching. Viewport CPU/GPU queries are delayed
engine results, not aligned current-frame submission measurements, and cannot be
added to script timings. CPU query differences here are tiny. Reduced call count
is proven; a useful end-to-end speed gain is not.

Both release candidates physically execute the intended source, checked through
the RoomContents `PreparedScreens` constant's normalized source hash. Each reference
records 105,099 native water packets; each candidate 108,739, including added
waveforms, with 1,320 unchanged water batches and zero rejected packets. Both
make ten stable-navigation calls. No preload-only implementation claim.

## Placement and subsequent pacing

Action is fixture frame 30; following window is frames 31–90, excluding action.

| Speed/order | Action reference→candidate | Next frame | Following 60 mean | Following 60 p95 | Following >50 ms |
|---|---:|---:|---:|---:|---:|
| Normal forward | 44.998→45.945 ms | 22.343→22.198 ms | 17.907→18.249 ms | 22.343→22.198 ms | 0→0 |
| Normal reverse | 46.668→45.431 ms | 23.978→22.292 ms | 18.419→17.931 ms | 23.385→22.292 ms | 0→0 |
| 4× forward | 56.857→55.660 ms | 22.929→22.568 ms | 22.509→22.456 ms | 32.965→41.082 ms | 1→1 |
| 4× reverse | 55.758→56.726 ms | 22.419→22.701 ms | 21.985→21.870 ms | 35.882→31.956 ms | 1→1 |

4× mean action 56.308→56.193 ms has opposite per-order signs. Following means
change little; forward p95 worsens materially. Each 4× following window still
has one >50 ms frame, or two including action. Entire comparison has eight→six
>50 ms frames, zero >100 ms, without a consistent FPS/hitch gain. Keep all valid
runs; no reruns selected to improve the sign.

## Verification and scope

Godot 4.7.2 `ed1daf0bf`, actual Windows release, Compatibility/OpenGL, RTX 4070 Ti,
1920×1080, muted visible secondary-display window. Serial reference→candidate→
candidate→reference; 180 warm frames then 120 each idle/placement at 1×/4× per
process. **1,920 measured frames**, eight exact phase-end simulation/route state,
camera endpoint and per-frame camera-path pairs. Existing benchmark observers
remain; no new detailed profiler wrappers in the timing lanes. Frame cap/VSync
measured off; process/window guard records no errors/foreign game process.

- Correct RED: `screen-red2` expected 18→14 but observed 18→18 before implementation.
  Initial `screen-red` had a test-generator parse typo; it is not RED acceptance.
- Native pixel oracle: **369 checks / 186 exact raster pairs**. Extension-absent
  script-packet oracle: **369 checks / 186 exact pairs**. Clocks, five widths,
  four scales, three colors, overlapping screen types, nonuniform rotated transform,
  inherited tint, Reduced Motion, activity/pause and owner lifetime covered.
  Isolated native run executes 368 waveform packets, zero rejected.
- **Seventeen** cross-process station/first-placement image pairs plus twelve
  repeats exact. Three zooms, lighting on/off and first-placement readiness/state.
  Representative zoom-0.5 image inspected.
- Read-only review finds no source blocker, verifies scope/order/fallback and
  the pinned feather math. No additional agent runtime jobs.
- Final audit passes: normal selected source/UID/test unchanged; 23 frozen scripts,
  only prepared screens differs. Prior 22 reference scripts and existing DLLs
  unchanged. All **19 owner guards**, **11 stable / 11 water binary guards** clean.
  Final protected **2,948-file** fingerprint equals initial/prior baseline. Only
  owner editor PID46624 remains. Existing profile-incident recovery caveat persists.

Engine memory counters: start 2,026.62 MB; end 2,044.11 MB except reverse reference
2,046.11 MB; peak texture counter 2,776.91 MB. These are not native transient/RSS
or long-soak acceptance. No new native code/build/dependencies, Mac package,
playable export, commit or upload.

## Evidence and next action

Evidence `C:/bs-submit-calls-20261015/`; helpers `output/submit-calls-20261015/`.
`submit1-analysis.json`, four timing reports, process guard, native/pixel contexts,
image parity files and `final-audit.json` are authoritative. `reference22.pck`
preserves preceding water candidate; new reference explicitly overlays unchanged
prepared-screen source as file 23. `source-snapshot.json`, `installed-before.json`
and `native-snapshot.json` record current identities. Copied earlier native build
manifests describe original build paths; relocated descriptor hashes are in the
new native snapshot. No existing DLL or source was rebuilt.

Next useful target is compatible **static prop/structural command groups** within
existing room/depth boundaries. First inventory their texture/material transitions
and triangle commands; then prototype one busy room's ordered batching or bounded
atlas, with sampling/memory and pixel checks. Do not spend another large-station
timing cycle on absent specimen effects or assume all live-room cost is animation.
