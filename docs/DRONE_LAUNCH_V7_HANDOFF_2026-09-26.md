# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Drone preview v7

## Objective and acceptance
Smooth submersion, enlarge Construction, center faster circular beacons, animate Construction screen, and add drone status lights.

## Accepted decisions and constraints
Blue = operational; red = stopped; yellow = out of power or charging. Yellow/amber lights remain exceptions to gray/cyan machine paint. Whole vehicle submerges together. Preserve level Salvage water and attached cables. No runtime installation.

## Current state
Desktop/BrineSpace Clean Prop Exports/drone-animation-bases contains updated build_cycle_preview.py, launch-recovery-v7.mp4, drone-status-light.png, manifest.json, v7-provenance.json, v7-check stills and launch-preview.html. Previous builder saved as build_cycle_preview_v6.py. Construction is about 50% wider than v6; all beacons now center side rails and rotate in 0.8 seconds. Screen has radar sweep and telemetry. Preview demonstrates stopped before launch, operational through recovery, charging after recovery. Submersion takes 3.35 seconds with smooth attenuation and slight depth blur. 2640×1150, 30 fps, 23 seconds.

## Verification
Reviewed parked and underwater stills for scale, screen fit, beacon placement, and status lights. Renderer retains hidden-away and hatch-closure assertions. Video decode checked after export. Browser playback unverified; owner visual acceptance pending. Mechanical endpoints match, while status colors intentionally change for demonstration.

## Next action
Owner review of v7; final articulated animation and Godot wiring remain separate.
