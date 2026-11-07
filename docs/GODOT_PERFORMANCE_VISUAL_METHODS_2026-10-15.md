# BrineSpace: performance and visual methods

Research completed October 15, 2026. This round covers rendering, lighting,
perspective, effects and simulation/physics. Recommendations combine the current
source with primary Godot documentation and the pinned 4.7.2 engine source
(`ed1daf0bf001b61586d9930840f2f1394092c079`). **No game changes, Godot runs or new
performance measurements were made.** Estimated savings would be speculation.

## Recommendations

The most promising direction is to remove repeated preparation of unchanged data,
then spend any recovered frame time on a small number of meaningful visual effects.
The current overhead/cutaway presentation already supports more depth without a
camera conversion or a general physics engine.

| Area | Best next method | Expected benefit to investigate | Appearance and risk |
| --- | --- | --- | --- |
| CPU preparation | Reuse shared station topology and hazard data while its inputs are unchanged | Fewer room scans, temporary arrays and dictionaries | Can preserve behavior; invalidation must respect changes within a frame |
| Atmosphere | Retain the terrain/survey/corridor mask until one of its channels changes | Less image preparation and fewer upload calls | Can preserve pixels; moving lights, silt and clocks remain live |
| Structural hitches | Rebuild affected rock-mesh chunks instead of the entire field | Shorter rebuild bursts during excavation or structural changes | Can preserve pixels; more steady draw calls are the tradeoff |
| Lighting/material depth | One masked task light and a restrained normal map on one machine | Clearer form and operating state | Deliberate visual change; adds GPU work and texture storage |
| Environmental motion | A shared local current affecting nearby silt and anchored plants | More coherent underwater motion | Deliberate visual change; keep it cosmetic and bounded |
| Physics | Keep the existing route/compartment simulation; use bodies only for objects needing physical forces | Avoid unnecessary simulation and integration work | No established benefit from replacing current crew movement with bodies |

These are candidates, not measured bottleneck rankings. First count and time the
specific work. A 60 FPS frame has 16.67 ms available; mean FPS alone does not show
whether zooming or placing a room exceeds that budget.

## What the game already does well

Several frequently recommended techniques are already present:

- [Room lighting](../rooms/whole-room/room_lighting.gd) uses a quarter-resolution
  multiply light map, authored lamp pools/halos and retained wall/contact shading.
- [Marine snow](../scripts/screen_atmosphere.gd) already uses a MultiMesh with
  shader animation. Moving all particles to the GPU would repeat existing work.
- [Underwater visibility](../scripts/underwater_visibility.gd) already supplies
  shafts, caustics, survey memory, local sediment and a bounded light selection.
- [Crew navigation](../scripts/bill_npc.gd) already reuses room geometry and swim
  links. The [main crew loop](../scripts/main.gd) limits normal graph rebuilds to
  one per frame when actors already have graphs. Drone route failures are cached
  against topology changes.
- [Flooding](../scripts/room_flooding.gd) already models connected compartments,
  door apertures, leaks and pumps. Flood/fire updates subdivide large deltas into
  steps of at most 0.1 seconds. That is a substep bound, **not a 10 Hz scheduler**.
- Retained surfaces, wall/floor batching, water-packet work and frond geometry
  reuse are recorded in [current status](CURRENT_STATUS.md). Room-image LOD is an
  existing private QA prototype, not newly proposed production functionality.

Default Medium effects deliberately omit the High screen-reading post-process:
`ScreenAtmosphere._apply()` hides it when its active strengths are all zero.
Medium still has its separate cool tint and underwater effects. The owner's
September feedback favored sharper imagery, less grain, less fringe and less
blue glow. Increasing whole-screen bloom or haze would work against that direction.

## 1. Remove repeated preparation before adding new machinery

### Shared topology and hazards

`BillNPC.topology()` caches its final string, but still walks occupied rooms and
constructs nested keys, type arrays and locked-door cells before a cache hit.
The main crew loop calls it before `actor.update()`, which calls it again.
`FireSafety.refresh()` similarly scans placed rooms; it is called in both paths.
This is concrete duplicated preparation, although its share of frame time is
not yet measured.

Start with call counts, scanned-room counts and elapsed time around these exact
operations. If material, prepare common room facts once per unchanged simulation
phase and let actors retain their individual graph/clearance state. Preserve
standalone actor-update callers. A single frame-number cache is insufficient if
an earlier actor changes a door, fire or room before the next actor updates.

