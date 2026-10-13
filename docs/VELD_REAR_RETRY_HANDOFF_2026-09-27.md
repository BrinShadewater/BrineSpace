# Veld rear walk retry

## Objective and acceptance
Owner rejected rear in four-direction comparison. Replace irregular slow rear gait; accepted side walks unchanged.

## Accepted decisions and constraints
Original rear v1 is owner_rejected_rear_gait in its manifest. One additional 4-credit Hailuo 2.3 Fast retry uses same approved rear input, explicit regular footfall cadence and restrained torso/heel motion. No other clips regenerated.

## Current state
character/veld-video-north-v2 contains raw source.mp4, generation.json, master input, reproducible review/build scripts, contact sheet, transparent frames, strip, manifest and north-loop-review.gif. Selected source frames 40-67, 28 frames, 1167ms at original 24fps. No speed-up or interpolation. Prompt/job preserved; same private project reused.

## Verification
Source decoded 141 frames at 768 square/24fps. Manifest validator zero errors/warnings, no clipped frames. Seam mean difference .00977 vs internal median .01215. Sampled poses show steadier torso but feet close together; no claim of owner acceptance or certified smoothness. Runtime unchanged.

## Next action
Owner reviews north-loop-review.gif at original speed. Foot-lane spacing and apparent floating remain the key visual questions; technical checks do not settle gait quality. Avoid blindly promoting based on seam score.
