# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: Marsh diagnostic style v7

## Objective and acceptance

Owner found v6 still changed art style. Match diagnostic poses to accepted standing masters and prevent the face/foot artwork switching during the action. V7 installed; owner visual acceptance pending.

## Accepted decisions and constraints

Keep readable held scanner, coherent arms/torso, android identity/right-temple hardware, restrained outlines and original action timing/calibration. Preserve all 180 unrelated state selections and accepted crew chat. Reversible art work authorized.

## Current state

`character/marsh-diagnostics-v7/` preserves the built-in matched-style source edit and prompt, eight authored working poses across four directions, held slots, 24 states / 120 slots, provenance, complete current timed viewer and v6/v7 comparisons. Head rows 0:58 and lower shin/boot rows 145:184 are exact selected idle pixels. Body between them remains coherent from the new source; no forearm/torso stencil. Material detail and suit construction use the four standing masters as reference, with existing palette packaging and fixed per-direction scale/foot registration.

Generated third row was compressed and is rejected. Only the first two rows supply working poses; the third packaged pose is explicitly a hold. Repair alternates the two genuine wrist/tablet poses, ending at the entry/exit join. Exact idle endpoints retained. A trial join through the thighs was rejected for a visible cut; final join is in lower shins/boots.

Catalog/rebaker/colour guard select/protect v7. Current runtime contract, timed media, pose boards and native chains refreshed. Previous candidates preserved with links to current review. Tools: prepare/publish_marsh_diagnostics_v7.py; tests: test_marsh_diagnostics_v7.py.

## Verification

Four identity/foot-art, scanner/margin, provenance/join and source-selection/timing tests pass. Game-player 22,504 checks pass; final native playback 1,058 source/elapsed checks / 432 captures passes. No warnings. Colour guard: 9,291 paths / zero errors. Source and native diagnostic poses reviewed at source/station size. Full set scan has no canvas contacts. Python/JavaScript syntax and review links pass. Checks establish source/clock integrity, not owner acceptance. Browser controls not exercised.

Godot used scratch APPDATA. Real profile fingerprints/comparison preserved with v7 logs; shared-session deltas are not restored or attributed to a particular process.

## Next action

Owner review at `character/marsh-diagnostics-v7/index.html`, especially idle-to-work and the two-pose working loop. Existing short pose cadence remains; held slots are not additional authored drawings.

Real profile: 2753 unchanged, 6 changed, 0 added, 0 removed. Shared-session deltas preserved; origin unestablished.


Full-library colour follow-up (September 30): diagnostic v7 remains the authored source; the current selected colour exports and whole-library review are in `character/marsh-quality-pass-v4/`. See `docs/MARSH_FULL_LIBRARY_COLOUR_2026-09-30.md`.
