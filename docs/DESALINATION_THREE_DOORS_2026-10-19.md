# Desalination Unit: three doors — October 19, 2026

Owner requested a three-door room. Desalination now uses the existing tee layout:
**west, east and south doors**, with the **north wall reserved for the ocean intake**.
All four sides rotate together. The room remains one cell, 5 Metal and 2 Power for
2 Water per functioning cycle; intake, pump, suspension and failure rules remain.

## Integration

- `scripts/room_database.gd`: only Desalination's layout changes, from dead-end to tee.
- `rooms/desalination-unit-v1/view.gd`: matching three-port shell in gameplay/Studio.
- `rooms/full-wall-v1/default-layouts.json`: only four Desalination records change;
  equipment occupies the sealed side and corners, leaving all three routes clear.
- `assets/new-room-cards/desalination_unit.png`: one card rebaked from the live view.
- The existing custom riser, palette, shared geometry, lighting and original art stay
  intact. No new raster generation was needed.

## Verification

**51 gameplay checks /0 failures**, `output/test-runs/20261019-150141-headless`:
three rotated ports, sole-neighbour placement through each of 12 entrances, rejection
on each intake side, actual paid build queue, production/Power, suspension, pumps,
blocked intakes and storage capacity. A red run first demonstrated the missing
three-door definition; final checks pass after integration.

**898 native checks /0 failures**, `output/test-runs/20261019-150219-native`:
real paid architect construction, economy, staged Save/Continue, native inspector,
all 12 rotated entrances and all three neighbour-to-neighbour pairs per rotation,
individual route-segment clearance, Studio geometry and prior riser contracts.
Scoped layout lint: **four orientations /zero findings**. One card bake passed.

Agent visually reviewed the [Studio](../output/desalination-three-doors-20261019/studio.png),
[four rotations](../output/desalination-three-doors-20261019/orientations.png),
[connected station](../output/desalination-three-doors-20261019/connected-north.png)
and updated card. Owner visual acceptance remains separate.

All tests/helpers used isolated APPDATA. All 16 protected hashes match, all other
authored layout records match, and the signed ZIP's size/mtime match. Owner profile
retains 2,970 files with no additions/removals; only active-game `last_session.json`
changed. Owner layouts were not reset and the running game was not restarted.

Local source only; no release export, signing, upload, Git publication or new
performance/platform acceptance. Full logs, hashes and handoff:
`output/desalination-three-doors-20261019/`. Packaged and pacing validation remain
separate from this geometry change.
