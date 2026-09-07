# Holographic Core — integrated, September 6

## Terminal glass follow-up: card v7

The terminal's two flat offline screen interiors now have a recessed dark glass
surface and restrained diagonal reflection. Existing bezels, controls and other
equipment are untouched; powered traces still draw afterward and stop with
operation. Source, registration, collision, room geometry and effect anchors are
unchanged. This implements the bible's existing unlit-construction rule, not a
new universal glass palette or complete cyan-emission extraction.

Native `output/batch-two/holo-material-review-v1` precedes the repair; reviewed
compute/projector/terminal light-background captures. The subsequent
`holo-glass-review-v1/holo_terminal-light.png` and 512-square card v7 were reviewed.
All six non-terminal captures are pixel-identical between the two runs. Both
terminal difference bounds lie within `(346,313)-(521,381)` on the 800-square
diagnostic canvas. Card v7 is selected in station/card mappings and the export
manifest, with LFS attributes; previous cards and donor remain intact.

`holo-glass-before-v1` rejects the old flat screens with 16 expected assertions.
`holo-glass-after-v1` passes the added dark-glass variation check and existing
bay-detail/host-motion checks in four rotations. `holo-glass-negative-v1` restores
flat screens in the fixture only and fails all 16 glass checks as intended.
The separate hardware negative control still rejects blank computing bays.

`holo-glass-state-v1` exits zero without engine errors: four rotations, four
actual economy states including restoration, four host-local motion/offline/pause
checks, input isolation and 1,616 legacy socket-route samples. Its 61 full frames
independently measure 1600x900. `holo-glass-registration-v1` passes full bounds,
non-overlap and 59,040 effect samples. Seven asset-audit and five export-bridge
unit tests pass. Raw-image warnings remain. Remaining tiny cyan details and owner
visual acceptance are pending. These fixtures do not certify autonomous traffic.

Fresh v22 individual exported checks pass this v7 revision at actual 1280x720,
1600x900 and 2560x1440: 61 dimension-checked full frames per size, 183 total.
All three runs exit zero without engine errors, with input isolation exercised.
Evidence: `output/batch-two/holo-glass-export-{1280,1600,2560}-v1`.
Reviewed the 1280 q3 room crop and 2560 q0 power-starved full frame. This selected
visual review is not blanket acceptance of every capture.
All three records identify pack SHA256
`3A51B01D450721425EBE25F12E727424FB71C550E67CA05CD2455D1F0B94DB8C`.
Selected card SHA256:
`DA78370ED80BC8D6584BF2C7246CD2D3199BE0E19C5025D65B43BD1342445E17`.

The same package's ordinary station tour fails at Research Lab after one leg:
waiting-for-passage is followed by `route obstructed`. Asset loading passes, but
this does not constitute a passing whole-station traversal. The exact route and
changed furnishing geometry require investigation; do not assume a traffic-only
cause. See `docs/ROOM_TOUR_TRAFFIC_DIAGNOSTIC.md`. Earlier v11 evidence describes
card v6, not v7.

Source SHA256: `03096676BA7B8C76E3F77D6814F7C1DD2D04CC355565E3EB6876B3C655F9430D`.
Renderer SHA256: `D9AFDE2269645993B7FC94E96DEA55151DFBD178EDABCC1B05961587CECCABFA`.

## Calibrator contour follow-up

Card v6 now replaces v5 in both live consumers and the export manifest. Refined
source-space upper edges remove floor wedges above the crossbar and beside the
optical plate. Source, placement, collision and effects are unchanged.
`edge-holographic_core-v3/holo_calibrator-light.png` was inspected against v1
and the original source; card v6 was inspected at native size.

`holo-contour-registration-v6.log` passes four-rotation bounds/non-overlap and
59,040 effect samples, plus retained-beam/excluded-floor point regressions.
`holo-contour-state-v6.log` passes four rotations, four economy states including
restoration, per-host motion/offline/pause and 1,616 socket samples. These logs
and the card/capture logs contain no engine errors. Standalone v11 now passes
card v6 at actual 1280x720, 1600x900 and 2560x1440, with input isolation and 61
dimension-checked full frames per size. See EXPORT_VERIFICATION.md. Remaining
cyan/edge cleanup and owner approval are separate.

Eighth integrated room in this task's batch. Station and card consumers select v6.
The immutable source supplies projector, computing cabinet, optical calibrator
and terminal. The verified Data Archive supplies computing hull materials and
floor treatment. The gameplay category remains Science; no economy migration.

The four-port geometry comes from the shared base, not painted openings. Props
remain south-facing. The wireframe projection stays local to its emitter and
rotates slowly as a separate engine effect. Other hosts use status/calibration
traces. This does not create a BRINE aquarium or add a memory-recovery mechanic.

Evidence in output/:

