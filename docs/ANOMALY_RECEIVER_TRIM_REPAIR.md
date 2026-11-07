# Anomaly receiver trim repair

Status: focused repair integrated; normal-scene motion verification needs an
occlusion-aware measurement follow-up. No fresh package claim. Low walls, room
geometry, machinery motion, source raster and furnishing layout are unchanged.

## Visual finding

The receiver's small front indicator suppression mask covered pale fascia as if
the entire rectangle were a dark lens. The donor close-up at
`output/anomaly-receiver-trim-source-v1.png` records source `(1005,925,50,40)`
at integer zoom 10. The actual fitting is smaller than the suppression region.

The renderer reconstructs the pale fascia within the existing region, then the
small recessed bezel/lens at `(1022,941,16,7)` with inner dark layers. This is a
local reconstruction, not preservation of every donor pixel. The three optical
windows and their motion are unchanged. No new blinking or light was introduced.

Renderer SHA-256:
`18EE7384363912DA5797CE6D489D712852874078C5F12B1F18903CEE593DCB78`.
Unchanged donor:
`67E810D4F3D2D87EEC9A16A70E71F2C40D0267091996E97FB44CB96FB0B1DE7A`.
Unchanged composition profile:
`6372E5F8DB0C40A1A342E910D8227F033CF00DD81E77F21F132DA3C55C9660F9`.

## Focused evidence

- `test_anomaly_receiver_trim.gd` fails eight pale-trim samples on the old renderer
  (`anomaly-trim-red-v2`, child 1) and passes all sixteen trim/dark-lens samples
  across four quarters after repair. Initial red-v1 was a fixture class-name parse
  error, not evidence of the art defect; it remains retained.
- `anomaly-finishing-edges-v1` / `anomaly-trim-edges-v1`: ten native offline
  diagnostic images each. All eight non-receiver images are SHA-identical.
  Repaired receiver dark-background image and new card visually reviewed.
- `anomaly_lab-card-trim-v10.png`, 512 square, is selected in both consumers and
  the batch-two manifest. SHA-256:
  `6ABD56CD4012BA4E7C2D51753DE7D37E16284619825A9CF16C914CDB60BD0EFD`.
  Previous organic-v1 card retained; LFS attributes and batch-two consistency pass.
- Native material tests pass four main-donor hosts, receiver optical depth,
  capacitor glass and ten platform strips. The flattened-lens negative control
  still fails twelve checks (`anomaly-trim-negative-v1`, child 1).
- The source indicator audit initially sampled the recording cart's coordinates
  from the wrong image, reporting 2,665 unrelated violet pixels. The profile uses
  `archive-service-cart-v1.png`; it does not use the room donor. The audit now
  reports four main-source hosts and one excluded separate-texture furnishing.
  This is not a claim that the cart has no emission. Dependency checks pass all
  ten batch profiles. The skill records this source-ownership lesson.
- Native editor import passes without engine/script errors and generates the
  new test and diagnostic script UIDs.

## Normal-scene motion result and controlled comparison

`output/anomaly-trim-native-v1` exits 1 with two diagnostics-machine motion
assertions: the generic host-motion check and the economy-driven host-motion
check. All four room crops were reviewed. The q1 crop shows Bill covering the
diagnostics display. No assertion identifies the repaired receiver as failing.

`tools/probe_anomaly_motion.gd` runs the same inherited room assertions while
disabling crew rendering before every capture. Its
`output/anomaly-motion-no-crew-v1` run exits 0 with no engine/script errors;
the q1 crop was reviewed and exposes the display. It retains four rotations,
three economy states and 404 socket checks. Its generic inherited PASS message
must be read with this explicit no-crew scope, not as normal-scene acceptance.
The comparison supports occlusion as the measurement failure mechanism.

## Separate measurement follow-up

`tests/playtest_anomaly_room.gd` now saves the normal review capture first, then
caches machine pixels in a separate crew-free pass and restores all three active
flags before continuing. Supplementary room crops and scope/state metadata live
under `machine-measurements/`; they are not crew-depth acceptance images.

