# Veld fitting/removal candidate — 2026-09-29

Staged candidate; owner liked the poses and requested glow removal. Runtime
installation and acceptance of the corrected preview remain pending.

## Consistency review supersedes palette iteration

Owner reports v13 has drifted too far. The wider read-only selection audit is in
../veld-consistency-audit-v1/FINDINGS.md and index.html. It identifies source
style/identity differences in face/hair, cloth detail/contrast and helmet rendering
that another palette-only correction cannot resolve. V13 remains preserved and
uninstalled; next fitting revision should start from the selected east idle/walk
identity and helmet sources rather than accumulating additional color maps.

## Material palette cleanup — current v13

Owner rejected v12's remaining hair, skin and suit shifts. Replaced the stacked
v8–v12 corrections with one pass from preserved source-v7-muted-patches.png,
keeping the clean source-v5 matte. material_grade.py draws explicit hair/skin
boundaries for each original pose; a source-coordinate review corrected the
raised-helmet head and the three aperture faces. The silver hair band is excluded
by geometry rather than excluding every gray highlight. Hair and bare skin use
one pooled-source LUT each, anchored to the installed bare idle RGB palette.
Skin through glass uses one separate LUT anchored to the installed helmet idle.
No frame-specific exposure normalization. A continuous neutral cloth curve includes
sleeve highlights; patches, brass and helmet regions are protected.

Changed build.py, added material_grade.py/review_materials.py, rebuilt candidate
frames, manifest, GIFs and checks; preserved build-v12-preserved.py for rollback.
Material masks, exact palette knots, source-coordinate overlay and selected
idle/action comparison are saved beside the candidate. All eight head/contact
poses and dark/light 82px comparisons inspected. Sixteen frame clipping/timing,
decoded-GIF exterior, exact idle endpoint and fixed-boot checks pass. Source alpha
and visible RGB outside selected masks are asserted unchanged. Pixel checks do
not certify owner acceptance. Current browser revision: material-palette-v13.
Runtime/native integration and owner acceptance remain pending; no shared actor
bindings or save folders touched. Older sections below retain rejected history.

## Sleeve and brown-hair mask correction

Owner reported suit shifts and hair becoming gray/lighter in motion. V12 freezes
the assembled v11 artwork. Earlier broad patch/head rectangles excluded adjacent
sleeve cloth from grading; they are replaced with tighter patch exclusions and
explicit face/hair polygons. A single fixed cloth curve now covers the exposed
sleeves as well as the torso. Explicit crown/bun polygons include low-chroma hair
strands, with a fixed warm-brown tonal map; the bright neutral silver streak is
excluded. Skin and helmet grading are preserved. No per-frame exposure, new
generation or pose/scale changes. Source alpha, outside-mask RGB, fixed shins/boots,
idle endpoints, timing, clipping and decoded exterior16 checks pass. Cloth sample
medians are about47–50 versus idle49–51; these pose-dependent samples are descriptive.
All eight contact/head crops inspected. Current review `brown-hair-sleeves-v12`;
corrected owner review and native installation remain pending. Curves, polygons,
source hashes and pre-pass grading report preserved. No runtime/shared/other-actor
or save changes.

## Joint face/hair/suit consistency pass (prior revision)

Owner requested all three material families be reviewed together. V11 keeps the
assembled v10 artwork and uses fixed material RGB offsets, informed by the new
grading candidate and accepted idle. Generated pose pixels are not substituted:
the v11 source changed one face shape, so only its palette is used. Skin, restrained
face highlights, brown hair, graphite cloth and silver fittings have separate
constant adjustments across the complete clip. Face-highlight masks now include
near-neutral glare that the warm-color mask missed. Patches/helmet are excluded.
Alpha and outside-mask RGB are asserted unchanged; registration, fixed boots and
idle endpoints remain exact. Source RGB under fully transparent pixels is zeroed
for clean reference reuse. Cloth samples now differ from idle by about0–2 levels.
These pose-dependent samples support the pass but do not establish owner acceptance.
All eight contact/head crops inspected; decoded exterior16, clipping, original
timing and fixed-foot checks pass. Current review `consistency-v11`; native
installation and corrected owner acceptance pending. Sources, prompts, masks,
offsets and prior comparisons are retained. No runtime/shared/other-actor/save change.

## Neutral suit grading continuation (prior revision)

Owner reported a remaining grading mismatch in v8. A read-only material probe
found neutral fabric samples around RGB63/62/61 versus idle49/49/51, with brighter
metal highlights. Selected neutral material correction is source-v10-neutral-grade.png,
composited only into neutral suit regions of the existing v8 assembly. Explicit
head, patch and helmet exclusions keep those accepted colors unchanged; v5 alpha
and fixed registration remain. Intermediate v9 is retained. Final cloth sample
medians are roughly51–54 versus idle49–51, down from62–63. These are descriptive
pose-dependent samples, not an exact perceptual-match certificate. Probe, before
and intermediate reports, sources and prompts are preserved. All eight contact
poses inspected; 16 decoded preview exterior frames, endpoints, timing, fixed boots
and clipping checks pass. Current preview is `neutral-grade-v10`. Corrected owner
review and native installation remain pending. No runtime/shared/other-actor/save
changes.

