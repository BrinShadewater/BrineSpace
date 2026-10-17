# Project handoff

Updated: September 27, 2026 · Project: BrineSpace · Task: standing 3D/2D art comparison

## Objective and acceptance
Improve standing render quality and compare front/side against Veld 2D pilot v12 at identical 148px height, with approximately 45px small previews. Owner visual acceptance pending.

## Accepted decisions and constraints
Preserve supplied GLB and runtime. Test rendering/proportions before expanding animation production.

## Current state
../render_standing.py reuses the existing accessor/skinning implementation without running walk exports. Poses arms down through skeleton world-space rotations. standing-comparison.png compares original 2D, raw 3D, filtered 3D, and filtered/proportion-adjusted 3D. Eight calibrated RGBA sprites and settings.json saved. Rendering uses 4x supersampling, 512px texture mip, Lanczos reduction and six-degree elevated camera. Last column widens/deepens suit and enlarges head using documented blended vertex transforms. Source geometry/texture files unchanged. Material palette remapping and new lighting were not applied; source baked shading retained.

## Verification
Script completed; finite vertex assertion passed. Visually inspected front/side comparison twice after proportion revision. Texture speckling substantially reduced. Remaining gap is clear: 2D face and equipment are larger/more articulated, silhouette has more depth and stronger painted highlights. Filtering alone does not establish style acceptance. Static height calibration is per view and must not be copied into per-frame animation scaling. Neutral arm pose not a production idle; animation deformation of proportion adjustments untested. No Godot execution or owner save access.

## Next action
Owner review of final comparison. Refine actual head/equipment forms and texture shading if closer parity is desired; avoid declaring camera/filter settings sufficient. Promote approved source-space changes to rig and then rerender motion at fixed scale. Runtime unchanged.