Full revision-based invalidation can follow only after enumerating room placement,
rotation, locks, ports, branch ownership, Moonbay state, layout loads and restore
paths. Initial layout queries can change the layout revision, so preserve that
query order. This is a targeted change, not a reason to split `main.gd`.

### Atmosphere mask retention

`UnderwaterVisibility.draw()` clears and repopulates the mask, scans wrecks,
surveyed water and corridors, then calls `ImageTexture.update()` on every draw.
Its mask is only **40 × 40 RGBA8: 6,400 bytes**. This is a candidate for removing
repeated scans/API work, not another large-atlas bandwidth diagnosis.

Retain the result while blocking terrain, survey membership, corridor occupancy
and corridor exterior-light levels are unchanged. Light-level fades must still
invalidate the blue channel; checking only a power boolean would freeze a fade.
Continue updating live light positions, camera-based selection, clocks, silt and
effect settings. Avoid replacing the work with an equally expensive full-state
comparison. Rebuild/upload counts and exact images should establish the result.

### Flood swim membership

`RoomFlooding.advance()` reconstructs the shared swim-cell dictionary after every
substep. Its membership depends on crossing the HIGH threshold and on room
footprints; continuously changing water below a threshold need not rebuild it.
Profile this separately from the already cached adjacency pairs. A later sparse
active-component update might help large stations, but must include leaking,
pumped and door-connected rooms. Keep all water transfers, oxygen and survival
updates exact; do not drop small flows with a new epsilon.

## 2. Reduce structural rebuild bursts without undoing batching

[TerrainContentCanvas.submit()](../scripts/terrain_content_canvas.gd) builds a
global rock/connectivity key. Any change rebuilds both whole-field meshes through
[RockSurfaceBatch.build()](../scripts/rock_surface_batch.gd), including polygon
triangulation. This gives few steady submissions but a potentially larger
structural rebuild.

