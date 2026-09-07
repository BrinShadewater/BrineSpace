# Modular room laboratory

## Current status (supersedes historical checkpoints below)

The nursery is now integrated into gameplay, station rendering, placement preview,
cards and inspector. Its single-room acceptance is complete, including a local
checkout-independent package smoke test. See `NURSERY_GAMEPLAY_INTEGRATION.md`
for the current requirement/evidence audit. Sections below retain the experiment history;
their statements about missing gameplay integration describe earlier checkpoints.

`output/embedding-final-01.log` revalidates the reusable scene after station
integration: four rotations, transparent exterior, canonical ports, host-driven
operation clocks, disabled independent input and single-owner edge omission.
All four fresh 512px renders were visually inspected together: vertical props stay
upright, directional machinery changes face, and all three openings remain equal.
The q0 PNG is byte-identical to `rooms/modular/nursery-card.png` (SHA256
`332C37CC69351D9DC41F31488CCD4DC7320850C8AA2536474751E5430EF0E41B`).

The reservoir and growth use explicitly documented upright sprite reuse, not
four reconstructed physical views. The microscope has registered directional
views with minor contour drift. These limitations remain visible in the recipe;
integration does not erase them or certify the entire older room pack.

## Embeddable room component (2026-09-05)

The tested canvas is now `rooms/modular/nursery_view.gd`, used both by the
laboratory and `rooms/modular/nursery.tscn`. This extraction only changes the
experimental renderer; `scripts/main.gd` and the existing station renderer are
untouched. The shared structural helper currently remains under `tools/` and
must be included with the scene when packaging it.

After adding the scene to its host, call:

```gdscript
view.configure_embedded(quarter_turn, open_screen_sides, functioning, visual_time, omitted_screen_sides)
```

Sides are N/E/S/W = 0/1/2/3. The room opens only its valid rotated ports. The host
resolves connectivity and shared-edge ownership; omitted sides suppress the
duplicate assembly on the non-owning room. Position and scale belong to the host
Node2D transform; do not rotate that transform. Embedded mode has no lab UI,
input processing, independent clock or test actor. Future crew integration must
participate in room depth ordering rather than draw a sprite over a baked image.

`tools/test_nursery_embedding.gd` validates four directional views, transparent
exterior, port masks, host-driven active/offline clocks, disabled input and edge
omission. `output/embedding-01/` contains four 512px native transparent renders
and a native 128px card preview, all visually inspected. These are preview assets,
not wired card mappings. `output/reusable-view-01/` passes the existing movement,
depth and animation suite; all 16 offline prop crops match `recipe-native-01`
byte-for-byte after extraction.

The nursery is not yet a gameplay database entry. Main-game integration still
requires its approved paid build/unlock behavior, station connection ownership,
crew depth integration, card mapping and gameplay regression evidence. Do not
route it through the old station's whole-texture rotation as a shortcut.

## Reusable nursery recipe and completed route-sheet review

`rooms/modular/nursery-room.json` now supplies the nursery's door sides, stable
prop IDs, local centers, collision footprints and art registration roots. The
renderer and collision layout consume this same recipe. Shared cell/wall/aperture
dimensions remain in `tools/modular_room_geometry.gd`; this is a pilot recipe,
not a second gameplay room database. Rotation policy and known art approximations
are explicit in the recipe.

Startup rejects malformed recipes before building the room. The focused test
`tools/test_modular_room_recipe.gd` passes the valid recipe, rejects 11 mutations
(including blocked aisles, duplicate IDs, invalid doors and missing asset roots),
and verifies 16 rotated placements. `output/recipe-test-02.log` is clean; the
earlier `recipe-test-01.log` retains a failed negative-rectangle diagnostic that
was corrected before acceptance.

`output/recipe-native-01/` passes the full native suite at 1600x900. All 16
offline prop crops are byte-identical to `room-acceptance-1600x900-01`, showing
that moving placement data into the recipe did not alter the registered art.
All remaining continuous-route sheets were inspected from the earlier acceptance
capture: bench q0/q2/q3, filter q0/q1/q3, rack q0/q1/q2, tank q1/q2/q3. Together
with the four previously reviewed sheets this covers every prop/orientation.
The sampled poses show correct side clearance and front/behind overlap. They
are eight samples per circuit, not a claim that every rendered frame was watched.

