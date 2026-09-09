# Power room expansion

Updated: 2026-09-08 · Project: BrineSpace · Task: Additional power rooms and opening access

## Objective and acceptance

Add Current Turbine, Biomass Digester and Heat Recovery Room, with distinct muted machinery, paid construction, useful placement conditions, discovery progression and reliable early access to another affordable generator.

## Accepted decisions and constraints

**Latest owner decision, September 8:** Restore the original brighter turbine. Its source, station selection and card are updated; the turbine no longer applies the extra 0.82 machinery tint. Native card review and all four rotation/state checks pass. The other rooms retain their existing treatment. Earlier muted-turbine station captures are historical.

- Owner approved the first three proposed power rooms and requested darker, less bright art. Other brainstorm candidates remain proposals.
- Current Turbine: starting blueprint, 4 Metal, 4 Power/cycle with a clear intake cell. Canonical intake points north and rotates clockwise with the room. Doors are east/west. Buildings, queued orders, uncleared wreck/rock, undepleted deposits and the map boundary obstruct it.
- Biomass Digester: 6 Metal + 2 Biomass to build; consumes 1 stored Biomass for 4 Power/cycle. Freshly produced Biomass is available next cycle. West/east/south doors.
- Heat Recovery: 6 Metal + 2 Data to build; 2 Power per cardinally adjacent functioning Reactor, capped at 4 per room. Shared walls suffice; no matching door requirement for heat transfer. Four doors.
- Opening hand remains Solar Array / Mining Drone Bay / Hydroponics Bay. The next offered card is Current Turbine, followed by Life Support and Corridor. Existing deck copies are staged, with no free construction or resource grants. Existing in-progress decks are preserved by Continue; start New Loop for the new opening order.
- Digester unlock: three functioning cycles of Current Turbine + Hydroponics. Heat Recovery unlock: three functioning cycles of Reactor + Mining Drone Bay. Hidden patterns remain concealed until functioning discovery. Digester + Hydroponics and Heat Recovery + Digester provide terminal patterns.

## Current state

Gameplay changes are in `scripts/room_database.gd`, `scripts/main.gd`, `scripts/run_manager.gd`, `scripts/synergy_manager.gd` and `scripts/station_ui_insights.gd`. Fuelled generators reserve their stored inputs before consumer allocation; no fuel is spent twice. Forecasts use the same operation checks. Cards and the resource inspector describe conditional recovery; turbine placement displays intake direction and blockage.

Station/card mappings are integrated in `scripts/grid_canvas.gd` and `scripts/room_card_art.gd`. New raw sprites, source revisions, exact generation prompts, three authored profiles, hashes, shared renderer and identity views live under `rooms/power-expansion-v1/`. Existing console and service-bench assets are reused with honest provenance. New scripts retain UID pairs. Raster paths resolve to the existing Git LFS filter; nothing was staged or committed.

Existing unrelated changes in the shared checkout are preserved. The room rollout ledger includes all three new identities; the catalog now contains 43 room identities.

## Verification

- Power mechanics: rotated intakes, rooms/queues/wrecks/deposits/boundaries, depletion, suspension, shared fuel, no same-cycle fuel, reactor adjacency/cap/isolation, nonmutating forecast and 100 opening seeds pass.
- Existing synergy, discovery, gameplay-polish, run-balance and station-operations suites pass. The foundation assertion was brought up to date with the previously added starting rooms plus Current Turbine. The operations fixture verifies the second generator on draw four and oxygen within six draws across 500 seeds.
- Native room review: three 512px cards, all 12 room/rotation combinations, canonical door masks, traversable port approaches, hull bounds, operating changes and offline freeze pass.
- Production crew movement through all three room identities at all four rotations passes with zero assertions (`output/power-current-routes-v2.log`). A focused wrapper selects Bill in the isolated fixture before the real core-wake sequence; the first inherited fixture attempt had incorrectly inherited the player's different selected architect and failed its setup assertion.
- Paid native playtest: all three new rooms built, both advanced discoveries earned, Bill awake and alive, at 256.5 simulated seconds / cycle 12. Paid costs and failures remain active. The advanced Reactor card is selected from the existing deck; earned prototypes are explicitly drawn. This is a controlled fixture, not a random-draft enjoyment or balance target.
- Disk Save/Continue preserves intake rotation and generation. Pause and native 1280×720, 1600×900 and 2560×1440 captures pass. Native cards and station overview were visually inspected.
- Three composition profiles pass declared texture/hash checks. Catalog/card/ledger reconciliation passes for 43 identities.

Evidence: `output/power-rooms/`, `output/power-*.log`, and the asset manifest. Prior failed fixture evidence exposed a placement on an authored basalt cell; the fixture was corrected to build on available space. A capture-only fixture was then improved to advance the real crew/process path, explicitly verifying Bill's survival.

## Next action

Ready for owner playtesting in a New Loop. Tune costs/output/intake feel from that feedback. No new Windows export was produced; raw files are beneath the existing `rooms` export root, but a fresh packaged-runtime acceptance pass remains separate from checkout/native validation. No other brainstorm rooms were implemented.

## Larger machinery follow-up - 2026-09-08

Owner requested all three machines be larger. Updated `rooms/power-expansion-v1/power_room_view.gd`, three composition profiles and regenerated cards: turbine width 144 to 250, digester 144 to 220, heat recovery 144 to 270. Moved the console and service bench behind the machines, preserving the brighter turbine. Updated manifest hashes and rollout records. Room grid size and gameplay are unchanged.

`tools/review_power_rooms.gd` now checks navigable detours instead of requiring straight paths through the enlarged skids. All 12 native rotation/state checks pass; real production crew traversal passes with zero assertions (`output/power-large-routes.log`). Paid station preview, discovery, Save/Continue and pause pass (`output/power-large-preview.log`). Visually inspected all three cards and focused station captures in `output/power-room-preview-large-v1/`. Ready for owner scale feedback; packaged build remains pending.

Turbine brightness follow-up (2026-09-08): reduced only turbine machinery modulation from 1.00 to 0.90, retaining its source and larger size. Updated shared view, baked card and manifest. Native rotation/state checks and paid preview pass; card and station capture visually reviewed at `output/power-room-preview-soft-v1/current_turbine.png`. Ready for owner visual feedback.

Turbine brightness follow-up: owner requested another 10% reduction; renderer modulation is now 0.81 (0.90 x 0.90). Card rebuilt and visually reviewed; station machinery reviewed in `output/power-room-preview-soft-v2/current_turbine.png`. Native state/rotation checks pass on isolated rerun after concurrent capture failed an operating-cue assertion. Paid preview passes.

Turbine south-wall placement (2026-09-08): owner requested machinery at far south given east/west doors. Skid now ends at y172 for those rotations; north/south door rotations retain rear access. Registered visible source region (18,260,1218,652) excludes faint alpha padding without editing source; rotor anchor adjusted. Brightness remains 0.81. View, card and manifest updated. Native card reviewed; 12 rotation/state checks and real turbine crew routes pass (`output/power-turbine-south-routes.log`). Ready for owner placement feedback.
