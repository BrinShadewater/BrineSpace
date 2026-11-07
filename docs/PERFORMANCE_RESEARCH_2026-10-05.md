# Performance research and shadow prototype

Updated: October 5, 2026 · BrineSpace PC/Mac readiness

## Objective and acceptance

Turn the measured rendering/memory/stall problems into implementable remedies.
Preserve selected pixels, timing, layouts and default quality. A microfixture
result is not gameplay or release acceptance.

## Accepted decisions and constraints

Keep Godot 4.7.2 Compatibility, runtime PNG loading and frozen release packages.
No compression/downscaling, engine upgrade, public upload or owner-data edits.
Do not repeat general profiling before testing a specific remedy.

## Research findings

1. **Explicit shadow geometry batching is the first implementation target.**
   Exact local engine revision ed1daf0bf confirms that each polygon command starts
   a new batch (`rasterizer_canvas_gles3.cpp:1091`); mesh commands also start new
   batches. `StyleBoxFlat::draw` submits its generated vertices through a triangle
   array (`style_box_flat.cpp:646`). Our equipment shadows use three StyleBoxes per
   foot, plus projected geometry. Existing caches save preparation, not those draw
   submissions. Concatenating ordered triangles, with per-vertex colours, can
   preserve alpha order and edge geometry in one command. Cache the resulting
   geometry using layout/footprint state; avoid generating it every frame.
   [Pinned renderer source](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/rasterizer_canvas_gles3.cpp)
   and [pinned StyleBox source](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/scene/resources/style_box_flat.cpp).

2. **Do not substitute primitive draws or regroup translucent shapes by colour.**
   The exact renderer packs primitive colours into half floats; the polygon path
   differs. Reordering overlapping alpha changes pixels. The proposed batch must
   retain original primitive order, transforms and colour precision. A textured
   snapshot cache would introduce resampling at fractional zoom and extra memory,
   making it a poor first remedy under current constraints.

