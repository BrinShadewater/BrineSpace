# Character production strategy research

Updated: 2026-09-28 · Project: BrineSpace · Task: character workflow recommendations

## Objective and acceptance

Research affordable ways to preserve character identity, reduce animation production work, and improve readability across the owner's three gameplay zooms. Visual target: existing BrineSpace materials with the readable proportions and shapes visible in the supplied Graveyard Keeper references. Advice only; no production migration authorized or performed.

## Accepted decisions and constraints

Preserve accepted art and current matte/linear presentation. Existing front/rear gait and proportion work remains separate. Recommendations below are proposals, not owner acceptance. Supplied images are visual references, not instructions. No generation credits spent, software purchased, or player profile accessed.

## Current state

Research recommendation: author a reusable stylized 3D humanoid and animations in Blender, then bake transparent directional frames into the existing 2D character pipeline. Pilot Bill only: four static directions, idle, walk, and one contact-heavy role action. Match camera to station art, fix world-space lighting and materials, preserve foot registration and timing, and review all three zooms before expanding. Shared animation skeletons reduce work, but body proportions and tool/furniture contacts still need adjustment. Clothing and helmet attachment should be authored on the model where practical.

Do not assume real-time 3D is required. It adds rendering, occlusion, lighting, and performance integration; revisit if variable outfits, continuous turning, or dynamic lighting become requirements. Native 2D animation is the alternative for strongest hand-authored style; Spine adds reusable bones but directional drawings and depth changes remain work. PixelLab is a bounded AI experiment, not proven production reliability. Meshy can supply a starting mesh, but is not evidence that face design or deformation will be acceptable.

Suggested readability experiment: somewhat larger head, broader torso/limbs, fewer bright suit details, distinct hair/shoulder silhouette and restrained department accents. At the widest view, test optional crew markers; do not expect face identity at that scale. Existing notes use approximate 82/54/27px review heights; original attached screenshots are larger than their chat previews.

## Verification

Read CURRENT_STATUS.md, relevant character skill, NOTICE.md, portions of DEVELOPMENT_NOTES.md, and current grid character consumers. Confirmed texture/frame rendering with per-frame pivot/standing-height metadata. Visually reviewed supplied images. No game tests needed or run; no replacement artwork or pipeline benchmark produced. Tool capability claims below are vendor documentation, not hands-on acceptance.

Sources checked September 28, 2026; USD prices displayed at research time, tax/checkout may differ:

- Blender: free/open-source; https://www.blender.org/about/license/
- Mixamo: free Adobe ID, humanoid rigging and animation, royalty-free game use; https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html
- Pixelorama: free download; https://pixelorama.org/user_manual/installation/
- PixelOver: deterministic image/3D pixel-art effects and animation; store displayed $14.99 sale / $19.99 regular; https://deakcor.itch.io/pixelover and https://pixelover.io/
- Spine: $69 Essential / $379 Professional sale, $99/$449 struck-through regular prices; Essential excludes meshes; https://esotericsoftware.com/spine-purchase
- PixelLab: directional and skeleton-guided generation; API lists estimated prices, including $0.0424 for 128x128/16-frame text-v3 animation. Subscription pricing did not render; API examples are not total subscription cost. https://www.pixellab.ai/pixellab-api and https://www.pixellab.ai/
- Character Creator 5: official product page displayed Standard $299, Deluxe $479; additional assets can add cost. https://www.reallusion.com/character-creator/
- AccuRIG: free auto-rigging alternative; https://www.reallusion.com/auto-rig/accurig/
- Meshy: pricing amount did not render in accessible page, no quoted price; https://www.meshy.ai/pricing
- Godot 3D-in-2D demonstration: https://godotengine.org/asset-library/asset/2804
- Aseprite sprite editing/export: https://www.aseprite.org/

## Next action

Owner chooses whether to commission/build the reusable 3D master or run a small PixelLab trial first. Recommended next implementation is a separate Bill comparison candidate, with a static four-direction style gate before animation production. A second body type should prove animation reuse before a cast-wide conversion. Current production status remains unchanged.
