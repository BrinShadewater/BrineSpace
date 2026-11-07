# Wall room rollout acceptance

Updated: 2026-09-08. Project: BrineSpace. This report supersedes the incremental status entries in WALL_ROOM_ROLLOUT_2026-09-08.md.

## Objective and acceptance

Complete the original fourteen additional wall installations, including directional artwork, room integration, cards, retained functional equipment, floor hosts and native/crew verification. Improve the production tools, maintained skill and visual bible from observed failures.

## Accepted decisions and constraints

Nine continuous installations: Salvage Drone Bay, Construction Drone Bay, Anomaly Lab, Radio Lab, Shield Generator, Quarantine Cell, Med Center, Med Office and Biomass Digester. Five independently split installations: Life Support, Hydroponics Bay, Battery Array, Storage Bay and Command Center. Cross-room banks leave the central doorway open. Interfaces face crew space in the fixed top-down view. Preserve department materials and restrained lighting, actual source dimensions, original rasters and rejected versions. Wall mounting uses authored straight backing edges and canonical geometry; personal layout data is preserved.

## Current state

All fourteen are integrated through rooms/full-wall-v1 wrappers and registrations, scripts/grid_canvas.gd, scripts/room_card_art.gd and rooms/floor-profiles-v1/rooms.json. The rollout ledger records 55 source versions and selects the reviewed sources used by 74 registration files, including split-helper seed registrations. Source versions are not a room count. Fourteen cards are refreshed from the final native capture.

Retained equipment includes fleet vehicles/hatches, quarantine berth, medical treatment/imaging and consultation equipment, life-support tank/console, hydroponic harvest/nutrient equipment, battery controls, storage lift/cargo and command chart table/system controls. Life Support fans, Biomass status light and Command displays have source-relative operating feedback. Existing retained equipment keeps its baseline effects.

Pipeline additions include immutable source recording, independent split registration, full-scope binding audit, scoped native/floor/crew checks and draft/effect regressions. Lessons and rejected revisions are recorded in the visual bible and skills/brinespace-room-pipeline/references/wall-room-rollout.md; the installed reference is synchronized.

## Verification

| Requirement | Authoritative evidence |
| --- | --- |
| Original identities and source provenance | assets/wall-room-rollout-v1/rollout.json; tools/audit_wall_rollout_bindings.py; output/wall-rollout-final-bindings.json |
| Live room, floor and card bindings | Binding audit: 14 live rooms/cards, 74 registrations, 55 source versions; exact source hashes and image dimensions |
| Placement, doors, retained equipment | output/wall-rollout-final-native.log: 14 rooms x 4 orientations x 2 states; assertions cover counts, hull bounds, door lanes, relocated overlaps and required equipment |
| Visual camera, inward controls, palette and seams | Inspected output/wall-rollout-final/rooms-q0.png through rooms-q3.png; per-room source and native review records in ledger |
| Floor hosts and clearance | output/wall-rollout-final-anchors.log: 112 placements, zero missing; containment, routes, spacing and missing-host negative control |
| Crew movement | Every room's ledger routes/crew_routes log inspected: four rotated layouts and return journeys using production movement, zero errors |
| Saved-layout compatibility | output/wall-rollout-final-drafts.log: 56 orientations; invalid fallback, valid authored positions and unchanged stored data. Found and fixed missing validation on horizontal rollout banks |
| Shared side-art regression | output/wall-rollout-final-legacy.log: 20 variants, source hashes, library loading and draft compatibility |
| New operating effects | output/wall-rollout-final-effects-v3.log: Life Support, Biomass and Command x four orientations; cropped new-bank pixels change while operating, remain still offline, freeze/resume with owning game clock |

The first effect fixture captured an incorrect viewport; v3 restores dimensions after game initialization, hides fixture UI and releases nodes before shutdown. Its successful run has zero errors. Earlier failed logs remain diagnostic evidence, not acceptance.

## Next action and limits

The requested rollout is complete in the local checkout. No remaining production or verification work for these fourteen assets. Owner aesthetic feedback can be applied as a later revision. This is not an exported-build certification, a commit or a publish; none was requested. The scene fixtures isolate personal drafts and saves. Existing raw-image export warnings and unrelated prototype work are outside this acceptance scope.