Remaining production work: main-game/card integration and an explicit decision
on whether the documented upright-sprite approximation meets the final art bar.
The room prototype is usable; the full production goal remains open.

## Current checkpoint: four-direction movement and viewport pass

The nursery is a working isolated room prototype, not a main-game replacement
or completion of the 34-room asset ledger. Its generated materials and separate
props are assembled over deterministic geometry; whole-room bitmaps never rotate.

Latest evidence: `output/room-acceptance-<size>-01/` and matching `.log`, for
1280x720, 1600x900 and 2560x1440. All three native Godot runs exit 0 without
errors or warnings and pass:

- 1,540 geometry passage samples, canonical 96-unit opening and single shared seam.
- Actual input-driven doorway traversal in all four orientations.
- 16 continuous prop circuits / 2,192 collision-checked movement steps per run.
- Eight walking-direction image comparisons, 32 per-machine state comparisons,
  offline machine freeze, independent crew clock and paused-frame equality.

The latest small q0, medium q2 and large q1 room frames were visually reviewed.
Earlier static depth sheets cover all 32 front/behind poses. Four continuous
route sheets were reviewed (bench q1, tank q0, rack q3, filter q2); the remaining
route sheets are captured but not yet visually accepted. Automated movement
success does not certify every intermediate occlusion frame.

Known art approximations remain: growth and reservoir details reuse upright
sprites; microscope guide-based paintovers have residual outline drift. Export
packaging and main-game/card integration are not tested by this laboratory.
These notes supersede the older remaining-work lists below, which are retained
as chronological evidence.

### Run locally

From the checkout, supplying your installed Godot executable:

```powershell
./tools/run_modular_room_pilot.ps1 -Godot 'C:/path/to/Godot.exe'
```

WASD/arrows walk; R rotates the pair; 1/2 rotate individual rooms; F focuses the
nursery; B shows the four-view prop board; O toggles machinery; Space pauses.
`-Test` runs geometry checks only, not the visual acceptance suite. For native
captures invoke Godot with `--script res://tools/modular_room_pilot.gd --
--require-directional-art --viewport=1600x900 --capture-dir=<new-absolute-path>`.
Keep the capture destination new to preserve prior evidence. No player save is
loaded or changed.

## Depth ordering and stable surface variation (2026-09-05)

Wall bands and jambs now participate in the same depth ordering as machinery and
the actor, fixing north-wall overdraw through the character's head. Floor labels
also render before props/characters instead of over their bodies. Collision and
clear doorway dimensions are unchanged.

`output/depth-review-native-01/depth-review-q0.png` through `q3.png` collect actual
native frame regions at unchanged pixel scale, four prop columns (rack, bench,
tank, filter), behind/front rows. All 32 views were visually inspected: front
actors cover cabinet/tank fronts, rear actors have their feet/lower bodies hidden
by the props, and the north wall no longer slices through their heads. These
are static positions; lateral and continuous corner-transition review remains.
The matching log passes actor motion, all 32 machine-state comparisons, pause,
door crossing and 1,540 geometry samples.

Floor tiles now select deterministic room-local texture offsets so stains do not
repeat every two tiles. Bench and filter surfaces sample different enamel areas;
world texel density stays fixed and source PNGs are untouched. Native evidence
`output/surface-variation-native-01/` passes the full current capture suite; the
1600x900 room view was inspected with quieter, less repetitive floor detail and
different wear on bench/filter enamel. This is not final room acceptance.

## Responsive laboratory and existing character art (2026-09-05)

The pilot accepts `--viewport=1280x720` (also tested at 1600x900 and 2560x1440).
The four-view board fits the actual viewport and sidebar line spacing adapts
without reducing the 14px body font. All three native runs passed geometry,
per-machine active/offline checks and pause equality. Evidence directories are
`output/viewport-<size>-native-01/`; the small room/board, medium connected pair
and large room were visually inspected without UI clipping. Those captures
precede the character replacement below.

