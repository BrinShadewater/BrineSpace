# Holographic Core status-lens repair

The projector's four small cyan lenses retained bright source art offline.
This repair re-samples only their registered angled regions with uniform RGB
modulation: 0.24 offline and 0.85 operating. The original texture, lens shape,
surrounding machinery, optical plate and metal highlights remain. The main
wireframe projection retains its existing operation/pause behavior. No geometry,
wall height, room composition, source raster or gameplay rules were changed.

## Evidence

- `output/holo-material-current-v1/`: current baseline, ten native 800x800
  offline diagnostic frames on light/dark backgrounds.
- `output/holo-material-lenses-v1/`: first masks missed bright edge pixels;
  retained as rejected repair evidence.
- Source pixel inspection refined the four polygons. The registration regression
  now checks every bright cyan core in four bounded source regions. All 189 core
  pixels are covered. Four-quarter host containment and 59,040 effect samples pass.
- `output/holo-status-registration-v1.*` exits 0. The explicit
  `--negative-missing-status-lenses` run exits 1, missing all 189 pixels as intended.
  This tests mask coverage, not aesthetic quality or all cyan source pixels.
- `output/holo-material-lenses-v2/`: revised native edge review. The eight images
  of calibrator, compute, terminal and calibration cart are SHA256-identical to the
  baseline. Agent reviewed the projector diagnostic and the newly baked card.
- `output/holo-status-native-v1/`: child exit 0, no engine errors, five assemblies,
  four-quarter motion/offline/pause checks and actual functioning/power-starved/
  suspended/restored states, with 1,616 socket samples. There are 65 full 1600x900
  frames. The q0 functioning station frame was inspected; not every frame has
  visual approval. Fine lenses are necessarily small at station zoom.

## Integration

New 512x512 card: `rooms/underwater/batch-two/holographic_core-card-status-v8.png`.
SHA256: `5f8de77aa10c48ec690ddd2953de41ee94b158db0507fb85a3dfd58d2b8c2ebe`.
Renderer SHA256 at this checkpoint:
`c86eb78e879572b6651bdad2f27c102af9134217c510f854b975a838175a6641`.
Station, RoomCardArt and batch export-manifest consumers select the new card.
Git attributes confirm LFS handling; previous cards and the source remain intact.

Fresh package/all-size follow-up remains required. V22/V38 packages predate this
repair. Overall organic composition, other fine edges and owner visual approval
remain separate; this is a four-lens finishing pass, not completion of the room
catalogue or a claim that every cyan mark is an emissive fitting.

## Fresh Windows package verification

`output/batch-two/holo-status-package-v1/verification.json` records a clean debug
export and external-directory runtime: 30 scheduled arrivals, 84 reciprocal
transitions and 6,359 movement collision/speed samples. Import, native host gate,
export and runtime have no engine errors. The now-expanded host gate measures
35 catalog identities, 33 views, 32 live dressing profiles and 492 references;
two procedural corridor types are reported separately. This is current measured
coverage, not the older 26-view or 29-profile checkpoint.

PCK SHA256: `ed6ad81f89c1a9597cc560de5d4f8297f0fd1a45c5b4be8f37dc974f9d3f0fa6`.
Six fixture-bridge consistency tests pass. The repaired renderer and card hashes
still match the integration checkpoint above.

All three `output/batch-two/holo-status-export-{1280,1600,2560}-v1/verification.json`
files pass against that same package. Each records 61 dimension-checked full
frames (183 total), actual 1280x720 / 1600x900 / 2560x1440 output, child exit 0,
and exercised input isolation. Four-quarter operation/offline/pause and real
economy-state assertions pass without engine errors. Agent reviewed the 1280 q0
functioning frame: machinery and main projection remain readable; fine status
lenses are small at this zoom. Other frames are not automatically visually approved.

This closes fresh-package and three-size verification for this lens repair.
It does not close full-catalog visual acceptance, remaining composition work,
autonomous destination choice, or release validation. All production walls remain
at the owner-selected low height.
