# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Krusher reusable body test

## Objective and acceptance
Test Bill body reuse for Krusher Dom, preserving size, density and existing motion; prepare reusable attachments. Full character production remains incomplete.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics. Matte muted grey-cyan markings. Existing Bill, Veld, James and Marsh may serve as bases according to build and likeness. This is an unselected art candidate.

## Current state
build_trial.py derives 948 bare/helmet cardinal idle/walk frames from krusher-bill-base-test-v2. Generated equipment parts come from krusher-equipment-study-v1. Fixed native dimensions, integer torso translation, original source motion and timings. Front/back use belt templates; side views use the rigid front chest because swinging gloves obscure the belt. First trouser and profile belt tracking attempts drifted and were replaced. Manifests, edit masks, source hashes, transparent APNGs, sampled walk boards and paired browser viewer are saved here.

## Verification
validate_trial.py: 4774 checks, zero errors. All source hashes, protected pixels, lower legs/feet, durations, pivot and APNG decoded frames pass. Sampled all bare directions and helmet south/north visually. These checks do not certify complete-cycle motion or foreground glove occlusion. Side-view glove overlap remains unaccepted. No Godot run, owner save change, normal runtime selection or owner acceptance.

## Next action
Review complete cycles, refine dynamic glove occlusion, then author a held-terminal typing action with exact idle entry/exit. Expressions, turn joins and isolated native station evidence remain outstanding. Full character work is still in progress.
