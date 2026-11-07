# Desalination Unit custom riser — October 19, 2026

The owner requested custom riser wall art to match the room's blue-green machinery.
The room now defaults to an opaque water-treatment wall: neutral cladding, teal
protected manifolds, pressure gauges, filter housings and a small droplet emblem.
No architectural windows are baked into the art. The central bay stays clear for
the separately drawn doorway.

## Source and integration

- Game atlas: `assets/desalination-unit-v1/riser-water-plant-v1.png`, 1024×178.
- Raw master and exact prompt: `assets/desalination-unit-v1/source/`.
- [Provenance and normalization](../assets/desalination-unit-v1/riser.provenance.json)
  record hashes, references, alpha probes and the independently sampled cap/face.
- One `desalination_unit` registration added in
  `assets/room-risers-v3/registrations.json`; all seven prior entries remain equal.
  The clinical family fallback and Studio **Room default** behavior are retained.
- Only this room's card was rebaked. No shared renderer, geometry, layout, prop
  registration, lighting or gameplay code changed in this pass.

The existing face remains 384×60 world units. Its 92-unit central reserve leaves
space around the independent 72-unit door aperture. Existing shared-neighbour
visibility hides the riser along an occupied north edge. Fittings are static art;
they add no animation, status simulation, recipe or resource behavior.

## Review and checks

**146 native checks /0 failures**, run
`output/test-runs/20261019-145205-native`. Coverage includes actual paid architect
construction, Water production, suspension, Save/Continue, all four crew routes,
Studio rotations, room-default source resolution, cap/face bounds and doorway
reserve. The initial fixture compared JSON floats with integer arrays; a focused
probe established equal geometry, and the fixture now compares numeric Rect2
values. Product art/registration did not change to resolve that fixture failure.

Agent reviewed the atlas, native room/card/Studio, four orientations and connected
north-neighbour captures. Owner visual acceptance remains separate.

- [Studio preview](../output/desalination-riser-20261019/studio.png)
- [Four orientations](../output/desalination-riser-20261019/orientations.png)
- [Connected north edge](../output/desalination-riser-20261019/connected-north.png)
- [Updated card](../assets/new-room-cards/desalination_unit.png)

All 18 protected source/art/library hashes match the before receipt; the signed
Windows ZIP's size/mtime are unchanged. The real profile retains 2,970 files with
no additions/removals; only the already-running game's `last_session.json`
changed. Tests and helper tools used isolated APPDATA. No player data was restored
or edited, and the running game was not restarted.

Local source only: no release export, signing, upload, Git publication or new
performance/platform acceptance. Receipts and the scoped handoff live in
`output/desalination-riser-20261019/`. Next is owner visual review, followed by any
separately requested packaged validation.
