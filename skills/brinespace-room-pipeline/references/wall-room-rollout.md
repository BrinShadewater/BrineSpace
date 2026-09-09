# Continuous and door-aware wall installations

Current owner scope (September 8): fourteen rooms recorded in
`assets/wall-room-rollout-v1/rollout.json`. Complete each named identity through
source, registration, live room, card, four-rotation visual review and crew routes.
The ledger is a progress record, not proof of acceptance.

Use canonical ports to choose continuous versus split banks before generation.
A cross room needs separate sections around its door bay. Never paint a doorway
onto equipment or mask out the middle of an otherwise continuous machine.

For full-wall artwork, the owner's inward-facing direction supersedes the general
south-facing upright-prop default. Inspect each interface, not only the wall back.
The last verified batch needed separate north-facing south-wall source art for
Tidal and Thermal; NS/EW straight rooms can instead use a sealed north or side
wall. Derive the needed views from actual placements in all four rotations.

Match wrappers to the current baseline method contract. The previous Tidal,
Biodome and Thermal integration caught nonexistent draw_prop_base/animation
methods inherited by copying a Research wrapper. Read methods before writing.

Register actual source dimensions and repair reviewed enclosed background gaps
without rewriting raster colors. The previous batch's pipe loop and planter rail
passed outer silhouette checks while retaining white holes; inspect native art.

After each verified batch, record concrete failures and fixes here and in the
bible, update the rollout evidence, then compare and sync maintained skill changes
into the installed snapshot. Never overwrite divergent installed content blindly.

## Verified pilot findings

Salvage, Construction and Anomaly passed four-rotation native review and crew
routes, with 24 floor-detail placements and no missing hosts. All three initial
side pairs retained one south-facing appliance despite an orientation reference.
Targeted console/window/drawer repairs succeeded. Starting with side views is
the next experiment, not a proven shortcut; record its results before recommending.

Reserve relocated fleet vehicles and hatches before fitting secondary furniture.
The stricter check caught a recovery tray overlapping the Salvage drone at q2.
Record the manual fleet shifts as moves so old floor services do not stretch
across the aisle. Preserve existing fleet animation props rather than baking a
second occupied drone into the new wall source.

The source recorder is `tools/record_wall_source.py`: save the exact prompt first,
then record immutable image bytes, dimensions, reference paths and separate review
status. Reject overwrites. Source batches use `tools/audit_room_source_batch.py`;
each view is its own provenance identity with revisions, not a new room count.
Native review and floor-anchor tools accept `--review-rooms=` to validate affected
rooms and relevant shared-code regressions without recapturing the entire catalog.

## Owner camera clarification during Radio production

The camera remains top-down. Inward means the console operator deck faces the
playable floor where crew stand. Do not interpret upwards as pointing apparatus
away from crew or tilt the camera below the base. Low-angle towers and cabinet
backs toward the room were rejected. For near-overhead side consoles, specify
physical working order across bank width: wall-side display/window, aisle-side
hand controls. Left bank controls lie right, right bank controls lie left. The
mounting rail remains north-south. Keep camera, footprint axis and operator-facing
direction separate in prompts and review. A mirrored tall bank alone proves none.

## Flush mounting

Owner correction: wall banks sit flush against the wall. Radio's prior side source
had a tapered backing rail and the generic 174-unit floor inset left a visible gap.
The revised source has straight outer flanges; registrations record `wall_contact`
with reviewed source edge coordinates. Mounted banks use the canonical inner wall
face `(CELL-WALL)/2`, currently 184 units. Their visual envelope can reach the actual
hull; other props retain their existing floor bounds. Preserve invalid-draft checks
and validate exact wall contact, source geometry, door lanes and native seam pixels.
Do not fix a tapered mounting edge by stretching the image or burying a large part
of its machinery in the wall. Source correction plus measured placement is required.


## Shield wall installation checkpoint
Shield Generator side-first sources retained its gunmetal/orange engineering identity and inward controls without a repair generation. Native four-rotation review and production crew routes pass; eight floor details resolve. The replaced injector and panel-cradle hosts needed an explicit full-wall fallback. Check semantic floor anchors even when native placement passes: visual replacement can remove their host IDs. This is one successful source-first case, not proof that every room will need no revisions.


## Quarantine retention gate
The first specimen-bank source copied the patient berth from its subject reference. A focused repair replaced it with vial trays before integration. Native inspection then caught the original berth omitted at q0/q3 despite passing bounds checks. Quarantine now reserves its berth before secondary furniture, and the native review asserts berth presence in every rotation. Explicitly preserve a room-defining apparatus when adding wall art; clearance alone does not establish semantic completeness. Four rotations/two states, eight floor anchors and production routes pass.


## Med Center integration finding
Med Center uses center_dressing rather than dressing or cryo_dressing. Include its profile in active host/service filtering; otherwise native rendering asserts on the omitted medical_station even when placement checks pass. Preserve medical_treatment and medical_imaging first and assert both across rotations. Source review also required darker enamel and transverse side keyboards; explicit across-width wording remains necessary. Native four-rotation review, eight anchors and crew routes passed after correction.


## Med Office checkpoint
Using the corrected Med Center side pair as camera/exposure reference produced inward keyboards without a repair generation while retaining separate office subjects. Preserve office_exam and office_consultation first; office_dressing requires the same host cleanup as center_dressing. The q1 records marking needed scale 0.5 to fit adjacent floor; other rotations keep 0.7. Four-rotation native review, eight anchors and crew routes pass. This is a specific success, not a universal no-revision guarantee.


