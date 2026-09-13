# Galley owner asset repair

Owner requests top-down/inward kitchen equipment and large mess-hall tables.
Current `galley_view.gd` pins rotation 0, selects a frontal kitchen and includes
only kitchen/serving props. Existing south kitchen is overhead but remains a
library companion. Preserve kitchen/serving semantic identities and crew behavior.

Habitation brief: warm wood, cream fitted cabinets, quiet olive upholstery and
matte cookware. Add long communal tables with bench seating, preserve central
entry-to-serving access and cooking/washing work space. No gameplay or character
animation edits. Final table count and dimensions require native crew-scale and
production collision review, not merely fitting the image in empty space.

New table raw source and exact prompt are in `assets/galley-owner-v2`. Source
shows overhead tabletop, two three-pad benches, four bowls, two mugs and shared
bread board. Reference `kitchen-south.png` supplies material/style only. Not yet
selected: alpha cleanup, native fit, kitchen conversion, four rotations, operating
and retained/pause checks, and card refresh remain.

Integration checkpoint: selected overhead south kitchen/serving registrations
are extracted through their original alpha polygons; kitchen turns 180 degrees
for inward north-wall use. Source hashes/crops recorded in equipment-review.json.
Two new 76x160 communal table assemblies occupy opposite sides of a central aisle.
All four props rotate in artwork and bounds. Only obsolete kitchen/serving default
position/size overrides were removed, with backups. Existing semantic IDs and
crew behavior are preserved.

Native `output/galley-owner-repair-2026-09-12/rotated-native` completed with empty
stderr. All four views inspected: overhead surfaces, table gaps, inward kitchen
and clear central circulation. Production collision/segment coverage passes all
176 layouts (`20260912-212921-headless`). This does not establish seated interaction
or crew-scale acceptance. Cooktop state alignment, retained/pause checks, native
crew-scale review and card refresh remain. No export or owner acceptance.

State/scale checkpoint: native furnishing contact confirms source-local cooktop
ring alignment in all four directions. Direct/retained RGB match; off/on and two
powered times differ. Actual station pause fixture completes with zero failures
across four orientations. Evidence is under `furnishing-states` and `station-pause`
in `output/galley-owner-repair-2026-09-12`. Production Bill reference uses unchanged
south sprite, pivot (92,172), standing height 148 and the room's production draw_actor
scale. `crew-scale/direct.png` reviewed: tables read as communal furniture with
clear central circulation. This is scale review, not seated behavior validation.
Card refreshed from reviewed q0. No gameplay/character behavior changed.
