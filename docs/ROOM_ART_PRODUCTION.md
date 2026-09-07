# Hybrid room art production log

## Complete decoration refresh — 2026-09-06

All 85 unique assets in the five earlier decoration families now have reviewed
style revisions: 79 new revisions plus six accepted wall revisions from the
preceding pass. Replacement packs use `*-style-v2` names; originals remain intact.
Native per-pack previews and an 85-item overview are in `output/art-style-refresh`.
Utility source regions/anchors were re-registered after generation moved items.
A floor drip tray mistakenly became a window in the atlas; that region is rejected
and a separately corrected tray supplies the export. Exact prompts, source/output
hashes, gap cleanup, replacement mapping and coverage ledger accompany the packs.
These remain reusable asset libraries, not newly placed gameplay furnishings.

## Wall decoration style audit — 2026-09-06

Reviewed both everyday decoration batches (24 pieces) against habitation and
corridor room references. `assets/wall-dressing-style-v1` collects eighteen retained
exports and six revisions: clock, comm panel, two posters, mask rack and pressure
gauges. Revisions reduce gloss, emission, rust noise and print texture. Native
1x/2x collection and same-height before/after evidence are included. RGB checkerboard
revision sources required neutral exterior cleanup and reviewed mounting-hole seeds.
This is sprite style acceptance only: prior 48-unit strips are historical mounting
studies and do not override the current low-wall requirement or approve placement.

## Second wall dressing collection — 2026-09-06

`assets/wall-dressing-v2` adds 12 new silhouettes: pressure gauges, station map,
extinguisher, emergency masks, key/tool racks, planter, pennant, fan, beacon,
seashell display and coat hooks. Two interrupted-generation sources were recovered;
ten remaining items were generated separately. Sources, prompts, alpha exports,
hashes and drawing helper are retained. Native sprite and three wall-strip previews
pass mounting and hatch-clearance checks; build checks also reject overlap.
These remain static reusable assets rather than newly functioning room systems.

## Everyday wall dressing — 2026-09-06

`assets/wall-dressing-v1` adds 12 individually generated clocks, comm fixtures,
paper decorations, framed pictures, posters and small station fixtures. Original
RGBA sources and exact prompts are preserved. Alpha below 128 was removed from
exports after faint exterior haze displaced trim bounds. Native 1x/2x and three
wall-strip previews verify rendering and mounting clearance at 18–32-unit heights.
Readouts are decorative: the clock generation shows 08:30 rather than requested
06:30. No gameplay furnishings, timekeeping, comm interaction or lighting systems
are added by this kit.

## Ocean windows and riser attachments — 2026-09-06

`assets/riser-wall-kit-v1` adds five window variants, four hull pieces and three
monitor/display variants. Transparent cutouts preserve the authored ocean behind
the glass. Suggested mounting heights of 24–40 units retain source proportions
within a 48-unit riser. Native sprite and three wall-strip previews check texture
loading, wall bounds and a reserved central hatch bay. Source, prompt, hashes and
Godot drawing helper are included; scenery/readouts are static and gameplay room
placement remains separate.

## Multi-department floor dressing — 2026-09-06

`assets/floor-dressing-v1` adds 16 reusable top-down pieces spanning Engineering,
Medical, Science, Cargo, Operations, Command, Habitation and Cultivation. Each has
placement guidance, suggested scale and floor-only metadata. Native 1x/2x review
caught enclosed white sectors in a double-ring marking; five reviewed cleanup
seeds preserve its negative space. Sources, prompts, alpha cutouts, hashes and
Godot helper remain together. This is an asset kit, not automatic room furnishing.

## Floor utility kit — 2026-09-06

`assets/floor-utilities-v1` supplies 13 top-down floor sprites: wire/cable runs,
bends and junctions; rubber cable-protection mats; paired floor pipes and recessed
service details. Native 1x/2x and joined-deck previews are included. An opaque-black
generation was preserved but rejected for extraction; imagegen prepared a white
revision before the existing neutral-background cleanup. Floor-layer metadata is
explicit, separate from upright utility sprites and navigation behavior.

## Utility decoration kit — 2026-09-06

