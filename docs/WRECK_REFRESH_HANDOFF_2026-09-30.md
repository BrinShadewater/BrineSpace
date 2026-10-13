# Wreck artwork handoff — September 30

## Objective
Replace the four live room wreck families with original, consistent matte overhead
artwork, maintaining pixel density, perspective and full/stripped stage alignment.

## Accepted decisions
Current accepted prop board governs material detail and department palette.
Wreck damage affects actual furniture/casings, not only floor scatter. No baked
illumination. Equipment remains modest and peripheral; open centers retain room
scale. Clearance simulation, footprints, timing, progress mix and cutting effects
remain unchanged. Anonymous recovery uses the same existing medical-wreck fallback.
Native review exposed late equipment ghosting in the prior compositor. The hull
perimeter now draws separately, and interior source-over weights preserve overall
opacity while excluding removed equipment. Progress thresholds and simulation stay
unchanged; a native pixel test covers the late-stage regression.

## Current state
`assets/environment/wreck-refresh-v1/`: eight immutable imagegen masters, eight
1024-square calibrated derivatives, exact prompts, bake, hash ledger, validator,
README and isolated verifier. Whole selected paths in `wreck_view.gd` retain old
sources as fallback and cache failed loads. `tests/preview_wreck_refresh.gd` and
paired UID provide native stage and station capture. No new gameplay or placement.
Concurrent character/card work is outside this art batch.

## Verification
Source gate checks immutable hashes, transparent exterior, opaque center and
registered hull bounds, then requires byte-identical rebake. Native fixture covers
four families at 0/44/60/94 percent progress, normal and distant screen scales,
unchanged field data and repeated-frame equality, and a production-fog station.
The permanent environment loader and existing paid-build wreck-clearance regression
run in scratch profiles; real profile fingerprint differences are recorded.
Results: 48 source checks, eight byte-identical exports, 89 loader checks, paid
wreck-clearance regression and final native gates pass. Final native evidence:
`output/wreck-refresh-20260930-003651/summary.json`; all 2,774 owner files unchanged.
Earlier profile differences were limited to Godot logs. Reviewed captures are
`output/wreck-refresh-v1/native-stages-v3.png` and `native-station-v3.png`.

## Next action
Owner review in ordinary gameplay. No commit, push or release requested. Separate
loose hull/pipe/cargo scenery and remaining habitat art remain later batches.