3. **PNG file compression is not a GPU-memory fix.** Godot documents that lossless
   and lossy disk compression do not reduce the GPU's uncompressed texture storage.
   VRAM compression changes that tradeoff but is outside the selected quality
   constraints. Our 18 drone atlases were recently used, so forcibly enforcing a
   smaller cache is not justified. The next memory candidate is bounded residency
   for inactive crew states, retaining frame-object identity and full-size original
   images. It requires explicit visible/transition pins and preparation before
   use; this is a proposal, not a demonstrated saving. Do not repeat rejected UV
   remapping/cropping experiments without a new remedy for their pixel differences.
   [Godot image import guidance](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)
   and [ImageTexture allocation/update contract](https://docs.godotengine.org/en/stable/classes/class_imagetexture.html).

4. **No verified ready-made Windows stall remedy found.** A targeted issue search
   did not establish a matching fix. Microsoft documents that PeekMessage can
   dispatch sent messages and internal events within the call; its name does not
   mean an observed wait is impossible. This supports keeping OS message processing
   separate from game rendering, but does not identify the external cause. The
   earlier screen-reader-cache patch failed the native control and remains rejected.
   Kernel tracing is still blocked by the host's profiling permission. Do not
   disable accessibility or replace the message pump based on speculation.
   [Microsoft PeekMessage contract](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-peekmessagew).

## Current state and verification

Experimental files: `output/shadow-batch-research-2026-10-05/probe.gd`, `run.py`,
`results.json`, `run.log`, `owner-check.json`, and reference/candidate PNGs.
No game runtime files changed in this research pass.

The restricted geometry prototype reproduces the engine's borderless, equal-radius
StyleBox shapes at detail 6 and AA size 1. It draws three overlapping footprints,
three contact bands each, in their original order. Initial corner scaling was
incorrect; after correcting the no-overflow case, the final native run reports:

- **24/24 byte-exact viewport images.** Four scales (0.5, 0.73, 1, 1.25), two
  offsets (0 and 0.5), three light levels (0, 0.5, 1).
- **9 draw calls become 1** in every comparison.
- Zero engine errors; all **2,936 owner non-log files unchanged**.
- The runner checks the resolved isolated profile before any fixture writes.

This is a contact-band proof, not a full StyleBox replacement. It does not cover
room-hull clipping, tiny adapted radii, Retina/text oversampling, projected shadows,
or actual room layouts. It has no measured gameplay FPS benefit yet.

## Next action

Implement a narrow cached equipment-shadow batch that appends projected and contact
geometry in the existing per-foot order. Preserve an exact reference path. Cover
clipping, corner footprints, fractional positions/zoom, lighting and display scale
before enabling it. Attribute its actual floor-pass draw reduction, then compare
three matched active-gameplay runs per path. Reject or revise if pixels differ or
frame pacing does not improve. Terrain is the next render target if this fails to
produce a worthwhile gain; memory residency remains a separate implementation.

All prior release failures remain open. Native Mac testing, signing/notarization
and Windows OS-level stall attribution are not solved by this prototype.

## Continued research: display scaling and residency

The exact engine's CanvasItem redraw callback supplies the viewport's effective
oversampling to StyleBoxFlat. Its AA feather width is divided by that value.
Therefore a shadow mesh cache must include effective oversampling and invalidate
on display-scale changes, in addition to footprint/layout changes. Hardcoding a
one-unit feather would change the existing appearance at higher display scales.
Node oversampling overrides also need accounting; node scale is not automatically
the same thing as viewport oversampling.
[Pinned CanvasItem implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/scene/main/canvas_item.cpp)
and [Viewport properties](https://docs.godotengine.org/en/stable/classes/class_viewport.html#class-viewport-property-oversampling-override).

Extended isolated experiment: `output/shadow-scale-research-2026-10-05/`, generated
by `output/shadow-batch-research-2026-10-05/extend_research.py`. The final run uses
`oversampling_override=1/2` and a corresponding AA-width calculation. **48/48
images match byte-for-byte; every case retains 9-to-1 draw reduction.** No engine
errors and all 2,936 owner non-log files unchanged. An initial fixture incorrectly
assigned the boolean `oversampling` property; its 24/48 result is not valid doubled
oversampling evidence. The corrected final run supersedes it. This Windows
viewport test is not native Retina certification. Clipping and tiny footprints
remain outside the prototype's supported cases.

Memory source review narrows the proposal:

- `crew_texture_pool.gd` already uses weak lookup references, and the grid clears
  startup lookups. Clearing that cache again cannot free textures still owned by
  animation wrappers. The residency change must address those owners.
- `crew_texture_batch.gd` currently materializes surviving frames before gameplay.
  Preserve that readiness contract; any later eviction requires reacquisition
  guarantees rather than missing frames or changed animation timing.
- CanvasTexture separates frame identity/filtering from diffuse image storage.
  It provides a potential attachment point for residency, not proof that unloading
  is safe. Immutable shared images must never be overwritten in place.
- `crew_life.gd` reads banks directly and builds reversed/concatenated sequences.
  Instrumenting only the player's primary frame selector would miss consumers.
  Pins must include portraits, previews, current/transition frames and retained
  canvas commands, and shared images must remain until every consumer releases them.
- Decode/prefetch can be bounded independently, but GPU creation/update on worker
  threads can still synchronize and stall. Do not assume a thread removes upload
  cost. Track readiness misses and upload-time tails at 4x before accepting eviction.
- Keeping all decoded pixels in CPU RAM merely moves pressure on an 8 GB unified-
  memory Mac. Include CPU retention and peak memory in the design; no saving is
  claimed until the complete working set is measured.
- Texture arrays alone are not compression: they contain separate same-sized
  images. They also change the sampling path, so are not a shortcut around the
  earlier atlas-remapping parity failures.

Sources: [CanvasTexture contract](https://docs.godotengine.org/en/stable/classes/class_canvastexture.html),
[thread/GPU synchronization guidance](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html),
[Texture2DArray storage model](https://docs.godotengine.org/en/stable/classes/class_texture2darray.html).

Decision: shadow batching remains the first implementation candidate. Memory
residency needs a consumer/pinning prototype before any eviction is enabled; it is
not a one-line cache-limit change. No further broad profiling or engine upgrade is
justified by this research. No runtime source or frozen package changed.

## Terrain research and implementation ranking

Further source inspection finds that `rock_view.draw_into` walks the whole field
and submits polygons into the shared retained terrain canvas. Retention avoids
rebuilding commands every frame, but does not remove their rendering submissions.
The room and derelict paths already have culling; do not assume terrain has the
same coverage. The measured terrain layer also includes wrecks and glow plants,
so its 798 calls cannot all be attributed to rocks without further separation.

**A second pixel-preserving candidate is now demonstrated.** The mineral surface
is submitted even when every vertex's smoothstep alpha is zero. An experimental
copy skips only that draw after calculating the original grade; texture loading,
all other drawing, cell order and excavation behavior stay the same. Final native
test: **16/16 images byte-exact**, across two cell sizes (16 and 24.3), integer/
half-pixel offsets, nearest/linear filtering and idle/active excavation. Draw calls
are **333 to 297** idle and **337 to 301** active: **36 fewer** per tested render.
This is approximately 11% of this isolated rock fixture's calls, not whole-game
FPS or terrain-layer savings. All 2,936 owner non-log files unchanged; final run
has zero engine errors. An initial PackedColorArray API error was corrected before
the successful run. Runtime source remains unchanged.

Evidence: `output/terrain-research-2026-10-05/` contains generator, copied candidate,
guarded native fixture, results, profile check and reference/candidate PNGs. The
fixture uses `WreckField.initial()` and the actual selected terrain textures.

| Priority | Candidate | Evidence / expected scope | Effort and remaining risk |
|---|---|---|---|
| 1 | Ordered equipment-shadow geometry batch | 48 exact microcomparisons, 9 calls to 1 | Medium: full-room clipping, tiny radii, effective DPI, invalidation and active gameplay |
| 2 | Skip zero-alpha mineral overlay polygons | 16 exact terrain comparisons, 36 fewer calls | Low: integrate, regression and matched gameplay; bounded modest saving |
| 3 | Retained terrain chunks with conservative bounds | Full-field source path, 798 calls for combined terrain layer | Medium: camera/zoom edge coverage, neighboring rock masks, excavation/reveal invalidation; benefit unmeasured |
| 4 | Merge compatible terrain polygon commands within chunks | Polygon submissions break engine batching | Medium/high: exact triangle/UV arithmetic and transparency order; no texture-based reorder across overlaps |
| 5 | Inactive animation GPU residency | Existing ownership audit; weak caches already cleared | High: every consumer must pin, all transitions ready, bounded upload latency and unified-memory peak |

Chunk proposal: retain separate CanvasItems for bounded world regions, calculate
draw bounds including cliff edges, outlines and effects, and rebuild only dirty
chunks. A cleared rock also invalidates neighbor connectivity and any newly exposed
buried site. Keep active work effects separate if needed without changing order.
Do not cull navigation, needs, production or discovery. Compare pan/zoom and
excavation workloads, including cameras crossing chunk boundaries. Do not choose
a chunk size from intuition alone: compare a small fixed set with the same scene.

MultiMesh is not the first terrain remedy: visibility applies to the entire group,
and Compatibility packs per-instance colour/custom data differently from full
precision paths. It may help repeated same-mesh props later, but arbitrary rock
geometry and translucent ordering favor explicit indexed batches first.
[Godot MultiMesh visibility guidance](https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html)
and [MultiMesh reference](https://docs.godotengine.org/en/stable/classes/class_multimesh.html).
The optimization guide flags its version coverage as incomplete; the current
class contract and local exact engine source remain the implementation authority.

Decision: enough research now exists for the first two scoped changes. Further
general searches have lower value than integrating those candidates and obtaining
matched gameplay results. No renderer upgrade, global quality reduction, monolith
rewrite or automatic quality switching proposed. Windows OS stalls and native Mac
certification remain independent release blockers.
