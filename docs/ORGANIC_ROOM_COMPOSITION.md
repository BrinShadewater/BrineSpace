# Organic room composition rollout

The owner rejected the evenly paired accessory pilot. Natural furnishing remains
an all-room objective, not a prop-count target. The database and
`ORGANIC_ROOM_ROLLOUT.json` currently contain the same 34 identities. Each ledger
entry now has a distinct activity, grounded furniture, supported-object, floor
service and lighting brief. A brief is not evidence of implementation.

## Integrated first revisions

Later Mining revision: `mining-bay-card-activity-v5.png` staggers the western ROV,
launch hatch and trolley/lamp group instead of retaining matched corner rows.
Four native rotations and graph checks pass; follow-up scope is recorded in
`DRONE_DOCK_STATUS.md`. This applies the existing unequal activity-group rule
without adding a new aesthetic rule to the bible.

Crew Lounge replaces duplicated accessories with a reading lamp, a book console,
a tea trolley and a coat stand. A single rug anchors the reading nook, the lamp
lead reaches an outlet on the sealed wall, and the drinks tray draws on the
existing dining tabletop. The coat stand provides a home for the bag. The new
support atlas is `rooms/production-ten/decor/lounge-support-v2.png` (RGBA,
1254 square). Selected card: `crew_lounge-card-organic-v3.png`.

Maintenance Bay has a small repair table, floor task light, parts trolley and
air-service bottle. The existing toolbox draws on the tool bench. One service
mat and a hose connection between the bottle and diagnostics replace repeated
floor pads. Selected card: `maintenance_bay-card-organic-v2.png`.

Research Lab uses its south-only doorway topology to introduce an offset
preparation island. The island supports samples, a scale and a clamped inspection
lamp. Its instrument lead connects to the scanner; a reagent trolley and cooler
serve the storage area. The specimen tray draws on the existing bench. Selected
card: `research_lab-card-organic-v1.png`. The island's alpha-corrected source is
1312 by 1199 pixels; generation changed framing, so it has new registration.

These are progress revisions. Lounge and Maintenance retain substantial empty
circulation and some isolated groups. Further composition review is required;
native geometry passes do not establish owner aesthetic acceptance. The other
31 rooms remain at authored-brief stage.

## Pipeline and asset handling

`rooms/whole-room/room_dressing.gd` reads authored JSON profiles for Maintenance
and Research. It registers grounded furniture, draws tabletop attachments with
their host, and draws mats and service routes below actors and furniture. It
does not scatter, duplicate or automatically distribute props. Profiles may
specify measured ground width and pivot independently of an overhanging sprite's
full visual region. Optional quarter-specific centers resolve fixed-facing
furniture clearances; they are authored adjustments, not a packing algorithm.

The lounge uses its existing view implementation. Converting that working pilot
to a profile is optional cleanup, not a reason to delay the remaining rooms.

Exact built-in image-generation and edit prompts are saved beside each new
source. No raster postprocessing was applied. The lounge and research cutouts
have verified real alpha. Maintenance's generation and two requested alpha edits
did not produce real transparency. Its first RGB source is therefore sampled
only through individually authored silhouette polygons, including separate legs,
lamp parts and trolley sections. A 1.5-source-pixel polygon inset limits exterior
checkerboard sampling. This is runtime geometry, not an alpha-cleaned PNG, and
the source must never be rendered as a full rectangle. Cutout edge quality remains
a visual-review concern; do not mark those RGB files as transparent assets.

`tools/audit_room_composition.gd -- --view=res://path/to/view.gd` reports each
rotation's floor and visual bounds and overlapping floor footprints. It is a
read-only diagnostic, not an organic-composition acceptance test. Godot generated
the new scripts' paired resource UIDs.

The station fixture now checks composition JSON hashes and parsing in addition
to source/card and component PNG hashes. `--negative-composition-check` injects
an invalid expected profile hash to exercise rejection. Profiles are listed in
the room manifest's `composition_assets`; PNGs remain in `component_assets`.

## Current native evidence

- Lounge: `output/production-ten/lounge-organic-support-v2`, four rotations,
  ten grounded assemblies, state/pause/containment and 1092 route samples pass.
  That run also reported missing environment files outside this room change;
  it is not a clean global runtime pass.
- Maintenance: `output/production-ten/maintenance-organic-v2`, four rotations,
  eight grounded assemblies, state/pause/containment and 1092 route samples pass;
  no ERROR or SCRIPT ERROR entries in that run.
- Research: `output/production-ten/research-organic-v1`, four rotations,
  seven grounded assemblies, state/pause/containment and 364 route samples pass;
  no ERROR or SCRIPT ERROR entries in that run.
- Selected 512-square cards were rendered through native Godot and inspected.
  Research's quarter-one room capture was also inspected at its native size.

Full-catalog packaged testing is tracked separately under
`output/room-rollout/windows-organic-pilot-v1`. Do not infer its result from the
presence of the directory. Actor visits, continuous occlusion review and owner
visual acceptance are distinct gates.


### Completed packaged follow-up

`output/room-rollout/windows-organic-pilot-v3/verification.json` proves a Windows
build launched from an external working directory: 34 source hashes, 68 raw
source/card PNG decodes, seven component PNG hashes/decodes and two composition
JSON hashes/parses. The controlled itinerary reached all 51 placed rooms (34
identities plus 17 battery support rooms), with 135 reciprocal transitions and
10,401 collision/speed samples. Runtime exited successfully with zero assertion
failures and no ERROR or SCRIPT ERROR entries. Normal crew avoidance remained
enabled; this is scheduled movement, not autonomous destination selection.

Pack SHA-256: `C273CFFED5FEF0522EE953204D8A1A8438FF6AAAE587DE7AC91284A93B623CB6`.

