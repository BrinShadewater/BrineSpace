# Research Lab registered pass

The existing Research Lab now uses its generated Science equipment in station,
placement preview, draft and inspector consumers. `research_lab_view.gd` records
the exact source outlines, world footprints, pivots, wall samples and local effect
anchors. Source art remains unchanged, including its opaque exterior checkerboard;
only registered regions are rendered. Cards use a native 512-square bake and
full-image aspect fit. Legacy alternates remain on disk but no longer override it.

The scanner is rendered as separate textured frame/head/base polygons so gaps
beside the head reveal the shared floor, rather than retaining source-floor colour.
The other three silhouettes remain single polygons; small source-floor areas
inside cable returns are a known extraction limitation. Piece boundaries and
complete silhouettes still merit close visual owner review.

Equipment remains south-facing through rotation. The actual south-only database
mask replaces the inherited cross mask. Three operating cues—specimen monitor,
analysis traces and scanning line—follow their hosts. The supply cabinet stays
still. No costs, production, unlocks, saves or hidden recipes changed.

## Evidence

`tests/playtest_research_lab.gd` passes at 1280x720, 1600x900 and 2560x1440:
four rotations, per-host operation/inactive/pause image comparisons, effect-point
containment, complete visual containment, non-overlapping footprints, sealed
disconnected sockets, canonical south-only topology and 364 center-to-port route
samples per viewport. Logs and native captures live in
`output/production-ten/research-native-*` and `research-*.log`.

The card and a 2560 native rotated station/draft/inspector frame were inspected.
Synergy, discovery progression, polish gameplay and run balance suites pass.
No ERROR/SCRIPT ERROR lines were found in research test stderr logs. Inherited
raw-image export warnings persist; PNG source and card use LFS attributes.

## Still pending

Neighbor/production-actor crossings, incompatible/disconnected pixel seam review,
actual economy-driven power cases, mature mixed-station zoom, checkout-independent
packaging and owner visual approval remain. Fixture state injection proves the
renderer contract, not every economy transition. This is initial integration,
not full production acceptance. Eight other rooms in this ten-room batch remain
at source stage; Battery has a separate initial integration record.
