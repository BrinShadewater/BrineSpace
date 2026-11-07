# BrineSpace: Godot performance, rendering and migration research

Research checked October 15, 2026. Scope: performance and pacing, text and rendering
glitches, alternative Godot renderers/drivers, engine upgrades and a possible engine
migration. Research only: no runtime, renderer, asset or save changes in this task.

## Findings and recommendation

The evidence points to several separate problems. Godot's handling of our many 2D
polygon/mesh commands is a confirmed engine limitation. Large runtime texture uploads
and synchronous structural work are demonstrated BrineSpace costs. Card sampling is
a demonstrated visual problem with an accepted local remedy. The Q-like zero and the
extra portion of the historical 128 ms placement event remain unconfirmed/unexplained.
There is no evidence of a single engine bug explaining everything.

**Recommended next experiment: compare rendering drivers and Mobile on the same Godot
4.7.2 build in isolation, with visual gates, before another round of small CPU changes.**
Keep current Compatibility as the control. This tests a potentially larger source of
CPU/driver cost while preserving the option to retain the present renderer. It is a
proposal; no renderer switch has been accepted or performed.

## What our measurements establish

Latest [environment comparison](ENVIRONMENT_GEOMETRY_HANDOFF_2026-10-15.md): 3,840
frames / 16 exact gameplay-camera pairs on Windows, RTX 4070 Ti, 1920x1080. Candidate
normal-speed idle is 18.688–18.946 ms, or 52.8–53.5 FPS. Idle p95 is about 21.0–21.1 ms;
all 16 mean/p95 60 FPS phase gates fail. Roughly 2.0–2.3 ms must leave the mean idle
frame to reach 16.67 ms; its p95 needs a larger improvement. Mixed 1x/4x workloads
average 21.7–21.9 ms. These are different metrics, not interchangeable FPS claims.

About 2,131 calls/frame and 4.8 ms delayed render-CPU samples remain. These are measured
costs in this workload, not a universal Godot draw-call limit. Nested script timers,
render CPU, GPU and present intervals overlap; subtracting render CPU from total frame
time does not yield a reliable "remaining script time."

**The frozen QA baseline includes the private room-image prototype.** The same baseline
is present in both comparison lanes, so the measured patch deltas remain useful. It
does not establish current delivery performance or certify the normal source without
that prototype. The Windows delivery predates subsequent source optimizations. Native
Mac and target-hardware release acceptance remain open.

## Engine limitations versus application costs

| Area | Finding | Confidence and consequence |
|---|---|---|
| Individual polygon/mesh drawing | Both Compatibility and RenderingDevice canvas rendering explicitly start new batches for these commands. | Confirmed in our pinned engine; retaining commands or sharing one mesh does not merge submissions. |
| Procedural live-room/environment drawing | Recent ordered packets and shared frond edges reduce actual work while preserving pixels. | Confirmed locally; remaining CPU work is game-specific and still worth targeting. |
| Drone stalls | Completed worker images can trigger large main-thread texture creation/upload bursts. | Confirmed association with measured API intervals; API duration is not an exact GPU execution breakdown. |
| Placement/removal | Navigation and visible-layer rebuilds perform substantial synchronous work. | Repeatable and partly reduced; no-upload placement events prove uploads are not the sole cause. |
| Card text and angled strokes | Small text and rotated-line sampling improved with the accepted card-specific changes. | Confirmed visual remedy; the original Q-like zero was not reproduced. |
| Black openings in large-room doors | The backing color was the near-black default; large rooms now supply their threshold floor color. | Application drawing choice, fixed and tested; no demonstrated renderer defect. |

### Why caching and a faster graphics card have not solved this