Major Bill's existing eight-direction walking art now replaces the block figure.
The original 92px canvases share the (46,68) feet reference at 0.75 world scale;
no source frames are altered. Cardinal idle uses existing breathing animations;
diagonal idle uses existing static rotations, since diagonal breathing frames
do not exist. Animation time is separate from machinery time and freezes on pause.
Blocked movement uses idle, while input direction still sets facing.

`output/actor-depth-native-03/` at 1600x900 passes eight paired walking-image
comparisons, pause-clock invariance, offline character-clock continuation, all
32 per-machine state comparisons and the prior geometry/crossing suite.
Log `output/actor-depth-03.log` has no errors or warnings and exits 0. The initial
actor run is retained as failed evidence of an incorrect diagonal-idle assumption;
do not use its exit-zero result as acceptance. Export packaging remains untested.

Remaining: inspect the full character-depth set (including lateral approaches),
repeat character acceptance at the other sizes, improve surface repetition and
finish room-level visual acceptance. No main-game scene or player save changed.

## Directional service faces and per-prop motion (2026-09-05)

Cabinet/rack faces now select the physical front, side or rear for the current
quarter turn. Front drawers/intake slots are no longer stamped onto every view;
the right side has a maintenance hatch and the rear has vents and a connector.
The bench console is a projected tilted panel with thickness, stand, screen and
rear vents. Its display is hidden when the rear casing faces the camera.
Bench vial bubbles keep functioning visible even when that screen is turned away.
These details extend the existing code-native chassis; no generated art was replaced.

Native capture now compares separate machine regions, not just whole-room pixels:
4 prop types x 4 orientations x active/offline = 32 passing comparisons. It also
saves 32 character-front/behind views for depth review. Evidence is
`output/prop-views-native-01/`, log `output/prop-views-01.log` (exit 0).
Initial visual checks cover rack q0 behind, bench q1 front, tank q2 behind and
filter q3 front; the full set is captured but not yet exhaustively inspected.
The tank-near-north-wall depth fixture partially hides the actor behind the hull,
so that frame alone is not sufficient evidence of clean character readability.

Remaining: complete depth review including lateral approach, responsive viewport
checks, less repetitive surface wear, and stronger final-art consistency.

## Shared-model microscope art (2026-09-05)

`tools/bake_microscope_proxy.gd` now builds one dimensional microscope and renders
four fixed-camera views. Camera compensation matches the pilot's oblique
screen=(x,ground_y-height) projection. Sixteen actual camera projection checks
verify axis landmarks and the shared (240,336) pivot on a 480-square canvas at
8 pixels/unit. Output `rooms/modular/microscope-proxy-02/` has native RGBA alpha.
This is a simplified authored shape, not an exact reconstruction of the first art.

Four built-in paintovers using those guides are in
`rooms/modular/microscope-guided-01/`, with exact prompts, raw copies, hashes and
registration. They follow the front/side/rear camera and support/stage occlusion
far better than the text-only yaw trial. All generated canvases are 1254 square;
the opaque checkerboards were removed with edge-connected neutral-light cleanup.
Full canvases are retained and use the same normalized ground pivot (0.5,0.7)
and 60-unit world canvas, not four independent tight fits.

Native evidence `output/microscope-guided-native-01/` shows all four views on the
bench. Directional coverage, 1,540 geometry samples, input-driven crossing,
active/offline frames and paused equality pass (log `output/microscope-guided-01.log`).
The microscope no longer needs missing-direction procedural art in this pilot.
Generated shapes still drift from the guide by several source pixels and the
side bases are not perfectly registered; this is provisional pilot acceptance,
not pixel-locked production approval. Do not infer perfect geometry from coverage.

Remaining room work: cabinet/service faces must follow local orientation, console
directionality, per-prop depth/operating-state evidence, target viewport coverage,
and visual polish. Upright growth/vessel reuse remains approximate. No main-game
renderer or gameplay changes were made.

## Directional coverage gate (2026-09-05)