If a placement/excavation trace attributes a hitch here, prototype spatial chunks
and update the changed chunk plus affected connectivity neighbors. Keep identical
world coordinates, UVs and edge generation. Draw **all backing chunks before all
textured chunks**, followed by the existing overlays; drawing a complete backing/
texture pair per chunk could change compositing at boundaries. Retain unchanged
commands rather than forcing redraws. Godot's custom draw commands are already
cached until redraw is requested. [Custom drawing documentation](https://docs.godotengine.org/en/4.7/tutorials/2d/custom_drawing_in_2d.html)

The acceptance question is whether smaller rebuild spikes outweigh additional
steady draws. Check chunk boundaries during mining/reveal, close and fitted zoom,
and sustained frame time. Do not replace a successful batch merely because
chunking sounds more scalable.

MultiMesh is useful for a proven group sharing geometry/material and compatible
ordering. It is not a universal replacement for the foundation renderer: shadows,
fascia, supports and sediment have interleaved transparency. MultiMesh also culls
the group as a unit, so large groups may need spatial partitioning.
[MultiMesh guidance](https://docs.godotengine.org/en/4.7/tutorials/performance/using_multimesh.html)
Pinned GLES source still treats individual mesh/polygon commands as batch breaks.
[Canvas batching source](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/rasterizer_canvas_gles3.cpp#L1061)

A narrow native geometry kernel is another later option if profiling still finds
water-stroke arithmetic expensive after the accepted packet work. GDExtension
would add Windows/macOS binaries, boundary overhead and floating-point parity
risks. Require identical packed outputs before image comparison. Rewriting scene
ownership around RenderingServer is similarly unjustified without measured node
management overhead. [GDExtension](https://docs.godotengine.org/en/4.7/tutorials/scripting/cpp/index.html)
and [server guidance](https://docs.godotengine.org/en/4.7/tutorials/performance/using_servers.html)

## 3. Improve lighting with selective material response

The strongest visual pilot is one working machine with an authored normal map,
very restrained specular response and one small shadowless task light. A normal
map can suggest surface direction while retaining the accepted color painting.
Godot's CanvasTexture supports normal/specular maps; their visible response
requires Light2D illumination. It does not automatically make existing unshaded
custom materials react to lights. [CanvasTexture documentation](https://docs.godotengine.org/en/4.7/classes/class_canvastexture.html)

Use the light's layer/mask limits to isolate the intended object. Preserve crew,
HUD and neighboring rooms. Review powered/offline and wet/dry states against the
painted highlights, which may conflict with a moving light. Added maps require
storage/uploads; this is a visual enhancement with an explicit cost, not a
performance optimization. A light's virtual height controls normal-map response.
[PointLight2D](https://docs.godotengine.org/en/4.7/classes/class_pointlight2d.html)

For most fixed lamps, refine the existing operation-bound halo/emission layer
first. Godot recommends additive sprites when full lighting is unnecessary; broad
lights cover more pixels and cost more. If a moving beam visibly crosses a solid
wall, try a few local LightOccluder2D segments and one shadowed point light.
Keep existing short contact shadows. DirectionalLight2D shadows are infinitely
long, so they are a poor replacement for those contact shadows. Start without
expensive soft-shadow filtering. [2D lighting and shadows](https://docs.godotengine.org/en/4.7/tutorials/2d/2d_lights_and_shadows.html)

This should make operation and shape clearer at ordinary gameplay size. Tiny
reflective details visible only in a close crop are a weak reason to spend the
large station's frame budget.

## 4. Make underwater motion coherent and bounded

Plants, silt, wakes and mining dust already move. A useful enhancement would make
nearby effects respond to the same small current: an airlock pulse or passing
drone gently displaces local sediment and nearby fronds, then decays. Keep roots
fixed, use a few bounded analytic impulses or cosmetic spring states, and isolate
cosmetic randomness from gameplay RNG. Navigation, collision and resource delivery
remain unchanged. Respect Reduced Motion and pause/speed behavior.

For a dense effect whose CPU update actually proves expensive, compare one pooled,
capped GPUParticles2D emitter against the existing method. Marine snow already
uses GPU animation. Moving small formula-driven populations to GPU particles is
not a guaranteed win, and transparent overdraw remains. Validate fixed seed,
lifetime, bounds, teardown and visual cadence. Compatibility has limitations:
manual `emit_particle()`, sub-emitters and trails are not generally interchangeable
with the other renderers. [GPUParticles2D documentation](https://docs.godotengine.org/en/4.7/classes/class_gpuparticles2d.html)
and [pinned GLES particle implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/storage/particles_storage.cpp#L391)

## 5. Preserve perspective; add depth within the accepted view

The current [visual bible, section 4](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md#4-camera-scale-and-composition)
and [station-props contract](STATION_PROPS_V2_2026-09-25.md) govern: overhead/cutaway,
visible tops, shallow front depth, and one painted facing while room positions
rotate. An older four-wall-facing pipeline reference does not supersede this.

Lighting, contact separation and coherent motion can add depth within that view.
Very slow parallax confined to distant exterior decoration is a possible later
pilot; atmosphere particles already have depth motion. Keep station geometry,
selection/picking and crew registration fixed. Godot has Parallax2D, but choosing
its motion strength and layers is an art decision, not an FPS remedy.
[Parallax2D](https://docs.godotengine.org/en/4.7/classes/class_parallax2d.html)

A 3D or isometric conversion would require new facing, occlusion, picking and
interaction decisions, with no established performance advantage here. It is a
separate design project rather than a prerequisite for early access.

## 6. Use physics where the object needs physics

Crew are currently RefCounted actors with explicit routing and swept clearance;
drones use grid routes and phase timers. These are already lightweight data
models. RigidBody2D is appropriate for future loose debris needing force,
collision and sleeping. CharacterBody2D is for prescribed movement, and Area2D
for overlap detection. None supplies room-service routing, breath decisions,
contact animation or resource rules. A physics-body migration has no demonstrated
benefit for this game. [Physics introduction](https://docs.godotengine.org/en/4.7/tutorials/physics/physics_introduction.html)

Fixed-tick gameplay plus render interpolation is a possible pacing experiment,
but not a project-setting fix. Current gameplay advances from scaled variable
delta in `_process()`. The engine cannot automatically interpolate arbitrary
RefCounted foot positions drawn by custom code: previous/current presentation
state would need explicit handling. Fixed 60 Hz could increase updates when
rendering is slower; lowering gameplay frequency can change hazards, traffic and
contact timing. Preserve accumulated simulation time, update order, pause/speed,
save/restore and gameplay RNG, and assess presentation delay.
[Using physics interpolation](https://docs.godotengine.org/en/4.7/tutorials/physics/interpolation/using_physics_interpolation.html)

Compartment flooding is well matched to station decisions. Full fluid simulation
or a body/joint per frond adds a different problem to solve without evidence that
it improves the intended gameplay or frame budget.

## Renderer features: avoid misleading shortcuts

| Suggestion | What applies to this game |
| --- | --- |
| Enable 2D MSAA | Documented only for Mobile/Forward+. It does not repair internal sprite-alpha edges, font rendering or procedural shader aliasing. Keep accepted local card treatment. [2D antialiasing](https://docs.godotengine.org/en/4.7/tutorials/2d/2d_antialiasing.html) |
| Enable FSR / lower 3D render scale | Godot's 3D scaling does not scale this 2D canvas. A lower-resolution world SubViewport is possible, but changes sampling and adds a pass; keep the HUD native and test only if pixel work is the bottleneck. [Resolution scaling](https://docs.godotengine.org/en/4.7/tutorials/3d/resolution_scaling.html) |
| Enable HDR 2D and glow in OpenGL | The documented HDR/glow 2D workflow targets Mobile/Forward+. Pinned GLES has a float render-target path, but that alone does not establish matching linear-light/glow behavior. No supported-workflow or parity claim follows from the flag. [Glow in 2D](https://docs.godotengine.org/en/4.7/tutorials/3d/environment_and_post_processing.html#using-glow-in-2d), [GLES targets](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/storage/texture_storage.cpp#L2554) |
| Add mipmaps/compression everywhere | Mipmaps can improve distant texture stability but add storage; lossy compression changes pixels. Selective visual pilots must preserve the runtime-PNG loading contract. Imported compression is not automatically applied to raw Image-to-ImageTexture loads. [Image importing](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_images.html) |
| Switch renderer for free speed/quality | Existing comparison did not establish strict image parity or clean comparative timings. Production remains Compatibility/OpenGL. [Comparison evidence](GODOT_RENDERER_COMPARISON_2026-10-15.md) |

## Small experiments worth doing next

1. **Measure repeated preparation.** Add scoped counters/timings for topology,
   hazard scans, atmosphere-mask rebuild/upload and full rock-mesh rebuilds. Use
   one frozen large station and report normal play, zoom and placement separately.
   Optimize one proven cost at a time; compare exact state and pixels.
2. **Try one machine-light study.** Keep it behind a reversible comparison flag,
   with one material/light and no shadows initially. Compare all four room
   rotations, fitted/mid/close zoom, power transitions and blackouts. Owner visual
   review establishes quality; benchmark incremental CPU/GPU/frame-time cost.
3. **Try one local current interaction.** A passing drone or airlock pulse affects
   nearby sediment and anchored fronds only. Compare readability, effect bounds,
   Reduced Motion, pause, speed changes and teardown before expanding it.

For performance acceptance, record frame-time distribution, p95/p99, maximum and
frames over 16.67/33.33 ms, plus event-aligned hitch windows. Check uploads, draws
and memory so a saving in one place does not hide a regression elsewhere. Validate
Windows and a real Mac separately; results from this Windows GPU are not Mac
evidence. Keep actual playable-release checks separate from editor/private QA.

No benchmark was resumed during this research round. After the owner subsequently
confirmed other sessions paused, the clean `pacing3` comparison completed; see
the [results](GODOT_RENDERER_COMPARISON_2026-10-15.md) and
[updated handoff](GODOT_RENDERER_HANDOFF_2026-10-15.md). No renderer switch was accepted.
Future tests must use scratch APPDATA and before/after fingerprints of the owner's
real save folder. This research round only read source and wrote documentation
and a source-download helper; it did not access or run against the player's save.

## Evidence scope

Code references describe the shared working tree inspected on October 15, not a
new frozen release acceptance. Parallel research covered lighting/effects,
rendering/perspective and simulation/physics; no branch ran Godot or edited game
code. The [earlier engine audit](GODOT_FOLLOWUP_RESEARCH_2026-10-15.md) retains the
memory-counter, tracing and private LOD caveats; none establishes new FPS gains.

Additional pinned viewport sources are archived at
`C:/bs-render-methods-20261015/source/`; their SHA-256 provenance is in
`C:/bs-render-methods-20261015/source-provenance.json`. The fetch helper is
`output/godot-research2-20261015/fetch_viewport.py`. These files are research
evidence, not shipped resources or a replacement engine build.
