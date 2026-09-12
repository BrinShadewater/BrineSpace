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
