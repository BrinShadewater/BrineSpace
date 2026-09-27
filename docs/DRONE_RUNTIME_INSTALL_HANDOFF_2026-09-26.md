# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Install remaining drone animations

## Objective and acceptance
Owner requested installation of the remaining latest animation packs after the audit. Construction/ROV, mining, salvage and v10 docks are now connected to existing production fleet jobs and bay props.

## Accepted decisions and constraints
Preserve approved raster art, owner layouts/Studio marks, job timings, costs and rewards. Keep the native top-down perspective and dock-calibrated vehicle scale. Additional art clips do not imply new gameplay commands. No executable rebuild requested.

## Current state
New `scripts/drone_animation.gd` and `scripts/drone_dock.gd` (paired UIDs); runtime manifests and 30 copied approved dock components in `assets/drone-runtime-2026-09-26`. Fleet/routes retain visual phase, distance, turn and rotor fields; grid and retained room canvases consume them. All three production-ten bay views and the catalog/library draw path use the new docks. Legacy service covers remain static. Cards and animation inventory refreshed. Review tools and a new targeted test are saved with UIDs.

Review: http://127.0.0.1:8780/drone-runtime-2026-09-26/ . Desktop organized exports now include `10-installed-drone-animations`.

## Verification
Fleet, battery, jobs, lifecycle/pause/checkpoint, work-face and finite-harvest checks passed. New sampler: 252 clips, 144 directional phase samples; all 541 explicit image paths exist. Native handoff: six comparisons, zero failures. Native visual review: 180 animation frames, 48 actual-game room/rotation/phase captures with Bill, 12 refreshed room/card views. Bay layout lint: 12 rotations, zero findings. Owner layout and four Studio mark files match their pre-install backups byte-for-byte. Index and HEAD each contain 34,567 tracked paths.

An initial native review exposed premature texture eviction; active canvas resources are now pinned, and the final capture set has no white rectangles. Texture-cache budget is a soft target while active atlases are pinned. PNGs retain Git LFS attributes. The initial editor-import attempt was stopped; direct native/headless runs subsequently parsed and exercised the installed scripts successfully.

## Next action
Owner visual review of the installed scale/motion. Executable packaging remains separate. Unused art-pack-only actions remain available in the manifests but are not new gameplay features. No commit, push or executable export performed.
