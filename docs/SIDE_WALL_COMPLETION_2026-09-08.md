# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: Missing vertical full-wall artwork

## Objective and acceptance
Provide matching vertical artwork for the full-wall installations missing east/west views, integrate it and verify room clearance.

## Accepted decisions and constraints
The 15-installation catalog had nine pairs and six missing pairs. New paired sources cover Research Lab, Med Bay, Pressure Control, Listening Post, Xeno Lab and Isolation Vault: six sheets, twelve views. Use the original accepted Pressure/Listening machinery as references; preserve their q0/q2 behavior. Side artwork is newly drawn with straight vertical backing, never a rotated or squeezed horizontal bitmap. Preserve original rasters and owner layout files.

## Current state
Sources, exact prompts, hashes and dimensions: assets/side-wall-completion-v1/. Twelve JSON cutouts added under rooms/full-wall-v1/registrations/. RGB white/checkerboard exterior is excluded through polygons; no claim of source alpha. full_wall_prop.gd loads and selects the new views for applicable vertical orientations; Room Layout Studio discovers the same registrations. room_layout_store.gd falls back to authored placement when an older new-side draft would leave the hull or block a doorway; it keeps stored data intact. Registration tools accept an alternate source directory and reviewed neutral threshold. Full-wall review supports isolated output and personal-draft diagnostics. Existing q0 card selection remains valid; diagnostic cards were written to output, not over selected assets. Tests/test_side_wall_variants.gd and paired UID added.

## Verification
output/side-wall-completion-final.log: native 15-room x four orientations x two-state review passes, including bounds, door lanes, relocated artwork and cryo recovery preservation. Reviewed east and west contact sheets; six-room preview: output/side-wall-completion-final/new-vertical-rooms.png.
output/side-wall-variants-test.log: twelve variants pass source hashes, library availability, states, invalid draft fallback and valid draft preservation.
output/side-wall-completion-routes.log: all six rooms pass four rotated layouts using production crew movement; zero assertions or engine errors.
All new PNGs are covered by Git LFS. No exported build.

First source registration rejected the Research checkerboard crossing the divider; reviewed neutral threshold 210 excludes its exterior without raster edits. Initial native fixture inadvertently read personal drafts and failed an older horizontal Research layout. Authored isolated review passes. A narrower personal vertical-draft diagnostic still reports Research cabinet overlap; personal files were not modified. Do not claim arbitrary personal layouts passed the geometry review.

## Next action
Owner review of the twelve new views. Personal Research draft furniture needs manual layout review if used. Earlier Pressure/Listening q2 directional-identity limitations remain outside this vertical-variant pass. Concurrent unrelated changes preserved; no commit/export.
