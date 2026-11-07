# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: industrial menu switch assets

## Objective and acceptance

Create switches and variations matching the existing menu theme, ready for later use. Menu replacement was not requested.

## Accepted decisions and constraints

Dark teal/blue-black panel housings, restrained steel edges and muted sage/amber indicators. Four families: sliding toggle, rocker, lever and pushbutton. Each has off/on/disabled states, with no baked labels. Raster sources use Git LFS.

## Current state

`brineui/industrial-switches-v1/` contains the production atlas, 12 .tres AtlasTexture regions, manifest/hash, README and exact prompts. Built-in image_gen created the atlas and corrected its background. The first checkerboard-backed source is retained as rejected; the final source is opaque dark-backed, not transparent. No script altered source pixels. Small mechanical differences between generated states remain; this is not a pixel-identical housing animation pack.

## Verification

Read-only image inspection confirms 1086x1448 RGB. `tests/review_industrial_switches.gd` loads all 12 textures and validates atlas bounds, then produces a native review at output/industrial-switches/review.png. Source appearance and menu-scale review are separate from owner approval. No gameplay tests are required for this unused asset pack.

## Next action

Owner select preferred switch families, then integrate them in appropriate menu controls with labels and keyboard focus. Transparent cutouts and authored hover/focus states are not included.


## Integrated hardware review lessons
The approved mockup now runs through `hardware_panel.gd`. Keep short one-line labels at sidebar scale (full names in tooltips); native minimum-window review caught excessive multiline spacing. Endpoint fades plus press travel provide feedback without claiming articulated mechanical animation. Keep global hardware state separate from per-room suspension, validate optional save fields before mutation, and render station spray above retained room contents. See `STATION_HARDWARE_2026-09-08.md` for behavior and test evidence.
