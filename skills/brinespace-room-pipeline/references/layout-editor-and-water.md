# Layout editor and water-rendering lessons



Recorded September 8, 2026. These are local native checks, not packaged acceptance.



## Tray asset pipeline

Use the registered silhouette to render each prop into a transparent SubViewport.

Never show a rectangular source-sheet AtlasTexture while the clipped preview loads.

Reserve a transparent fixed-size slot to avoid row jumps; use selection outlines

rather than an opaque block behind the artwork. Keep source art and registration

unchanged when the defect belongs to thumbnail presentation. Test actual alpha

and inspect the native tray: alpha alone does not prove a correct cutout.

Process pending thumbnails with a finite queue; preserve room/rotation identity

across asynchronous completion and drain jobs safely on editor close.



## Editing and performance workflow

Free placement defaults on; preserve explicit saved preferences. Empty left-drag

pans, Shift-drag selects a box, and clicking floor decorations selects their layer.

Entryway areas controls clearance guides; Clean preview hides editing overlays.

Free authoring does not establish playable doorway or crew-route clearance.



Translations may reuse current props, but resizing, variants and membership edits

need the complete refresh. Compare geometry, sorting, undo and rendered pixels

against the full path. Convert logical canvas bounds through the viewport stretch

transform before cropping screenshots; exclude asynchronous tray updates.

Report CPU update cost separately from render-inclusive cost and startup time.

The 40-added-prop fixture measured 0.933 to 0.058 ms update time; rendering remained

about 6.06 ms and startup about 0.9 seconds. This is not a 94% frame-rate gain.



## Water graphics

Retain readable water heights, restrained irregular surface patterns and broken

crew wakes; avoid the previously rejected net-like pattern and circular blue halo.

Leak variants must communicate their different rates and retain repair feedback.

Rendering caches must not freeze live door aperture used by physics or input.

Culling must leave room for tall props, risers and actors at viewport edges.

The 49-room fixture improved from 64.418 to 44.584 ms flooded median frame time;

it excludes crew AI/campaign progression and still exceeds the 60 fps budget.



## Evidence and continuation

Project records: docs/LAYOUT_CONTROLS_2026-09-08.md,

docs/LAYOUT_EDITOR_POLISH_2026-09-08.md, docs/DENSE_STATION_POLISH_2026-09-08.md,

and docs/FLOOD_SAFETY_AND_SCALE_2026-09-08.md. Use CURRENT_STATUS for newer decisions.

Editor checks: tests/test_layout_workflow.gd and tests/test_layout_performance_guards.gd.

No new image generation or asset-batch rerun is needed for a documentation closeout.



## Saved-layout parity and corner clearance — September 9



Treat omitted free-placement flags like Studio's default-on setting. Runtime directional guards must not silently shrink or move near-wall saved equipment; retain explicit constrained checks and detached stale-layout fallback. Compare every rotation's actual editor/runtime prop rectangles, not just JSON keys. The owner requested larger equipment and fewer small floor props; current saved layouts supersede older generic size advice.



Open corner consoles need separate normalized collision rectangles for their arms, scaled and mirrored with the rendered prop. A single image bounding box blocked BRINE's north approach despite a visible empty notch. Production crew graph checks now pass with the saved layout and recovery pod. See `docs/PREFERRED_LAYOUTS_2026-09-09.md`; graph reachability is distinct from a full animated tour.



September 9 density correction: owner wants 3–4 large assets per room, not many enlarged props. Keep the defining equipment and remove secondary filler. Count a multi-piece fitted bank as one visual asset; preserve sparse rooms rather than adding filler to reach three. Back up and reconcile personal overrides when an explicit owner correction removes previously saved props. Evidence: `docs/LARGE_ASSET_LAYOUTS_2026-09-09.md`.


## Native performance evidence — September 21

Verify the rendered subject before interpreting a performance capture. Record visible
room-center counts at the start and end of room profiling and inspect the screenshot;
an empty viewport can produce misleadingly good timings. Supply the destination to
`_set_grid_zoom` itself: its deferred restore can overwrite a subsequent immediate
scroll correction. An irregular station's bounding-box midpoint may be empty, so a
close-room fixture should target an occupied cell. These are fixture requirements,
not permission to change the owner's layout or player camera behavior.

Attribute render layers before optimizing. Floor passes include equipment shadows;
already-batched tile meshes were not the dominant cost in the September 21 fixture.
Keep translucent triangle order, prop footprint registration, clipping and rounded
contact edges intact when batching shadows. Native pixel comparisons must cover
multiple light levels/scales and overlaps. Forced-draw profiling is not ordinary
play FPS; do not infer drone performance from a run with zero active-drone frames.
See docs/PERFORMANCE_BASELINE_2026-09-21.md for bounded results and limitations.

A populated fixture is not necessarily operating: drone bays require a paid economy
cycle. Use `_apply_room_economy()` and verify the bay in `powered_room_cells` before
expecting launch; do not inject power flags or remove dispatch rules to pass a test.
Record observed flight phases and construction-induced room-count changes. A phase
counter proves simulation activity, not that the drone is visible or well animated.

A per-prop cache stamp validates survivors, not collection completeness. Store the
last applied prop count as well; partial/empty removal must reapply saved library
furniture, while unchanged calls keep their serial and explicit saved deletions
remain deleted. test_layout_cache_removal.gd covers those distinct cases. This is
a correctness guard, not evidence of a frame-rate gain.

Projected shadow geometry cache keys must include effective footprint and visual
rise. Lighting color remains dynamic outside the mesh. Bound position-dependent
caches for Studio dragging, test movement/height/eviction, and preserve native
image parity. Isolated geometry speedups do not establish station FPS.

Split wall asset IDs identify artwork, not necessarily Studio layouts. Seven rooms
save under room-<room_id> while their split-wall helper previously read <name>-wall.
Keep layout_asset_id separate from asset_id; configure it from the editor catalog.
Regression coverage must apply a catalog-key override, repeat setup, rotate away
and back, and verify both prop presence and selected layout metadata. A clear route
through the wrong/default furniture is not proof that owner edits were loaded.

Single-wall helpers also need catalog layout keys independent of art IDs. Check
rotation-specific post-placement code: Medical Office/Center restored deleted
legacy stations after the main layout pass. Retained furniture must read the same
key and respect null deletions. Include deletion assertions, not only added-prop
presence, in repeated/rotation tests. Non-wall views may apply on render, so empty
setup-time metadata alone is not a missing-layout bug.

After changing layout selection, verify grid.bill_room_geometry as well as room
rendering. It explicitly applies non-wall layouts before drawing; wall helpers
must already have applied theirs. Validate saved additions/deletions in snapshots
without interpreting that as full route or activity acceptance.


September 23 Studio corrections: register effective surface details after saved
furniture has been applied. Host-relative details may not exist when defaults are
first enumerated; missing draft coordinates broke selection. A deleted detail
must not respawn beside a fallback host. Verify click, delete, undo and reload.
Movable equipment must render at its saved picking rectangle: the Airlock's north
locker variant formerly drew at a fixed riser position. Defer walking-preview
navigation reconstruction during drag/resize and resume on release. Isolated
preview CPU savings do not establish long-session frame-rate acceptance.
The September 23 cleanup protected 19 rooms and cleared 84 secondary rotations.
On September 24 the owner finished eight more rooms, bringing protection to 27
(all rotations). Use the current list in docs/CURRENT_STATUS.md; never reapply
the old cleanup to newly completed rooms. Historical evidence remains in
docs/STUDIO_OWNER_DECORATION_FIXES_2026-09-23.md.