`assets/utility-kit-v1` contains 20 separate RGBA sprites across pipes, ducts,
flexible tubes, armored power cables and signal wires. Source sheets and prompts,
reviewed extraction regions, alpha-gap seeds, family scales and connector anchors
are preserved. Native Godot gallery and five assemblies are included. Electrical
alpha was preserved; mechanical white backgrounds were cleaned with the existing
pipeline. These are decorative modules, not seamless autotiles or new utility
simulation. No room rollout is implied by this kit's count.

## Airlock hull attachment pass — 2026-09-06

Six independently registered wall/deck fittings now serve the airlock: ocean
window, porthole, pressure controller, manifold, shielded lamp and drain cassette.
Raw generation, actual-alpha findings, repeatable cleanup, wall profile and
dependency manifest are in `rooms/underwater/airlock-v4`. The retained floor-prop
atlas is declared separately. `tools/audit_wall_fittings.py` adds wall-specific
alpha/containment/door-bay checks, separate from navigation and visual review.
Current station/card references use v4; older sources remain. This is one room's
attachment pass, not a new catalog-completion count.

## Active production update

Current count: 18 of 34 identities have normalized PNG candidates. Latest additions:
ore_refinery, maintenance_bay, salvage_drone_bay, life_support, corridor, corner,
crew_hab, crew_lounge and med_bay. Exact generation prompts, source output names
and review flags are saved beside these PNGs as `.provenance.json` files.
Known correction queue: Refinery conveyor obstructs its route; Corridor has false
side-door trim; Corner lacks genuine openings; Lounge has oversized door recesses.
None of these are accepted as finished production assets. Sixteen identities
still lack candidates. The earlier nine-count paragraph below is historical.

Owner authorized deterministic local cleanup and continued full-set production.
`tools/room_art_pipeline.py` now removes only edge-connected neutral light
backgrounds, preserves enclosed bright details, and normalizes aspect-preserving
art into a transparent 1280 square. Three focused Python tests pass. Original
images are retained. Run `python -m unittest discover -s tests -p test_room_art_pipeline.py`.

Nine normalized candidates now exist under `rooms/hybrid/`: reactor,
hydroponics_bay, mining_drone_bay, tidal_condenser, mycelium_nursery,
gravity_loom, battery_array, solar_array and storage_bay. These are not yet
integrated or accepted in-engine. Door alignment and remaining exterior fringe
need visual checks. All 25 other identities remain to be produced; the goal is
the complete 34-identity set, not just this pilot.

Generation for the six additional candidates used the inspected hybrid reactor
as the hull/camera/material reference, with individual subject and door prompts:

- Condenser: large U-shaped chilled coils, turquoise brine tanks, west/east/south tee.
- Nursery: two glass fungal hoods, cream/violet caps, substrate bins, west/east/south tee.
- Loom: concentric segmented rings and suspended fragments, violet center, four doors.
- Battery: four armored charge stacks, cyan windows, four doors.
- Solar: navy photovoltaic racks and inverter, west/south elbow only.
- Storage: four olive cargo stacks and pallet mover, four doors.

Shared prompt contract: single production square room, worn steel hull, overhead
cutaway pixel illustration, quiet slate floor, large readable forms, centered
14-percent-width door notches, no text/UI/characters, alpha exterior. Built-in
image generation used for each separately; the approved Python pipeline handles
cleanup and normalization, not generation. No gameplay or runtime mappings changed.

## Pilot status

Three candidates generated with the built-in image generation tool. Saved in
`output/room-art-pilot/`, not connected to runtime or card mappings. Existing
game assets, player saves and project.godot remain untouched by this work.

- Reactor: 1254 square, actual transparent corner verified (alpha 0).
- Hydroponics: 1254 square, opaque checkerboard exterior (alpha 255).
- Mining Bay: 1254 square, opaque checkerboard exterior (alpha 255); larger outer
  margins also need normalization before integration.

The generator did not honor the requested 1280 canvas. Keep native resolution
during candidate review; no candidate has been resized. Both hydroponics output
and a subsequent background-extraction edit retained an opaque checkerboard.
Do not accept these candidates as production-transparent sprites.