Three built-in microscope candidates are preserved with exact prompts and hashes
in `rooms/modular/microscope-directions-01/`. All are opaque RGB despite requested
alpha. Materials remain recognizable, but the requested rear view still exposes
front features; the set is withheld, not counted as three completed directions.

The pilot now consumes registered direction metadata for the microscope instead
of hardcoding facing zero. JSON numeric directions are normalized to integers.
`--test --require-directional-art` exits 2 with missing views [1,2,3], as expected.
This is a narrow microscope gate, not exhaustive visual acceptance for the room.
Ordinary native capture remains passing: 1,540 geometry samples, input-driven
crossing, operation/offline behavior, four rotations and identical paused frames.
Evidence: `output/directional-native-01/`; gate log: `output/directional-gate-02.log`.

Both installed and repository pipeline skills now route to `layered-assets.md`;
both pass skill validation. Next: use an authored dimensional microscope proxy
to establish coherent views before another art pass, and expand per-prop depth
and animation evidence. Current upright vessel/growth reuse remains approximate.

An isolated, playable **geometry and rendering prototype**, not approved production
art. It does not load the main scene, meta-state or player save, and changes no
normal-run gameplay. No generation credits are required.

## Run

### Generated materials and cartridge pass

`rooms/modular/materials-01/` adds original generated enamel and slate surface
maps plus a cylindrical cartridge sprite. Exact prompts and hashes are preserved
in provenance. Generated pixels remain unchanged; cartridge alpha bounds are used
for display registration. The surface renderer repeats texture UVs every 128 world
units and rotates their coordinates with facing, inside the existing polygon.
Doors still come entirely from geometry. Cabinet fronts use a darker material tint.

Native evidence: `output/materials-native-01/`; log `output/materials-01.log`.
All four room orientations inspected; 1,540 passage samples, input crossing,
operation/offline and pause checks pass at 1440x1000. Cartridge stays upright.
G toggles all generated materials/components. The finish is closer, but cabinet
bevels/vents remain procedural, wear is broadly distributed, and the microscope
still has only its front generated view. Texture seam continuity is not certified.
No main-game integration or full production-ready room claim.

### Generated component trial

`rooms/modular/components-01/` holds three separately generated assets, their
untouched originals, cleaned copies, registration and exact prompts in provenance.
Built-in image generation was used. The pilot now loads these in addition to
the previous jamb/south-rack registry; G toggles generated art.

Growth clusters use upright camera-facing sprites at rotating tray anchors.
The reservoir uses a rotationally symmetric sprite body with separate valve and
bubble effects. This is a billboard approximation: its wear stays screen-fixed.
The generated microscope is enabled only at facing 0; unsupported views deliberately
retain the procedural instrument. This is not a completed four-direction prop pack.

Native alpha was preserved for growth and microscope. Reservoir output contained
an opaque checkerboard, removed using the authorized light-neutral exterior cleanup.
Display regions for native-alpha assets ignore faint specks using alpha >=128 bounds
plus two pixels of margin; original canvas pixels remain intact. Display is
aspect-preserving and ground-anchored, without rotating or stretching textures.

Evidence: `output/components-native-02/`, log `output/components-02.log`.
Four native room orientations inspected at 1440x1000; passage tests (1,540 samples),
input crossing, active/offline/pause checks pass. Three cleanup tests pass and
all new PNGs match LFS attributes. The art is more detailed, but repetition in
the growth clusters and mixed procedural/generated finish remain visible.
Cabinet surfaces, wall/floor materials and remaining microscope directions are
unfinished. No main-game or card integration was performed.

### Full nursery prop pass (2026-09-05)

The nursery now has a complete procedural prop treatment in the pilot: layered
growth rack; specimen bench with upright vials, microscope and operating monitor;
round nutrient reservoir with level marks, bubbles and an occluded rear valve;
three-cartridge recycler with a gauge and operating bubbles. Other room furniture
is unchanged. Flush floor grates, a rotating service hatch and wall-panel seams
add construction detail without adding obstacles or changing the 96-unit aperture.

Brief: quiet cultivation bay with pale fungal growth as its focus, cream enamel
against slate flooring, restrained teal liquid and local operating cues. Existing
four prop footprints remain authoritative. This pass is drawn in Godot, not
generated or extracted from the accepted raster art. No paid generation was used.

