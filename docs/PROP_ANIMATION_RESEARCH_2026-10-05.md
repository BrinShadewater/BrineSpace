# Room prop and animation research

Updated: October 5, 2026 · BrineSpace

## Objective and acceptance

Review animation and room-prop work for avoidable overhead without changing pixels,
timing, layering or owner layouts. This pass is source research, not a measured
gameplay improvement or runtime patch.

## Accepted decisions and constraints

Keep selected animation frames and reference identities. Preserve procedural motion,
crew/prop occlusion, flood shading and rotation. Do not replace custom rendering
with AnimatedSprite2D, atlases or a global animation-rate cap without evidence.
Godot already retains custom drawing commands until redraw is requested; retention
saves command rebuilding, not the GPU work of displaying those commands.
[Godot custom drawing](https://docs.godotengine.org/en/4.5/tutorials/2d/custom_drawing_in_2d.html).

## Current state

### 1. Split-prop wrapper identity can defeat static retention

**October 5 native follow-up: not a default gameplay defect.** The original
hypothesis below missed `_sorted_content_queue` pre-expanding and retaining the
wrappers. The direct-call reproduction bypassed that cache. Default-path native
verification now passes 181 checks; the proposed runtime fix was removed. See
[corrected finding and scope](SPLIT_PROP_RETENTION_2026-10-05.md). Historical
candidate discussion below does not supersede this result.

In `scripts/room_content_canvas.gd`, `expanded_prop_entries()` makes fresh shallow
wrapper dictionaries for `prop_base`, `prop_effects` and `prop_pass`. The cheap-key
path compares `is_same(slot.item,item)`. It compensates for fresh wrappers only for
`library_base`/`library_live`, by comparing kind and underlying prop identity.
Consequently the other expanded wrappers enter the changed path on resubmission,
even when their underlying prop and static state are unchanged. A static base can
therefore queue another redraw. This applies when the cheap-key path is enabled
and the view does not advertise `props_rebuilt_each_configure`.

Examples of renderers exposing `draw_prop_base` include whole-room life support,
hydroponics, med bay and crew hab. This is not automatically every frame: unchanged
eligible rooms bypass submit via `advance_live`. Rooms containing actors and several
special room types are excluded from that bypass in `_room_setup_skippable`.
Actual selected props may use the already-correct library branch, so measure
affected slot counts before estimating a station-wide saving.

Candidate: use stable underlying prop identity plus kind and pass method/live
classification for expanded wrappers, retaining the existing static/layout key.
Verify repeated unchanged submit, movement, copies, rotation, layout replacement,
crew crossing and changed pass methods. Do not compare prop ID alone: copies and
shared renderer instances make it insufficient.

### 2. Large-room layout caching is not per-prop render retention

`rooms/large-rooms/studio_view.gd::live_props` caches prepared props by room type,
rotation and Store revision. It does not rebuild the owner's layout every draw.
However, dry `draw_live` creates a PaintContext and calls `draw_props`, which loops
over all non-hidden props and calls Library.draw. That loop has no per-prop viewport
culling or static/live slot split. Flooded equipment follows a separate node path
and must be evaluated separately. Do not conflate this with smaller rooms, where
`room_content_canvas` already provides slots, conservative bounds and static bodies.

Candidate: bring compatible per-prop retention to the large-room path, then use
complete visual bounds for culling. Preserve its existing order and crew rendering;
do not impose a new sort order or use footprint-only bounds. Measure dry/flooded
large rooms separately, with props partially offscreen, moved/deleted props,
pan/zoom, doors, tidal rotation and crew crossing. Cache scope and invalidation
must include layout changes and scene lifetime.

### 3. Live does not always mean different pixels

`advance_live` redraws every visible live slot. Library screen/effect functions set
their local time to zero for reduced motion, yet the slot remains classified live.
Some `prop_effects` slots are always live even when their renderer returns early
because machinery is not operating. These give narrowly defined unchanged-output
cases to investigate. Keep reduced motion an explicit user choice.

Many effects genuinely vary continuously: radar sweeps, waveforms, specimen motes
and holograms use time-dependent geometry. A blanket lower redraw rate changes
their appearance. A safe output key must cover operating state, authored frame,
material, geometry, water, layout, transform and relevant preferences. Shader
uniform updates can still be needed when drawing commands are retained.

Holograms also rebuild arrays and evaluate constant angular samples repeatedly.
Precomputed invariant samples may save CPU, but benefit and floating-point parity
need measurement. Do not migrate to shaders as an assumed improvement.

### 4. Character frame selection is a smaller CPU hypothesis

`crew_sprite_player.gd` already caches authored cycle duration, while frame selection
walks duration arrays. Bill's `_human_frame_index` additionally sums durations per
call. Cumulative timing tables or same-clip cursors are candidates only if profiling
shows material cost. Preserve nonuniform durations, equipment timing, loop edges,
non-loop final frames, interrupted transitions and distance-driven movement.
Never suppress simulation or animation state progression merely because rendering
is culled. No evidence here attributes the large memory budget to frame lookup.

Large-room `common.gd::sprite` also caches uploaded textures; its PNG decoding,
grading and optional wall-bank resizing occur on a cache miss, not every draw.
First-use preparation remains a loading concern; blaming continuous PNG decoding
in that function would be incorrect.

## Verification

Read grid setup/retention, room-content submission/painting, large-room layout and
drawing, library effects, representative split renderers, and crew timing code.
No Godot process launched, no owner-profile writes, no runtime edits. Findings are
source-confirmed mechanisms with unmeasured frequency/cost, not visual acceptance.
Changed this report and CURRENT_STATUS.md only during this research pass.

## Next action

First reproduce expanded-wrapper redraw counts with an isolated native fixture,
including a real affected renderer and selected library-prop control. Then compare
the narrow identity fix with pixel and rebuild-count checks. Profile large-room
prop submission next. These are more concrete than reducing animation quality;
existing shadow, terrain and blocked-route candidates remain on the implementation
queue. Packaged matched workloads must establish any actual frame-time benefit.
