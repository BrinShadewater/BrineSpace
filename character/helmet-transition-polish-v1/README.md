# Helmet transition pacing and continuity

September 27, 2026. Installed in source for Veld and Branforth.

Both fitting and removal now reference eight distinct existing poses: bare idle, six authored interior keys, and helmeted idle. Removal references the fitting images in reverse order. No PNG pixels were changed, so the shared palettes, anatomy, transparency and foot registration are intact. The previous ten-pose minimum was stale after later six-key source replacements; the regression test now verifies all eight source poses and exact joins rather than demanding invented poses.

## Timing

Fitting remains 2,140 ms; removal remains 2,240 ms. Maximum consecutive pose holds fell from 440/460 ms for Veld and 500/660 ms for Branforth to 340 ms. The new timing distributes time through the reach, lift, seating and release instead of repeating frozen slots. This is a pacing correction using existing artwork, not newly authored inbetweens. The remaining pose-to-pose jumps would require additional source artwork to smooth further.

## Files and rebuilding

Only the two selected bare 184x208 manifests change runtime selection: two clips each. Inactive PNG files are retained. `selected.json` freezes the prior paths, metadata and PNG hashes; `checks.json` records before/after timing. `tools/polish_helmet_transitions.py` performs the deterministic metadata update and is called at the end of full Veld/Branforth source rebuilds. Palette postprocessing remains required after a source rebake.

The palette comparison generator now resolves the current selected frame order and pairs those poses with their preserved pre-palette originals. Its frozen baseline still describes the earlier colour-only milestone; the two helmet manifests intentionally supersede those historical hashes. Do not overwrite the palette baseline to make its old installer accept these changes.

## Checks and review

- `python tests/test_fitted_crew_helmets.py`: both tests pass; exact idle joins, reverse order, eight distinct keys, all source pose pixels preserved, duration/hold limits and metadata lengths.
- Isolated native `tools/review_helmet_transitions.gd`: 1,876 checks, zero failures; actual game crew loaders, both action clocks, repeated-time pause behaviour and held final frames. Real profile fingerprints unchanged.
- All 8,575 palette-pass PNG hashes remain unchanged; precisely the two intended manifests differ from that baseline.
- `native/phase-*.png` and the local `index.html` compare the actual loaded clips before/after at 100 ms intervals, at source and gameplay sizes. Agent reviewed samples; owner visual acceptance remains separate. This is renderer/playback evidence, not a full locker service/save/restore playtest.

No executable rebuild. Broader walk softness, Veld neck gaps and Marsh style differences remain separate work.