`output/anomaly-measurement-native-v1` reports zero assertions. The normal q1
room crop was visually inspected with crew present, alongside the unoccluded
q1 operating crop. Metadata records all three active flags restored to true.
The negative control overrides diagnostics effect generation with no marks:
`anomaly-measurement-negative-v1` exits 1 with exactly eight diagnostics-motion
failures (four generic and four economy-driven). The assertions remain effective.
All six generated export-bridge consistency tests pass.

No display enlargement, furniture relocation, production crew change or wall
height change was needed.

## Fresh package: split result

`output/batch-two/anomaly-trim-package-v1` imports, passes host preflight and
exports. Runtime loads 20 source hashes, 40 raw PNGs, 29 component assets and 19
composition profiles, but fails `Controlled tour initializes the production NPC`.
Do not call this a passing mixed-station tour. PCK SHA-256:
`327E4170EFB0ABBFD37E0D2830D3F2DA55A8ACA7584DF88A6D26535656D3E2BD`.

The shared checkout now gates NPC updates through `Architects.present`, which
requires a living recovered architect for nonlegacy runs. Individual exported
measurement metadata records all three active flags as false, unlike the earlier
native comparison's three true flags. The fixture preserves those flags; its
generic wording about retaining crew means retaining input visibility state,
not proving that crew are present. Exported machine-state results therefore must
not be reported as crew-depth validation. Adapt fixture setup to the actual
recovery lifecycle next, without disabling production progression rules.

The same PCK passes individual Anomaly checks at actual 1280x720, 1600x900
and 2560x1440: 53 dimension-checked full frames per size, 159 total, child 0,
no engine/script errors and input isolation exercised. Evidence:
`output/batch-two/anomaly-trim-export-{1280,1600,2560}-v1/verification.json`.
Supplementary measurement crops are separate from those full-frame counts.
This passes machinery/state assertions, not the mixed tour or crew-depth review.

Both project and installed repair-loop skill copies now require separate
occlusion review and machine measurement with a missing-effect negative control.
Both validate and match SHA-256
`BC5D585D899ABA0408CA4EFA0CDC1C6B04D98C7A6D663F450122F1DA85A0B114`.
The bible's approved low-wall and material direction is unchanged.

## Recovered-crew station follow-up

The controlled-tour fixture now completes Bill's actual emergency core wake via
`Architects.advance_core` before movement. Pause is restored afterward. It does
not clear architect state, insert a fabricated roster or change production code.
This deliberately wakes Bill only; Veld and Branforth remain unrecovered.

`output/anomaly-recovered-tour-native-v1` exits 0 without engine/script errors:
30 scheduled arrivals, 30 visited rooms, 86 reciprocal transitions and 6498
collision/speed samples. The fresh Windows package
`output/batch-two/anomaly-recovered-package-v1/verification.json` independently
passes the same tour from an external working directory, plus loading gates.
PCK SHA-256:
`28AD517031FF55C9096F6F6AB663A9F2C9E1053898B6AA3FC3A6C7D4C52A7D93`.
This is single-crew scheduled traversal, not three-crew avoidance or autonomous
destination-choice coverage. The earlier failed package remains failed evidence.

Normal capture sidecars now record `crew_active` and `crew_present` in Bill,
Veld, Branforth order. The packaged tour-start sidecar reports `[true,false,false]`
for both, at actual 1600x900. Anomaly measurement wording now explicitly allows
inactive input crew. All six generated-bridge consistency checks pass.

The skill records recovery prerequisites and crew-count evidence; both copies
validate and match SHA-256
`1995ED79ED2374C4EB79EE4CFFA248373F4ED0BD9A8BAB1A4E17EF3A7984BA5A`.
Remaining: recover additional crew through their actual lifecycle for traffic
review, and continue the room-specific visual queue. No new aesthetic rule was
needed; low walls, 72-unit doors and south-facing equipment remain unchanged.
