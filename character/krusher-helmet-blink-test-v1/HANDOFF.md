# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: Krusher helmet blink reuse

## Objective and acceptance
Reuse the authored south blink inside the existing helmeted face while preserving helmet hardware, visor, body motion, registration and clocks. Keep the current consolidated runtime candidate unchanged.

## Accepted decisions and constraints
Krusher Dom / System Administrator / muted matte cyan AI & Robotics. Use the generated eye-only source from krusher-blink-study-v1. No new face redesign, helmet deformation, mirrored profile or fabricated inbetween.

## Current state
build_study.py reconstructs the original face-fitting operation from the preserved Bill helmet source and independently checks it against current Krusher face pixels before editing. The original head crop [0,5,23,28] fits to 17x17 at (83,29), inside face box [83,29,100,46]. Only changed filtered eye-source pixels admitted by the original face mask are copied. All 73 idle source poses and durations remain; frames 47/48 close the eyes at 1958–2042 ms. baseline-manifest.json and blink-manifest.json provide the paired comparison, with native masks and verification.json retained.

## Verification
Original helmet source hashes match the preserved build evidence; existing face reconstruction is exact. Each closed pose changes 65 pixels within the admitted face region after the original Lanczos fit. Helmet, visor, body and alpha outside the face edit remain exact. Godot 4.7.2 exit 0 / 14.09 seconds, 219 paired events over three cycles. 956 native clock/coverage checks and 296 composition checks pass, zero errors. Finish overrun 15.514 ms; max selection latency 16.118 ms and draw latency 32.724 ms. All 2,930 fingerprinted owner files unchanged under scratch APPDATA. Native closed pose visually inspected: stable helmet/face placement, subtle eyelid change at display size. Natural motion and owner acceptance remain separate.

## Review media and next action
build_preview.py creates review/blink-motion-preview.mp4 and source-hashed metadata from all 73 paired first-cycle captures. Browser index.html provides original/half speed, Watch blink, Hold closed pose and download. Next: assess the paired bare/helmet facial motion before including it in a new consolidated runtime revision. Existing runtime package and normal selectors remain unchanged. Profile expressions need their independently authored sources and face registrations.
