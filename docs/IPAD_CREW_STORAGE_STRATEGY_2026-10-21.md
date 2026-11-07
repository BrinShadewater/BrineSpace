# iPad crew storage strategy results — October 21, 2026

Accepted playable build remains **brinespace-19db95fa680a52e5**, with its complete signed app/PCK preserved in `allocation-redraw-pass/candidate`. No new playable validation export is promoted in this pass. Source HEAD remains81b2f9a4a36eb0e3162d86ccfb4e9ef735836122 plus prior dirty work and the candidate below. Frozen Mac/Windows releases are unchanged.

## Candidate retained in source

`scripts/crew_storage/slots.gd` can share immutable full-frame GPU uploads by existing CpuFrame identity and sampler policy. Each wrapper keeps independent metadata/sampler CanvasTexture; at most eight aliases per slot. Excess aliases use the existing immutable spill path. The 128-slot / 64 MiB pixel budget, retained-canvas leases, visibility retirement and last-owner cleanup are preserved. `--reference-crew-source-sharing` selects original wrapper identity for a same-package comparison. No source pixels, logical dimensions, UVs, timing, gameplay or save format change.

Twelve source-sharing/metadata/filter/alias-limit tests and 72 native real-art pixel checks pass. Six suites also pass against the exact probe PCK: source sharing, pixel matrix, pose cache (18 checks), routed pixels (12 checks), hidden leases (13 checks) and tablet decode. Exact base-plus-seven-overlay audit: 37,383 resources, zero errors; strict development signature verifies. The physical A14 iPad 10 / iPadOS 27.2 passes the 72 pixel checks, including fractional zooms that rejected atlas packing.

## Physical comparison

Same signed probe package; normal 56-room/four-crew checkpoint; ABBA order, 120 actual active seconds per run. Comms are advanced through the existing Next action and paused time is recorded separately. All four crew survive every run. Saving through the game method reproduces complete serialized state and exact timer in all four runs. Across loading reveal, only discovery_bursts ages; these are not complete-startup-state-equivalence acceptance or physical touch tests.

| Median of two run results | Reference | Shared source |
|---|---:|---:|
| Uploads per pose request |0.4607|0.4391|
| Retained slot pixel MiB |23.36|23.30|
| Frame interval ms |50.40|50.45|
| P99 interval ms |86.27|89.25|
| Sampled gameplay footprint MiB |2029.0|2018.1|

Uploads/request fall about4.7%; no reliable total-RAM, FPS or initial-loading gain is established. Footprint samples overlap run-to-run variation; the window is an approximate PID-matched native1Hz subset, not allocation attribution. First redraws remain507–595ms. First reference setup is slower than later runs, so the apparent setup difference is not attributed to sharing. Eight active minutes is a targeted comparison, not a long-soak/leak/release clearance. Console processes are deliberately terminated only after results/save checks; their exit1 is recorded as an intentional stop. Console output is sparse on this wrapper and does not establish an error-free full game log.

## Rejected page experiment and next direction

The cropped six-frame page initially passed 46/48 native/device checks and reduced its pixel payload 67%. Expanded arbitrary-zoom testing failed 18 of 86 native comparisons. Crop/transpose/material fallbacks and later long-clip chunking did not establish a general pixel-equivalent replacement. Atlas code/UID/tests are preserved outside the repo and its bank/router/display changes were restored byte-exact. The installed playable build never received it. Earlier largely paused station lanes are excluded from active-performance claims.

The active pose GPU cache is only about23MiB in this fixture; it is not the main2GiB footprint. The same bank retains 134.0 MiB of compressed CPU pixels and 16,432 frame references. Next investigate a bounded on-demand CPU animation store and first-viewport room/render preparation, with original full-frame pixels and checkpoint compatibility as gates. Inventory payloads are not additive whole-process RAM measurements.

Evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261021/crew-source-sharing/HANDOFF.md`, RESULTS.json, probe-signed-build.json, probe-pack-audit.json and physical/*; rejected page evidence is adjacent in compact-crew-pages. Exact before/after slot patch is change.patch. Current owner five-file backup is in compact-crew-pages/owner-backup; final restoration receipt records after-launch hashes. Owner state remains cycle 64 / seven rooms with exact crew/timer; only background-save timestamp/event history changed before restoration. Keep current and rollback packages intact.
