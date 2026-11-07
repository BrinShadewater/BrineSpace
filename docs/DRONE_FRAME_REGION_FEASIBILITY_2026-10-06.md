# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: exact drone frame-region feasibility

## Objective and acceptance

Remove measured whole-sheet transition uploads while preserving selected drone pixels, clocks, roots, filtering, layer order and scene ownership. Full release gates remain open.

## Accepted decisions and constraints

Private native probe only; normal runtime unchanged. Direct cropping is not accepted because it changes rendered pixels. Preserve runtime PNG decoding; no image downscaling, lossy encoding, reduced frames or engine change.

## Current state

New private probe and isolated runner: output/drone-frame-region-2026-10-06/{probe.gd,run.py}. Quantified results in results.json; initial-results.json retained. Two runs compare original whole-sheet draw_texture_rect_region with exact Image.get_region pixels drawn through the same API. Synthetic adjacent cells and actual mining West sheet; six cells each, three scales, nearest/linear, mirrored/unmirrored, transparent background and tint.

## Verification

Both native runs: 144 comparisons, 45 mismatches. Actual West: 10 nearest cases differ (up to 107 pixels and 128 channel levels); 30 linear cases differ (up to 3777 pixels, maximum 2 channel levels). Synthetic: five linear cases differ, at most 13 pixels/one level. Nearest failures mean this cannot be dismissed as harmless color rounding. Changed texture dimensions/source UV representation is the controlled variable; precise shader/sampler mechanism remains unproven.

Real full sheet: 144506880 bytes, upload 17.763/19.068ms. Exact frame: 802816 bytes, upload 0.068–0.159ms first run, 0.059–0.210ms second, crop 0.114–0.297ms second run. These are isolated call timings, not gameplay FPS or cache/churn acceptance. First run used Image.load_from_file and emitted an export warning; corrected second run uses existing load_png_from_buffer(FileAccess.get_file_as_bytes) and has no warning/error. Expected exit1 records raster rejection. Both owner fingerprints: 2936 non-log files unchanged; runs terminal.

## Next action

Inspect original GLES region UV interpolation/clamping and test a frame-backed sampling path that preserves original full-sheet normalized coordinates and sampler behavior. Keep nearest and linear exact gates; do not loosen comparisons to admit cropping. Then bounded frame/source caches, multi-drone transitions, worker shutdown and matched 4x performance/memory coverage. Background decoding alone still does not remove full-sheet uploads.
