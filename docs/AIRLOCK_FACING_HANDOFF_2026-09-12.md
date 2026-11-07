# Airlock directional inventory - September 12, 2026

## Objective and constraints
Continue all room directions while preserving live diving and helmet handoff. Existing source geometry and owner furnishings take priority over a generic continuous-bank replacement.

## Current state
Inventoried composition.json and four native room views. assets/airlock-directional-v1/live-inventory-review.json records actual texture regions, per-quarter centers, source hashes and findings. Corrected north/east/west unknown-source ledger entries without marking them facing-complete. No production art/code/card changes.

## Verification
Viewed q0/q1/q2/q3 from output/airlock-facing-review-2026-09-12/native. Chamber rotates, furniture relocates but uses unchanged frontal artwork. North-positioned bank faces inward; side/south placements need new art. Separate shelf helmet is runtime-drawn from crew equipment; static source helmets are distinct. This is visual/source inventory, not new service, pathfinding or interlock acceptance. No unrelated tests or export run.

## Next action
Author separate side suit-locker and equipment-check-bench companions, then validate actual handoff reachability for every orientation before integration. Earlier south source failed an east-facing handoff and remains uninstalled. Do not bake removable helmet into replacements or block chamber access.


## Equipment-check side bench companion

Added check-bench-side.png and its exact prompt/registration/review in assets/airlock-directional-v1. Native pair at 40.82 by 100 units reviewed in output/airlock-check-bench-2026-09-12/companions/native.png. Drawer access points inward; no helmet/suit baked into bench. One authored east library entry with horizontal flip for west.

Live host fit remains pending. Airlock's draw_registered_prop delegates to dressing.draw, which rejects non-dressing registrations; a library-only substitution would disappear without an explicit rendering branch. Preserve semantic prop IDs and verify chamber/crew service clearance when integrating. No default/card/runtime code changed. Native fixture proves library drawing, not live handoff or owner acceptance.


## Side bench live installation follow-up

Airlock view now substitutes the bench in q1/q3 and explicitly draws library props. Final bounds q1 [139.18367,76,40.81633,100], q3 [-180,-176,40.81633,100] fit the 180-unit furniture envelope and clear chamber visual bounds. Initial 184-unit placement failed containment and was corrected. North/south images are identical; only equipment_check_bench changes in side metadata. Final native images reviewed in output/airlock-check-bench-2026-09-12/final.

176 preferred-layout cases passed before the four-unit margin correction. Airlock service test failed both unchanged baseline and revised room: existing suit-locker containment, q1/q2 fitting reachability and subsequent helmet actions. Final failure-comparison.json shows no new errors compared with baseline. Baseline test output/test-runs/20260912-105552-headless, revised 20260912-105649-headless. This is not a green service acceptance. Existing failures remain for follow-up; no crew behavior/test assertions altered to pass. No card change because q0 is unchanged, no export.


## Locker service failures resolved

Default locker positions are now q0 [76,-42], q1 [-142,40], q2 [-140,-205], q3 [74,-210], with 1.35 scale retained. Fitting-point probes proved q1/q2 wall collisions; route probe proved q3's standable point was disconnected beside the chamber. Repositioned lockers, no navigation/helmet behavior changes. q0 now contained; all four final native views reviewed. Updated q0 locker-fit card and three consumers.

Service suite passes at output/test-runs/20260912-110641-headless: actual loop covers Bill four quarters plus Veld/Branforth q0, not every human in every quarter despite its broad summary label. Interlocks/power/pause/save/UI checks pass. Final 176 furnished layouts pass at 20260912-110753-headless; 47 card-binding identities pass. Earlier baseline failures are resolved for this scope. See assets/airlock-directional-v1/locker-fit-review.json. Directional locker art and full catalog still remain; no export.


## Reserve-air side bank

Added reserve-air-side.png, exact prompt, registration and reserve-air-side-review.json. Three overhead tank shoulders with inward buckles and hose outlet. Native paired source at 104-unit length reviewed. Installed mirrored west in q3 at [-180,76]; authored east remains library-only. Existing explicit library draw path used, semantic reserve_air_bank ID retained.

