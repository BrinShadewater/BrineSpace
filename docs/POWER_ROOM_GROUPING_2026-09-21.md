# Power-room grouping review

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Group large and medium power equipment into believable service areas. Preserve
door access, directional turbine machinery and the owner's protected rooms.
Geometry checks and agent visual review do not establish owner acceptance.

## Current state
Installed selection: `output/power-rotation-review-2026-09-21/candidate-r4.json`.
Eight entries changed in `rooms/full-wall-v1/default-layouts.json` and the player's
`user://room_layouts.json`. Guarded against concurrent edits to the target keys;
all other layout keys preserved. Both `assets/room-cards-v2` power-room PNGs refreshed
and visually reviewed; LFS filters verified. Source pixels and registry unchanged.
R1 removed loose gauges/valves but left Heat Recovery sparse. R2 paired its process
module and cabinet at y=-100, blocking west access. R3 moves that pair to y=-135,
preserving the exchanger at its previous candidate position. R4 also groups the
Turbine transformer with its medium controls, with quarter-specific positions.
Previous candidates, native images, reports and logs remain beside the candidate.

## Verification
R2: eight native views, 1280 walking samples, four west-door failures; rejected.
R3 and R4: each eight native views, 1280 walking samples, zero failures.
Visually inspected all R4 views and both installed cards. The live station fixture
shows both rooms at two zoom levels with isolated saves and synthetic funding;
native focused crops reviewed. This is not a balance or ordinary-expedition test.
Both machines pass four-quarter operating/offline/held-clock pixel checks; these
verify existing feedback, not every decorative lamp or actual station pause.
Installed defaults and installed saved layouts each pass eight views/1280 samples.
Sixteen decoded RGBA comparisons against R4 have zero mismatches (`parity.json`).
The grouped equipment reads more coherently than the isolated r1 supports.
Heat remains relatively sparse; do not claim finished furnishing from route results.

## Next action
Owner visual acceptance remains open. Owner room keys and library marks remain
protected. Release refresh is still pending
for the later Bill work repairs and door-edge optimization as well as any future
selected room changes.
