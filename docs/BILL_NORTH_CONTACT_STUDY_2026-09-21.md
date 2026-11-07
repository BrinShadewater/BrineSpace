# Bill north contact source study

Updated September 21, 2026. Broad goal remains active.

## Objective and decisions
Investigate north stance sliding without altering owner rooms or accepted walks.
No Higgsfield. Two built-in image generations, prompts/raw sources preserved.
No runtime art, movement, timing, stride or release package changes.

## Findings and current state
Evidence: output/bill-north-contact-2026-09-21/.
Sources: character/major-bill-v3/sources/north-walk-contact-2026-09-21/.
The selected north stride is 0.12 cells, equivalent to104.47source pixels per
900ms cycle at the declared standing height. Travel from the first to third pose
onsets is34.82source pixels. The apparent forward/supporting boot moves only a
few pixels within the old source, so the cycle has substantial visible sliding.
This is a rendering/source observation, not measured anatomical world contact.
Lowest opaque pixel is not a reliable toe contact when the heel lifts.

A new six-pose rear atlas has clearer opposing contacts and passing poses and
more within-half-step boot progression. Its smooth suit and shorter/simpler
backpack diverge from the canonical idle reference. A second detail edit did not
resolve this identity mismatch. Neither source is selected for production.

Motion-only normalization uses the first raw atlas, source alpha threshold128,
shared146/458scale, horizontal head registration and common vertical offset16.
It deliberately does not align every lowest boot to a common baseline: doing so
would erase the foot-depth progression being examined. Binary alpha finalized
at128. Recipe, raw cell crops and hashes are retained in study.json.

## Verification and limits
Native comparison:27samples, current and candidate, source/game scales, production
sprite player, same existing stride/timing, moving vertical ground reference;
exit0, zero missing textures. Candidate still slides at the current stride.
All12installed north bare/helmet PNGs remain byte-identical. Candidate is bare
only; no helmet, live station or integration acceptance is claimed.
No full-library rerun was needed because production art/code did not change.

## Next action
Retain canonical backpack/body proportions while authoring measurable support-foot
progression. Establish contact landmarks across the whole half-step before fitting
a stride, and distinguish raised-heel silhouette from planted toe. Do not select
this motion-only draft or simply accelerate playback to hide the discrepancy.
Continue broader room, release and performance polish independently.