## Biomass source checkpoint
Biomass required an explicit circular top-lid repair: merely requesting top-down retained tall source tank elevations. Specify circular lids and absence of side walls for vertical cylinders. Its north source has real RGBA transparency; the first south source instead painted an opaque checkerboard. South-v2 repairs that background to white. Inspect mode and alpha per output, even between adjacent generations. These sources remain pending native integration.


## Biomass integration checkpoint
The wall skid replaces power_machine and its fixed service run; the wrapper supplies the new operating lamp while retaining ordinary console behavior. North source uses alpha-to-vector registration; white side/south sources use neutral exterior registration. South wall_contact now places the entire footprint at the canonical inner wall face and native review checks the south coordinate explicitly. The q3 drain fits at scale 0.6. Native four rotations/two states, eight floor anchors and crew routes passed.


## Split source registration
Use tools/register_split_wall_props.py with explicit columns, rows and row-major labels. It chooses actual alpha or neutral exterior registration per source, preserves PNG bytes, refuses existing output directories, and rejects any silhouette touching a cell divider or sheet edge. It does not infer doors or approve art. Life Support north pair registered two separate 712x465 sprites; source camera needed a lying-cartridge repair. Native split integration and remaining directions are pending.


## Verified split placement
Life Support uses split_wall_prop.gd and split-life-support-wall.json: eight independently authored sections, two 128-unit spans per rotation, +/-184 inner-wall mounting and a 112-unit central gap. Each section has its own collision footprint. Original fan/filter art is replaced; tank/console are placed first and asserted present. Active dressing hosts follow surviving props, saved layout overrides apply last, and the wrapper supplies fan motion. Native four-rotation/two-state door/contact/count checks, eight anchors and production crew routes pass. Reuse this two-section contract for remaining cross rooms; keep their subjects and preserved equipment explicit.


## Hydroponics source findings
A side-facing control strip alone did not produce a vertical bank: the first four-cell sheet retained horizontal footprints and top rails. Pair the subject reference with an accepted side-layout reference and explicitly remove old top rails. Hydro side repair then produced tall modules with straight outer rails. All eight directional sections registered without touching dividers. Native integration remains pending; do not count source completion as a verified room.


## Hydroponics service-host correction
Split Hydroponics retains hydro_harvest and hydro_nutrients, with native presence assertions. room_services.gd previously used an empty Rect2 for removed beds and drew phantom irrigation lines to the origin. Skip missing bed hosts; the new wall sections have integrated plumbing. Native four-rotation review, eight anchors and production crew routes pass. Inspect bespoke service renderers as well as dressing profiles when replacing equipment.


## Battery split checkpoint
The split helper reused the eight-section battery source set without geometry changes. battery_breaker and battery_distribution are prioritized and asserted present across all rotations. Standing mats needed scale 0.45 at q1/q3 beside the retained test bench; other poses keep 0.7. Native door/contact/presence checks, eight floor anchors and production crew routes pass. Room card refreshed.


Storage directional lesson: check every bin handle and strap buckle as well as console controls. A correct outer rail can conceal south-facing access on individual cargo lids. On side modules, handles belong on the inward left/right lid edges; on south modules, all handles face north. Preserve targeted rejected revisions and register actual dimensions (Storage side sheet 962x1634), without changing raster pixels.


Storage integration checkpoint: retain loading lift and loose cargo when replacing wall shelving; attach restraint floor detail to the new cargo bank. Eight anchors and four rotated production routes pass. Source handle-direction review and runtime wall-contact checks are complementary: neither alone establishes acceptance.


Command source checkpoint: specifying keyboard strips beside the wall-side displays produced inward side-console working order in the first candidate. North/south outputs use true alpha while the side sheet uses white background; inspect each image independently and select registration by actual alpha. Preserve the original command-table sonar and add source-relative screen feedback when replacing active consoles.


Command integration checkpoint: source-relative screen centers differ by direction and module. Preserve the old chart-table/system effects and draw new display marks only while operating with the room machine clock. Four-rotation placement and crew tests pass; rendered pause/offline behavior remains a separate final-audit gate.


Completion-audit finding: side-only draft tests missed horizontal rollout banks that accepted out-of-hull saved positions. Apply placement fallback validation to every orientation of each new continuous bank, and test split sections individually. tests/test_wall_rollout_drafts.gd covers all 56 room orientations while preserving saved data. A Godot assertion can leave SceneTree running; inspect errors and enforce runner timeouts rather than accepting process status alone.


Final fourteen-room acceptance: bindings audit covers 55 preserved source versions and 74 registration files, not 74 room identities. Native review covers all 56 orientations, floor audit all 112 placements, and draft fallback all poses. New-effect pixel tests crop only animated banks and use the owning pause clock. Restore fixture viewport after game initialization, hide CanvasLayer UI and free nodes before shutdown to avoid misleading captures and teardown errors. See docs/WALL_ROOM_ROLLOUT_ACCEPTANCE_2026-09-08.md.


Data Archive follow-up: layout_06_core exposes all four doors even though its legacy source looks enclosed. Derive split-bank geometry from the database and live layout, not the source shell. Keep independent cartridges/index sections and preserve archive_library/archive_terminal effects. Three sheets and eight sections pass native/floor/crew review. Keep this follow-up manifest separate from the completed original fourteen-room scope.


Holographic Core follow-up: avoid copying subject identity from a geometry reference; cartridge-like first draft was replaced with three optical processors and a lattice display. Unequal sprite-sheet rows need reviewed native gutter coordinates: register_split_wall_props.py --row-cuts 800 preserves the actual white gap. A cut at 780 is rejected for crossing machinery with no output. Keep strict divider checks, not an exception that crops a machine. Projector/calibrator retained in all four native poses.
