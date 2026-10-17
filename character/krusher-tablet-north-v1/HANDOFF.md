# Project handoff

Updated: 2026-10-03 | Project: BrineSpace | Task: Krusher North head turn

## Objective and acceptance
Continue selected James utility Krusher with a source-matched North tablet glance. New authored angled head sources and a bare draft; North remains incomplete.

## Accepted decisions and constraints
Krusher Dom, System Administrator, AI & Robotics, matte muted cyan #527C80, James utility suit. Preserve body/tablet/source clocks and exact canonical joins. No normal selection or NPC changes.

## Current state
krusher-north-head-turn-v1 retains built-in image_gen rear-right source and two-head intermediate atlas, reference board and exact prompts. A significant-alpha bounding box (>128) excludes faint background speckles; cropped alpha retained, one24px-width Lanczos extraction per authored view. Original rear24x23, partial24x25, read24x23. Intermediate atlas second head retained but unused. Named angle requests are not verified numeric camera angles.

krusher-tablet-north-v1/build_action.py builds all137 original body poses/5500ms. Three discrete views: rear0..10/128..136, partial11..21/120..127, read22..119. This is a draft mapping, not a full reconstruction of gradual source head rotation/pitch. Collar45, head bottom45 with original source head top/axis tracking. Head edit limited x<108 to protect tablet. Body/tools/clock preserved outside masks; upper suit yellow recoloured muted cyan. Exact full-RGBA start and return idle-north joins.

## Verification and limits
413 composition checks, zero failures. 561 independent checks, zero failures. Validator checks current hashes, state clocks, outside-mask/tablet pixels, generated-head hashes and endpoints. Density board, all137 original head crops, four registered key poses and explicit view-boundary sheet viewed. Source-derived5.5s preview180955bytes. No native run yet for North and no temporal artistic acceptance; endpoint/protection tests do not prove smoothness.

## Next action
Refine the discrete head transitions against gradual original source turn, including pitch and relative head/collar size. Review actual motion at common scale before helmet fitting. Then add North bare/equipped and all cardinal actions to combined canonical package and verify native joins. Goal active; existing East/South/West preserved. No commit/publication/export.
