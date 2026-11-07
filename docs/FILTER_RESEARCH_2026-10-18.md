# Pixel art and visual-filter research for BrineSpace

Research date: October 18, 2026. Scope: techniques worth auditioning against the current game, informed by primary technical sources, the current source renderer and the retained live-game captures. These are recommendations, not accepted art direction or measured visual/performance improvements. No runtime or artwork changes were made for this research.

## Recommendation

Audition colour grading and gentle brightness simplification before increasing pixel size. The existing art depends on small machinery details, crew silhouettes, metallic highlights and departmental colours. A stronger grid removes some of those features. A restrained grade or palette can instead make different assets feel more related while retaining their shapes.

The strongest first candidates are:

1. **A restrained underwater colour grade:** readable midtones, cool environmental shadows, warm practical lights, and neutral machinery highlights.
2. **Gentle luminance posterization:** simplify brightness into a modest number of steps while largely retaining colour identity.
3. **An authored station palette:** a more deliberate graphic style using a palette derived from this game's rooms, crew, departments and lighting.
4. **Selective bloom and local contrast:** improve the separation between lighting, machinery and the background by tuning existing effects.

Fine pixelation, dithering and miniature/diorama focus are useful secondary comparisons. Outlines, painterly abstraction and CRT treatments should be separate style experiments. My assessment of fit is artistic judgment; the cited sources establish how the techniques work.

## What the current audition actually does

`scripts/look_audition.gd` currently blends the scene with samples from a coarse screen grid. At 2 px/60%, the output retains 40% of the original scene and mixes in 60% of the grid sample. It is a spatial treatment, not a colour-palette filter. The mixed output does not have one flat colour per coarse block, so the result can feel like softened detail rather than tightly authored pixel art.

The earlier screenshot prototype's “32 levels / channel” option also was not a 32-colour palette: three independent channels with 32 levels allow up to **32³ = 32,768 RGB combinations**. This is an important distinction when judging whether the experiment captured the desired style.

The Princeton/Rutgers research on pixelated abstraction treats feature placement and palette selection together; its comparisons show why ordinary downsampling followed by colour reduction is an incomplete approximation to deliberate pixel art. This does not establish that its iterative algorithm is suitable for this game's live renderer. [Gerstner et al., Pixelated Image Abstraction](https://gfx.cs.princeton.edu/gfx/pubs/Gerstner_2012_PIA/Gerstner_2012_PIA_full.pdf).

## Pixel-related techniques worth distinguishing

| Technique | What changes | Likely fit here | Principal tradeoff |
|---|---|---|---|
| Point-sampled pixel grid | One scene sample represents each block | Useful baseline; keep pitch small | Thin details can disappear or change as the camera moves |
| Area/weighted pixel sampling | A neighbourhood contributes to each block | Worth comparing with the existing point sample | More stable averages can look softer and mix important colours |
| Edge-aware downsampling | Tries to retain important boundaries while simplifying | Interesting second-round experiment | A colour edge cannot tell machinery detail from a meaningful object silhouette |
| Luminance posterization | Reduces brightness steps, with colour retained as far as possible | High-priority graphic treatment | Too few steps flatten metal, faces and dim lighting |
| RGB channel quantization | Rounds red, green and blue separately | Quick reference, lower priority | Arbitrary colour shifts; does not produce an authored palette |
| Authored palette mapping | Maps colours into a selected set | High priority for stronger stylistic unity | Palette must preserve departments, crew colours, warning signals and light transitions |
| Gradient mapping | Maps brightness through a colour ramp | Good for sonar/BRINE/terminal looks | A single ramp can make different departments look alike |
| Ordered/Bayer dithering | Uses a regular threshold pattern between colour steps | Optional retro-material treatment | Visible grid/hatching can compete with floor and prop texture |
| Blue-noise dithering | Uses an irregular, evenly distributed threshold pattern | Better first dither trial for subtle gradients | Still introduces visible texture and needs motion review |
| xBR/xBRZ/hqx-style scaling | Reconstructs larger images from existing low-resolution art | Low priority for this objective | Primarily an enlargement problem, not automatic pixel-art creation |

