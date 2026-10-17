# Veld animation pilot v8

Candidate only, not installed. Adds rear idle to v7: 42 frames in seven clips,
including four-direction bareheaded idle. All 36 previous frames are byte-identical.
Rear material masks exclude facial skin and front ivory modules, preventing warm
bun highlights from becoming skin. Same locked material ramps and 148px standing
height, 184px canvas, [92,172] pivot. Continuous shading, not 24-colour quantization.

Front and rear walk sources are preserved in held-sources, outside the manifest.
See review-findings.json for defects and remaining edge/loop review.
New source prompts are in new-prompts.json; original sources remain untouched.

Validation: manifest validator no errors/warnings; native player 160 checks,
zero failures, 24 captures. All 2670 real-profile hashes unchanged.
Rebuild: build_pilot.py, run_native_review.py, build_review.py.
Runtime artwork and production pack selection remain unchanged.
