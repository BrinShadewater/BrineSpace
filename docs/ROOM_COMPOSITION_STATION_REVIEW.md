# Room composition at station scale

The current review captures are in `output/production-ten/activity-station-v3-1600`. The optional `--composition-review` flag on `tests/playtest_production_ten_station.gd`, used with `--controlled-tour`, captures each unique room after the traversal. This run contains the original ten production identities, not all 35 identities.

The manifest records 52% zoom for all ten views. `cell_pixels` is the logical canvas cell size (320.112), not physical screenshot pixels after viewport scaling. Screenshots are 1600 by 900. Real station neighbours and retained crew positions remain visible. Capturing a room does not imply visual acceptance.

## Reviewed findings

- The Maintenance-focused frame also shows Research and Storage. The enlarged Research preparation surface and Maintenance repair surface retain their role at this scale. Storage remains comparatively sparse; its floor marks establish zones but do not finish the cargo story.
- The Quarantine-focused frame shows its four detached major assemblies and small clinical accessories. It needs a purposeful berth/observation/filtration arrangement. Neighbouring Command retains substantial unstructured empty floor despite its paired controls.
- The Ore Refinery frame still reads as four separate machines. Its next layout should make the processing sequence and assay/service area legible while keeping the actual north/south route clear.

These observations prioritize Quarantine and Ore Refinery for further composition. They do not certify the other rooms or settle final aesthetic acceptance.

## Technical evidence and rejected runs

Native station v3 passes 15 arrivals, 15 visited rooms, 37 reciprocal transitions and 2,824 collision/speed samples. All ten sources, twenty source/card PNG decodes, nineteen component records and nine profiles pass. All ten focused PNGs exist. Existing image-loader warnings remain.

Station v1 supplied only a 22% overview. Station v2 failed the new capture method because it referenced a nonexistent room `cell` field; v3 uses the authoritative occupied-cell map. Do not use v2's zero assertion count as success: its error log contains the failed capture.

Windows 35-room v3 exposed an incomplete SceneTree-to-Node frame-wait conversion in the export bridge. The generator now converts the station fixture as well as the base fixture. Windows v4 failed on an invocation typo in the Gravity Loom manifest path. The export helper now checks additional manifest existence and nonempty array shape before creating an export directory; single-entry arrays are preserved with `ConvertFrom-Json -NoEnumerate`. A deliberate missing-manifest invocation was rejected without creating a directory.


## Fresh Windows result

Windows organic-35-v5 passes the corrected export bridge and preflight. It verifies 35 sources, 70 source/card decodes, 48 component records and 32 profiles. All 53 placed rooms were reached through 139 reciprocal transitions with 10,682 collision/speed samples. The host preflight checks 492 references. The executable ran from an external working directory. No script/assertion errors were logged; image-loader warnings remain. This package uses the overview tour; the optional 52% captures above are native evidence, not packaged captures.


## Sixteen-room native review v4

The original ten plus the six whole-room manifest identities were captured at 52% in output/production-ten/activity-station-v4-1600. All sixteen focused PNGs exist. The controlled tour passes 24 arrivals, 62 reciprocal transitions and 4,732 movement samples; asset checks cover sixteen sources, 32 source/card decodes, 27 component records and fifteen profiles.

Med Bay, Crew Hab, Quarantine and Ore Refinery focused frames were reviewed. The paired beds, reading corner, care/preparation separation and processing/assay group remain visible at play scale. This is a local readability improvement, not final natural-room acceptance. Neighbouring Nursery still retains separated quadrant machinery and should be a next composition target; Storage remains sparse. The views preserve neighbours and current crew, rather than rendering isolated cards.

The exporter now accepts -CompositionReview with -ControlledTour, forwards the native capture option and checks focused capture count, zoom and file presence. A negative invocation without ControlledTour was rejected before creating its output directory. Captured images still require visual inspection.


## Windows v6 with focused views

Windows organic-35-v6 passes all 35 source hashes, 70 source/card PNG decodes, 48 component records and 32 profiles. The tour reached 53 placed rooms with 139 reciprocal transitions and 10,681 movement samples from an external working directory. All 35 unique identities have 52% focused captures; a separate read-only decode inventory confirms 1600x900 PNGs and records their hashes. The packaged Med Bay frame was inspected. Existing loader warnings remain; no script/assertion errors occurred.

