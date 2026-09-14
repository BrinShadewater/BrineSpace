## Polish, optimization and bug pass - September 14, 2026

Fixed and pushed: vented Power is named when the reserve is full (likeliest cause of the west-turbine report; no directional defect exists); construction no longer draws service routes to unplaced props (the Sept 12 Solar log's 492 assertions); retained room content keys on a per-view layout serial so one churning view no longer invalidates every room; failed crew construction approach searches retry once per second instead of every frame (profile-station simulation 6.7 -> 2.3 ms/frame); Observation Room reading derives its station from the desk and chair after the scale pass covered the fixed point.

Tests brought up to date with intentional behaviour: crew-built construction (Cold Store, Galley, Observation Room, Salvage Workshop), Salvage pickup pose, Galley drink pose, Observation rise on suspension, and the crew water station destination moved off the Sept 13 rebuild cradle. New `test_construction_fitting_routes`.

Rendering pass (same day): rocks/wrecks and unpowered derelict wards moved to retained environment passes; unflipped props skip the flip bounds lookup; retained rooms whose frame inputs are unchanged skip configure/submit and only advance `machine_clock` (`--configure-all-rooms`, `--redraw-derelicts` restore the old paths). Observation reading stations now resolve for all four rotations. Environment and content parity tests compare cached/direct pixels themselves, and each new cache was proven by a deliberately broken key or clock failing them.

Measured findings that should steer the next rendering work: paused frames render the whole 50-room station in ~13-17 ms with the same ~6,600 draw calls, so draw calls are not the bottleneck on this machine (hiding the 1,447-call floor pass saved ~2 ms). The running-frame cost is per-frame GDScript. The old `profile_draw` stages undercounted it (derelicts were invisible) and its per-room string keys inflate setup costs; attribute by timing pass `_draw` entries instead. After this pass the largest per-frame items at 50-fit are: room contents 2.8 ms, grid key validation 2.9 ms (spread across ~15 sub-0.5 ms checks, not worth trimming), slot paints ~2.5 ms, foreground and haze lines ~1 ms each. Whole-frame means vary by ~±3 ms between runs; compare stage timings and repeat runs.

Native lane cleanup (same day): Studio, floor, Xeno and crew comms tests were brought up to date with owner decisions (free placement default, retired tile brushes replaced by the finish picker, Studio-only floor details, retired Listening Post flush panels, composition dressing textures, high-resolution selection portraits); none was a game bug. Orphaned floor-profile decals whose host furniture was replaced (turbine and heat-recovery benches, med_preparation, xeno_service_cart) were removed at the owner's request. Card-baking tests now write under `output/` unless `--cards=res://assets/...` is passed, and the crew water station writes evidence to `output/` unless `--record-evidence` is passed, so routine native runs no longer dirty tracked files.

Latest full native lane (before the crew comms fix): 64 pass, 1 skip (bug_report harness), and only owner-accepted failures remain. **Kept by owner:** four floor-detail cases in `test_floor_detail_visibility` (refinery pipe cap q3, research teal marking q2, biomass and mining no-clear-floor). **Parked by owner:** `test_camera_pixel_stability` fails 2 of 64 cases at 960x540 / zoom 0.6 (a one-pixel line on the BRINE ring changes on third-pixel scroll offsets; whole-pixel offsets are identical). Layer hiding and `--redraw-brine-parts` did not isolate it; do not resume without owner request.

Still waiting on the owner's normal paid playtest: live feel of the rendering changes, the vented-power feedback on screen, and whether the 12-Power storage cap still makes power feel scarce (a balance decision). Ask for an F8 report on any fault.

## Gameplay/performance task closed; Claude handoff - September 13, 2026

Owner requested workflow consolidation and closure. Read [the detailed Claude
handoff](CLAUDE_HANDOFF_2026-09-13.md) for the recent Claude reference point, current
paid-gameplay fixes, startup/hatch/Studio work, F7/F8/F9 diagnostics, measured gains,
newer room/character status, checks and next actions. Room and character skill
references plus targeted installed mirrors, asset workflow and bible now carry the
lessons. This was a documentation-only closeout: no fresh game-wide validation,
commit, export or generation. Original power/reserve and west-turbine reports stay
open; animation polish remains unfinished and paid generation remains prohibited
without explicit owner approval. No background continuation is intended.

## Room asset workflow session closeout - September 13, 2026

The large/medium room-asset lessons are consolidated in the maintained room-pipeline skill, `docs/ROOM_ART_PRODUCTION.md` and `docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md`. Future batches use one process-specific anchor plus at most one smaller functional universal support, preserve quiet floor, verify both asset IDs and silhouettes in four native orientations, then publish cards and dependency hashes.

The communications furnishing v9 batch closes with six audited assets across Radio Lab, Listening Post and Holographic Core, 12 reviewed native orientations and a passing focused suite at `output/test-runs/20260913-024217-headless`. Owner aesthetic acceptance and a fresh export remain pending. See `docs/ROOM_ASSET_WORKFLOW_CLOSEOUT_2026-09-13.md`.

## BRINE/scale investigation session closed — September 13, 2026

Owner requested workflow consolidation and session closure. Accepted BRINE tube contact is retained; the 47-room scale-pass evidence remains tied to its September 12 revision and later furnishing selections take precedence. Veld's scanning-head report remains unreproduced; Solar dressing assertions and the earlier Salvage approach issue are separate open findings. Maintained/installed skills, asset workflow and visual bible now include source-density, shadow ownership, authored-versus-local layout attribution and report-state diagnosis lessons. See [session closeout](HANDOFF_ART_SCALE_SESSION_CLOSE_2026-09-13.md). Documentation-only closeout; no new generation, export or scheduled continuation.

## Crew animation session closed - September 13, 2026

Owner requested session closure. Animation polish remains unfinished. Do not resume Higgsfield generation or spend credits without explicit owner approval. Existing generated assets and controller work are retained; Veld north seating candidate is unselected after visible sliding in native transitions. See `docs/HANDOFF_CREW_ANIMATION_SESSION_CLOSE_2026-09-13.md` for current coverage, verification and remaining work.

## Communications themed/universal furnishings v9 - September 13, 2026

Radio Lab, Listening Post and Holographic Core now pair a large matte process-specific work surface with one medium neutral support furnishing. The signal-routing console, hydrophone-analysis table and projection-alignment deck replace older centerpieces; a patch-cable organizer, rugged power conditioner and instrument-calibration case extend the reusable family.

All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-024217-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V9_2026-09-13.md`.

## Service and logistics themed/universal furnishings v8 - September 13, 2026

Maintenance Bay, Storage Bay and Data Archive now pair a large matte process-specific workstation with one medium neutral support furnishing. The component-rebuild cradle, cargo-sorting island and media-restoration table replace scattered legacy floor clusters; a fastener chest, folded handling dolly and sealed transit case extend the reusable family.

All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-021608-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V8_2026-09-13.md`.

## Clinical and biology themed/universal furnishings v7 - September 13, 2026

Life Support, Med Bay and Bio Lab now pair a large matte process-specific workstation with one medium neutral support furnishing. The atmosphere-analysis island, sterile triage island and culture-preparation island replace weaker repeated work pieces; a sealed filter chest, enclosed equipment cart and specimen transit case extend the reusable family.

All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-014953-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V7_2026-09-13.md`.

## Utility and science themed/universal furnishings v6 - September 13, 2026

Tidal Condenser, Gravity Loom and Xeno Lab now pair a large matte process-specific workstation with one medium neutral support furnishing. The condensate-analysis island, field-tensor console and sealed assay table replace smaller generic work pieces; a valve-spares locker, diagnostic rack and narrow decontamination caddy extend the reusable family.

All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-013058-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V6_2026-09-13.md`.

## Cross-department themed and universal furnishings v5 - September 13, 2026

Reactor, Clone Lab and Biodome now pair a large matte themed workstation with one medium neutral support furnishing. The control-rod inspection bench, genome-preparation island and potting-and-seed island replace smaller generic work pieces; a sealed tool chest, rolling sample trolley and folding supply pallet demonstrate the reusable family across engineering, clinical science and cultivation.

All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-011605-headless`; the focused asset audit reports zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V5_2026-09-13.md`.

## Power-room themed and universal furnishings v4 - September 13, 2026

Current Turbine, Biomass Digester and Heat Recovery no longer repeat the same generic service bench. Each now has a large matte themed work anchor paired with one medium neutral support furnishing: a flow-governor console and instrument cabinet, feedstock-prep island and maintenance trestle, or exchanger manifold and cable caddy.

All 12 native orientations and three refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-010049-headless`; the focused asset and dependency audits report zero errors. Owner aesthetic acceptance and export remain pending. See `docs/ROOM_FURNISHINGS_V4_2026-09-13.md`.

## Themed and universal room furnishings v3 - September 13, 2026

Six additional matte furnishings are integrated across Hydroponics Bay, Ore Refinery, Cryo Chamber, Quarantine Cell, Pressure Control and Isolation Vault. The themed nutrient island, sorting bench and thaw cart reinforce room activity; the neutral parts chest, equipment plinth and task table add sparse station-wide support.

All 24 native orientations and six refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-003920-headless`. The batch remains locally saved with owner aesthetic acceptance and export pending. See `docs/ROOM_FURNISHINGS_V3_2026-09-13.md`.

## Themed and universal room furnishings v2 - September 13, 2026

Six additional rectangular matte furnishings are integrated across Research Lab, Command Center, Medical Center, Crew Hab, Anomaly Lab and Medical Office. Three are themed and three form a neutral station-wide family; the batch is evenly split between large and medium assets. All sources are true-alpha 1254-square rasters with external registrations.

All 24 native orientations and six refreshed cards were visually reviewed. Preferred layouts, card consistency and side-wall variants pass in `output/test-runs/20260913-001455-headless`. The batch remains locally saved with owner aesthetic acceptance and export pending. See `docs/ROOM_FURNISHINGS_V2_2026-09-13.md`.

## Room centerpiece asset pass - September 12, 2026

Twelve new themed furnishings are selected across ten previously sparse rooms: seven large and five medium assets, including ten square or rectangular silhouettes. All selected rasters are true-alpha 1254-square sources with external silhouette registrations. Ten refreshed room cards and 40 native orientation captures were visually reviewed; the batch audit reports zero errors.

Preferred-layout routing passes all 176 furnished orientations after explicit Battery q2 and Storage q2 center corrections. The selected assets, hashes, prompts, rejection record and bounded evidence are in `assets/room-centerpieces-v1/manifest.json` and `docs/ROOM_CENTERPIECE_ASSET_PASS_2026-09-12.md`. Owner aesthetic acceptance and a new export remain pending.

## Current room-art coverage reconciled - September 12, 2026

A fresh current-source native catalog covers all 47 room identities and 167 applicable renders across rotatable and fixed rooms. Four quarter contact sheets were visually reviewed against the entirely top-down, inward-facing contract. The coverage ledger has 47 unique rows, every declared direction, and 47 evidence-linked current-contract review gates. Historical per-direction pending labels remain as provenance. See [coverage audit](ROOM_ART_CURRENT_COVERAGE_AUDIT_2026-09-12.md) and [asset closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md). Owner acceptance, packaging, gameplay, character animation/art, and the incomplete Mining sentence remain outside this milestone.

## Crew-relative room art scale pass - September 12, 2026

Owner confirmed an in-game pass across furnishings, machinery, doors and fixtures using existing crew sizes. All 47 identities were natively reviewed against production Bill at 65.28 world units; 153 placements in 22 rooms corrected and 22 cards refreshed. Medical q3 and Mycelium source drawing now honor authored scale. 176 layouts, cryo recovery, 36 native crew-life cases, exact direct/retained parity for changed renderers and 47 card identities pass. Broader Salvage q1 approach failures reproduce before this pass. See [scale handoff](CREW_RELATIVE_ART_SCALE_2026-09-12.md). Source implementation complete; no export or owner visual acceptance claimed.

## Construction drone material review complete - September 12, 2026

The live Construction ROV now receives a matte ochre/graphite transform inside its own shared-atlas rectangle. The atlas bytes, silhouette and articulated UVs remain exact; Mining and Salvage regions are untouched. Docked, travelling and working states were natively reviewed, and the q0 card is refreshed. Drone fleet/jobs/lifecycle, Production Ten connections/walker paths, 176 layouts, 20 side variants and 47 card identities pass. Final integration also moved Med Center q3 stations against its closed wall, restoring both side-door routes. See [Construction repair](CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md) and [asset closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md). No gameplay timing, animation geometry, export or owner acceptance.

## Remaining owner room-asset queue closed in source - September 12, 2026

Medical Treatment, Mycelium Cultivation, Crew Lounge, Mining Drone Service and Research Analysis now use exact four-direction turns of their strongest south overhead banks. Blue medical upholstery, stable inventories and inward access carry across every wall. BRINE corner banks sit six world units lower in all quarters. Current Quarantine and Anomaly facing/cutout repairs were independently re-reviewed and retained. Native review, 176 layouts, 20 side variants, 47 card identities and the BRINE route fixture pass. See [asset closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md). The incomplete Mining sentence and optional Construction-drone redesign remain owner questions; no character animation, gameplay behavior, export or owner acceptance is claimed.

## Shared equipment floor-contact polish - September 12, 2026

Shared machinery shadows now hug footprints with short directional shade; broad offset mats removed. Native Galley, Cold Store, Salvage and Command reviewed in four rotations; BRINE station fixture passes and custom tube shadow is retained. Representative coverage, no export or owner acceptance. See [report](EQUIPMENT_GROUNDING_2026-09-12.md).

## BRINE tube floor contact accepted - September 12, 2026

Owner reviewed the corrected tube and confirmed it looks better. Retain the tight source-aligned contact shadow and suppression of the duplicate rectangular shadow. This acceptance covers the tube grounding treatment; no new export. See [report](BRINE_TUBE_GROUNDING_2026-09-12.md).

## Battery Array north overhead repair - September 12, 2026

Battery Array q0 now uses shallow overhead cell and distribution banks with four closed cells, three distribution units and three inward-facing gauges. Matte graphite and muted rust replace the former north elevation while the verified q1-q3 family, split frames, collision, placements and gameplay remain unchanged. Native q0 review, exact unchanged-quarter comparison, 176 layouts, 20 side variants, 47 card identities and direct/retained state parity pass. See [Battery owner repair](BATTERY_OWNER_NORTH_REPAIR_2026-09-12.md). Source workspace only; no owner acceptance or export.

## BRINE tube floor contact corrected - September 12, 2026

Tube now owns a tight source-aligned contact shadow; duplicate generic rectangular machinery shadow is suppressed. Native four-direction visual review and BRINE fixture pass. See [report](BRINE_TUBE_GROUNDING_2026-09-12.md). No export or owner acceptance.

## Fire performance and paid-operation pass - September 12, 2026

Fire transitions now preserve unrelated rooms' already-paid operation; a regression reproduced a mining bay losing service after its last reserve unit was spent. Fire updates avoid repeated safe-room scans and unnecessary power checks. Controlled 300-room fire-update timings improved with state parity; no whole-game FPS claim. Power/fire checks, native fire gameplay and the full hazard chain pass. Retired directive-reward tooltip removed. See [pass handoff](FIRE_PERFORMANCE_POLISH_PASS_2026-09-12.md). No art/animation replacement or export; original power-balance and west-turbine reports remain open.

## BRINE floating-tank polish verified - September 12, 2026

Detailed BRINE now has restrained sway, clearer contrast and fading bubbles. Native motion, pause, actual hardware-off, containment, four rotations and three viewport sizes pass. Earlier fixture failures resolved against current startup-power and furniture contracts. See [report](BRINE_RESOLUTION_2026-09-12.md). No export or owner acceptance.

## BRINE tank source resolution - September 12, 2026

Live BRINE now uses detailed original pixels with the same float and placement. Native visual review and containment/pause checks recorded; full room fixture still fails furniture and offline equality checks. See [report](BRINE_RESOLUTION_2026-09-12.md). No export or owner acceptance.

## In-game performance diagnostics - September 12, 2026

F7 now toggles bounded live performance stats; manual F8 reports include timing history with pause/focus markers alongside the live diagnostic station save. Studio moved to F9 to fix its F8 conflict. Collector and native input/report tests pass; overlay reviewed at 1600x900 and 960x540. See [diagnostics handoff](PERFORMANCE_DIAGNOSTICS_2026-09-12.md) for limits and playtest instructions. In-memory history does not survive crashes; no export or overall FPS improvement claimed.

## Cold Store owner asset repair verified - September 12, 2026

Matte blue overhead banks and two central coolers rotate through four layouts. Native crew scale, route, powered frost, retained cache and actual station pause checks pass; selected card is refreshed. See docs/COLD_STORE_OWNER_ASSET_REPAIR_2026-09-12.md. No gameplay/character animation change, export or owner acceptance.

## Galley owner asset repair verified - September 12, 2026

Overhead kitchen/serving and two communal tables rotate through four layouts. Native crew-scale, cooktop direct/retained and actual pause checks recorded; card refreshed. 176 layouts, 20 side variants and 47 cards pass. See docs/GALLEY_OWNER_ASSET_REPAIR_2026-09-12.md. Next: Cold Store blue equipment, scale and central coolers. No export or owner acceptance.

## Salvage owner asset repair verified - September 12, 2026

Overhead bench and tote rotate through four default layouts. Native alpha, retained power transitions and actual station pause verified; selected card refreshed. See docs/SALVAGE_OWNER_ASSET_REPAIR_2026-09-12.md. Next: Galley and mess-hall tables. No export or owner acceptance.

## Observation owner asset repair verified - September 12, 2026

Overhead furnishings now rotate with the room; portholes remain background architecture. Layout, native visual, retained power-transition and actual station pause checks recorded in docs/OBSERVATION_OWNER_ASSET_REPAIR_2026-09-12.md. Next asset queue item: Salvage Workshop. No export or owner acceptance.

## Command owner asset repair reviewed - September 12, 2026

Matching charcoal/red wall, overhead inward table/systems/comms and wall antenna corrections integrated. Native alpha, state/retained and actual pause checks recorded; selected card refreshed. Next: Observation rotation and architectural portholes. See docs/COMMAND_OWNER_ASSET_REPAIR_2026-09-12.md. No export or owner acceptance.

## Performance, bug and polish pass - September 12

Targeted live-state optimization removes repeated floor/wall rebuilds for hatch and fire progress while preserving chamber water invalidation. Native exact pixel comparison passes. Airlock clearance now accepts cleared wrecks and rejects remaining deposits/queued builds; feedback identifies blocker and cell. Fire-alert refresh safely handles absent UI. See [pass report](PERFORMANCE_BUG_POLISH_PASS_2026-09-12.md) for measurements, checks and remaining limits. Dense-station performance is not declared solved; no art/animation replacement or export.

## Owner checklist cross-check correction - September 12

All 45 pasted requests are accounted for in [the checklist audit](OWNER_PLAYTEST_CHECKLIST_AUDIT_2026-09-12.md). Keep the original power/reserve and west-turbine reports unconfirmed, and the separate weak cryopod animation complaint open. Cold mist/tint and staged startup do not close animation-quality work. Other sessions retain art/character scope; reported source repairs are not owner acceptance. This audit ran no new gameplay tests and made no export.

## Command matching wall reviewed - September 12, 2026

Command architecture now matches charcoal/red consoles. Native q0-q3 palette/seams reviewed and card refreshed. Independent table/comms overhead and inward facing remain open. See docs/COMMAND_OWNER_ASSET_REPAIR_2026-09-12.md. No export.

## Tidal owner asset repair verified - September 12, 2026

Overhead wall family, matching riser and independent pump/monitor integrated. Native four-direction, operating, retained parity and real station pause checks pass. Next asset review: Command Center. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export or owner acceptance.

## Tidal independent overhead equipment - September 12, 2026

Pump and monitor now use inward overhead variants. Static native q0-q3 reviewed; 176 layouts, 20 side variants and 47 card checks pass. Card refreshed. Operating/pause and retained effect review remain open. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export.

## Tidal matching rear wall - September 12, 2026

Tidal now selects grey-blue rear-wall panels and dull-brass pipes through a room-specific riser entry. Native joins/palette reviewed; original geometry retained. Independent pump/monitor overhead and effects remain open. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export.

## Tidal Condenser overhead wall family - September 12, 2026

All four walls now share three coil returns, two vessels, three cartridges and console with inward controls. Native q0-q3 reviewed; layout, side and card checks pass. Tidal-specific riser palette and independent pump/monitor remain open. See docs/TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md. No export.

## Construction static equipment repair - September 12, 2026

Fabrication bank, assembly bench, flat panel pallet, circular hatch and square docking deck now use matte overhead art. Native room/dock/hatch state reviews recorded. Drone silhouette retained; material repaint recommended separately. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. Source workspace only; no export or owner acceptance.

## Owner movement polish priority - September 12

Marsh west starts/stops and five-to-seven-unit short steps are integrated and verified. Native short-route joins are planted; full disk Save/Continue during start, stop, short travel and settling preserves pose pixels and clocks. Complete-pack and battery regressions pass in output/test-runs/20260913-021738-headless. The ledger contains 814 selected clips; broader autonomous, north/south transitions and older action/carry continuity remain open. See docs/HANDOFF_MARSH_WEST_TRANSITIONS_2026-09-13.md.

Marsh south idle now matches the replacement walk, completing all four cardinal idle replacements. Fixed registration retains the original two-pose 650/650-ms timing. Native exact-source checks pass across 143 body states, and the south idle/walk/idle review passes 51 samples with both boundary pairs visually reviewed. The source validator reports zero errors and preserves all 211 original frames. Directional starts/stops, other tiny-route distances and older action/run/carry continuity remain open. See docs/HANDOFF_MARSH_SOUTH_IDLE_2026-09-13.md; no owner acceptance or export is claimed.

The owner rejected stiff torsos and unnatural feet. Whole-body weight transfer, opposing arm swing and credible foot contact take priority over preserving rejected gait pixels. Veld is a mature woman without glasses; helmets must fit her poses. Marsh stays helmet-free and Bill is outside this replacement.

All eight Veld and eight Branforth walk variants have bounded native/live review. All four Marsh directions are also selected and reviewed: all 20 targeted walk variants now have bounded native/live review. Broader animation polish remains open. These counts do not close broader animation, identity, seated, start/stop or transition work in the clip ledger, or establish owner acceptance.

Veld uses independent directional video cycles and fitted helmet variants, retaining six-slot timing. East/west strides are 102/108 dense pixels; north/south are 0.12 cells. Each direction passed selected native checks; live approach samples per variant were east 15, west 34, south 53 and north 61. Original 670 frames and 108 manifests remain preserved. See docs/HANDOFF_VELD_VIDEO_WALK_2026-09-12.md.

Branforth uses independent directional sources and authored fitted helmet heads. East/west strides are 106/108 dense pixels; north/south remain 0.128 cells. Corrected west timing is 130/170/150/200/150/100 ms; other directions retain 170/130/150/170/130/150 ms. All directions passed 60 selected native samples. Bare/helmet live fixtures passed all original state-coverage checks: east 32 samples into north kneel, west 47 into north kneel, north 58 continuous into west walk plus three short adjustment episodes, south 11 into east kneel. Asset checks preserve 669 original frames and 108 manifests with zero errors/border touches.

Branforth west reference 02 incorrectly placed the right-hip wrench on the visible anatomical-left side. Corrected reference 03 and video 02 now show the left-hip meter. Retimed support phases and changed-source native/live checks passed. A float/int test mismatch and numeric-format hash churn were diagnosed and corrected; east/north/south regression checks and all 19,259 complete-pack checks pass. Earlier sources and captures remain preserved. See docs/HANDOFF_BRANFORTH_MOTION_2026-09-12.md.

Marsh's east standing reference and completed video 01 preserve his human-looking blond identity, visible right-temple plate, ivory/slate suit and full gloves. Cycle 36-64 is selected with six 150-ms holds and a 96-dense-pixel stride. Asset validation and 60 selected native samples pass. The live fixture captured 32 samples through north kneel, with battery drain preserved and no helmet. Contact sheets were reviewed; this is bounded agent review, not owner acceptance. See docs/HANDOFF_MARSH_MOTION_2026-09-12.md.


Marsh west uses independent video 01, cycle 28-52, six 150-ms holds and a 126-dense-pixel stride. Asset validation and selected native checks pass; 25 live samples through north kneel preserve battery drain and helmet-free behavior. Source and live contacts were reviewed. North and south use independent cycles 24-44 and 28-54, six 150-ms holds and axial stride 0.128 cells. Each passed 60 selected native samples; live north captured 29 samples into north kneel and south 33 into south kneel. The combined pack check passed 19,259 checks with zero failures. South kneel is partly occluded by room machinery; this does not accept its contact pose. Broader motion and identity work remain open.

Current continuity work (September 13): all 20 targeted walk variants are selected with bounded native/live review. Veld remains a woman without glasses; fitted helmets preserve each character's identity. Marsh remains helmet-free. Bill is unchanged.

Marsh's four cardinal idles now match the replacement walks. East and west starts/stops and short steps are integrated: east short routes span 3.5-4.5 world units, west 5-7. Six supplemental states contain 30 frames. Art validation reports 146 body states and 706 references, zero errors, and all 211 original source frames preserved. West production short-route joins are visually reviewed. Full disk Save/Continue preserves position, timers, animation clocks and selected texture pixels through east/west start, stop, short travel and settling. Complete-pack and battery checks passed in output/test-runs/20260913-021738-headless; subsequent obstacle/timing repairs passed the battery/Save regression in output/test-runs/20260913-022937-headless (116 route samples).

Remaining work: north/south starts, stops and short steps; other short-route distances and broader autonomous use; older Marsh action/run/carry, Veld carry/seated, and Branforth kneel/carry continuity. North generation was rejected for insufficient Higgsfield credits before a job was created. Its prompt, endpoint hashes and reviewed 155-sample baseline are saved. Local existing-source/controller work remains available.

The selected ledger contains 814 clips. This is an inventory, not a count of clips needing regeneration or proof of complete acceptance. No export or owner acceptance is claimed. Current evidence: docs/HANDOFF_MARSH_WEST_TRANSITIONS_2026-09-13.md, docs/HANDOFF_MARSH_SOUTH_IDLE_2026-09-13.md and docs/HANDOFF_MARSH_NORTH_TRANSITIONS_2026-09-13.md. Earlier dated reports retain historical evidence rather than the current queue.


## Construction overhead launch hatch - September 12, 2026

Circular overhead hatch and source-aligned opening integrated. Closed/half/open native states reviewed in four directions, plus room placement. Deployment state/timing unchanged. Cradle camera review and drone decision remain open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.

## Construction overhead assembly bench - September 12, 2026

The assembly bench now uses an overhead parked-arm companion with controls facing room center. Native q0/q1/q3 reviewed; q2 omits the bench. Cradle/hatch camera review and drone design decision remain open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.

## Construction panel pallet overhead companion - September 12, 2026

The tall glossy panel rack is replaced by a matte flat-storage pallet in Construction. Live q2 placement reviewed with inward catches and aspect-preserving bounds inside the old maximum size. Four alternate pallet placements now pass native inward-facing/bounds review. Other floor equipment facing remains open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.

## Construction static equipment material pass - September 12, 2026

Cradle, bench and launch hatch now select a Construction-only matte atlas. Source-region and transparency probes plus q0-q3 native review pass. Original drone source retained. Panel rack and floor-equipment facing review remain open. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.

## Construction material repair in progress - September 12, 2026

Four overhead fabrication-bank directions now use a matte casing repaint. Native mounting reviewed after preserving wall_contact metadata. Roller/spool refinement now passes native review; independent floor equipment remains open; this room is not complete. See docs/CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md. No export.

## Biomass Digester material correction - September 12, 2026

Biomass Digester retains the strong four-direction Biomass Processing wall geometry with orange hardware moved into a muted feedstock-moss family. The shared service console now uses a Biomass-only legibility tint. The supplemental service-bench source has true alpha and lifted matte midtones, eliminating its white exterior field. Native q0-q3 reviewed. See docs/BIOMASS_DIGESTER_OWNER_MATERIAL_REPAIR_2026-09-12.md. Source workspace only; no export.

## Isolation Vault owner asset correction - September 12, 2026

Isolation Vault now uses the accepted south Emergency Isolation bank through exact turns in north/east/south/west. The obsolete north-only baked perimeter and all Battery Array furnishings inherited by the vault have been removed. The independent Battery Array test-bench source received a matte steel/orange highlight pass without geometry or alpha changes. Native vault q0-q3 and battery-room placement reviewed. See docs/ISOLATION_VAULT_OWNER_ASSET_REPAIR_2026-09-12.md. Source workspace only; no export.

## Clone Growth Wall overhead family - September 12, 2026

Clone Lab now uses the owner-approved east Clone Growth bank through exact turns in north/east/south/west. The outer service rail stays wall-side while the tissue window, microscope, keyboard and consumables face inward. The former frontal north composition and unrelated shallow south appliance strip remain archived but are no longer live. Native q0-q3 reviewed. See docs/CLONE_LAB_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.

## Bio Culture Wall overhead family - September 12, 2026

Bio Lab now uses the accepted south overhead microscope bench through exact turns in north/east/south/west. Jar lids, dishes and worktops read from above; microscope eyepieces and work access face inward. Tall trough/front-elevation companions remain archived but are no longer live. Native q0-q3 reviewed. See docs/BIO_LAB_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.

## Crew Hab three-berth overhead wall - September 12, 2026

Crew Hab now uses the accepted compact three-pod berth bank through exact turns in north/east/south/west. Mattress and pillow access faces inward and sleeping capacity no longer changes by direction. The rejected oversized bed/wardrobe/canopy family and its lamp overlay remain archived but are no longer live. Native q0-q3 reviewed; 176 layouts, 20 side variants, 47 cards and 72 crew-life cases pass. The broader crew-activity run timed out on an unrelated listening_post0bill station-choice assertion and was left to the concurrent gameplay/character work. See docs/CREW_HAB_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.

## Maintenance Repair Wall overhead repair - September 12, 2026

Maintenance Bay now uses the accepted south overhead tool bench through exact turns in all four directions. Tool grips, vise and drawer handles face inward; tall side/elevated north sources are no longer live. Saturated orange is muted and border-connected neutral background is transparent while steel tools and the yellow cloth remain distinct. Native q0-q3 reviewed. See docs/MAINTENANCE_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.

## Xeno Containment Wall strict overhead repair - September 12, 2026

Xeno Lab now uses one shallow overhead containment bank through exact quarter turns for north/east/south/west. The sealed specimen lid, scanner, hatch and glove ports remain readable; rear rail stays wall-side and every work edge faces inward. The prior north elevation, unrelated side conversions and unrelated south bank remain archived but are no longer live. Native q0-q3 reviewed; 176 layouts, 20 side variants and 47 cards pass. The separate native base-view Xeno test still reports q1/q2 workbench status-strip failures; its source-aperture audit passes and this wall repair does not claim that operating-effect issue. See docs/XENO_OWNER_OVERHEAD_REPAIR_2026-09-12.md. Source workspace only; no export.

## Listening Post Deepwater standardization - September 12, 2026

The live Listening Post now uses inward-facing navy/teal/brass Deepwater wall banks in all four orientations. North is an exact 180-degree counterpart of the accepted south bank; the old q0 U installation and bright north pack remain archived but are no longer selected. Listening-only floor equipment replaces saturated red trim with muted brass while preserving geometry, activity anchors, operating effects and the Radio Lab source. Native q0-q3 reviewed; 176 layouts, 20 side variants, 47 cards and native operating-effect checks pass. See docs/LISTENING_OWNER_REPAIR_2026-09-12.md. Source workspace only; no export.

## Cryo Chamber strict overhead walls - September 12, 2026

All four selected Cryo support banks now derive from one strict orthographic
overhead source. The compressor, two vessel lids, coil, pipes, coolant cylinder,
terminal, three samples and gas bottle remain, without tall cabinet or cylinder
fronts rotating around the room. Real-display q0-q3 captures were inspected; 176
furnished layouts, 20 side variants, 47 card identities and both Cryo recovery
suites pass. q0 card bindings were refreshed. Concurrent q2 pod selection changed
after the baseline; this asset pass did not edit pod logic or placement. Evidence:
CRYO_OWNER_OVERHEAD_REPAIR_2026-09-12.md.

## Ore Refinery owner repair complete - September 12, 2026

All selected wall directions and the independent machinery atlas now share a
restrained burnt-orange engineering palette. Edge-connected neutral backgrounds
are transparent, removing the reported white seams while preserving enclosed pale
trim, gauges, yellow logistics marks, copper billets and ore. Real-display q0-q3
captures were inspected. 176 furnished layouts, 20 side variants, 47 card
identities and both production-ten route suites pass. The refreshed q0 card is
selected by all three consumers. Evidence: REFINERY_OWNER_REPAIR_2026-09-12.md.

## September 12 Current Turbine owner art repair (source only)

North q0 now uses a low overhead companion with an inward elliptical intake instead of the tall frontal source. East, south and west retain their accepted geometry with bright orange paint reduced to muted rust-brown. The arrow, rotation rules and power behavior are unchanged. Built-in generation returned RGB imitation transparency; deterministic cleanup removed the neutral exterior and 25 disconnected alpha specks before registration. Native q0-q3 review, Power Expansion, 176 preferred orientations, 20 side variants and all 47 card identities pass. See [Turbine owner repair](CURRENT_TURBINE_OWNER_REPAIR_2026-09-12.md). No character animation or export work.

## September 12 gameplay startup, hatch and cable follow-up (source only)

BRINE now opens dark, lights and consoles precede pod power, and humans emerge
with cold mist and a brief blue tint. Airlocks close after departure and reopen
before reentry; the north exterior hatch is visible while closed. Decorative
power cables are retired at their render/placement owners, including Data Archive.
The earlier power/selection and Studio/menu fixes remain. See
[gameplay handoff](GAMEPLAY_STARTUP_HATCH_HANDOFF_2026-09-12.md) for implementation,
native evidence, save checks and limits. The original power/turbine playtest build
is still unidentified; no speculative balance change or new EXE. Other sessions
retain room art and character animation replacement work.

## September 12 Shield Generator orange correction (source only)

The weak hull cradle remains absent and all four selected Shield wall directions now use restrained rust-brown construction beneath graphite/steel machinery. Compact amber indicators remain legible; geometry, placements and gameplay state are unchanged. The q0 card matches the live room. Native q0-q3 review, 176 preferred orientations, 20 side variants and all 47 card identities pass. See [Shield handoff](SHIELD_ORANGE_HANDOFF_2026-09-12.md). No gameplay, character animation or export work.

## September 12 Battery Array orange correction (source only)

All eight selected split-wall registrations now use a coherent muted family across north, east, south and west. Large orange shells became dark rust-brown while compact amber/yellow indicators remain readable; geometry, inventory and placements are unchanged. The q0 card matches the live room. Native q0-q3 review, 176 preferred orientations, 20 side variants and all 47 card identities pass. The north source still needs a later camera conversion under the top-down owner contract. See [Battery handoff](BATTERY_ORANGE_HANDOFF_2026-09-12.md). No gameplay, character animation or export work.

## September 12 Solar Array orange correction (source only)

The selected north, side and south wall-length sources now use restrained burnt-orange structural accents while preserving their machinery, geometry and shading. The q0 card matches the live room. Native q0-q3 review passes, along with 176 preferred orientations, 20 side variants and all 47 card identities. Explicit Hydroponics stand, Anomaly task-light and Shield cradle removals were also confirmed already effective; Isolation Vault's old q0 flush wings remain open. See [Solar handoff](SOLAR_FACING_HANDOFF_2026-09-12.md) and [removal audit](OWNER_ASSET_REMOVALS_2026-09-12.md). No gameplay, character animation or export work.

## September 12 Studio scale and title preview (source only)

Studio now offers Scale: Bill -> Hidden / Standing / Walking and a Place button.
The preview uses current Bill art at gameplay scale, respects local clearance and
does not enter saved layouts. Continue Loop's summary/schematic is on the right.
Native scale/movement, three-size saved-title and existing editor/menu checks pass.
See [Studio/menu handoff](GAMEPLAY_STUDIO_MENU_2026-09-12.md). The non-art playtest
goal continues with startup, airlock presentation and decorative cables. No EXE.

## Veld identity correction selected - September 12

Veld is a woman with medium-brown skin, a silver-streaked dark bun and no glasses,
including under her fitted helmet. Her original concept controls identity.
Selected corrections cover all four directions of idle, walk, scanner and
kneel/sample/stand, plus east helmet donning/removal: 29 body clips and 27
helmet variants, 348 frames. The ledger records 56 selected corrections;
278 other Veld variants remain under identity review. The full Veld, Branforth
and Marsh replacement goal remains open; these counts do not imply completion.

The two helmet transitions use six authored key poses, explicit holds and the
original twelve-slot timing for each action. Held helmets are empty, the worn
helmet is fitted, and endpoints exactly match corrected bare/equipped idle.
The taller frozen transition canvas preserves the overhead lift. Source 01,
rejected for a duplicated face inside the held helmet, remains beside corrected
source 02 and both exact prompts. A legacy endpoint overwrite was fixed so
selected poses cannot silently restore older identity art.

Native selected-source, timing and endpoint checks pass: 170 body / 164 equipped
states, zero failures. Preservation validation reports 670 original frames and
108 manifests unchanged, zero errors and no border touches. Evidence:
output/crew-replacement-2026-09-12/veld/helmet-transition-{selected,validation}.log;
helmet-transition-study-native/all-phases.png and selected native phase captures.
The all-phase contact and selected overhead pose were visually inspected.
Continuous locker pickup/placement and live transition occlusion remain open.

Earlier continuous laboratory work review covers north/east/south, bare and
helmet-equipped: each bounded run captures 63 frames over 6.2 simulation seconds
through kneel/sample/stand/walk, retaining equipment and fixed work position.
Evidence is in live-core-review{,-east,-south,-helmet,-helmet-east,-helmet-south}/
under the same output directory. West live work, broader activity joins and the
remaining life, water, death and other action families still require review.
Per-clip ledger rows retain prior evidence; missing evidence is not proof of a
required redraw. No export or whole-library visual acceptance is claimed.

Changed: tools/prepare_veld_helmet_transition_body.py, tools/veld_scanner_revision.py,
tools/rebuild_human_crew_art.py, tests/playtest_human_crew_candidate.gd, Veld selected
frames, source/review records and the animation ledger. The maintained character
workflow and installed mirror now require selected endpoint comparisons and
pivot-aware taller-canvas registration. Bill remains unchanged; Marsh helmet-free.

Native live locker follow-up: the focused Veld airlock test passes 224 travel
samples, equipment pickup/return, pause, power interruption and disk save/restore.
Captured phase traces compare the actual runtime texture bytes with the selected
source. Pickup at 0.321 seconds uses frame 2 with the helmet in her hands and
shelf hidden. This resolves the apparent empty-hand ambiguity in the small room
capture; no runtime animation mapping repair was needed. Evidence:
output/crew-replacement-2026-09-12/veld/helmet-locker-source-trace.log and
helmet-locker-source-trace-native/*-pose.json / *-actor.png / room captures.
These are discrete checkpoint captures; continuous locker motion remains open.

Continuous Veld locker review now captures both actions at 0.05-second steps:
44 pickup captures through 2.15 seconds and 46 removal captures through 2.25
seconds, including all twelve authored slots in each. Fixed-foot and equipment
completion checks pass, and runtime texture bytes match selected sources.
Native phase review found a remaining visual mismatch: the staged shelf helmet
is larger than the fitted held helmet, causing a size jump at pickup/return.
Keep live visual acceptance open until the shelf/held size relationship is fixed.
Evidence: output/crew-replacement-2026-09-12/veld/helmet-locker-continuous.log and
helmet-locker-continuous-native/{continuous-equip.json,continuous-remove.json,
handoff-phases.png,continuous-equip.gif,continuous-remove.gif}. That first run's
summary reused the broad test label; its actual scope is continuous locker motion,
travel and UI. The fixture now reports mode-specific coverage accurately.
Next: reconcile the staged shelf helmet with Veld's fitted held source while
preserving other actors and the shared interaction anchor.

Veld shelf scale correction: AirlockService now derives a 0.6 staged-helmet
scale from the active/reserved Veld locker request, retaining it while she stands
at the interaction point after return. Other servicing actors and Studio retain
the existing default. The shelf base and shared interaction point are unchanged;
no new save field or gameplay timing was introduced. The held shell is roughly
12 room units wide at Veld's existing body scale, matching the 12-by-15 shelf draw.
Changed: scripts/airlock_service.gd, scripts/grid_canvas.gd and
rooms/underwater/airlock-v1/airlock_view.gd.

The repeated native continuous Veld review passes 223 travel samples, both full
helmet actions, fixed-foot registration and UI. Native shelf-handoff-contact.png
was inspected: the previous conspicuous shelf/hand size jump is corrected.
Evidence: output/crew-replacement-2026-09-12/veld/helmet-locker-fitted-shelf.log and
helmet-locker-fitted-shelf-native/ captures. This establishes bounded q0 Veld
locker continuity, not every room rotation or broader animation acceptance.
Next: resume remaining Veld action-family identity corrections and the broader
Branforth/Marsh review/replacement queue. Counts remain 50 corrected Veld variants.

East seating identity study: generated canonical female Veld sit-down, seated
idle and rise sources, registered with one standing-derived anatomical ruler and
exact corrected standing endpoints. Eighteen bare study frames are prepared by
tools/prepare_veld_seated_identity.py under the identity folder's
review/seated-east-body-01/. Registered body contact was inspected. Source 01
had a baked checkerboard and is rejected for extraction; source 02 uses keyed
magenta. Both raws and exact prompts are retained. The source idle has two
authored settling poses with explicit holds, not six independent drawings.
Fitted equipment, furniture contact and native playback remain to be reviewed;
these frames are unselected and the 50-variant correction count is unchanged.

East seated fitted study now contains 18 bare and 18 helmet poses with bounded
collar edits and exact standing/seated/rise joins. Native study checks pass
original timing and all paired source slots; middle-descent native capture was
inspected. Evidence: output/crew-replacement-2026-09-12/veld/seated-identity-study.log
and seated-identity-study-native/page-00-frame-03.png. Added
prepare_veld_seated_helmet.py and seated-identity fixture modes. The fixture now
creates the final mode-specific output directory and checks every screenshot
write; an initial missing-directory run was corrected and rerun successfully.
The study remains unselected pending furniture contact and selected-pack checks.
Current correction count stays 50 variants.

East seated sequence selected: sit-down, seated idle and rise now use corrected
female Veld body art and pose-fitted helmets, adding six variants / 36 frames.
Totals are 29 body clips + 27 equipment variants = 56 corrected variants,
348 frames; 278 other Veld variants remain under identity review. All selected
pixels, original timing and corrected standing/seated joins pass the native
fixture; the selected endpoint phase was inspected. Preservation validation:
670 original frames / 108 manifests unchanged, zero errors or border touches.
Evidence: output/crew-replacement-2026-09-12/veld/seated-identity-{selected,validation}.log
and seated-identity-selected-native/page-00-frame-05.png. Explicit overrides
respect per-slot source offsets: only the embedded standing endpoints need the
smaller crop. Sources, prompts and registration remain preserved.

Current lounge and observation stations request north-facing seated actions;
this east selection does not claim live chair contact. Next: north-facing seated
and reading identity replacements, then continuous furniture review. The full
Veld/Branforth/Marsh goal remains active. Bill unchanged; Marsh helmet-free.

## September 12 gameplay power follow-up (source only)

Drone bays retain service for their paid cycle instead of losing it when a next-cycle
forecast cannot afford the bay. Prepaid charging continues at zero reserve; pause,
master-off and the next unfunded cycle still stop it. New loops start with no
blueprint selected. Power feedback explains battery charge/discharge; turbine
feedback names the intake cell and blocking object. Focused economy, drone/save,
native UI and hardware checks pass. No turbine rotation defect reproduced; no balance
change. Original playtest build/save unidentified. See
[gameplay handoff](GAMEPLAY_POWER_HANDOFF_2026-09-12.md). No EXE.

## Veld identity correction - owner direction, September 12

Dr. Veld is a woman. Her canonical identity is the original concept at
character/dr-veld-v1/concept-01.png: silver-streaked dark bun, cobalt Science
markings and ivory chest panels. She does not wear glasses, including inside
the fitted helmet. Preserve her face through every direction and action.

Recent generated references drifted from this identity. Prior technical passes
and selected-source matching do not establish identity acceptance. Reopen Veld
body and equipment visual review; do not propagate the recent male-looking or
glasses-bearing source studies. South sample strip01 and fitted heads01 are
unselected and rejected as identity references. Retain their raw files/prompts
as provenance. East sample is installed but requires identity correction along
with affected existing clips. Use the original concept for identity and existing
frames only for motion/registration. Review bare and helmeted faces together.

## September 12 owner playtest handoff - new room art contract

All room equipment moves to top-down, inward-facing art on every wall. Older
conflicting north elevations/fixed-facing acceptance is superseded. Slight north
perspective is allowed only when low and rotation-safe. Observation portholes become
background wall/riser art. This session is handing off; the broad goal is unfinished.

Start with [room-art/playtest handoff](ROOM_ART_HANDOFF_2026-09-12.md) and
[top-down direction/workflow](TOP_DOWN_ART_DIRECTION_2026-09-12.md). Raw notes and
source-selection snapshot are preserved. Power/reserve and turbine behavior are
owner-reported issues awaiting diagnosis; no playtest fixes were implemented in
this consolidation. Preserve the concurrent work recorded below.

Future direction accepted: partially procedural maps assembled from authored pieces,
with a viable starting area, variable mountains/regions and buried discoveries.
Use reproducible expedition seeds and preserve excavation/discovery state. Keep
the authored map for testing; generation follows lighting/excavation playtesting.
See [accepted map direction](LIGHTING_MOUNTAINS_2026-09-12.md#accepted-future-map-generation-direction).

Lighting/mountain session closed on September 12. Accepted decisions, findings,
verification limits and next steps are consolidated in the
[session closeout](DERELICT_LIGHTING_MOUNTAIN_SESSION_2026-09-12.md).
Source changes remain in the working tree; no session commit or EXE export.

## 2026-09-12 - Lighting and excavatable mountain foundation

New loops have broad connected mountains and a buried service-wreck pocket.
Mining opens reachable exposed sections into tunnels. Dense exterior haze now
uses station, diver and drone beams with terrain shadows, drilling silt and saved
survey memory; interiors stay readable. Enemies are deferred. Native visuals,
shader pixels, paid clearance, save and hardware checks pass. See
[lighting/mountain handoff](LIGHTING_MOUNTAINS_2026-09-12.md). Source only, no EXE.

Derelict lights now start off. Completed repair removes weathering; lights
then follow power availability and the interior switch. All six paid-repair
transitions and material checks pass natively. Mixed repaired-ward wall geometry
is also fixed. See [derelict handoff](DERELICT_CONDITION_2026-09-12.md). No EXE.

## 2026-09-12 - Autonomous crew conversations (source only)

Nearby available crew now face each other for brief conversations, alternating speaker/listener states before resuming routines. A cooldown keeps exchanges occasional; needs, active jobs and emergencies take priority. Partner/cooldown persist in actor saves. Social and primary-work fixtures passed, and native conversation placement was reviewed. See docs/CREW_SOCIAL_2026-09-12.md. No new talking art or EXE export; deliberate social visits and relationships remain future scope.

## 2026-09-12 - Primary workplaces and autonomous needs (source only)

Owner accepted mostly autonomous crew with a primary workplace, compatible synergy, meals and sleep. Implemented inspector assignment, physical work attendance, +1 Metal/Data specialty bonus, slower matching fatigue, saved assignments and autonomous work/meal/sleep/return. Needs breaks require reachable services so missing facilities do not prevent construction. Marsh retains battery behavior. See docs/CREW_PRIMARY_WORK_2026-09-12.md for changed files and evidence.

Checks: primary routine, 72 room-life cases, diver mining and hull repair passed; native work/eat/sleep captures reviewed. Construction regression remains unresolved: four Branforth directions fail because he waits without a clear route from spawn, including below the needs threshold. Details and probe evidence in the handoff. Automatic mining/repair order generation remains later scope. No EXE rebuilt.

Helmeted crew can now mine surveyed mineral deposits via the Diving Airlock mission selector. Trips use existing tank/range/recall rules and deliver 2 Metal after safe return. Native inspector dispatch, locker fitting, mine/cargo saves and return checks pass; existing salvage regression passes. See [diver mining handoff](DIVER_MINING_2026-09-12.md). Source only; prior hazard EXE predates this addition.

## Three-crew detailed replacements selected - September 12, 2026

Veld east sample inspection and its fitted helmet are now selected; native
source/timing/endpoints and preservation checks pass. Live workplace review
remains pending. See CREW_ACTION_REVIEW_2026-09-12.md and the clip ledger.

All twelve directional instrument actions are selected across Veld, Branforth
and Marsh. Native selected-source checks pass; complete-pack refresh passes
19,259 checks. Live workplace and repair/life/water/death review remain unfinished.

Branforth west meter action is selected with fitted helmet poses and corrected
amber-tool endpoints. Native source checks pass; north and wider review remain.

Branforth south diagnostic-meter action is selected with fitted helmet poses.
Native selected-source checks pass; west/north and broader action review remain.

Veld scanner replacements are selected in all four directions, bare and equipped.
Native selected-source checks pass; complete-pack refresh passes19,259 checks.
Branforth remaining diagnostic directions and broad action/live review remain.

Veld west scanner is also selected with authored fitted helmet poses; native
selected-source checks pass. Veld north and broader three-crew review remain.

Veld south scanner is selected with authored fitted helmet heads. Corrected
directional pivot registration passes native selected-source checks; original
sources remain unchanged. North/west role actions and broader review remain.

Marsh controller interactions are selected in all four directions. Native source
and timing checks pass; complete-pack refresh passes 19,259 checks. Live workplace
and remaining human/life/repair/water/death visual review are still outstanding.

Marsh south controller interaction is selected with independent idle endpoints.
Native timing/source checks and six rendered samples passed; original sources
remain unchanged. West controller is also selected after native source checks; north and broader action review remain.

Veld, Branforth and Marsh use their complete detailed packs. Both humans have
character-fitted locker pickup/don/removal and all four cargo, seating and sleeping
directions selected. All 256 rest joins pass. Live lounge and berth review covers
north-facing activities; other directions have clip checks, not live-room approval.

Marsh east/west walk/run use corrected measured anatomy. All four carry directions
now alternate legs at their original four-frame timing with distance cadence.
West walk/run/carry and north/south carry each pass 60 native source comparisons;
exported filmstrips and axial native sampled stills were inspected. Source checks
preserve 211 original frames/1 manifest, with no equipment or border errors.
Marsh has all four draw/weld/stow sequences, isolated from old aliases.
South reach sequence01 is now selected with deep forward lean and native
painted-leaf contact. Twelve draw/stow renderer samples and five active poses
pass. Selected-pack native references, joins and timing checks report zero
failures; source validation preserves 211 frames/1 manifest with zero errors.
Marsh east controller interaction is selected, preserving distinct original idle
endpoints. Native source checks and original-asset validation pass.
Production navigation/clearance is unchanged.
Veld east scanner interaction is selected in both bare and fitted-helmet packs.
All twelve native source comparisons pass; 670 original frames and108manifests
remain unchanged. Live-workplace review remains.
Branforth east diagnostic interaction is selected in bare/fitted packs;
selected-source native checks pass and669originalframes/108manifests are intact.
Complete-pack refresh:19,259checks,0failures (complete-packs-role-update.log). See
[action review](CREW_ACTION_REVIEW_2026-09-12.md) for exact evidence and changed files.

Remaining: continuous cargo motion and pickup/unload joins, broader role/work,
dining/reading, construction, rest and water/death interiors, and full visual
acceptance. Locker containment/sidebar failures remain separately recorded in the
[fitted helmet handoff](CREW_FITTED_HELMETS_2026-09-12.md). Skills and the visual bible
track selected revisions and limitations. Bill is unchanged. No new export.

# BrineSpace current status

Med Center side counters (2026-09-12): low overhead diagnostic banks selected; tool grips and cartridge releases inward. Card refreshed. Native eight screen cases, 176 layouts, 20 variants and 47 card identities pass. Other directions/placement metadata unchanged. See docs/MED_CENTER_OVERHEAD_HANDOFF_2026-09-12.md.


Med Office side counters (2026-09-12): low overhead banks selected with inward controls and operating-only screens; default card refreshed. Native eight screen cases, 176 layouts, 20 variant regressions and 47 card identities pass. Other directions/placement metadata unchanged. See docs/MED_OFFICE_OVERHEAD_HANDOFF_2026-09-12.md.


Crew Hab west matte (2026-09-12): authored west berth now matches the matte idle/steady operating-lamp treatment. Native direct/retained lamp checks, 176 layouts and 20 variant regressions pass. Other views and placement metadata unchanged. See docs/CREW_HAB_MATTE_HANDOFF_2026-09-12.md.


Crew Hab east matte (2026-09-12): berth material repair selected with a separate steady operating lamp. Native direct/retained power and steady-light checks, 176 layouts and 20 variant regressions pass. Other views and placement metadata unchanged. See docs/CREW_HAB_MATTE_HANDOFF_2026-09-12.md.


Storage Bay sides (2026-09-12): low overhead cargo/inventory platforms selected with inward releases and operating-only amber console. Both sides reviewed; four direct/retained state cases, 176 layouts and 20 variant regressions pass. North/south pixels and placement metadata unchanged. Owner acceptance and station pause remain open. See docs/STORAGE_SIDE_HANDOFF_2026-09-12.md.


Data Archive sides (2026-09-12): low overhead drawers/indexing desks selected with inward controls and operating-only screens. Both walls reviewed; eight direct/retained screen cases, 176 layouts and 20 variant regressions pass. North/south pixels and placement metadata unchanged. Owner acceptance and station pause remain open. See docs/ARCHIVE_SIDE_HANDOFF_2026-09-12.md.


Battery Array sides (2026-09-12): low overhead east/west companions selected with inward controls and outer cabling. Both native sides reviewed; 176 layouts and 20 variant regressions pass. North/south pixels and all placement metadata unchanged. Owner aesthetic acceptance remains open. See docs/BATTERY_SIDE_HANDOFF_2026-09-12.md.


BRINE south service (2026-09-12): matte idle source and operating-only screen selected; native direct/retained state checks, 176 layouts, 20 variants and 47 card identities pass. Refreshed idle card reviewed. Station pause and owner aesthetic acceptance remain open. See docs/BRINE_CORNER_SIDE_HANDOFF_2026-09-12.md.


Salvage matte pair (2026-09-12): north bench and south tote selected; refreshed native card reviewed, 176 layouts and 47 card identities pass. Owner side-view acceptance and alternate south bench selection remain open. See docs/SALVAGE_SIDE_HANDOFF_2026-09-12.md.


Cold Store side pair now uses the overhead west fridge and matte east food rack. Native art/card review,176layout routes,20side variants and47card parity pass. See docs/COLD_STORE_SIDE_HANDOFF_2026-09-12.md. Owner visual and retained/pause review remain; no export.


Turbine east/west now use the overhead skid source with inward intakes and source-local powered effects. 176 layout routes, 20 side variants and four native temporal effect checks pass. See docs/TURBINE_SIDE_REVISION_2026-09-12.md. Owner aesthetic and retained station pause review remain; no export.


BRINE corner-state update (September 12): northwest and northeast banks now use quiet idle art plus operating screen traces. All15screens verified individually in direct and retained renders; layout/variant and card checks pass. Other BRINE painted screens and owner visual acceptance remain. See docs/BRINE_CORNER_SIDE_HANDOFF_2026-09-12.md.


Airlock directional update (September 12): south and north locker companions are installed. North mounting now follows exposed, shared and low-wall modes while preserving the helmet handoff. Native Bill q2 service/interlock checks and current headless service/176 layouts pass. Side lockers and exposed shelf-support polish remain; see docs/AIRLOCK_FACING_HANDOFF_2026-09-12.md.


Airlock south locker installed q0 with shared helmet/fitting anchor and visible pickup/return attachment. Headless service and176layouts pass; native Veld handoff reviewed, but3sidebar viewport assertions fail. Card refreshed. Other locker directions remain. See docs/AIRLOCK_FACING_HANDOFF_2026-09-12.md.


Facing ledger reconciled against fresh RoomDatabase: 47 identities, no missing/duplicate rooms or absent direction entries. This is inventory coverage, not completion; library/live fit, Airlock lockers, BRINE states and owner camera review remain. See docs/FACING_COVERAGE_AUDIT_2026-09-12.md.


BRINE NE bank now has inward catches/buttons with its filter and console inventory retained. Native fit and layout/side checks pass; card refreshed. Display states and final camera acceptance remain pending. See docs/BRINE_CORNER_SIDE_HANDOFF_2026-09-12.md.


BRINE NW bank now has inward access with six screens/two bottles retained. Native fit and layout/side checks pass; card refreshed. Painted display states, NE arm and owner camera acceptance remain pending. See docs/BRINE_CORNER_SIDE_HANDOFF_2026-09-12.md.


BRINE northwest side study rejected: improved inward access but unintended north-arm and instrument changes. Live art retained; tighter repair pending. See docs/BRINE_CORNER_SIDE_HANDOFF_2026-09-12.md.


Gravity Loom north service pair installed q2 with doorway gap preserved. Service companions now cover all compass directions; native review, 176 layouts and 20 variants pass. Owner camera acceptance remains open. See docs/GRAVITY_SIDE_HANDOFF_2026-09-12.md.


Gravity Loom side control console now installed opposite its calibration bench in q1/q3. Native pair review, 176 layouts and 20 variants pass. North companions remain pending. See docs/GRAVITY_SIDE_HANDOFF_2026-09-12.md.


Gravity Loom calibration weights now have an inward side companion, installed east q1 and mirrored west q3. Native review, 176 layouts and 20 variants pass. North and control-console companions remain pending. See docs/GRAVITY_SIDE_HANDOFF_2026-09-12.md.


Reactor north service companion installed in q2, replacing its east station. All compass companions now available; native fit, side-variant and 176-layout checks pass. Owner camera acceptance remains open. See docs/REACTOR_SIDE_HANDOFF_2026-09-12.md.


Reactor side service station now installed in all four layouts, switching sides around the cooler. Native review and 176 layout checks pass; q0 card refreshed. North companion remains. See docs/REACTOR_SIDE_HANDOFF_2026-09-12.md.


New Reactor side-service companion registered and reviewed in east/mirrored-west library views at 120-unit length. Inward access corrected by source edit. Live fit and north companion remain pending. See docs/REACTOR_SIDE_HANDOFF_2026-09-12.md.


Shield side valve grips corrected inward with tanks/compartments preserved and quiet screens. Native q0/q2 and refreshed card reviewed; 176 layouts, 20 variants and 47 card bindings pass. Owner side-camera acceptance pending. See docs/SHIELD_SIDE_HANDOFF_2026-09-12.md. Source only.


Isolation side machinery revised with all three switchboxes/levers preserved and powered source-local lamps. Native side review, 12 lamp/renderer cases, 176 layouts and 20 variants pass. Owner camera acceptance pending. See docs/ISOLATION_SIDE_HANDOFF_2026-09-12.md. Source only.


Listening Post side consoles revised toward overhead view with inward access and quiet screens. Native side review, sonar off/on/temporal checks, 176 layouts and 20 variants pass. Owner camera acceptance remains pending. See docs/LISTENING_SIDE_HANDOFF_2026-09-12.md. Source only.


Radio Lab side banks now show overhead worktops, inward handles and dark static screens. Native comparison preserves all prop bounds and q0/q2 views; 176 layouts and side variants pass. Owner side-camera acceptance remains pending. See docs/RADIO_SIDE_HANDOFF_2026-09-12.md.


Airlock south check bench now uses inward-facing overhead art. Native review and scoped service/176-layout checks pass; directional suit lockers and side-view owner acceptance remain pending. See docs/AIRLOCK_FACING_HANDOFF_2026-09-12.md. Source only.


## Airlock south reserve-air bank corrected - September 12, 2026

q2 overhead bank now faces inward; native review and Airlock/layout checks pass. Other rotations unchanged. See AIRLOCK_FACING_HANDOFF_2026-09-12.md. South check bench, lockers and other rooms continue.


## Airlock west reserve-air bank corrected - September 12, 2026

Overhead west bank installed in q3 with inward service access; east library companion reviewed. Other rotations unchanged. Airlock service and 176 layout cases pass. See AIRLOCK_FACING_HANDOFF_2026-09-12.md. Remaining directional art continues.


## Airlock locker service restored - September 12, 2026

Moved default lockers clear of wall collisions/disconnected fitting space while retaining scale and helmet attachment. Service suite now passes (Bill four rotations, Veld/Branforth q0), plus 176 layouts and card parity. Native placements/card reviewed. See AIRLOCK_FACING_HANDOFF_2026-09-12.md. Directional art/full catalog continue; no export.


## Airlock side check bench installed - September 12, 2026

q1/q3 inward benches fit the furniture envelope and clear chamber; q0/q2 unchanged. Existing baseline locker-service failures remain, with no new final failures. See AIRLOCK_FACING_HANDOFF_2026-09-12.md for exact test scope. No card/export change.


## Airlock check-bench side companion - September 12, 2026

New east/mirrored west bench reviewed in library at 100-unit length. Live host drawing and chamber/service clearance still pending; no runtime/card changes. See AIRLOCK_FACING_HANDOFF_2026-09-12.md.


## Airlock live directional inventory - September 12, 2026

Four native views confirm modular furnishings relocate without directional art changes. Recorded source regions and helmet/service constraints; side repairs remain required. No production changes. See AIRLOCK_FACING_HANDOFF_2026-09-12.md.


## Salvage side bench companions - September 12, 2026

One east source and mirrored west reviewed natively with inward vise, quiet indicator and corrected handle cutout. Library-only; fixed workshop unchanged. See SALVAGE_SIDE_HANDOFF_2026-09-12.md. South host fit and broader catalog remain active.


## Corridor directional inventory corrected - September 12, 2026

Existing shared architecture covers straight/corner/junction rotations; 36 raised views visually reviewed with selected full-size checks from 72 native captures. Twelve stale missing-art entries corrected. No production changes. See CORRIDOR_COVERAGE_HANDOFF_2026-09-12.md. Full room and side work continues.


## Mycelium side access corrected - September 12, 2026

Both lower cabinets and hanging tools now face inward; native side review and layout/effect checks pass. North/south unchanged. See MYCELIUM_SIDE_HANDOFF_2026-09-12.md. Owner side-perspective acceptance and full catalog remain open.


## Galley side companions - September 12, 2026

One overhead east serving source registered and reviewed with mirrored west at existing counter scale. Inward mug handles verified. Library-only; live kitchen, serving layout and cards unchanged. See GALLEY_SIDE_HANDOFF_2026-09-12.md. Full catalog and side feedback continue.


## Observation south shelf companion - September 12, 2026

Missing overhead south shelf added to library and reviewed natively. Fixed live north window/south entrance retained; no runtime/card change. See OBSERVATION_SOUTH_HANDOFF_2026-09-12.md. Side feedback and full catalog continue.


## Turbine elevated side study rejected - September 12, 2026

Native comparison found weaker intake readability and tower-like construction despite more top surfaces. Preserved study and lessons; live defaults unchanged. See TURBINE_SIDE_REVISION_2026-09-12.md. Side revision and full room catalog remain active.


## Listening Post live north idle repair - September 12, 2026

U-shaped console now has quiet electronic displays and unlit strip lamps; powered sonar sweep retained. Native/card review and layout checks pass, placements and other rotations unchanged. See LISTENING_NORTH_HANDOFF_2026-09-12.md. Side review/full catalog continue; no export.


## Listening Post north library companion - September 12, 2026

Idle console registered and natively reviewed; live U-shaped q0 and all four views unchanged. Live sweeps remain temporal. Actual U-shaped idle displays and E/W perspective still need review. See LISTENING_NORTH_HANDOFF_2026-09-12.md. No card or export change.


## Heat Recovery side companions added - September 12, 2026

One authored east asset supplies mirrored west; both reviewed natively with inward controls. North/south companions retained. All four live views and prop metadata unchanged; no doorway placement change. See HEAT_NORTH_HANDOFF_2026-09-12.md. Full catalog and owner side feedback remain active.


## Heat Recovery north companion - September 12, 2026

Matte north library prop registered and natively reviewed at 270-unit width; cable-loop cutout corrected. All four live views unchanged, south default/card retained. East/west companions remain. See HEAT_NORTH_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Shield north reviewed and retained - September 12, 2026

Native north fit/materials reviewed at actual q3; monitor effects verified all four orientations and injector q3. Corrected direction mapping in coverage; source/runtime/card unchanged. See SHIELD_NORTH_REVIEW_2026-09-12.md. Side review/full catalog continue.


## Isolation north feedback restored - September 12, 2026

Three source-local status lamps now pulse while powered. Direct/retained native checks and layout suites pass; off images and other powered orientations unchanged. Earlier north feedback gap resolved. See ISOLATION_NORTH_HANDOFF_2026-09-12.md. Side review/full catalog continue; no export.


## Isolation north idle-art checkpoint - September 12, 2026

Inactive north bank/card integrated; native review/layout checks pass and other rotations unchanged. q0 flush props show no operating changes; that cue remains under investigation. Other rotations retain battery effects. See ISOLATION_NORTH_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Crew Lounge east repair verified - September 12, 2026

Both side coffee machines open inward; separate galley effects verified in all four orientations. Native views/layout suites pass; north/south art and all prop metadata unchanged. Owner side aesthetic feedback remains open. See LOUNGE_REMAINING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Crew Lounge west coffee station - September 12, 2026

Missing west coffee station restored with inward access; lamp fully framed. North retained after review. Other three rotations and all prop metadata unchanged; layout suites pass. East coffee facing and owner side feedback remain open. See LOUNGE_REMAINING_HANDOFF_2026-09-12.md. No export.


## Mycelium operating feedback restored - September 12, 2026

Bench/filter effects now animate in all four orientations; north nozzle pulses restored on dry art. Retained native state checks, off-image parity and layout suites pass. Earlier missing-effect finding resolved; side art review remains. See MYCELIUM_NORTH_HANDOFF_2026-09-12.md. No export.


## Mycelium north art checkpoint - September 12, 2026

Dry north cultivation art/card integrated and natively reviewed; layouts/card parity pass, other views unchanged. State captures reveal no active effects because old irrigation targets are absent. Effect wiring remains required; see MYCELIUM_NORTH_HANDOFF_2026-09-12.md. Full catalog remains active; no export.


## Radio Lab north idle art - September 12, 2026

North waveform removed from static bank; physical reel, patch cables and headset retained. Card refreshed. Native review, operating captures, 176 layouts and card parity pass; other three rotations RGB-identical. See RADIO_NORTH_HANDOFF_2026-09-12.md. Side review and full catalog remain active; no export.


## Cold Store library companions - September 12, 2026

North/south fridge and rack companions registered and reviewed natively at 92-unit width. Fixed playable q0 remains RGB/metadata identical; no card or gameplay rotation change. Prompts, rejected studies and provenance retained. See COLD_STORE_REMAINING_HANDOFF_2026-09-12.md. Full catalog and side-view feedback remain active.


## Diving-room floor and material refinement - September 12, 2026

[Deck handoff](AIRLOCK_DECK_2026-09-12.md): fitted anti-slip wet deck with recessed side drains, quieter dry flooring and matte suit lockers integrated. Four native rotations and dry/wet actor visibility reviewed; all airlock route/service checks pass. Cards refreshed. Owner accepted this look at session close. Source only; no executable rebuild. See [session closeout](BILL_AND_AIRLOCK_SESSION_CLOSE_2026-09-12.md) for Bill, airlock and package evidence scopes.

## Side-view feedback and Med Bay checkpoint - September 12, 2026

Owner dislikes side views; exact target/reason remains unconfirmed. Prior native fit is not owner acceptance. Med Bay north idle material and card updated; side candidates stay pending owner review. Layout suites pass; operating-frame evidence captured. See MED_BAY_REMAINING_HANDOFF_2026-09-12.md. Full catalog remains active; no export.


## Anomaly Lab four directions reviewed - September 12, 2026

Third side specimen tubes restored, banks seated flush; north retained. Native review, 176 layouts and four-prop operating checks pass in all rotations. North/south unchanged; current card retained. See ANOMALY_REMAINING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Bio Lab four directions reviewed - September 12, 2026

Four side culture trays restored; drawer, lid and microscope access corrected inward. North idle screens/card refreshed. Native review, 176 layouts and centrifuge/storage state checks pass. Prop placements preserved; south unchanged. See BIO_REMAINING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Xeno Lab four directions reviewed - September 12, 2026

Correct inward geometry retained with quiet idle screens and painted markings preserved. Native/card review, 176 layouts and independent state checks pass. Rectangles/IDs unchanged; south unchanged. See XENO_REMAINING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Biodome four directions reviewed - September 12, 2026

Inward aquarium/valve access and dry idle irrigation integrated; side banks seated against walls. Native/card review, 176 routes and tree/aquatic state checks pass. Independent props unchanged; south unchanged. See BIODOME_REMAINING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Ore Refinery four directions reviewed - September 12, 2026

North idle/exterior repaired; side loading/service access corrected with industrial palette retained. Native review, 176 layouts, 47 card bindings and machinery state checks pass. Rectangles/IDs preserved; south unchanged. See REFINERY_REMAINING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Clone Lab four directions reviewed - September 12, 2026

Side cabinet/monitor access, catches and missing instruments corrected; north idle screens repaired. Native review, 176 routes, 47 card bindings and console/nutrient state checks pass. All rectangles/IDs preserved; south unchanged. See CLONE_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Research Lab four directions reviewed - September 12, 2026

Side instrument inventory and inward access corrected; all bounds/IDs preserved, north/south unchanged. Native review, 176 routes and scanner state checks in four rotations pass. See RESEARCH_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Research north idle art reviewed - September 12, 2026

North screen graphics corrected with equipment and bounds preserved. Native q0 and 176 layouts pass; other rotations unchanged. Side studies rejected for inventory drift. See RESEARCH_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Crew Hab directional review complete - September 12, 2026

East open-entry companion integrated; north retained. All inventories/rectangles preserved, other rotations unchanged. Native review, 176 routes and four desk state checks pass. See CREW_HAB_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Crew Hab west berth corrected - September 12, 2026

Fresh open-entry berth integrated with inward storage access and retained shelf inventory. Native review, 176 routes pass; all bounds/IDs and other rotations unchanged. See CREW_HAB_FACING_HANDOFF_2026-09-12.md. East/north and full catalog continue; no export.


## Quarantine four directions reviewed - September 12, 2026

North idle/keyboard and side case access/gauge inventory corrected. Native/card review, 176 routes and 47 bindings pass. All bounds/IDs preserved; final side changes leave north/south unchanged. See QUARANTINE_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Quarantine south companion integrated - September 12, 2026

Matching overhead bank now selected q2. Original berth/filter/monitor retained and relocated; other rotations unchanged. Native review, 176 routes and filter/monitor state checks pass. See QUARANTINE_FACING_HANDOFF_2026-09-12.md. Other directions and full catalog continue; no export.


## Pressure Control directional review complete - September 12, 2026

Retained side art seated against walls; needle overlays aligned with painted hubs. Native gauge state checks pass in all four rotations, with 176 routes passing. North ledger now names actual custom fitted source. See PRESSURE_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Maintenance directional review complete - September 12, 2026

Side bench access corrected with toolbox/reel retained per bank. Runtime inventory/bounds and north/south unchanged. Native review, 176 routes and four diagnostics state checks pass. See MAINTENANCE_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Maintenance north idle cleanup - September 12, 2026

Running wash water and task-lamp emission removed from idle art. Native review preserves inventory/bounds and other rotations; 176 routes pass. Card refreshed. See MAINTENANCE_FACING_HANDOFF_2026-09-12.md. Side facing and state review remain; no export.


## Tidal Condenser directional review complete - September 12, 2026

Side filters face inward, three coil returns restored, frames seated. North retained and accepted south unchanged. Native review, 176 routes and four-rotation pump/monitor state checks pass. See TIDAL_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Solar Array north and state review complete - September 12, 2026

North retained after native review; independent monitor operating/temporal changes verified in four rotations. Fitted banks and pumps remain static. South owner acceptance preserved. See SOLAR_FACING_HANDOFF_2026-09-12.md. Continue Tidal Condenser/full catalog; no export.


## Solar Array side inventory corrected - September 12, 2026

Four vents and two pumps restored per side bank; outer frames seated against walls. Native review and 176 routes pass. North/south and independent equipment unchanged. See SOLAR_FACING_HANDOFF_2026-09-12.md. North/state review and full catalog continue; no export.


## Biomass Digester four directions reviewed - September 12, 2026

Existing art retained after native facing and wall-fit review. Four localized operating indicators verified off/on and over time. No runtime or raster changes. See BIOMASS_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Mining Drone Bay four directions reviewed - September 12, 2026

North access/idle cleanup and inward side service cabinets integrated. All runtime inventories and rectangles preserved; south unchanged. Native/card review, 176 routes and 47 bindings pass. See MINING_FACING_HANDOFF_2026-09-12.md. Full catalog continues; no export.


## Mining Drone Bay missing south companion - September 12, 2026

Overhead service bank integrated q3; original independent equipment sizes and inventory preserved. Native fit/deployment reviewed, 176 routes and lifecycle pass. Other rotations unchanged. See MINING_FACING_HANDOFF_2026-09-12.md. Remaining directions and full catalog continue; no export.


## Salvage Drone Bay four directions reviewed - September 12, 2026

North/side sources reviewed and retained; side banks seated10 units outward against walls. Fleet props and north/south views unchanged. Native/card review,176 routes and47 bindings pass. See SALVAGE_DRONE_FACING_HANDOFF_2026-09-12.md. Full catalog continues with Mining Drone Bay; no export.


## Salvage Drone Bay missing south companion - September 12, 2026

Overhead disassembly bank installed q3; drone/hatch/winch retained at original sizes and relocated north. Native deployment and winch state checks,176 routes and lifecycle pass. Other rotations unchanged. See SALVAGE_DRONE_FACING_HANDOFF_2026-09-12.md. Other directions and full catalog pending; no export.


## Construction Drone Bay four directions reviewed - September 12, 2026

North/side art reviewed and retained; side banks seated10 units outward against walls. Independent fleet props and north/south views unchanged. Native/card review,176 routes and47 bindings pass. See CONSTRUCTION_FACING_HANDOFF_2026-09-12.md. Full catalog continues with Salvage Drone Bay; no export.


## Construction Drone Bay missing south companion - September 12, 2026

Overhead fabrication bank installed q3; original drone/hatch/bench retained at original sizes and relocated north. Native docked/deployed review,176 routes and drone lifecycle pass; other rotations unchanged. See CONSTRUCTION_FACING_HANDOFF_2026-09-12.md. Other directions and full catalog pending; no export.


## Cryo Chamber four directions reviewed - September 12, 2026

Side terminal/vessel access corrected with sample counts retained; north reviewed and retained. Native/card review confirms all prop bounds unchanged and north/south RGB identity.176 routes and47 card bindings pass. See CRYO_FACING_HANDOFF_2026-09-12.md. Full catalog continues with Construction Drone Bay; no export.


## Cryo Chamber missing south companion - September 12, 2026

Overhead machinery installed q3; two pods and compressor retained at original sizes and relocated north, automatic duplicate console suppressed. Other rotations unchanged. Native/state/cache comparison,176 routes and recovery suite pass. See CRYO_FACING_HANDOFF_2026-09-12.md. Other directions and full catalog pending; no export.


## Med Center four directions reviewed - September 12, 2026

North/side cartridge access, case hinges/catches, keyboards and idle screens corrected. Native/card review confirms unchanged prop bounds and identical south view.176 routes,20 existing side variants and47 card bindings pass. See MED_CENTER_FACING_HANDOFF_2026-09-12.md. Full catalog continues with Cryo Chamber; no export.


## Med Center missing south companion - September 12, 2026

New overhead diagnostic bank installed q3. Treatment/imaging/supplies retained at original sizes and relocated north; other rotations unchanged. Native review,176 routes and two localized operating checks pass. See MED_CENTER_FACING_HANDOFF_2026-09-12.md. Other directions and full catalog remain pending; no export.


## Med Office four directions reviewed - September 12, 2026

Side document/storage cues corrected and card refreshed. Native q0/q2 show unchanged prop bounds; north/south renders unchanged.176 routes,20 side variants and47 card bindings pass. All four Med Office directions reviewed; owner acceptance and full catalog remain pending. See MED_OFFICE_FACING_HANDOFF_2026-09-12.md. No export.


## Med Office north correction - September 12, 2026

Bottom spacebar, outward clipboard clip and idle consultation symbol corrected. Native comparison confirms all prop bounds unchanged and other rotations RGB-identical;176 routes pass. North/south reviewed, side document/storage cues pending. See MED_OFFICE_FACING_HANDOFF_2026-09-12.md. No export.


## Med Office missing south companion - September 12, 2026

Overhead records bank installed q3. Exam, consultation and records stations retained at original sizes and relocated north; other rotations unchanged. Native review,176 routes and localized exam monitor state checks pass. See MED_OFFICE_FACING_HANDOFF_2026-09-12.md. Full catalog remains pending; no export.


## Room-facing ledger audit - September 12, 2026

Added read-only consistency audit and corrected12 ledger links/references.113 registered PNG sources pass signature/hash checks.40 directions lack recorded registrations and150 lack direct evidence links; these are ledger gaps, not missing-art or completion totals. See ROOM_FACING_COVERAGE_AUDIT_2026-09-12.md. Full visual catalog goal remains active.


## Biodome missing south companion - September 12, 2026

New overhead habitat bank installed q3; separate tree/aquatic units retained at original sizes and moved north. Other rotations unchanged. Native review,176 routes and two localized state checks pass. See BIODOME_FACING_HANDOFF_2026-09-12.md. Full catalog pending; no export.


## Holographic remaining directions reviewed - September 12, 2026

Dim north/side optics installed and north seated into riser. Calibrator preserved after auto-placement correction. All footprints unchanged; native/card and six state checks pass, plus176 routes. See HOLO_FACING_HANDOFF_2026-09-12.md. Full catalog pending; no export.


## Command side materials reviewed - September 12, 2026

East/west art revised to subdued bronze/red; inward controls and all equipment/bounds preserved. Native and four display-local state checks pass, as do176 routes. All Command directions now reviewed. See STORAGE_COMMAND_FACING_HANDOFF_2026-09-12.md. Full catalog pending; source only.


## Command north material and fit - September 12, 2026

Matte north art seated into riser; native/card and localized display motion verified. All collision rectangles and other rotations unchanged.176 routes/47 bindings pass. See STORAGE_COMMAND_FACING_HANDOFF_2026-09-12.md. East/west material pass remains pending; no export.


## Data Archive remaining directions reviewed - September 12, 2026

North art seated into riser; side sources reviewed and retained. All collision rectangles, independent equipment and other rotations unchanged. Card refreshed;176 routes/47 bindings pass. See ARCHIVE_FACING_HANDOFF_2026-09-12.md. Full catalog pending; source only.


## Storage remaining directions reviewed - September 12, 2026

North art seated into riser; sides reviewed and retained. Lift/crates, collision rectangles and other rotations unchanged. Card refreshed;176 routes/47 bindings pass. See STORAGE_COMMAND_FACING_HANDOFF_2026-09-12.md. Full catalog pending; no export.


## Life Support remaining directions reviewed - September 12, 2026

North art seated into riser; east/west source art retained after review. All collision rectangles and other rotations unchanged. Card refreshed;176 routes/47 bindings pass. See LIFE_SUPPORT_FACING_HANDOFF_2026-09-12.md. Full catalog pending; source only.


## Hydroponics remaining directions reviewed - September 12, 2026

North art now meets riser; east/west reviewed and retained. All collision rectangles and other rotations unchanged. Card refreshed;176 routes/47 bindings pass. See HYDROPONICS_FACING_HANDOFF_2026-09-12.md. Full catalog pending; source only.


## Battery remaining directions reviewed - September 12, 2026

North banks now overlap riser slightly; east/west existing art reviewed and retained. All collision rectangles and other rotations unchanged. Native review,176 routes and47 card bindings pass; card refreshed. See BATTERY_FACING_HANDOFF_2026-09-12.md. Full catalog pending; no export.


## Ore Refinery missing south companion - September 12, 2026

New overhead south bank installed in q3. Independent crusher/hopper retained and moved north; other rotations unchanged. Native review,176 routes/188 layout keys pass. See REFINERY_FACING_HANDOFF_2026-09-12.md. Source only; full catalog remains pending.


## Holographic Core south bank - September 12, 2026

Inward keyboard/handles and subdued idle optics installed. Native review preserves equipment and bounds; only q2 bank pixels change. 176 routes and localized projector/calibrator state checks pass. See HOLO_FACING_HANDOFF_2026-09-12.md. Full catalog pending; no export.


## Storage and Command south banks - September 12, 2026

Storage existing overhead art reviewed and retained. Command controls corrected inward with subdued materials; only q2 bank pixels change. Native review, 176 routes and display-local powered checks pass. See STORAGE_COMMAND_FACING_HANDOFF_2026-09-12.md. Source only; full catalog pending.


## Data Archive south service - September 12, 2026

Keyboard spacebar now inward; outward reader lever corrected. Native review preserves all equipment/bounds and other rotations. 176 routes/20 existing variants pass. See ARCHIVE_FACING_HANDOFF_2026-09-12.md. Source only; full catalog pending.


## Battery Array south service - September 12, 2026

Overhead battery/distribution banks now face inward. Native comparison preserves all equipment and bounds; other rotations unchanged. 176 routes and 20 existing variants pass. See BATTERY_FACING_HANDOFF_2026-09-12.md. Source only; full catalog remains pending.


## Life Support south service access - September 12, 2026

Three overhead filter lids and fan tabs face inward. Native review and176 routes
pass; only south-bank pixels change. Existing equipment, bounds, other rotations
and card unchanged. See LIFE_SUPPORT_FACING_HANDOFF_2026-09-12.md. No export.


## Hydroponics south service access - September 12, 2026

South nutrient-canister caps now face inward. Native review and176 routes pass;
only south-bank pixels change, inventory/bounds/other rotations unchanged. Split
coverage inventory corrected:21 directions already had assets, still awaiting
review. See HYDROPONICS_FACING_HANDOFF_2026-09-12.md. No export.


## BRINE Core south memory service - September 12, 2026

New overhead service bench avoids rotated architect pod. Core/corners unchanged.
Native occupied-pod review, architect recovery,176 routes and47 card bindings pass.
Card refreshed; existing corners added to coverage inventory. See
BRINE_CORE_FACING_HANDOFF_2026-09-12.md. Source checkout only.


## Reactor coolant service station - September 12, 2026

New overhead south service station installed on the clear half-wall in each
rotation. Existing machinery unchanged. Native review and176 routes/188 layout
keys pass; card refreshed. See REACTOR_FACING_HANDOFF_2026-09-12.md. No export.


## Gravity Loom calibration banks - September 12, 2026

New paired south stations flank the doorway with a120-unit gap. Native review
and176 routes pass; central loom unchanged in all four views. Card refreshed.
Also aligned two stale Airlock references with its furnished card;47 card bindings
now pass. See GRAVITY_FACING_HANDOFF_2026-09-12.md. Source checkout, no export.


## Listening Post south console - September 12, 2026

Overhead console installed with inward keyboard and matte pipework. Native sweep
alignment and off/two-time captures verified. 176 routes/20 variants pass; only
bank changes, other props/rotations/card unchanged. See LISTENING_FACING_HANDOFF_2026-09-12.md.


## Emergency Isolation south bank - September 12, 2026

Overhead closed empty chamber with inward supply access installed. Native review
and comparison show only bank changes; inventory and other rotations preserved.
176 routes/20 variants pass. See ISOLATION_FACING_HANDOFF_2026-09-12.md. No export.


## Mycelium Nursery south bank - September 12, 2026

Overhead four-tray bank installed flush south with inward service tabs. Final
inventory matches baseline; only bank pixels change. 176 routes/20 variants/188
layout keys pass. New compare_room_art.py catches inventory and placement changes.
See MYCELIUM_FACING_HANDOFF_2026-09-12.md. Card unchanged, no export.


## Bill and Airlock playable build - September 12, 2026

[Release handoff](BILL_AIRLOCK_RELEASE_2026-09-12.md): builds/BrineSpace-bill-airlock-20260912 contains brinespace-4aae058895cf7c27. Complete Bill journey reviewed; chamber floor no longer hides crew. Native visibility, airlock/expedition, packed-asset and actual-release New Game/F8 checks pass. Selected runtime sources frozen alongside current room/system work. Owner playtest next; no publication.

## Radio Lab south bank - September 12, 2026

New overhead bench selected in q2 with inward controls, clipboard and headset.
Separate listener/transducers/receiver preserved. Native review, 176 routes and
20 variants pass; both signal effects verified OFF and at two powered timestamps.
Other rotations RGB-identical, card unchanged. See RADIO_FACING_HANDOFF_2026-09-12.md.


## Anomaly Lab south bank - September 12, 2026

Overhead containment bank installed flush south with inward microscope. Separate
specimen platform preserved after automatic layout initially omitted it. Native
review and inventory comparison pass; 176 routes/20 variants pass. Other rotations
RGB-identical, q0 card unchanged. See ANOMALY_FACING_HANDOFF_2026-09-12.md.


## Xeno Lab south bank - September 12, 2026

New overhead containment bank installed q2 with inward catches and forceps grip.
Native reviewed;176 routes/20 side variants pass. Other rotations RGB-identical,
q0 card unchanged. Source and prompts in assets/xeno-directional-v1. No export.

## Diving Airlock furnished - September 12, 2026

[Airlock handoff](AIRLOCK_FURNISHING_2026-09-12.md): restored live lockers, compressor and changing bench; added reserve-air/hose rack, equipment-check bench and six wall fittings. All four native room views inspected, active card refreshed. Three-crew/four-rotation airlock checks pass with 1,039 travel samples. Ordinary dressing remains paused elsewhere. Source checkout only; no executable rebuilt.

## Research Lab south bank - September 12, 2026

New overhead research bank has inward eyepieces, visible screen and inward lid
latches. q2 now selects it instead of east-bank library art; scanner moved clear.
Native q2 reviewed,176 routes/20 side variants pass; other rotations RGB-identical.
q0 card unchanged. Evidence: output/research-directional-2026-09-12/verified/.

## Airlock south storage source - September 12, 2026

New overhead two-kit storage bank registered in library. Live trial passed general
routes but failed the Airlock-specific east-facing helmet handoff. Live placement
restored; source retained for service-anchor and removable-helmet follow-up.
Do not treat output/airlock-directional-2026-09-12/after as an adopted layout.

## Cold Store operating cue restored - September 12, 2026

State audit found the side-bank library path skipped its refrigeration pulse.
Explicit custom drawing restores it. Native OFF/two powered captures differ only
at the indicator; offline card is RGB-identical. Evidence in
output/cold-store-state-2026-09-12/. No layout, card or source-art changes.

## Heat Recovery and turbine state verification - September 12, 2026

New matte overhead Heat Recovery skid integrated in its lower work area, preserving
all four door approaches. Card refreshed; 176 routes pass. Turbine temporal audit
found shared library rendering bypassed machine effects; explicit custom draw
flag restores them. Off/two powered timestamps now differ within the machine in
all four views. Evidence in output/turbine-directional-2026-09-12/states-verified/.

## Fire systems playable build - September 12, 2026

[Release handoff](FIRE_RELEASE_2026-09-12.md): builds/BrineSpace-fire-20260912
contains brinespace-f04642316baa2ca3. Packed assets and actual release smoke
checks pass; native captures reviewed. Frozen current art and fire changes.
Owner playtest pending; existing builds preserved; no publication.

## Turbine follows arrow wall - owner correction, September 12, 2026

Current Turbine now mounts north/east/south/west with its arrow, using new side
companions and overhead south art. Console clears machinery; arrow remains visible.
All four native placements reviewed and alignment-checked; 176 routes pass.
This supersedes the sealed-south-only rule below. No export.

## Current Turbine south skid - September 12, 2026

Overhead inward-facing turbine skid installed against sealed south walls in q0/q2.
q1/q3 remain RGB-identical. Rotor cue now fits visible intake; refreshed card and
native review recorded. 176 routes pass. Other sources pending. See
assets/turbine-directional-v1/README.md. No export.

## Sprinkler feedback - September 12, 2026

Two nozzle spray fans and room-level SPRAYING / NO WATER / NO POWER feedback
are integrated. Shared inspector status, native captures and pause checks pass.
Controlled suppression takes 1.6-12.9s depending on fire intensity. See
[report](SPRINKLER_FEEDBACK_2026-09-12.md). No executable rebuilt.

## Observation owner wall replacement - September 12, 2026

Owner requested the north installation at the wall top, replacing the separate
riser. Observation now supplies its own upper wall art at y=-258; generic riser
face/cap/returns are omitted for this room. Side banks connect from y=-104 to170.
Native preview/card reviewed; 176 routes pass. This supersedes the slight-overlap
placement below. Evidence: output/observation-directional-2026-09-12/owner-wall-replacement/.

## Observation Room side banks - September 12, 2026

New inward-facing matte side bookcases and flush north porthole-bank placement
are integrated, preserving the desk and chair. Native q0 and refreshed card
reviewed; 176 route cases pass. South source remains pending. See
assets/observation-directional-v1/README.md. No export.

## Electrical pacing check - September 12, 2026

Controlled native repair took 6.2s travel plus 8s work; checks passed. Separate
six-cycle opening probe charged actual build costs with failures enabled.
No balance change: natural fault timing in a longer expedition remains untested.
See [electrical report](ELECTRICAL_FAULTS_2026-09-12.md). No executable rebuilt.

## Salvage Workshop directional companions - September 12, 2026

North bench now overlaps the riser slightly; new overhead southwest tote and
refreshed card are installed. South bench source is registered as a library option,
with host fit pending because the default room has a south doorway. Native q0 and
176 route cases pass. See assets/salvage-directional-v1/README.md. No export.

## Electrical warning and repair - September 12, 2026

[Electrical faults](ELECTRICAL_FAULTS_2026-09-12.md) now warn with sparks at 75%
heat. Suspension isolates machinery for eight seconds of reachable crew repair.
Partial work survives Save/Continue; restart remains manual. Focused native,
headless, save and hull-repair checks pass. No executable rebuilt.

## Bill complete local art replacement - September 12, 2026

Additional [equipment polish](BILL_POLISH_2026-09-12.md): corrected oversized tread helmets in all four directions and their swim start/stop endpoints (32 equipped frames). All bare frames remain identical. Source validation, complete-pack checks and native rendering pass. Source checkout only; no new executable.

[Final handoff](BILL_FULL_REPLACEMENT_2026-09-12.md): `major-bill-v3` replaces all
175 bare states / 1,134 frame references and 168 helmet states / 1,080 references
at twice source density and the same world size. Original detail and V4 repairs
are retained. East/west walks now alternate stance legs, with synchronized helmets
and calibrated directional strides. All source-preservation/coverage checks,
11,773 consumer checks, 240 native walk comparisons, native room playback and the
final all-state render pass succeed. The earlier trial-only status below is superseded.

Maintained/installed pipeline skills, rebuild/validation tools and the visual bible
are updated. Complete scope, evidence and the separate Cold Store room-test finding
are in the handoff. No EXE rebuilt.

## Galley inward serving bank � September 12, 2026

New overhead south serving bank and flush north kitchen placement are integrated,
with a refreshed card. Native q0 review and 176 route cases pass. Mug handles,
spoons and urn tap face inward. East/west companions remain pending; full catalog
rollout continues. See assets/galley-directional-v1/README.md. No export.

## Electrical sparks integrated — September 12, 2026

Burning machinery now shows occasional blue-white spark bursts alongside fire.
Native capture reviewed; asset/rule and native gameplay checks pass. See
[FIRE_ART_2026-09-12.md](FIRE_ART_2026-09-12.md). No executable rebuilt.

## Cold Store directional side family — September 12, 2026

[Full rollout](ROOM_FACING_ROLLOUT_2026-09-12.md) now includes a previously custom
room: Cold Store has inward-facing west refrigeration and east storage banks,
flush wall placement and a refreshed card. Fixed-orientation native review and
176 route cases pass; north/south source coverage remains pending. No export.

## Fire art integrated — September 12, 2026

[Fire art handoff](FIRE_ART_2026-09-12.md): 24 transparent frames across flame,
smoke and embers now render in live rooms. Asset checks (37), fire rules (35),
and native gameplay checks (25) pass. Close/fit views and animated preview
reviewed. Owner-reported white fringe corrected in flame v2; native checks
repassed (20260912-022651-native). No executable rebuilt.

## Habitation/biology south banks and Shield installation — September 12, 2026

[Active rollout](ROOM_FACING_ROLLOUT_2026-09-12.md): Crew Hab, Lounge and Biology
overhead south revisions pass native review; nine other orientations unchanged.
Shield's new south bank is installed at q1 with clear door access. Preferred routes
(176) and furniture interactions (72) pass. Catalog reports now include actual
variant selection and visual/ground rectangles. Full-catalog work continues;
owner review pending, no executable rebuilt.

## Complete room-facing rollout active — September 12, 2026

Owner accepted the engineering south batch and requested every other room,
including missing artwork, with ongoing skill/workflow/bible improvements.
[Full rollout](ROOM_FACING_ROLLOUT_2026-09-12.md) tracks all 47 identities and four
directions. Medical and Clone south revisions pass native review and routes;
Shield has a new registered south source with host placement still in progress.
The remaining catalog is explicitly pending; no executable rebuilt.

## Three more overhead south banks — September 12, 2026

Owner accepted the Tidal pilot. [Next batch](ROOM_FACING_BATCH_2026-09-12.md)
integrates Pressure Control, Thermal Power Control and Maintenance Bay top-down
south artwork. Native review complete; nine other rotations pixel-identical,
176 crew-route cases pass. Maintenance retains its original placement envelope
to preserve furnishing fallback. New batch awaits owner review; source only.

## First playable fire system — September 12, 2026

[Implementation and tuning](FIRE_SYSTEM_2026-09-12.md): machinery heat warns before local ignition; fires halt room production, grow and damage the hull. Armed sprinklers now perform real suppression using emergency power and stored Water, while 25% flooding extinguishes fire. Crew and companions evacuate through accessible doors and refuse burning destinations. The inspector and a clickable HUD alert expose the hazard. Intensity, heat and purchased sprinkler time persist through Save/Continue; pause freezes simulation and flame animation. Focused headless/native checks and affected flooding, repair, construction, save and hardware regressions pass; owner pacing acceptance remains pending. Source only; no executable rebuilt.

## Wall-art camera clarification and Tidal pilot — September 12, 2026

Owner direction: side banks may sit flush with every appliance facing inward;
north banks are flush and slightly overlap the riser when overheight; south banks
face inward but are viewed top-down. The visual bible and room workflow now record
this contract. [Tidal pilot](ROOM_FACING_REPAIR_2026-09-12.md) installs a top-down
south bank; earlier rear-elevation studies remain unselected. Native review and
176 preferred-layout route cases pass. Owner accepted this pilot; remaining room
revisions continue in the batch above. No executable rebuilt.

## Existing sprite repair trial — September 12, 2026

Owner rejected the simplified V2 treatment as muddy and less detailed, and approved
a density-only experiment using Bill's original higher-resolution sheets.
[Density rebake](BILL_DENSITY_REBAKE_2026-09-12.md): all 17 states / 102 frames rebuilt
at 148px standing height on 184x184 canvases, retaining the exact shipped 64-colour
palette, poses and timing. Baseline extraction reproduces all shipped frames;
manifest, source-preservation and standing-height checks pass. A native Godot
fixture loads all dense frames and captures both packs at the same world size.
Agent review finds substantially clearer face/equipment detail at close zoom.
Owner acceptance and full gameplay/equipment integration remain pending; production
art and bindings are unchanged. Earlier animation and rejected material previews
are recorded in the [local repair handoff](LOCAL_SPRITE_REPAIR_2026-09-12.md).
Continuation V4 repairs 49 frames across four idles, five walk head bands, and the
east-facing interaction, retaining dense detail and the original palette. Idle
height variation becomes 1px and interaction legs stay planted. Source/pixel checks,
manifest validation, and 102 native timed frame selections pass. Runs and the
kneel/repair/stand chain remain unchanged. The underlying side-view stride is still
unresolved; comparisons await owner motion review. See the density handoff for files.

## Character art pipeline established — September 12, 2026

[Pipeline](CHARACTER_ART_PIPELINE_2026-09-12.md): the crew do not match the rooms because of drawing language, not resolution — the rooms are drawn for the pixel grid, the crew are painted illustrations shrunk to 65px. Ruled out along the way: the cleanup path (re-cutting from source reproduces what ships), canvas size (Bill is ~73px inside both the 92px and 128px canvases; `grid_canvas.gd` calibrates on a ~74px figure), and resolution generally (at the owner's saved fit zoom the character is ~29px tall and every version looks alike). The working pipeline is hybrid: **GPT Image 2.5 for the look** in the rooms' language, **PixelLab for rotations and motion**, and the existing local bake for alpha, palette and pivot. PixelLab's `animate-with-text-v3` animated the approved Bill with real stride, foot lift and arm swing while preserving his face, patches, belt and boots, at one subscription generation. Known defects: one frame needed inpainting, the loop does not close cleanly, and PixelLab's own rotations came out narrow in profile. Owner acceptance of the new look given for the test art only; conversion scope (501 manifests, 1,495 states, 7,272 frames) is still an open decision in the [art-direction proposal](CHARACTER_ART_DIRECTION_PROPOSAL_2026-09-12.md).

## Higgsfield pilot — September 12, 2026

[Pilot verdict](HIGGSFIELD_PILOT_2026-09-12.md): eight generations, 28 credits, no source-tree writes and no registrations. **GPT Image 2.5 beats Nano Banana Pro on this project's art contract** — Nano Banana Pro produced flat front elevations twice, including with an accepted asset as reference, while GPT Image 2.5 matched the shallow overhead geometry, detail density and material discipline, and returned native transparent alpha. What made it work: passing an accepted asset as an image reference, naming the geometry explicitly ("not a flat elevation"), and self-referencing for controlled revisions — which lifted the engineering bank from 101 to 120 units tall at 324 wide, against 123 for the accepted bench. Outstanding gaps: alpha is always soft and needs a binary threshold, invented iconography slips through, interior depth is shallower than the authored art, and available aspect ratios do not match authored side regions. A side-wall finding became its own [proposal](MIRRORED_SIDE_WALLS_PROPOSAL_2026-09-12.md): author one side and mirror it, since separately authored sides drift (accepted strips are 303x974 and 279x979). Owner acceptance not given; nothing adopted.

## Rebuilt release live on itch — September 12, 2026

`builds/BrineSpace-2026-09-12-main/` exported from a clean tree at `68c6cc4e` and uploaded as version `2026-09-12-main` (build `1970435`), replacing the September 11 slim build on the same `windows` channel so the existing download updates. Same 1.24 GiB package; butler sent a 794 KiB patch. Validation before upload: pack audit `checked=7780 missing=0 changed=0`, release smoke fixture `0 failures; debug=false` with no resource-loading errors, and a PCK scan confirming the owner-reference photo is not packed (its filename appears only inside a provenance JSON). Note for future rebuilds: the Windows export templates under `output/production-ten/export-tools/` had to be re-extracted from the verified `.tpz` bundle — the presets depend on files inside `output/`, which cleanup passes target.

## Workflow hardening and shared placement envelope — September 11, 2026

[Workflow handoff](WORKFLOW_HARDENING_2026-09-11.md): Track 4 completed — Codex skill copies resynced with an end-of-line-tolerant `check_source_sync.py`, character bindings extended 4 → 16 with an `installed-portraits.json` cross-check, a new art-free layout-key guard (`tests/test_layout_keys.py`) in CI, and a `push_warning` replacing the silent out-of-envelope prop reset. Studio and the live game now share one placement envelope (`RoomLayoutStore.envelope_for()` / `door_lane()`), with the live values as the truth: across 47 rooms × 4 rotations 30 placements change status, 29 of them Studio relaxing to match the game, and only constrained layouts are affected (0 of 188 authored, 1 owner layout). Three long-failing native tests were traced to owner decisions rather than regressions — dressing and common decorations stay in Studio, free placement is the Studio default, wall decorations are paused — and one real flake (`test_run_save`, a fixed wait after the Continue scene swap) was fixed and re-verified under load. Headless 112 PASS / 0 FAIL; native layout lane 7 PASS. Source and tests only; no executable rebuilt. A follow-up claim that the `battery_array/1` cells section is reset in game was withdrawn on September 12: that placement is owner-authored in free placement, where the guard does not run, and a probe confirms it survives untouched.

## Release size cut — September 11, 2026

Shipped pack 5.81 GB → 1.19 GB with no tracked file removed: raster import roles (normal / keep / skip, see [release workflow](RELEASE_WORKFLOW.md)) stop `.ctex` duplicates and unshipped sources from packing, and two manifest-crawler fixes (`swim_helmet_fit.gd` tree literal, `addons/` prefix test) drop ~1.3 GB of QA captures that were shipping to players. Manifest 11,273 → 8,108 files; empty-directory pack audit `missing=0 changed=0 remapped=8`; release smoke (title → New Game → Continue → Resume → F8) 0 failures on warm runs — the first cold launch after export raced the fixture's fixed frame counts on the two post-Continue timing checks, a fixture-hardening note rather than a game fault. Build: `builds/BrineSpace-2026-09-11-slim/`. Local `.import` sidecars rewritten (gitignored); `.godot/imported` still holds ~30k stale `.ctex` safe to clear.

## Performance pass phases 1+2 — September 11, 2026

[Performance handoff](PERFORMANCE_PASS_2026-09-11.md): phase 1 (retained environment passes, layout-store memoization, door/surface key memos, idempotent hardware panel, flooded quick wins) plus phase 2 (sorted prop-queue caching with pre-expanded stable entries; cheap identity+serial DrawSlot keys replacing per-slot deep dictionary compares). Measured on the same build via opt-out flags: **100-room fit 74.8→61.4 ms (−17.9%)**, 50-room fit −21%, save hitch −43%. All native parity gates pass — content-cache parity's 33 capture pairs verified pixel-identical with a comparator (the GD test alone does not compare pixels) — plus the new environment parity harness and the headless battery (176 preferred orientations, 47 cards, companion water). Five parity fixtures' 7-second thaws corrected to the 10-second pod duration. Dense fit still misses the 60 fps budget; the remaining headroom (render_into internals, painting, GPU) and the owner-decision options (mipmaps, atlasing) are recorded in the handoff, as is a pre-existing sub-perceptual fit-zoom capture variance in two old pixel comparators, reproduced on the unmodified code path. Source only; no executable rebuilt, no commit.

## Bug-fix session — September 10, 2026

[Bug-fix handoff](BUGFIX_SESSION_2026-09-10.md): companion water-mode hysteresis (personality starvation fix) with powerdown-exit wake, flood alerts no longer re-announce on Continue, flood-retreat re-validates its refuge mid-route, correct journal pet-refusal reasons, crew rest restored at crew hab/lounge rotation 2, rotated-door navigation walls corrected in the shared embedded-view path, MetaState fixture isolation (test_marsh_unlock now green), Josh swim-clearance guard, settings-panel crash guard, and test_bill_npc modernized to the post-thaw spawn model. Thirteen affected tests pass, including 176-orientation preferred layouts and 47 card bindings. Source only; owner behavior review pending; no executable rebuilt, no commit.

## Starting-screen facial likeness - September 9, 2026

[Title likeness handoff](TITLE_LIKENESS_2026-09-09.md): BRINE's starting-screen face revised toward the owner's supplied cover reference, preserving the body, stage and floating silhouette. Native 1600/960 layout, float and Reduced Motion checks passed; agent visual review complete. Source only; executable and itch.io build retain the prior title until the next release.

## Butler upload workflow saved - September 9, 2026

Future owner-requested Windows uploads should use the [saved Butler procedure](ITCH_UPLOAD_WORKFLOW.md). Reuse brinshadewater/brinespace:windows. First verified version: 2026-09-09-face-icon, build 1963891. Page remained Restricted; no new gameplay validation implied.

## BRINE face executable icon - September 9, 2026

[Icon handoff](APP_ICON_2026-09-09.md): current BRINE portrait assigned to the project and Windows executable. Embedded icons reviewed at native sizes; release title launch passes. Updated playable folder: builds/BrineSpace-2026-09-09-face-icon/. Gameplay unchanged from the polished build.

## Combined polish and release - September 9, 2026

[Combined handoff](FINAL_POLISH_RELEASE_2026-09-09.md): completed local art, animations and reliability work integrated; sprite failure handling, clip duration calculation and title/badge loading polished. Focused source/native checks and actual release New Game/Resume/F8 pass; 10,978 packaged assets checked with zero missing/changed. Source pushed to GitHub. Playable build: builds/BrineSpace-2026-09-09-polished/. See the handoff for package identity and remaining performance/pacing limits.

## UI, character and build session closed - September 9

[Closeout](SESSION_CLOSEOUT_UI_CHARACTERS_2026-09-09.md): accepted portrait/sidebar decisions added to the bible; character/room skill lessons and installed copies updated; [release workflow](RELEASE_WORKFLOW.md) now distinguishes editor/PCK evidence from actual release gameplay. This session has no remaining active work. Later optimized-release, animation, portrait and room entries below retain their own scope and acceptance. No new build or source-art cleanup during closeout.

## Art session closed - September 9, 2026

[Closeout](ART_SESSION_CLOSEOUT_2026-09-09.md): selected room/title assets and current dependency integration checked, runtime manifest refreshed to 11,273 files, assets and supporting work staged with verified LFS pointers. Bible and maintained/installed room-pipeline lessons updated. Current 47 card bindings pass and newer riser/animation selections are preserved. Source session closed; generated build metadata stays local, and no executable, commit or push was made by this closeout.

## Reliability session closed — September 9, 2026

[Closeout](SESSION_CLOSEOUT_RELIABILITY_2026-09-09.md) consolidates the merged teegly
fixes, local reliability/performance work and maintained pipeline lessons. The
optimized executable uses frozen bindings; newer companion water, animation and
room-art source milestones below are not jointly accepted in that build. Follow
[release delivery](RELEASE_ASSET_CONTRACT.md) for the next combined build.

## September 9 character session closed

[Character closeout](CHARACTER_SESSION_CLOSEOUT_2026-09-09.md): all completed portrait and animation selections are bound to the source game. The active registry audits nine packs (355 clips / 1,488 frame references including retained states) and eight portraits with zero errors. Visual bible, character skill/installed mirror and asset pipeline guide updated with observed lessons. Recent native water, dry action, repair and save checks remain passing. Session complete; no executable rebuild or commit/push.


## September 9 companion water behavior

[Companion water](COMPANION_WATER_2026-09-09.md): Margot swims from 20% room flooding, River floats from 25%, and Josh shuts down at 50% until water recedes. Four-direction water motion, surface rendering, route restrictions, pause and checkpoint handling are installed. Native flooded-room rescue/routing/save tests and dry-action/repair regressions pass. [Animation gallery](../character/companion-water-v1/review.html). Source only; no executable rebuilt.

## Riser session closed — September 9, 2026

Six new walls remain assigned to reactor, cryo chamber, data archive, storage bay, crew lounge and research lab, now with coordinated door finishes. Separate wall decorations are suppressed in gameplay and Studio, including the airlock; source fittings and saved placements are retained. Seven cards refreshed. [Final review](../assets/riser-session-closeout/review.html) and [handoff](RISER_SESSION_CLOSEOUT_2026-09-09.md). Native 28-rotation captures and focused wall/door checks passed; source checkout only, no executable rebuilt.


## September 9 reliability, smaller release and rendering

[Implementation and acceptance](RELIABILITY_PERFORMANCE_2026-09-09.md): safe image fallbacks, exact release IDs and live diagnostic snapshots; 30% smaller data pack; 98-room frame time improves 30.5% fitted and 60.1% close. Native geometry/pixel parity, failure/report checks, 10,300 packed assets and actual release New Game/F8 pass. Build: `builds/BrineSpace-2026-09-09-optimized/`; stable animation bindings used while concurrent animation work continues.

## Room risers V3 — September 9, 2026

Added six window-free risers for reactor, cryo chamber, data archive, storage bay, crew lounge and research lab; catalog overrides and refreshed card bindings installed. Owner direction: future windows are separate wall props. Keep mounting panels and the central door reserve clear. [Review gallery](../assets/room-risers-v3/review.html) includes toggleable guides; [placement notes](../assets/room-risers-v3/WINDOW_PLACEMENT.md) record source/world bounds. Native checks and 24 captures passed; 47 card identities passed. Future prop fit/occlusion needs validation when props are added. No executable rebuilt. See ROOM_RISERS_V3_2026-09-09.md.


## September 9 character animation expansion

[Animation expansion](ANIMATION_EXPANSION_2026-09-09.md): Marsh now has dedicated sitting/reading/resting/cargo and distinct swim/tread poses; Margot has directional sit/groom/nap plus stretch/yawn; River and Josh have start/stop/turn transitions, startup and standby. Installed v5 packs preserve prior sources. Asset, checkpoint/pause, real-station companion and repair tests pass; native captures reviewed. [Animated gallery](../character/animation-expansion-v5/review.html). Source checkout only; no executable rebuilt.

## September 9 room-specific riser walls

[Room risers](ROOM_RISERS_2026-09-09.md): six installed wall strips for medical, hydroponics, maintenance, galley, command and observation with baked fittings, static windows and reserved central entries. All 24 native rotations reviewed; adjacency, Studio and card-binding checks pass. Six cards refreshed. Source only; no executable rebuild.

## September 9 floor variants V5

[Six further finishes](FLOOR_VARIANTS_V5_2026-09-09.md) for reactor, cryo, robotics, refinery, command and observation add 96 tile slots to Studio. Sources and six furnished captures reviewed; native texture/rotation and selection/undo/redo checks pass. Two rejected robotics candidates preserved separately. Existing defaults retained; no executable rebuilt.

## September 9 common prop and floor-wire removal

[Room declutter](ROOM_DECLUTTER_2026-09-09.md): live rooms suppress common props/accessories, floor wiring/conduit and decorative overlays; the layout editor retains the assets and saved placements. Specialist equipment positions and sizes are preserved. Native 47-room/four-rotation checks pass; 44 furnished cards refreshed and all 47 card bindings pass. [Gallery](room-declutter-2026-09-09/review.html). Source checkout only; no executable rebuild.

## September 9 Josh tread and blowtorch pass

[Josh torch](JOSH_TORCH_2026-09-09.md): installed neutral charcoal tracked base across Josh movement/actions, plus four-direction torch deploy/weld/stow. Josh assists nearby paid crew hull repairs at +25% progress only while actively welding; costs and job ownership remain with crew. Focused repair, real-station routing/checkpoint/interruption and native sprite tests pass. Review gallery saved; no executable rebuild.

## September 9 Teegly release fix and bug reports

[PR integration](TEEGLY_PR_INTEGRATION_2026-09-09.md): integrates release-safe image loading and F8/unclean-session diagnostic bundles, with newer-loader coverage, pause support, safer report writes and a CI assertion guard. Fixed local Windows release is in `builds/BrineSpace-2026-09-09-fixed/`; detailed verification and limits are recorded in the handoff.

## September 9 expanded floor variety

[Floor variety](FLOOR_VARIETY_2026-09-09.md): six more selectable finishes for medical, hydroponics, cargo, data, galley and lounge; 96 additional tile slots. Sources and six furnished native captures reviewed; texture/rotation and selection/undo/redo checks pass. Existing room defaults retained. No executable rebuild.

## September 9 room materials and headphone scale

[Room art consistency](ROOM_ART_CONSISTENCY_2026-09-09.md): 16 selected matte source repaints across six room families, smaller radio headsets, and refreshed cards. Owner layouts and the restored BRINE room remain intact. All 47 rooms reviewed in four native rotations; final layout, source, dressing and card checks pass. [Before/after gallery](room-art-consistency-2026-09-09/review.html). Source checkout only; final headset correction awaits owner feedback.

## September 9 additional floor tiles

[Floor additions](FLOOR_TILE_ADDITIONS_2026-09-09.md): three new 4x4 atlases available in Studio's Floor finish selector. Native furnished review, texture/rotation and selection/undo/redo checks pass. Existing defaults retained; per-room adoption remains open. Source only; no executable rebuild.

## September 9 companion white-cutout repair

[Companion extraction repair](COMPANION_EXTRACTION_FIX_2026-09-09.md): River/Josh/Margot now load companion-cleanup-v3. Preserves interior white panels, removes connected exterior backgrounds, and area-downsamples original sources to reduce speckling. All six manifests, extraction regression and native sprite board pass; full personality run is not green amid concurrent room compile/render errors. Before/after gallery saved; no executable rebuild.

## September 9 sprite scale and animation polish

[Sprite polish](SPRITE_POLISH_2026-09-09.md): installed revised adult-proportion Marsh sprites and dedicated idle, consistent 64-color companion packs, and River/Josh action entry/exit clips. Native sprite and companion personality checks pass. Marsh broader test has peer-count failures reproduced with old art; secondary pose sharing remains. Review gallery and native captures saved; continuous browser review was blocked. Source checkout only, no executable rebuild.

## September 9 latest portraits installed

[Portrait installation](PORTRAITS_INSTALLED_2026-09-09.md): all eight latest portraits now load in the game, including the final suit/lighting pass, distinct station backgrounds, Margot realism V3 and BRINE V14. Native selection/comms reviewed at two sizes; bubble test passes. Room-dressing assertions noted separately. Source checkout only; existing executable not rebuilt.

## September 9 title and terrain fixes

[Fixes and before/after review](ART_FIXES_2026-09-09.md): revised title uses BRINE V13 likeness/rendering with matte slate/ivory surroundings and retained float, monitors and Reduced Motion. Eleven habitat patches now use continuous source fields rather than mirrored repeats. Native title, habitat and focused visual regressions pass. Source only; no executable rebuilt.

## September 9 art consistency audit

[Audit and review board](ART_CONSISTENCY_2026-09-09.md): 47 room families / 188 native orientations reviewed; distinct department palettes and owner layouts retained. Owner-selected pixel-textured V2 portraits installed for all seven architects/companions, with proportional Continue portraits. Native UI checks pass at two sizes. Title illustration style and some mirrored habitat ground repeats remain documented follow-ups. Source only; no executable rebuilt.

## September 9 portrait individuality review

[Portrait review](PORTRAIT_INDIVIDUALITY_2026-09-09.md): seven V3 portraits revise underlying anatomy and materials after owner feedback that V1/V2 looked generic. Margot uses her original photo reference. Version comparison saved; runtime portraits unchanged. Owner likeness and final pixel-texture review remain open.


## September 9 camera shimmer correction

[Camera handoff](CAMERA_SHIMMER_2026-09-09.md): align the entire rendered world to physical screen pixels to reduce nearest-neighbor shimmer during panning at fractional window scales. Logical camera/input coordinates and sharp filtering are preserved. Native 64-case sampling regression and navigation checks pass; source only, owner motion review pending.

## September 9 companion personality

[Personality handoff](COMPANION_PERSONALITY_2026-09-09.md): Margot's sit/groom/nap/pet actions, River's head scans/equipment inspection/quiet chirps, and Josh's head gestures/tread pivots/repair watching. Journal > Crew offers Pet Margot and companion Locate links. Action clocks, cooldowns and pending approaches persist through Continue. Native action and companion regression checks pass; owner animation/pacing review remains open. Local source only, no executable rebuilt.

## September 9 playable Windows build

Windows x64 release is available in builds/BrineSpace-2026-09-09. Quick regression, package startup/assets and release launch checks pass. Includes an export dependency correction and startup zoom-slider signal fix. [Build handoff](WINDOWS_BUILD_2026-09-09.md).

## September 9 character portraits and recap discoveries

Companion selector portraits now match architect portrait dimensions. End-of-loop discoveries include newly unlocked architects and companions, preserved across Continue. [Handoff and checks](CHARACTER_DISCOVERIES_2026-09-09.md).

## September 9 Margot companion

[Margot integration](MARGOT_INTEGRATION_2026-09-09.md): selected frog-hat portrait V2, four-direction cat idle/walk, pet cryopod rescue beside two failed human pods, optional future selection and Save/Continue. Older robot-only loops remain intact. Focused native/headless and affected regression checks pass. Owner gait/pacing review pending; local source only, no executable rebuild.

## September 9 game maintenance pass

[Maintenance handoff](MAINTENANCE_2026-09-09.md): fixed delayed camera centering overriding Fit Station, startup/resize view drift, guide-visible sidebar overflow, and flood warnings consumed during pause. Removed redundant layout lookups during prop drawing with identical flip pixels. Inspector still expands to 520 design pixels when the guide closes. Broad regression and native visual checks are recorded in the handoff; no overall FPS claim or executable rebuild. Existing authored layouts preserved.

## September 9 BRINE layout restored

Owner requested BRINE return to its pre-simplification arrangement. Restored its four authored quarters, original personal BRINE entry and matching card, including the lower workstations, servers and observation pedestal. Other rooms and their saved overrides are unchanged. BRINE is an explicit exception to the 3�4-asset direction. Four native editor/runtime comparisons and card consistency pass; capture reviewed. Evidence: `output/brine-layout-restore/`; no executable rebuilt.

## September 9 uncluttered large-asset correction

[Layout correction](LARGE_ASSET_LAYOUTS_2026-09-09.md) supersedes the denser pass below: 3�4 major assets per furnished room, with already simpler rooms left sparse. Removed 139 prop instances across 97 orientations; 188 native editor/runtime comparisons match. Updated saved removals with original-file backup, verified 176 native kept-prop lists, and refreshed 44 cards. Local changes only; no executable rebuilt.

## September 9 Marsh battery tradeoff

[Android survival and recharge](MARSH_BATTERY_2026-09-09.md): Marsh needs no helmet or Oxygen, including underwater expeditions. Initial battery lasts five minutes; he returns to his original pod at 35%, recharges at 5%/s for 1 Power per 25%, and resumes work. Battery and prepaid charge survive Save/Continue. Native docking, zero-Oxygen expeditions, recall, core/derelict return, human survival and construction checks pass. Owner balance review pending; local source only.

## September 9 preferred room layouts

[Layout handoff](PREFERRED_LAYOUTS_2026-09-09.md): adopted the owner�s 49 saved orientations unchanged and extended larger equipment/selective clutter removal to the remaining furnished layouts. All 188 Studio entries covered; 176 furnished orientations pass door-route checks. Gameplay now matches free-placement saves, BRINE corner notches have matching collision, and 44 room cards are refreshed. Native editor/runtime parity, live core/recovery-pod routes, Studio workflow and card checks pass. Personal saves unchanged; owner visual review pending, no executable rebuilt.

## September 9 River and Josh companions

[Companion integration](COMPANIONS_HANDOFF_2026-09-09.md) adds small green River
and larger blue-lavender Josh with owner-requested treads. Paid derelict recovery,
container opening, powered restart, a separate roster, optional pre-loop selection
and Save/Continue are installed. Both have four-direction idle/rolling packs.
Focused headless/native and affected regression checks pass; [visual review](../character/companions/review.html)
is ready. Owner motion/pacing review and Margot remain pending. Local source only;
no executable rebuilt. Prototype behavior and log limits are recorded in the handoff.

## September 9 Marsh charging chamber

[Charging chamber implementation](MARSH_CHARGING_2026-09-09.md) supersedes Marsh's cryo route in new loops. Reconnect his dedicated derelict and restore power: white fluid pumps through attached tubes for 12 seconds, then Marsh wakes and permanently unlocks. Charge persists through power loss, suspension and Save/Continue. Distinct occupied/empty cradle art and native fluid motion/freeze checks pass, alongside Marsh recovery and legacy/selection regressions. Owner visual review pending; existing loops preserve their original occupants. Local source only.

## September 9 Marsh unlockable architect

[Marsh integration](MARSH_UNLOCK_2026-09-09.md) adds the approved blond android as a fourth recoverable architect in new loops. Recovery permanently unlocks selection; starting cache is +4 Data/+4 Metal. Independent actor, portrait, pod art, sprites, helmet frames, construction and saves are installed. Four-crew recovery/persistence, legacy recovery, picker and four-direction paid-construction checks pass. Old loops retain existing occupants; no executable rebuilt. First-pack animation sharing and owner review limits are recorded in the handoff.

## September 9 building decisions and discoveries

[Decision pass](BUILD_DECISIONS_2026-09-09.md): inspector priorities, visible placement explanations, adaptive construction/supply guidance and three hidden synergies. Discovery suite is clean and native UI assertions pass; screenshot reviewed. Native logs also report missing assets from concurrent Marsh integration, so global native acceptance remains pending. Local source only.

## September 9 maintenance session closed

[Maintenance closeout](MAINTENANCE_SESSION_CLOSEOUT_2026-09-09.md) records export cleanup and the brief north-placement investigation. Owner reported placement working again; no gameplay/layout fix was made. The follow-up portrait/asset integration request was canceled before implementation. Other art and gameplay sessions remain independent.

## September 9 Marsh android concept

Latest revision: [V3](../character/marsh-portrait-v3/README.md) adds owner-requested blond hair, visible steel temple plate and an off-white suit, preserving the human-looking male identity. Saved for owner review; no gameplay integration.

Owner correction: Marsh is male and more humanoid. [V2](../character/marsh-portrait-v2/README.md) now uses human skin, ears, neck and dark hair, with subtle android details. Supersedes V1's visibly mechanical design; owner review pending.

Created [Marsh's portrait concept](../character/marsh-portrait-v1/README.md) in the current crew style: ivory synthetic face, graphite shell, amber eyes and sage shoulder panels. Source, prompt and manifest saved. Owner review and role definition pending; no gameplay integration.

## September 9 matching crew portraits

[Crew portrait handoff](CREW_PORTRAITS_2026-09-09.md) records new Bill, Veld and Branforth close-ups matching BRINE V13, replacing the old concept crops in the shared portrait loader. Comms use the larger portrait size for all speakers. Native all-speaker and picker checks pass at both sizes, with small-size visual review; owner acceptance pending.

## September 9 sidebar readability

[Sidebar handoff](SIDEBAR_READABILITY_2026-09-09.md): Construction/Flood buttons hidden, hardware and time controls compacted, inspector reading area enlarged with clearer font and contrast. Final native navigation and hardware checks pass; screenshot reviewed. Local source only.

## September 9 BRINE reference restart

Owner liked V13. Animated bubbles are now 62.5% smaller, dimmer and thinner at their request. Native comms and bubble mask/clock checks pass; small-size capture reviewed, owner bubble review pending. See portrait handoff for evidence.

Latest follow-up: V13 darkens the face slightly while preserving V12's soft shadows. Installed and native-checked at both sizes; captures saved with V13. Owner review pending.

Follow-up: V12 softens facial shadows and caustic contrast at owner request, retaining V11 identity and framing. Installed and native-checked at both sizes; captures saved with V12. Owner visual review pending.

Owner requested a fresh portrait from a supplied photo reference. [V11 handoff](BRINE_REFERENCE_RESTART_2026-09-09.md) records the new tied-back hair, reference-based face and close composition, installed in the enlarged comms portrait area. Native checks at both sizes and revised bubble masking pass; owner visual acceptance pending. This supersedes V9 selection below.

## September 9 menu, portrait and comms polish

[Polish handoff](MENU_PORTRAIT_POLISH_2026-09-09.md): Continue uses the approved selection portrait, comms is wider, and the in-game menu has five main choices with clearer labels. Four native fixtures pass; menu, dialogue and title preview captures reviewed. Local source only.

## September 9 HUD sizing

[HUD sizing handoff](HUD_SIZE_POLISH_2026-09-09.md): top-right icons enlarged from 44 to 60 design units; time/cycle controls use a compact shared pause/speed row and tighter margins. Native navigation checks pass; both HUD sizes and cycle panel visually reviewed. Local source only.

## September 9 dialogue pause

[Dialogue pause handoff](DIALOGUE_PAUSE_2026-09-09.md): visible conversations pause station time until explicit close, preserving any previous manual pause. Removed timed dialogue dismissal. Native pause/menu/queue checks and headless context/archive checks pass. Local source updated; no new export.

## September 9 larger BRINE comms portrait

BRINE's V9 portrait now fills the comms panel's interior height at 150x150, 56% wider than before, retaining the closer crop. Native comms checks pass at both resolutions; small-screen capture visually reviewed. [Portrait handoff](BRINE_PORTRAIT_STYLE_2026-09-08.md) records captures and pending owner review.

## September 8 readable awakening intro

[Intro handoff](INTRO_CONTINUE_2026-09-08.md): the complete transmission renders before station setup and stays until explicit Continue. Gameplay pauses while reading. Native new/restore, GUI and keyboard acknowledgement, reduced-motion and archive checks pass; screenshots reviewed. Local source updated; no new package.

## September 8 BRINE portrait style pass

[Portrait handoff](BRINE_PORTRAIT_STYLE_2026-09-08.md) records the owner's preference for the previous portrait after V10. V9 is restored with 25% closer runtime framing for readable features; source pixels are unchanged. Bubble masking follows the crop. Native comms at both sizes and crop-aware bubble checks pass; owner review of framing and packaged validation remain pending. Earlier sources retained.

## September 8 second game-wide maintenance round

[Second-pass handoff](GAME_MAINTENANCE_PASS2_2026-09-08.md) records the final-drainage
inspector fix, invalid-checkpoint control rejection, stale-error cleanup, shared source
atlases and reduced renderer/layout work. Twenty-one targeted fixtures pass; all 33
native retained/direct pixel comparisons match. Native shutdown checks are clean;
an Ogg warning remains in the headless economy fixture. The paid two-generator salvage
comparison now buys generation earlier, without changing game costs. Dense frame time
is essentially unchanged at 25.205 ms dry / 34.312 ms flooded. Work is local and
uncommitted; a new package and owner normal-play acceptance remain pending.

## September 8 game-wide maintenance round

[Maintenance handoff](GAME_MAINTENANCE_2026-09-08.md) records checkpoint isolation
fixes, cached door lookups, lighter inspector/badge updates, corrected guide copy and
updated construction fixtures. Twenty-six targeted current-source checks return zero,
with intermittent shutdown warnings in two fixtures documented separately. Native
49-room median frame time improves from 33.943 to 25.221 ms dry and 44.885 to 34.120 ms
flooded; dense views still exceed the 60 fps budget. Native HUD, lighting and wet-door
checks pass. Costs, failures and hidden discovery remain intact. Local work is
uncommitted; new package and owner normal-play acceptance remain pending.

## September 8 obsolete compiled export cleanup

Owner requested disk cleanup. Removed 67 superseded `.pck`/`.exe` files (66.775 GiB): environment-export-v1 through v22, airlock-low-package-v1 through v3, mat-repair-package-20260906-v1/v2, drone-fleet-v2/v3, station-package-v1, and earlier tiled-floor/game-polish/layout-performance/layout-studio playtest binaries. Historical references below to those runnable binaries are now archival; their source snapshots, manifests, captures and test evidence remain.

Retained `output/tiled-floor-complete-20260908/build/` and `output/audio-playtest-20260908/build/` (EXE/PCK checksums matched their recorded manifests), plus the latest export in each numbered series and the integrated-acceptance package. These retained binaries are dated snapshots, not rebuilds of subsequent source changes. Source art, Git data and game saves were not pruned.

## September 8 fitted service art session closeout

[Session handoff](FITTED_SERVICE_SESSION_CLOSEOUT_2026-09-08.md) consolidates this art session, host-fit findings and restart point.29 scoped export records match current files. Skill lessons and visual bible updated; this session is paused at owner request. Other sessions remain separate; work is local and uncommitted.

## September 8 navigation UI session paused

[Session handoff](NAVIGATION_UI_SESSION_CLOSEOUT_2026-09-08.md) records the final
four-button HUD row, selected clean badges, cream Codex, skill/bible updates and
verification limits. Local work saved; owner review and optional alpha exports remain.


## September 8 room material session closeout

[Material session handoff](ART_MATERIAL_SESSION_CLOSEOUT_2026-09-08.md) consolidates Tidal-reference repaints, shared accessories, Bio/Xeno follow-ups and the cryo machinery replacement. Latest Xeno front/side views pass native rotation, card and draft checks with visual review. Full asset matching and owner acceptance remain incomplete. Session paused at the owner's request; reconcile newer architecture work below before resuming. No executable rebuild or commit from this session.

## September 8 crew animation session closeout

[Crew animation closeout](CREW_ANIMATION_SESSION_CLOSEOUT_2026-09-08.md) records completed coverage, runtime checks and pending owner visual review. Character skill, asset-pipeline/workflow reference and visual bible updated with facing, cropping, furniture-depth and checkpoint lessons. Other sessions remain separate; this closeout performs no commit or deployment.

## September 8 wall-asset session paused

[Session handoff](WALL_ASSET_SESSION_CLOSEOUT_2026-09-08.md) consolidates wall families, companion props, material/alpha workflow and seed placement evidence. Production stopped at owner request for now. Remaining directions, crew/service validation and runtime installation are explicitly recorded; other sessions are managed separately.


## September 8 room/corridor art session closeout

[Session closeout](CORRIDOR_ART_SESSION_CLOSEOUT_2026-09-08.md) records corridor/riser direction, live variants, source locations, tests and review limits. The room skill, asset-production notes, layout workflow and visual bible include the reusable lessons. Work remains local and uncommitted. Other sessions are independent; resume from current status and latest owner notes.

## September 8 Studio / BRINE session closed

Owner closed the session with V8 selected. [Closeout](STUDIO_BRINE_SESSION_CLOSEOUT_2026-09-08.md)
records Studio, lighting, portrait direction, source provenance and tested scope.
Portrait pipeline guidance and visual bible updated; no remaining work in this task.

## September 8 water and editor session closeout

[Session handoff](WATER_EDITOR_SESSION_CLOSEOUT_2026-09-08.md) consolidates this session's water/editor changes, validation, remaining performance limits and pending owner review. Room skill, thumbnail production notes, editor workflow and visual bible updated. Work remains local and uncommitted; other sessions are managed separately.

## September 8 opposite-facing corner defaults

New corner selections alternate west/south and east/south defaults, based on placed corners plus queued corner orders. Manual rotation and existing saved rooms remain intact. Automatic hand selection and explicit card selection share the rule. Focused tests pass queued/completed parity and preservation. [Both directions in all three finishes](../output/corner-defaults-v1/index.html). Native art is reused from the validated rotation captures.

## September 8 crew life animations

[All eight crew-life categories](CREW_LIFE_EXPANSION_2026-09-08.md) are integrated for Bill, Veld and Branforth: sitting, meals, sleep, oxygen distress/recovery, pickup, reading/inspection, carrying turns and additional death directions. 258 new runtime clips include fitted helmet counterparts. Native pack, 72 furniture/rotation/actor cases and affected expedition, flooding, swimming, construction and repair checks pass. [Moving review](../output/crew-life-review.html) and [showcase](../output/crew-life-preview.gif); owner visual acceptance pending.

## September 8 layout editor performance and tray polish

[Editor polish](LAYOUT_EDITOR_POLISH_2026-09-08.md) removes raw source-sheet thumbnail backgrounds and solid selection fills, stabilizes tray rows during loading, and uses a finite thumbnail queue. Translation-only drag updates reduce populated-fixture CPU update time from 0.933 to 0.058 ms; total render-inclusive time remains about 6.06 ms. Transparent-preview and fast/full pixel/geometry checks pass. [Tray review](../output/layout-editor/polished-tray.png). Owner acceptance pending.

## September 8 corridor doors and water review

[Corridor floor/door pass](CORRIDOR_DOORS_WATER_2026-09-08.md) adds restrained floor variation and gray metal doors at all default corridor, corner and T entries. Shared connected doors use the same finish. Nine live wet-door variants pass closure and pause checks; all 36 rotated water masks match their footprints, and water physics reports zero failures. [Dry and flooded review](../output/corridor-polish-v3/index.html). Owner acceptance pending.

## September 8 corridor junction and floor polish

[Corridor polish](CORRIDOR_POLISH_2026-09-08.md) removes the 35-unit overextension of inner T/elbow wall returns and gives all nine shape/variant combinations distinct floor arrangements. Transit tread/grating, utility service runs and observation grating retain solid borders and compatible entrance lanes. Native rotations, floor mapping/coverage, routing and card checks pass. [Review and notes](../output/corridor-polish-v2/index.html). Owner acceptance pending.

## September 8 aligned hallway floor runs

The industrial floor now follows the path: solid perimeter strips, matching central grating/pipe lanes, and grated manifold covers at elbows and T branches. Symmetric lane selection keeps flipped corridor sockets compatible. Explicit tile/finish edits are preserved. Native rotations, footprint/UV/finish tests and refreshed cards pass. [Aligned floor review](../output/hallway-floor-aligned-v1/index.html); owner acceptance pending.

## September 8 industrial hallway floor revision

Owner rejected the first floor as too large and plain. The new [industrial deck](HALLWAY_FLOOR_TILES_2026-09-08.md) uses 64 smaller grating, steel-panel and recessed-pipe modules at 24 units wide, half the prior panel width. It is the corridor/corner/T default; the prior quiet finish remains selectable. Native views, footprint/UV/finish checks and refreshed cards pass. [Updated review](../output/hallway-floor-tiles-v2/index.html). Owner acceptance pending.

## September 8 hallway floor tiles

[Hallway tile pass](HALLWAY_FLOOR_TILES_2026-09-08.md) adds a 16-panel matte grey-green atlas as the corridor, corner and T-junction default. Tiles use the existing 48-unit grid and clipped footprints; explicit saved finishes remain. Native previews, full mesh coverage at 12 shape/rotation combinations, current finish selector and 47-card consistency pass. [Floor review and notes](../output/hallway-floor-tiles-v1/index.html). Owner visual acceptance pending.

## September 8 corridor cleanup and north-entry doors

Owner follow-up removes corridor/corner/T floor drains, service pipes, cables, hatches and legacy mounted props. Observation windows are vertically centered within the riser; exposed north-facing port faces use a closed door without windows. Connected faces still cull. [Updated review](../output/corridor-wall-variants-v1/index.html) includes all nine variants and rotations. Native port mapping, raised/low and card checks pass; owner review pending. Scope is the corridor set under review, not furnished-room machinery.

## September 8 unique corridor and corner walls

[Dedicated routing architecture](CORRIDOR_WALL_VARIANTS_2026-09-08.md) adds six original transit, utility and observation designs: separate straight and turning-bay sources, nine combinations across corridors, corners and T-junctions. Low hulls, raised faces and nine cards now use the new art through existing variant selection. Native rotation/raised-low, fitting bounds, connection masks, taper coverage and card consistency checks pass. [Variant gallery and notes](../output/corridor-wall-variants-v1/index.html). Owner visual acceptance pending.

## September 8 layout editor controls

[Editor controls](LAYOUT_CONTROLS_2026-09-08.md) enable free placement by default (explicit saved settings remain), add left-drag camera panning on empty canvas and retain Shift-drag marquee selection. Canvas clicks find floor decorations without manually changing modes. Entryway areas and Clean preview are accessible in the main toolbar. Native workflow, movement/undo, camera, save/reload and recovery checks pass; clean room preview inspected.

## September 8 department riser walls and default visibility

[Department riser pass](RISER_DEPARTMENT_PASS_2026-09-08.md) adds eight distinct matte wall families, retaining the dedicated BRINE and airlock designs. All 47 room types are assigned; corridor faces and 47 primary cards plus six corridor variants are refreshed. Risers now default on in the game and Layout Studio. A new saved preference migrates the retired forced-low setting while remembering subsequent explicit changes. Native station/default/adjacency/cache, settings, studio controls and card checks pass. [Before/after gallery with notes](../output/riser-departments-v1/index.html). Owner visual acceptance pending.

## September 8 dense-station rendering polish

[Rendering polish](DENSE_STATION_POLISH_2026-09-08.md) tightens off-screen room culling and shares door aperture calculations within each render frame, while physics reads live state. In the same 49-room fixture, flooded median frame time falls from 64.418 to 44.584 ms (about 31%); dry falls from 48.215 to 33.372 ms. Culling comparisons are pixel-identical at two tested zoom levels. Rendering cache and native wet-door/pause checks pass. Active repair wording is clearer. Dense views still exceed the 60 fps frame budget; owner review during normal play remains pending.

## September 8 crew action expansion

[All five animation priorities](CREW_ACTION_EXPANSION_2026-09-08.md) are generated,
packaged and integrated for Bill, Veld and Branforth: underwater work, swimming
transitions, torch draw/stow, cargo carry/unload and directional interactions.
168 added runtime clips include helmet variants; unloading checkpoints before
one-time cargo credit. Native pack, expedition, hull repair, construction,
swimming and room-activity checks pass. [Moving review](../output/crew-actions-review.html)
and [showcase](../output/crew-actions-preview.gif); owner visual acceptance pending.

## September 8 detailed doors and flooded closing

[Door art polish](DOOR_ART_POLISH_2026-09-08.md) integrates detailed skins across shared front/side, raised, BRINE default and airlock doors, with five finishes. Flooded closing adds aperture-limited wash/foam, pressure ripples and amber indicators; sealed doors show no crossing flow. Native production/pause, aperture, water physics, airlock and BRINE route checks pass; 44 cards refreshed and all 47 card identities validate. [Animated review and notes](../output/door-polish-v1/index.html). Owner visual acceptance pending.

## September 8 flood safety, controls and scale checks

[Safety and scaling pass](FLOOD_SAFETY_AND_SCALE_2026-09-08.md) adds conservative
repair air budgets, physical low-air retreat/refill, cancel/refund and crew
assignment, plus a station flood alert with room location and threshold hysteresis.
Standard rupture tuned to 3.2%/s and 14s work, still 5 Metal; old severe damage and
paid jobs remain compatible. Native safety/save and expedition tests pass; a
64-room open network conserves water. Water physics in a 49-room fixture fell
from 1.425 to 0.301 ms, but dense-overview rendering remains slow (~65 ms/frame).
[Controls preview](../output/hull-safety-controls.png). Owner review pending.

## September 8 submerged BRINE portrait

[V8](../character/brine-comms-v8/README.md) adds buoyant hair and refracted
underwater light so BRINE reads as suspended in water. Bubble occlusion updated
for the wider hair. Native comms and mask checks pass; owner review pending.

## September 8 BRINE glass background

[V7](../character/brine-comms-v7/README.md) replaces generic background light
bands with curved glass and cropped ivory framing matching the actual tube.
Smile and smaller bubbles preserved; native comms checks pass. Owner review pending.

## September 8 BRINE default entry doors

All four BRINE sockets now display closed pressure doors by default, including unconnected entries. North uses the themed riser door when raised walls are enabled; low north and the other three use ceramic/aquamarine leaves. Connected/open wall spans retain the existing animated door handling. Collision and connection rules are unchanged. Native card refreshed; see `assets/brine-default-doors-v1/README.md` for verification.

## September 8 hull leak variations and crew repairs

[Physical hull repairs](HULL_LEAK_REPAIRS_2026-09-08.md) replace instant hull sealing.
Hairline, seam and rupture profiles flood at 0.8/2/4% per second; repairs allocate
2/3/5 Metal and take 6/10/16 seconds at the worksite. Crew navigate and weld;
submerged work consumes oxygen. Partial paid work survives death and Continue.
Native repair/save, physics, render-cache and existing construction checks pass.
[Leak comparison](../output/hull-leak-variants.png); owner visual/pacing review pending.

## September 8 crew water contact

Owner accepted softer water and hull leaks. [Crew wake refinement](CREW_WATER_WAKE_2026-09-08.md)
replaces blue circles with faint, separated trailing strokes aligned to the crew.
Native stages/Save-Continue pass; [preview](../output/crew-wake-polish.png), owner review pending.

## September 8 softer water and hull leak

[Visual refinement](WATER_SOFT_LEAK_2026-09-08.md) removes the net-like water
highlights in favor of broad drifting light. Hull leaks now have fractured metal,
curved streams, droplets and impact ripples. Native stage/save check passes;
[before/after preview](../output/water-soft-leak-comparison.png), owner review pending.

## September 8 water physics and shadow polish

[Second polish pass](WATER_POLISH_2026-09-08.md) fixes near-empty pump and saturated
leak transfer, skips equal-depth water checks, adds aperture-driven doorway
currents, softens submerged crew shadows and reduces deep-water glare.
Physics/material-reuse, native Save/Continue and three-crew transit checks pass.
Three-room median frame time is 10.98 ms versus 10.50 ms before this pass; no
full-station speedup claimed. [Native stage comparison](../output/flood-heights-polish.png).
Owner visual acceptance pending.

## September 8 BRINE machinery, wall and starting thaw

[Room renewal](BRINE_ROOM_RENEWAL_2026-09-08.md) adds a distinct northeast machinery bank to the BRINE tray, ceramic/aquamarine riser and matching door panels, a fitted tube label and removal of the protruding floor decoration. Starting cryopod now retains the selected architect for ten simulation seconds; pause and Continue preserve progress. Recovery/save and default-room routes pass; native art reviewed. NE bank is available for placement, with an isolated fitted preview replacing the old workstation. Owner visual acceptance pending.

## September 8 water depth and performance

Water now visibly submerges crew and equipment as it rises, with animated floor
caustics, surface wakes and a front cutaway waterline. Two repeated room rebuilds
were removed: the three-room native fixture improved from 206.6 ms to 10.5 ms
median frame time. Targeted gameplay, rendering, live-layout and native checks
pass; owner visual acceptance pending. See [handoff](FLOOD_VISUAL_DEPTH_2026-09-08.md)
and [four-height comparison](../output/flood-heights-v2.png), plus the
[60-fps transit replay](../output/flooded-transit-v2.mp4).

## September 8 swimming helmet fit

Side-view follow-up now uses 36 measured per-pose face anchors and scalp occlusion
to prevent the bare head protruding through the shell. Close-up native review and
playback checks pass; moving preview updated to pose4 for owner review.

Swimming helmets now compose at a smaller, closer fit across all three architects
and four directions. Per-pose layering and timing retained. Native 72-pose loader
comparison and swim playback checks pass; owner visual/motion review pending.
See [handoff](SWIMMING_HELMET_FIT_2026-09-08.md).

## September 8 BRINE corner asset

Owner equipment revision: [v2 console](../assets/brine-corner-service-v2/README.md) adds dense monitors, diagnostic controls and circulation equipment to both arms using the supplied reference. The same tray entry now uses v2; 128-unit width and flush NW fit retained. Native tray/clearance and alpha checks pass; personal layouts unchanged. [Updated preview](../output/brine-corner-equipment-2026-09-08/room.png). Owner visual acceptance pending.

[Northwest corner service console](../assets/brine-corner-service-v1/README.md) starts the corner-fitted furniture series. A pearl-white/aquamarine L-shaped bank fits both walls while preserving BRINE's central chamber. Available in BRINE Core's Room Default tray at 128 world units wide; [native fitted preview](../output/brine-corner-service-2026-09-08/room.png), static prop/door clearance and alpha export pass. Personal layouts unchanged; one authored NW orientation, owner visual review pending.

## September 8 room style polish

[Before/after review](../output/room-style-polish-2026-09-08/index.html) polishes twelve recent south-facing banks against approved Tidal material quality and department references. Registered placement frames and personal layouts preserved. Riser doors now have recessed textured panels, seals and threshold details. Twelve comparisons beside Bill, ten default south placements, door animation and the 47-room gallery reviewed; card/source/alpha checks pass. Owner style acceptance pending. See [handoff](ROOM_STYLE_POLISH_2026-09-08.md).

## September 8 Studio owner-note corrections

[Illustrated review](../output/studio-owner-notes-2026-09-08/index.html) updates all 47 room previews and preserves the owner's three edited-room layouts. Studio adds centered Rotate Room / Next Room / Save, valid-edit autosave across rotations, R variant cycling, F flip and default-tray vertical views. Listening Post slices move; north riser door animates and replaces the low north edge. Mining/Refinery materials and three cutouts repaired; twelve authored south views added, ten used by current south-wall defaults. Forty-four cards refreshed. Native editor/targeted checks, 47-card consistency and 162 source hashes pass; owner visual acceptance pending. See [handoff](STUDIO_OWNER_NOTES_2026-09-08.md).

## September 8 room flooding and survival

Follow-up: [35-second native transit replay](../output/flooded-transit.mp4) shows
all three crew swimming through real doorways and changing movement as water
spreads between compartments. Headless/native routes and video decode pass.

[Implementation and checks](ROOM_FLOODING_2026-09-08.md) add gradual hull leaks,
open-door water transfer, powered pump drainage and low/wading/swimming/critical
stages. Crew have 15-second breath, 60-second helmet tanks, real locker refills,
oxygen/exposure deaths and a provisional 90-second starvation period. Water and
survival clocks persist through Continue. Focused logic, expedition/refill and
disk-save checks pass; native stages reviewed. Owner pacing/visual acceptance is
pending. This supersedes the earlier instantaneous food-shortage casualty behavior.

## September 8 BRINE expression

[V6](../character/brine-comms-v6/README.md) gives BRINE a faint composed smile
to address the sad expression. Crew style, tube framing and smaller bubbles
preserved. Native comms checks pass; owner review pending.

## September 8 BRINE crew-style portrait

[V5](../character/brine-comms-v5/README.md) brings BRINE closer to Bill/Veld's
angular, matte pixel rendering and reduces bubble size by about a third.
Spacious tube framing preserved. Native comms checks pass; owner review pending.

## September 8 full room art catalog

[Owner review catalog](../output/room-catalog-2026-09-08/index.html) covers all 47 room types with 167 native stills and 75 recent standalone prop records. All 44 furnished-room cards refreshed from live renderers; primary/grid/variant consistency and native portrait checks pass. 150 wall-source hashes match. New standalone libraries still need fitted room installation, including known seed/communications overlap fixes. See [handoff](ROOM_ART_CATALOG_2026-09-08.md); owner notes and installation work remain pending.

## September 8 navigation badges

Owner follow-up groups Archive, Diagnostics, Journal and Menu into one top-right row and removes the top resonance/cycle displays. Compact badge labels and two-size native review complete.

[Clean colored badges](NAVIGATION_BADGES_2026-09-08.md) now appear on the HUD, title tiles and pause Codex entry. Runtime silhouette clipping excludes source checkerboards. Native Journal/Diagnostics checks pass;1600/960 HUD and title captures visually reviewed. Owner review pending.

## September 8 maintenance parts-cleaning bank

[North cleaning bank](../assets/parts-cleaning-wall-v1/README.md) adds dry basin, supplies and ribbed parts mat at320 by78.70 units. V2 corrects washer and quiets fittings; muted bottle shoulder facets remain. Native material/alpha review and clean log pass. Standalone art only; room fit, other directions and cleaning behavior remain outstanding.


## September 8 short communications section host study

The [100-unit section](../assets/communications-south-section-v1/README.md) adds finished ends and fits the tested Radio Lab south gap without visual furniture or door overlap. Native art and static host capture reviewed. Host helper gains --section mode; no room data changed. Mounting, occupied access and owner acceptance remain pending.

## September 8 seed carrier supported group

[Group review](../output/seed-packet-carrier-v1/group-scale.png) places the24-unit carrier on the right worktop while retaining the28-unit propagation tray on the left. Native and2x review shows support and a clear central sorting tray. Static group pass; hand clearance, lifting and runtime attachment remain unverified.


## September 8 seed packet carrier

[Small carrier](../assets/seed-packet-carrier-v1/README.md) adds three supported packets at24 by19.50 units. Native material/alpha review and clean export log pass; enclosed handle aperture is registered and sampled transparent. Handle pose, worktop placement and carrying animation remain unverified.


## September 8 communications host fit rejected

The [Radio Lab study](COMMUNICATIONS_HOST_STUDY_2026-09-08.md) retains current furniture while comparing all four full banks. North overlaps the installed signal wall; south intersects the electronics bench; both side banks cross doors and furniture. Native capture reviewed, no room data changed. Next: shorter service sections or a distinct host layout.

## September 8 gallery placement evidence

The material review gallery now displays contextual host, relocation and supported-group reviews with separate verdicts, findings and evidence links. Rejected original layouts remain visible alongside later static proposals; changed hashed study evidence gets a stale warning. Five gallery tests pass;72 records generated with no stale export hashes. Browser rendering was not checked in this change.


## September 8 seed section relocation proposal

[Relocation study](../output/seed-sections-relocation-study.png) retains all six Hydroponics furniture items and clears measured seed-section overlaps. Crops move68 units right; nutrients and harvest stand96 right. West door stays clear with other walls closed. Native visual review and clean log pass. No runtime installation; crew access and service connections remain unverified.


## September 8 foundation seabed contact

Foundation feet now have broader contact shadows and overlapping sediment to
connect them visually to the ocean floor. Opening-room native preview reviewed;
owner acceptance pending. See [handoff](FOUNDATION_CONTACT_2026-09-08.md).

## September 8 split seed bank host review

[Paired host study](../output/seed-sections-host-study.png) confirms a96-unit section gap clears the72-unit west doorway with12-unit axial margins. Sorting still overlaps crops; storage overlaps nutrients and harvest stand. No room data changed. These assets need a distinct preparation layout or measured furniture relocation before installation.


## September 8 handheld signal meter

The [16-unit meter](../assets/handheld-signal-meter-v1/README.md) adds a supported communications companion. V2 quiets pointer and casing details; native material/alpha and static mat-group review pass. Source-space support and actual dimensions recorded. Pickup, live signals and room placement remain unimplemented.

## September 8 short seed storage section

[West storage section](../assets/seed-storage-west-section-v1/README.md) adds four tins and cassette with right-facing catches. V2 quiets shiny lid rims. Native material/alpha review passes. Actual67.84 by136 is deeper than sorting55.24; paired room fit remains pending.


## September 8 short seed sorting section

[West sorting section](../assets/seed-sorting-west-section-v1/README.md) adds a finished-end136-unit module. V2 quiets seed shading and widens the narrow first pass; actual depth55.24 exceeds the45-unit brief and awaits host assessment. Native material/alpha review passes. Storage companion and furniture-fit solution remain outstanding.


## September 8 communications four-direction coverage

The [east bank](../assets/communications-service-east-wall-v1/README.md) completes four standalone directions at66.54x320 with left-facing access. Native material/alpha and clean-log review pass. [Family handoff](COMMUNICATIONS_SERVICE_FAMILY_2026-09-08.md) records dimensions and pending host/clearance review. No runtime changes.

## September 8 west communications counter

The [west bank](../assets/communications-service-west-wall-v1/README.md) adds right-facing access. V3 reduces visual depth from95.17 to65.07 at320-unit length, retaining three leads and spare connectors. Native review passes; north/south/west indexed. East and runtime placement pending.

## September 8 seed bank host fit rejected

[Host study](../output/seed-bank-host-study.png) overlays the slim west bank on current Hydroponics with furniture retained. It intersects crops, nutrients and harvest stand; an open west wall also blocks the central door. No room data changed. Next art work: shorter sections with central access or a distinct preparation-room host. Native standalone art remains valid; this placement does not.


## September 8 seed bank four-direction art family

[East seed bank](../assets/botanical-seed-east-wall-v1/README.md) completes four standalone directions at46.76 by320 with left-facing access. V2 restores four tins lost in V1. Native scale/material/alpha review and clean export log pass; four-view provenance audit passes. Casebook and bible record dimension and inventory drift. Runtime placement remains unverified.


## September 8 portrait room-card preview

Room cards now use 224 × 320 portrait proportions with larger artwork and
width-relative rarity badges. The hand tray is taller to accommodate them.
Native 1600 × 900 preview shows three cards without clipped names or costs:
`output/portrait-room-cards.png`. Owner review pending; see
[handoff](PORTRAIT_ROOM_CARDS_2026-09-08.md).

## September 8 south communications counter

The [south bank](../assets/communications-service-south-wall-v1/README.md) adds north-facing fixtures and cabinet access. V3 quiets the rear rail and screen after orientation repair. Native320-unit review passes; north/south indexed with cabinet differences recorded. Side variants and runtime placement pending.

## September 8 slim west seed bank

[West botanical seed bank](../assets/botanical-seed-west-wall-v1/README.md) adds a 45.36 × 320 matte side-wall variant with right-facing access. V1 rejected for excess depth; V2 has three packets and narrower construction. Native visual review and clean export log pass. Family now north/south/west; east and runtime installation remain outstanding.


## September 8 radial lighting and riser cutaways

Hidden risers now hide their light fixture housings in-game and in Room Layout
Studio; neighboring rooms and the wall hardware toggle also suppress unsupported
mounts. Interior and exterior illumination now use soft radial falloff. Native
cutaway, Studio, power-toggle and renderer checks pass; owner visual review pending.
See [lighting handoff](RADIAL_LIGHT_CUTAWAY_2026-09-08.md).

## September 8 communications service counter

The [communications bank](../assets/communications-service-wall-v1/README.md) adds patch leads, a compact tester/handset and clear repair mat. V2 quiets bright hardware. Native320-unit material/alpha and clean-log review pass; waveform and cables are static art, with placement and owner acceptance pending.

## September 8 spacious BRINE tube

[V4 portrait](../character/brine-comms-v4/README.md) fills the comms frame with
the wider tube interior, with outer supports beyond the crop. BRINE's scale and
animated bubbles are preserved. Native comms checks pass; owner review pending.
Bubbles subsequently enlarged and brightened, with staggered starting positions
so they are visible immediately. Native small-portrait review and comms checks pass.

## September 8 south botanical seed bank

The [south bank](../assets/botanical-seed-south-wall-v1/README.md) adds north-facing
drawers and container latches. Native320-unit material/alpha review passes; white
source background preserves pale edges. North/south indexed with added right
drawers recorded. Side views and room placement remain pending.

## September 8 textile counter four-direction coverage

The [south bank](../assets/textile-repair-south-wall-v1/README.md) completes four standalone textile directions after correcting the sewing throat toward the operator. Native material/alpha and clean-log review pass. [Family handoff](TEXTILE_REPAIR_FAMILY_2026-09-08.md) records independent dimensions, the basket companion and pending runtime placement.

## September 8 BRINE portrait correction

[V3](../character/brine-comms-v3/README.md) removes the bottom tube rim and adds
sparse animated bubbles masked behind BRINE. Native comms and foreground checks
pass; corrected artwork and prompt retained alongside earlier versions.

## September 8 seed-bank supported grouping

The [propagation-tray group](../assets/covered-propagation-tray-v1/README.md) places
the28-unit tray on the bank without overhang or sorting-tray overlap. Native/2x
static support review and hash checks pass. Hand clearance, lift animation and
runtime attachment remain unverified; original raster assets unchanged.

## September 8 east textile counter

The [east bank](../assets/textile-repair-east-wall-v1/README.md) adds left-facing access at320-unit length and67.65 visual depth. Native material/alpha and clean-log review pass. North/west/east indexed with independent dimensions; south and runtime placement pending.

## September 8 covered propagation tray

The [28-unit tray](../assets/covered-propagation-tray-v1/README.md) adds a closed
opaque companion for Hydroponics. V2 removes shiny bevels; native material/alpha
review passes. Backed vents stay opaque. Contents, support placement and owner
acceptance remain unverified; both sources and prompts retained.

## September 8 west textile counter

The [west bank](../assets/textile-repair-west-wall-v1/README.md) adds right-facing access at320-unit length and74.28 depth. V3 corrects orientation, tin latch and accessory scale. Native material/alpha and clean-log review pass; north/west indexed, south/east and runtime placement pending.

## September 8 botanical seed-storage wall

The [seed bank](../assets/botanical-seed-wall-v1/README.md) adds packets, sorting
tray and opaque tins for Hydroponics. Native320-unit material/alpha review passes.
V2 replaces a dark checkerboard that conflicted with pale cabinet edges; rejected
geometry retained. Static candidate, pending placement and owner review.

## September 8 BRINE tube comms portrait

The [tube portrait](../character/brine-comms-v2/README.md) puts BRINE inside her
canonical pale-collared glass chamber, preserving her established face and suit.
Installed in Comms; the original portrait is retained. Native reveal/replay and
1600/960 containment checks pass, with both sizes visually reviewed. Owner visual
acceptance remains pending.

## September 8 reusable alpha probe validation

The [pixel validator](ASSET_ALPHA_PROBES_2026-09-08.md) makes named opening/interior checks executable and hash-bound. Nine tests and the textile basket five-point check pass. Material workflow updated and installed reference synchronized. Selected pixels only; no new silhouette or runtime acceptance.

## September 8 textile repair basket

The [28-unit basket](../assets/textile-repair-basket-v1/README.md) adds a loaded fabric companion. Native/shared-scale review passes after black-background and rim repair, followed by registration spike cleanup. Named alpha probes include coordinates and export hash for reproducibility. Static art only; room placement and owner acceptance pending.

## September 8 directional registration guard

The [audit update](DIRECTIONAL_REGISTRATION_GUARD_2026-09-08.md) rejects changed
reviewed outlines and swapped registration paths. Sixteen tests and both four-view
chart/tool families pass. Legacy registration coverage is explicit; no new visual
or placement acceptance. Material workflow updated.

## September 8 textile repair counter

The [textile workbench](../assets/textile-repair-wall-v1/README.md) adds a compact sewing machine, clear cutting space and fabric storage. V2 corrects oversized equipment and bright hardware. Native320-unit material/alpha and clean-log review pass; static north-wall candidate with placement and owner acceptance pending.

## September 8 chart-counter four-view coverage

The [east counter](../assets/observation-chart-east-wall-v1/README.md) completes
four standalone chart-bank directions. Native320-unit material/alpha review and
four-view metadata audit pass. Sleeve construction and depth differences remain
explicit; room placement and owner acceptance pending.

## September 8 listening counter four-direction coverage

The [south bank](../assets/crew-listening-south-wall-v1/README.md) completes four standalone listening-counter directions. Native320-unit light/dark review and clean Godot log pass. Directional depths differ; room placement and owner acceptance remain pending. See [handoff](CREW_LISTENING_FAMILY_2026-09-08.md).

## September 8 west chart-counter candidate

The [west counter](../assets/observation-chart-west-wall-v1/README.md) adds east
access at320-unit length and74.01 depth. Native material/alpha review passes;
three-view family metadata checks pass. East art and room placement remain pending;
side-view storage differences are recorded.

## September 8 crew listening east candidate

The [east counter](../assets/crew-listening-east-wall-v1/README.md) adds left-facing controls and access at full320-unit length. Native light/dark material and alpha review pass. North/west/east are indexed; south and runtime placement remain pending.

## September 8 south chart-counter candidate

The [south counter](../assets/observation-chart-south-wall-v1/README.md) adds inward
north drawer access and a plain rear panel. Native320-unit material/alpha review
passes. North/south indexed with depth/construction differences; side views and
room placement remain pending.

## September 8 Observation chart folio

The [22-unit closed folio](../assets/observation-chart-folio-v1/README.md) adds a
matte canvas companion to the chart counter. Native alpha/material and supported
tabletop group review pass. Static art, pending runtime placement and owner review;
source, exact prompt and evidence preserved.

## September 8 riser-mounted fixtures and exterior beams

The [lighting follow-up](RISER_LIGHTING_2026-09-08.md) removes low north-strip
dressing and makes the riser the single light mount. Fixtures stay visible and
stationary when the riser is hidden; legacy low-light offsets/settings remain
readable. Brighter exterior cones point away from exposed edges, clearing the
riser crown and foundation. Native studio/station captures, migration, editor
regressions and hardware controls pass. Owner visual acceptance remains pending.

## September 8 Observation chart counter

The [chart bank](../assets/observation-chart-wall-v1/README.md) adds matte wood map
drawers, plotting surface and rolled-chart storage. Native320-unit material/alpha
review passes after base-fringe cleanup. Static standing counter; room placement
and owner acceptance pending. Source, prompt and revised bounds recorded.

## September 8 crew listening west candidate

The [west listening counter](../assets/crew-listening-west-wall-v1/README.md) adds right-facing player access and smaller headphones in backed docks. Native320-unit review passes;92-unit visual depth recorded separately from north. Family index tracks north/west with south/east absent. No runtime changes.

## September 8 wall-host evidence clarification

The [host review](WALL_HOST_EVIDENCE_2026-09-08.md) separates16-unit strip depth
from the owner-directed60-unit raised face. Notice-rail dependency hashes still
match; its schematic fit remains valid only for the strip. Workflow and asset
notes clarified, installed skill synchronized. No new mounting acceptance.

## September 8 audit report protection

The [family audit](DIRECTIONAL_FAMILY_AUDIT_2026-09-08.md) now protects linked files and unrelated JSON, writes atomically, and records failures instead of leaving an earlier tool-owned pass. Thirteen tests pass; water-assay and galley have valid protected-format reports. No art or runtime changed.

## September 8 mechanical tool four-view coverage

The [east bank](../assets/mechanical-tool-east-wall-v1/README.md) completes four
standalone directions. Native320-unit material/alpha review passes; all four
metadata records audit successfully. East75.21 and west70.47 depths remain explicit.
Room placement and owner acceptance are still pending.

## September 8 unrolled exercise mat

The [olive mat](../assets/crew-exercise-mat-v1/README.md) adds a28x57.11-unit floor candidate beside the exercise cabinet. V2 corrects the overly elongated source; native/shared-scale and alpha review pass. Unrolled static state only, with occupied clearance and placement pending.

## September 8 mechanical tool west candidate

The [west bank](../assets/mechanical-tool-west-wall-v1/README.md) adds east-facing
access. V2 narrows depth from102.13 to70.47 at320-unit length. Native material and
alpha review pass after rear-edge cleanup. Three directions indexed; east and
room placement remain pending. Sources and exact repair prompts retained.

## September 8 riser height and square-wall refresh

[Risers are 25% taller](RISER_WALL_REFRESH_2026-09-08.md) (48 to60 units), with
matching caps, returns, mounts and lighting. Eight rooms now use textured square
perimeters and corner caps. All44 furnished rooms were reviewed in four rotations;
44 cards refreshed. Native wall/adjacency checks pass. The broader Airlock test
reported five helmet-state failures, recorded separately for investigation.

## September 8 Room Studio usability follow-up

The [usability pass](ROOM_STUDIO_USABILITY_2026-09-08.md) fixes pointer-centered
previews, restored-default clearance and stable corner resizing. The tray now
has focused common categories, five more reusable props (45 total), and clean
registered-cutout thumbnails. Native title entry, normal-rule drag/drop and return,
save/reload, existing editor behavior and thumbnail shutdown pass. Category and
window-size captures were visually reviewed; owner hands-on acceptance remains.

## September 8 crew exercise storage wall

The [exercise cabinet](../assets/crew-exercise-wall-v1/README.md) adds modest weights, bands, mats and fabric storage. V2 reduces rubber-edge glints; native320-unit and alpha review pass. Static low storage candidate, with retrieval and occupied exercise clearance unverified. Placement and owner review pending.

## September 8 mechanical tool family metadata

The [family audit](MECHANICAL_TOOL_FAMILY_AUDIT_2026-09-08.md) verifies both source
dimensions and hashes and converts the index to the reusable directional schema.
Both indexed views pass metadata checks; east/west remain missing. South repair
history and final evidence now have hashes. Raster and visual verdicts unchanged.

## September 8 mechanical tool south counterpart

The [south bank](../assets/mechanical-tool-south-wall-v1/README.md) adds north-facing
access. V2 repairs pouch/drawer facing; V3 removes tool shine through dark sleeves
and plain spanners. Native320-unit and alpha review pass. North/south family indexed
with construction differences; side views and room placement remain pending.

## September 8 reusable directional audit

The [family metadata audit](DIRECTIONAL_FAMILY_AUDIT_2026-09-08.md) checks coverage, declared facing, hashes, review evidence and scale. Eight tests pass; water-assay and galley pass all four indexed views. Metadata validation does not establish visual or runtime acceptance. Production guide updated with the reusable command.

## September 8 playable character construction

The [construction handoff](CHARACTER_CONSTRUCTION_IMPLEMENTATION_2026-09-08.md)
replaces opening emergency-drone builds with an architect welding from an existing
room. Twelve directional loops and work-driven room assembly are integrated;
paid costs, ten seconds of manual work, interruption/save progress and later
dedicated drone builders remain. Twelve native actor/direction cases, save and
fleet regressions, sprite checks and the paid-opening fixture pass. Native review
also corrected full-wall cached drawing at completion. Owner pacing/animation
acceptance and a new packaged build remain separate.

## September 8 mechanic kneeling-pad companion

The [28-unit pad](../assets/mechanic-kneeling-pad-v1/README.md) adds a matte fabric
companion to the tool wall. True-alpha export and native/shared-scale review pass.
Pouch is closed; no kneeling behavior or placement is installed. Occupied posture
and clearance remain pending. Existing material/group workflow reused.

## September 8 crew listening wall candidate

The [listening counter](../assets/crew-listening-wall-v1/README.md) adds cassette trays, a player and two backed headphone docks. V2 replaces unintended book-like storage; native320-unit and alpha review pass. Standing counter candidate, no playback or seated-use behavior. Placement and owner review pending.

## September 8 mechanical tool wall candidate

The [tool bank](../assets/mechanical-tool-wall-v1/README.md) adds olive drawers,
recessed tools and a clear repair mat. V2 reduces shiny hardware; native320-unit
material/alpha review passes. Standalone, pending placement and owner review.
The [handoff](MECHANICAL_TOOL_WALL_2026-09-08.md) records a new graphical review
wrapper that rejects error logs even when a PASS marker appears; four tests pass.

## September 8 water-assay directional candidates

The [four-view handoff](WATER_ASSAY_DIRECTIONAL_CANDIDATES_2026-09-08.md) records north/south/west/east art. East native review passes; all source/export hashes match. Visible depth differences remain explicit. Standalone directional coverage complete; owner acceptance and runtime placement remain pending.

## September 8 water-assay west candidate

The [west bank](../assets/water-assay-west-wall-v1/README.md) adds a328-unit vertical view with right-facing access. V2 restores filtration tray and corrects analyzer orientation. Native material/alpha review passes; family now records north, south and west. East view and runtime placement remain pending.

## September 8 water-assay south candidate

The [south bench](../assets/water-assay-south-wall-v1/README.md) puts backing south and access north. V2 corrects individual analyzer/case facing; native328-unit review passes. North/south family index records exports and missing side views. Standalone, awaiting placement and owner review.

## September 8 reading-wall knee-recess variant

The [desk variant](../assets/lounge-reading-recess-v1/README.md) removes the
central lower panel/plinth while retaining side supports and matte reading art.
Native320-unit material/scale and alpha review pass. The opening measures85.36
units at the recorded sample; original wall preserved. Occupied seating and
runtime placement remain unverified; gallery refreshed.

## September 8 simplified Room Layout Studio

The [studio simplification](ROOM_STUDIO_SIMPLIFICATION_2026-09-08.md) adds WASD
camera movement, fourteen whole-room floor presets, visible doors, 50% new tray
placements and bottom-right drag resizing. A bordered thumbnail tray includes
Room Default and forty common props; objects drag out and back in. Coordinates
and saved arrangements leave the visible UI; secondary controls sit under Options.
Three graphical fixtures pass, including native drag preview/drop and 1600/960
visual review. Existing saved sizes remain; owner usability acceptance is pending.

## September 8 Lounge shared-scale arrangement

The [reading group](../assets/lounge-reading-stool-v1/README.md) pairs the26-unit
stool and320-unit wall in a native/2x diagnostic. Visual proportion, palette and
export/hash checks pass. The solid cabinet front has no knee recess, so occupied
reading posture and reach remain unverified; this is a static grouping proposal.

## September 8 cargo dolly state-pair review

The [state-pair handoff](CARGO_DOLLY_STATE_REVIEW_2026-09-08.md) verifies both exports at one crop and36-unit width. Native/2x static review passes; binary silhouettes overlap99.1%, with small recorded bounds drift. Runtime transitions and collision remain unverified. Existing casebook entry updated with this evidence.

## September 8 drone component wall candidate

The [drone service bank](../assets/drone-component-wall-v1/README.md) adds gripper
jaws, empty assembly cradle, actuator and diagnostics. V2 corrects inherited
battery-pack shapes. Native320-unit matte/scale and alpha review pass; gallery
refreshed. Standalone, pending placement and owner review. Reference-subject
transfer failure recorded in the casebook.

## September 8 archive trolley candidate

The [loaded archive trolley](../assets/archive-trolley-v1/README.md) adds a32-unit companion to the restoration bench. Native material/alpha and shared-scale group review pass. Loaded state and handle exclusions recorded; no hauling behavior or room placement added. Existing group and alpha workflow reused without adding duplicate skill rules.

## September 8 archive restoration wall candidate

The [restoration bench](../assets/archive-restoration-wall-v1/README.md) adds continuous cartridge intake, reading, sorting and preservation tasks. V2 reduces inherited bright trim; native328-unit and alpha review pass. Standalone, pending placement and owner review. Reference-transfer lesson recorded in the casebook.

## September 8 filter-service comparison completed

The [filter bank](../assets/filter-service-wall-v1/README.md) now has a clean native
comparison beside the furnished Life Support room at320 units. Visual scale
review passes; export hash is unchanged. The earlier renderer failure remains in
the history, and the gallery reflects the completed agent review. Placement and
owner acceptance remain pending; no floor code was changed in this art task.

## September 8 filter-service wall candidate

The [filter bank](../assets/filter-service-wall-v1/README.md) adds Life Support
filter shelves, inspection tray and test equipment. V2 corrects silver brackets
and paper highlights; isolated native material/alpha review passes. Full room
comparison remains pending after an undeclared `pads` error in the floor renderer.
The failed log is retained; no floor code changed. Gallery records partial scale
review and standalone status rather than a full visual pass.

## September 8 maintenance bench arrangement

The [case support proposal](../assets/seal-maintenance-case-v1/README.md) places the26-unit case on the pressure-seal mat with its full handle inside measured support bounds. Native group visual and export/hash checks pass; tools remain clear. Runtime attachment and occupied clearance remain pending. The faucet trial moved intact into the material casebook, preserving the concise daily guide.

## September 8 water-assay wall candidate

The [water-assay bench](../assets/water-assay-wall-v1/README.md) adds three unequal science task zones and clear preparation space. V3 replaces a persistently shiny faucet with a flat-sided spout. Native328-unit and alpha review pass; standalone, pending owner review and placement. Repair lesson recorded in the room skill.

## September 8 material workflow consolidation

The [workflow handoff](MATERIAL_WORKFLOW_CONSOLIDATION_2026-09-08.md) separates
the119-line daily guide from the preserved304-line casebook. Original text
preservation is hash-verified; maintained/installed skills match. All production
gates remain, with detailed future trials routed to case notes or asset records.
No asset or runtime changes in this maintenance step; art production remains active.

## September 8 Battery service wall candidate

The [battery bank](../assets/battery-service-wall-v1/README.md) adds pack cradles,
an inspection surface, cable trays and enclosed diagnostics. Native320-unit
matte/scale and alpha review pass; gallery refreshed. Four unequal task areas
vary the composition. Standalone, pending placement and owner review.

## September 8 maintenance case candidate

The [sealed maintenance case](../assets/seal-maintenance-case-v1/README.md) adds a26-unit engineering prop. V2 removes glow and excessive edge wear; native and handle-alpha review pass. Closed static candidate, not installed. Material-repair lesson recorded in the room pipeline.

## September 8 notice rail measured-size follow-up

The [rail handoff](../assets/crew-notice-rail-v1/README.md) now records a
131.74×14 alternative for the inherited16-unit wall strip. Native schematic
size/readability review passes with unchanged source/export. Fine marks become
decorative. Mounting-plane orientation, depth ordering and doors remain unverified;
no wall geometry or runtime art changed.

## September 8 group-preview validation

The [group diagnostic](PROP_GROUP_REVIEW_2026-09-08.md) rejects clipped crops/arrangements, invalid coordinates, stale hashes and export overwrites. Eight graphical checks pass; valid console/stool capture visually reviewed. This establishes static preview integrity, not room placement or collision.

## September 8 pressure-seal maintenance wall candidate

The [pressure-seal bank](../assets/pressure-seal-wall-v1/README.md) adds gasket storage, assembly space, enclosed testing and lubricant supply. V2 reduces bright tool and gauge hardware; native328-unit and alpha review pass. Standalone, pending placement and owner review. Edit-output transparency lessons recorded in the room skill.

## September 8 Crew notice rail candidate

The [notice rail](../assets/crew-notice-rail-v1/README.md) adds a shallow clock,
paper/postcard strip and personal-effects ledge. Native240-unit matte/scale and
alpha review pass; gallery refreshed. Host fit and owner review remain pending:
the25.50-unit visual height must not be used to justify raising the low hull.

## September 8 operator stool and group diagnostic

The [operator stool](../assets/operator-stool-v1/README.md) adds a modest22-unit companion to the analog control bank. Alpha and native visual review pass; a reusable Godot group board checks shared scale and export hashes. Static arrangement only, with occupied clearance and runtime placement pending.

## September 8 Lounge reading stool candidate

The [small reading stool](../assets/lounge-reading-stool-v1/README.md) complements
the wooden wall bank with matte fabric seating. Native26-unit scale/material and
between-leg alpha review pass; standardized gallery refreshed. Standalone,
pending placement and owner review. Seating approach/interaction remains separate.

## September 8 analog control wall candidate

The [analog control bank](../assets/analog-control-wall-v1/README.md) adds five connected olive console bays inspired by the owner references. Transparent export and native 328-unit visual diagnostic pass agent review. Standalone asset; room placement and owner acceptance remain pending.


## September 8 Ore sampling wall candidate

The [sampling bank](../assets/ore-sampling-wall-v1/README.md) adds mineral trays,
weighing/preparation equipment, an enclosed analyzer and sealed samples. V2
reduces silver edging and stone sparkle. Native320-unit matte/scale and alpha
review pass; standardized gallery refreshed. Standalone, pending placement and
owner review. Mineral-material guidance added to the skill and bible.

## September 8 gallery coverage refinement

The [material gallery](MATERIAL_REVIEW_GALLERY_2026-09-08.md) now includes22
standardized records, including multi-asset `*-review.json` files. All export
hashes and110 local links match. Three discovery/findings tests pass; duplicates
are rejected and written review findings are shown. Browser rendering remains
unverified. This is a candidate subset, not total room-art coverage.

## September 8 empty cargo dolly candidate

The [empty dolly](../assets/cargo-dolly-empty-v1/README.md) complements the loaded
prop. Native36-unit and alpha review pass. A state index records both exports,
small bounds drift and a proposed shared region; runtime transitions remain
unverified. Both are standalone candidates awaiting placement and owner review.

## September 8 Lounge reading and games wall candidate

The [reading bank](../assets/lounge-reading-wall-v1/README.md) adds books, games,
a reading surface and compact radio. V2 reduces bright wood-edge lines and grain.
Native320-unit matte/scale and alpha review pass. Standalone, awaiting placement
and owner review; warm-wood material lessons added to the skill and bible.

## September 8 loaded cargo dolly candidate

The [cargo dolly](../assets/cargo-dolly-v1/README.md) adds a small strapped-parcel
platform matching the packing area. Native36-unit and alpha review pass, including
handle opening and retained parcel checks. Loaded state is explicit; no hauling
or empty variant is installed. Gallery rebuilt with matching export hashes.

## September 8 Cryo recovery wall candidate

The [Cryo support bank](../assets/cryo-recovery-wall-v1/README.md) adds blankets,
recovery clothing, a preparation counter, monitoring dock and enclosed thermal
service cabinet. V2 repairs outer-edge flecks and bright trim. Native320-unit
material/scale and alpha review pass. Standalone; placement and owner review remain.

## September 8 cargo packing wall candidate

The [cargo wall](../assets/cargo-packing-wall-v1/README.md) adds weighing, packing,
labeling and open dispatch trays. Native328-unit and alpha review pass; records
describe the actual open-tray configuration. The gallery now has 16 standardized
candidates with matching hashes. This wall is uninstalled and awaits owner review.

## September 8 Quarantine preparation wall candidate

The [Quarantine bank](../assets/quarantine-preparation-wall-v1/README.md) adds
garment storage, a basin, transfer cassette, returns hatch and filtration cabinet.
Native320-unit matte/scale and alpha review pass; source-specific dark-background
cleanup retains the basin and garment. Standalone, pending placement and owner
review. Pipeline guidance extends the existing measured-threshold lesson.

## September 8 local material review gallery

The [review gallery workflow](MATERIAL_REVIEW_GALLERY_2026-09-08.md) gathers 14
standardized candidates with facing, scale and native-evidence links. All export
hashes and local links pass. Browser policy blocked the local-file preview, so
page rendering/filter interaction remains unverified. This is a record subset,
not total art coverage; ongoing asset production remains active.

## September 8 Storage Bay dispatch wall and dolly

The [dispatch set](../assets/storage-dispatch-wall-v1/README.md) adds a packing/
weighing wall at320 units and small cargo dolly at38. Native material/scale and
alpha review pass, including the dolly grab slot. V2 corrects shiny case corners
and bumper; rejected source retained. Both are standalone, pending placement and
owner review. Skill/bible guidance now preserves usable packing work surfaces.

## September 8 emergency response wall candidate

The [emergency wall](../assets/emergency-response-wall-v1/README.md) adds rescue
supplies, a folded stretcher, masks, trauma kit and incident terminal. V3 removes
persistent visor reflections; native 328-unit and alpha review pass. Earlier
revisions remain recorded. Standalone, with placement and owner review pending.

## September 8 acoustic service wall candidate

The [acoustic service bank](../assets/acoustic-service-wall-v1/README.md) adds
hydrophone preparation, recording storage, calibration and cable trays for the
Listening Post. Native 320-unit matte/scale and true-alpha review pass. It remains
standalone, with placement and owner review pending. The record initializer was
used for provenance; the art guidance now records complementary service tasks.

## September 8 specimen carrier candidate

The [specimen carrier](../assets/specimen-carrier-v1/README.md) adds a small sealed
laboratory case. Native 28-unit and alpha review pass, including transparent handle
and retained inspection-window checks. The new initializer captured provenance
before visual findings were added. Standalone; placement and owner review remain.

## September 8 reusable asset review initializer

The [record initializer](ASSET_RECORD_INITIALIZER_2026-09-08.md) replaces repeated
provenance setup with one command. It records hashes and native scale, rejects
stale sources and overwrites, and leaves visual/owner acceptance unset. Five
focused tests and real east-galley metadata/overwrite checks pass. The room skill
now documents its use for subsequent assets.

## September 8 medical supply wall and cart candidates

The [clinical supply set](../assets/medical-supply-wall-v1/README.md) adds a 320-unit
wall bank and 36-unit cart. Native matte-material/scale and alpha review pass.
Cart V2 reduces glossy rim/packet highlights; the wall required a bounded rear-edge
registration repair. Skill/bible lessons updated. Both remain standalone; placement
and owner acceptance are pending, with ongoing art production still active.

## September 8 salvage workbench wall candidate

The [salvage workbench](../assets/salvage-workbench-wall-v1/README.md) adds parts
sorting, mechanical repair, a vise and electrical testing artwork. True-alpha
export and native 328-unit review pass. The projecting vise needs actual operator
clearance review during placement; the asset remains static and uninstalled.

## September 8 cultivation service wall candidate

The [cultivation service wall](../assets/cultivation-service-wall-v1/README.md)
adds seed storage, potting, propagation preparation, mixing and irrigation artwork.
True-alpha export and native328-unit review pass. The review template separates
depicted functional bays from runtime behavior; this remains uninstalled static
art awaiting owner review.

## September 8 Crew linen wall and hamper candidates

The [linen utility set](../assets/crew-linen-wall-v1/README.md) adds a warm fitted
wall and a small 34-unit hamper. Transparent exports and native material/scale
review pass. Hamper V2 removes shiny frame highlights; darker checkerboards and
the handle opening required source-specific cleanup. Skill/bible lessons recorded.
Both remain standalone candidates, with placement and owner review pending.

## September 8 crew utility wall candidate

The [crew utility wall](../assets/crew-utility-wall-v1/README.md) adds clothing
storage, washing, drying, folding and linen supplies. V2 corrects upright drawer
facades into low overhead surfaces. Transparent export and native328-unit review
pass; it remains standalone and awaiting owner review. The skill records the
projection correction for future storage briefs.

## September 8 engineering repair trolley candidate

The [repair trolley](../assets/repair-trolley-v1/README.md) adds a small diagnostic,
tool and cable cart. V2 reduces silver tool rims and surface speckling. Native
38-unit review passes; its enclosed handle gap is verified in geometry and export
alpha. Standalone candidate, not installed or owner accepted. The skill records
individual tool finishes and enclosed-aperture checks.

## September 8 Airlock low side-wall candidates

The [Airlock side-bank handoff](../assets/airlock-side-wall-v1/README.md) adds west/
east low preparation banks with inward access. Both have transparent exports and
native 320-unit length review; they are companion designs with packed-suit drawers,
not exact side views of the hanging-suit wall. A stacked-elevation failure is kept.
The review tool now segments tall material details, with a passing horizontal
export regression. Skill/bible lessons updated; room placement remains open.

## September 8 station hardware sidebar

The [eight-control hardware panel](STATION_HARDWARE_2026-09-08.md) is integrated:
power, Comms, wall/foundation visibility, sprinklers, internal door locks,
interior/exterior lights and Pumps. Owner decision: Pumps gates existing water
production while preserving manual suspension; sprinklers are visual only.
Controls and feedback, save compatibility, compact Comms and power checks pass.
Native 1600/960 review is complete; owner playtest remains.

## September 8 four-direction galley candidates

The [south galley](../assets/galley-south-wall-v1/README.md) completes standalone
north/south/east/west artwork. The [family index](../assets/galley-wall-v1/family.json)
maps facing, backing, exports and reviews; linked hashes and alpha channels pass.
South native review passes after backing and tap corrections. All four remain
uninstalled candidates awaiting owner review; ongoing production remains active.

## September 8 equipment and deposit audio

[Three cues](EQUIPMENT_DEPLETION_AUDIO_2026-09-08.md) confirm helmet sealing,
helmet removal and newly depleted nearby deposits. Completed-state observation,
cooldowns and silent restore priming prevent repeated feedback. Focused audio
tests and native mixer capture pass. WAVs are in `output/audio-equipment/`;
previous Windows packages are unchanged.

## September 8 east-facing galley candidate

The [east galley](../assets/galley-east-wall-v1/README.md) adds the opposite-facing
vertical view, with controls and taps toward the left. Full328-unit native review
and alpha export pass; placement and owner review remain. The neutral-registration
helper now records its actual thresholds without changing silhouette geometry.

## September 8 Reactor and Loom wall candidates

Two [wall banks](../assets/reactor-loom-wall-v1/README.md) add Reactor cooling/
shutdown cabinets and a Gravity Loom calibration bench. True-alpha exports and
native 320-unit scale reviews pass. Reactor V2 corrects reflective pipe/handle
detail; Loom uses varied supported working heights and muted ceramic parts.
The skill and bible record those lessons. Both remain standalone candidates;
room integration and the ongoing wall-asset production goal remain open.

## September 8 west-facing galley candidate

The [west galley](../assets/galley-west-wall-v1/README.md) adds newly drawn vertical
art with right-facing controls and fittings. Two directional failures are retained;
V3 passes standalone 328-unit height and alpha review. The review tool now uses
taller native panels for side banks. Owner acceptance and room placement remain.

## September 8 underwater, work and hazard audio

[Twelve new sounds](EXPANDED_AUDIO_2026-09-08.md) cover swimming/suits/bubbles,
active mining/salvage, galley/medical/lab/cultivation details and distinct
oxygen/power/hull warnings. Local activity and warning cooldowns stay bounded;
continuous ambience remains at nine layers. Focused integration, native spatial
checks and mixer capture pass. WAVs are in `output/audio-expanded/`; previous
Windows packages remain unchanged.

## September 8 galley wall and meal trolley candidates

The [galley asset handoff](../assets/galley-wall-v1/README.md) adds a warm fitted
food-service wall and separate small meal trolley. Both have transparent exports,
source/reference records and native scale reviews; neither is installed or owner
accepted yet. The review tool now fits portrait enlarged details while preserving
true display scale in native previews, verified with both new assets.

## September 8 power-room wall assets

Two [standalone wall banks](../assets/power-wall-v1/README.md) add Current Turbine
intake/controls/cable storage and Heat Recovery exchanger/manifold/pump storage.
Transparent exports and native material/scale boards pass. Heat's repeated coil
shine required a plate-fin revision; the pipeline records the lesson. These are
candidate assets, not installed room layouts or changes to live machines.

## September 8 laboratory wall candidate

The [laboratory wall](../assets/laboratory-wall-v1/README.md) adds a continuous
science bench with sample storage, analysis, specimen examination, preparation,
wash and sterilization bays. V2 reduces chamber reflections; source provenance,
true-alpha export and native 328-unit scale review are recorded. Standalone and
awaiting owner review. The workflow now explicitly rechecks alpha after edits,
because this material correction returned an opaque checkerboard.

## September 8 airlock and return sound

[Five cues](AIRLOCK_RETURN_AUDIO_2026-09-08.md) cover pressure adjustment, seal
release, chamber ready, recall acceptance and safe empty-handed return. Full-cycle
gameplay and silent checkpoint-restore checks pass. WAVs and native mix captures
are under `output/audio-airlock/`; an intermittent capture shutdown warning and
clean diagnostic repeat are documented. Earlier Windows packages are unchanged.

## September 8 fitted operations wall candidate

The [operations wall asset](../assets/operations-wall-v1/README.md) translates the
owner references into a continuous matte gray-olive instrument bank. Transparent
export and native 328-unit scale review pass; owner review remains. This is a
standalone asset, not installed room art or a change to existing layouts.


## September 8 fitted room reference direction

The owner supplied six [interior references](ROOM_REFERENCE_DIRECTION_2026-09-08.md)
and prefers wall-length installations for room character. Subsequent art should
use varied functional bays, tactile retro-industrial controls and restrained warm/cool
lighting, retaining matte materials, modest scale, inward faces and top-down geometry.
This is art direction; no bulk room restyle or gameplay change was performed.


## September 8 recovery and crew audio

[Three new cues](AUDIO_RECOVERY_2026-09-08.md) confirm stable hazard recovery,
successful crew dispatch and actual cryo emergence. Crew Foley no longer overlaps
another crew cue's tail. Focused audio, dispatch and recovery assertions pass;
native mixer capture is clean. A transient fixture shutdown warning and its clean
diagnostic rerun are recorded in the handoff. Prior Windows packages are unchanged.

## September 8 Airlock wall asset and matte-style workflow

The [Airlock wall-bank handoff](../assets/airlock-wall-v1/README.md) adds a standalone
suit, fitting-bench and breathing-air bank. V1 was rejected for reflective tanks
and helmet glass; targeted V2 is exported with true alpha and reviewed at room
scale. It is not installed; side-facing views or a split layout must respect the
pressure chamber and fitting station before integration.

Owner direction now explicitly requires matte materials and modest prop scale.
The room skill and visual bible include separate material/scale review gates,
a review template, a reusable native export/scale-board tool, and milestone-based
feedback into the maintained workflow. Changed skill files are synced to the
installed snapshot. This revision does not restyle other rooms or change gameplay.

## September 8 industrial UI switch assets

The [switch asset handoff](UI_SWITCH_ASSETS_2026-09-08.md) records four industrial
switch families with off/on/disabled states and 12 Godot atlas resources. These
are dark-backed menu assets ready for selection and integration; live menus are
unchanged. Transparent cutouts and dedicated hover/focus art are not included.

## September 8 sound variation pass

The [variation pass](AUDIO_VARIATION_2026-09-08.md) adds subtle pitch/level variation
to crew and selected mechanical cues, shared crew burst limiting and pitch-aware
tail cleanup. Focused tests and a native repeated-cue mix capture pass. Source
playback is updated; previous Windows packages and base WAVs are unchanged.

## September 8 missing audio cues created

[Ten new original sounds](MISSING_AUDIO_CREATED_2026-09-08.md) cover construction,
drone launch, expedition outcomes, nearby crew Foley, Cold Store and Salvage Workshop.
Real triggers, cooldowns, distance gating and nine bounded ambience layers are
integrated. Audio, paid-construction and native spatial checks pass; WAV previews
and mixer evidence are in `output/audio-missing-cues/`. Earlier packages are unchanged.

## September 8 Holographic Core wall artwork

The [Holographic Core handoff](HOLO_WALL_2026-09-08.md) adds optical processors
and projection-control wall banks in all four orientations. Main projector and
calibrator retained; native visual/placement, eight floor anchors and production
crew routes pass. The card is refreshed. Gameplay and existing packages are unchanged.


## September 8 audio coverage and third pass

The [audio inventory](AUDIO_COVERAGE_2026-09-08.md) records current coverage and
remaining construction, expedition and crew Foley gaps. Incoming comms and manual
Save now have restrained feedback; queued messages do not chatter. Mechanical
variants start at a random sample. Focused integration and native mixer checks
pass. This source pass is separate from earlier frozen Windows builds.

## September 8 Data Archive wall artwork

The [Data Archive handoff](ARCHIVE_WALL_2026-09-08.md) adds eight directional
wall sections with inward controls and flush backing rails. Native four-orientation
review, eight floor anchors and production crew routes pass. The existing room
keeps its library/terminal and gameplay behavior. Holographic Core is a next-art
candidate, not started. The [earlier fourteen-room rollout](WALL_ROOM_ROLLOUT_ACCEPTANCE_2026-09-08.md)
is complete in the checkout; packages retain their recorded snapshot scopes.


## September 8 Cold Store

Owner requested smaller, less shiny props. Matte V2 now uses charcoal panels,
subdued ochre and simpler pixel detail; live width is reduced by 25.8%. Native
card/room and clearance checks pass. See the Cold Store handoff for revision evidence.

The [Cold Store handoff](COLD_STORE_2026-09-08.md) adds a through-room with
refrigeration, ingredient weighing and stock-check visits. It adds 40 Food and
20 Biomass capacity, consumes 1 Power/cycle, and retains capacity during outages.
Connected Galley operation offers a hidden discovery. Paid connected construction,
crew routes, storage/discovery and native visual checks pass. The roster now has
47 identities. No standalone package was rebuilt for this addition.

## September 8 second audio mix pass

The [second mix pass](AUDIO_MIX_PASS_TWO_2026-09-08.md) preserves short UI cue
attacks, gently ducks ambience under priority sounds, and isolates music shuffle
randomness. Focused audio tests and a native stereo capture pass with no clipping
or dropped capture frames. These are source changes; previous Windows packages
remain frozen. Listening acceptance and a future package update remain separate.

## September 8 compact comms popup

The owner requested a smaller rectangular popup with only Next and X. This
supersedes the expanded conversation controls and floating inbox. Dialogue now
uses a 520x170 logical panel with a smaller portrait and disappears five seconds
after text completes; queued dialogue advances in order. A dedicated COMMS button
in the side panel reopens it. Native timer, queue, control-count and 1600/960
viewport checks pass. See [comms handoff](CREW_COMMS_HANDOFF_2026-09-08.md).

## September 8 audio Windows playtest

The [audio build handoff](AUDIO_PLAYTEST_BUILD_2026-09-08.md) records a fresh
Windows package at `output/audio-playtest-20260908/build/`. All six native package
checks pass, including positional sound, settings and normal gameplay save/quit.
Audio now drains before normal closing. Exported settings received visual review;
headphone/speaker listening remains with the owner. Earlier packages are unchanged.
This snapshot includes then-current room/editor work but does not establish full
acceptance of those concurrent changes; its manifest records the included files.

## September 8 tiled-floor Windows playtest

The verified package is `output/tiled-floor-playtest-20260908/build/BrineSpace.exe`.
Keep its PCK alongside it. Open Room Layout Studio → Research Lab or Corridor →
Floor tiles. Five exported checks pass, including floor editing/pixel comparison,
connected station/collision, editor workflow, menu/save recovery and music restart.
Packaging caught and fixed shared music playlist ownership. Quarantine uses its
previous complete production view in this snapshot; later checkout work remains
separate. See the [pilot report](TILED_FLOOR_PILOT_2026-09-08.md) for exact scope.

## September 8 Galley

The [Galley handoff](GALLEY_2026-09-08.md) adds a warm Crew room with a pantry,
stove/sink bank and serving counter. Cooking converts 1 stored Biomass, 1 Water
and 1 Power into 4 Food. Hungry crew take meal breaks; connected Hydroponics
offers a hidden discovery. Paid construction, economy, crew and native art checks
pass. The roster now has 46 identities. Standalone packages remain unchanged.

## September 8 Salvage Workshop

The [workshop handoff](SALVAGE_WORKSHOP_2026-09-08.md) adds a paid Engineering
room with workbench, parts shelves, repair press and crew tote deliveries.
It converts 3 stored Metal and 2 Power into 1 Rare Mineral per functioning cycle.
A connected salvage bay offers a hidden discovery using the existing three-cycle
stabilization rule. Native art, economy, paid construction and crew checks pass.
The room roster now contains 45 identities. No standalone package was rebuilt.

## September 8 tiled floor pilot

The [tiled floor pilot](TILED_FLOOR_PILOT_2026-09-08.md) adds cached floor meshes
and paint/fill/rectangle/variation tools to Research Lab and straight Corridor.
Default pixels and corridor clipping are verified; native editor, save/reload,
undo, connected-pair and collision checks pass. The edited-floor submission
microbenchmark improves by about 69%; no whole-game speedup is established.
Review it in the current checkout or the tiled-floor Windows package above.

## September 8 positional station sound

The [positional audio pass](POSITIONAL_AUDIO_2026-09-08.md) adds camera-relative
local sounds, saved Effects/Ambience controls, bounded room-character layers,
short music rests and small missing cues. Global warnings and the existing
polished assets remain. The handoff records source/native checks and listening
limits. Earlier frozen Windows packages are unchanged.

## September 8 game performance and regression pass

The [performance/polish report](GAME_PERFORMANCE_POLISH_2026-09-08.md) records
6.5–8.4% lower measured frame times in 50/100-room fixtures, saved-layout visual
refresh, native prop restoration on reset, and crew collision cache fixes.
19 final source fixtures and five exported gameplay/editor workflows pass.
The frozen Windows package is `output/game-polish-playtest-20260908/build/`.
Startup loads, with a remaining forced-shutdown audio resource warning; large
station overviews and first-frame rebuilds still need further optimization.
Concurrent edits after the source snapshot are outside its acceptance.

## September 8 Observation Room

The [Observation Room handoff](OBSERVATION_ROOM_2026-09-08.md) adds a paid Crew
blueprint with a giant north porthole, two side bookshelves and owner-requested
square corners. This version has a fixed south entrance and no resource output.
Native card/clearance checks, paid construction, Save/Continue and a crew return
route pass; three window sizes were captured. The live roster now has 44 identities.
The darker room now includes the wooden desk, rear-facing chair and lamp/open book.
All three crew alternate seated reading and window visits, with interruption and
snapshot restore checks. See [reading handoff](OBSERVATION_READING_2026-09-08.md).
No standalone package was rebuilt; owner visual review remains separate.

## September 8 music and sound polish

The [audio polish pass](AUDIO_POLISH_2026-09-08.md) matches music/loop loudness,
installs 15 shorter event edits, crossfades music, lowers it briefly for priority
cues and reduces repeated warnings. Source audio and station-system checks passed;
the handoff records mixer-capture evidence and listening limits. The existing
Windows playtest package predates these edits and remains unchanged.

## September 8 targeted Windows playtest package

The frozen local Windows debug package at
`C:/Users/Alex/Documents/Codex/2026-09-07/can/outputs/BrineSpace-Windows-Playtest`
passed six targeted native acceptance cases: title/architect selection, loading
and Continue, station systems/crew salvage/replay, save restoration, paid mining,
and paid salvage. Its README and evidence identify the exact snapshot and checks.
PCK SHA-256: `ab749328e96ad28bbe000b4a5070bd9a7aa41970dcce0496834201545b40a288`.
Final normal-entry startup also exited without engine errors. Headless paid checks
passed gameplay assertions but reported Ogg resources alive at shutdown; native
repeats were clean after explicit fixture music cleanup. Broader shutdown
reliability, subjective pacing and the owner-supplied audio mix still need review.
This is bounded acceptance of that package, not the older 21-case suite or later
checkout edits. No balance changes or online publication were performed.

## September 8 Suno audio integration

The [Suno audio handoff](SUNO_AUDIO_2026-09-08.md) records the owner's 27 supplied
exports: four Moonlit music tracks, station/ocean/airlock/drone loops and event
effects. A persistent playlist and saved music-volume control are integrated.
Original WAVs remain in Downloads. Focused source validation is separate from
in-game listening and packaged-build acceptance; the mix still needs owner review.

Guidance reconciled September 7, 2026 (Vancouver). Update this page at meaningful
owner decisions or acceptance milestones; keep detailed evidence in dated reports.

## Accepted direction

Restore a silent underwater station through satisfying placement and interdependent
systems. The underwater visual bible supersedes the old orbital setting.
Normal play uses paid construction, resource failures, hidden discoveries and three
functioning stabilization cycles. Starting doctrines, timed directives and scenario
victory are retired; Conclude Expedition ends the open loop. Do not restore them
from old balance notes. Preserve deliberately provisional systems unless the requested
change calls for revisiting them.

## Latest recorded integrated acceptance

The [September 7 build/playtest report](INTEGRATED_BUILD_PLAYTEST_2026-09-07.md)
records 21 automated acceptance runs on one frozen Windows debug package, repeated
whole-crew traces and a normal title-launch smoke check. It completes the combined
build and bounded packaged-test step that was still open in the
[September 6 handoff](BRINESPACE_HANDOFF_2026-09-06.md).

That result belongs to the package and source baseline identified in the report.
The checkout contains later/uncommitted work; the report is not blanket acceptance
of the current tree. Check the relevant diff before reusing its evidence. No new
build, gameplay test, release or publication was performed for this documentation update.

## Remaining work and next action

1. Play a short normal paid expedition from the recorded build. Focus on opening
   power/charging feedback, recovery choices and human pacing. Controlled tests found
   substantial one-generator charging waits; they do not establish a universal
   generator requirement or authorize an automatic balance change.
2. Review the new crew salvage expedition's pacing and sound mix in normal play.
   The September 8 systems pass connects chamber transit, exterior salvage and safe
   return; targeted packaged checks now pass, while human pacing review remains.
3. Complete continuous animation/art review, including provisional swim/helmet
   transitions. Headless checks and manifests do not establish visual approval.
4. Resolve larger-station performance (including 101-room scenarios), broader
   gamepad/display/hardware coverage and release-size optimization as relevant work
   is scheduled. These remain separate from the bounded debug-package acceptance.

The next useful step from the recorded acceptance is the human opening-power playtest.
A later owner request can change that priority; this page does not authorize unrelated
work or a new asset-generation batch.


## September 8 storage cleanup

The [storage handoff](STORAGE_CLEANUP_2026-09-08.md) records owner-authorized removal
of 215 temporary/rejected/older EXE/PCK files, totaling 157.26 GiB. Artwork, source,
Git, review evidence and current accepted builds were preserved. Historical
batch-two/room-rollout/production-ten binaries named in the removal log are no
longer locally replayable; their recorded test results remain historical evidence.
Export-tool automatic temp cleanup remains unimplemented. This was storage and
documentation maintenance, not new gameplay or visual acceptance.
