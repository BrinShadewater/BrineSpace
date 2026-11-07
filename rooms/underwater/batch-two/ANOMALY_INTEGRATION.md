# Anomaly Lab integration — September 6

## Platform strip follow-up: card v9

Ten existing platform masks now carry dark recessed lenses, with a 1.5-source-unit
polygon inset following straight and angled strips. Source raster, aperture
coverage, collision, placement and operating effects are unchanged. Card v9 is
selected in both live mappings and the export manifest; v8 is retained.

Reviewed native platform light-background before/after captures in
`output/batch-two/anomaly-platform-{before,after}-v1`, card v9 and the native q0
room crop. The strips now retain a rim/lens distinction without re-sampling the
donor's violet activity. Tiny supplemental masks remain a separate review item.

`anomaly-platform-positive-v2` passes source-highlight coverage, existing optical/
capacitor materials and ten strip interiors across all four rotations. The flat
platform negative control exits 1 with 40 expected strip failures. Positive v1
failed 11 detail checks at whole-room scale; v2 resolves the same art in a native
4-pixels/world-unit prop diagnostic. This does not assert all bezels resolve at
distant gameplay zoom. Both v1 records remain available.

`anomaly-platform-station-v1` passes native 1600x900 four-rotation checks, per-host
motion/offline/pause, three actual economy states, containment and input isolation.
Legacy socket samples are not current autonomous-NPC evidence. No engine errors
were reported in the accepted native runs; raw-image warnings remain. Card uses
LFS. All 53 full-frame captures independently measure 1600x900.

V18's mixed-station export is not accepted: all 20 room-source hashes/40 raw
source-card decodes and three component assets pass, but the controlled tour
fails physical arrival at `(25,21)` (Holographic Core), after capturing Anomaly
arrival 26 and Bio arrival 27. The cause is not established by this art pass.
No controller, geometry or arrival gate was changed to make it pass. Failed
logs remain in `output/batch-two/windows-validation-v18`. Anomaly-specific
exported state runs are separate from that mixed-station result.

Those individual v18 runs now pass at actual 1280x720, 1600x900 and 2560x1440:
`output/batch-two/anomaly-platform-export-{1280,1600,2560}-v1/verification.json`.
Each has 53 dimension-checked full frames (159 total), input isolation and zero
engine errors. PCK SHA256:
`B1C81A8418268A4086618471BA46E54CA2E46EA415E969C0C67662AF46175F65`.
The exported 2560 q3 room crop was visually reviewed; this is not an all-seam
review or a passing mixed-station tour. Tiny masks and owner approval remain open.

Workflow follow-up: both skill copies now route focused repairs to
`references/repair-loop.md`; both validate and their edited files match by hash.
The bible clarifies unlit hardware construction versus emission. Its original
mixed-encoding file is preserved in `output/batch-two/bible-before-utf8-normalization-v1.md`;
one Windows-1252 em dash was normalized before the narrow documentation edit.

## Small indicator follow-up: card v8

Diagnostics, capacitor and receiver indicator covers now retain dark recessed
lenses. The grouped receiver/diagnostic lamps use separate slots rather than
one blank panel. Card v7/edge v5 was an intermediate visual trial, not selected;
card v8 is selected by both live consumers and the export manifest. Raw sources,
registered placement, collision, aperture bounds and animation anchors stay intact.
Platform strips and tiny supplemental highlight masks remain separate polish debt.

Reviewed edge-v5 diagnostics/receiver, revised edge-v6 receiver, card v8,
exported 1280 q0 and 2560 q3 room crops. This is not a complete seam/depth review.
The material-v2 registration test passes; native bake/capture logs have no engine
errors. Seven asset-audit and four bridge tests pass; card v8 uses Git LFS.

Standalone v12 now verifies card v8 at actual 1280x720, 1600x900 and 2560x1440:
`output/batch-two/anomaly-indicators-export-{1280,1600,2560}-v1/verification.json`.
Each passes all four rotations, three economy states, host motion/offline/pause,
containment, 404 socket samples and input isolation, with 53 dimension-checked
full frames per size (159 total). The v12 controlled tour passes 30 arrivals,
84 transitions and 6,367 movement samples. See EXPORT_VERIFICATION.md for hash
and scope. Raw-image warnings remain; this is not release or owner acceptance.

## Capacitor glass follow-up: card v6

The three capacitor apertures now use bounded, recessed blue-grey glass instead
of uniform grey suppression rectangles. The immutable source, aperture coverage,
placement, collision and operating strokes are unchanged. Native light-background
close-up `edge-anomaly_lab-v4/anomaly_capacitors-light.png`, card v6 and native
room q2 were visually reviewed. The new shading is deliberately non-emissive.

`anomaly-capacitor-material-v2.log` passes source coverage and all four rotations
of receiver/capacitor material checks. The flat-capacitor negative v2 exits 1 with
twelve expected material failures. Negative v1 also leaked an unused test node;
the fixture allocation was corrected and the failed evidence retained.
`anomaly-capacitor-state-v1.log` passes four rotations, three economy states,
per-host motion/offline/pause, containment, 404 socket samples and input isolation.
Its 53 full frames independently measure 1600x900. Positive, capture and card
logs have no ERROR/SCRIPT ERROR entries; legacy raw-image warnings remain.

At this earlier checkpoint both live card consumers and the export manifest selected card v6; seven asset
audit and four export-bridge tests pass, and the PNG has the LFS filter. The
bridge is regenerated, but the v11 standalone binary still contains card v5.
Fresh packaged v6 coverage, other indicator covers and owner approval remain
pending. Historical v5 three-resolution evidence below is not v6 coverage.