The first build's asset checks passed but its old tour stopped when Bill yielded
to Veld; the current fixture can reschedule that explicit traffic interruption.
The second build caught an in-progress main-script edit and could not run. Those
failed outputs remain preserved. The third build is the successful result.

Fresh 1280x720 fixtures are recorded in
`output/production-ten/organic-pilot-native-verification.json`: all three room
fixtures pass with no script/runtime errors. The profile-hash negative control
`output/organic-negative-profile-v2.log` produces exactly the two intentional
profile-hash failures and skips the tour. Its first attempt was interrupted by
the same temporary main-script parse errors and is not verification evidence.

The selected cards, additional native rotation captures and all six final raster
paths were reviewed; the new rasters resolve to Git LFS. Packaged traversal does
not replace close actor-occlusion review or the owner's aesthetic judgment.

### Next production wave

Continue through Mining Drone Bay, Salvage Drone Bay, Command Center and Quarantine Cell using their individual
ledger briefs. Inspect each room's real door topology before layout. Preserve the
remaining 24 identities after that wave; the full objective is all 34 rooms.


## Engineering and cargo support pass — 2026-09-06

Battery Array now has an insulated diagnostic cart with supported instruments and
clamped task light, a cable reel, and a ribbed flush cover over its service run.
Storage Bay has a packing bench with scanner, parcel and manifests on its worktop;
the incoming case sits on the handling platform rather than loose on the floor.
Ore Refinery has a sample preparation bench beside the crusher, supported sample
cups, a pressure-service unit, connected hose and a floor drain. Actual north/south
ports allow the refinery bench to occupy its sealed side wall.

Selected cards are battery_array-card-organic-v2.png,
storage_bay-card-organic-v2.png and ore_refinery-card-organic-v1.png under
rooms/production-ten. Exact generation prompts and rejected versions remain in
the decor directory. No raster postprocessing was applied.

Final 1280x720 native fixtures under output/production-ten/organic-ROOM-final-1280
pass all four rotations, state, pause, containment and route assertions: 1456
samples each for battery and storage; 728 for refinery. Selected cards and q1
captures were inspected. These captures still strongly retain four perimeter
clusters; this is support-furniture progress, not final organic visual acceptance.

The packaged run output/room-rollout/windows-organic-engineering-v1 passes 34
source hashes, 68 raw source/card decodes, 12 component checks and five profile
checks. Its controlled tour FAILS at Research Lab after one completed leg while
waiting for another crew member. Preserve that failure; it does not prove complete
station traversal. Previous successful packaged evidence predates this pass.

Six rooms now have support-composition revisions; 28 remain at brief stage.
All six remain subject to visual refinement and close actor-occlusion review.

The read-only tools/register_alpha_silhouette.py emits hole-free source-space
polygons from true alpha. It rejects opaque inputs and never edits the PNG.
Three unit tests verify holes, faint-haze exclusion, input rejection and unchanged
source hashes. Threshold registration can remove useful translucent glass; inspect
native results and never apply it indiscriminately to BRINE or specimens.


### Storage layout v4
The secured rack now shares the shelving side, with an offset handling platform,
packing bench and flush corner marks defining an empty receiving position.
Selected card: storage_bay-card-organic-v4.png. The previous v3 layout failed six
non-overlap assertions after wall containment shifted tall shelves; it is retained
as negative evidence. The narrower rack in v4 passes all four rotations and 1456
route samples, state/pause and containment at 1280x720, without runtime errors:
output/production-ten/storage-layout-v4-1280. Card and q1/q3 captures reviewed.
This improves functional grouping but still leaves broad circulation; it is not
full-room aesthetic acceptance or a fresh packaged traversal result.


### Mining Drone Bay support pass
Tool trolley, component worktable and hooded inspection lamp occupy the sealed
side work areas between drone machinery. Supported meter, fittings and tools come
from the existing maintenance-support-v1 atlas through its registered silhouette
pieces; this RGB source must never be drawn as a transparent rectangle. No new
raster generation or raster edits. Tether/service lines connect equipment anchors;
flush drain ribs sit beside the component table. New furniture remains static.
Native evidence: output/production-ten/mining-organic-v1-1280, seven assemblies,
four rotations, 728 route samples, state/pause/containment/nonoverlap all pass with
no runtime errors. Selected card mining_drone_bay-card-organic-v1.png and q1/q3
captures inspected. Packaged checks and final aesthetic acceptance remain pending.
Seven rooms now have revisions; 27 remain at brief stage. This changes furnishing
between the main assemblies but does not establish final natural composition.


### Salvage Drone Bay intake pass
Shared logistics bench provides a scanner, manifest, sealed recovery case, clamped
lamp and under-surface collection bins beside the sorter. The source is unchanged
storage-packing-bench-v3.png, clipped by the existing alpha registration. Winch to
hatch service routing and a flush drainage strip occupy the sealed right side.
Native evidence output/production-ten/salvage-organic-v1-1280 passes five assemblies,
four rotations, 728 routes, state/pause/containment and nonoverlap, with no runtime
errors. Card salvage_drone_bay-card-organic-v1.png and q3 capture reviewed.
Major perimeter placement remains apparent: furnishing progress is not final visual
acceptance. Eight identities have revisions; 26 remain at brief stage. Current
packaged and close actor-occlusion verification remain outstanding.


