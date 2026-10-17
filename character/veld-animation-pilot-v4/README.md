# Veld pilot v4

Adds a six-frame right-facing breathing idle to v3's front idle, right walk and
inspection. Total: 24 frames, 184x184, pivot 92/172, standing height 148. Sources,
prompts and deterministic colour processing are retained. Existing runtime packs
remain unchanged. The old front idle is shown opposite new idle-east because v3
had no matching direction; other comparisons use the same state from v3.

Build: `python character/veld-animation-pilot-v4/build_pilot.py`.
Native capture: `python character/veld-animation-pilot-v4/run_native_review.py`.
Review page/media: `python character/veld-animation-pilot-v4/build_review.py`.

The native wrapper isolates APPDATA and fingerprints the real profile before/after.
Final run: all 2670 real files unchanged; 97 sprite-player checks pass, 24 native
captures at source and 45px standing scale. A preliminary v3 diagnostic found only
nanosecond phase rounding at exact frame boundaries; sampling inside each frame
avoids that ambiguous assertion. No runtime clock change was needed.

V3 planted-foot measurements remain applicable because the walk PNGs are unchanged:
flat-foot residuals +1.73 and -1.27 source pixels (about +0.53/-0.39 at 45px height).
They exclude heel-roll/toe-off and do not certify station occlusion or zero sliding
during held frames. Inherited stride is retained, not guessed from bounding boxes.

Remaining: full material masks for hair/ivory/steel, inspection orientation/joins,
additional directions and helmet states, native station integration. Candidate
coverage and native playback checks do not imply owner visual acceptance.
