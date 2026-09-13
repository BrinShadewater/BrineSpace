# Hull damage atlas

Generated with the built-in image tool on 2026-09-12. Gameplay screenshot used only as a style reference.

## Initial prompt
Use case: stylized-concept. Create a production game sprite atlas for BrineSpace underwater station hull damage. The visible gameplay screenshot is STYLE REFERENCE only. Match its muted weathered ivory/gray teal industrial pixel art, dark navy crevices, restrained warm corrosion, crisp pixel clusters, no glow. One single atlas 1536x1024, exact 3 columns x 2 rows of equal 512x512 cells. Transparent RGBA background, absolutely no backdrop, labels, text, grid, checkerboard or water. Each isolated wall decal centered within its cell, generous clear margin. Top row left: narrow hairline crack with chipped ivory paint and dark thin branching seam. Top row middle: split seam wider jagged dark opening and chipped metal lips. Top row right: hull rupture, torn dark opening with bent weathered metal edges. Bottom row left: emergency rectangular bolted steel patch, four corner bolts, scratched dull gray teal sheet with a little rusty edge, front-facing. Bottom row middle: fully sealed weld scar, thin uneven silver-gray welded bead with restrained brown heat discoloration, no opening. Bottom row right: another fully sealed weld scar, smaller. These are small decal overlays NOT chunks of square wall, no large backing wall surrounding cracks. Mostly vertical cracks, in a frontal orthographic view to sit on upper interior wall of cutaway room. Clean actual alpha outside each object, no white matte fringes. Readable silhouettes when reduced to 40 pixels. No perspective floor, no characters, no interface. Generate only the atlas.

## Cleanup prompts
Preserve all six objects, positions and dimensions; replace baked checkerboard with genuine transparent alpha. This attempt still returned a checkerboard.

Preserve the exact six-sprite layout and foreground objects. Replace all checkerboard and background smudges with uniform magenta RGB(255,0,255); no transparency, gradients or background shadows. Keep dark holes intact and crisp edges. Output 1536x1024.

## Production bake
source-v1.png is the selected chroma-key source. bake.gd removes magenta pixels and reduces each 512px cell to 96px with nearest-neighbor sampling. hull-full.png retains full resolution with alpha; hull-96.png is the runtime 288x192 RGBA atlas. Cells: hairline, split, rupture, patch, weld scar, spare short scar. Runtime water remains separate.
