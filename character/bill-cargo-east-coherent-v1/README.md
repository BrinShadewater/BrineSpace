# Bill bare east cargo candidate

Current revision detail-v6: owner accepted the darker direction but found the face
too dark and suit detail reduced. Skin now receives a local brighter remap; the
hair mask excludes bright forehead pixels that it previously darkened. Hair and
metal base remain at matte-v5. Source seam/panel shading recovered using masked
high-frequency cloth detail (2.2px source radius, gain1.1, residual limit18),
excluding silhouettes, skin and silver. No invented panels or regenerated poses.
Parameters recorded in registrations. Before snapshot review-before-detail-v6;
close comparison in detail-comparison.png; full-cycle browser at detail-v6.
122 packaging/43 grade checks pass, plus23 alpha comparisons to detail predecessor.
Selected sample cloth medians50/50/51.3 vs idle46.3; face/detail owner review pending.
Motion/registration/timing unchanged. Cargo remains staged.

Prior revision matte-v5 supersedes the partial grade-v4 pass. Owner still saw
animated brightness drift; carry/unload had retained the earlier brighter grade.
matte_grade.py now calibrates one neutral tone curve per original source sheet
against selected idle (standing neutral body, head/cargo excluded). Apply that
frozen curve to all poses in that sheet, with separate hair/skin/burgundy masks;
no per-frame normalization. This covers pickup, carry, unload and ground cases.
All23 alpha planes, all timing/metadata and exact action joins preserved. Selected
idle pixels remain intact outside the ground case's existing boot-edge occlusion.
122 packaging/43 grading checks pass. audit_materials.py saves quantitative
evidence: sampled cloth medians47.7/48.3/49.0 vs idle46.3; carry bright fraction
falls0.113 to0.050 vs idle0.045. These support, not replace, visual review.
Masks and82/54/27px dark/light views inspected. Snapshot in review-before-matte-v5;
browser compares full cycles at matte-v5. Still staged; owner review pending.

Prior color revision grade-v4: owner found pickup-v3 too bright. Deterministic
material remap from preserved raw source restores darker graphite, muted silver,
brown hair, softer skin and burgundy. No source regeneration or geometry changes.
One fixed curve/multiplier set across the pickup; parameters in pickup-registration
and implementation in refine_pickup.py. Spatial head masks prevent burgundy from
being mistaken for skin; grade-masks includes inspected standing/crouch/rise masks.
Bright predecessor preserved in review-before-grade-v4.134 packaging and55 color
preservation checks pass (`verify.py`, `verify_grade.py`). Browser compares bright
and corrected full cycles at grade-v4. Color owner review pending, still staged.

Three staged clips: pickup-east (11 selected poses), carry-east and unload-east
(six poses each). Pickup smoothing revision pickup-v3 retains 520ms, adds authored
intermediates, preserves both exact endpoints and all 12 carry/unload frame hashes.
134 packaging checks pass. Largest crown step is20px versus32px in cargo-v1.
Preview compares full cargo cycles and supports manual pickup pose stepping.
Sources pickup-smooth-v2.png and pickup-smooth-v3.png and their exact prompts
are retained. v2 had a large crouch-to-lift jump; v3 corrects the lift. Source
pose10 overshoots standing size, so final selection uses cells1..9 between the
retained endpoints without per-pose scaling. Burgundy remap recorded in
pickup-registration.json. New original source files:
exec-220e0202-3877-4c61-9a40-65a70f954a5b.png and
exec-7016fec1-35f1-4a16-81c7-0f7f03c41721.png.

The initial cargo-v1 pass had six poses in each clip:
Built-in image generation supplied whole figures; exact prompts and both raw
sources are preserved in this folder. Initial carry row repeated stride phases;
actions-gait-v2.png is the selected correction. Original generated sources:

- exec-74c2b50e-be96-41d6-8f86-45a35f47ea1b.png
- exec-ffee340c-24bb-4171-a83a-a5a90ca3defa.png

Both remain in C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f.
One fixed neutral anatomical calibration for the whole pack; crouches retain
their authored height. Preserve detached ground cases by their authored cell,
register standing endpoint bodies to the actual selected idle, and keep current
legacy timing/stride/profile metadata. Pickup and unload share exact resting and
held-case endpoints. Carry uses six distinct authored walking poses.

Rebuild: `python character/bill-cargo-east-coherent-v1/build.py`, then
`build_review.py` and `verify.py` in this folder. Initial99 packaging checks passed;
contact and 82/54/27px dark/light samples reviewed. Browser has six before/after
tracks and gameplay-height controls in cargo-v1; current revision compares two
complete cycles. This candidate is not yet bound to runtime:
remaining directions, matching helmet variants and derived carry turns must be
handled together before integration. No gameplay/controller timing changed.


## Installed selection — September30,2026

Bill's actual grid loader now appends all four cargo profiles,paired helmet packs,
and the full carry-turn matrix. Native test_bill_cargo_selected passes1615 checks
covering selected pixels,registration,paired timing,all directed turn clocks,
gait restart,NPC cargo-state selection and explicit scratch user:// resolution.
Native offscreen selected half-turn contact view:output/bill-cargo-native-v1.
Owner acceptance and whole-station movement settling/turn/resume polish remain
separate. Earlier staged statements above describe the source milestone.

The selected locomotion stride fields now remain authoritative:Bill's partial
action/timing/fitting loads opt out of inherited legacy stride imports. Cargo
manifests/builders override only carry=.12. Generic player behavior defaults remain
unchanged for other actors.1600ms authored half clocks now reach the actual loader;
pickup/unload/carry simulation timing remains unchanged.
