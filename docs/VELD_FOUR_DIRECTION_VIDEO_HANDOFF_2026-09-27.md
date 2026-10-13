# Veld four-direction video review

## Objective and acceptance
Continue from owner acceptance of east/west video walks. Establish front/rear walks matching approved front/rear idle artwork and side scale.

## Accepted decisions and constraints
Owner: Looks good, lets keep going, in response to east-west comparison. Side walks accepted as shown, including previously disclosed cyan detail. Existing game runtime remains unchanged. Two further 4-credit Hailuo 2.3 Fast jobs submitted, no more.

## Current state
character/veld-video-north-v1 and veld-video-south-v1 contain source videos, prompts/job IDs, master inputs, deterministic preparation/extraction scripts, transparent frames, manifests and GIFs. Master inputs use first front/rear idle source poses with existing pilot-v12 material processing. North prepare.py builds both inputs. Private Higgsfield project reused.

Front candidate: source 47-72, 26 frames at 24fps (1083ms). Rear diagnostic: source 10-129, 120 frames at 24fps (5000ms). Rear is unexpectedly slow; first restricted cycle search found an invalid partial cycle, superseded by the full five-second candidate. No generated in-betweens or per-frame scaling. Shared side-walk scale/offset retained.

four-direction-review.gif uses 41 display frames /1708ms for all cycles to compare gait at a common pace. This preview retimes/subsamples existing frames only; source manifests retain original timing. North reads about 3x faster, south about 0.63x original speed. It is a comparison, not an accepted production timing decision.

## Verification
Both sources decoded 141 frames at 768 square/24fps. Both manifests validate without warnings/errors; zero clipping in selected exported frames. Front seam pixel difference .01027 vs median .01400; rear .01174 vs median .00714. Sampled contact sheets inspected. Rear vertical motion/gear drift and retimed gait need owner visual review; no motion acceptance claimed for front/rear. No runtime installation or Godot tests.

## Next action
Review front/rear with accepted sides in four-direction-review.gif. Decide whether retimed rear is usable or needs regeneration; do not promote its slow source timing blindly. Then consolidate accepted cycles and timing for runtime integration.
