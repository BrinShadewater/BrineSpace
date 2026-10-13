# Project handoff

## Read-only consistency audit — September 27
Owner requested pixel density, color and art style review. Completed across all
14 current sources and representative native hosts. Report:
`assets/ocean-windows-v3/CONSISTENCY_REVIEW.md`; reproducible measurements and
source hashes in `consistency-audit.json` and `audit_consistency.py`.
Finding: palette/placement broadly coherent, density and finish need refinement.
Windows use 17.81–34.75 source pixels per display unit versus walls 4.92–5.59;
nearest sampling and native pinprick detail warrant a calibrated export pilot.
Dark green palette is consistent, but compact/wide/square wear treatment differs.
Brass is relatively shiny; ocean microdetail/exposure varies. No art/runtime
changes or new Godot tests. Next action is a three-shape density pilot, then
targeted finish/exposure repair if owner requests it. No new acceptance claimed.

## Green window readability — September 27
Owner requested darker, more readable green windows. Edited all three sage
sources with built-in image_gen toward deep forest/petrol green frames, retaining
the existing ocean compositions and construction. Original bytes preserved in
`assets/ocean-windows-v3/previous-sage/`; exact edit prompt in `dark-green-prompt.json`.
Re-registered the measured alpha bounds in `ocean_windows.gd` (minor generated
edge differences); mounting sizes and positions unchanged. Updated source hashes
and gallery. Four native Biomass Digester orientations passed, and the native
three-window view was visually inspected for contrast against the olive wall.
Scratch profile confirmed; concurrent session breadcrumbs changed. Owner visual
acceptance and baked-card/export refresh remain pending.

## Side-panel centering — September 27
Owner found left/right room windows too high. `ocean_windows.gd` now lowers only
the side mounts by 7 units (center y -233 to -226), leaving size, x position,
center viewing windows, doors and corridors unchanged. This centers the fittings
within the inset side-panel field above the bottom service band. Native review:
16 captures, zero failures; Galley and Cold Store screenshots visually inspected.
Gallery/manifest refreshed. Scratch profile asserted; concurrent real session
breadcrumbs changed, as in prior runs. Owner visual acceptance remains pending.

## Slight size reduction — September 27
Owner found doors and large windows slightly too big. Center mounts reduced from
64 to 56 units (12.5%), keeping the same center and all eligibility rules. Raised
department doors now scale the complete assembly to 90% around the threshold,
including leaves, frame, header, sill and dark aperture. Motion timing, logical
doorway geometry, low cutaway doors and the separate ocean hatch remain unchanged.
Changed `ocean_windows.gd`, `painted_door.gd`, focused review minimum-size check,
gallery builder and gallery. Native room check: 16 captures, zero failures;
remaining door-bearing hosts and corridor finish views refreshed separately.
Sources unchanged; no image generation. Owner visual acceptance remains pending.
Scratch profile confirmed; concurrent real session breadcrumbs again changed.

## Large square center-window follow-up — September 27
Owner requested large square viewing variations for the middle north wall. Added
graphite steel, warm ivory and muted sage sources (14 window designs total), with
exact built-in image_gen prompts in `assets/ocean-windows-v3/square-prompts.json`.
`ocean_windows.gd` now fits a material-selected square in a 64x64 center mount at
(-32,-248), fully inside the existing 92x79 central panel. The existing outer
room eligibility gate excludes north doors, exterior hatches and BRINE Core.
Side fittings remain. Actual source silhouettes are near-square (~1.03 aspect)
and are fitted uniformly without stretching. Source PNG bytes are unchanged.
Square interiors have alpha 251–254: a dark opaque inset backing prevents wall
bleed while preserving the transparent exterior. Native source-coverage gate
records >98% alpha rather than claiming fully opaque source pixels.

