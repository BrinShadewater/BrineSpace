# Xeno Lab registered pass

## Neutral lens repair: card v4

Five vessel lamp interiors now use source-space polygons and nested dark blue-grey
glass, preserving the previously modulated housings outside those faces. The
two upper lamps, front strip and sloping base indicators no longer read olive.
Tiny supplemental regions remain unchanged; this is not full emissive extraction.
Source raster, equipment placement, collision, effects and sockets are unchanged.
Card v4 replaces v3 in both mappings, variant fallback and export manifest.

Reviewed native vessel light-background `xeno-neutral-lamps-review-v1` and the
512-square card. Compared with `xeno-aperture-review-v1`: all six captures of
the other three props are pixel-identical; the two vessel frames differ in 3,010
pixels, all within the five existing lamp-region envelopes plus a two-pixel
raster allowance. This verifies those diagnostic frames, not every state/rotation.

The new five-point lamp-colour regression fails against the former renderer in
`xeno-neutral-lamps-before-v1`. Repair v1 fails the existing front-strip detail
test; v2 adds another recessed glass layer and passes unchanged source-highlight
coverage, six surface-detail checks and five lamp samples in all four rotations.
Failed logs are preserved. Native card/capture/material success logs contain no
engine errors; raw-image warnings remain. Original source and old cards survive.

Station v1 caught an old variant mapping loaded before that mapping was patched;
the assertion was not changed. Station v2 passes with all consumers updated:
four rotations, four hosts, motion/offline/pause, three actual economy states,
containment and input isolation. All 53 full frames independently measure
1600x900; the q3 room crop was reviewed. Legacy route-helper checks are not
current autonomous crew evidence. The flat-material negative control still
exits 1 with all 24 expected surface-detail failures.
Fresh card-v4 individual standalone checks now pass in v20 at actual 1280x720,
1600x900 and 2560x1440: 53 dimension-checked full frames per size, 159 total.
Each run exits zero with no engine errors and exercises input isolation,
four rotations, host-local motion/offline/pause and three actual economy states.
Raw-image warnings remain. Reviewed the 1280 q3 room crop and 2560 offline q0
full frame; this is selected visual review, not owner acceptance of every frame.
Evidence directories: `output/batch-two/xeno-neutral-lamps-export-{1280,1600,2560}-v1`.
All three verification records identify pack SHA256
`A1399F00525F1A6BAD0B8D3FFF08807106AE65DFAD3D11D44201646824412A1F`.
Renderer SHA256 at this export:
`970DA601BDD53E6FC8DF42F9AFC9A641A8AF81AC0A26B44F5465CBCE66531520`.

The same v20 package's ordinary controlled station tour fails at Crew Lounge
after seven completed legs, with a retained crew-traffic trace. Asset checks
pass, but the whole-station traversal does not. Individual Xeno results do not
certify autonomous crew recovery; see `docs/ROOM_TOUR_TRAFFIC_DIAGNOSTIC.md`.
V19 remains evidence for card v3, not v4.

Both skill copies' repair-loop reference now requires checking unintended hue
shifts as well as retained detail. The bible clarifies lens-versus-housing repair
without imposing a universal glass palette. Both skill copies validate.

## Fresh aperture review after v19 export

Inspected the immutable donor and native offline vessel close-up in
`output/batch-two/xeno-aperture-review-v1/xeno_vessel-light.png`. The optical
centre retains depth, but the two upper strip lamps and lower/front indicators
still show the muted olive tint from RGB modulation. Keep their surrounding
metal/angled housings; target actual lens interiors in the next repair rather
than replacing the complete rectangular regions. Source regions 1/2 (upper
lamps), 3 (front strip), and 4/5 (sloping base indicators) are the priority.
Tiny supplemental masks remain separate. The native capture run exits zero
without engine errors; this review changed no renderer, donor or selected card.

The eight captured images are an inventory, not eight reviewed props: only the
vessel light-background image was inspected in this pass. Card v3 remains current.

Coverage correction: the material-export runs labelled 1280 and 1600 actually
captured 2560x1440 full frames. Their earlier three-size claims are superseded;
see EXPORT_VERIFICATION.md. Fresh standalone v11 now passes card v3 at actual
1280x720, 1600x900 and 2560x1440, with input isolation and 53 dimension-checked
full frames per size. Fine aperture/material review remains pending.

Science host architecture with localized containment instruments: pale blue-grey
deck, white/grey hull, blue equipment and a restrained violet vessel cue. The
existing Anomaly gameplay category, single south socket, costs and unlocks are
unchanged. Source hash and exact prompt remain in source-review.json and
production-briefs.json. The generated tee shell was rejected, not rotated or
cropped into a false claim of correct topology.

xeno_lab_view.gd registers the complete vessel (78x72 ground footprint), scanner
(106x70), sample cabinet (94x68) and workbench (94x70). Ground centres rotate;
upright equipment remains south-facing. Full silhouettes and short service lines
stay within the four-unit wall margin. Shared engine geometry controls infill,
72-unit doors and independent white fixtures. Card/station/variant consumers all
use xeno-lab-card-v3.png; legacy originals remain on disk but are not selected.