Coverage correction: material-export runs labelled 1280 and 1600 actually
captured 2560x1440 full frames. Fresh standalone v11 now passes card v5 at actual
1280x720, 1600x900 and 2560x1440, with input isolation and 53 dimension-checked
full frames per size; see EXPORT_VERIFICATION.md. Remaining indicator-cover
polish is not implied complete by these passes.

Sixth registered room in this task's ten. Source retained unchanged; prompt and
hash remain in production-briefs.json and source-review.json. Active card v8 is
registered in grid_canvas.gd and room_card_art.gd (the current card consumer).

The four source equipment groups sit on the verified Science host, with pale
floor/cladding rather than the candidate's uniformly dark shell. Canonical
south-only topology, 384 cell, 48 module, 72 aperture and full visual containment
are preserved. Ground centres rotate; equipment continues facing screen-south.
Four restrained instrument effects stop when not functioning. Blue glass remains
static material; the violet coverage check is not a complete emissive export.

Evidence under output/:

- anomaly-registration-v1 caught 25 uncovered violet pixels. V2 passes after
  local aperture corrections; failed card v1 and original source remain intact.
- anomaly-state-v2, anomaly-state-1280-v1 and anomaly-state-2560-v1 pass all four
  rotations, four-host motion/offline/pause, three actual economy states (powered,
  power-starved, suspended), host/surface/aperture containment and 404 socket
  route samples per run. No production costs or recipe rules were changed.
- anomaly-station-v1 passes four rotated connected layouts, 404 forward plus
  404 return walker samples and mixed 40-room fit. Visual review covered the
  q0/q1 midpoint seam frames; this is not all-frame seam acceptance. Auto-fit
  uses different scales for vertical and horizontal pairs.
- anomaly-depth-v1 captures 32 standable production-actor poses at native 2x
  scale. All front/behind pairs inspected in anomaly-depth-q0..q3-v1.png.
  Static poses do not certify autonomous controller transitions.
- anomaly-four-rotations-v1.png inspected with unchanged native crop pixels.
- anomaly-test_synergy_manager-v1, test_discovery_progression, test_polish_gameplay
  and test_run_balance v1 pass. anomaly-test_batch_two_resource_uids-v1 validates
  17 paired canonical unique resource IDs. Latest successful state, registration,
  station, depth and regression logs contain no ERROR/SCRIPT ERROR entries.
  Existing raw-image export warnings remain; no release-package claim is made.

Read-only inspect_room_indicator_regions.py reports connected colour clusters to
help author aperture masks. Suggestions require semantic review: coloured paint
and glass must not automatically be erased as lamps. The stricter per-prop audit
still caught tiny highlights excluded by the helper's minimum cluster size.

Historical remaining list at initial integration: owner aesthetic approval, fine silhouette/background-gap cleanup,
additional neighboring-room cases and package/export verification. No anomaly
acquisition or containment mechanic was added. Bio Lab, Holographic Core, Medical
Center and Medical Office remain source candidates awaiting integration.

## Receiver lens material revision

All ten batch-two rooms have since been integrated; see the batch README and
EXPORT_VERIFICATION.md for subsequent evidence. Anomaly card v3 now shows layered
dark optical glass on the receiver's three faces. Its source active points remain
covered, with operating marks drawn separately. Other hardware covers are unchanged:
the broader modulation trial in `edge-anomaly_lab-v2` was rejected because strip
lamps still appeared illuminated offline. See PROP_EDGE_REVIEW.md for that finding.

`output/batch-two/anomaly-state-v3.log` passes four rotations, four hosts,
motion/offline/pause, containment, three actual economy states and 404 socket
samples, with no engine-error entries. `anomaly-lens-registration-v3.log` passes
source coverage and lens detail; `anomaly-lens-negative-v3.log` exits 1 for the
fixture-only flat-lens replacement. Seven asset audit tests pass. Card v3 was
visually inspected, uses LFS, and is selected by station/card/export consumers.

The latest lens/card change still needs a fresh standalone export. Remaining
hardware aperture reconstruction, fine silhouettes and owner approval are not
resolved by these tests. No gameplay, source PNG or prop placement changed.

## Slanted platform apertures

Two lower platform masks now follow their diagonal lamp openings, exposing the
surrounding metal. Native `edge-anomaly_lab-v3/anomaly_platform-light.png` was
inspected against v1. `anomaly-aperture-fit-v5.log` passes full source-highlight
coverage, positive/negative face points, and the existing lens checks. Card v5
is now selected by both live consumers and the export manifest; its clean bake
and inspected image supersede card v4's error-containing bake. Seven asset audit
tests pass. Other platform strips/capacitor masks remain unfinished.

State-v4 is invalid evidence despite its PASS banner: a transient shared BRINE
parse failure and actor dictionary errors were logged. The BRINE source had
already been corrected when inspected; this pass did not modify other work.
Standalone export remains pending for these aperture changes.

Retry `anomaly-state-v5.log` passes four-rotation motion/offline/pause,
containment, three economy states and 404 socket samples with no engine errors.
It began before the card-v5 mapping update, so use the separate clean card bake
and post-update asset audit for card selection evidence, not that runtime alone.

Standalone V9 now includes card v5 and passes controlled traversal. Individual
1280/1600-v1 and isolated 2560-v2 exported fixtures pass. The concurrent 2560-v1
run failed motion/pause assertions; its cause is unresolved, so retain this
intermittency caveat. All four 1600 room-rotation images were visually inspected.
See EXPORT_VERIFICATION.md for exact artifact hashes and evidence scope.
