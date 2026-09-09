# Floor coverage and integration lessons

## Evidence from September 8, 2026

The first v6 integration reached all 43 live room views but still reused one neutral floor grain and generic material layouts. This was consumer coverage, not completion of distinct floors and details for every room. Do not equate a populated asset library, a shared draw call, or a rebaked card count with per-room art acceptance.

Use tools/audit_floor_coverage.gd to resolve current live identities, the actual inherited floor method, and current machinery footprint IDs. Its runtime.json is a read-only inventory. A subclass can implement draw_room_floor merely to call super and add furniture; find the underlying material call before editing. Full-wall replacements can change host IDs and available floor area.

rooms/floor-profiles-v1/rooms.json records one row per live room, department, independent condition, source and hash, machinery snapshot, and separate floor/detail stages. Keep these stages honest. A profile added to JSON is not proof it was used at runtime or seen in a native render.

## Material rules

Preserve the 48-unit construction module and 72-unit apertures. Visible material panels may span multiple modules. When a source already contains panel seams, do not blindly superimpose the generic floor grid: that creates competing grids. Map surface artwork onto authoritative floor geometry; material never owns openings or collision. BRINE's floor stays dark enough to support its bright chamber even when its material source is pale.

Pass the room view explicitly to a profile-aware floor helper. Avoid global mutable current-room state, which can leak between card, preview and station consumers. Keep legacy helper behavior available for diagnostic fixtures that have no registered production profile.

## Detail acceptance requirements

Anchor equipment entries, mats, drainage and handling marks to actual machinery/activity areas, including all rotations and current full-wall replacements. A coordinate safe in an old composition is not automatically safe in the current one. Randomly distributing every library variation is not the goal. Record a reason for unused pieces, and create missing art only after the per-room brief identifies a functional gap.

Validate true alpha, native reading scale, source-dependent pixel density, furniture occlusion, condition appropriateness, and service endpoint continuity. Source alpha repairs and clean replacements are different outcomes; preserve and label originals. The 384-pixel transparent v6 exports use a center anchor at (192,192); smaller submitted UV regions must still include each piece's actual extent.

## Reproduction and limits

Use tests/review_floor_profiles.gd for full-catalog native rotation renders; inspect rendered images, not just exit status. The older inherited harness repeated powered corridor rendering across its state loop; the final v3 fixture now passes actual power values. Preserve the older evidence limitation. Use the isolated-save station fixtures for native zoom and doorway behavior. Rebake selected cards to a new output directory with tools/bake_floor_kit_cards.gd -- --output-dir=res://assets/<revision>/cards, then update the selected mapping and hashes.

At the earlier material checkpoint, department materials were installed and the 43-room native render run passed. The first attempt caught a transient shared-renderer compile state; its failure was preserved, current code reinspected and a fresh run used for evidence. The later follow-up below completes machinery-specific detailing and full-set floor/detail visual review. Standalone-package acceptance remains separate. See docs/FLOOR_COVERAGE_2026-09-08.md for final evidence and limits.

For denser floor tiling, repeat the source at a smaller physical size instead of
adding a second seam grid. The natural-layout pass repeats department sheets twice
per axis. Preserve door and construction dimensions; inspect both repeat joins and
furnished gameplay scale, then refresh the current card mapping across the catalog.


## Machinery-anchored details and visibility (September 8 follow-up)

Author a functional purpose and actual host IDs per room in rooms/floor-profiles-v1/rooms.json. Details.resolve uses the current rotated host footprints, visible artwork envelopes, existing registered floor pads, protected port routes and separation from other details. Pressure Control needs explicit alternative host IDs because its zero-degree composition uses baked perimeter assemblies. Tight layouts may have explicit rotation overrides for scale or stand-off; do not silently relax route/occlusion checks to make the count pass. Linear drains run along the equipment edge; service entries point outward.

A geometry-only audit initially placed 320 detail instances but native before/after pixel comparison found 25 completely hidden. Artwork envelopes and existing pads must be considered separately from collision footprints. After that correction, 12 were still hidden by later floor drawing. The correct production order is floor material, room-specific pads/routes, final flush floor overlays, then upright props and crew. The shared draw_floor_overlays hook now applies this order to both full-room and floor-only station passes. Do not move the overlay above furniture just to make it visible.

Run tests/audit_floor_detail_anchors.gd for all hosts/rotations, with a missing-host negative control that also checks cache invalidation. Cached placements must be invalidated by actual geometry, visual bounds, floor pads and authored detail specifications, not just room ID. Run tests/test_floor_detail_visibility.gd for paired native frames: its separate process toggles only new details and checks changed pixels inside every resolved ink region. The corrected run checks 320 placements with none hidden. A pixel-change test establishes visible contribution, not artistic quality; still inspect the contact sheets and live station.

The existing equipment pad beneath a bench is different from an operator footing in front of it. Preserve authored pads and avoid overlapping them with a second mat. Keep registered UV extents and physical scale explicit when fitting compact spaces. Sources did not need regeneration for this pass; the missing work was composition and drawing order.

The native review now supplies real powered/unpowered corridor values, correcting the historical repeated-powered loop. Earlier reports retain that limitation; do not retroactively upgrade their evidence. Use the new revision paths in tools/review_floor_contact_sheets.gd and tests/review_floor_profiles.gd, preserve previous exports, and update selected card mappings only after the new bake succeeds.