- holo-registration-v1: four-rotation full containment/non-overlap and 59,040
  sampled effect points inside host/envelope. Perimeter walking still needs its
  own production-controller checks; centreline geometry is insufficient.
- holo-card-v1: native offline 512-square card, visually inspected; candidate only.
- holo-depth-v1: 32 standable native production-actor front/behind poses. q0's
  eight poses reviewed in holo-depth-q0-v1.png; other rotations captured but not
  yet visually reviewed.
- holo-pilot-v1: preserved fixture parse failure (Panel shadowed a native class).
  Renaming the helper HoloPanel fixes it. holo-pilot-v2 passes four-rotation,
  per-host working/offline motion comparisons, using directly supplied renderer
  state rather than economy. q0-working-0 inspected. No fixtures/power fade are
  drawn in this isolated machinery preview.
- Successful logs above contain no ERROR/SCRIPT ERROR. Inherited raw-image
  export warnings remain. This is not release or package acceptance.

Ring follow-up: projector_lens_quads() replaces the bright annular band while
preserving the recessed centre. Both rendering and validation use the same 32
source-space quads. holo-registration-v2 tests centre exclusion and containment;
holo-pilot-v4 passes all host motion/offline comparisons after the change. Native
offline q0 from v3 inspected; card v2 retains the correction without overwriting
card v1. Remaining cyan details are not claimed fully cleaned by this local fix.

Live integration evidence:

- holo-state-v1, holo-state-1280-v1 and holo-state-2560-v1 pass four rotations,
  four real economy states (working, power-starved, suspended, restored), per-host
  animation/pause and 1,616 canonical socket samples. These precede the small
  projector placement correction; holo-state-v2 reruns the corrected art at 1600.
- holo-station-v1 found six actual perimeter collision samples. V2 preserves a
  diagnostic indentation parse error; v3 reports exact foot positions. Moving
  only projector authoring x from -160 to -168 clears the contact; no resizing,
  socket or walker-path change. Card v3 contains that registration correction.
- holo-station-v4 passes 404 forward and 1,212 reverse/perimeter samples across
  all rotations, state checks and 40-room fit. q0 pair frame and native
  holo-four-rotations-v2.png visually reviewed. Other seam captures are not
  automatically visually accepted.
- holo-test_synergy_manager-v1, holo-test_discovery_progression-v1,
  holo-test_polish_gameplay-v1, holo-test_run_balance-v1 and
  holo-test_holo_registration-v1 pass. Latest successful state v2, station v4
  and regression logs contain no ERROR/SCRIPT ERROR entries.

Combined-batch follow-up:

- Twenty-room production-path coverage found 110 additional projector contacts.
  Moving authoring x from -168 to -172 clears all of them; card v4 and both live
  consumers agree. See CROSS_ROOM_VERIFICATION.md for full and focused counts.
- holo-registration-v4 passes containment and 59,040 effect samples.
- holo-state-v4, holo-state-1280-v4 and holo-state-2560-v4 pass four rotations,
  four actual economy states, four hosts and 1,616 socket samples each. These
  successful logs and holo-depth-v4 contain no ERROR/SCRIPT ERROR entries.
- holo-depth-q0-v4.png through q3 reviewed: all 32 static front/behind poses
  retain upright machinery and correct actor overlap ordering. This is not an
  autonomous traversal or pixel-perfect silhouette acceptance test.
- holo-four-rotations-v4.png and offline card v4 visually reviewed. No visible
  wall overflow in these views; dark replacement cabinet panels remain an art debt.

Remaining: painted cyan trim/indicator cleanup, finer
optical-rig background gaps, and package/owner acceptance.
The computing-bay flat covers have now been replaced; see the material follow-up.

Offline hardware material follow-up:

- Four computing bays redraw their original texture with a restrained RGB
  modulation (0.72, 0.52, 0.48), rather than opaque flat rectangles. Slot geometry,
  recesses and small hardware remain visible; operating traces stay separate.
  This does not introduce a shader or alter the source PNG. Faint source cyan
  details remain; this is not a full emissive-material separation claim.
- Native light-background compute capture in `edge-holographic_core-v2` and
  offline card v5 visually reviewed. The card and both live maps/export manifest
  select the new treatment. Geometry, registration and effect anchors unchanged.
- `holo-material-pilot-v1.log` passes all four rotations and host motion/offline
  checks, plus at least eight distinct interior pixel colours in each offline
  computing bay. Crops exclude the frame to avoid bezel texture passing the test.
- `holo-material-negative-v1.log` deliberately recreates the old flat bays in a
  test-only subclass and exits 1 with 32 offline-detail rejections. This proves
  the check detects flattening, not that colour count alone proves good art.
- `holo-material-registration-v1.log` passes full bounds/non-overlap and 59,040
  effect samples. Successful pilot/card/registration logs contain no engine
  errors. Export scope is recorded separately in EXPORT_VERIFICATION.md.
