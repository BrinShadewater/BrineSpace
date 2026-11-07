# Early Water: Desalination Unit — October 19, 2026

**Later art revision:** the owner requested a recoloured membrane machine and
more room character. The current room has five equipment props, service details
and a blue-green membrane skid; see [art revision](DESALINATION_ART_POLISH_2026-10-19.md).
The initial four-prop evidence below retains its original scope.

The owner reported early Water shortages and approved a simple common
Desalination Unit. It gives an early deliberate Water supply while retaining
Power and placement decisions.

## Accepted behavior

- Starting Life Support blueprint, one cell, costs **5 Metal** and no Data.
- Each functioning cycle converts **2 Power into 2 Water**, capped by storage.
- **North intake / south door**, rotating together. An obstructed intake stops
  output and draws no Power, including in the blackout demand calculation.
- Pumps off, master power off, suspension and normal resource/hazard rules apply.
- An existing deck copy is staged seventh: **Solar → Mining → Hydroponics →
  Current Turbine → Salvage → Life Support → Desalination → Corridor**. Copy
  counts, draw-on-build, prices, reroll charges and unlock purchases remain normal.
- **New loops begin with 4 Water** before existing research bonuses. Continue
  keeps its saved quantities and deck; it does not retrofit starter supplies or
  rewrite a checkpoint's offered cards.

The existing Tidal Condenser and Water Reclamation blueprints retain their
behavior. No new synergy recipes, general Power subsidy or free-building mode
was introduced.

## Implementation and presentation

Room definition and starting unlock live in `scripts/room_database.gd`. The main
loop sets starter Water, stages the blueprint, evaluates the intake in forecast
and actual economy, and presents placement/blueprint guidance. The inspector
reports the rotated intake, its obstruction and operating requirement. BRINE's
specific line is: “Salt remains outside. I have declined to inventory it.”

[Room artwork and provenance](../rooms/desalination-unit-v1/README.md) use four
existing painted props, the shared clinical shell and four new default layouts.
The station view, actual Studio picker and baked card all use this renderer.
Existing authored layouts and owner overrides were not replaced.

## Validation and evidence

Six focused fixtures pass: Desalination gameplay, native Desalination integration,
Salvage opening, discovery progression, station operations and existing condenser
gameplay. The native fixture has **139 checks / 0 failures**: actual architect
completion after paid placement, Water production, inspector controls, suspension
and resume, checkpoint write/read and staged Continue, all four crew-graph door
routes, four live equipment layouts, and the actual Studio picker/rotations.
Opening sampling includes **500 expanded-deck seeds**, plus 32 fresh and 32
expanded seeds in the opening fixture. This is offer consistency, not a survival
or pacing acceptance test. Scoped layout lint checks four orientations with
**zero findings**. One card was baked; no unrelated asset batch ran.

Evidence: `output/desalination-unit-20261019/FINAL.json` and `HANDOFF.md` include
exact test runs and preservation checks. Visual review covers the actual
[station](../output/desalination-unit-20261019/station.png),
[Studio](../output/desalination-unit-20261019/studio.png),
[four orientations](../output/desalination-unit-20261019/orientations.png) and
[card](../assets/new-room-cards/desalination_unit.png). Initial native fixture
failures came from deleting generated recovery wards in the test setup, inline
resource-icon spacing, and freeing a RefCounted actor; these fixture mistakes
were corrected rather than weakening production Save validation.

Tests/probes used isolated APPDATA. The owner's already-running game remains
open. No new release was exported, signed or uploaded; the existing signed ZIP
does not contain this source addition. Human visual/pacing review and relevant
packaged regression checks are the next validation before release.