This snapshot includes the Quarantine, Refinery, Crew Hab and Med Bay activity revisions that postdated v5, and compiles the extended current-controller route fixture. It does not exercise the focused medical/crew tour flags in the package; those four-rotation results remain native evidence. Capture availability does not establish visual acceptance for all 35 rooms. Nursery, Life Support and Hydroponics still need larger layout work; Storage needs a fuller cargo story.


Life Support activity revision: tank and console now share a service pad; the enlarged maintenance cart carries its own task lamp, with the pressure bottle beside it and a short perimeter hose. Native state checks, four current-controller rotations (24 arrivals, 32 transitions, 2544 movement samples), and 72 depth poses pass; all 24 prop fronts are accessible. Selected card: rooms/whole-room/life-support-card-activity-v1.png. This postdates Windows v6. Visual review still finds excessive empty floor; this is an intermediate layout, not final art acceptance.


Life Support follow-up: selected composition-v3 and card-activity-v3 add a grounded tool-bearing filter-service bench and flush drainage slots. The initial bench placement overlapped the tank in rotated views; reduced width and four authored centers resolve all floor/art bounds overlaps. Current-controller tour v2 passes 24 arrivals, 32 transitions and 2550 samples; depth v3 passes 84 poses with all 28 fronts accessible. This supersedes the earlier six-assembly intermediate layout, remains post-Windows-v6 and is not whole-catalog visual acceptance.


Hydroponics activity revision: enlarged potting trolley and harvest bench share a work pad; a smaller nutrient station feeds the growing bed along the wall with a flush crossing cover and drainage. Selected hydro-composition-v2.json and hydroponics-card-activity-v1.png. Four rotations have no floor/art overlaps; all 20 prop fronts are accessible in 60 depth poses. Native effects pass; current-controller tour passes 24 arrivals, 32 transitions and 2551 movement samples. Card reviewed, station-scale visual acceptance pending; postdates Windows v6.


Crew Lounge activity revision selects crew_lounge-card-activity-v2.png: enlarged tea trolley beside galley, games seating closer to dining with a localized rug. Corrected rotated coat collisions and reading-lamp access. Native current-controller tour v2 passes 20 arrivals, 24 transitions and 1946 movement samples; depth v2 passes 96 poses with all 32 sampled fronts accessible. Initial ten-assembly state checks pass. Remaining lamp/sofa and plant/table artwork bounding-box overlap in q0/q1 is intentional peripheral placement, with separate floor footprints. Postdates Windows v6; broader station-scale visual acceptance remains pending.


Reactor activity revision selects reactor-composition-v2.json and reactor-card-activity-v1.png: enlarged tool-bearing bench with task lamp and shared pad, plus a cooler-side service cylinder. Corrected cylinder overlap in q1. Native current-controller v2 passes 24 arrivals, 32 transitions and 2717 samples; depth v2 passes 72 poses with all 24 fronts accessible. No floor overlaps; lamp overhang above bench remains intentional. Card reviewed; station-scale/package acceptance pending, post-Windows-v6.


Windows activity-review-v1: all 35 identities captured at 52%; 53 arrivals, 141 transitions, 10813 movement samples pass. Life Support bench/cart read at play scale; Lounge groups read but a detached central rug is an unresolved visual defect. Cryo and Archive initial cards retain isolated equipment and tiny service props. Prioritize these revisions. PNG inventory proves decoding, not aesthetics.


Lounge detached-rug correction: RoomFloor.draw_dressing now accepts an optional central_textile flag, default true. Lounge opts out because it already draws furniture-anchored seating rugs. Selected card-activity-v3 visually confirms removal; prop geometry is unchanged. Initial bake parse failure was corrected (CRLF prevented the first signature edit); fixed bake passes. This floor-only revision postdates Windows activity-review-v1.


Cryo Chamber activity revision: larger supply trolley paired with console, transfer cooler beside compressor, and trolley pad rendered in normal-room dressing only. Selected cryo-composition-v2 and cryo_chamber-card-activity-v1. Current-controller tour: 16 arrivals, 16 transitions, 1350 movement samples. All four rotations have no floor/art overlaps; 72 depth poses pass with all 24 fronts accessible. Recovery layout/lifecycle unchanged. Card reviewed; fuller visual character and station-scale acceptance remain pending. Postdates Windows activity-review-v1.