L compares layered props against the previous study. F isolates the nursery for
inspection while leaving the actual two-room collision fixture intact; the missing
neighbor in this view is only hidden, not deleted. R still rotates the pair.

Evidence: `output/nursery-room-native-03/art-detail.png`, four
`layered-detail-N.png` views and full-pair `rotation-N.png` views.
`output/nursery-room-03.log` reports 1,540 passage samples, radius-aware jamb
checks, input crossing, whole-room changing active pixels and identical offline
pixels, and identical paused frames. Captures are native 1440x1000.
Depth captures cover the rack, not exhaustive movement behind every new prop.

Visual review: upright components and clear paths survive the four orientations.
The finish remains schematic, with simpler materials and repeated cabinet faces
than the Higgsfield reference. This is a complete *pilot room pass*, not approved
production art, a new gameplay blueprint, or station/card integration. Main scene,
save behavior and normal-run mechanics remain unchanged. Whole-game suites were
not rerun because this executable pilot does not load or modify their consumers.

### Current layered-rack experiment

The default rack now uses procedural layers in the isolated pilot. L toggles back
to the prior generated-art trial, and B opens a native four-direction comparison.
No source image was cut up or repainted and no generation credits were spent.
The generated south rack remains available; rejected directional images stay disabled.

The 102x74 chassis, three trays, service patch and valve mount rotate in room-local
coordinates. Screen-up elevation, mushroom stems/caps and valve shape stay upright.
Growth clusters sort by projected anchor within the rack; the whole rack continues
to use the existing prop/character depth queue. The visible chassis face is a
repeated vent treatment on all sides, not a fully authored four-sided cabinet.
This is a layering proof, not production-quality replacement art.

Verified in Godot 4.6.1 at 1440x1000: all four views inspected, 1,540 passage samples,
input doorway crossing, active effect pixels change, offline pixels stay identical
despite changing phase, and paused frames match. Native evidence:
`output/layered-rack-native-02/`; log: `output/layered-rack-02.log`.
Use `layered-directions.png` for the same-scale four-view board.
Main gameplay, cards, collision dimensions and player saves remain unchanged.

Next art gate: replace these procedural growth clusters and surface treatments
with separately authored, fixed-anchor art while retaining this layout/projection.
Improve cabinet side identity and wear before expanding to more props.

From the checkout, pass your Godot 4.6 executable to:

```powershell
./tools/run_modular_room_pilot.ps1 -Godot 'C:/path/to/Godot.exe'
./tools/run_modular_room_pilot.ps1 -Godot 'C:/path/to/Godot.exe' -Test
```

WASD/arrows move. R rotates the connected arrangement (both spatial layout and
room-local facing); 1/2 independently rotate room door masks and furniture. A
mismatched shared port closes the seam. Home resets. Tab shows footprints and
depth anchors. O stops machinery effects; Space freezes simulation and movement.
Unconnected exterior ports are capped for safety in this closed laboratory.

## Contract demonstrated

- Cell pitch 384 world units; clear opening 96; wall band 16; character radius 7.
  These are pilot constants, not a change to existing game door dimensions.
- Door centers are edge midpoints; the structural edge is generated exactly once.
- Both neighboring masks must expose a port to open their shared edge.
- Collision uses the same wall rectangles and prop footprints as rendering.
- Rotate layout coordinates and local details, not a flattened room illustration.
  Screen-facing prop surfaces remain upright under a fixed camera.
- Character and props share a feet/ground-anchor depth-sorted drawing list.

The furnishings are temporary code-drawn racks, tanks, benches and filters. They
demonstrate the replacement interface for future four-direction artwork; they do
not recreate the approved Higgsfield finish or prove generated views consistent.
The nursery/reclamation pair is a fixture, not two added gameplay blueprints.

### First generated-art trial

The pilot now loads `rooms/modular/art-trial-01/registration.json` when present.
Only the south-facing rack and jamb cap are enabled. Other furniture and rack
directions remain procedural. **G** toggles art for comparison; **F** focuses on
the nursery origin. `output/modular-art-native-01/` contains native captures.

