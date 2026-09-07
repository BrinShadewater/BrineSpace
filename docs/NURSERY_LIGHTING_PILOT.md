# Nursery lighting and moving-part prototype

Isolated native scene: `rooms/whole-room/nursery_lighting_pilot.tscn`.
Controls: P electrical power, O machine operation, R layout rotation, Space pause,
WASD/arrows crew. No player saves, simulation or existing room PNGs are changed.

The room-pipeline separation is implemented as a subclass of the accepted
south-facing assembly. One procedural wall fixture has a housing, independent
lens and floor pool. Its anchor rotates around the wall, away from centered
sockets; horizontal/vertical housings remain screen-upright. The bounded pool is
drawn below machinery and clipped to the interior. It cannot spill through walls.
A separate four-blade fan with fixed housing and status lens follows the filter's
registered position, inside its visible silhouette. These are technical fixture
assets, not final generated sconce/fan art or department-finish approval.

Electrical power and machine enablement are separate. Powered-idle retains light;
unpowered stops machinery immediately and fades ambient lighting over 0.65 seconds.
Low ambient keeps crew readable. Pause freezes machinery, crew and the fade.
There is no emergency battery gameplay, dynamic shadow casting, wall reflection,
normal mapping or cross-door light spill. The ambient overlay covers the complete
isolated room; it is NOT ready to overlay shared walls in the station renderer.
Older source art still contains painted indicators/screen marks that a later
non-emissive-base pass must separate; this pilot does not erase them.

Reproduce with Godot `--path . --script res://tests/playtest_nursery_lighting.gd`.
The script refuses to overwrite evidence. Native captures cover four rotations,
three states, intermediate fading and paused pairs. Tests exercise fan envelope,
operation-clock and pixel changes, idle/offline stillness, pause and offline crew.
Evidence: `output/whole-room-pilot-01/lighting-pilot-v2/` and
`output/whole-room-pilot-01/lighting-pilot-v2.log`.

Before main-game rollout: approve final fixture appearance, separate actual
electrical availability from the existing functioning flag, integrate light
ordering with shared-edge ownership, and test mixed-power neighbors at station
zoom. Do not infer that this isolated visual experiment completes that work.
