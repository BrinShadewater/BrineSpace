# Project handoff

Updated: September 28, 2026 · BrineSpace · Bill direct north loop

## Objective and acceptance
Owner accepted direct v2 source with "looks good, lets keep going". Extract a complete alternating stride and show it beside installed directions before promotion. Source approval is recorded; the newly cut/retimed loop is a candidate.

## Accepted decisions and constraints
Preserve approved master, dark matte suit, brown hair and fixed registration. No new generation, pose interpolation, frame-by-frame resizing, extra finish pass or mirrored views. Keep existing native runtime while reviewing this cut.

## Current state
`character/bill-north-loop-v3/build.py` deterministically copies direct v2 frames 91-120 (30 consecutive poses) into a complete cycle. Source period is 1250ms at 24fps; selected playback is 1500ms (50ms/frame), matching all installed Bill walk directions. Manifest retains the existing stride distance 69/384 cells, 184-square canvas, (92,172) pivot and 148px standing reference. Source video hash and exact copied-frame hashes are saved. No API calls or costs this turn.

Review: http://127.0.0.1:8791/character/bill-north-loop-v3/. Canvas compares south/east/new-north/west/installed-north at inspection and 82/54/27px reference heights. Pause, phase scrubber and speed controls permit seam/pose comparison. The full approved source remains linked. Build does not alter the runtime or the source review folder.

## Verification
Inspected sequential every-other-frame stride sheet to identify both alternating steps. Five-frame neighborhood seam search ranked 91->121 lowest among tested 24-48-frame windows. Selected wraparound foreground MSE 0.01129 is below largest internal adjacent transition 0.01300 (median 0.00893); supporting evidence only. 30 copied frames match source hashes exactly, zero clipping. Selected alpha>127 heights range 139-145px; body motion remains unnormalized. Neutral material median ranges RGB (56,54,55) to (58,57,57).

Browser comparison visually inspected, all images reported loaded, pause/phase/play controls exercised. These observations and contact sheets are not a claim of full temporal gait acceptance or native engine verification. No Godot tests or owner-save writes were needed.

## Next action
Owner reviews loop pacing/seam and directional match. If accepted, install just this walk-north state with previous-manifest backup, preserve unrelated states byte-for-byte, update selected hashes/acceptance, and run the existing isolated crew validation/native fixture. Old north idle remains a separate transition/proportion check. Branforth side gait follows this Bill milestone; Higgsfield free run remains reserved.
