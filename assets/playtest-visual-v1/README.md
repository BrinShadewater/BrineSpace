# Playtest visual refinement — 2026-09-07

Generated with the built-in image generator. Original sources are retained here, with no raster post-processing. Runtime texture registration and animation live in Godot.

- `switch-source.png`: generated industrial housing. `scripts/industrial_room_switch.gd` animates the rocker over 0.18 seconds and provides real room ON/OFF control, preserving Button keyboard/focus behavior and existing salvage/repair actions.
- `deck-source.png`: generated quiet steel deck, mixed with each department's existing floor tint in `room_floor.gd`.
- `door-source.png`: generated closed low cutaway pressure door. `department_door.gd` registers leaf surface regions and clips their existing mechanical sliding motion. Canonical 72-unit aperture and collision are unchanged.
- `pressure-source.png`: refined U-shaped machinery. The generator returned an opaque checkerboard, so explicit equipment-only source rectangles exclude the aisle and exterior in `pressure_control_view.gd`.
- `pressure-alpha-attempt.png`: rejected transparency repair; its center still contains a painted checkerboard. Not used by the runtime.

Pressure refinement source regions: top (70,12,1114,600), left (70,612,256,637), right (928,612,256,637). These are texture registrations, not new collision footprints. The q0 machinery layout is the existing authored exception; other rotations retain their separately registered furniture.

The live checkout also contains a concurrently developed full-wall Pressure Control variant that replaces its top machinery. Its selection must be reconciled with the owner's focal-design preference before claiming the gauge is visible in that variant.

Native evidence: `output/playtest-visual-v1/`, including switch transition frames and a pixel-equal drone-under-hull/no-drone pair. `tests/playtest_visual_refinement.gd` reproduces those checks with isolated save paths. The baseline September 7 Windows executable has not been overwritten.
