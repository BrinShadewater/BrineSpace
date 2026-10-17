# Veld west four-keyframe regeneration

Owner liked latest character appearance but reported stuck walking. Built-in
image_gen used the latest master-v1 sheet as appearance reference, explicitly
rejecting its repeated poses. Exact prompt and raw RGBA source preserved.

Four newly authored poses in 2x2 source: contact/pass/contact/pass. Second contact
has distinct forward near-arm swing; final passing knee silhouette differs.
Single clip-wide scale, no per-frame normalization, no palette edits. 184px frame,
148px median body height,900ms cycle. Head/collar band31-32px; bounds147-149px.

walk-review.gif: approved standing master left, new four-pose cycle right.
contact-sheet.png shows sequence. Manifest validator clean. No native playback
or foot-contact calibration, no runtime replacement. East unchanged.
Four-pose rhythm remains coarse; final knee lift and arm swing need owner review
before authoring in-betweens. Appearance reference approval is not gait approval.
Rebuild: python build_review.py.
