# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill east sitting transitions

## Objective and acceptance
Continue the full master-consistent Bill animation set, then full-set consistency
and polish. This milestone stages east sit-down and rise in both gear states.
It is candidate source/player evidence; runtime selection and owner acceptance
remain separate.

## Accepted decisions and constraints
Exact currently loaded east standing endpoints, native selected helmet, matte
master grade, same anatomy and projected head/torso/boot scale. Lower through
authored hip/knee motion; never shrink each pose to simulate sitting. Both boots
stay planted. A fully seated torso may straighten after the lowest crouched pose.
Retain800ms finite sitting and exact reversed rise, depth0..40, pivot128,224 and
standingHeight148 on256px planes. East's current standing sole is223; retain that
authority rather than shifting it to another direction's222px sole.

## Current state and changed files
Four gear states/24 frame refs. `build.py` selects primary source1/4/5 and two
independent middle-source figures. Primary0 becomes exact selected idle; primary
2/3 are omitted from this transition. Primary generation
exec-bda2c1e2-1b68-4de7-a56b-2bfb9766bc3f; middle generation
exec-6617bcb3-aa9c-483f-aaa6-363c47abcfc6. Raw images and exact prompts are retained.
Primary ruler .27/.3058; independently measured higher-density middle ruler
.125/.1426. One fixed resize per source, then opaque boot translation. CrownYs:
76,85,99,109,106,103. `grade.py` derives frozen neutral/hair/face/burgundy curves
from the selected east idle. Source density bounds the anatomical material ROIs.

`bill-seated-helmet-east-coherent-v1/build.py` fits the selected native helmet
with measured head positions/tilts and protects body pixels below collar. Both
frame0s use exact RGBA padding; no alpha double-blend. Mixed sources require output
frame-index registration: sourcePose numbers repeat across primary and interiors.
The initially inherited sourcePose-keyed map failed before completion; corrected
to frame keys. No normal loader, selection registry or NPC behavior changed.

## Verification
49 paired package source/ruler/contact/endpoint/hash/body checks pass.
181 native candidate checks pass9.39sec: exact currently loaded bare/equipped idle
joins, loaded source pixels, shared plane/density, actual Bill life-stage chooser
and simulation elapsed times, paused poses, finite800ms terminal holds and valid
intermediate snapshots. Fresh native82px paired down/rise board visually reviewed.
All2,914 real non-logfiles unchanged under scratch APPDATA.

The primary atlas already settled by its fourth pose; repeated seated poses did
not supply a gradual lowering curve. Independent middle anatomy fills that gap.
Do not infer smoothness or world furniture contact from six nominal frame slots.

## Remaining work and next action
East seated breathing and reading/tool transitions, real furniture contact,
normal family selection, interrupted stages and disk restores remain. West
seated/reading, other life/rest actions, wider world journeys and full-set final
material/proportion/motion polish remain. Full Bill goal stays active.
