# Project handoff

Updated: 2026-10-14 · Project: C:/Users/Alex/Documents/Brine Space · Task: Krusher Dom style, pixel density and neck integration

## Objective and acceptance
The owner rejected V8's head/body style mismatch and detached necks. Match the existing James-body art and native detail density; make the short neck enter the collar through standing, bowed, reclined and prone poses. Deliver a reviewable full-set revision. Owner visual acceptance is pending.

## Accepted decisions and constraints
Keep the original body, muted cyan suit, tools, helmet shell, 148-source-pixel standing ruler, per-pack canvas/pivot and every original clock. Preserve alpha edges rather than binarizing them. New authored matte heads come from the supplied body-style reference and Krusher likeness. No global suit blur or palette reduction. Existing authorization covers this reversible revision and the existing private Site update.

## Current state
- `character/krusher-animation-package-v9/`: portable 586-state candidate (338 bare / 248 helmet), 8,058 holds, 3,486 unique PNGs. 3,112 drawings changed; protected rear/no-visible-head drawings retained.
- `character/krusher-style-neck-v1/`: generated integrated bust/action/quarter/rest/rear source sheets, exact prompts, extraction/mapping/build scripts, native fixtures, review evidence and comparison image. `sources/` retains antialiased native cutouts with uniform source scaling.
- `character/krusher-style-neck-bank-v1/`: unique-drawing repair map, masks and manifests. Original skin restored only inside the anatomical contact, excluding gold suit pixels; prone south neck tips hidden behind the jaw; original collars/tools remain in front. Every V8 drawing has one consistent replacement.
- `character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd`: two additional exact style-cue hashes, proven identical outside the head/neck mask and across the entire case/lower-body RGBA region. Older hashes and strict rejection retained.
- Private Site: https://krusher-dom-preview.brinshadewater.chatgpt.site/animations/ . Previous/Revised selection covers every animation. Source commit `109372e5489fb2ab6351648d646d25fca369c2a7`; deployment `appgdep_6ad05902487881918e3a226258ddb84b` succeeded. Original reference homepage and owner-private access preserved.

## Verification
17,424 source/body protection checks; 16,790 portable package checks; zero attachment findings or conflicting source replacements. All helmet alpha and pixels outside local head/neck masks exact. 3,486 lossless WebPs decode exactly to current PNGs; both 586-state browser libraries have no missing files.

Godot 4.7.2 native: loader 57,025; repair 8,951 / 120 captures; bunk 240 / 30; water 6,399 / 104; West case 383 / 98. Total 72,998 checks, 352 captures; zero failures/errors/warnings/leaks. Every run used scratch APPDATA and preserved all 2,947 owner non-log files. Reports in package `verification/` and here `review/`.

Visual evidence: 256 representative family/gear/facing midposes; enlarged standing, work, reclined and prone collar details; sampled station captures; browser current/previous idle at 3x, repair motion, prone swim and helmet portrait. No browser console errors. Static coverage is not exhaustive continuous-motion acceptance. The comparison screenshot is `browser-comparison.png`.

## Next action
Review the live Previous/Revised switch with the owner, especially repair, get-up, sleep, swim and turns. Any additional specific pose defects should be corrected in the authored source/registration and propagated through its aliases. No normal roster integration, game export or game-repository commit was performed. The old V8 coverage milestone remains historical evidence, superseded by the owner's style/neck rejection.