### Command chart cabinet pass
New command-credenza-v1.png supplies finished grey and burgundy furniture with
physically supported navigation charts, headset, binders, lamp and lower storage.
Source is unchanged; command-credenza-registration-v1.json clips faint exterior
alpha haze. Exact prompt is preserved. Quarter-specific positions avoid consoles
while keeping all four doors accessible. Native command-organic-v1-1280 passes
five assemblies, four rotations, 1456 routes, state/pause/containment/nonoverlap,
without runtime errors. Card command_center-card-organic-v1.png and q3 inspected.
Central operations layout is still unfinished: adding this cabinet is not that
redesign. Nine identities have furnishing revisions, 25 remain at brief stage.
Packaged and final visual acceptance remain pending.


### Quarantine preparation pass
A clinical preparation surface with supported instruments and lamp occupies the
sealed north-wall space between berth and filtration. A sealed cooler sits by the
southern monitoring/storage area. Existing research-island-v2 and research-v1
sources are reused unchanged. Filtration routing follows the sealed northern wall;
flush markings define the preparation and collection positions. East/west doors
remain clear. Native quarantine-organic-v1-1280 passes six assemblies, four rotations,
728 routes, state/pause/containment/nonoverlap with no runtime errors. Card
quarantine_cell-card-organic-v1.png and q1 inspected. Packaged, actor occlusion and
final visual acceptance remain outstanding. All ten original production identities
now have initial furnishing revisions; 24 other identities remain at brief stage.
These revisions do not complete the all-room natural composition objective.


### Crew Hab shared-living pass
A book cabinet occupies the sealed north-wall space between berths. A coat stand
serves the sleeping area; a reading lamp and one rug accompany the chair. Reuses
unchanged lounge-support-v2 alpha art with source registrations. Native evidence
output/production-ten/hab-organic-v1-1280 passes seven assemblies, all rotations,
state/pause/containment and the base fixture routes without runtime errors.
output/hab-organic-audit.log independently finds no floor overlaps in any quarter.
Card crew-hab-card-organic-v1.png inspected. Packaged, actor occlusion and final
visual acceptance pending. Eleven identities have revisions, 23 remain at brief
stage. The pre-Hab read-only manifest audit matched all 25 component/profile hashes;
that is source integrity, not packaged execution evidence.


### Med Bay preparation pass
A supported preparation surface and task lamp occupy the sealed north wall;
a sealed cooler serves the treatment side. Sources research-island-v2 and research-v1
are reused unchanged. Card med-bay-card-organic-v2.png inspected. Native
output/production-ten/med-organic-v2-1280 passes four rotations, 808 actual entry
samples, containment/nonoverlap, powered/offline host checks and socket infill,
without runtime errors. The earlier v1 placement failed one image-based host-state
check because the preparation capture overlapped moving neighboring equipment.
V2 separates the furniture visually; the test retains static checks for new furniture
and moving checks for original equipment. Twelve identities have revisions; 22 remain
at brief stage. Packaged and final aesthetic acceptance remain outstanding.


### Life Support service pass
A diagnostic cart sits alongside the tank, and a pressure bottle serves the wall-side
filter line with a flush cover across the service run. Reuses unchanged battery cart
and registered maintenance bottle. Floor drains now belong only to fluid equipment,
not every prop. V1 put furniture too prominently ahead of main equipment; v2 moves
it beside its task. Card life-support-card-organic-v2.png inspected. Native
life-organic-v2-1280 passes six assemblies, four rotations, state/pause/containment
and base routes without runtime errors. Independent audit-v2 finds no floor overlaps
in any quarter. Thirteen identities have revisions; 21 remain at brief stage.
Packaged and final natural-composition acceptance remain outstanding.


### Thirteen-room packaged follow-up
output/room-rollout/windows-organic-thirteen-v1 completed all 51 arrivals, visited
51 rooms and crossed 135 reciprocal transitions over 10,337 movement samples.
It FAILS one collision-clearance assertion; traversal acceptance is not established.
Asset loading passed: 34 selected source hashes, 68 raw source/card PNG decodes,
22 component hashes/decodes and 12 profile hashes/parses. This build contains all
13 current furnishing revisions. Earlier packaged passes predate these revisions.
The fixture now prints exact collision sample positions and target cell on future
failures, preserving the existing assertion. The failing build predates that diagnostic.
The new read-only dependency audit passes all 12 profiles; its focused test verifies
undeclared textures, stale hashes and Windows path normalization. This is a pipeline
improvement, not organic composition acceptance. Collision repair remains outstanding.


### Current-controller native follow-up
output/room-rollout/native-thirteen-diagnostic-v1 passes all 51 arrivals/visited rooms,
137 reciprocal transitions and 11,108 collision/speed samples with no runtime errors.
Controller hash FFE25488002785A2BE38F531D340F5B17EF5AA623827C8D771C1F730212B3F8D
differs from failed packaged hash 25A06732CC77336CA9F5162A8E232F406B7C34851E17208443053B2CD305CE1C.
This is current-workspace native evidence, not reproduction or explanation of the
old packaged collision. No controller repair was made in this follow-up. The possible
multi-waypoint chord explanation remains an unverified hypothesis. Fresh packaged
verification remains required; thirteen furnishing revisions are still not final
natural-composition acceptance.


### Hydroponics potting trolley
New hydro-potting-trolley-v1.png provides supported seedlings, pruning tools, lamp,
and under-surface hose/bottle storage. Exact prompt and unchanged source preserved;
alpha registration clips exterior haze without editing the raster. It sits alongside
the harvest unit. Native hydro-organic-v1-1280 passes five assemblies and four-rotation
state/pause/containment/base routes without errors; separate audit finds no floor
overlaps. Card hydroponics-card-organic-v1.png inspected. Trolley reads small at
512-square scale; overall activity layout and visual acceptance remain unfinished.
Fourteen identities have revisions, twenty remain at brief stage.

