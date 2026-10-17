# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Krusher moving south blink

## Objective and acceptance
Fit the authored blink source onto the existing breathing idle without changing body motion, head registration, size, alpha or source clocks. Keep the existing runtime package unchanged.

## Accepted decisions and constraints
Krusher Dom / System Administrator / matte muted cyan AI & Robotics. New eye pixels come from the builtin-generated blink source in krusher-blink-study-v1. Only south bare idle is covered. No opacity-fade inbetweens or mirrored profiles.

## Current state
build_study.py retains all 73 south idle poses and holds. Frames 47/48 close the eyes at 1958–2042 ms (84 ms), aligned with the original 3,042 ms cycle. Each frame uses its recorded headPaste registration; those anchors are (81,23) throughout this particular idle. baseline-manifest.json points to the preserved runtime source; blink-manifest.json loads the study derivative. native/review.gd uses existing CrewSpritePlayer to compare original and blink variants on a continuous clock. run_native.py isolates APPDATA.

## Verification
Godot 4.7.2 exit 0 / 14.26 seconds, 219 paired events over three cycles. 956 native checks, zero errors: complete source schedule and coverage; finish overrun 9.535 ms, max selection latency 16.664 ms, draw latency 33.253 ms. 296 source/native composition checks, zero errors: all body and face pixels outside the small filtered eye region match the original, alpha exact, both closed poses affect rendered pixels. All 2,930 fingerprinted owner files unchanged. Native closed pose visually inspected: calm eyelid change, stable face/neck/body; display-size change remains subtle. This does not certify final natural motion or owner acceptance.

## Review media and remaining work
build_preview.py retains source-hashed capture metadata and creates review/blink-motion-preview.mp4, 85,510 bytes, from 73 paired native captures at declared holds before 60 fps quantization. Browser index.html provides Watch blink, Hold closed pose, speed controls and download. Hold closed pose seek/pause verified at 1.98 seconds. Current runtime candidate and normal selectors remain unchanged. Next: assess blink motion/readability, then fit the compatible helmet face or profile views using their actual registrations rather than this bare head anchor.
