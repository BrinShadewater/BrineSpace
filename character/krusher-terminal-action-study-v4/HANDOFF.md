# Project handoff

Updated: October 2, 2026 - Project: BrineSpace - Task: Krusher tight release and native art preview

## Objective and acceptance
Refine representative terminal action while retaining the Bill-body reuse direction. Full Krusher character work remains active. Standalone native artwork evidence does not establish station gameplay or owner acceptance.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics / matte muted grey-cyan. Use existing body/motion where appropriate, keep source density, fixed foot pivot and exact endpoints. New anatomical poses use authored art; deterministic masks only composite existing artwork.

## Current state
Builtin tight edit e6d8fd2c-5193-437b-8536-113aecc4f23c saved as source-release.png with exact prompt-release.txt. Generation reference is the canonical idle enlarged4x nearest-neighbour, with provenance. Only near forearm/glove (91,84)-(106,110) is composited; clipped hardware (88,92)-(96,108) remains exact, three-row upper seam feather. Prior V3 raise/type/closing sources retained. Candidate covers west bare raise6/type6/lower7 references with exact idle and held aliases. Native standalone project/script and safe runner live under native/ and run_native.py. Review media and native reports/captures live under review/.

## Verification
validate_candidate.py:79 checks,0errors. Native Godot4.7.2 run:exit0,19 captures,0reported errors,5.24s. validate_native.py:86 checks,0errors; source/time binding, viewport, stable Bill reference, rendered endpoint aliases and protected release pixels pass. Native observed pose hold overrun max16.34ms. All2930owner non-log files unchanged before/after; APPDATA explicitly scratch. Native fixture uses current Bill manifest's west idle000 (idle-west-breathing-v1) for the comparison, not a hardcoded obsolete source.

Reclip/release/idle board, native typing and release screenshots reviewed; full continuous motion not accepted. Current texture filtering and92px display canvas/74px standing ruler shown. Narrow release patch avoids prior source-wide hardware drift. Generated whole body is discarded. No main project/controller/normal art selection or owner-save mutation. Separate native project does not load station scenes.

## Next action
Review the complete action with native-clock media and inspect equipment shape/contact across the sequence. Resolve locomotion glove occlusion and source fringe pixels, then establish compatible helmet and cardinal variants. Expressions/turn joins and isolated real station evidence remain. Consolidate the reusable body/head/palette/attachment sources once representative action quality is established; keep rejected sources out of selected playback. Full character goal is incomplete.
