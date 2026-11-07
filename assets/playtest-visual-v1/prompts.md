# Exact generation prompts

Built-in image generator, 2026-09-07. No external API or CLI used.

## switch-source.png — new image

Create a production game UI asset: one isolated industrial ON/OFF rocker switch assembly, straight-on orthographic front view, transparent background. BrineSpace is a utilitarian underwater pressure station, chunky deliberate pixel-art clusters, muted charcoal gunmetal housing, four captive steel corner screws, recessed rectangular mechanical rocker, small restrained amber pilot lens above it, no bloom. Wide horizontal housing 2.5:1 aspect ratio centered on transparent canvas, large rocker centered, readable at 150 by 60 pixels. Rocker in neutral/off position, no letters or text (labels will be drawn by game UI). Clean intact but lightly handled steel, bevels with subdued cool grey highlights, dark rubber waterproof gasket. Single complete switch only, no sheet, no surrounding wall, no shadows outside housing, no white background. This is a reusable interface texture; camera absolutely straight-on with no perspective tilt. Save generated image file.

## deck-source.png — new image

Production game texture, square seamless interior deck material for BrineSpace underwater industrial station. Strict top-down orthographic flat surface, no perspective, no walls, no props, no doors, no typography. 4 by 4 grid of large flush square pressure-rated steel floor plates. Quiet matte medium neutral grey steel, narrow dark recessed seams, very subtle edge bevels, only two small recessed fasteners per plate. Mostly clean restored interior, subtle handling wear, no rust speckles. Chunky deliberate pixel-art surface clusters consistent with detailed top-down retro-futurist game machinery. Uniform low-contrast neutral lighting, absolutely no blue glow, no bright highlights, no dramatic shadow. Fill entire square edge to edge; outer seams align for tiling. Keep large plain quiet areas; readable subtle geometry at 384px room scale. Opaque texture, no border or background.

## pressure-source.png — edit

Reference: `rooms/underwater/rare-dead-ends/pressure-u-flush-clean-v1.png` (composition, silhouette, materials).

Refine this BrineSpace pressure control machinery sprite, preserve EXACT U silhouette, canvas, transparent exterior and large transparent center aisle, all major machinery positions and proportions. Style refinement only: simplify excessive tiny pipe and rivet noise into deliberate chunky readable pixel-art clusters; mostly clean matte charcoal pressure vessels, restrained muted brass joints, larger readable pipe runs, central analog pressure gauge remains focal with subdued warm grey dial (not luminous white); reduce cyan lenses to dim grey-green glass with no bloom. Keep all equipment facing camera as existing, same top-down game view and dark steel materials. Do not add floor/walls/door, do not fill transparent aisle, do not add machinery, do not alter footprint. Retain original larger tanks, pumps, U perimeter equipment and central gauge. Transparent background alpha.

## door-source.png — new image

Single isolated production asset for BrineSpace game: top-down orthographic low cutaway underwater station pressure door, horizontal very wide shallow rectangle (6:1 aspect). Two CLOSED rigid steel sliding leaves meet at central vertical seam, enclosed by slim rubber gasket and small reinforced jamb caps at left/right ends. Low hull cutaway, no tall arch, no visible front facade. Muted matte grey steel, subdued brass fasteners, narrow engraved grooves, restrained dark grey-green side indicator inserts, no bloom. Chunky pixel-art rendering, uniform neutral illumination, machinery-readable at 100 by 18 pixels. Transparent background real alpha, no checkerboard, no shadows outside asset, no letters, no props or floor. Center the entire thin horizontal door on canvas with generous transparent margin. This is texture art for code-controlled sliding leaves, crisp straight edges, absolutely no perspective tilt.

## pressure-alpha-attempt.png — rejected edit

Reference: `pressure-source.png` (preserve equipment).

Remove only the baked light grey and white checkerboard background from this image, including the large open center aisle and all outer margins. Replace that background with REAL transparent alpha. Preserve every equipment pixel, all U-shaped metal machinery, exact canvas size and location. No restyling, no new shadows, no extra content. Output PNG with actual transparency; do not paint a transparency grid.
