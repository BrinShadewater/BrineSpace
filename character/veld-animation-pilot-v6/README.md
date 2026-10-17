# Veld v6 material consistency

Extends v5 colour processing with bounded masks for brown hair, the separate silver
streak, ivory chest modules and bright steel. Authored anchors still come directly
from crew-turnarounds-v4/palette-reference.json. Brown hair never uses the silver
anchor. Ramps preserve intermediate shading rather than posterizing to flat colours.

All 24 frame alpha masks are byte-identical to v5. Poses, registration, timing and
the two exact inspection/idle joins are unchanged. Generated sources are retained
unchanged; this pass is deterministic colour processing only.

Run build_pilot.py, run_native_review.py, then build_review.py from this folder
using Python. The native wrapper isolates APPDATA and fingerprints the real save
folder. Final: 100 native checks pass; all 2670 real-profile files unchanged.
The sprite validator reports no errors/warnings. Source-scale contact sheet,
diagnostic mask and native render inspected.

These are bounded colour/position masks, not hand-labelled per-pixel segmentation.
Very small neutral logos/fasteners can share the bright-steel ramp, and dark metal
shadows remain outside the conservative steel selection. Tiny instrument lights
are retained. These edge cases still warrant review before production selection.
No runtime art has been replaced. Remaining direction and helmet coverage follows.