Phaser's own technical guide usefully separates original-colour block sampling, blended pixelation, channel quantization and brightness-ramp mapping. These are distinct looks, even when a product groups them under “pixel art.” [Phaser 4 Pixel Art Guide](https://github.com/phaserjs/phaser/blob/master/docs/Phaser%204%20Pixel%20Art%20Guide/Phaser%204%20Pixel%20Art%20Guide.md). Kernel-based sampling has different reconstruction behaviour depending on its weights and colour space; averaging is not inherently an aesthetic improvement. [GPU Gems: High-Quality Filtering](https://developer.nvidia.com/gpugems/gpugems/part-iv-image-processing/chapter-24-high-quality-filtering).

### A palette should be chosen for this game

Start by collecting representative room/crew/terrain/light colours, then deliberately reserve distinctions for department colours, hazards, rare resources, warm lamps and AI-white. Compare perhaps 64, 96 and 128 selected colours before a severe 16/32-colour treatment. These counts are proposed trial settings, not research-established optima.

Use a perceptual space such as Oklab when constructing or comparing candidate palette colours rather than assuming equal RGB distance looks equally different. Oklab explicitly separates perceived lightness from chromatic axes. That improves the basis of the comparison; it does not guarantee preservation of the game's semantic colours. [Bjørn Ottosson, Oklab](https://bottosson.github.io/posts/oklab/).

Keep the palette fixed during a trial. Recalculating it from each camera view would make the visual target change as the player pans. A precomputed colour-to-palette lookup is an implementation candidate; avoid a large per-pixel palette search without profiling. Continuous grading LUTs and strict palette LUTs need different sampling: interpolation is useful for smooth grading, but interpolated palette entries create colours outside the selected set.

### Dither only where it helps

Compare **no dither**, a low-amplitude 4×4 Bayer pattern, and a small precomputed blue-noise texture. Keep the palette/posterization settings fixed between those comparisons.

Regular Bayer thresholds deliberately create patterns; blue noise spreads the structure without the same strong directional grid. The shader author's examples make that distinction visible. [Xor, Mini: Dither](https://mini.gmshaders.com/p/gm-shaders-mini-dither). Christoph Peters explains blue-noise distribution and demonstrates small tileable masks suitable for real-time thresholding. [Free blue noise textures](https://www.momentsingraphics.de/BlueNoise.html).

For BrineSpace, start with water/fog gradients and leave crew, machinery highlights and interface untouched. This requires useful masks or drawing-order separation; the current viewport rectangle alone cannot select those materials. Do not animate the noise by default. A static screenshot cannot establish whether a pattern crawls over a panning floor or breaks up a moving face. World anchoring can help some surfaces, but does not by itself solve zoom, rotation or independently moving sprites.

### Upscaling filters are a different category

xBRZ is explicitly an image-upscaling filter for low-resolution inputs. It is worth knowing about, but would not be my first route to making this game's current scene more convincingly pixel-art-like. [xBRZ implementation and description](https://github.com/kayahr/xbrz). Test any such scaler at the actual input/output relationship; a polished enlarged emulator screenshot is not evidence for a mixed-resolution station with free zoom.

## Other filters with a plausible benefit

### 1. Colour grading — first priority

