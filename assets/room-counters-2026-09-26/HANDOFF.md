# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: counters for varied rooms

## Objective and acceptance
Four distinct dressed counters created for galley preparation, medical supplies, specimen examination and engineering repair. Owner review pending.

## Accepted decisions and constraints
Current painted industrial style, accepted overhead/cutaway reference, generic matte materials with restrained accessory colors. Wall-friendly rear edges, sparse useful objects. Existing assets preserved.

## Current state
masters/ holds four built-in image_gen originals; game-size/ holds proportional transparent exports. production.json records exact prompts and reference; sources.json records generated paths. build_exports.py reproduces exports and review sheets. manifest.json records dimensions, hashes and proposed display widths.

## Verification
Four RGBA exports have full alpha range and transparent margins. Native light/dark visual review complete: coherent perspective, distinct cabinet/support construction, readable room-specific accessories and complete silhouettes. Density convention remains 0.34 world units per library pixel. Wall contact, crew scale and runtime fit are untested; no registry, gameplay or owner layout changes.

## Next action
Follow-up perspective/density/style audit complete; see AUDIT.md and audit-comparison.png. Broad match confirmed, with optional metallic-highlight polish and module-height differences recorded. No artwork changed during audit.

Owner review of review-light.png/review-dark.png; live placement and rear-edge alignment if integrated.
