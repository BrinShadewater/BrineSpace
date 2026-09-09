# Observation Room — squared installation

The owner's three-wall observation-library room: a giant round north porthole,
inward-facing bookshelves on both side walls, square outer corners and a clear
south entrance. V2 replaces the rounded V1 installation after owner feedback.

The room is integrated as `observation_room`, a Crew blueprint costing 6 Metal,
available to new neutral decks. It has a fixed north-facing orientation and no
resource production, ongoing cost or new crew bonus. These are conservative
implementation choices; the requested scope was the physical room and art.

`source-v3.png` is the selected unchanged 1254-square RGB generator output. It has
painted checkerboard, not alpha. `registration.json` excludes edge-connected
neutral background with vector polygons and splits the U into three independently
depth-sorted pieces. The renderer keeps the center transparent, the porthole
opaque, and the 72-unit south doorway authoritative. Ground footprints remain
separate from artwork. The floor reuses the habitation composite profile.

`card.png` is the native Godot room render. `manifest.json` records source/card
hashes. Exact built-in generation prompts and reference roles are in `prompts.md`.
The original rounded source and its registration are retained as rejected evidence.

Validation: `tools/review_observation_room.gd` passes native card rendering,
three-piece bounds, south access and shelf collision. `tests/test_observation_room.gd`
passes paid queued construction, unlocked deck membership, fixed entrance,
Save/Continue and 168 continuous production-controller movement samples into the
room and back. Native station captures at 1280x720, 1600x900 and 2560x1440 are in
`output/observation-room-v1/`; final log is `output/observation-room-gameplay-v3.log`
with zero script/engine errors. Earlier runs caught concurrent unrelated room
edits and are not acceptance evidence. Existing raw-image loader warnings remain.

Run Godot 4.6.1 with `--path . --script res://tools/review_observation_room.gd`
to rebake the card; use `res://tests/test_observation_room.gd` for the gameplay
fixture. Tests use isolated save/settings paths. Source PNGs are LFS-covered;
the existing raw export plugin includes this directory. No new standalone build
or packaged-source verification was performed. Rotatable variants, animated ocean
and gameplay bonuses are outside this version.

## Palette revision V3

Owner requested a slightly darker palette. Built-in image edit deepens timber, bronze and cabinetry while retaining the square installation and round ocean window. Native card visually reviewed; bounds, entrance and shelf collision pass (`output/observation-room-v3-art.log`). V2 card/source preserved. No gameplay changes or new standalone build.
