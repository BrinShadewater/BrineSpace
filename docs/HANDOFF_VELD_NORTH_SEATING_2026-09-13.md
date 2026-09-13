# Veld north seating candidate

## Objective and constraints
Use existing north source to continue identity/movement polish while generation credits are unavailable. Veld is a woman, no glasses, dark low bun, science suit, rear vials viewer-right. No production selection yet.

## Prepared source
Reviewed character/veld-identity-correction-v1/sources/seated-north-body-01.png and prompt. Six rear-view poses show lowering with consistent equipment. New tools/prepare_veld_north_seated_identity.py separates six columns, uses one standing scale matched to the selected runtime idle-north, registers boot support, and creates18candidate frames across sit-down/sit-idle/sit-rise. Standing endpoints reuse selected idle; rise reverses sit-down, seated idle uses explicit pose holds. This is derived coverage, not18independently generated frames.

## Evidence
review/seated-north-body-01/body-contact.png viewed: lowered body remains shorter and foot baseline stays registered; rear identity matches. Registration records source hash and transforms. Chair-contact anatomy, furniture occlusion, fitted helmet and native joins remain unreviewed. Do not call the isolated lowered pose seated acceptance. Existing runtime catalog unchanged.

## Next action
Load candidate north poses in a native chair fixture and inspect hips/feet/seat contact before fitting helmet or selecting. No generation job or active process.

## Native seated-body review
Added opt-in north-seating-candidate to tests/playtest_crew_seating_room.gd and a local trial manifest preserving selected state metadata/timing while loading the new bare frames. Real lounge approach and activity selection pass with0failures: direction north, stage life_seated, foot8000/8000, existing render offset(-42.56675,-25). Log output/crew-replacement-2026-09-12/veld/seating-north-candidate-01.log. Capture seating-north-candidate-01/lounge-q0-north.png visually reviewed: body stays within the chair footprint and boot placement is visible. This is a single resting pose and does not accept descent/rise, chair orientation semantics, helmet or full motion. No runtime catalog change. Next: capture transition phases and inspect continuity before selection. Native process completed.


## Transition review: candidate withheld
Native fixture now captures eight actual actor-update samples at 0.1-second intervals for each of life_sit and life_rise, with stage/time/render-offset evidence in transition-samples.json. Native run exited 0 with 0 fixture failures; log seating-north-candidate-transitions-01.log. The 16-frame transition-contact.png was reviewed. The existing furniture offset translates the body diagonally between approach point and chair while the authored boots remain in a stationary lowering pose. This produces visible sliding; the body also changes proportions between the selected idle endpoint and the source poses. Candidate remains unselected. Mechanical fixture success does not establish visual acceptance. Next work must coordinate chair approach/contact travel and consistent source anatomy before fitting a helmet or promoting the states. No provider submission; credits remain unavailable.
