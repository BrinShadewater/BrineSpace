# Josh and River artwork polish

September 26, 2026. Owner requested the same artwork/animation pass as Margot.
Selected in the source game; executable not rebuilt. Owner visual review pending.
Preview: http://127.0.0.1:8774/ .

## Owner consistency correction

Owner flagged Josh's colour changing between animations. Selected welding V3 and
shutdown V2 now match the muted lavender movement reference more closely; source
edits preserve the pose grids and detailed shading. Earlier sheets remain intact,
and pre-correction exports are frozen under `review/pre-consistency/`.
`review/colour-consistency.png` compares four directions against idle. The head-paint
median blue-minus-red diagnostic was63–70 for welding and65–79 for standby; it is
now48–53 and49–54 respectively, compared with idle51–57. This metric supports the
visual review, not a guarantee of identical lighting across differently angled poses.

The same pass checks both robots at2.2672 source pixels per world unit. Maximum
source resize factors are0.757 (Josh) and0.521 (River), so no source is enlarged.
Both retain184px canvases and distinct body scales. Final-alpha ground registration
now puts every rolling frame exactly at y172, removing a one-pixel resize-rounding
wobble. River's authored colours are retained. All144states/439references still
pass coverage, alpha, bounds, timing and exact action-endpoint checks.
`audit_consistency.py` rebuilds diagnostics and the before/after review board.
Final native robot and companion-water regressions pass (`robot-consistency-native`
and `robot-consistency-water` logs); both entire real-profile fingerprints unchanged.
Corrected torch/standby joins sampled at four times in each of four directions in
the browser without console errors. Native west welding and colour board reviewed.

## Contract

Josh retains lavender upper shells, rectangular binocular head, amber eyes, both
arms and charcoal twin tracks. River retains ivory/sage spherical head and wheeled
chassis with amber camera/status lighting. Current `portraits-brine-style-v1`
portraits establish identity; four-direction motion sources establish body design.
No portrait bindings changed. Fine painted industrial shading follows the visual
bible; no 64-colour reduction. Each direction is authored independently.

184x184 canvas, pivot (92,172), standingHeight 148, walk stride 0.1 cells.
Josh standing anatomy is approximately 140 source pixels, River 88: world sizes
remain approximately 61.8 and 38.8 units respectively. The common denominator is
not an instruction to make the companions equally tall. Margot uses the same density.
River waterline is source y140; clearance derives from the upright lower chassis.

| Pack | States | Frame references |
|---|---:|---:|
| Josh locomotion | 28 | included below |
| Josh actions | 48 | total 228 |
| River locomotion | 28 | included below |
| River actions | 32 | included below |
| River water | 8 | total 211 |

Movement covers cardinal idle/rolling, start/stop and all 12 directed turns.
Josh has watch, turn, torch deploy/weld/stow and shutdown/restart chains.
River has scan, inspect, boot and moving/stationary floating. Existing gameplay,
repair rewards, flood thresholds and navigation rules are unchanged.

## Rebuild and source selections

Run `python character/robot-polish-v1/build.py`, then `validate.py`.
Raw generations and exact prompts are in `sources/`; hashes and extraction boxes
are in `review/`. Rebuilds never invoke generation. Baselines are frozen copies of
the previous active packs, never overwritten by a rebuild. Runtime submanifests
share the full pack frame files.

All new sources were authored with the built-in image generator. Motion prompts
use current portraits plus the previous full-body sheet for construction; other
sources use extracted new canonical directions. `diagonals-v1` references both
canonical boards. Raw outputs remain intact, including rejected frames:

- `josh-actions-v1` supplies watching only. Its powered-off face drift was rejected;
  dedicated `josh-power-v1` replaces shutdown, and a single terminal pose holds.
- `josh-weld-v1` front deployment swapped arms. V2 corrects it. The generated side
  rows are east then west, so packaging explicitly reassigns them, never mirrors.
  Side welding still merits owner review for far-arm readability.
- Both original turn sheets repeated angles or delivered wrong endpoints. They
  remain as source history but their frames are not selected. The separate
  `diagonals-v1` sheet supplies southwest/northwest/northeast/southeast poses;
  exact cardinal idle endpoints form quarter turns. Reverse/half turns reuse and
  compose these authored views, not six newly authored intermediates per turn.
- River action columns 4/8 (one-based) turn too far in some views and are omitted.
  Inspection reverses the authored descent for recovery. The west boot's first
  source cell faces south; it is omitted. Remaining west frames show startup lift.
- Actions share exact idle endpoints. Registration anchors lower chassis instead
  of total reaching-arm width. Torch registration uses head center, as in the old
  pipeline. No painted replacement pixels, geometric limb synthesis or upscaling.
- True source alpha is thresholded at128; crops preserve silhouette islands inside
  their recorded bounds. LANCZOS downsampling retains painted colours and binary alpha.

## Evidence

`review/validation.json`: 144 states /439 frame references, complete former key
coverage, bounds/alpha/timing/joins, four distinct rolling frames per direction,
runtime partition paths, source hashes and unchanged legacy baselines pass.
These are export checks, not a claim that every gait is artist-approved.

80 browser action/facing selections exercised without console errors; source
contact sheets and selected native full-station captures reviewed. The browser's
scale board is explicitly an illustrative composite; native links are actual game
captures. The preview normalizes old/new chain durations for comparison.

Godot4.7.2:
- `tests/test_robot_polish.gd`: native PASS,28 directional action captures; verifies
  active184px/148 calibration, complete packs, cached-container independence,
  terminal shutdown, real-core spawn, pause and checkpoint restore.
- `tests/test_companion_water.gd`: native PASS; River real-room float routes,
  interruption, pause/restore/drain; Josh flood shutdown/recovery and blocked routes.
- `tests/test_animation_expansion.gd`: headless PASS, existing companion actions,
  transitions and snapshot playback regression coverage.

The active-binding audit validates all five robot runtime partitions (144 states).
Its global result still reports12 pre-existing portrait-registry mismatches against
the newer `portraits-brine-style-v1` selection. No robot animation findings; unrelated
portrait records were not rewritten. Full output: `review/bindings-audit.log`.

Commands use `tools/run_margot_check.py` with labels `robot-native-fixed`,
`robot-water`, `robot-expansion`, isolating APPDATA and copying only room layouts.
Logs/fingerprints are under `output/margot-polish-native/`; captures under
`output/robot-polish-native/` and `output/companion-water/`.
The first custom fixture failed restore because it manually cleared action names
without their clocks; corrected to use the production reset, then passed.
During the water run an unrelated `new-room-native-test.loop.comms.json` and logs
changed in the real profile, causing the wrapper's profile guard to fail although
the water test itself passed. Those concurrent files were left untouched. The
final native and expansion runs each verified the entire real profile unchanged.

No executable rebuilt. Owner art/motion acceptance remains the next review.
