# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Krusher animation consolidation

## Objective and acceptance
Deliver reviewable Krusher art and animation reuse with consistent source size, density, body motion and equipment. Existing normal selection remains unchanged.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics / matte muted cyan. Bill supplies the demonstrated body. Preserve sources, directions, per-frame clocks, strides and registration. No extra full crew action catalog is implied by this trial.

## Current state
bare-manifest.json and helmet-manifest.json consolidate four-direction idle/walk and west terminal raise/type/lower into 11 states each. 970 unique PNGs / 986 frame references. Terminal idle aliases locomotion idle; held action joins alias one pose file. build_package.py copies exact bytes, provenance.json records source hashes; validate_package.py checks package metadata and source fidelity. native/review.gd is assembled from retained stage/probe fragments by build_probe.py. run_native.py uses scratch APPDATA and the real existing CrewSpritePlayer.

## Verification
Package: 3,015 checks, zero errors. Godot 4.7.2 existing-consumer probe: 3,967 checks, zero errors, exit 0 / 6.55 seconds. Every frame midpoint resolves to exact source image pixels in both gears; helmet admission, registration, filtering and clip duration pass. Three native samples retained; terminal capture visually inspected. All 2,930 fingerprinted owner files unchanged. PNG Git LFS attribute verified. No editor imports, gameplay controller edits, normal selection changes or owner acceptance claim.

## Next action
Finish artistic continuous-motion review using the compact MP4 and existing native captures. The consumer's elapsed API clamps; loop callers must explicitly use modulo. Additional expressions/turns/action directions require actual consumer needs and source work; other base families remain proposed rather than tested. Actual station/controller integration is outside the evidence collected here.

## Complete package playback milestone
native/motion.gd (assembled from motion.inc and the same stage) uses the real existing consumer on one uninterrupted timeline, with per-state elapsed selection and two 22,480 ms cycles. run_motion.py isolates APPDATA. Godot 4.7.2 exit 0 / 50.37 seconds; all 986 paired pose events retained. validate_motion.py: 4,444 checks, zero errors; finish overrun 6.669 ms, maximum selection latency 19.295 ms, draw latency 33.298 ms. All 2,930 fingerprinted owner files unchanged. No omitted pose, consumer mismatch or deadline failure. First cycle retains all 493 paired captures; second cycle has no capture stalls. Four native-size idle boards cover all 289 bare poses and were visually inspected without an obvious head/equipment discontinuity. This is not a claim of complete temporal artistic acceptance.

build_full_preview.py creates review/full-motion-preview.mp4 (1,118,590 bytes) and source-hashed chapter metadata from this new native capture set. Browser index.html playback and idle chapter seeking verified. Complete preview supersedes the shorter walk/terminal-only media for coverage. No source sprite, normal selector or game behavior changed in this milestone.

## Body reuse trial closeout - October 2, 2026
Review delivery: character/krusher-review-bundle-v1. native/gait_probe.gd and run_gait.py exercise the existing movement-driven API against Bill: 10,812 checks, zero errors, all 185 walk poses reached; matching pose indices, phase, clocks/strides and leg pixels below row 125. Stops and facing changes included. Godot exit 0; 2,930 owner files unchanged. Prescribed-input headless check, not station movement or footplant acceptance. Requested reference/reuse trial delivered. Next useful step: owner visual review of supplied sheet/video. Other families remain proposals; full NPC and extra actions outside trial.
