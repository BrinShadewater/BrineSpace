# Biodome registered pass

## Fern contour repair: card v4

The upper-left edge of the tallest left fern now follows the leaf contour rather
than retaining a grey donor-floor fringe. Only this part of the source-space
outline changed; pivot, scale, footprint, effects, pipe opening and source raster
are preserved. Source SHA256:
`88FEDA3D0E5DABB1C2CBAF70D5A1D0E0ECCBA7982F2265F6073101E5E0C2D070`.
Card v4 is selected in station/card mappings and the export manifest; prior cards
remain. Its 512-square native bake was visually reviewed and has LFS attributes.

`output/batch-two/biodome-fine-edges-before-v1` and `-after-v1` retain all eight
native prop-only captures. Reviewed tree/light, fern/dark and processor/light
before, then fern/dark after. All six non-fern captures are pixel-identical.
The dark fern capture changes 872 pixels: 323 differ by more than one 8-bit
channel step; those larger differences lie within `(236,216)-(315,262)`.
The other 549 differences are one-step sampling changes; the complete fern frame
is not claimed pixel-identical outside the contour. Fine remaining margins are
not certified by this local repair.

`biodome-fringe-before-v1` exits 1 with 12 expected fringe assertions (three points
in each rotation). The unchanged checks pass after repair in
`biodome-fringe-after-v1`: retained leaf/rim points, four rotations, four economy
cases, four host-local motion/offline/pause checks, input isolation, full bounds,
the retained processor opening and 808 legacy socket-route samples. All 61
full-frame PNGs independently measure 1600x900. Successful fixture, edge and card
logs contain no engine errors; raw-image warnings remain. Seven asset-audit tests
pass. These route checks do not certify autonomous crew traffic.

Fresh v21 individual exported checks now pass at actual 1280x720, 1600x900 and
2560x1440: 61 full-frame dimension checks per size, 183 total, with input
isolation exercised in each run. All runs exit zero without engine errors;
raw-image warnings remain. Evidence directories:
`output/batch-two/biodome-fringe-export-{1280,1600,2560}-v1`.
Reviewed the 1280 q3 room crop and 2560 q0 power-starved full frame; remaining
frames are tested/captured, not individually visually approved.

All three records identify pack SHA256
`E15270102F1A4895F8F6CA15B1AAA14EDE64740E0B1AA5FE71AFB8B94F007987`.
Renderer SHA256: `A6A1BA2E2312885EDBB47F8B0DBBEE6B24E2949A4BE5084A02854EDFAF9AC5C5`.
Selected card SHA256: `929FD07573FEBE6C0893A90A7079C74BF48D91C595C36B5374DD62D6D4123A33`.
The same package passes the ordinary 30-room tour, 84 transitions and 6,333
movement samples, with 36 full frames at 1600x900. Its movement-controller hash
differs from the failed v20 run; this art pass made no controller edit and does
not establish traffic recovery. See `docs/ROOM_TOUR_TRAFFIC_DIAGNOSTIC.md`.
V11 remains evidence for v3, not the current v4 contour.

The repair-loop skill now distinguishes retained leaves/rims from floor fringe
and exact pixel equality from bounded sampling differences. The bible clarifies
foliage silhouette preservation without requiring visible serrations at all zooms.

## Processor pipe opening

Card v3 replaces v2 in both live consumers and the export manifest. A verified
source-floor rectangle `(866,780,7,38)` between the tank and right return pipe
is omitted by cached source-polygon partitioning. This is a real visual opening,
not background-colored paint. The source image, scale, pivot, outer silhouette,
collision reservation and operating marks are unchanged.

Inspected `edge-biodome-v3/biodome_processor-light.png` against the prior native
view and source, plus card v3. The source-floor strip is removed; other margins
and foliage fringe remain under review. Positive tank/pipe and negative gap
points are checked in every rotation by the room fixture. Seven asset audit
tests pass; the card uses LFS. Capture/card logs have no engine errors.

Fresh standalone v11 now passes this card-v3 revision at actual 1280x720,
1600x900 and 2560x1440, including input isolation and 61 dimension-checked full
frames per size. See EXPORT_VERIFICATION.md. Full art approval remains pending.

`biodome-pipe-state-v4.log` passes four rotations, four actual economy cases,
per-host motion/offline/pause, complete bounds, gap/retained-hardware points and
808 socket samples with no engine errors at requested 2560. No new traversal
space is granted by the small visual gap.

Exact-size follow-up: native `biodome-pipe-exact-1280-v6` and `-1600-v6` pass
the same full room fixture with clean logs. Every state-sidecar full PNG was
independently checked as 1280x720 or 1600x900 respectively. The 1280 q0 room crop
was visually inspected; other frames were captured/tested, not newly approved.
The failed 1280-v5 run captured 2560x1440 due to inherited display settings; it is
preserved. Fixture-local preferences and clearing borderless mode fix the tested
size mismatch without modifying player preferences. Fresh export remains pending.

