# Krusher Dom runtime candidate

System Administrator · AI & Robotics · matte muted grey-cyan `#527C80`.

This package consolidates the existing Bill-body Krusher trial. Both gears have four-direction idle/walk plus west terminal raise, type and lower: 11 states per gear, 986 total frame references and 970 unique PNGs. Source canvas 184 × 184, pivot (92,172), standing ruler 148 px, linear filtering. Original durations, loop flags and directional walk strides are retained.

Use `bare-manifest.json` and `helmet-manifest.json` with the existing crew sprite player. The helmet manifest is precomposed and can be admitted as `diving-helmet`. The terminal starts and ends on the same `idle-west/000.png` file, and its held joins share the same pose file. PNGs and manifests are self-contained in this folder; artwork sources remain preserved in the earlier candidate folders listed by `provenance.json`.

`CrewSpritePlayer.frame_at_elapsed` clamps to the clip extent. A caller that wants a looping clip must supply elapsed modulo the clip duration; the normal `frame` method handles its loop/movement clock. The terminal action means retrieving and opening the hip terminal, typing, then closing and stowing it. Only the west action is supplied.

## Rebuild and verify

From the checkout root:

```powershell
python character/krusher-runtime-candidate-v1/build_package.py
python character/krusher-runtime-candidate-v1/validate_package.py
python character/krusher-runtime-candidate-v1/build_probe.py
python character/krusher-runtime-candidate-v1/run_native.py
```

The native runner sets scratch APPDATA before launching Godot, fingerprints owner files before/after, and uses the existing project sprite player. It checks midpoint selection and exact source pixels for every frame reference, gear admission, canvas/pivot/standing metadata, linear filters and clip duration. Three native captures are retained under `review/native/`.

Package validation: 3,015 checks, zero errors. Existing-consumer validation: 3,967 checks, zero errors, Godot 4.7.2 exit 0. All 2,930 fingerprinted owner files unchanged. Raster LFS attributes apply to these PNGs.

## Review and scope

Production references: `character/krusher-production-reference-v1/`.
Compact walking and terminal MP4: `character/krusher-locomotion-native-review-v1/review/krusher-motion-preview.mp4`.

Complete package MP4: `review/full-motion-preview.mp4`, about 1.1 MB, including all idle cycles. `review/index.html` provides all 11 chapter controls, original/half speed and download. The video reconstructs 493 native paired captures at declared source durations; source time is 22.480 seconds, presented at 60 fps. This presentation does not change source timing metadata.

Complete continuous consumer pass: `python character/krusher-runtime-candidate-v1/run_motion.py`, then `validate_motion.py`. Two 22,480 ms cycles produced all 986 paired pose events, with 4,444 checks and zero errors. The native runner uses scratch APPDATA; all 2,930 owner files remained unchanged. All 289 bare idle display-size crops were inspected chronologically on the four boards under `review/`. Mechanical full-cycle playback and pose-by-pose inspection do not replace temporal artistic review.

This is an unselected candidate. Normal game selectors, crew definitions and gameplay behavior were not changed. Technical consumer compatibility is verified; complete artistic motion acceptance remains separate. Expressions, authored turning inbetweens, additional role directions and other body-family compatibility are not supplied by this package.
