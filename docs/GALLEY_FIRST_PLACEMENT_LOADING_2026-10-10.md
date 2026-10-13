# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: first-placement loading hitch

## Objective and acceptance

Continue the full PC/Mac performance and release plan. Reduce the reproducible
reported-station construction hitch while preserving selected pixels, geometry,
gameplay and historical preview/fallback artwork. Full release gates remain open.

## Accepted decisions and constraints

Keep lazy legacy galley artwork loading in normal source. The old PNGs and north
kitchen template remain available on actual bounds/draw requests. No art deletion,
quality reduction or change to navigation algorithms, owner layouts or gameplay.
Use muted secondary-display native tests, isolated profiles and owner fingerprints;
reuse the retained physical package instead of making full package copies.

## Current state

Changed `rooms/underwater/galley-v1/galley_view.gd`: stop loading kitchen/serving
PNGs and the old north kitchen template at ready. Retain identical decode, region,
texture and fallback drawing logic behind on-demand requests. Whole quoted PNG
paths replace the old constructed path. Internal `--reference-eager-galley` selects
the original eager behavior for matched measurements. Normal file is byte-identical
to the measured V2 candidate.

Added `tests/test_galley_lazy_art.gd` and Godot-generated paired UID
`uid://3wl35d4np7vj`; registered performance-diagnostics with an explicit native lane.
No new packaged delivery, commit or upload. Frozen Windows/Mac packages still omit
this and the later accepted shadow changes.

## Verification

Reported12 source data: first-placement frame has no drone upload. Crew update
123.5ms is almost entirely first galley geometry setup, not goal choice or routes.
New isolated template census attributes111.437ms to geometry creation; galley
point generation1.008ms/links2.233ms. Navigation redesign would miss this cold cost.

Diagnostic fixture first failed because placement-only phases left the new galley
in place. Corrected placement/demolition fixture completes job79442 with owner2,938
unchanged. First V1 lazy PNG trial completes four runs/4,320samples: first-placement
210.337->171.340ms and211.810->179.629ms, ~16MiB texture reduction, states equal;
average frame results nearly unchanged. V2 also defers the north template.

Actual debug=false V2 comparison job49218, reported12 with copied owner layouts,
RTX4070Ti/1080p, placement/demolition at1x/2x/4x, four runs/4,320samples:

| Metric | Forward eager / lazy | Reverse eager / lazy |
| --- | --- | --- |
| First1x placement |216.210 /150.785ms|211.034 /154.357ms|
| Simulation step in that frame |133.678 /68.121ms|131.285 /71.390ms|
| Overall mean |14.608 /14.766ms|14.942 /14.724ms|
| First phase texture counter |1602.841 /1580.843MiB|1602.841 /1580.843MiB|
| Frames >100ms |1 /1|1 /1|

All12 paired phase-end states equal, clean engine/art/profile/display/input guards;
owner2,938 unchanged. Admission is a targeted27–30% construction-hitch and ~22MiB
retained texture improvement, not a general FPS gain. Means are mixed and every run
still fails the >100ms stall gate. Texture counters are engine measurements, not
independent driver VRAM certification. No large-map improvement is claimed.

Original-source versus V2 native rendering:48 byte-exact prop pairs across four
rotations, powered/unpowered operation and original overhead/legacy fallback
paths. First kitchen image visually reviewed. Normal-source functional test14checks,
zero failures: cold state, requested-image-only loading, exact decoded pixels and
source regions, bounds and repeated texture identity. Source hashes match tested
candidate. Pixel harness had two preparation failures (empty process query exit
status and missing helper in frozen source); corrected V3 succeeds, earlier logs
retained. All actual test owner guards unchanged.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`placement-template-census-v2/template-analysis.json`,
`galley-lazy-performance/paired-analysis.json`,
`galley-lazy-v2-performance/paired-analysis.json`,
`galley-lazy-v2-pixels-v3/results.json`, `galley-lazy-normal-functional/`.
Drivers and small pixel fixture under `output/renderdoc-tools-2026-10-08/`.
Runtime configuration/fixture restored, jobs terminal. Latest free C124.36GiB /
D81.41GiB. No full PCK copies or automated screenshot batches created.

## Next action

Profile the remaining cold galley setup and ~68ms drawing independently, preserving
the complete interactive room and selected pixels. Large-map visible drone upload
bursts remain a separate unresolved cost; reuse rejected cache/cropping/indexed and
floor/wall trial evidence. Finish full original bug/endurance, target-PC/Mac native,
frame/stall/memory, release packaging/signing/notarization gates. No itch publication.
