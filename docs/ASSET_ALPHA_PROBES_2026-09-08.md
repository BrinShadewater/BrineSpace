# Asset alpha probe handoff

Updated September 8, 2026. BrineSpace ongoing asset pipeline.

## Objective and constraints

Make selected opening/interior checks reproducible without confusing point samples
with complete silhouette acceptance. Source and export rasters remain unchanged.

## Current state

`tools/check_asset_alpha_probes.py` reads a project-local record containing export
path/hash, native canvas size and named integer pixel coordinates. Each point must
declare transparent (0) or opaque (255), with a matching saved alpha measurement.
No reports or art are written. Invalid or stale evidence exits unsuccessfully.

The material workflow documents the command and the textile basket schema example.

## Verification

Nine focused tests pass: valid/read-only, changed hash, filled handle, erased body,
RGB export, invalid coordinates, empty/duplicate samples, stale record/canvas and
outside export. The basket's five current probes pass, including both handles and
retained cloth/interior. This adds no new visual or runtime acceptance.

## Next action

Use on new assets with reviewed apertures. Preserve light/dark silhouette review;
small point sets cannot detect defects elsewhere. Geometry changes need renewed
visual probe selection, not automatic hash replacement.
