# Balanced full-wall room installations

## Owner correction: brightness and displaced furniture

Pressure Control now retains its complete original installation in every rotation. The new manifold is an unused alternative, not drawn over the old art. Maintenance Bay uses the darker built-in image_gen revision at `assets/full-wall-props-refined-v2/maintenance-repair-wall.png`; its prompt and provenance are recorded alongside it.

Displaced props are offered clear positions at their original size. Placement preserves source offsets and depth sorting, rejects visual/ground overlap, keeps hull containment and an 84-unit doorway approach clear, and omits old service routes that no longer match moved hosts. The relocated lounge lamp has a new direct wall lead. Fixed-coordinate baked wall slices are not moved. Props without a clear position remain in their original view/source; they are not squeezed into an occupied area.

The native relocation audit found 35 distinct room props restored in at least one applicable rotation across 11 room types. Per-rotation moved/unplaced lists are in `output/full-wall-v2/relocations.json`. Updated 15-room/four-rotation native review and final production walking checks passed with zero assertion failures (`output/full-wall-v2/review.log`, `routes.log`). The review also rejects visual overlaps involving relocated props. Updated cards are live in both consumers. These corrections supersede the original integration notes below.

The September 7 owner request replaces paired large furnishings with the approved colorful, softer-lit installations. `manifest.json` maps all 15 room types to their original view and new leaf view. The original sources and views remain available.

`scripts/grid_canvas.gd` uses these views for both room rendering and crew collision geometry. `scripts/room_card_art.gd` and GridCanvas thumbnail mappings use `cards/`. Cards show the default rotation, including original furniture when that rotation only has a free side wall.

## Placement

- Research Lab, Med Bay, Listening Post, Xeno Lab and Isolation Vault: full-width installation in all four rotations. Pressure Control retains its original installation.
- Mycelium Nursery, Crew Lounge, Maintenance Bay, Crew Hab, Bio Lab and Clone Lab: full-width installation at 0/180 degrees; original composition at 90/270 degrees.
- Mining Drone Bay, Ore Refinery and Cryo Chamber: full-width installation at 90/270 degrees; original composition at 0/180 degrees.

Horizontal artwork always faces screen-south. It is not stretched or rotated into side-wall art. Full-width placement occupies a sealed north or south edge; the tallest sources are scaled to leave the 72-unit door lanes clear. A side-only layout retains its original composition instead of miniaturizing the installation. A northern built-in's collision footprint extends back to the wall so crew cannot walk through its rear machinery.

Lower furnishings survive unless replaced or overlapping the new installation. Dressing routes with removed hosts are omitted. Hull geometry, room identity, costs, doors and gameplay definitions are inherited unchanged. Recovered cryo wards bypass this revision entirely, preserving their one/two-pod layouts and recovery rendering. Mining retains its operational vehicle and launch hatch; the robot pictured in the new installation is stationary service equipment.

## Source registration

The approved `assets/full-wall-props-balanced-v1/*.png` are RGB palette sources with baked checkerboards. They remain byte-for-byte unchanged. `tools/register_full_wall_props.py` reads them and writes vector registration only, following the existing source-polygon renderer approach. Edge-connected neutral background and individually reviewed pipe/gantry apertures are excluded by source geometry. The JSON records the source SHA-256 and polygons. It does not claim the PNG itself has alpha. There is no recoloring, raster rewrite, or runtime chroma-key filter.

The new installations are static artwork; existing retained furnishing effects and room lighting remain active. Dedicated animated versions of the new fixtures have not been authored.

## Validation and review

- `tools/review_full_wall_rooms.gd`: 15 rooms x four rotations x powered/offline configurations. Checks installation count, visual bounds and door-lane clearance; verifies live mining vehicle/hatch retention and compares recovered cryo props with the original view for one/two pods in all rotations.
- `tests/playtest_full_wall_rooms.gd`: dedicated actor selection for the existing production-route fixture. Final run passed all 15 rooms and four rotations with zero assertion failures. The original generic fixture initially selected a different architect and failed its Bill precondition; this leaf fixture explicitly selects Bill without changing player preferences or gameplay.
- Godot 4.6.1 native OpenGL captures: `output/full-wall-v1/previews/rooms-installed.png`, four `rooms-q*.png` sheets and 15 default-orientation cards. The installed sheet uses 90 degrees for the three straight-through rooms so every new installation can be compared at full width.
- Connected-station captures and walking traces: `output/full-wall-v1/station-review-v2/`. Final collision verification: `output/full-wall-v1/final-route-check/`, `final-route.log` (zero assertion failures). Earlier station captures precede the final rear-footprint expansion; visible artwork is identical.

Review artifacts and logs live under ignored `output/`, outside the raw-asset export folders. PNG source/card files are covered by the repository's existing Git LFS rule. No player save or gameplay logic was changed.

To rebuild the review and cards:

```text
Godot --path <project> --script res://tools/review_full_wall_rooms.gd
```

To repeat production movement checks, supply a fresh capture directory:

```text
Godot --path <project> --script res://tests/playtest_full_wall_rooms.gd -- --review-rooms=research_lab,med_bay,pressure_control,mycelium_nursery,crew_lounge,mining_drone_bay,ore_refinery,cryo_chamber,listening_post,xeno_lab,maintenance_bay,crew_hab,bio_lab,clone_lab,isolation_vault --capture-dir=res://output/full-wall-v1/new-route-check --route-check-only
```

## September 8 polish pass

Nine room identities now have authored west/east side-wall variants, replacing the
previous side-only fallback. See docs/ROOM_ART_POLISH_2026-09-08.md for selection,
cutout, brightness and test evidence; assets/side-wall-props-v1/generation.json for
exact prompts; cutout-review.json for the current source/hash/aperture ledger.
The earlier notes describing side-only fallback are historical. Pressure Control
and recovered cryo retain their explicitly selected original behavior.

## Approved autumn couch

Owner-approved side palette v5 and its matched horizontal source in
assets/full-wall-props-autumn-v1 now replace the brighter couch in all rotations.
The side views retain straight wall-aligned geometry. Fresh card and native review
are under output/couch-autumn; source prompts/hashes remain with the originals.
The room skill now identifies v5 as the approved reference, synced to installed.

## Active dressing follow-up

Full-wall substitutions now filter active furniture, mats and supported objects
against surviving hosts, retaining complete saved profiles for other rotations.
Catalog host/mat audit: zero errors. Deliberately missing-host control is rejected.
Native full-wall rotation/state and cryo-recovery review passes. Evidence:
output/full-wall-followup/. This removes stale definitions, not source assets.
