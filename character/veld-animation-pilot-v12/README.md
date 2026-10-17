# Veld v12

B/D/E/F/G face highlight fix: recover larger pale islands missed by warm skin
selection and remove white from the side-profile skin ramp. Highlight endpoint
is the locked warm skin-light. Geometry/timing retained; A/C unchanged.

42 alpha masks unchanged, 12 A/C frames byte-identical, manifest clean,
160 native checks pass, real profile unchanged. Candidate only.
Review review-all/all-animations.gif and face-before-after.png.

Rebuild: build_pilot.py, run_native_review.py, build_review.py, build_overview.py.
