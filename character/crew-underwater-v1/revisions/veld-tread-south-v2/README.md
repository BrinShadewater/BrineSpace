# Veld south tread facing correction

Native water fixture now passes (`tread-native-clear-position.log`). Diagnostics
identified Veld's old sample point (7920,7920) as unsafe for upright treading.
The fixture first asserts the horizontal fallback, then selects a nearby graph
point with clear tread envelopes in all four directions and peer spacing for
visual sampling. Production geometry, collision margins and controller behavior
are unchanged. This verifies blocked/clear state selection; full continuous
treading-quality review remains outstanding.

Six body and six front-helmet candidate frames retain the established 92 x 92
canvas, (46,35) shoulder anchor and 14/80 source head calibration. Rebuild with
`python character/crew-underwater-v1/build_tread_revision.py`.

Contact inspection shows a centered south-facing head/torso and face visible
inside the front visor. Source, measured anchors, crops, body and overlay hashes
are recorded in registration.json. Frames have nonempty margins. This pack is
not integrated; treading rhythm and transitions still require motion review.

Current status: provisionally integrated into renderer, main review and tread
clearance export. `test_crew_medium.gd` passes. The broad native water fixture
fails three repeated treading-state assertions at its fixed sample positions;
`tread-native-test.log` preserves this failure. Actor/position/upright-clearance
diagnostics have been added for the next run. Do not report native acceptance
until this is resolved; rhythm and transition review remain outstanding.
