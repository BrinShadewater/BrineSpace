# Battery Array registered pass

The existing Battery Array now uses four registered source assemblies and the
shared geometry in station, placement preview, draft and inspector art. The
source remains immutable at 1254 square. Source-pixel polygon outlines, ground
pivots, uniform scale, collision footprints and wall sample regions live in
`rooms/production-ten/battery_array_view.gd`. Canvas exteriors are excluded by
registration; the source image itself has not been cleaned or overwritten.

Bank centers rotate while equipment stays south-facing. Warm charge-slot cues
and breaker traces follow their host transform and stop with operation. Cable
distribution stays still. These are operating cues, not a new stored-charge model.
Potential sockets are sealed by the shared hull until reciprocally connected.
The source's dark isolated floor pixels inside concave cable silhouettes remain
a registration tradeoff requiring close visual review.

Both PNG maps and alternate-art selection use the native-baked v1 card. Draft
thumbnails use full-image aspect fit. Original art and player saves are preserved.

## Verified evidence

- `tests/playtest_battery_array.gd` passes at 1280x720, 1600x900 and 2560x1440.
- Four rotations: complete visual bounds inside the safety margin, non-overlapping
  collision footprints, 1456 center-to-port samples per viewport.
- Per-host active motion, inactive stillness, paused equality and effect-point
  containment pass. The static distribution assembly is explicitly exempt from
  expected motion, rather than given an arbitrary effect.
- Native v1 card, quarter-turned room crop and 2560 station/draft/inspector frame
  inspected. Captures and logs: `output/production-ten/battery-native-*`.
- Synergy, discovery progression, polish gameplay and run balance suites pass.
- No ERROR or SCRIPT ERROR lines in these test stderr logs. Existing inherited
  raw-image export warnings remain. Source/card PNGs have LFS attributes.

## Remaining acceptance

This is initial integration, not complete production acceptance. Dedicated
neighbor crossings with the production actor, disconnected/incompatible seam
captures, economy-driven power states, mature mixed-station zoom, isolated
packaging and owner visual approval remain. Other nine requested batch rooms
remain at generated source stage. No balance or discovery changes were made.
