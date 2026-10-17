# New room props — production preparation
September 26, 2026.

154 individual static props from 28 room concepts and additional sheets are installed
in the Layout Studio through rooms/station-props-v2/props.json (477 total entries).
Choose Operations, Life Support, Recreation, Anomaly or Robotics; search by room name.
Existing 323 entries and all owner room layouts/marks are preserved. Reopen an already
running game/Studio to reload its cached catalog.

## Files
- index.html: searchable department gallery with actual world-scale zoom and light/dark backgrounds.
- game-size/: installed PNGs, .34 world units per pixel, grouped by originating room.
- masters/: source-resolution transparent cutouts.
- catalog.json: these 154 entries only, with full resource paths, footprint and collision metadata.
- manifest.json: original source, source hash, crop, resize and export hashes.
- cleaned-sheets/ and cleanup-provenance.json: three transparency edits and exact prompts.
- review/: native production-crew scale pages, Studio screenshot, alpha backgrounds and validation.
- animation-studies/: preserved aquarium and four-wall launcher studies with dependencies.
- ocean-reuse/: separate aquatic artwork retained for future exterior use.
- before-install/: untouched catalog and protected owner-data backups.

A copy of exports/masters/review/ocean art is in the organized Desktop collection's
06-production-exports folder. Original sheets and previous revisions remain unchanged.

## Checks and decisions
All 154 exports visually reviewed in native Godot with Bill at the production 65.28
world-unit standing height. Props use the established .34 world units per texture pixel.
Most 1536 sheets export at .60; the larger dome, rear seating and shared computer sheets
have recorded individual normalization factors. These are world-scale decisions, not
claims that source images share an identical painted pixel grid.

Source alpha is preserved inside crop bounds; no global luminance cutoff or halo paint.
Bounds derive from each substantial alpha body plus three pixels, excluding remote
transparent residue that previously inflated footprints. Small console replacements
supersede five sheet consoles. Mats have no collision or contact shadow. Ordinary
equipment uses the existing station-family front-60% collision convention and a lower
55% floor footprint; these are conservative floor registrations, not exact per-leg meshes.

Native fixture: 616 single-prop/quarter checks, zero failures, crew walking area and
perimeter routes available. All 154 appear in their Studio department; placement tested
from each of five departments. 188 existing authored layouts retain valid keys.
Original 323 catalog records compare equal; six protected files hash-identical.

Aquarium: 48-second exact loop join; 3 swimmers, 6 plants, 2 coral clusters; all layer
toggles pass, no browser errors. Four-wall bay: loaded/empty/returned states and exact
13-second join pass; prelaunch beacon rotates with .8-second period and is off afterward.
The NEWER survey mission is assets/survey-probe-v1-2026-09-26 (do not overwrite it with
the older bay study). Its 52 clips, 960 effect frames and 5,120 path samples pass.

## Furnished prototype integration
Continuation adds 28 single-cell rooms, 112 quarter-specific layouts and 28 baked
room cards. There are now 75 room types. Open furnished.html for the native review;
all original 188 layouts, 323 props and owner Studio marks/layout files are preserved.
The rooms are available in Studio and through the existing Archived Data blueprint shop.
They do not change starting unlocks. Their metal costs and resource rates are provisional.
See rooms/new-room-expansion/definitions.json and docs/NEW_ROOM_EXPANSION_HANDOFF_2026-09-26.md.

The aquarium's 48-second swimmers/plants/habitat now draw inside live tank props.
Station pause freezes its clock; living inhabitants continue during equipment outages.
The survey bay has four fitted launchers and a 32-second local circuit using the newer
mission art. Warning beacon, status LED, launch, empty launcher, scan and return are wired
into the native renderer. Existing survey memory records discoveries. Mission phase lives
in each room's checkpoint; pause, suspension, unavailable power and blocked routes hold it.
The circuit repeats locally rather than planning a route across the whole ocean.

112 furnished views / 17,920 walking samples: zero failures and visual overlaps.
38,512 runtime checks: zero failures. Native captures cover 36 probe states and five
habitat phases. Studio regression passes with 75 room entries. Owner review and balance
playtesting remain separate from these checks. No release/export is claimed.
Directional launcher fittings remain distinct paintings, not an articulated shared hatch.
Ocean sprites are retained for reuse and are not automatically spawned in the sea.

## Rebuild
python tools/prepare_new_room_props.py
python tools/package_new_room_props.py
Native checks: tools/review_new_room_props.gd and tools/verify_new_room_studio.gd.
Animation checks: python tools/verify_new_room_animations.py.
Preparation rebuilds the pack catalog; it deliberately does not rewrite the live
catalog or player layouts. Merge only this pack's stable IDs if revising installed art.


Furnished pipeline: tools/build_new_room_layouts.py generates candidate files; merge only
its new layout keys into defaults. tools/bake_new_room_cards.gd bakes these cards;
tools/review_new_room_gameplay.gd captures an isolated native fixture.