Data Archive activity revision selects archive-composition-v2 and data_archive-card-activity-v1. Larger service cart, standing task lamp and work mat group with the relocated terminal. No floor overlaps in four rotations; minor cart cable/terminal edge and lamp art overhang remain. Native current-controller tour passes 24 arrivals, 32 transitions and 2613 samples; 72 depth poses pass with all 24 fronts accessible. Added support texture is declared and hashed. Floor helper now draws this leaf profile. Visual review remains incomplete; postdates Windows activity-review-v1.


Clone Lab preparation revision: selected clone-composition-v2 and clone_lab-card-activity-v1 enlarge the preparation bench and its mat. No floor overlaps in four rotations. q1/q3 close reviews identify lamp overhang, not obscured worktops. Depth: 60 poses pass, all 20 fronts accessible. Current-controller: 20 arrivals, 24 transitions, 1933 samples. Card reviewed; full organic composition and station-scale acceptance remain pending. Postdates Windows activity-review-v1.


Bio Lab activity revision selects bio-composition-v2 and bio_lab-card-activity-v1. Preparation bench enlarged, centrifuge repositioned, sample cooler paired with smaller cold storage. q1 cooler was hidden despite collision success; close review prompted side placement. Final tour v2: 20 arrivals, 24 transitions, 1943 samples. Depth v2: 72 poses, all 24 fronts accessible; q1 visibility inspected. Full room visual acceptance remains pending, postdates Windows activity-review-v1.


Holographic Core floor correction: the Archive parent gained dressing.floor during its revision; Holo still delegated to the parent and called dressing.floor again. Removed the redundant leaf override. The inheritance-aware audit now rejects duplicate hooks as well as missing hooks; negative duplicate control and single-delegation positive control pass, with all 32 live profiles passing. Selected holographic_core-card-floor-v1 is rendered and reviewed. This is a floor integration correction, not a completed activity-layout revision.


Holographic Core activity revision selects holo-composition-v2 and holographic_core-card-activity-v1. Larger cart paired with relocated calibrator and local service connection. Native current-controller: 24 arrivals, 32 transitions, 2607 samples. Depth: 60 poses, all 20 fronts accessible. Card reviewed, no floor overlaps; q0 small cable/upper silhouette overlap remains. Full visual acceptance remains pending.


Radio Lab activity revision selects radio-composition-v2 and radio_lab-card-activity-v1. Electronics bench enlarged between smaller receiver/test equipment, with direct cable and resized mat. No floor/art overlap in four rotations. Current tour: 16 arrivals, 16 transitions, 1350 samples. Depth: 60 poses, all 20 fronts accessible. Card reviewed; full visual acceptance pending.


Shield Generator activity revision selects hull-composition-v2 and shield_generator-card-activity-v1. Enlarged calibration bench and supporting rack/injector proportions. No floor/art overlaps in four rotations. Current tour: 16 arrivals, 16 transitions, 1347 samples. Depth: 60 poses, all 20 fronts accessible. Card reviewed; broader room composition remains pending.


Tidal Condenser activity revision selects tidal-composition-v2 and tidal_condenser-card-activity-v1. Enlarged sampling bench, direct tank connection, smaller pump/monitor. No floor/art overlaps in four rotations. Current tour: 20 arrivals, 24 transitions, 1931 samples. Depth: 60 poses, all 20 fronts accessible. Card reviewed; broader room composition remains pending.


Gravity Loom activity revision selects loom-composition-v2 and gravity_loom-card-activity-v1. Larger calibration bench and standing task light. No floor overlaps; q1/q2 close views confirm circular apparatus stays visibly clear despite bounding rectangles. 36 depth poses pass, all 12 fronts accessible. Current tour: 24 arrivals, 32 transitions, 2876 samples. Full visual acceptance pending.


Medical Center trolley revision selects med-center-composition-v2 and med_center-card-activity-v1. Enlarged supplies trolley, corrected q2/q3 floor collisions. Final four rotations have no floor/art overlaps. Current tour: 16 arrivals, 16 transitions, 1347 samples. Depth: 60 poses, all 20 fronts accessible. Card reviewed. Focused scale improvement, not full composition acceptance.