Packaged windows-organic-thirteen-v2 did not run cleanly: its captured Salvage view
referenced undeclared drone_deployed, preventing compilation. Current source now
contains that declaration. Preserve failed build; it is not traversal evidence.
The 34 sources/68 PNGs, 22 components and 12 profiles passed asset checks before
runtime validation failed. Hydroponics was added after that build's snapshot.


Hydroponics v2 scale correction: trolley width increased from 28 to 42 room units
and repositioned alongside harvest machinery. Selected card is now
hydroponics-card-organic-v2.png, inspected at 512 square. Native
hydro-organic-v2-1280 passes four rotations/state/pause/containment/base routes
without runtime errors; audit-v2 finds no floor overlaps. The complete room layout
still requires refinement. This revision improves scale, not catalog completion.


### Nursery supplies pass
A reagent/supply trolley sits between the growing rack and analytical bench on the
sealed north side. Reuses research-v1 unchanged. Nursery-specific furnished view
extends the older source-pixel renderer; other subclasses do not inherit these props.
New script UID generated through Godot ResourceUID API and kept paired. Floor drains
now serve reservoir/filter only. Native nursery-organic-v1-1280 passes 8 motion
comparisons, 404 real path samples, 28 walking captures and 4 paused pairs without
runtime errors. Separate four-quarter audit finds no floor overlaps. Selected
nursery-card-organic-v1.png inspected. Fifteen identities have initial revisions,
19 remain at brief stage; complete layout/visual and packaged acceptance pending.


### Reactor service corner
Supported repair table and task lamp occupy the southwest corner, using registered
maintenance-support-v1 silhouettes unchanged. Initial north-side placement passed
visual containment but failed 31 route assertions; v2 moves the activity into unused
corner space. Native reactor-organic-v2-1280 passes station state/pause checks,
404 paired walker samples, additional reactor perimeter assertions and 40-room fit
checks without runtime errors. Card reactor-card-organic-v2.png inspected. Sixteen
identities have initial revisions, eighteen remain at brief stage. Full composition
and packaged acceptance remain outstanding.


### Medical Office reference furniture
Reading lamp serves the desk; a shared wooden book cabinet with books and small
decorations occupies the sealed side wall between records and consultation. A single
mat anchors consultation seats. Reuses lounge-support-v2 unchanged. V1 mistakenly
occupied a north/south route; v2 passes all rotations, four actual economy states,
808 socket samples and host checks without runtime errors. Card
med_office-card-organic-v2.png inspected. Evidence: office-organic-v2-1280.
Seventeen identities have initial revisions; seventeen remain at brief stage.
Complete natural composition and packaged acceptance remain outstanding.


### Cryo supplies pass
Supply trolley and sealed transfer cooler reuse research-v1 beside the pod-service
areas. Discovered recovery wards exclude these ordinary-room additions. Card
cryo_chamber-card-organic-v1.png inspected. Native cryo-organic-v2-1280 passes four
rotations, powered/starved/suspended states, source/service containment and base
checks. Audit finds no floor overlaps; cryo recovery test passes. Initial test wrongly
required new static furniture to animate; revised expectation checks both static
furniture and original animated hosts. Eighteen identities have initial revisions;
sixteen remain at brief stage. Full visual and packaged acceptance remain pending.


### Clone Lab preparation pass
Shared research-island-v2 supplies supported instruments and lamp between vessel
and incubator. V1/v2 overlapped tall neighboring artwork in rotated views despite
separate floor footprints. V3 reduces width to 54 units and authors quarter positions
inside the actual visual gap. Native clone-organic-v3-1280 passes all rotations,
six economy states, 1212 socket samples and visual/service bounds without errors.
Selected clone_lab-card-organic-v3.png inspected. The read-only composition audit
now reports visual_overlaps separately from floor overlaps. Nineteen identities have
initial revisions; fifteen remain at brief stage. Final visual and packaged acceptance
remain pending. Earlier missing external asset errors are preserved in failed runs.


### Archive service cart
New archive-service-cart-v1.png supplies supported data caddies, diagnostic pad,
patch cables and protected lower storage. Source raster unchanged; exact prompt and
alpha registration preserved. Quarter-specific positions retain the tall racks' visual
clearance. Native archive-organic-v1-1280 passes five assemblies, all rotations,
three economy states, aperture/assembly containment and base state/route checks
without errors. Card data_archive-card-organic-v1.png inspected. Twenty identities
have initial revisions; fourteen remain at brief stage. Complete activity layout,
actor occlusion and packaged acceptance remain outstanding.

## Biodome activity-area revision

Biodome v2 integrates a cultivation cart with tools and a task lamp on its worktop, a work mat, staggered planting beds, edge irrigation connections and a flush service drain. The floor dressing is explicitly drawn below furniture and adds no collision. Selected card: `rooms/underwater/batch-two/biodome-card-organic-v2.png`. Native evidence: `output/biodome-organic-v2.log` and `output/production-ten/biodome-organic-v2-1280`; four rotations, four economy cases and 808 socket-route samples passed with no assertion failures. The dependency audit passes all 20 profile records.

This is an initial revision, not completed natural composition: the large assemblies still dominate four perimeter areas. Further work must change relationships and scale, rather than count added accessories as success. There are now 21 initial room revisions and 13 remaining brief-stage identities; owner visual acceptance and current whole-catalog packaged verification remain outstanding.

## Xeno Lab containment layout

Xeno v2 moves the vessel from a corner to the north focal position, places its service cart alongside, and arranges scanner and preparation stations along the east side with sample storage to the west. A source-anchored conduit connects containment and scanning; the preparation pad is floor-only. Existing specimen effects remain stateful; the cart is static. Selected card: `rooms/underwater/batch-two/xeno_lab-card-organic-v2.png`. Native fixture `output/xeno-organic-v2.log` passes four rotations, three economy states and 404 socket samples. `output/xeno-organic-audit-v2.log` reports no floor or visual overlaps in any quarter. V1 is preserved as the rejected isolated-cart placement.