output/airlock-reserve-side-2026-09-12/comparison.json confirms q0/q1/q2 RGB/metadata unchanged and only q3 bank changed. Native q3 reviewed. Airlock service suite and 176 preferred layouts pass at output/test-runs/20260912-111123-headless. Exact actor coverage remains Bill four rotations plus Veld/Branforth q0. No card change or export. South reserve bank and directional locker art remain.


## South reserve-air bank installed

Added reserve-air-south.png, exact prompt/registration/review. q2 now uses a 104-unit overhead bank with north-facing buckles/hose outlet, bottom at y180. Native q2 reviewed; comparison in output/airlock-reserve-south-2026-09-12 proves only reserve_air_bank changed, other rotations RGB/metadata identical. Airlock suite (Bill four quarters; Veld/Branforth q0) and 176 preferred layouts pass at output/test-runs/20260912-111451-headless. No q0 card change, no export. South check bench and directional lockers remain.


## South equipment-check bench installed

Added check-bench-south.png, exact prompt, registration and review. q2 uses a 100-unit overhead slatted bench with north/inward handles at x=-178, bottom y180. Native q2 reviewed; comparison in output/airlock-bench-south-2026-09-12 shows only equipment_check_bench changes, other rotations RGB/metadata identical. Airlock service (Bill four quarters; Veld/Branforth q0) and 176 layouts pass at output/test-runs/20260912-111816-headless. No q0 card change or export. Directional suit lockers and owner acceptance of the side camera remain pending.


## South pickup-tray preparation

Added suit-storage-south-empty-tray.png, exact prompt, new registration and south-empty-tray-review.json. Removed only the painted helmet from the projecting pickup tray; retained two stored kits. Carrying-handle neutral apertures repaired in registration after native review. Native library width120 reviewed, side variants pass. No live selection, card or service-code changes. Existing fixed east-facing fitting anchor and separate rendered helmet need tray-relative alignment before live installation.


## South locker live service integration

q0 now selects the empty-tray south locker at [58,152.897474],width120,bottom180. Shared AirlockService.helmet_anchor uses optional normalized prop anchor [0.051,-0.80]; old lockers retain exactly the previous anchor formula. Fitting point derives from that anchor plus[-21,31], preserving east-facing handoff. Added supported shelf above the side tray. custom_library_draw allows the separate helmet in direct rendering; room_content_canvas now honors the same flag for retained rendering. Semantic suit_lockers ID remains.

Changed airlock_view.gd,airlock_service.gd,room_content_canvas.gd,q0 default locker position/scale and card consumers. Native final q0 and Veld before-grasp/after-grasp/after-release captures reviewed in output/airlock-south-locker-live-2026-09-12. Helmet disappears at pickup and returns on release; source spare helmets remain in main compartments. Comparison proves only q0 suit_lockers changes; other3views RGB/metadata identical. Headless service (Bill4quarters,Veld/Branforth q0) and176layouts pass at20260912-122223-headless. Native Veld run has3 failures, all Locker controls fit within sidebar viewport; no full native-suite acceptance claimed.47card identities pass after transient file-write retry. No export. Side/north locker artwork, shelf visual polish and native sidebar issue remain.

## Native sidebar follow-up

The geometry probe confirmed all six Airlock service controls and the Time / Cycle panel are fully reachable through SideScroll at each requested window size. The former assertion mislabeled the time panel as locker controls and required its initial position to fit without scrolling. tests/test_airlock.gd now verifies the six controls exist and each control plus the time panel is visible and fully enclosed after scrolling. Native Veld validation exited 0 with 224 travel samples; evidence: output/airlock-sidebar-check-2026-09-12/validation.log and validated/. This resolves the three sidebar assertions, not owner acceptance of side artwork. Directional lockers and shelf visual polish remain open.

## North locker library companion

Added suit-storage-north.png, exact built-in imagegen prompt, registration and review JSON. Source inventory and inward latches reviewed; native width120 silhouette reviewed in output/airlock-north-locker-2026-09-12/companion. Existing 20-variant regression passes at output/test-runs/20260912-123626-headless; this fixture does not certify the new companion. Live north placement, service anchor, material polish and side locker directions remain. No card or live selection changed. Pipeline references, bible and coverage updated.

## North locker material revision