Xeno Lab revision selects xeno-composition-v2 and xeno_lab-card-activity-v2. Enlarged service trolley; main workbench moved inward after depth review found q0 front blocked by wall clearance. Final depth v2 passes 60 poses and all 20 fronts. Current tour v2: 12 arrivals, 8 transitions, 682 samples. Broader visual acceptance pending.


Anomaly Lab activity revision selects anomaly-composition-v2 and anomaly_lab-card-activity-v1. Enlarged recording cart, standing task light, receiver moved inward. No floor overlaps; q3 lamp art overhang remains. Current tour: 12 arrivals, 8 transitions, 682 samples. Depth: 72 poses, all 24 fronts accessible. Card reviewed; full visual acceptance pending.


New Storage Bay detail candidate: storage-staging-pallet-v1.png, built-in generation, 1254-square RGBA. Bundled hose, ochre case, straps and net on a low pallet. Exact prompt/provenance and read-only alpha registration saved beside it. Generated and registered only; not selected or integrated. Next: fit into cargo staging group, review at play scale, verify rotations and access. This begins a distinct detail pass beyond furniture resizing.


Storage staging pallet integrated in storage-composition-v4, card-staging-v1. Raw generated source unchanged; read-only alpha polygons, 60x25 footprint. Card shows readable hose coils/case/net at small scale beside waiting cargo. No floor overlaps. Current tour: 24 arrivals, 32 transitions, 2545 samples. Depth: 96 poses, all 32 fronts accessible. Full packaged station-scale acceptance pending.


Habitation drying rack production: v1 has believable boots/jacket/gloves but diagonal camera, rejected. v2 camera correction has horizontal front but opaque RGB checkerboard including interior voids. Sources and exact prompts saved in rooms/whole-room/hab-drying-rack-prompts.json. Neither integrated; alpha repair and small-scale review required.


## Hab drying rack integration

The v3 image-generation alpha edit remained opaque RGB. A new clean-v1 output removes the exterior and two reviewed enclosed background regions without rescaling; raw candidates remain preserved. crew-hab-composition-v3 places the rack beside sleeping furniture with separate q1/q3 positions. The jacket and gloves rest on its upper shelf and boots on its lower tray. Its status lens has an offline cover. Selected card: crew-hab-card-drying-v2.png. Native depth review passes 96 poses and all 32 furniture fronts; four current-controller tours return successfully. Final composition audit has no footprint overlaps; existing q3 chair/lamp visual overlap remains. Profile dependency closure passes. Normal-play visual approval and updated packaged evidence remain pending.


## Drone servicing details

Mining composition v2 substitutes a purpose-built cutter stand for the generic component table: supported cutter, replacement teeth, torque wrench, hooked hose and folded protective pad. Salvage composition v2 adds a low tray for recovered casing, pipe elbows and bundled umbilical beside the hatch. Both generated sources retain real RGBA alpha and exact provenance prompts. The mining inspection lamp now has explicit q1/q3 positions beside its trolley; its old approach was blocked. Final depth reviews cover 84 mining and 72 salvage poses, all 52 fronts accessible. Eight rotated production tours pass; current evidence is output/drone-detail-routes-v2 with 52-percent station captures. Profile closure passes. New details are legible in the inspected q0 station images, but open areas and overall room composition still need review; no full-room or package approval is implied.


## Biodome propagation shelf

Composition v2 adds a true-alpha sage shelf with uneven cuttings, trailing leaves, pots, watering can and trowel, supported on two levels between fern bed and processor. Raw source and exact prompt are preserved. Native audit reports no footprint or visual overlaps in four rotations; depth review passes 72 poses and all 24 fronts. Current-controller tours pass 16 arrivals, 16 transitions and 1347 movement samples. Selected card and 52-percent q0 station view were inspected, plus q2 crew-depth composition. The detail reads clearly below the main planter scale; overall room approval and new packaged evidence remain pending.


## Full selected-catalog package: detail review v1

Fresh Windows debug export passes 35 source hashes, 70 source/card PNG decodes, 58 component records and 32 profile hashes/JSON parses. Current-controller traversal visits all 53 placed rooms with 141 reciprocal transitions and 10,815 movement samples. All 35 focused 52-percent PNGs decode at 1600x900. No script/assertion errors; existing image-loader warnings remain. Pack hash: B37CFBCF4D5A73704C49F14680F0DD7F848B08EA1AAFBF2C16B965293B2669BE. Med Office and Construction Drone Bay packaged views were inspected and still need activity grouping. This baseline includes recent drying-rack, storage-pallet, cutter-stand, salvage-tray and propagation-shelf revisions; it does not establish completed all-room art direction.


