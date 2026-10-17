# Project handoff

Updated: October 2, 2026 - Project: BrineSpace - Task: Krusher corrected shared action master

## Objective and acceptance
Keep corrected locomotion and terminal action on one exact resting master. Full character goal active; no normal art selection or owner acceptance.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics / matte muted grey-cyan. Reuse existing Bill body and authored pose art; no new generated anatomy in this revision.

## Current state
build_candidate.py recomposites stored registered action sources onto moving-equipment-test-v2 bare west idle000. V4 action idle had27 differing hip pixels; new idle file is byte-identical to corrected locomotion master. Main authored arm/waist patch now extends to y110 to include the transition band using original registered artwork, with original four-row seam feather. Release retains its narrow mask. Twelve unique frame images cover west bare raise6/type6/lower7 references; fixed184canvas/(92,172)pivot and original timings. Original idle/held aliases exact. No imagegen calls in this revision.

## Verification
validate_candidate.py:97checks,0errors. Protected head/lower-body pixels, original authored hashes, shared master file, joins and APNG decode/timing pass. Godot4.7.2 standalone native preview:19captures,engine0/4.95s. validate_native.py:86checks,0errors including stable Bill reference, source/time binding, rendered joins and protected release pixels. Scratch APPDATA; all2930owner non-log files unchanged. Native idle/type screenshots and shared-master board reviewed. Earlier V4 native evidence applies to its revision only; this fresh interval establishes V5 rendering.

## Next action
Full-cycle visual review, equipment shape/contact polish, corrected locomotion native review and isolated real station evidence. Helmet/cardinal role counterparts and turn/expression references remain. No full continuous-motion/gameplay acceptance or normal runtime integration claimed. Pair with moving-equipment-test-v2; earlier action masters are historical trials.
