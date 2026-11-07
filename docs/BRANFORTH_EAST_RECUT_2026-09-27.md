# Branforth east walk recut

## Objective and acceptance
Owner likes the Higgsfield source but rejects the47-frame extracted loop as incomplete motion/stuttering. Recut locally; no new generation.

## Accepted decisions and constraints
Preserve original source speed, pose order, colour correction and body scale. Bill/Veld previews accepted. Source video is the motion reference, not frame-similarity score alone.

## Current state
`character/branforth-video-east-v2/` supersedes v1 for loop review. Includes92 consecutive source frames24–115 (3833ms at24fps), original MP4, same extraction/colour transform, manifest, master comparison and old-new-review.gif. Existing47 shared PNGs verified byte-identical. v1 retained; neither installed.

## Verification
Inspected dense source leg-phase contact sheet spanning all141frames. Previous search limited candidate periods28–52frames, which could select similar-looking passing poses without enough stride coverage. New two-step search84–104frames yields92framecut, preserves all intervening poses and both stride extrema. Seam mean difference0.00364 vs old0.00876; internal median0.00703. This is supporting evidence, not visual acceptance. No source/export clipping. Manifest0errors/0warnings.47 overlapping frames pixel-identical; no interpolation or synthetic motion. Zero credits spent; last verified balance108.

## Next action
Owner review of old-new-review.gif for complete range and stutter. Do not restore short automatically selected cut based solely on numerical seam similarity. If needed, inspect actual near/far-foot phase around boundary in the original video before changing timing.
