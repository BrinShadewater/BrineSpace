# Veld v7: left-facing coverage

Adds independently generated idle-west and walk-west, six frames each. Total:
36 frames / six bareheaded clips. The 24 v6 frames remain byte-identical. Near
left hip carries the scanner; right-hip canisters remain on the far side. No image
mirroring is used. Head/face/hair masks now accept facing for correct spatial tests.

The new left gait has a different source stride. Its measured flat-foot front-edge
movement is 20px over 130ms in both half-cycles. At 148px standing height and .17
cell body height this gives walk-west strideDistanceCells=0.15904365904365905.
The right walk retains 0.11716216216216217. The old shared stride produced 5.27px
flat-foot drift; the new value yields zero residual at those measured boundaries.
Landmark uncertainty is +/-1px. This does not promise zero sliding during rolling
contacts, frame holds, or all parts of a cycle. See direction-review.json.

Run build_pilot.py, run_native_review.py, then build_review.py using Python. Native
review exercises independent east/west distance clocks and shows both at 148px and
45px standing scale. 148 checks pass; 2670 real-profile file hashes unchanged with
scratch APPDATA. Geometry validator reports no errors/warnings. Raw sources,
prompts, material masks, contact sheet and native captures are retained.

coverage.json compares this new-design pilot against the current active catalog.
Remaining front/rear walking, rear idle, other actions and helmet states are not
implicitly completed by this pass. Runtime art and production selection unchanged.
