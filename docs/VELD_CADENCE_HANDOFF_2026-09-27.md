# Four-direction cadence candidate

## Objective and acceptance
Owner accepted extracted rear v6 loop (Okay looks good) and requested continuing with front review and cadence matching. East/west motion already accepted. Front motion and new timing remain candidates.

## Accepted decisions and constraints
No generation/credits. Original accepted source packs unchanged. Preserve all frame RGB/alpha bytes, frame counts and spatial registration. Timing changes are a separate review, not implied acceptance or runtime integration.

## Current state
character/veld-walk-cadence-v1/build.py consolidates south26/north28/west41/east40 frames into one manifest, each 1500ms. This compromise speeds west/east slightly and slows front/rear. Every exported PNG byte matches its source. Original source durations and hashes retained in manifest. four-direction-cadence.gif uses the union of centisecond frame boundaries, so all original frames appear and all directions loop at the same endpoint without the earlier comparison restart jump. front-master-review.gif pairs front with approved A idle.

## Verification
135 copied frames hash-verified. All four duration sums1500ms. Manifest validation zero errors/warnings. Static front/master preview inspected: front-facing motion changes the slight three-quarter head angle in idle; face/arms require owner review in motion. No claim of temporal acceptance, runtime tests or installation.

## Next action
Owner reviews front design/motion and common cadence. After acceptance, integrate the complete reviewed pack with matching idles and correct runtime stride controls; inspect consumer before replacing artwork. Accepted north reference is v6, never earlier failed rear trials.
