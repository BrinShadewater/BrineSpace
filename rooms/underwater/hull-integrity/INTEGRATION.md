# Hull Integrity Control initial integration

Canonical `shield_generator` now renders four registered south-facing assemblies
with shared north/south geometry. Plain wall samples exclude the generated
midpoint inserts. Station, card catalogue and aspect-fit consumers select card
v1; old art files remain intact. Gameplay values and legacy catalogue text are
unchanged. The baker accepts `--hull` with a new output destination.

Operating visuals comprise a bounded pressure-compartment diagram with moving
scan line and a local injector gauge. Calibration rig and stored repair parts
are static. These cues do not implement new strain/repair mechanics.

`tests/playtest_hull_integrity.gd` passes at 1280x720, 1600x900 and 2560x1440,
covering four rotations, host-specific motion/offline/pause, full bounds,
non-overlapping footprints, 728 aisle samples and screen containment. Four
gameplay regression suites also exit zero without SCRIPT ERROR/ERROR lines.
Evidence is under `output/hull-integrity/`; inherited Image.load warnings remain.
The 512-square card and 1600 active station/card/inspector frame were reviewed.

Remaining: economy-driven states, production walker and boundary/depth review,
export coverage, small source-floor remnants within enclosed equipment frames,
and owner aesthetic acceptance. Captured images are not all implicitly reviewed.

## Economy and traversal follow-up

The focused walker sweep against the ten-room pack, Thermal Power Control,
Acoustic Communications and itself passes 1,600 ordered pairs (512 compatible),
178,568 production foot samples, zero failures. It checks actual neighbor
selection and collision, not sprite occlusion. Four real economy states and
paired frames pass at base rotation/1600x900, without working-cell overrides.
Evidence: `output/hull-integrity/walker.*`, `economy.*`, `economy-1600/`.

Both ports across four rotations pass eight production arrivals against Battery
Array. All 56 sampled doorway frames were visually reviewed as unscaled 100x100
crops at fixed 30% zoom; approaches and thresholds remain clear with appropriate
door retraction/closure. Full frames and index are in `crossings-1600/`; review
scope, crop bounds and sheet hash are in `crossings-review.json`. All runs exit
zero with no SCRIPT ERROR/ERROR lines. Unsampled frames, other neighbor materials,
blocked-boundary pixels and full prop-depth poses remain outside this evidence.

The common final fixture banner now defers coverage to subject-specific output,
so an economy-only subclass no longer inherits a false four-rotation claim.
Earlier logs retain their original wording and must be read against fixture scope.