## Med Office grouping revision

med-office-composition-v2 and med_office-card-group-v1 group the reference shelf and reading lamp with waiting seats, and bring the examination couch toward the desk. No new raster component was added. Explicit q1/q3 lamp positions fix blocked approaches found in the first depth review. Final depth review passes 72 poses and all 24 fronts; four current-controller tours pass. q0 normal-zoom and q3 waiting-area views inspected. Native evidence: output/office-group-depth-v2 and output/office-group-routes-v2. This pass postdates windows-detail-review-v1 and improves furniture relationships; clinical detail and full-room visual acceptance remain open.


## Construction assembly group

Composition v2 moves the hatch nearer its cradle, places the trolley near fabrication equipment and adds a clamped-panel trestle with rivet tool, fasteners and hanging lead. Source is true RGBA and unchanged after generation. The construction renderer now reports actual fleet asset bounds, including the 100-wide bench and tall panel rack; placeholder 90x64 outlines had understated those visuals. Quarter-specific trestle and lamp positions resolve initial overlaps and blocked fronts. Final audit has no footprint overlaps; remaining lamp visual overlaps are articulated reach. Depth v2 passes 84 poses and all 28 fronts; current-controller tours pass in four rotations. q0 normal station and q1 service-group views inspected. New card assembly-v2 is selected. Final art acceptance and package coverage remain pending.


## Thermal Control equipment group

thermal-composition-v2 brings the converter alongside the exchangers on the sealed north wall, adds a rear service connection, and places the pressure bottle beside that equipment with orientation-specific positions. Initial card review found the bottle detached, so its placement was tightened before final verification. Audit v2 has no footprint or visual overlaps; depth v2 passes 72 poses and all 24 fronts. Current-controller tours pass four rotations through actual west/south ports. Selected card group-v2 and normal q0 station capture reviewed. No new raster source; this layout postdates windows-detail-review-v1 and is not full-room visual acceptance.


## Corridor and corner emergency fittings

Shared routing surfaces add a recessed intercom and conduit along the cabinet wall band. The corner conduit steps around the actual chamfer; the initial overhanging elbow was caught by the bounds test and repaired. New intercom-v1 cards use production geometry. Final bounds check passes 516 samples; a deliberate invalid fitting returns exit 1 and reports its rect/point. The fixture now exits on failures rather than hanging on an assertion. Current-controller tours pass both identities in four rotations; q0 corner normal-zoom view inspected. No walking geometry or blockers changed. This pass postdates the current package.


## BRINE current selection reconciliation

The old rollout entry described only an observation pedestal. Current selected renewal-v2 composition includes the chamber, startup pod, dual-monitor workstation, diagnostic desk, server and tablet pedestal. Fresh native review output/brine-organic-current-v2 passes four rotations, 16 entries and returns, 3569 movement samples, offline/pause/motion and three viewport sizes. Review card inspected. New --review-only and --output fixture options preserve the selected card and prior evidence. The first attempt caught a concurrent renderer edit before its new script existed; that failed process was stopped after the parse error, and a fresh run passed after the file existed. No room art was changed in this reconciliation.

### Battery Array: staggered bank/service grouping
The selected battery-composition-v3 profile and battery_array-card-group-v4 move the second bank to the southeast, keep the breaker/distribution group west, and give the supported test cart a northeast working area. Smaller host-bound matting and endpoint-linked service cables replace the detached southeast accessory pair. No new raster source was needed. All 72 depth poses pass, including 24 usable fronts, and battery-group-routes-v4 passes all four rotations and returns. The normal-scale q0 station capture was inspected. This remains a composition revision, not finished visual acceptance: it still reads as separate quadrants and needs more hull-integrated working detail. It postdates the catalog37-v2 package.
The initial routes-v3 run reached the default mixed-station branch because a newline-sensitive insertion silently failed. Its failed result is retained; routes-v4 is the correctly identified focused fixture. Future scripted edits must assert that their exact target occurs once and verify the resulting branch before launch.

