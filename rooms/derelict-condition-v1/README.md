# Derelict condition layer

Owner correction: floor, wall and prop surfaces must also be weathered. The
condition now includes `scripts/derelict_material.gdshader`, confined to uncleared
rooms. Source-attached grime, pitting and exposed oxide preserve alpha and stop
at restoration. The raster below remains unchanged. Native shader and restored
pixel parity evidence: `docs/DERELICT_CONDITION_2026-09-12.md`.

September 12, 2026. Medical cryo/charging and companion recovery compartments
retain their existing departments, furniture, occupants and door geometry.
Abandonment is a separate visual condition: sediment, biofouling, broken grates,
deck fragments and disconnected cables beneath equipment, plus restrained hull
corrosion on actual wall segments. Cleared rooms omit the condition entirely.

`floor-decay.png` is the unchanged built-in imagegen output, actually 1254 square
RGBA (requested 1024); no cleanup, recolor or pixel editing. Native registration
is a 352-square room-local rectangle centered on the floor. It has true alpha,
including the central crossing. Exact prompt: `prompt.txt`; hash/alpha evidence:
`manifest.json`. The initial procedural floor candidate was rejected during native
review for flat geometric shapes and replaced before delivery.

Runtime: `scripts/derelict_condition.gd`, selected only while drawing uncleared
recovery rooms in `scripts/grid_canvas.gd`. Shared whole-room floor/world hooks
place decay below furniture and corrosion over existing wall strips. No new
collision, time, save data or gameplay randomness. Cards represent restored
blueprints and retain their original art. Raw export already includes rooms/;
no executable was rebuilt or verified for this change.

Native fixture: `tests/playtest_derelict_condition.gd`; captures in
`output/derelict-condition/after/`. The restored views are explicit visual fixture
setup; paid restoration and persistence are tested by the existing recovery suites.