22 identities now have initial furnishing revisions; 12 remain at brief stage. This count does not establish natural-layout completion. Xeno still needs more purpose-specific surface detail and full packaged review; the whole catalog retains its visual revision gates.

## Anomaly Lab monitoring layout

The containment platform now anchors the north of the room, with a supported recording cart beside it and a floor conduit to the diagnostic equipment on the east. Capacitors and receiver remain separate support stations. Anomaly explicitly replaces its inherited Xeno dressing profile after replacing the machinery list. Native evidence `output/anomaly-organic-v1.log` passes four rotations, three economy states, visual nonoverlap and 404 socket samples. Card: `rooms/underwater/batch-two/anomaly_lab-card-organic-v1.png`.

23 identities now have initial furnishing revisions; 11 remain brief-stage. Additional fine instrumentation and stronger room-specific floor treatment are still pending, as are catalog visual and packaged acceptance.

## Bio Lab preparation area

A supported preparation bench with instruments and task lamp occupies the sealed north work area beside culture processing. A floor mat and short service hose connect the work area; the reactors are staggered. Bio explicitly replaces inherited Biodome furnishings. Native `output/bio-organic-v1.log` passes four rotations, five economy states including restoration and 1212 socket samples. The independent audit reports no floor or visual overlaps. V2 changes only hose bends, reviewed in `rooms/underwater/batch-two/bio_lab-card-organic-v2.png`; no placement or motion changes followed the native run.

24 identities have initial furnishing revisions and 10 remain brief-stage. Bio retains four major perimeter assemblies and needs further visual composition refinement. These counts do not establish catalog completion or packaged acceptance.

## Medical Center bedside supplies

V2 places a supported care trolley beside treatment rather than isolated mid-room. Its mat is floor-only and its furniture is static. Native `output/med-center-organic-v2.log` passes four rotations, four economy cases and 808 socket samples; the matching audit reports no floor or visual overlaps. Medical Office clears the inherited center dressing before selecting its own profile. Its inheritance audit retains six office assemblies with no floor overlaps; desk/lamp artwork bounds overlap and remain a visual-review item, not an asserted pass.

25 identities have initial revisions; 9 remain brief-stage. Medical Center still retains the four-perimeter composition and needs further visual refinement. No whole-catalog acceptance is claimed.

## Radio Lab electronics bench

New preserved RGBA `rooms/underwater/acoustic-comms/electronics-bench-v1.png` supplies a meter, headset on cloth, connector case, tool tray, patch lead, attached lamp and lower-shelf instrument cases as one supported assembly. The exact prompt and original path are preserved beside it. Read-only alpha registration yields seven polygons; no raster editing was applied. The bench joins receiver and hydrophone servicing along the lower sealed wall with a floor mat and short receiver lead. Native `output/radio-organic-v1.log` passes four rotations, offline/pause and 728 aisle samples. The independent audit reports no floor or visual overlaps.

26 identities have initial furnishing revisions; 8 remain brief-stage. Current larger-layout and packaged acceptance gates remain open. The selected card was reviewed at 512 pixels; additional close actor review remains outstanding.

## Hull integrity calibration area

Shield Generator uses the preserved electronics bench as a calibration station beside the hull test rig, with a work mat and wall-edge service connection. Instruments, patch leads and cases stay supported on bench/shelf. This follows the actual hull-integrity equipment identity rather than inventing a field emitter. Native `output/hull-organic-v1.log` passes four rotations, offline/pause and 728 aisle samples; matching audit reports no floor or artwork overlap. Selected card: `rooms/underwater/hull-integrity/shield_generator-card-organic-v1.png`.

27 identities now have initial furnishing revisions, with 7 brief-stage identities remaining. Larger layout refinement, actor-scale review and current whole-catalog packaged verification remain outstanding.

## Thermal control service area

Solar Array uses its implemented thermal-control identity: a service table beside the pumps, connected floor hose and mat, plus a pressure bottle beside the converter. V1 placed the bottle too independently; v2 groups it beside equipment with quarter-specific placement. Native `output/thermal-organic-v2.log` passes four rotations, offline/pause and 728 corner-route samples. `output/thermal-organic-audit-v3.log` confirms no floor or visual overlaps. The earlier v1 audit failed on a duplicate method introduced during integration; that process was stopped and the existing topology method retained.

28 identities now have initial furnishing revisions; 6 remain brief-stage. Larger layouts and full-catalog visual/package acceptance remain incomplete.

## Tidal Condenser sampling area

A washable instrument bench with task lamp occupies the sealed north work area beside the collection tanks. Its supported tools, short sample service line and mat give sampling a physical location without obstructing the east/south/west tee. Native `output/tidal-organic-v1.log` passes four rotations, offline/pause and 1092 aisle samples. The independent audit reports no floor or artwork overlaps. Card: `rooms/underwater/tidal-condenser/tidal_condenser-card-organic-v1.png`.

29 identities now have initial furnishing revisions and 5 remain brief-stage. Pump-side furnishing and larger layout refinement remain outstanding; these counts do not establish catalog completion.

## Holographic Core calibration support

A compact dark calibration cart sits beside the projector with supported instruments, task lamp and lower storage. A short service lead and floor pad stay within its quadrant, preserving all four entrances. The view replaces inherited Archive furnishing data and draws the floor profile explicitly. Native `output/holo-organic-v1.log` passes four rotations, four economy states including restoration and 1616 socket samples. Its independent audit reports no floor or artwork overlaps. Card: `rooms/underwater/batch-two/holographic_core-card-organic-v1.png`.