Selected suit-storage-north-matte.png for the north library entry, preserving the previous source and registration. Exact imagegen prompt and updated review retained. Native width120 preview reviewed in output/airlock-north-matte-2026-09-12/companion; silhouette region changed from height441 to442. Large cabinet highlights are quieter, small brass detail remains dense. Live fitting, crew handoff and furnished-room material review remain; no live/card selection changed. LFS attribute verified.

## North locker initial live fit

q2 selects matte north locker at[-158,-180],width120,shared helmet anchor[.051,1.3]. Changed airlock_view.gd and q2 default layout scale/position. Native floor-edge capture reviewed; comparison proves only q2 suit_lockers changed. Headless service and176layouts pass at20260912-123952-headless. Raised -228 trial overlapped upper fittings and failed containment, so reverted to exact prior tested placement. Native focused Bill q2 probe also failed interlock endpoints; not yet diagnosed. Evidence in output/airlock-north-live-2026-09-12. Wall mounting and native interlock investigation remain; no q0 card change or export.

## Native north service verification

Probe proves first screenshot opened BRINE greeting: paused false->true, crew_comms.holds_pause false->true, room remained ready and sealing_inner elapsed0.1. tests/test_airlock.gd now disables automatic crew_comms processing and dismisses dialogue alongside its existing disabled main simulation. Production unchanged. Focused native Bill q2 exits0 with204travel samples and all ten interlock phases; before-grasp,after-grasp,after-release captures reviewed. Evidence service-validated.log and bill-q2-validated/ under output/airlock-north-live-2026-09-12. North wall mounting remains incomplete; earlier native interlock issue resolved.

## North wall projection installed

Added wall_art_rect at[-158,-252] in airlock_view.gd while preserving verified floor footprint/helmet anchor. Draws source at the riser top and extends shelf support; north_wall passes wall_view to Airlock fittings, which omits intersecting wall items. Isolated q2 reviewed; all footprint metadata and other3RGB unchanged. Headless service/176layouts pass20260912-124748-headless. Native Bill q2 passes204travel samples; mounted after-release capture reviewed. Adjacent-room station content occludes the cabinet at this height; shared-wall visibility and long support polish remain. See output/airlock-north-mounted-2026-09-12 and prior batch service-mounted.log/bill-q2-mounted. No card change or export.

## Shared north wall corrected

Full station/camera-offset evidence corrects the previous occlusion diagnosis: cabinet was above viewport. Shifted camera revealed actual projection into northern room because shared riser was absent. airlock_view now uses BASE_Y when omitted_sides includes north, TOP otherwise. Native shared-wall after-release screenshot reviewed; Bill q2 exits0 with service/interlock checks in output/airlock-north-mounted-2026-09-12/shared-wall and shared-wall.log. Floor geometry unchanged. Exposed long support and disabled-riser settings remain.

## Low-wall mounting verified

grid_canvas assigns raised_north_visible before configure_embedded; airlock_view uses it plus omitted north side to choose TOP or BASE_Y. Same-view raised/low/shared/raised-again native fixture preserves floor rect and checks exact mounting heights; all four images written, low and raised-again reviewed. Headless service/176layouts pass20260912-125347-headless. Evidence output/airlock-wall-modes-2026-09-12. Exposed support polish and side lockers remain. No card/export change.

## Side locker overhead companion

Rejected first upright tower study. Revised source suit-storage-side-overhead.png preserves two suits/two helmets/four boots and empty tray while showing inward side visors and boot toes. Exact prompts, raw identity and review saved. One east registration with mirrored west,world34.02985x120; both native library previews reviewed in output/airlock-side-locker-2026-09-12/native. LFS attribute verified. Live q1/q3/service fitting and owner camera acceptance remain. No live/card selection changed.

## Side lockers installed

q1 mirrored west and q3 east use overhead kit source, existing120length. Added per-prop helmet_tray_uv for support connection and handoff anchors; changed airlock_view and q1/q3 default layouts. Native rooms and both after-release images reviewed. Headless service/176layouts pass20260912-125910-headless; native Bill q1/q3 pass315travel samples,all interlock/power/pause/save/UI checks. Only q1/q3 lockers differ; q0/q2identical. Evidence output/airlock-side-live-2026-09-12. Support bracket polish remains, especially west; all-direction source availability is not owner visual acceptance. No card/export change.
