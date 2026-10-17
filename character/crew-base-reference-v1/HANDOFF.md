# Project handoff

Updated: 2026-10-02 · Project: BrineSpace · Task: reusable crew body families

## Objective and acceptance
Support the owner's proposal to reuse Bill, Veld, James and Marsh as body families selected by likeness/build, beginning with Krusher's Bill-body trial.

## Accepted decisions and constraints
Veld is the owner's suggested default for female characters. Actual proportions, role and equipment govern a derivative's fit. Preserve existing sources; common standing metadata does not certify cross-family head/gear compatibility.

## Current state
base-family-comparison.png shows sixteen original idle views at a shared 2x nearest scale. catalog.json records source hashes and paths, physical metadata, idle/walk counts and durations, and opaque body bounds. Human references use declared matte locomotion overrides; Marsh resolves later matching idle entries in ordered selected catalog.body. build_catalog.py and validate_catalog.py reproduce and check the reference. README.md records family differences and derivative rules. No existing artwork or normal selectors changed.

## Verification
All sixteen views inspected for appearance, labels, scale and direction order. Validator: 147 checks, zero errors, including 98 input hashes (ACTIVE_ASSETS included), 16 source tile bounds, all nonzero-alpha source character pixels including inherited faint fringes, shared standing profile and complete family/view coverage. This reference catalog does not establish new animation coverage, other-family Krusher derivatives or runtime integration. No Godot run needed for read-only sheet composition.

## Next action
Use the catalog to choose the next derivative family and inspect its exact head/tint/equipment sources before applying Krusher's demonstrated Bill workflow. Krusher facial studies remain separate from the current consolidated runtime candidate pending motion review.
