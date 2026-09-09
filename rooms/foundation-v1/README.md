# South-edge station foundations

Generated 2026-09-08 using built-in imagegen; exact prompt and immutable raw hash recorded beside this file. One reusable modular foundation asset: dark steel fascia, two braced piles, mineral-encrusted seabed feet. Source transparency verified; no pixel edits.

Integrated in grid_canvas.gd below room floors/walls. A room with an occupied south neighbor has no exposed foundation. Supports stay screen-south regardless of door rotation. Narrow corridors use a smaller support module. Static floor cache handles changes with station occupancy. No collision, resource costs or room-card changes: this is exterior station scenery.

Native paid gameplay preview passes construction/discovery/crew/Save/Continue/pause; source and station renders visually inspected. Evidence: output/foundation-preview-v2/. No fresh packaged build. Owner visual acceptance pending.

South rock occlusion follow-up: solid uncleared rocks/wrecks directly south now conceal foundations. The static surface key includes south blockage, so clearance reveals supports without requiring camera movement. Native screenshot reviewed in output/foundation-preview-v3/heat_recovery.png; paid preview and clearance-cache assertion evidence in output/foundation-occlusion.log.

Terrain variants (2026-09-08): added three true-alpha generated sources with exact prompts and hashes: broad silt mud mats; reef-rock feet with low marine growth; heavy mineral-crusted basalt anchors. Original rock feet serve manganese nodules. grid_canvas.gd selects at room center from actual sub-biome coverage, then ash/clay/sand overrides in ground-layer order (coverage threshold 0.5). Default seabed and brine flats use silt. Existing solid south-neighbor occlusion remains. Textures cache by variant; no per-frame image loading.

Native source alpha/dimensions checked; seven terrain selection assertions pass. Paid gameplay runs before isolated reef/mineral visual specimens are injected: these two specimens are not claimed as paid builds. All three in-terrain captures visually reviewed in output/foundation-terrain-v1/. Native log output/foundation-terrain.log passes. No exported build; owner art feedback remains next.

Derelict/blocker extension (2026-09-08): exposed uncleared wrecks, cryo derelicts and basalt blockers now draw terrain-selected foundations on the environment layer before their own art. Occupied or solid south neighbors conceal supports; cleared and rebuilt cells are excluded to avoid duplicates. Basalt foundations use 0.86 cell width and an inset 0.83-cell attachment height to tuck behind irregular edges. Native paid preview and exposed/stacked/cleared-south assertions pass; derelict and rock captures reviewed in output/foundation-exterior-v2/. Code: scripts/grid_canvas.gd. No packaged export.

Partial rock occlusion (latest owner direction, 2026-09-08): supersedes the all-or-nothing south-rock rule. Room, derelict and blocker foundations render before rock/wreck silhouettes on the environment layer. South occupied rooms still suppress foundations; southern rocks mask only overlapping pixels, leaving exposed sections visible. Terrain variants and cleared-owner exclusion retained. Native paid preview and eligibility assertions pass; visually reviewed output/foundation-partial-v1/heat_recovery.png. No source edits or export.

Latest depth pass: see docs/DEPTH_PASS_2026-09-08.md. Continuous slabs, weathered derelict source and actual-contour stone bases supersede earlier isolated metal supports on basalt. Partial rock occlusion retained.