Operating effects: vessel scan line/lens, scanner traces, sample diagnostic marks
and a work-surface scan. The manipulator itself does not articulate. Preserved
green samples and dark glass remain static source contents, not acquisition or
specimen-state systems. Bright violet indicator apertures are separately drawn;
the source audit initially found 20 uncovered pixels, then passed after local
coverage corrections. This threshold audit is not an exhaustive emissive mask.
Small concave silhouette gaps may still retain source background at close zoom.

Evidence in output/:

- xeno-registration-v1 preserves the 20-pixel failure; v2 passes. Original source
  and card v1 are preserved; card v2 includes the corrected apertures.
- xeno-state-v1 preserves a fixture type-inference parse failure, fixed explicitly.
  xeno-state-v2 (1600), xeno-state-1280-v1 and xeno-state-2560-v1 pass four rotations,
  four-host activity/stillness/pause, surface envelopes, aperture containment,
  full bounds/non-overlap, single-door topology and 404 static socket samples.
  Powered, power-starved and suspended cases use the actual economy in each layout.
- xeno-station-v1 passes 404 forward plus 404 return production-walker samples,
  four rotated reciprocal seams, state comparisons and mixed 40-room fit. The
  Nursery turns to face the single Xeno socket; topology was not loosened for art.
- xeno-depth-v1 has 32 standable poses. The new close-up fixture v2 exposed an
  insufficient review gutter and was stopped after its assertion. V3 passes all
  32 poses/crops with extra canvas margin at unchanged 2x world scale. All front/
  behind prop pairs were visually inspected in xeno-depth-q0..q3-v1.png. This is
  static depth evidence, not a free-roaming controller or animation-state audit.
- xeno-test_synergy_manager-v1 hit a resource preload failure; retry v2 passed
  without changing database/test logic. Discovery, polish and balance v1 pass.
  Latest successful logs have no ERROR/SCRIPT ERROR entries. Historical failure
  logs remain. Inherited raw-image export warnings remain; release packaging is
  not established by this pass. xeno-main-smoke-v1 loads without engine errors.
- Card, native four-rotation sheet, connected pair and actual 1280/2560 state
  frames inspected. xeno-four-rotations-v1.png retains native crop pixels.

Pipeline corrections:

- capture_registered_room_poses.gd now records full-host/actor detail crops plus
  JSON crop coordinates, with a 1000x1040 canvas and unchanged 2x sprite scale.
  review_registered_depth.py assembles one rotation's eight native crops without
  resampling, making every prop/actor pair practical to review.
- An engine round-trip audit caught invalid hand-written UID sidecars introduced
  by this session. After checking they had no other source references, the five
  registered views, seven related tests and pose tool received engine-generated
  IDs. Existing user identities were not rewritten. The new read-only
  test_batch_two_resource_uids.gd validates 14 paired/canonical/distinct IDs,
  including its own. Evidence: batch-two-resource-uids-v1.log.

Historical remaining list at initial integration: owner aesthetic approval, complete export/package verification, fine
source-gap cleanup and additional neighbor/autonomous traversal cases. No new
aliens, contamination spread or specimen loading is implied. Five batch-two rooms
are now registered; Anomaly Lab, Bio Lab, Holographic Core, Medical Center and
Medical Office still need their integration passes.

## Offline material follow-up

Card v3 now replaces v2 in station, alternate-art, card and export-manifest
consumers. All ten batch-two identities have since been integrated; see the batch
README and EXPORT_VERIFICATION.md for subsequent scoped export evidence.

The vessel's nine small indicator regions retain original housing texture through
local RGB modulation (0.62, 0.70, 0.48), rather than blank rectangles. Their glass
now has a muted olive tint. The optical lens uses three dark nested surfaces,
not its original bright violet points. This improves offline construction but is
not full emissive extraction or a claim that every aperture contour is finished.
Source PNG, registration, collision, sockets and functioning marks are unchanged.

Inspected the vessel light-background native capture in `edge-xeno_lab-v4` against
v3 and the new 512-square card. Hardware contours/readable inset details return;
the lens no longer reads as a single flat fill. Other captures in this set were
not individually reviewed. `xeno-material-registration-v6.log` passes original
source-aperture coverage and six material-interior variation checks in all four
rotations. `xeno-material-negative-v6.log` exits 1 when fixture-only flat covers
are restored. Earlier v4/v5 test attempts had parser errors, retained separately;
they are not negative-control evidence. Successful capture/card/registration logs
have no ERROR/SCRIPT ERROR entries. Seven batch audit tests pass; card uses LFS.

Current repair still needs owner approval. Fresh standalone V8 and the three
`xeno-material-export-<width>-v1` records now verify the material/card revision;
see EXPORT_VERIFICATION.md for exact checks and limited visual-review scope.

`output/batch-two/xeno-state-v4.log` passes the integrated four-rotation room
fixture: four hosts, motion/offline/pause, containment, three actual economy
states and 404 supported-socket samples. This does not establish autonomous
all-room visitation or a fresh standalone package.