Five Higgsfield images cost 10 credits (913.5 to 903.5). All source prompts, job IDs,
raw/clean hashes and rejection findings are preserved beside the assets. All raw
canvases remain 2048 square; cleanup only removes edge-connected light neutral
background. Visible bounds are aspect-preserving contain-fitted into fixed visual
boxes with bottom-center anchors, without altering collision. This registration
is provisional, not an assertion of consistent physical scale across directions.

The west/east requests failed to turn the rack: trays and front service panels
stayed largely front-facing. North changed its panel but is withheld pending
stronger consistency evidence. The renderer intentionally falls back to procedural
art for all three; it never rotates or squeezes the south image to disguise failure.

The cap is reused in two fixed 16-unit square wall-end boxes per open shared edge.
Neither image can enter the 96-unit clear aperture. Wall outlines were also moved
inside the wall rectangles so they cannot visually narrow the opening. This is
doorway hardware, not a finished animated door leaf or a complete wall-art kit.

Native tests still pass for 1,540 passage samples, all four structural rotations,
jamb exclusion from the aperture, input-driven crossing and identical paused frames.
The south art reads in the native detail view; the four-direction art gate remains
failed. Next trial should use explicit directional geometry guides plus the style
reference, not repeat unconstrained rotation prompts.

## Verification

### Directional geometry-guide trial (2026-09-05)

Two further Higgsfield candidates are preserved in `rooms/modular/art-trial-02/`.
`tools/render_rack_geometry_guides.py` renders new parametric layout guides:
102x74 world-unit footprint, 23-unit screen-up extrusion, fixed 10px/unit scale,
2048-square canvas. Ground coordinates rotate; mushroom stems do not. These
are geometry proxies, not replacements for the approved art or exact models of it.

Each request used its guide first and the approved south rack second for materials.
The west candidate ignored the guide and reproduced horizontal trays. The east
candidate followed the vertical footprint and marker placement, but mushroom
details look sideways/repeated rather than physically reprojected. Both are
withheld; no new assets are enabled and the previous pilot is unchanged.

Read-only bounds diagnostics found the guide at [654,400,1395,1651], west output
at [225,409,1823,1711], east at [645,338,1403,1649]. Thus even the better silhouette
is not pixel-locked. No cleanup, crop, rescale or image repair was performed.
Exact prompts, reference IDs, hashes and findings are in the trial provenance.

This trial strengthens the case for a deterministic dimensional prop source:
rotate the chassis/layout, use direction-specific surfaces, and place upright
mushroom clusters and valves separately. AI can supply material/prop candidates,
but this two-image test does not establish dependable geometry control. No
additional paid retries or main-game renderer changes were made.

`--test` runs all four connected orientations, 1,540 radius-aware centerline samples,
unique seam count, both jamb boundaries, furniture collision and nonmatching-port
closure. Native capture mode additionally tests input-driven walking through the
seam and operation/pause state transitions. It captures four rotations, character
behind/in front of a rack, and two paused frames whose image bytes must match.

```powershell
& 'C:/path/to/Godot.exe' --path . --script res://tools/modular_room_pilot.gd -- '--capture-dir=C:/new/absolute/evidence-directory'
```

The capture directory must not already exist. Current evidence is under
`output/modular-pilot-native-03/`; logs are `output/modular-pilot-test.log` and
`output/modular-pilot-capture.log`. Native evidence uses 1440x1000; other viewport
sizes and exhaustive human movement are not yet validated.

## Next art-production gate

Retain the approved Higgsfield nursery as **style only**. Produce floor surfaces,
wall-cap material swatches and separately registered props, with directional
views where required. Lock exterior bounds, pivots and collision footprints;
keep machinery animation in separate layers. Do not independently tight-crop
each direction or let generated wall thickness define cell spacing.

First replace just the rack and one tank, and inspect the actual native pilot at
all four rotations. Do not generate an AI composite as evidence of modular fit.
Only after visual acceptance should the shared-edge/prop-rendering approach move
into the main renderer. No monolith refactor or main-scene migration was done here.
