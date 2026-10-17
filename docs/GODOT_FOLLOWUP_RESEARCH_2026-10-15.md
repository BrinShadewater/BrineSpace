# Godot follow-up research — October 15, 2026

Research while independent character sessions occupy the GPU. This adds source-level
findings to the [first research round](GODOT_RESEARCH_2026-10-15.md) and
[renderer comparison](GODOT_RENDERER_COMPARISON_2026-10-15.md). The research phase
started no Godot process, benchmark, trace or installation and changed no engine or
gameplay code. Afterwards the standing renderer comparison resumed during a process
gap; another art test contaminated Mobile and the series stopped. Both `pacing1`
and the incomplete `pacing2` remain excluded from accepted three-way performance
results. Clean renderer timings remain pending.

## Decisions this research supports

Keep OpenGL as the control. Mobile's image differences need isolation before any
switch; ANGLE's tiny differences are not evidence of broken artwork. Investigate
placement/zoom with a short correlated thread/GPU trace before assuming shader
compilation. Treat engine memory counters as bookkeeping, not physical residency.
There is no newly demonstrated FPS improvement in this research.

## 1. A concrete Compatibility memory-accounting error

Two independent source reviews found an error in the pinned Godot **4.7.2** creation
path. An unmipped image has zero extra mip levels; GLES initialization adds one to
represent its base level, then passes that integer to a **boolean** image-size
argument. The size estimator consequently includes a complete mip chain. Utilities
records that estimate before upload. Upload corrects the texture object's byte count
but does not reconcile Utilities' separate counter.
[Creation/upload source](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/storage/texture_storage.cpp#L1039),
[boolean parameter](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/core/io/image.h#L400),
[size calculation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/core/io/image.cpp#L2871),
[separate bookkeeping](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/storage/utilities.h#L130).

`ImageTexture.create_from_image()` does not automatically perform a later update.
Explicit `ImageTexture.update()` does reconcile this counter; freeing removes the
original cached estimate. Thus this is over-reporting while a texture is alive,
not evidence of a persistent allocation leak or extra mip levels actually uploaded.
[ImageTexture lifecycle](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/scene/resources/image_texture.cpp#L58),
[update reconciliation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/storage/texture_storage.cpp#L1283).

The earlier [atlas trial](DRONE_GPU_REBUILD_TRIAL_2026-10-14.md) recorded a
137.8125 MiB unmipped payload adding 183.75 MiB to the engine counter—almost exactly
the full-chain ratio predicted by this error. This corroborates the mechanism,
but a dedicated runtime reproduction is still required. It does **not** establish
actual driver-resident memory, explain every backend difference, or reverse the
rejected GPU-rebuild trial's measured CPU/performance regression.

Deferred minimal reproduction, static scene and retained 1024×1024 RGBA8 image:

| Stage | Source prediction for global texture counter |
| --- | ---: |
| Create without mipmaps | +5,592,404 bytes, versus 4,194,304 actual image bytes |
| Update with the identical image | −1,398,100 bytes, with dimensions/mips unchanged |
| Release and drain rendering | Return to baseline |
| Genuine-mipmap control | Creation/update should agree |

Also compare per-texture debug usage, which reads the corrected object size. Do not
divide the entire historical GL counter by 4/3: imported mipmapped textures, render
targets, format conversions and buffers have different accounting paths. No upstream
issue was filed; focused searches found no directly matching report, which does not
prove none exists.

Compatibility includes renderbuffer storage in its texture counter; Mobile obtains
texture/buffer/total figures from RenderingDevice, whose total also covers other
allocations. Record all three metrics rather than treating texture bytes as total
VRAM. [GLES counters](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/storage/utilities.cpp#L439),
[RD counters](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/servers/rendering/renderer_rd/storage_rd/utilities.cpp#L298),
[documented scopes](https://docs.godotengine.org/en/4.7/classes/class_renderingserver.html#enum-renderingserver-renderinginfo).
Windows additionally assigns changing per-process video-memory budgets; exceeding
that budget can cause penalties even without exhausting the card's advertised VRAM.
DXGI budget queries describe the calling process, so an unrelated helper's result
must not be labeled BrineSpace's usage. Neither paging nor budget exhaustion has been
demonstrated here. [Budget contract](https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/ns-dxgi1_4-dxgi_query_video_memory_info),
[process scope](https://learn.microsoft.com/en-us/windows/desktop/api/dxgi1_4/nn-dxgi1_4-idxgiadapter3).

## 2. Image differences: stronger suspects, no established cause

Final captures have matching complete saved state, clocks, camera and visual sidecar.
Independent GL processes match exactly. ANGLE's maximum difference is 1/255 in all
six cases. In Mobile's fitted station region, only **698 of 1,285,200 pixels** differ
by more than 16/255; 31 exceed 64/255. The HUD maximum is 6/255. Large maxima should
not be described as the whole picture being broken.

The strongest shader candidates are the sine/fract hash in
`scripts/underwater_fog.gdshader:27`, similar wear noise in
`scripts/derelict_material.gdshader:8`, and narrow water/meniscus thresholds in the
flood shaders. Small backend arithmetic or sampling differences can be amplified
by those operations. Exact clocks eliminate time drift, not arithmetic differences.
This is a mechanism hypothesis, not attribution of the captured pixels.
[Related upstream procedural-noise report](https://github.com/godotengine/godot/issues/67150).

Avoid two unsupported explanations: Godot documents shader precision as `highp` by
default; and our captured `use_hdr_2d` is false on all three backends. The RD canvas
color path conditions HDR handling on the target, so “Mobile always uses linear
2D” does not establish the cause. [Precision contract](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shading_language.html#precision),
[pinned RD canvas](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/servers/rendering/renderer_rd/renderer_canvas_render_rd.cpp#L672).

The private LOD adds transparent SubViewport rendering and another sampling step.
At `.25`, its `.24/.28` hysteresis means activity depends on the preceding view.
Record actual cache activity rather than inferring it from zoom alone. Next visual
isolations: compare LOD off/on within each backend; isolate fog and derelict passes;
then compare a shader-free opaque/translucent pattern directly and through one
transparent viewport. Read capture textures only outside timed frames. These tests
distinguish procedural math, offscreen sampling and final blending without changing
the delivery renderer or accepting a looser appearance gate.

## 3. Shader compilation counters have a backend trap

Mobile's `Performance.PIPELINE_COMPILATIONS_CANVAS` is reachable in the actual
release runtime. The RD canvas requests its first-use pipeline with waiting enabled.
Its cumulative counter records a new **request**, not compile duration or completion.
[Release forwarding](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/main/performance.cpp#L266),
[canvas request](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/servers/rendering/renderer_rd/renderer_canvas_render_rd.cpp#L441),
[request counting](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/servers/rendering/renderer_rd/pipeline_hash_map_rd.h#L109).

The pinned GLES implementation returns **zero unconditionally**. Both OpenGL and
ANGLE therefore need an “unsupported” label; zero cannot exclude compilation.
Use `CANVAS`, rather than only `DRAW`/`SURFACE`, for this 2D investigation.
[GLES implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/rasterizer_canvas_gles3.h#L350).
Godot's pipeline-precompilation remedies apply to Mobile/Forward+, and Canvas still
has first-draw work. Resource preload is not equivalent to drawing each variant.
A fresh scratch APPDATA also does not guarantee a cold driver cache; do not clear
global caches on the owner's machine. [Pipeline documentation](https://docs.godotengine.org/en/stable/tutorials/performance/pipeline_compilations.html).

## 4. A smaller, more informative hitch capture

After the GPU is clear, retain the planned clean three-backend pacing comparison.
For attribution, add one short OpenGL placement/zoom sequence and warmed repetitions
with existing frame/action, simulation, Grid redraw and upload start/end/byte markers.
Pair it with a brief Windows trace and an uncaptured control to bound overhead.

| Observation | What it establishes |
| --- | --- |
| Main thread executing during a long navigation/Grid marker | Application CPU work |
| Long texture-creation call | API allocation/driver/upload-call cost; not completed GPU transfer time |
| Mobile canvas-counter increase at first use | A pipeline request; correlation still needs attribution |
| Thread ready but not scheduled | Scheduling contention |
| Thread waiting near graphics/presentation | Blocking; GPU/driver/present evidence must explain why |

WPR/WPA can separate sampled execution from precise running/ready/waiting intervals
and correlate GPU activity. Check the selected profile actually records needed stacks
and has the required capture capability. Use bounded recording; inspect lost events.
Only `wpr.exe` was found on PATH locally; missing WPA/PresentMon/RenderDoc commands
on PATH do not prove those tools are uninstalled. No capture was started.
[CPU analysis](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/cpu-analysis),
[WPA graph scopes](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/list-of-wpa-graphs),
[bounded WPR recording](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/logging-mode).

Official Godot binaries omit debug symbols. Thread states, modules/offsets and
symbolized Windows frames can still help, but named Godot/GDScript/NVIDIA internals
are not guaranteed. A newly built same-commit binary's PDB does not symbolize the
official executable. Treat any symbol-enabled engine as a separate diagnostic build.
[Godot symbol policy](https://docs.godotengine.org/en/4.7/engine_details/development/compiling/introduction_to_the_buildsystem.html#debugging-symbols),
[WPA symbols](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/symbol-support).

PresentMon supplements presentation timing but documents unavailable
`CPUFramePacingStall` and less accurate CPU timing on common OpenGL/Vulkan paths.
RenderDoc belongs in a separate resource/submission investigation, not the baseline
pacing measurement; call-stack resolution also needs symbols.
[PresentMon limitations](https://github.com/GameTechDev/PresentMon),
[RenderDoc call stacks](https://github.com/baldurk/renderdoc/blob/v1.46/docs/how/how_capture_callstack.rst).

## 5. Private LOD admission issue

The capture-event journal in `private-large_room_canvas.gd:247–253` has no capacity,
trim, reader or reset in the inspected eighteen-file cohort and 25 fixtures. It can
grow with continuing captures, at most one entry per process frame accepting a capture. This is
metadata, not retained image payload; no measured size/timing impact or normal-source
leak is established. Remove, disable or bound it before extended endurance admission.

The inspected LOD capture paths use `UPDATE_ONCE` and draw ViewportTexture directly;
they do not call `get_image()`. Therefore GPU-to-CPU screenshot readback is not an
established LOD zoom cost. The benchmark's final screenshot occurs after timed phases.
Keep future image readbacks and RenderDoc captures separate from pacing samples.

## Evidence and next work

Eight pinned source files plus URL/SHA256 provenance are archived in
`C:/bs-godot-research2-20261015/`; helper scripts are in
`output/godot-research2-20261015/`. Source findings received independent review.
Deferred: memory-counter reproduction, pass/LOD image isolation, clean pacing and
OS-trace attribution. Mac and target-hardware release acceptance remain open.
No previous rejected optimization is reinstated by this research.
