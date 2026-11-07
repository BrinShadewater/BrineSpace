# Lighting and shadows first pass

Updated: 2026-09-08. Project: BrineSpace.

## Objective and acceptance
Add visible shadows and lighting to the station while preserving readable machinery and circulation. Owner visual acceptance remains pending.

## Accepted decisions and constraints
Keep the muted machinery palette, power-aware lighting, pause behavior, existing layouts and gameplay. This is a first pass of deck contact shadows and fixture light pools, not dynamic silhouette occlusion.

## Current state
Changed rooms/whole-room/room_lighting.gd: fixture pools extend 112 units instead of 56, with restrained fading intensity. Both batched and reference rendering paths match. Added three-band footprint contact shadows clipped to the room interior.
Changed scripts/grid_canvas.gd: shared detailed-room floor pass draws equipment shadows before machinery and crew. Existing retained floor surfaces cache these draws. Narrow corridors retain their existing specialized lighting. No source images or room geometry changed.

## Verification
Native light-pool parity passes (maximum byte difference 1). Native station lighting assertions for rotations, neighbors, input starvation, power fade and pause report no lighting failures. The inherited broader fixture fails 29 checks involving nursery animation, footprint overlap and four-room movement; these are unresolved, and this is not a clean full-suite result. Evidence: output/atmosphere-station.log and output/atmosphere-station-v1/.
Paid native gameplay preview passes at cycle 12, including discoveries, construction, crew survival, Save/Continue and pause. Visually reviewed powered station and focused turbine capture: output/atmosphere-preview-v1/current_turbine.png. No packaged build produced.

## Next action
Owner review of effect strength. Investigate broader fixture failures separately before claiming full station acceptance.
