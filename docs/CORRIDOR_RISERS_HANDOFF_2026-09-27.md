# Corridor riser renewal

Updated: September 27, 2026 · BrineSpace

## Objective and acceptance
Redo hallway, corner and tee risers/art in every direction. Owner clarified the
overlapping door was the corridor door. Visual acceptance of this revision pending.

## Decisions
Muted neutral corridor steel; retain transit, utility and observation identities.
Raise corridor faces from 35 to 60 units and reserve eight units for door headers.
Keep navigation, floors, room rotations and the locked probe installation unchanged.
Owner follow-up: place windows/arrows within empty panel bays and use larger
hallway windows. Cladding and fittings now share bay geometry; transit arrows get
a separate 38-unit bay on wider runs. Short runs reserve their bay for glazing.
Windows use the available bay height; utility service pipes stay below them.

## Current state
New exact generated atlas, prompt, nine registrations, manifest, nine cards and
native evidence: `assets/corridor-risers-v2/`. Shared modular textures cover all
three shapes; geometry determines each face and return in every rotation.
Changed `rooms/underwater/corridor_dressing.gd` (height, returns, window mounts),
`rooms/underwater/corridor_wall_art.gd` (catalog and door fit), and
`scripts/room_card_art.gd` (three default bindings). Original sources preserved.
Review gallery: `assets/room-risers-expansion-v1/corridors/index.html`.
Latest bay-placement pass refreshed all 72 captures and nine cards; all 36 raised
views inspected again, with frames clear of ribs and services. Owner review pending.

## Verification
Isolated native `test_corridor_wall_variants.gd`: pass, 72 raised/low captures,
nine distinct shape/finish combinations, registration bounds and neighbor culling.
All 36 raised captures visually inspected across three contact sheets. Door headers
fit below the cap; inside returns retain the concave vertex. Real profile before/after
fingerprints match. Four locked probe hashes unchanged. New PNG uses Git LFS filter.
Follow-up: isolated live `test_corridor_water_variations.gd` passed nine variants,
36 closing-door captures, pause equality and 36 rotated water-mask checks. All nine
flooded views inspected; three four-pose closing loops added to the gallery.
The initial run failed whole-frame pause equality on the last variant. A diagnostic
run retaining exact equality passed; cause remains unproven. The fixture now saves
the offending frame and door state and exits nonzero on recurrence instead of hanging.
Both runs preserved the owner profile. No executable export tested.
Follow-up files: water-variation test, isolated runner, wet evidence and gallery.

## Next action
Owner review at http://127.0.0.1:8812/corridors/. No commit, push or export.

## Floor and furnishing follow-up
Owner requested dark-grey metal on every hallway connection, bespoke wall art,
new floors, and small/medium props people can walk around. Added exact generated
floor and three-panel sources with prompts/hashes in the same pack. Door skin uses
scoped neutral dark-grey modulation; shared connection selection gives hallway
precedence in either direction. Transit map, pressure panel and marine display
occupy separate bays alongside the large windows. Existing calibrated bench/cart/
crate assets retain native world scale and source pixels.

Changed: door finish selection/renderer, modular floor default, corridor wall art,
12 shipped corridor layout keys, grid corridor prop geometry/depth sorting, and
crew corridor blocker checks. Original corridor layout keys backed up in
`layouts-before-furnishing.json`; owner profile and Studio marks untouched.
Floor props and crew now share depth order. Live navigation sees the same effective
props as rendering and performs exact blocker sweeps for corridor segments.

`test_corridor_furnishing.gd`: 12 rotations pass, every port reachable using the
production standing/segment checks, furniture centers blocked, and hallway door
precedence verified from either room. The refreshed 72 native views/nine cards pass;
all 36 raised views visually inspected. Art bible records the persistent door rule.
Final furnished/depth-sorted live run passes all nine wet variants, 36 closing
captures, pause equality and 36 rotated water masks. Native and live owner-profile
fingerprints match; locked probe hashes unchanged. Gallery and live loops refreshed.

Join cleanup: owner reported pale-blue squares at inside corners and bright wall
outlines. `corridor_surfaces.gd` now textures the hull backing exposed between wall
strips; `corridor_dressing.gd` uses subdued grey edge trim instead of pale strokes.
Fresh 72-view/card capture passes. Corner and tee joins visually checked. No floor
footprint, prop placement, collision or navigation changes in this correction.
Final trim correction: owner rejected the teal line following wall bases. Replaced
the three legacy blue/teal seam colours with neutral charcoal in corridor_dressing.
Fresh 72 native views and nine cards pass; corner inspected. Live motion captures
remain evidence from before this colour-only adjustment and are labelled accordingly.

## Additional hallway riser variations

Owner requested more hallway riser variations. Added reinforced, service and
acoustic materials as IDs 3–5; original IDs 0–2 unchanged. New unmodified generated
atlas and prompt are in alternate-walls.png / alternate-walls-prompt.txt.
Changed registrations.json, corridor_wall_art.gd (six material names, panel bays,
service vent), grid_canvas.gd (full variant for hull), main.gd (six placement
variants per corridor shape), and test_corridor_wall_variants.gd. Gallery, cards,
contact sheets and manifest refreshed.

Checks: 18 registrations / distinct variants and 144 rotated raised/low captures
pass; 36 new raised views visually inspected. Real profile fingerprint unchanged;
new PNG is covered by Git LFS. Earlier live flooding tests cover the original
three finishes only. Remaining: owner visual acceptance of the new finishes.

