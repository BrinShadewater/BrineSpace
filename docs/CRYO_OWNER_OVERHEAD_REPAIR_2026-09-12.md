# Cryo Chamber owner overhead repair

Updated September 12, 2026. This pass replaces the Cryo Chamber wall bank's
rotated shallow elevations with one coherent orthographic overhead installation.
It does not change recovery rules, pod logic, gameplay, or character animation.

## Changed state

The selected bank preserves the accepted compressor, two closed coolant vessels,
folded heat-exchange coil, insulated pipes, blue coolant cylinder, terminal,
three samples and gas bottle. Equipment now presents top lids and shallow service
surfaces rather than upright vessel bodies, cabinet fronts, or a vertical monitor.
Matte grey-ivory enamel, charcoal insulation, subdued brass and muted coolant blue
remain the material authority.

`assets/cryo-directional-v2/north-overhead-v1.png` is the cleaned canonical
source. Exact 90-degree rotations produce north, east, south and west sprites, so
the overhead camera cannot drift between walls. Each registration has its own
direction and wall-contact metadata. The old registrations are preserved under
`assets/cryo-directional-v2/original-registrations`; prompt attempts, rejection
reason, hashes, alpha cleanup and build metadata remain beside the selected art.

The initial generated candidate was rejected because it retained tall vessel
fronts. The selected candidate contained one 693,759-pixel machinery silhouette
plus 5,100 disconnected alpha speck pixels; the generic cleanup tool removed only
the 1,623 secondary components.

## Review and validation

Real-display OpenGL captures in `output/cryo-owner-repair-2026-09-12/native`
cover all four rotations and were inspected. The bank stays shallow, readable and
flush to every outer wall; the room's independent pods and console remain visible.
The refreshed q0 west card is selected by all three current card consumers.

The current q2 capture contains `cryo_pod_1` as well as `cryo_pod_0`, while the
earlier baseline contained only pod 0. That changed during concurrent room work;
this asset pass did not edit pod selection or placement and makes no gameplay
claim about it.

- 176 furnished layouts and 20 side variants pass.
- 47 card identities and all three Cryo card bindings pass.
- Architect recovery and Cryo recovery suites pass.

Evidence is recorded in `assets/cryo-directional-v2/review.json` and test runs
`20260912-182448-headless`, `20260912-182611-headless`, and
`20260912-182650-headless`. No executable or release export was built.
