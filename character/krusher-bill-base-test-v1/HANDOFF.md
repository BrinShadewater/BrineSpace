# Project handoff

Updated: 2026-10-02 · BrineSpace · Krusher Dom / Bill body reuse trial

## Objective and acceptance
Owner requested testing existing crew models as reusable bases. Deliver a derived
Krusher standing/idle and short walk comparison before larger adaptation.
Visual owner selection of this body/head combination remains pending.

## Accepted decisions and constraints
Krusher Dom, System Administrator, AI & Robotics, muted matte grey-cyan markings.
Reuse Bill's actual selected matte body, not a newly generated approximation.
Separate unselected trial; original libraries and gameplay selection preserved.

## Current state
`build_test.py` extracts a 23×28 native head from the accepted concept front view,
recolours red suit markings to luminance-preserving muted cyan, and fits the head
to each source skull/face position. Source concept crop and native component kept.
184×184 canvases, pivot (92,172), standing ruler148. Exact original durations/loops.
132 exported frames: idle-south73 /3042ms, walk-south59 /2458ms. Original body RGBA
outside explicit edit masks preserved exactly; feet/lower body exact.
`manifest.json`, per-frame masks, source hashes and `verification.json` retained.
`review/standing-comparison.png`, paired GIFs, exact transparent APNGs, sampled neck
board and interactive `review/index.html` provide comparison and playback.

## Verification
`validate_test.py`:669 checks,0errors. All132 APNG frames decode exactly; originals
unchanged, timing/loop equal, no canvas-edge clipping, lower body/feet exact.
Agent viewed standing/native-scale comparison,15 sampled neck crops and browser
idle/walk playback samples. Corrected source head axis remains90–92px for walk,
92idle. Body likeness/readability promising; no formal full-motion/owner acceptance.
No Godot run needed for this source-only trial; owner save folder not touched.
Initial action attempt revealed its256canvas; action omitted rather than forced
onto184. Initial warm-region walk mask included collar/markings and shifted head;
corrected using crown-band axis and bounded face region. APNG disposal corrected
to background after decode check failed. Lower-body validation starts112, after
the explicitly recoloured belt region. Final source/package checks pass.

## Next action
Owner review of Bill build with Krusher head; then cardinal head masters and
pose-aware matching on other directions, shared helmet fitting and custom terminal
equipment/action. No mirroring assumed. This trial retains Bill's equipment;
static head has no independently authored blink/turn/expression. No actor integration
or other crew-base variations yet. Broad library generation remains out of scope.