30 identities have initial revisions; 4 remain brief-stage. Main four-corner composition remains a visual limitation; current whole-catalog packaged acceptance remains unproven.

## Gravity Loom calibration station

A supported calibration bench now sits southwest of the central apparatus, connected by a floor-only control conduit with a work mat beneath it. V1 isolated the bench too far into the corner; v2 brings it closer. Existing field motion remains confined to the loom while the bench stays static. Native `output/gravity-organic-v2.log` passes four rotations, offline/pause and a new 1440-position inner-perimeter clearance check. Card: `rooms/underwater/gravity-loom/gravity_loom-card-organic-v2.png`.

31 identities have initial furnishing revisions, with corridor, corner and BRINE core still brief-stage. Additional visual refinement and current full-catalog package proof remain outstanding.

## Corridor and Corner wall services

Both routing identities now include a recessed cabinet in the wall band and staggered inspection lamps. Corner lighting follows the turn; straight lighting alternates sides. Existing edge conduits, drainage and inspection hatch remain floor/structure details with no new collision. `output/routing-organic-bounds-v1.log` passes 420 fitting-corner samples within hull and outside tapered approaches. `output/routing-organic-v1.log` passes 1616 actual narrow-room walker samples across four rotations, both directions, power states and incompatible sockets. Both cards and the dedicated station-q3-rtrue-leg2-step65 traversal capture were reviewed; the generic station-q3 image belongs to the base fixture and is not routing evidence.

The corridor baker now accepts a filename suffix, preserving earlier exports while producing matching card revisions. 33 identities have initial revisions; BRINE Core remains brief-stage. Full-catalog visual refinement and current packaged acceptance remain unfinished.

## BRINE observation pedestal and current catalog reconciliation

A new preserved pearl observation pedestal with docked dark tablet sits southwest of the chamber. Its true-alpha source and exact prompt are preserved under `rooms/underwater/brine-core`; one registered polygon renders it without a floor rectangle. Native `output/brine-organic-v1.log` passes four rotations, static pedestal behavior, independent body/bubbles/light states and 1440 chamber-perimeter samples. Card: `rooms/underwater/brine-core/card-organic-v1.png`.

The current database contains 35 room identities, not the historical 34: Construction Drone Bay was added by ongoing game development. It has now been added to the furnishing ledger with a room-specific brief. All original 34 have initial revisions, while Construction Drone Bay still needs its pass. Initial coverage does not satisfy the requested natural compositions: larger layout revisions, close actor review and full packaged verification remain outstanding.

## Construction Drone Bay service supplies

Parts trolley, supported tools, a standing inspection lamp and work pad occupy the fabrication side of the bay. The lamp overhangs the trolley intentionally; floor footprints remain separate in all rotations. V1 retained donor lamp positions and the new test accidentally closed the doors under test; both corrected in v2. Native `output/construction-organic-v2.log` passes four rotations, static-state/pause checks and 808 socket samples. Existing drone deployment code remains unchanged. New fixture has its paired Godot UID. Card: `rooms/production-ten/construction_drone_bay-card-organic-v2.png`. Packaging must include `rooms/production-ten/construction-manifest.json` with the other manifests.

All 35 current identities now have initial furnishing revisions. This is coverage, not completion: the four-corner layout remains in many rooms, full natural-composition review is outstanding, and the current catalog still lacks a passing standalone package. The next phase must refine those layouts rather than add another token accessory to each.

## Command Center activity-layout revision

The four equal corner assemblies are replaced by a paired control station, larger planning table and separate communications station. The chart credenza remains a secondary work surface. Two smaller consoles share a floor work area and service connection; explicit quarter placement preserves the pair without overlapping their full artwork. Card `rooms/production-ten/command_center-card-activity-v2.png` and q1 room capture were reviewed. Native `output/command-activity-v2.log` passes four rotations, offline/pause, screen envelopes, disconnected walls and 1456 center-to-door samples.

V1 route checks passed but its screen-position assertion failed: that assertion encoded the old fixed 36-unit cross band rather than equipment containment. It now verifies transformed effects remain within their registered artwork; source-screen and actual walking-route checks are retained. This is not final visual acceptance, and no packaged success is claimed.

## Full current catalog standalone verification

`output/room-rollout/windows-organic-35-v2/verification.json` passes all 35 source identities, 70 source/card PNG decodes, 47 component records and 32 profile hashes/parses. The controlled tour reaches 53 rooms with 139 reciprocal transitions and 10658 collision/speed samples. This supersedes earlier missing-package status for this exact snapshot, while preserving the failed attempts. V1 failed UTF-8 import; the shared worktree was corrected before the attempted local repair, and v2 succeeded. No encoding repair was applied by this pass. See `docs/ROOM_FURNISHING_STATUS.md` for the current scope and remaining visual work.

## Battery Array activity-layout revision

The banks retain visual priority while breaker and distribution controls form one smaller station on a shared floor pad. A larger service cart and cable reel occupy their own work area. The covered feeder still connects banks to controls; an obsolete cross-room reel connection was removed. Duplicate post-registration footprint overrides were removed so each original machine has one authored footprint. A quarter-specific reel placement avoids tall-cart overlap.

Native `output/battery-activity-v2.log` passes four rotations, motion/offline/pause and 1456 center-to-port samples. `output/battery-activity-audit-v2.log` reports no floor or artwork overlaps. Card `rooms/production-ten/battery_array-card-activity-v2.png` was reviewed. This revision follows the passing 35-room package snapshot and therefore is not covered by that earlier package hash. Further close actor review remains outstanding.

## Full furnishing-helper audit