## Prompt provenance

Execution: built-in imagegen, no CLI or paid API fallback.
Source reference files inspected before generation: rooms/reactor.png,
rooms/hydroponics.png and rooms/miningdronebay.png.

Reactor primary prompt:

> Use case: style-transfer. Single production BrineSpace reactor room PNG, square 1280x1280 requested. Redesign reference into cleaner composition with rich worn metal: ONE dominant amber reactor in center, only four large supporting machinery clusters, much quieter dark slate floor, readable large forms, polished industrial pixel illustration. Keep EXACT overhead cutaway camera, square footprint, four centered door openings north east south west and clear perimeter walkway around reactor leading to each. Hull fills canvas with approximately 8px outer margin, clipped corner silhouette. Door openings each about 14 percent room width centered precisely on the side midpoint. Open doors are unobstructed floor passages out to image edge, no black filled rectangular holes or closed doors. Hull sides meet image bounds consistently to tile beside other rooms. Genuine transparent alpha outside hull, NO opaque black or checkerboard background. No text, no UI, no characters, no diagram, no comparison. Preserve worn metal mood, amber energy and very restrained cyan screens, no excessive glow. Static seed art for later operation overlays, full complete room not cropped.

Reactor accepted candidate is the follow-up extraction:

> Precise production correction to this reactor sprite. Preserve all existing room art, machinery, walls, composition and colors. Remove the white exterior background completely and return a PNG with genuine alpha transparency outside the room hull and in the empty doorway notches. Not white, not black, not checkerboard: actual transparent pixels. Output canvas exactly 1280 by 1280 pixels. Keep the room full size and centered with approximately 8 pixel margins. This is background extraction and canvas correction only, not a new illustration. No labels.

Hydroponics prompt (original room subject plus corrected reactor style reference):

> Single production HYDROPONICS BAY sprite for BrineSpace. Image 1 is subject reference; image 2 is the approved target hull, scale, camera and hybrid style. Redesign hydroponics with four LARGE clearly readable planting beds, one in each quadrant, leafy green crops and a few restrained magenta blossoms, one conspicuous cyan irrigation tank integrated into a bed. Quiet slate floors, broad uncluttered CROSS-shaped walkway connecting exactly four doors centered north east south west. Match reference 2 square hull footprint and door anchors, worn steel materials and fine selective detail but simpler machinery composition. Overhead cutaway, not isometric. Square native 1254x1254 canvas, hull nearly fills canvas with 8px margins. Genuine transparent alpha exterior and doorway notches, NOT opaque background or checkerboard. No reactor, text, UI, labels, characters or atmosphere outside room. Door openings 14 percent of room width, perfectly centered. Recognizable at small game scale. One room only, no sheet.

Hydroponics unsuccessful extraction prompt:

> Background extraction ONLY. Preserve this hydroponics room exactly. Remove ALL the baked white and gray checkerboard outside the hull and in doorway notches, replace with genuine transparent alpha pixels. Output transparent PNG, not a checkerboard picture. Keep the exact square canvas, room geometry, colors and machinery unchanged. No other changes.

Mining prompt (original mining room subject plus corrected reactor style reference):

> Single production MINING DRONE BAY game sprite. Image1 is subject reference, image2 target hull style. Redesign with exactly TWO large recognizable yellow mining drones in docking cradles, one left and one right of a broad vertical aisle. Reduce clutter strongly; some large maintenance tools and cyan dock screens. Worn dark industrial steel, quiet slate floor, selective pixel detail, clean strong silhouettes. EXACT overhead cutaway square room. ONLY two centered door openings NORTH and SOUTH, no east or west doors. Match reactor hull scale and wall thickness, room fills square1254x1254 canvas with tiny8px margin. True transparent alpha outside hull including doorway notches, absolutely no white or baked checkerboard background. No text UI characters or poster. Doors centered and14 percent room width. Static game asset, not comparison.

## Verification still required

Exterior cleanup and hull normalization, production asset tests, runtime/card
mapping changes, LFS staging verification, native viewport checks and regression
suites have not been completed. No claim of in-game acceptance or completed pilot.