### Battery electrical test bench
Battery Array now selects battery-composition-v4 and battery_array-card-bench-v1. The earlier narrow cart is replaced by a wider supported test bench: mounted voltage meter and fuse holders, hooked leads, instruments and gloves on the worktop, cable/spare storage below, and a clamped task lamp. The reel sits beside this service area. The first generated image clipped its lamp and was rejected; the reframed RGB source needed connected-background cleanup with three reviewed gap seeds. Exact prompts, source names and cleanup are in rooms/production-ten/decor/battery-test-bench-provenance-v2.json. The cleaned source remains full size with true alpha; registration is vector-only.
Native battery-bench-depth-v1 passes 72 poses with all 24 fronts usable; battery-bench-routes-v1 passes four rotations and return routes. The composition audit reports no floor overlap; its q0 bench/reel bounding-box overlap covers empty sprite space, and the actual card and station q0 capture were inspected. Dependency closure passes. This is a concrete supported-workspace improvement; it does not approve every room or erase the remaining sparse areas. It postdates the latest package.

### Flush processing connections
Ore Refinery's floor pass connects crusher to processing vessels and vessels to sorter through contained runs. The main-aisle crossing has a recessed service cover, and a narrow catch grate sits along the hopper's maintenance edge. These are authored floor-only details, with real machine source-space endpoints; they add no collision or gameplay function. Furniture and its prior depth registration remain unchanged. Select refinery-composition-v3 / ore_refinery-card-transfer-v2 after native route review. The full catalog still needs visual acceptance; decorative connections do not establish simulated material flow.

### Quarantine floor services
Quarantine now selects quarantine-composition-v3 and quarantine_cell-card-services-v2: an exposed berth/monitor lead, a berth catch grate and an east-door recessed entrance grate. Floor furniture remains unchanged. Native quarantine-services-routes-v2 passes canonical east/west access in all four rotations; the q0 normal-scale station view was inspected. The earlier v1 fixture incorrectly assumed a south door and failed four graph checks; its misplaced entrance grate was corrected before selection. Do not infer sockets from room names.
The Dressing helper now supports optional surface_routes after decals, retaining existing routes below finishes. This prevents exposed leads being hidden by a pad. The full-catalog native host audit includes both route categories and passes (quarantine-surface-hosts-v1). Component/profile dependency closure passes. This source revision remains outside the latest package and does not complete all-room visual acceptance.

### Research analysis/service grouping
Research Lab selects research-composition-v3 and research_lab-card-services-v1. The scanner moved 44 units toward the analysis benches; a short exposed specimen/analyzer lead and a floor service run to the scanner connect the working area. Existing supported preparation furniture and cooler remain. Native research-services-depth-v2 covers all seven objects (84 poses, all 28 fronts usable), and research-services-routes-v1 passes the canonical south connection in all four rotations. The q0 station capture was inspected; its open entrance approach remains deliberate. The initial depth v1 omitted the cooler, so v2 is the complete furniture scope. New dependency closure passes; this revision is not yet in the last Windows package.
The host auditor now has --negative-surface-host, which injects a missing endpoint only in a local duplicate of the test profile. surface-route-negative-v1 exits 1 with exactly the two expected missing endpoints; no runtime profile is changed. Positive full-catalog coverage remains quarantine-surface-hosts-v1 for the helper addition.

### Command Center operator station
The chart station gains one north-facing operator chair with a physical headset hook and side tray supporting a logbook and flask. Original command-operator-chair-v1 PNG alpha is preserved; only its vector registration is derived. Exact prompt and processing are in command-operator-chair-provenance-v1.json. During review, the q1 chart credenza was found against the wall: moving its center from (-42,158) to (-42,127) restores its working face. This was a pre-existing wall clearance issue, not chair collision. command-chair-depth-v2 passes 72 poses and all 24 working fronts. This chair is decorative furniture, with no newly implemented sitting interaction.

### Keep new identities visible while integration is incomplete
The current catalog may grow during a furnishing pass. Inventory v6 contains 40 rooms; three new rare rooms have no selected cards yet. Add their identities to the furnishing ledger immediately. The review-board generator's --include-incomplete mode displays missing-art entries and the inventory errors; it never substitutes another room's card. Default strict mode still rejects the same inventory, and changed hashes remain errors even in report mode. A successful 33-profile dependency audit covers declared assets only and does not prove all 40 rooms are integrated.
Command: python tools/build_room_composition_review.py output/room-review-inventory-v6.log docs/room-composition-review.html --include-incomplete

