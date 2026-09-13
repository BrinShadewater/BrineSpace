# BrineSpace fire effects

Created September 12, 2026 with the built-in image-generation tool, then locally
cleaned with owner authorization. [Exact prompts](prompts.json) and
[source audit](source-audit.json) preserve provenance. Style references were the
reactor source-v1 and card-v4: copper/orange flames, small ivory cores,
charcoal/taupe smoke and sparse cinders.

## Deliverables

Each layer has eight frames in a 4x2 grid, with real transparency:

| Layer | Runtime atlas | Full-size atlas | Playback |
|---|---|---|---|
| Flame | flame-96x128-v2.png | flame-atlas-v2.png | 8 fps |
| Smoke | smoke-96x128.png | smoke-atlas.png | 6 fps |
| Embers | embers-96x128.png | embers-atlas.png | 8 fps |

Runtime cells are 96x128, sharing pivot (48,118). Full-size cells are 384x512.
[Animated review](review.html) includes playback, frame stepping, intensity and
layer controls. [Contact sheet](contact-sheet-v2.png) shows all 24 frames over light
and dark backgrounds. [Manifest](manifest.json) records dimensions and hashes.

## Preparation and integration

The original RGB sheets are retained, including the rejected opaque alpha retry.
`prepare.py` removes the flame's baked checkerboard and the other sheets' magenta
matte, translates each root to a common canvas without individual scaling, then
exports an exact 4:1 nearest-neighbor reduction. Masks are specific to these
palettes. The script defaults to audit; `--write` refuses existing output files.

`scripts/fire_effects.gd` draws the three atlases using simulation time, so pause
freezes animation. Fire intensity changes size and secondary flames. The old
procedural renderer remains a fallback if assets cannot load. Gameplay is unchanged
by the art integration.

## Verification and remaining review

Asset validation passed 37 checks; fire rules passed 35; native gameplay passed
25, including rendered animation and pause stability. Latest native run:
`output/test-runs/20260912-022651-native`. Close and station-fit screenshots were
visually reviewed, along with transparency over light/dark backgrounds and the
preview's frame 8-to-1 stepping. Owner style and pacing acceptance remains open.

The release dependency crawl selects only the three runtime PNGs from this pack.
The executable was not rebuilt or validated. PNGs inherit Git LFS rules.

## Owner correction: white fringe

The initial visual review missed pale matte residue along flame edges.
`fix_flame_fringe.py` removes 2855 exterior pale pixels while preserving the
bright interior and existing transparent gaps. Runtime and animated review now
use v2 flame atlases; v1 remains for comparison. The updated contact sheet shows v2. Smoke and embers are unchanged.
