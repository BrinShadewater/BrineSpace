# Project handoff

Updated: October 2, 2026 - Project: BrineSpace - Task: Krusher action intermediates

## Objective and acceptance
Refine representative terminal motion for the reusable Bill-body Krusher character. Full character work remains active; no normal art selection or owner acceptance claimed.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics / matte muted grey-cyan. Preserve character density, original head/legs, pivot and exact idle/held joins. New anatomical poses require authored source art.

## Current state
Three isolated builtin imagegen calls are saved with exact prompts and source hashes: source-lift.png (0596a086-701f-4fa3-9a25-df82189ab170), source-open.png (a662834d-7ddf-40f3-a654-bd4f1787a5dd), source-release.png (8eb6a970-af5b-4377-8c93-ca82069a70ec). Native paired review rejected lift (device too high) and release (hardware silhouette and hand boundary drift). Only partial opening is provisionally admitted. Existing authored V1 key-007 lowering pose is reused during raise in reverse action order; this is explicitly derived reuse, not new lift art. Eleven unique frame images now define raise6/type6/lower6 references. Bounded arm/waist patch and V2 seam feather retained. All states, APNGs, pose selector and transition board rebuild locally.

## Verification
validate_candidate.py checks hashes, admission, protected pixels/head/legs, exact aliases, APNG decoded frames and durations. Authoritative count in validation.json. Earlier 111-check result covered provisional rejected poses; final run supersedes it. Browser reached two playback cycles; native-size partial opening, lift and release were inspected separately. Rejected sources remain in review and provenance. This is not continuous-motion or native station acceptance. No Godot run, gameplay selector or owner-save writes.

## Next action
Review the revised full sequence with the reused low pose. Author a hand-release pose that preserves clipped device geometry and arm boundary; use the canonical hardware as compositing input. Refine any terminal shape/hand drift before other cardinal views or helmets. Dynamic glove overlap in locomotion, expressions/turn joins and isolated station evidence remain. Do not count rejected raw sources as coverage or technical package checks as visual approval.