### Review current sockets and preserve texture ownership
Use --review-rooms=id,id with tests/playtest_production_ten_station.gd to derive canonical doors from current RoomDatabase layouts, then exercise all four rotations. Unknown room/layout/door names fail explicitly; catalog-review-negative-v2 exits 1 for the requested unknown ID. The v1 negative attempt failed during startup while main.gd was temporarily invalid UTF-8; it is not rejection evidence. Current source had been corrected before any byte repair was written here.
The three rare room views previously discarded their Dressing helper while retaining its registered props, causing wrong-atlas image fragments. Preserve the helper when retaining those props. rare-room-catalog-routes-v3 passes all three rooms in four rotations and q0 captures were inspected. This restores texture ownership only: generic positions and inherited service routing still need authored room-specific layouts. Earlier v1 captures also contained an inspector layout-API error; the current worktree had already corrected that call before v2.

### Isolation Vault dedicated grouping
The vault now has local, ID-keyed placements: reserve banks along the west working side, breaker and distributor east, supported test bench below them and spare cable reel southwest. Dedicated isolation-composition-v1 replaces Battery Array's diagonal service routes with perimeter connections. Native isolation-group-depth-v1 passes 72 poses with all 24 fronts usable; isolation-group-routes-v1 passes all four rotations and the south entrance. The q0 normal-scale capture and card were inspected. The selected isolation_vault-card-group-v1 and isolation-manifest.json record reused machinery truthfully and pass dependency closure. Full visual acceptance and current Windows packaging remain pending.
The card baker now accepts --view=res://... with an explicit --output path, allowing new room views to use the same native bake path without adding another named flag. Existing card overwrite protection remains.

### Pressure Control dedicated service area
Pressure Control Chamber now selects pressure-composition-v1 and pressure_control-card-group-v1. Explicit placements retain seven distinct objects: fan, pressure vessels, tank, controls, maintenance cart, spare bottle and supported filter bench. Perimeter service hoses replace inherited routing. The room creates its own Dressing helper from the local profile after removing inherited dressing registrations, preserving correct texture ownership without duplicate furniture. The q1 spare bottle moved inward to restore its working front.
pressure-group-depth-v2 passes 84 poses with all 28 fronts usable; pressure-group-routes-v1 passes canonical south access in four rotations. The q0 native station capture and card were inspected. pressure-manifest.json records reused machinery and selected dependencies, with closure passing. Full aesthetic acceptance and updated packaged coverage remain pending.

### Dedicated Deepwater Listening Post
The listening post now owns listening-composition-v1 and its textures, with explicit ID placements for four acoustic instruments, an electronics bench and a north-facing operator chair. The chair reuses the recorded Command Center source, including its physical headset hook and supported side tray; no new sitting interaction is implied. Perimeter services and the short receiver/bench connection explain the work area. listening-group-depth-v1 passes 72 poses and all 24 working fronts; listening-group-routes-v1 passes four rotations and south entry. Card and normal-scale q0 station capture inspected. The three rare-room manifests pass dependency closure; updated packaging and complete aesthetic acceptance remain pending.
Isolation Vault's profile ownership was also corrected: its local helper now loads local textures independently. output/isolation-profile-owner-v2.png has identical decoded pixels to its selected card, confirming that this wiring change preserves the reviewed appearance.

### Full 40-room packaged baseline
windows-catalog40-v1 passes 40 selected sources, 80 source/card PNG decodes, 68 component records and 36 composition profiles. The Windows controlled tour visits 60 placed rooms across 162 transitions and 12,525 movement samples. All 40 focused captures decode at 1600x900; hashes are in focused-capture-decode.json. Pack SHA-256: 58270AC6D6C83ADE1BD7C8E35EDC6549071763AC0424788D33CBE9E14AA66E9A. The ledger preserves the earlier package as historical. This is technical coverage, not full visual acceptance.
The floor-hook auditor now counts surface_routes as floor detail alongside mats, buried routes and decals. catalog40-floor-hooks-v2 covers all 36 current profiles without errors. This audit-only change postdates the package and changes no runtime art. Continue room-by-room visual review at actual station scale; a complete asset inventory does not establish natural composition.
