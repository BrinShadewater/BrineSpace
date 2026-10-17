# Upright grass-shaped kelp

Owner requested kelp that rises straight up like grass. Emerald, sea-white and violet variants use compact holdfasts and nearly parallel narrow stalks, with restrained bends in the blades. This deliberate upright silhouette differs from the earlier overhead ribbon crowns; other scenery retains its camera contract.

The renderer anchors each sprite at its bottom holdfast, preserves its aspect ratio and never rotates it. Widths are 0.28, 0.30 and 0.28 cells; heights follow the native source proportions. Sparse variants dress kelp, sponge, brine, coral and iron habitat regions while avoiding the station core. Decorative foliage creates no collision or resource state.

Immutable masters and exact prompts are preserved, including rejected violet v1 with its exterior haze. Selected violet v2 is a fresh generated clean cutout. `bake.py` trims transparent margins and resizes isotropically to 1024px height. No alpha repaint or source colour grading occurs; the existing underwater tint applies at draw time.

Use `tools/review_upright_kelp.ps1` for native density/colour comparisons, station samples at three zooms, lit production habitat views and environment checks in an isolated profile.

## Sway animation — September 30

Upper blades bend gently in a seamless eight-second loop. The lower 8% containing the holdfast stays fixed; deterministic location phases prevent synchronized clumps. The production visual clock supplies pause and selected-speed behavior. Reduced Motion or effects off uses the original static sprite. Shared textured-strip edges preserve painted colours and continuous detail; no raster changes were made.

Run `tools/review_upright_kelp_sway.ps1` for rendered motion, root-pixel stability, exact loop closure, frozen-time, accessibility and authoritative pause/speed checks. Native PNG frames remain the visual evidence; the GIF is a preview encoding of those captures.

Smoothing pass: 16 bend subdivisions and reduced secondary flutter soften live movement. Native preview captures now use 30fps rather than the initial 5fps, retaining the same eight-second timing.