## Three muted coloured materials

Request: three additional textures and muted hallway colours. Added separate
unmodified sage-wall.png, clay-wall.png and slate-wall.png sources with exact
prompts and source hashes in manifest.json. IDs 6–8 preserve the earlier six.
Changed corridor_wall_art.gd names, main.gd corridor placement counts (nine),
registrations.json and scoped native test totals. Cards and gallery refreshed.
Initial coloured perimeter was rejected during agent review; final low/cap
registrations sample charcoal metal, keeping colour on upright panel bays only.

Validation: 27 distinct shape/finish variants, 216 raised/low rotated captures,
neighbor culling pass; 36 new final raised views visually reviewed. Profile
fingerprints unchanged. New PNGs covered by LFS. Earlier live wet checks remain
limited to original three finishes. Remaining: owner visual acceptance.

## Ocean tunnel variants

Owner requested giant glass sections looking onto the ocean. Added IDs 9–10,
panoramic and pressure-ribbed, using one new unchanged generated ocean window
source with prompt/hash. Whole upright non-entry faces now display the panorama;
short faces crop centrally to preserve scale. Ribbed variant adds structural ribs.
Door apertures, low walls, floor and navigation unchanged. Ocean is static art.

Changed corridor_wall_art.gd, corridor_dressing.gd, registrations.json, main.gd
(11 hallway finishes), scoped native test, cards, gallery and manifest. Test now
compares all raised rotations for uniqueness: north/south straight halls have no
visible glazing face, so q0 alone cannot distinguish glass from matching steel.
Initial q0-only assertion caught that fixture limitation; revised 264-view run
passes with 33 distinct shape/finish combinations. 24 new raised views visually
reviewed; owner profile unchanged. Earlier live wet evidence covers original three
finishes only. Remaining: owner visual acceptance.

## Heavy bulkhead alternate and opposite wall

Owner liked glass direction and requested thicker frames plus matching opposite
walls. Added bulkhead ID 11 using existing ocean/steel art, 8-unit vertical
frames and 5-unit rails. Exposed south non-entry walls in all glass variants
now have 18-unit cutaway glass; shared boundary culling and doorway exclusions
remain in force. Cutaway stays low to preserve aisle visibility.
Changed corridor_wall_art.gd, corridor_dressing.gd, main.gd (12 choices),
registrations.json, native test counts, cards/gallery/manifest. No new raster
generation, collision or save-format changes. 288 raised/low captures pass,
36 updated glass raised views visually checked, real profile unchanged.
Remaining: owner visual acceptance.

## Individual window frames

Owner requested frames around window sections. corridor_wall_art.gd now draws
continuous metal top/bottom rails on every tunnel finish and a recessed dark seal
around every pane, including opposite cutaway panes. Existing heavy uprights
retained. Native 288 captures pass; horizontal heavy corridor visually reviewed.
Cards/contact sheets and gallery refreshed. Owner profile unchanged; visual
acceptance pending.

## Plain hallway floor default

Owner requested removing the old floor pattern and using new tiles. Changed
modular_floor.gd default corridor path to HALL_QUIET (hallway-floor-tiles-v1),
using its 4x4 atlas on 48-unit cells instead of the procedural 24-unit service
lane arrangement. Explicit Studio finishes remain supported; owner files untouched.
Refreshed all cards/contact sheets/gallery. Native 288 captures pass; horizontal
bulkhead corridor visually reviewed; profile unchanged. Owner acceptance pending.

## Correction: use the newly generated steel floor

Owner rejected the plain-floor substitution above. Correct source is
assets/corridor-risers-v2/floor.png from this session. modular_floor.gd now uses
that atlas in authored 8x8 order at 24-unit module scale; removed the old
hall_module centre-lane/border selection algorithm. Preserves explicit Studio
finishes. 288 native captures pass, owner profile unchanged, horizontal bulkhead
view checked. Cards and all gallery contacts refreshed. Prior plain-floor
direction is superseded, not accepted.

## Floor alternatives

Added three generated floor sources/prompts and floor-alternates-manifest.json.
Actual atlas grids: rubber 8, sage 6, bronze 7 per axis; all sampled at 24 world
units. modular_floor.gd registers three picker finishes and supports alternate
atlases through corridor module meshes. Existing default and owner choices stay.
Native fixture/wrapper accept --floor to compare consistent rooms. Each of three
alternates passes 288 rotated raised/low captures; three horizontal bulkhead
views visually reviewed. Owner profile unchanged. Gallery comparison added.
Remaining: owner visual acceptance of materials.

## Consistency fixes

Owner authorized all five audit repairs. Changed corridor_wall_art.gd (uniform
panel samples; glass crops maintain aspect and 60-unit scene scale), modular_floor.gd
(manual tile cells use correct atlas and 24-unit modules; stable finish paths map
to v2 images), survey_probe_art.gd (matte outlet source), native test (48 UV-bound
cases plus glass aspect/scale assertions). Added floor-sage-v2.png,
floor-bronze-v2.png and outlet-matte-v2.png; exact prompts and hashes saved.
Original images and locked launcher preserved. Gallery/cards refreshed.
Four floor runs each pass 288 captures; four explicit outlet views pass; owner
profiles unchanged. Wall/floor comparisons and all outlet orientations visually
reviewed. Source mean luma sage .468→.297, bronze .351→.265. All locked launcher
hashes match. No navigation geometry changed. Remaining: owner visual acceptance.
