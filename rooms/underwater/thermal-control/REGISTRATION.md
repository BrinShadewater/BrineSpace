# Thermal registration pilot

Source v1 is registered as four south-facing assemblies. The shared geometry
helper now includes kind 4, the canonical west/south standard corner mask.
Existing masks and gameplay data are unchanged.

`tests/playtest_thermal_registration.gd` passes four rotated socket comparisons,
full visual bounds, non-overlapping footprints, 728 open-port aisle samples and
sampled source-space effect anchors. The 880-square native four-room sheet in
`output/thermal-control/registration-v2/rotations.png` was inspected: machinery
remains upright and contained, with sealed unused sockets and clear circulation.
Console and converter diagnostics are authored; paired operating pixels have
not yet been verified. Vessel and pump mechanisms remain static.

The v1 fixture incorrectly checked full travel through sealed ports, producing
16 boundary failures. V2 opens only canonical ports during route assertions and
seals sockets again for the native sheet. Failed evidence remains preserved.
V2 exited zero without SCRIPT ERROR/ERROR lines; inherited raw-image loading
warnings remain. This is not an export check.

Remaining: source floor within pipe loops, live station/card consumers,
operation/offline/pause pixels at target viewports, neighbor/walker depth tests,
relevant regressions and package verification. No owner aesthetic acceptance
is inferred from the isolated pilot.

## Station/card integration follow-up

The station renderer, placement allowlist, draft aspect-fit list and shared card
catalogue now select thermal source/card v1. Legacy art variants are retained on
disk but no longer selected for this identity. Costs, production and the legacy
Solar Array display text are unchanged. The baker accepts `--thermal`.

`tests/playtest_thermal_control.gd` passes at 1280x720, 1600x900 and 2560x1440:
four rotations, full bounds, host-specific operating/offline/pause pixels and 728
corner route samples. Logs and captures are under `output/thermal-control/native-*`.
The 1600 active station/inspector/draft capture and 512-square card were visually
reviewed; this does not imply every capture was inspected. The four gameplay
regression suites exit zero without SCRIPT ERROR/ERROR lines.

Remaining gates above now exclude station/card integration and initial state
fixtures. Real-economy states, reciprocal neighbors, walker depth, exported
thermal assets, source pipe-loop floor remnants and owner aesthetics remain.

## Economy and connected production paths

The shared walker fixture now accepts `--additional-manifest=` and `--focus=`.
Using this manifest and focus `solar_array` checks both ordered directions against
all ten production rooms and itself, at four rotations and all boundary sides:
1,344 pairs, 448 compatible, 159,176 ingress/departure samples, zero failures.
This uses the actual walker foot position and neighbor selector. It proves sampled
paths against registered collision, not actor sprite occlusion or door pixels.
Evidence: `output/thermal-control/walker.log` and `.err`.

The economy fixture accepts `--manifest=` and names the tested identities.
At 1600x900, supplied/depleted/suspended/restored states and paired frames pass
through `_apply_room_economy()` without working-cell overrides. Empty reserves
correctly leave this zero-input producer functioning. Evidence:
`output/thermal-control/economy.log`, `.err` and `economy-1600/`.
The inherited final banner mentions rotations; this economy body covers only
base rotation. Four-rotation state coverage remains the separate room fixture.

Remaining: neighbor pixel and walker-depth review, exported thermal assets,
source pipe-loop floor remnants and aesthetic acceptance.

## Both-port native crossing review

The seam fixture now accepts `--manifest=` and `--all-ports`, with dynamic
pair/frame counts. Thermal v1 passes eight production-walker arrivals: both
canonical ports at four rotations, each paired with Battery Array, at 1600x900
and fixed 30% game zoom. All 56 sampled frames were reviewed in unscaled 100x100
threshold crops (`output/thermal-control/crossings-review.png`); crop bounds and
sheet hash are recorded in `crossings-review.json`. The walker clears equipment
and thresholds; door opening/retraction and subsequent closure read correctly.
This does not cover unsampled frames, other department materials, disconnected
neighbors or every prop depth pose. Full source frames and index are preserved
in `crossings-1600/`; process exit is zero without SCRIPT ERROR/ERROR lines.

## Exchanger aperture cleanup

Registration v2 draws the manifold, two vessels and shared skid separately,
removing the central source-floor aperture without editing source pixels or
changing collision footprints. Card v2 is baked and selected by station/card
consumers; the native 512-square card was reviewed. The room fixture now checks
representative gap exclusion, retained equipment points, and effect containment
against the union of actual drawing pieces. Small peripheral pipe-loop floor
patches remain, so this is not a claim of complete silhouette cleanup.
