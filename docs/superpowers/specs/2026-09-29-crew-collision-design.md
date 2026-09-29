# Crew collision: spacing between crew

Date: 2026-09-29. Status: draft for owner review. Origin: owner playtest note, Sept 28 ("Players need to
walk around door frames, character collision should be a thing"; on follow-up: "both, and props").

## Intent

Crew and companions should never visibly overlap each other while they walk. When two of them meet, the
one who cannot pass waits or detours, as they already do. The owner chose "spacing plus waiting" over
"sliding past" (steering around each other while moving).

Door frames and props are covered separately and are already shipped (commit e90cdece: crew keep 16 units
off walls and door frames, 11 off props). This spec covers crew-to-crew spacing only.

## What exists today

- `scripts/bill_npc.gd` is the walking actor for all four crew (and companions reuse its avoidance).
  `CREW_CLEARANCE := 20.0` is the minimum centre-to-centre distance between two actors.
- `crew_clear(a, b)` stops a step that would bring an actor inside that distance; `move()` then reports
  "waiting for passage", retries a detour every 0.5 s and gives up after 3 s.
- `detour_around_crew()` searches for a route that keeps 32 units from every peer.
- `scripts/crew_passage.gd` resolves stand-offs: one actor steps aside if the other has waited 0.3 s and
  they are within 48 units.
- Peers are collected each frame in `scripts/main.gd` (crew) and `scripts/companions.gd` / `architects.gd`.

## Measurements (2026-09-29)

- A standing crew sprite is about 29 units wide and up to about 45 units mid-stride (65.28 units tall, in
  the 384-unit cell). Measured from the runtime-matte frame packs for Bill, Veld and Branforth.
- At `CREW_CLEARANCE` 20, two crew can overlap by 9 to 25 units.
- Soak on the owner's 6-crew station (`expedition-73-progressed-known-recipe-final/latest.loop`, 120
  cycles, 2,400 frames, 0.05 s steps):

| Clearance | Frames with a pair closer than 29 | Closest centre distance | Waiting actor-frames |
|---|---|---|---|
| 20 | 44 (1.8%) | 20.3 | 48 |
| 30 | 0 | 30.2 | 56 |

- Crew processing time did not change (0.475 ms per frame at 20, 0.459 ms at 30).
- With 30, these pass: `test_station_navigation`, `test_npc_segment_clearance`,
  `test_production_ten_walker_paths`, `test_bill_npc`, `test_veld_walk_integration`,
  `test_crew_social`, `test_crew_medium`, `test_battery_passage_probe`, `test_parts_passage`,
  `test_procedural_route`, `test_navigation_segment_parity`, `test_reactor_route_segment`.

## Design

1. Raise `CREW_CLEARANCE` from 20.0 to 30.0, with a comment naming the sprite widths it is based on.
   The other values already sit above it: detour padding is 32, stand-off range is 48. If a later
   change lowers detour padding below the clearance, detours would plan routes that `crew_clear` then
   refuses, so keep detour padding at or above the clearance.
2. Add `tests/test_crew_spacing.gd`: two crew start on opposite sides of a doorway and walk to each
   other's side. Assert (a) the distance between them never drops below 29 on any frame, and (b) both
   arrive within a set number of seconds. Register it in `tests/index.json` (crew subsystem).
3. No change to route planning, the graph, `crew_passage.gd`, or how peers are collected.

## Not in scope

- Sliding or steering around each other while moving.
- Clearance that depends on each character's measured width.
- Drones: they fly and are not in the crew peer list.
- Re-spacing furniture so props can take more padding (the five rooms whose doorways fail above 11:
  battery array, storage bay, maintenance bay, ore refinery, research lab).

## Risks and checks

- More brief waits at doors and in tight corridors. Watch `stuck_watch` warnings and "waiting for passage"
  counts in a soak; the measured cost was about 8 extra waiting frames per 120 cycles.
- A rare gridlock in a crowded doorway that 120 cycles did not show. Mitigation: `traffic_wait > 3.0`
  already abandons a blocked goal, and `crew_passage.gd` already makes an idle actor step aside.
- Josh (tracked companion) may be wider than crew. Measure his frames before shipping; if he is, keep
  30 for crew pairs and consider a per-actor extra for him as a follow-up.
- Verification before commit: the test list above, the new spacing test, `tools/soak_test.gd` on the
  6-crew station, and a repeat of the 120-cycle gap measurement showing zero pairs under 29.

## Open questions

- None blocking. Owner to confirm 30 (versus 32, which would match detour padding exactly).
