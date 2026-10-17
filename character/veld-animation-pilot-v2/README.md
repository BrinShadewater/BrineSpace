# Veld refinement pilot

Owner requested consistent brightness, stable size and a corrected walk on 2026-09-27.
This preserves v1 and the selected v4 reference sheets. No runtime pack is changed.

Run `python character/veld-animation-pilot-v2/build_pilot.py`, then `build_review.py`
from this folder (or give its full path). Sources and prompts are retained locally.

Idle and inspection are stationary upright figures. Their mismatched source scales
are normalized to 148 px standing height; the walk retains one clip-wide scale to
preserve pose-dependent height. Registration uses the head band, avoiding arm-driven
horizontal drift. This does not replace an eventual anatomical root/foot-contact pass.

`brightness.py` identifies warm head, blue material and neutral cloth regions, and
matches their median luminance to pooled idle source measurements. Scalar RGB gains
preserve source hue and detail; masks are feathered to avoid hard colour seams. It
does not enforce the selected 24 exact palette swatches. Measurements are computed
on the same source masks before/after, in normalized sRGB luminance (not physical light).
Keep highlights and material identity under visual review; aggregate colour metrics
alone cannot establish visual acceptance.

The comparison shows v1 on the left and this revision on the right, at enlarged
and approximately station scale. Walk source revisions are retained for provenance.
Final acceptance requires actual motion/foot-contact review and native game-scale
review before replacing runtime art. No Godot probe or owner save access is needed
for this standalone candidate.