The native preflight now discovers Dressing instances by script identity rather than the property name `dressing`, and includes furniture IDs in reference validation. Its first expanded run caught retained Cryo helpers in Medical Center and Medical Office. Medical Center now clears that inherited helper after replacing the base room; Medical Office inherits the cleanup. The positive audit passes 32 profiles and 480 references over all 35 live room identities. Deliberate missing `office_dressing` host and unmapped database identity controls exit with failure as expected. Both clinical native fixtures pass after cleanup. Evidence: `output/dressing-helpers-positive.log`, matching negative-control logs, and `output/med-center-helper-cleanup.log` / `output/med-office-helper-cleanup.log`. This improves validation coverage without claiming further visual completion.

## Storage Bay activity-layout revision

Incoming crates and lift now share a receiving pad; smaller secured storage sits beside shelving, packing retains its supported workbench, and a small case occupies the marked staging area. The lift-supported case is resized with its support. Main footprint overrides are consolidated, with narrow quarter-specific adjustments for tall shelving and lift silhouettes. V1 exposed shelf/rack artwork overlap; v2 resolved it; v3 adds the staged case. Native `output/storage-activity-v3.log` passes six assemblies in four rotations, passive/offline/pause, disconnected walls and 1456 center-to-door samples. The selected card was reviewed. This postdates the recorded package snapshot, and close actor review remains open.


## Storage work-area and crew review (activity v5)

The packing bench now shares a standing task light and short floor lead using the existing maintenance support source. The secured rack moves 18 units south in q0 to clear the shelf-front standing pose. Profile storage-composition-v3.json and card storage_bay-card-activity-v5.png are selected in the manifest and card consumers. No cargo or NPC behavior changed.

Native storage-activity-v5 passes seven assemblies, four rotations and 1,456 route samples. storage-crew-depth-v3/review.json passes 84 static ordering probes with all 28 sampled front positions standable. Forced overlaps are diagnostic positions, not walking evidence. The q3 packing-bench close capture and v5 card were inspected; lamp overhang above the work area is intentional. The generalized depth tool also preserves its default mining/salvage regression: 48 poses, zero failures. Full-room captures now include the floor layer; isolated ordering comparisons still omit it.

This is a local improvement, not natural-layout acceptance for Storage or the remaining rooms. Broad empty areas remain. The Windows 35-room package predates this revision.


## Research Lab activity layout v2

The specimen station and analyzer now share the sealed rear wall and a restrained floor work zone. The sample cabinet is smaller beside them. A larger preparation island on the entry aisle shows its attached lamp, sample rack, papers and instrument on a physical work surface; the reagent trolley supports this area. The scanner retains separate working space. The former long cross-room lead was rejected during review and replaced with a local bench-to-trolley lead. Canonical footprints now have one definition rather than later overrides. Quarter-specific cooler/trolley placements resolve two rotated art-envelope overlaps.

Profile research-composition-v2.json and card research_lab-card-activity-v2.png are selected by manifest and card consumers. The native v2 fixture passes seven assemblies, all rotations, operating/offline/pause and 364 center-to-port samples. Composition audit v2 has no ground or visual-envelope overlaps. Final research-crew-depth-v2 records 84 static depth probes, with all 28 sampled fronts standable. The v2 card and close preparation-area captures were reviewed. These checks do not prove autonomous activity selection or final station-scale composition. Updated packaging remains pending.


## Maintenance Bay activity layout v2

A larger 90-unit repair table now sits between the repair machine and tool wall along the sealed rear side. Supported workpiece and hand tools remain on the table, with a standing task light alongside. The panel rack and parts trolley form a smaller staging group; compact diagnostics and a pressure bottle share a short service connection. One canonical footprint per machine replaces the former late overrides. Quarter-specific lamp and bottle placements avoid unrelated silhouettes while preserving the room tee routes.

The v2 native fixture passes eight assemblies, four rotations, operating/offline/pause and 1,092 route samples. Audit v2 has no ground overlaps; lamp/table visual-envelope intersections in q0-q2 are intentional overhead reach. The 96-pose maintenance-crew-depth-v1 review has no ordering failures, and all 32 sampled fronts are standable. The q0 close repair-table capture was inspected. Profile maintenance-composition-v2.json and card maintenance_bay-card-activity-v2.png are selected. New package and final station-scale visual acceptance remain pending.


## Quarantine care/work groups (activity v2)

The larger berth and smaller monitor share the north care zone, with dedicated filtration toward the opposite end. The supply cabinet, enlarged preparation surface and cooler form a southern clean-work group. The preparation lamp, samples and instrument remain supported by the table. A perimeter filter connection and restrained floor zones communicate the separation without adding collision. The q3 cooler moved away from the cabinet after its front standing pose failed the first crew review.

Audit v2 has no ground or visual-envelope overlaps in any rotation. The native v3 fixture passes six assemblies, four rotations, state/pause checks and 728 center-to-door samples. Its old effect test incorrectly reserved a four-way cross in this east-west room: it now verifies the equipment envelope and the actual east-west aisle in canonical coordinates. Actual doorway and route tests remain intact. Quarantine crew-depth-v2 passes 72 static probes; all 24 sampled fronts are standable. The q0 berth close view and v2 card were inspected. Profile quarantine-composition-v2.json and card quarantine_cell-card-activity-v2.png are selected. This revision postdates the Windows v5 snapshot; station-scale review and updated package remain pending.


## Ore Refinery processing and assay layout (activity v2)

Crusher and hopper now occupy one side of the north-south aisle, with a nearby assay bench; vessels and sorter occupy the other. The pressure unit has a short direct service connection. A subdued work-zone pad groups the crusher/hopper. The first 104-unit assay bench was too large and visually collided with the hopper; the final 82-unit surface restores hierarchy while retaining readable supported dishes, instrument and lamp. The q2 crusher shifts toward the wall to preserve upright silhouette separation. Existing floor drain detail remains.