Agriculture/Bio architecture, maintained condition: pale moisture-resistant deck,
white composite hull and green equipment trim. The original 1254-square source,
hash and exact prompt remain in source-review.json / production-briefs.json.
No new generation, source overwrite or plant-acquisition mechanic was introduced.

biodome_view.gd registers a tree bed, fern bed, aquatic planter and nutrient
processor. Ground footprints are 94x74, 106x76, 96x66 and 108x80 world units.
Foliage/tank visible height is separate from ground depth; source polygons retain
protruding leaves and complete equipment. Ground centres rotate, art stays
south-facing, and full silhouettes stay inside the four-unit wall margin.

The engine owns the 384 cell, 48 floor module, 72 doorway and canonical north/south
ports. Unused sockets are flush walls. The floor uses quiet two-module seams and
short drainage slots at the front of each assembly, not the source grid. Hull
surface sampling is recorded in the renderer. Full-spectrum-white fixtures are
independent of operating effects. Both station/card mappings use biodome-card-v2;
the actual draft consumer uses aspect fit. Other session room mappings preserved.

Operating cues are irrigation strokes in the dry beds and circulation marks in
the aquatic planter/processor tank. Every host has a source-space effect envelope;
the test checks the bed/tank region as well as the full assembly. These envelopes
are not flood masks or simulation volumes. Plants do not vanish when power stops;
there is no foliage sway, growth/harvest animation or dynamic crop-state system.
Small painted green indicator/glass highlights remain source art, not a full
emissive-layer export. Fine foliage edges and concave service gaps retain some
source-background pixels at close zoom; further silhouette cleanup is separate
from the passing containment tests.

Native evidence in output/:

- biodome-state-v1 and v2 (1600x900), biodome-state-1280-v1 and
  biodome-state-2560-v1 pass four rotations, four-host motion/stillness, pause,
  full assembly/drainage containment, assembly non-overlap, canonical port masks
  and 808 supported socket-route samples. V2 adds explicit bed/tank-envelope tests.
- Four actual economy cases per rotation: functioning, missing water, missing
  power and suspended. Water shortage leaves normal lighting on but stops
  irrigation/circulation. Power loss/suspension stops motion and normal lighting.
  Resources are reset only inside the process-isolated fixture save/scene.
- biodome-station-v1: 404 actual neighbor-walker samples, four rotated Nursery
  seams, wall visibility, state comparisons and mixed 40-room station fit pass.
- biodome-depth-v1: 32 native front/behind poses with production actor geometry;
  all standable. Tree q0 behind and fern q1 front visually inspected. Remaining
  poses are captured, not individually visually certified.
- Four gameplay suites pass in biodome-test_* -v1 logs. Native and regression
  logs contain no ERROR/SCRIPT ERROR entries; inherited raw-PNG export warnings
  remain. New PNGs have Git LFS attributes; nothing was staged or committed.
- Card, native four-rotation sheet, connected room pair and actual 1280/2560
  economy frames inspected. output/biodome-four-rotations-v1.png preserves native
  crop pixels. Bright deck and green foliage remain distinct at gameplay scale.

Remaining: owner visual approval, fine source-gap cleanup and full depth/neighbor
family review. Export evidence is tracked in EXPORT_VERIFICATION.md; this is not
normal playable release acceptance. Plants are the current cultivated
presentation, not proof of future acquisition/restoration-state implementation.
This was the fourth registered batch-two room; all ten are now integrated.

Contrast-edge follow-up:

- `tools/capture_registered_prop_edges.gd` renders the actual offline registered
  prop against dark and light solid backgrounds at four pixels/world unit, with
  no room floor. It changes no source pixels and records view hash/scale/state.
- `output/biodome-edges-v1` exposed a triangular source-floor spike beside the
  left fern blade. Removing only three erroneous outline points excludes it;
  footprint, pivot, scale, source PNG and effects are unchanged.
- `output/biodome-edges-v2/biodome_ferns-dark.png` visually reviewed: the spike
  is absent. Tree/processor dark previews also reviewed; fine grey foliage fringe
  and pipe gaps remain, not claimed clean. Eight renders exist per diagnostic run;
  their existence is not blanket acceptance.
- The native fixture now checks the excluded floor point and a retained fern
  blade point. `output/biodome-state-v3.log` passes all four rotations, four
  economy states and 808 socket samples. It and edge/card logs contain no errors.
- Offline card v2 visually inspected and mapped in station, card and export
  manifest. Original card/source retained; new card retains Git LFS attributes.
- V4 standalone build passes mixed-station checks; the repaired Biodome passes
  its individual exported fixture at all three viewport widths. Exact paths and
  selective scope are recorded in EXPORT_VERIFICATION.md.