## Skin/hair correction (prior revision)

Owner liked v7 except for skin/hair color mismatch. Source-v8-skin-hair.png supplies
only warm material inside eight explicit head regions, composited onto v7 color
artwork. This avoids another whole-suit grading change: RGB outside this material
mask is pixel-exact to v7, the silver streak is retained, and v5 clean alpha is
unchanged. Faces are less orange and hair darker/more muted. All eight packaged
poses inspected on the new contact sheet. Decoded-GIF exterior checks (16 frames),
exact idle endpoints, fixed shins/boots, timing and clipping checks pass. Current
preview is `skin-hair-v8`; owner corrected review and native installation pending.
No runtime/shared/other-actor/save changes.

## Muted patches and exported glow check (prior revision)

Owner reported glow/bright arm patches in v6 and otherwise liked the motion.
Selected color source is now source-v7-muted-patches.png with the preserved v5
extraction matte. Patches are dark muted navy cloth and visor cyan accents subdued;
all eight packaged poses were visually inspected. All 16 decoded GIF frames pass
the new flat-background check: at most three RGB levels of error more than two
pixels from the opaque silhouette. Alpha, exact endpoints, fixed boots, clipping
and timing checks also pass. Revision-specific GIF/contact filenames prevent old
preview assets being reused. Existing browser tab refreshed to `muted-patches-v7`
and visually checked. No native/runtime/save changes.

## Registration and grading correction (prior revision)

Owner requested less movement and closer color grading. Source-v6-graded.png now
provides the color artwork; source-v5-alpha.png remains the clean extraction matte.
The earlier registration gave interior boot bounds up to nine pixels left of the
accepted idle. Each pose now receives translation-only measured sole registration
with unchanged scale. Rows 168–207 reuse accepted idle shins/boots, pixel-exact in
all eight fitting and reversed removal frames. This action does not step; upper
body and arm poses retain the authored motion. All eight poses were inspected on
the rebuilt dark contact sheet; the darker graphite suit is closer to accepted
idle. Source prompt and previous versions are preserved. Fixed shins/boots,
endpoints, no exterior alpha haze, clipping and original timing checks pass.
Complete motion and native installation review remain pending. No other actor,
runtime binding or player profile was changed.

## Glow correction (prior revision)

Selected source is now source-v5-alpha.png, from an alpha-only cleanup request;
source-v3 remains preserved. Exterior partial-alpha haze fell from 320,296 pixels
to three under the recorded source-resolution criterion (alpha 6–199 more than
four pixels from the solid silhouette). The builder guards against its return.
All eight packaged poses were visually inspected on the dark contact sheet:
head/helmet haze is gone, carried helmets remain empty and the equipped bun is
contained. Original canvas dimensions, registration, timing and exact accepted
idle endpoints remain. Frame clipping and timing checks pass after rebuilding.
This is source cleanup, not new native playback or installation evidence.

The earlier inspection below records the superseded v3 haze and candidate history.

The loader audit found 153 retained bare keys and 143 retained equipped keys,
alongside 20 revised bare and 24 revised equipped keys. These are selected catalog
keys, not claims of runtime exercise; derived joins remain outside this inventory.
The retained east fitting/removal sequence visibly changes body scale/materials
and uses the old orange-lit helmet.

Source v3 is packaged as eight fitting poses plus reversed removal with original
timing. The two endpoints reuse exact accepted idle pixels. Carried helmets are
empty; fitted poses contain the bun. Both endpoints, frame clipping and timing
cardinality checks pass. The source, original frame hashes and fixed registration
are preserved in checks.json and original-selection.json.

Visual inspection of all eight packaged poses found unresolved issues: diffuse
brown/blue partial-alpha haze around the head/helmet, brighter gray cloth than the
accepted idle and an interior-to-idle appearance switch. The contact sheet is
evidence of these limitations, not approval. Source v1 retained the exterior bun;
v2 introduced duplicate faces in carried helmets; v4 attempted alpha cleanup but
changed proportions/material brightness and still shows haze. They are retained
for provenance and rejected. Do not silently select v4 because it is newest.

The review page and GIFs allow complete fitting/removal playback at diagnostic and
approximately 82/54/27px standing scales. Full motion/native visual acceptance is
still pending. No runtime bindings, shared registry, other actor artwork or player
profile were changed. No Godot run was needed for this staged asset-only milestone.

Next: owner review of the corrected preview; retain the previously noted material
continuity concern as a review limit rather than overriding the owner's stated
approval of the appearance. Complete native checks when installation is requested.
Avoid another full-sheet generation merely to repair a local material/alpha defect;
use a bounded source correction with unchanged anatomy and verify the result before
packaging. Keep exact idle endpoints but inspect adjacent interior frames as well.