Audit v2 has no ground or visual-envelope overlaps in four rotations. Native v2 passes six assemblies, state/pause/effect checks and 728 route samples. The effect test now checks actual equipment bounds and the canonical north-south aisle, replacing an obsolete four-way-cross restriction without changing door geometry. Crew-depth-v1 passes 72 static probes with all 24 sampled fronts standable. The q0 assay-bench close capture was inspected. Profile refinery-composition-v2.json and card ore_refinery-card-activity-v2.png are selected. This revision postdates Windows v5 and awaits station-scale review and updated packaging.


## Crew Hab sleeping/reading/work layout

Two berths now form a sleeping area, with books and a reading chair/lamp together and a separate desk/coat-stand group. Personal objects remain on the bookshelf and desk. Long upright bed silhouettes require explicit q1/q3 spacing rather than a mechanical rotation of the initial positions. A q1 coat stand also moved closer to the desk after it obstructed a production-controller diagonal approach.

Profile crew-hab-composition-v2.json and card crew-hab-card-activity-v1.png are selected. Native state v2 passes seven assemblies and all rotations. Composition audit v3 has no ground overlaps; the q3 chair/lamp envelope intersection was reviewed in the close capture. Crew-depth-v2 checks 84 static poses. The current-controller tour v3 passes four rotated tee layouts, 16 arrivals, 20 reciprocal transitions and 1,617 movement samples. Per-quarter traces remain under output/production-ten/crew-hab-current-routes-v3-1280. This is scheduled traversal, not autonomous destination-choice acceptance. Station-scale review and packaging remain pending after Windows v5.

The older whole-room pair fixture failed 202 assertions: it varied legacy test_walker_progress while get_test_walker_position returned an active Bill position, so those repeated samples did not measure their claimed interpolation. It is not passing movement evidence. The new --crew-hab-tour option on the production station fixture uses the current controller. Its v1 setup missed an occupied starting cell in one rotation; v2 then exposed the coat-stand approach issue; v3 passes after correcting both. Keep failed outputs.


## Med Bay treatment/preparation layout

The two treatment beds share a ward area, with the main console nearby and the preparation surface, supply cabinet and sealed cooler grouped separately. Existing IV stands, bedside monitors, preparation lamp and tabletop supplies remain supported by their source assemblies. Side rotations use explicit spacing for the second bed; the q3 preparation table moves below the entrance aisle rather than colliding with the cabinet.

Med Bay activity v2 passes four-rotation containment, hardware gaps, powered/offline state and socket-infill checks in --state-only mode. The old progress-based walker loop is explicitly skipped and its output no longer calls those samples current movement. The new --med-bay-tour uses the actual controller and returns to its starting room: 12 arrivals, 8 reciprocal transitions and 699 movement samples across four rotated two-room layouts. Audit v2 has no ground or visual-envelope overlaps. Crew-depth-v1 passes 72 static poses with all 24 sampled fronts standable. The card and q1 bedside capture were reviewed. Profile med-bay-composition-v2.json and card med-bay-card-activity-v1.png are selected. Station-scale and package checks remain pending after Windows v5.

The shared focused-tour return-to-start extension also passes Crew Hab regression v4: 20 arrivals, 24 transitions and 1,958 production movement samples. This extends the earlier 16-arrival proof rather than replacing its historical trace.


## Nursery cultivation layout

The growing rack now anchors the rear area. The preparation bench and larger supply trolley form a work area; the reservoir and filter retain their local service details. Only nursery_furnished_view.gd repositions source-pixel assemblies. Art offsets, ground rectangles and sort anchors move together, preserving the original extraction and functioning effects. Quarter-specific spacing resolves silhouette and footprint overlaps without changing the shared parent renderer. Profile nursery-composition-v2.json and card nursery-card-activity-v1.png are selected.

Audit v2 has no ground or visual-envelope overlaps. Native state-only v2 passes eight motion comparisons and four paused pairs. The base fixture explicitly skips its legacy progress loop in this mode and no longer calls those samples current-controller movement. Nursery crew-depth-v1 passes 60 static probes with all 20 sampled front positions standable. The v1 card was visually reviewed. Current nursery tour v2 passes four rotated tees and return trips: 20 arrivals, 24 transitions and 1,967 movement samples.

The first tour failed before movement because the current architect-presence gate required recovered Bill. Before an attempted local patch applied, the shared worktree already acquired production core-wake setup in controlled_tour; that change was preserved and used for the passing rerun. No gameplay lifecycle change was made by this furnishing pass. The passing tour has Bill present and the other architects absent, as recorded by its setup line. Station-scale review and updated packaging remain pending after Windows v6.


### Reviewed decoration libraries in live rooms — 2026-09-06

All 40 current room identities now consume appropriate revised decoration art.
Use `rooms/decoration-integration/manifest.json` for selected card hashes and raw
asset dependencies. Shared floor replacements retain authored host-relative pads,
service endpoints and layer order. Low hull fittings fit existing solid segments;
a library asset's suggested height never changes the room wall height. Larger
furniture, machinery and interactive overlays retain their existing renderers.

Verification: 320 native rotation/state renders, 37 shared-edge room captures,
and 28 low-wall station captures with zero failures. The host audit resolves 875
active references with zero errors; three rare q0 baked interiors explicitly
suppress their dressing profiles and use separate aisle covers. The audit now
records those exceptions and still checks all other rotations. Native pictures
are under `output/decoration-integration/` and `output/decoration-station/`.
New cards are selected in GridCanvas, including all corridor variants. Export
filters include raw PNG/JSON; no new executable was built during this pass.
