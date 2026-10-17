# West stutter repair candidate

Owner accepted east v1 and reported west stutter. All six east PNGs and east
timings are unchanged. West combines v1 source/export frames 2/0/1 (zero-based)
with three new opposite-half poses, no mirroring or synthetic interpolation.
West timing now evenly spaced 150ms per frame, total900ms.

Built-in image_gen used only the approved side master for new poses; exact prompt
and raw RGBA source preserved. build_review.py performs extraction/registration,
manifest and GIF packaging. Validator passes. Runtime unchanged.

west-before-after.gif: old left/new right, enlarged and gameplay-scale views.
west-contact-sheet.png: six chronological revised poses.
New poses show more far-side canister exposure and some body-detail variation.
This remains a visual-review candidate; no native foot-plant/stride calibration
or claim of fully resolved stutter. Next assess the loop, then tighten gear joins.
