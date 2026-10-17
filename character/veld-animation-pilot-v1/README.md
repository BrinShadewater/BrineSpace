# Veld selected-design animation pilot

The owner selected the four crew turnarounds on September 27 and requested animation repair. Reference hashes and palette targets are frozen in `../crew-turnarounds-v4/design-lock.json`.

This first pilot covers bareheaded idle-south, walk-east and interact-east (sample inspection). Existing loader profile is 184x184, foot pivot (92,172), standingHeight 148. Existing total clip timing is preserved. No runtime manifests or images are replaced by this pilot.

Built-in imagegen creates source poses; `build_pilot.py` deterministically extracts isolated body components, thresholds source alpha (or keys the corrected walk from flat magenta), uses one standing-derived scale per clip and anchors torso centre/ground. It produces PNG frames, a compatible review manifest, frame contact sheet, before/after lossless animated WebP previews and geometry checks. No opposite directions are mirrored and no new poses are drawn procedurally.

Prompts and rejected candidates are retained. The first eight-frame walk failed clear leg alternation; the six-frame retry uses an existing six-pose motion reference solely for gait, with the selected new sheet defining appearance. A targeted opposite-half correction and scanner continuity correction are recorded separately.

Material swatches are target specifications, not proof the generated frames already match them exactly. Source colour is retained during motion review. Semantic material masks and deterministic ramp mapping are still needed before promotion. Global palette reduction is deliberately avoided because it can erase facial detail and mix skin with suit accents.

Production promotion requires visual review of gait, foot contact, source-grid extraction, identity, device continuity and loop seams; native station-scale checks with isolated saves; then broader directional/helmet coverage. The review page is a pilot, not a claim that the complete character library is repaired.

Current review: geometry validator passes without warnings. Idle 148-149px height, walk 146-149px, inspection 144-153px. Walk torso yaw and inspection height variation remain visible defects, so this pilot is not ready for installation. See review.json.
