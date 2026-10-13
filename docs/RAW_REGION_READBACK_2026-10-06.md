# Project handoff

Updated: October 6, 2026 · BrineSpace · Loading gap confirmation and raw image bounds

## Objective and acceptance
Remove redundant startup GPU readbacks while preserving exact textures and source
bounds. Gameplay FPS, full release memory and platform certification remain open.

## Accepted decisions and constraints
Normal art/filtering/mipmaps/save behavior unchanged. Compressed crew stays private.
Tests use verified scratch data; all 2,936 owner files unchanged.

## Current state
`scripts/grid_canvas.gd::_load_png_texture` passes the already decoded CPU image
to bounds calculation after upload instead of immediately reading the texture back.
Imported-resource/null fallback remains. No cache or retained image added.
New `tests/test_raw_texture_regions.gd` and UID registered as native render-perf.
Diagnostic generators support physical Grid copies and event/draw pump timing.

Evidence: private single-buffer `loading-progress-fast-scan/`, `card-profile-raw/`;
`output/compressed-crew-2026-10-06/raw-region-regression/`.

## Verification
After prior card scan fix: fresh 105 loading callbacks over 13.039 s, max gap 364 ms;
Continue 36 over 4.764 s, max 322 ms. Earlier maxima 783/656 ms. Single runs with
separately generated sites, not deterministic speed certification. Loading draw
max 2.820/3.689 ms, events <0.021 ms. First registration/nursery gaps remain.

339 native checks pass: JPEG, doors, caustics, card paths, saved import-only texture
and missing source. GPU bytes, dimensions, formats, mipmaps and source bounds match
the prior SafeImage upload/readback path. No unexpected artwork failures. Actual
native title/transmission/Studio/save/Continue: 154 checks pass, zero engine errors,
restored crew and sampled resource release. Anonymous exit ObjectDB warning open.

Observed 94-call readback totals before/after: fresh 179.886→144.532 ms, Continue
139.333→104.903 ms; scan totals ~92–93 ms unchanged. One native comparison with
different generated sites, not overall loading/FPS or texture-memory certification.
Shared Main card textures still require readback.

## Next action
Main `_load_card_thumbnail` uploads, reads back, generates mipmaps and uploads again.
Validate direct CPU mipmap preparation against every GPU mip level and fan filtering
before changing it. Gameplay rover upload/rendering stalls remain a separate priority;
storage admission, bugs, endurance, warning and PC/Mac executable gates stay open.