Focused native review passed: 16 captures of Galley, Salvage Workshop, Biomass
Digester and Cold Store in all four orientations; all source/fit checks plus
central panel containment and minimum 60-unit visible size passed. Representative
native samples reviewed. Godot confirmed scratch profile; only real session
breadcrumbs changed concurrently, so strict unchanged-profile wrapper remains
nonzero. Gallery/manifest updated. Owner visual acceptance and card/export
refresh remain pending.

Updated: September 27, 2026 · Project: BrineSpace · Task: Ocean-floor pressure windows

## Objective and acceptance
Replace ocean-window artwork with material-matched small portholes, medium bulkheads and wide viewing windows, including corridor/corner/tee fittings. Owner visual acceptance remains pending; source-project integration is complete.

## Accepted decisions and constraints
Owner requests north riser walls only where no doorway connection is present. Existing room window reserves remain authoritative. Room north ports and the airlock exterior hatch suppress windows; corridor entries and connected cell boundaries suppress their segments. BRINE Core keeps its special assembly. No room layouts, mechanics or real save files were edited by this task.

## Current state
Seven original generated PNGs, exact retained prompts, source hashes, gallery and native captures: `assets/ocean-windows-v3/`. Two rejected trials retained separately. Built-in image_gen used; no Higgsfield jobs. The registered renderer is `rooms/whole-room/ocean_windows.gd` with paired UID. `painted_shell.gd` selects room-material windows and existing mounts; `corridor_dressing.gd` installs shape-specific fittings beside route marks and gives utility windows a solid mounting panel. `corridor_wall_art.gd` suppresses the former baked observation-window band. Source PNGs retain their bytes; only runtime source-region cropping and uniform fit occur.

## Verification
- Index and HEAD each had 36,418 paths; no HEAD paths missing from index.
- Seven PNGs have transparent exterior and opaque aperture centers; registered regions fit source and preserve aspect within all tested mounts. PNGs covered by Git LFS attributes.
- Native Godot review: 56 distinct captures, four orientations of five room types and three corridor shapes; corridors additionally cover utility and observation finishes. Latest corridor pass: 36 captures, zero failures. Earlier room/shape passes also zero failures. Representative material, doorway, porthole and all-finish captures visually inspected.
- `tools/review_ocean_windows.gd` and its paired UID provide repeatable checks. `assets/ocean-windows-v3/run_review.py` sets scratch APPDATA; Godot asserts and prints its actual scratch user directory. All native test saves/logs use this directory.
- Real profile fingerprints changed during runs (session breadcrumbs and owner layouts); an independent live game was confirmed running. No restoration attempted. Thus wrapper reports failure on the strict unchanged-profile check even though native functional checks pass. Do not claim real-profile byte equality.
- Relevant source diff whitespace checks passed. Packaged executable, baked card refresh, performance profiling and owner visual acceptance are not covered by this evidence.

## Next action
Owner reviews `assets/ocean-windows-v3/index.html` and native examples. Refine particular materials/sizes if requested. Refresh baked cards and release package after visual selection; this pass updates the live source renderer only. Keep future tests isolated and preserve concurrent Studio edits.

## Expansion follow-up — September 27
Owner requested more windows. Added four separately generated sources: oval brass,
octagonal steel, divided sage viewing window and blue twin portholes (11 designs
total). Exact prompts are in `assets/ocean-windows-v3/expansion-prompts.json`;
the regenerated manifest records source hashes and measured alpha bounds.
`ocean_windows.gd` registers the new sources and uses each in the second existing
mount of Galley, Salvage Workshop, Biomass Digester and Cold Store respectively.
Original designs and placement gates remain. Gallery builder and gallery updated.
Focused native review: 16 captures across those four hosts, zero failures;
all 11 source registrations/fit checks passed. Representative native captures
visually inspected. Scratch profile asserted; real `last_session.json` changed
concurrently, so unchanged-profile wrapper remains nonzero. No save restoration.
Owner art acceptance and baked-card/export updates remain as above.
