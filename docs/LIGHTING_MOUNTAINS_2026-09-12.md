# Lighting and excavatable mountains

Updated: 2026-09-12 · Project: BrineSpace · Source implementation

## Objective and acceptance

Foundation for connected mountains that can be excavated into and thick underwater darkness lit by the station, divers and drones. Enemies and predator attraction are explicitly deferred.

## Accepted decisions and constraints

Light is a core game concept. Exterior and interior switches remain separate; divers and drones carry their own lights. Occupied interiors remain readable. Rock interrupts exterior light, and survey memory persists after a light leaves. Keep normal construction costs, drilling time, battery/recharge, cargo delivery and the shared clearance job.

## Current state

- New loops extend the existing connected basalt renderer with two broad mountain masses. The west formation contains a sealed engineering-wreck pocket. Excavation opens sections one cell at a time; exposed sections can be reached across open water, without extending the station to each cut. The drone fleet still checks its actual bay route before dispatch. The hidden pocket uses the existing salvage content and becomes identifiable when an adjacent section opens.
- Exterior fog uses a world-space 2D shader with directional beams, strong distance attenuation, drifting haze, fine suspended texture and terrain shadows. This approximates scattered underwater light; it is not a 3D volumetric simulation. Up to 48 nearby sources render. Station sources follow power allocation and the exterior switch, with the existing core starter exception. Diver beams follow facing; drones have work beams and navigation lamps. Drilling is rendered at the rock face and creates silt that fades over six visual seconds.
- Surveyed water and first exposed rock faces remain faintly mapped. Survey is stored separately from current light, validated on checkpoint read/restore, and starts empty for old saves. Existing saved terrain is never replaced by the new formations. Transient silt resets for New Loop and Continue.
- No new raster sources, enemies, export, commit or push.

Changed in this pass: `scripts/underwater_visibility.gd`, `scripts/underwater_fog.gdshader` and UIDs; targeted integration in `grid_canvas.gd`, `main.gd`, `wreck_field.gd`, `run_save.gd`, `station_hardware.gd`; rock/wreck renderer visibility; two new native fixtures, rock regression updates and the `underwater` test group in `tests/index.json`. Existing unrelated working-tree changes were preserved.

## Verification

- `output/underwater-native-final.log`: foundation PASS, including sequential cuts, enclosed-target rejection, buried-pocket reveal, station switching, diver/drone sources, exposed-face survey and checkpoint capture. Native captures in `output/underwater-foundation/` reviewed for station on/off, diver tunnel, drill/silt and faint surveyed mountain. Controlled fixture positions the diver/drone for these views; it is not a complete expedition playthrough.
- `output/underwater-shader.log`: native pixel checks PASS for directional light, blocked/unblocked rock shadow, frozen clock, moving haze and dim survey memory.
- `output/test-runs/20260912-144619-headless/`: paid rock clearance PASS, including 16 neighbor masks, connected boundaries, pause, real drone work/cargo, checkpoint survey restoration and paid rebuild.
- `output/test-runs/20260912-144202-headless/`: drone fleet and full save suite PASS.
- `output/test-runs/20260912-144758-native/`: station hardware PASS, including switches, power, save/restore and two-size UI checks.

Run the focused group with `python tools/run_tests.py --subsystem underwater` and its native lane with `--native`. Native rendering checks do not establish packaged acceptance.

## Next action

Owner playtest in a new loop to judge darkness density, beam reach and excavation pacing. Actual enemies remain on the back burner. Broader cave contents and specialized mountain resources can build on this foundation later.

## Accepted future map generation direction

Owner approved partial procedural generation on September 12: procedural layouts assembled from authored pieces, with a viable BRINE starting area, expansion space and reachable early resources. Vary mountain shapes/thickness, tunnels, sealed cavities, buried derelicts/deposits and regional geology/water clarity. Save a reproducible expedition seed and preserve excavation/discovery state. Keep the authored map as a testing ground; introduce generation after lighting and excavation feel good in play. This records future direction only; generation is not implemented in this pass.