The pinned GLES3 renderer forces a new batch for a polygon and for a mesh. The pinned
RenderingDevice 2D renderer, used by Mobile/Forward+, does the same. This explains why
retaining geometry saves preparation yet still leaves submission work. It also explains
why our ordered float triangle packets have helped. Faster GPU shading alone does not
remove CPU-side command handling. [Pinned Compatibility implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/rasterizer_canvas_gles3.cpp),
[pinned RenderingDevice implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/servers/rendering/renderer_rd/renderer_canvas_render_rd.cpp#L2387).

Upstream [issue #117312](https://github.com/godotengine/godot/issues/117312), opened
March 11, 2026, remains open and classified as discussion/documentation. It reproduces
the same-mesh behavior in Compatibility and Mobile on macOS; explicit MultiMesh reduces
the example's ten calls to one. That supports the limitation, not an imminent fix.
MultiMesh is a candidate for genuinely repeated compatible geometry; its individual
instances lack independent screen/frustum culling. Alpha order, transforms and materials
still need our native checks. [MultiMesh constraints](https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html).

### Texture uploads: fewer bytes or allocations did not guarantee smoother frames

Our [upload attribution](DRONE_UPLOAD_EXTERIOR_PROFILE_2026-10-14.md) captured a 116 ms
frame alongside two mining-body uploads totaling 275.625 MiB and about 50.5 ms in
image-creation API calls. Earlier worker-stage evidence found those decoded images
already complete. More decoder threads would not remove this demonstrated upload cost.

The documented `ImageTexture.update()` optimization reuses an existing allocation with
matching dimensions, format and mipmap configuration; it still replaces image data.
Our allocation-reuse trial was slower, so the generic API advice is insufficient for
this workload. [ImageTexture contract](https://docs.godotengine.org/en/stable/classes/class_imagetexture.html#class-imagetexture-method-update).

Likewise, our [GPU reconstruction trial](DRONE_GPU_REBUILD_TRIAL_2026-10-14.md) preserved
pixels and halved one transfer, but added target creation/backing and regressed timing.
Larger-cache, crop and prewarm experiments also have recorded rejections. Do not revive
them unchanged based on a general optimization tip.

Partial texture updating is still an open upstream proposal/PR, not a released
`ImageTexture.update_region()` remedy: [proposal #13012](https://github.com/godotengine/godot-proposals/issues/13012),
[PR #109985](https://github.com/godotengine/godot/pull/109985). Even a future partial API
would not automatically solve first allocation, original-size residency, readiness or
retained consumers. A custom transfer implementation would be a separate substantial
prototype. `RenderingDevice` is unavailable in Compatibility, so examples using its
low-level APIs cannot simply be inserted into our present renderer.
[RenderingDevice availability](https://docs.godotengine.org/en/stable/classes/class_renderingdevice.html).

### Pacing has multiple causes

The [placement investigation](PLACEMENT_PACING_HANDOFF_2026-10-15.md) reproduced a
76.5 ms placement frame with synchronous navigation/simulation and roughly 34 ms of
drawing. The historical 128 ms event had no sampled drone upload. Its extra slowdown
remains unresolved; a texture remedy cannot explain every event.

Shader compilation is another possible first-use cost, but is not established as the
cause of these repeated upload or structural events. Godot's modern pipeline remedies
apply to Forward+/Mobile; the documentation still identifies Canvas compilation at
first 2D draw. A switch therefore does not guarantee shader-stutter elimination for
this game. [Pipeline compilation documentation](https://docs.godotengine.org/en/stable/tutorials/performance/pipeline_compilations.html).

Window composition, refresh/VSync and driver scheduling are separate presentation
questions. Test equal-size windowed/exclusive-fullscreen modes and controlled VSync/VRR
after measuring raw work. These settings cannot recover CPU work already over budget.
[Godot pacing guidance](https://docs.godotengine.org/en/stable/tutorials/rendering/jitter_stutter.html).
For unexplained events, align the existing markers with OS thread/present traces.
[PresentMon](https://github.com/GameTechDev/PresentMon) supports OpenGL/Vulkan, but
documents less accurate CPU frame timing and unavailable CPUFramePacingStall for those
paths; a zero counter is not proof that no wait occurred. Pair it with thread-stack
sampling rather than treating it as a complete attribution tool.

Do not conflate decoder workers, Godot's separate render thread and NVIDIA's driver
threaded optimization. Our separate-render-thread trial crashed before gameplay;
Godot documents known bugs and synchronization stalls in GPU/resource operations.
[Thread-safe API guidance](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html).
On Windows, Godot defaults to disabling NVIDIA driver threaded optimization because
of known OpenGL stuttering; blindly enabling it is not a supported remedy.
[Setting documentation](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html#class-projectsettings-property-rendering-gl-compatibility-nvidia-disable-threaded-optimization).

## Text, thin lines and precision

Keep the accepted [card fix](CARD_READABILITY_HANDOFF_2026-10-14.md): a separate
medium-weight, non-MSDF face, 2x oversampling, mipmaps, larger text, thicker interior
strokes and appropriate turned-card filtering. Small font hinting and distance-field
tradeoffs support testing this choice locally; a blanket global MSDF change is not a
demonstrated cure. [Font guidance](https://docs.godotengine.org/en/4.7/tutorials/ui/gui_using_fonts.html).
The frame overlapping the colored border is intentional draw order, not an engine issue.

Two related open reports warrant regression fixtures, not attribution:

- [#119504](https://github.com/godotengine/godot/issues/119504): disappearing one-pixel,
  non-AA diagonal lines in 4.6.2, macOS M1 Compatibility. Check our tilted cards on Mac;
  it does not prove the Windows issue had the same cause. [2D antialiasing guidance](https://docs.godotengine.org/en/4.7/tutorials/2d/2d_antialiasing.html).
- [#117338](https://github.com/godotengine/godot/issues/117338): tiny nearest-filtered
  raster-font spacing in 4.5/4.6.1 with Forward+. It is not a reproduced 4.7.2
  Compatibility defect in our larger Barlow card text. Capture actual `0 O Q` glyphs
  at production sizes if the original zero symptom returns.

Older fixes already included in our engine are not upgrade opportunities:
[text shadow/outline batching #103471](https://github.com/godotengine/godot/pull/103471)
merged for 4.5; [#114200](https://github.com/godotengine/godot/pull/114200) concerns
editor resampling and merged for 4.6. [MSDF outline issue #110126](https://github.com/godotengine/godot/issues/110126)
is closed with a 4.5 milestone.

Our exact-pixel constraint makes representation changes consequential. ArrayMesh packs
colors into bytes, whereas the canvas polygon path keeps float colors. Converting
existing translucent float polygons can change alpha. Existing mesh artwork should
keep its selected quantization. [Packing source](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/rendering/rendering_server.cpp#L708),
[mesh attributes](https://github.com/godotengine/godot/blob/4.7.2-stable/drivers/gles3/storage/mesh_storage.cpp#L951).
Cropping a texture also changes physical sampling; our rejected atlas trials establish
pixel differences, not a proven universal driver-quantization explanation. Original
UVs/dimensions and inherited shader inputs remain part of acceptance.
[Canvas shader contract](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/canvas_item_shader.html),
[local sampling evidence](ATLAS_SAMPLING_AND_INDEXED_WHEEL_2026-10-10.md).

## Renderer and engine decisions

The [official archive](https://godotengine.org/download/archive/) currently lists
4.7.2 stable, released August 18, 2026; 4.8 is a development series. Our build already
matches the [4.7.2 release](https://godotengine.org/article/maintenance-release-godot-4-7-2/).
There is no newer stable upgrade established here as a remedy. The CanvasRD
instance-data/VBO optimization in [PR #112481](https://github.com/godotengine/godot/pull/112481)
landed for 4.6 and is already included. Its advertised gains cannot be counted again.

| Option | What it could change | Decision |
|---|---|---|
| Current Compatibility/OpenGL | Known appearance and validated optimizations | Keep as control and production default. |
| Compatibility/ANGLE | Different driver translation path while keeping Godot's Compatibility canvas | First bounded comparison if supported by the actual binary. Windows uses D3D11; pinned Mac implementation selects Metal. |
| Mobile/Vulkan on Windows; Mobile/Metal on Mac | RenderingDevice driver/submission behavior | Worth measuring. It retains the polygon/mesh batching restriction and may change pixels/features. |
| Forward+ | Different rendering feature/cost balance | Secondary control; shares the RenderingDevice 2D implementation, so no demonstrated extra batching advantage. |
| 4.8 development build/custom engine | Potential future or bespoke fixes | Research branch only if tied to a specific fix and minimal reproduction. |
| Different engine | Complete replacement of runtime behavior and platform work | No measured evidence justifies the rewrite; require a representative prototype to establish a decisive advantage first. |

Renderer switching can require appearance adjustments. A change must pass our visual
gate, not just boot or report higher FPS. [Renderer comparison and switching guidance](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html).

There is a documentation inconsistency worth recording: stable ProjectSettings describes
macOS ANGLE over native OpenGL, but **our pinned 4.7.2 implementation requests Metal**,
matching the compilation guide. Binary support is conditional and fallback is possible.
Requesting a driver does not prove it ran. [Pinned ANGLE source](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/platform/macos/gl_manager_macos_angle.mm#L45),
[driver settings](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html#class-projectsettings-property-rendering-gl-compatibility-driver),
[macOS compilation guide](https://docs.godotengine.org/en/latest/engine_details/development/compiling/compiling_for_macos.html#compiling-with-angle-support).

Mac must be tested directly. Several accepted circle/surface/border packet paths are
Windows-gated and retain original drawing elsewhere. Windows timings cannot establish
Mac call counts, visual parity or performance. Check actual platform/OS support against
the [engine system requirements](https://docs.godotengine.org/en/stable/about/system_requirements.html).

## Concrete next investigation

1. **Freeze the exact experiment.** Separate a normal-source release candidate from
   the private LOD experiment; retain the same code/assets/settings within each pair.
   Reuse scratch profiles and save fingerprints. Record actual renderer, driver,
   adapter, OS and fallback messages from the running executable.
2. **Run a bounded backend comparison.** Windows: current native GL, ANGLE/D3D11 if
   available, then Mobile/Vulkan. Mac: current supported control, ANGLE/Metal if
   available, then Mobile/Metal. Use the same station, resolution, clock/quality,
   idle/pan/zoom/light changes and structural actions, both orders. A silent fallback
   invalidates that comparison. Keep first-use and warmed timing distinct.
3. **Apply visual and lifetime gates.** Compare cards, doors, floors, transparent
   overlaps, fog, flood shaders, animated rooms, atlas frame edges and texture-wrapper
   lifetimes. Inspect every difference; retain the current renderer if the unchanged-
   appearance requirement fails. Test real Mac display scaling and supported hardware.
4. **Classify remaining hitches.** Align upload API events, navigation/rebuild work,
   engine markers and OS thread/present events. Do not assume shader compilation,
   worker decoding or Windows scheduling without a matching trace.
5. **Choose the next implementation from that result.** Continue ordered geometry
   packets for confirmed submission costs; use localized rebuilds for structural
   spikes. A small C++/GDExtension kernel is an option only for a measured arithmetic
   hot path. Faster script/native math does not remove built-in graphics API costs;
   keep byte/pixel tests and cross-platform packaging gates.
   [CPU optimization guidance](https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html).

Mean improvement alone is insufficient: compare p95/p99, >50 ms frames, first-use
spikes, memory peaks, exact gameplay state and image/motion parity. No performance
gain, Mac acceptance or engine-migration result was measured in this research task.