A colour grade transforms colour relationships without discarding spatial detail. It can make the sea, metal, cloth, lamps and foliage feel as if they belong in the same lighting environment. LUTs are an established way to represent complex colour transformations efficiently. [GPU Gems 2: Using Lookup Tables to Accelerate Color Transformations](https://developer.nvidia.com/gpugems/gpugems2/part-iii-high-quality-rendering/chapter-24-using-lookup-tables-accelerate-color).

Proposed starting direction: keep cool ambient water; preserve near-neutral steel and AI-white; gently favour warm practical lights; increase separation of useful midtones without turning unlit areas grey. Preserve red warning signals and departmental differences. Compare at low blend strengths before committing a palette shift. These are art-direction hypotheses based on the retained captures.

Do not stack a new teal cast blindly over the existing atmosphere grade. Validate colour-space assumptions as part of implementation, particularly for averaging, brightness curves and threshold effects. [GPU Gems 3: The Importance of Being Linear](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-24-importance-being-linear).

### 2. Selective bloom and contrast — first priority

The game already has bloom, grade, snow, grain, fringe, water blur, shadow, fog and light spill in `screen_atmosphere.gd`. The recorded owner adjustments in `title_settings.gd` explicitly reduced darkness, grain, blur, bloom and colour fringe. Tuning the relationships between existing effects is a better initial experiment than adding another copy of them.

Candidate: preserve the lamp glow while keeping the edges and specular detail of machinery crisp. Luminance thresholds alone cannot distinguish a lamp from a bright white wall; more selective treatment may need an emitter/material mask. Low-strength local contrast may separate props from floors, but avoid amplifying every floor seam or making darkness reveal undiscovered geometry.

Godot 4.7 lists glow and colour adjustments for Compatibility, while HDR 2D remains unavailable there. Existing custom screen-space glow therefore does not imply that we should switch renderers or introduce an HDR pipeline. [Godot 4.7 renderer comparison](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).

### 3. Edge-preserving smoothing — targeted experiment

Bilateral filtering is a relevant family for smoothing local variation without treating every boundary like an ordinary blur. [Paris and Durand, Fast Bilateral Filter research](https://people.csail.mit.edu/sparis/bf/).

My proposed use is very selective: quiet repetitive floor or distant seabed detail so machinery and characters stand out. A whole-scene pass can remove just the details that make a small sprite readable. Start with an explicit floor/background mask. Neighbourhood kernels cost more than a simple colour transform, so this belongs after the inexpensive first trials.

### 4. Painterly/Kuwahara abstraction — stronger alternate art direction

Anisotropic Kuwahara filtering follows local image structure to produce painterly regions while retaining directional features. The authors also discuss temporal coherence. [Kyprianidis, Kang and Döllner](https://www.kyprianidis.com/p/npar2009/).

This could connect disparate textures into an illustrated station look. It also risks turning mechanical components into waxy patches and removing face or equipment detail. Treat it as a separate preset, initially weak and restricted to background surfaces. A small basic Kuwahara implementation is not equivalent to the paper's anisotropic algorithm or its coherence results.

### 5. Contour/ink effects — alternate style or selection aid

Thin contours could improve prop silhouettes, but a full-scene colour-edge detector also finds floor scratches, interior panel lines and lighting transitions. A silhouette outline based on sprite alpha or an object mask is a different, more targeted operation.

XDoG is a research-backed family for ink/pencil and related stylization, not a semantic object-outline detector. [Winnemöller, Kyprianidis and Olsen, XDoG](https://www.kyprianidis.com/p/cag2012/). Try a weak technical-illustration preset if desired; use targeted silhouettes for a readability experiment rather than applying black outlines to every screen edge.

### 6. Adaptive sharpening — conditional

CAS adjusts sharpening according to local image contrast. It offers a better reference than an unrestricted sharpening slider. [AMD FidelityFX CAS](https://gpuopen.com/fidelityfx-cas/).

Worth auditioning at low strength only if the current camera scaling is visibly soft at the player's normal zoom. It cannot recover detail removed by coarse pixelation and can emphasize existing texture or halos. The provided FidelityFX SDK is not a drop-in dependency for this OpenGL Compatibility project; a suitable fragment implementation or simpler bounded filter would need its own review and profiling.

### 7. Tilt shift / diorama — keep optional

The current adjustable focus band is a screen-position blur. It can give a miniature feel, but it does not know room height, crew importance or actual object distance. At low settings it is worth keeping in the audition. At higher settings it can obscure useful activity near screen edges.

HD-2D is a broader rendering/art direction: Square Enix describes Octopath Traveler II as 2D characters in a 3D world. A blur filter alone cannot reproduce that scene construction. [Square Enix's official description](https://www.square-enix.com/asia/newsportal/en/sg/octopathii/). A future importance-aware focus treatment would need masks or scene information rather than assuming a 2D station has a usable camera-depth buffer.

### 8. CRT / phosphor / scanlines — themed option

CRT shaders vary substantially in their phosphor masks, scanlines, bloom, distortion and multi-pass reconstruction. Libretro documents distinct families and a parameter-heavy CRT-Royale implementation. [CRT shader catalogue](https://docs.libretro.com/shader/crt/), [CRT-Royale](https://docs.libretro.com/shader/crt_royale/).

This fits a BRINE monitor, comms portrait or surveillance view more naturally than the entire station. For a world-view experiment, start with a very light static treatment and no curvature or moving interference. The game's fine text and lines make strong masks/scanlines an unattractive default candidate. A full CRT-Royale chain is considerably more integration work than a small Godot canvas shader; screenshots and parameter presets are references, not drop-in code.

## Proposed audition order

First compare isolated effects on the same scene: a grade with no pixelation; brightness posterization without dither; an authored palette without dither; then the same palette with Bayer and blue noise. This establishes which ingredient helps before combining them.

If those comparisons are useful, build these modest presets:

| Preset | Ingredients | Intended question |
|---|---|---|
| Original | Existing game appearance | Reference, always available |
| Clean underwater | Restrained grade + tuned existing light glow | Can lighting/colour unity improve the current detail? |
| Fine pixel | Current small grid + better sampling/stability comparison | Does a light pixel structure help in motion? |
| Illustrated station | Gentle luminance steps + restrained grade | Can simpler brightness make props read more clearly? |
| Palette station | Custom 64/96/128-colour trials; dither separately switchable | Does a deliberate palette create the desired identity? |
| Miniature station | Best-performing base + very mild current tilt shift | Does focus add depth without hiding useful activity? |

Painterly, contour and CRT options follow only if the owner wants a larger style departure. This recommendation does not imply all six presets should be combined or shipped.

Controls should stay understandable: preset, overall strength, and only the controls meaningful to that preset. Preserve the original A/B toggle and sharp interface. Existing pixel, blur and focus sliders remain useful; there is no reason to expose a dozen technical parameters simultaneously.

## Implementation implications specific to this project

The project currently selects `gl_compatibility` in `project.godot`; the retained actual-game logs confirm OpenGL 3.3 Compatibility. Ordinary 2D fragment shaders and colour textures are the appropriate first path. Compute shaders, CompositorEffects and HDR 2D are not available in this renderer. A general engine feature table is also not proof of access to 3D depth/normals for this Control-based 2D game. [Renderer comparison](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).

Godot's first screen-reading shader triggers a back-buffer copy; overlapping screen effects do not automatically read one another's output. Our existing atmosphere plus audition already has explicit ordering/copying to address this. Adding a node per effect without considering that order can silently bypass earlier effects or add unnecessary copies. Also, region-limited copies must include the neighbourhood read by blur/outline kernels. [Godot 4.7 screen-reading shaders](https://docs.godotengine.org/en/4.7/tutorials/shaders/screen-reading_shaders.html).

Prefer combining simple colour operations in an existing compatible pass when an implementation is chosen, while keeping off truly off. Treat extra screen copies, blur mip generation and neighbourhood sampling as real costs. No FPS or iPad suitability claim follows from the technique being described as “real time” elsewhere.

A useful inspectable Godot example combines luma/RGB quantization with ordered or texture dithering. It is an implementation reference, not evidence for this game's appearance or performance. [Author's shader and examples](https://godotshaders.com/shader/retro-luma-color-reduction-quantization-posterize-dithering/).

## How to decide whether an audition improves the game

Use the retained station, a busy larger station, a dark exterior/harvesting view and a crew close-up at the actual normal play zoom. Hold scene, lighting and quality settings constant when comparing. Check paused images, then normal movement, camera pans and zooms; animation and sampling stability cannot be accepted from a still.

Judge whether crew remain recognizable, small equipment remains legible, resource/department colours stay distinct, lamps preserve shape, dark exploration stays appropriately dark and the interface remains exact. The desired result is a more coherent station that is still pleasant to watch for a whole loop. Reject effects that look interesting in a crop but make that play view less readable.

Profile only the candidates that survive that visual review, on the same workloads and actual Windows/Mac/iPad paths. Compare frame-time distribution, extra render-target/copy costs and memory; do not infer improvement from average FPS alone. No new tests, renderer switches, asset conversions, game restarts or benchmarks were run for this research.

## Evidence and remaining uncertainty

Primary sources linked above include engine documentation, original papers/research pages, author-written shader explanations and the relevant tool owners. Repository evidence: project.godot, scripts/look_audition.gd, scripts/screen_atmosphere.gd, scripts/title_settings.gd, the live audition handoff and retained October 18 game captures.

Established: technique distinctions, current shader behaviour, renderer selection and important integration constraints. Proposed: artistic priorities, palette sizes, masks, preset names and starting directions. Unestablished: which new treatment the owner prefers, whether it improves sustained play, and its cost on supported hardware. The research does not change the current game's visual default or accept a new style.
