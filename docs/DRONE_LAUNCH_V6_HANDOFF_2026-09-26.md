# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Drone launch refinement v6

## Objective and acceptance
Align cable tops, retain pixel density, submerge the whole drone at contact, flatten Salvage water, and mount industrial yellow warning lights on surface rails.

## Accepted decisions and constraints
Charcoal steel/cyan machinery; amber warning lights are the authorized yellow exception. Mining drives on seabed, other drones swim. Drones disappear beneath base. Hatch closes after both launch and recovery.

## Current state
Desktop/BrineSpace Clean Prop Exports/drone-animation-bases: build_cycle_preview.py, salvage-water-pad-v6.png, industrial-beacon.png, manifest.json, launch-preview.html and launch-recovery-v6.mp4. Previous builder saved as build_cycle_preview_v5.py; old media preserved. Cable anchors fixed, braid tiled without length stretching; entire vehicle water-tints/fades together after contact. Render 2640×1150, 20 fps, 23 seconds. Bible and CURRENT_STATUS updated. No game changes.

## Verification
Contact and submersion stills visually reviewed. Renderer checks hidden-away state, hatch closure, and matching loop endpoints. Browser playback remains unverified following earlier denied browser access. Owner visual acceptance pending.

## Next action
Review v6 video. Final articulated sprite export and Godot integration are separate remaining work.
