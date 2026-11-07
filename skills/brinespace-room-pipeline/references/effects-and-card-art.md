# Sea life, effects and card artwork

Use for ambient fauna art, underwater lighting textures and card UI artwork.
The current visual bible owns style; existing consumers own motion and geometry.
For companion identity or new NPC behavior, also use the character pipeline.

## Establish the rendering contract

Inspect the actual consumer before producing art. Record native size, draw extent,
alpha role, filtering, tint, pivot, animation clock and state/quality behavior.
Use explicit whole res:// paths, validated raw-image loading and the existing
procedural/flat fallback. Cache invalid assets and warn once rather than every frame.
Preserve resource and gameplay rules while changing appearance.

Measure apparent density from world draw extent divided by source pixels, or from
physical screen pixels after the viewport transform. Master resolution alone is
not a density measure. Ambient fauna, distant large silhouettes, linearly sampled
optical fields and tiny UI symbols can have different contracts; record deliberate
exceptions rather than forcing one pixel ratio onto all of them.

## Separate material, color and opacity

Card frames use neutral matte metal with visible dark fitted seams and restrained
raised detail. Department identity is a separate continuous colored inner outline
whose outer edge touches the metal's inner edge. Current card geometry: 200x284;
metal inner edge at 6px, inner outline 2px, matching rounded corners. Stock fill/opacity is
independent from opaque metal; existing whole-card affordability modulation remains.
Department and selection colors come from the current consumer, not a new palette.

When details disappear, inspect source luminance range, bake transfer, runtime tint,
alpha, layer order and actual sampling separately. Mapping every source value toward
white erases dark joints even if alpha is fully opaque. Correct the failed stage;
do not apply blanket darkening or grade every creature/room to teal or grey.

A panel background draws before its child content. A correctly located outline can
still be hidden by title/art/rules panels. Render the inner outline above content
without participating in container layout or input handling; retain state colors,
fallback behavior and resize updates. Review all four sides and rounded corners.
For TextureRect marks, set EXPAND_IGNORE_SIZE before texture/size so source 64/48px
art does not silently enlarge intended 16/12px emblems and rarity marks.

## Produce and preserve

Use imagegen for new painted image sources and image repairs. Preserve immutable
masters and exact prompts. Existing simple UI symbols and procedural light bands
can be exported through their deterministic native geometry instead of replaced
with decorative generated imagery. Keep those roles explicit in provenance.

A reproducible pack contains sources, prompts/algorithms, bake, exports, manifest
with hashes/dimensions/pivots, validator and native review. Rebuilding must not call
a generation service. Store raster art through Git LFS; keep script/UID pairs.
Separate installed textures from studies: current warm/cool halos, caustics, hull
bubbles and beacon are installed; three shafts and the wide pool are review-only.
Do not wire studies merely because their PNGs exist. Keep clocks, radius, tint,
brightness, quality and Reduced Motion behavior from existing consumers.

## Native review and checks

Show a full card/effect at actual gameplay scale plus an enlarged diagnostic crop.
A contact sheet alone may hide seams. Derive crop coordinates from the actual
viewport/global/final transforms, then verify a full-screen/crop pair. Distinguish
1920x1080 design coordinates from a 1600x900 captured image. Use revision-specific
preview filenames so the desktop image cache cannot show an earlier result.

For card styling, preserve a real before baseline and compare card/text rectangles
at 960/1280/1600/2560 widths. Wait for observable startup/layout stability and rendered
frames rather than a fixed delay. Normalize JSON numeric types before exact geometry
comparison; do not replace the baseline or loosen tolerances to obtain a pass.
Use tools/check_card_art.py for isolated runtime/native checks and
assets/sea-life-v1/cards/validate.py for source raster/hash/rebake checks.
Lighting equivalents are tools/check_lighting_art.py and the lighting pack validator.

Every Godot fixture uses scratch APPDATA/LOCALAPPDATA and compares real owner-profile
fingerprints. Choose checks for changed behavior: alpha/tint/fallback/mark size,
pause and quality handling, input drag if layering changes, and native visual review.
Once relevant checks pass, repeat only for a new change or unresolved concern.
Keep source quality, engine evidence, owner acceptance and release acceptance separate.
Refresh release dependencies from the intended final tree before exporting; exclude
masters and review files. A local manifest refresh is not a playable-release test.

## Session closeout

Keep accepted rules in the bible and procedural lessons here; place dated checks,
commit IDs and remaining work in the session handoff. Do not carry an older batch
TODO forward after the owner moves on. Stage only owned files/hunks in shared scripts,
docs and generated metadata. A shared index lock is not permission to remove it or
commit somebody else's work. Use an isolated codex/ branch/worktree when needed;
verify a complete HEAD index, LFS pointers and staged paths. If a deliberately
limited authoring checkout is used, label it and do not treat it as a runnable build.
Record whether tests exercised the shared working checkout or the exact commit.

Session evidence: docs/ART_SESSION_CLOSEOUT_2026-09-29.md and each pack HANDOFF.md.
