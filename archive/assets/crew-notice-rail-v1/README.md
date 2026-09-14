# Crew notice rail candidate

September 8, 2026. A shallow mounted wood/cork strip with a small clock, three
paper notices, ocean postcard and two notebook cases on a supported ledge.
`rail.png` is a2172×724 true-alpha canvas, visible240×25.50 world units.

Built-in imagegen source and exact prompt are preserved. Neutral228 source-space
registration removes the opaque white background without changing the raster.
Native material/scale and light/dark alpha review pass, with evidence in
`output/crew-notice-rail-v1/rail-scale.png` and `output/crew-notice-rail.log`.
Hashes and separate acceptance stages are in the standardized review record.

Standalone, not installed or owner accepted. Its25.50-unit visual height is NOT
proof of fit on the low hull. Measure the actual host face or furniture backing,
scale uniformly or revise the source if needed; never raise the room walls to
fit this accessory. Preserve doors. The clock is static decorative artwork.

## Measured strip-size follow-up

The inherited renderer uses `Geometry.WALL=16` from
`tools/modular_room_geometry.gd`; its horizontal wall rectangles are16 units deep.
`low-strip-fit.json` records a uniform131.74×14 alternative with1-unit margins.
Native review in `output/crew-notice-rail-v1/low-strip-fit.png` passes for size
and accessory readability. Fine paper marks are decorative at this scale.

Reproduce with Godot `--script res://tools/review_notice_rail_fit.gd`. The check
verifies current strip depth, export hash and uniform scaling. The host is drawn
schematically: this does not prove mounting-plane orientation, doorway clearance
or render ordering. The original240-unit furniture-backing study remains intact.

## Riser revision caveat

The later owner-directed riser update sets projected face height to60 units in
`rooms/whole-room/riser_geometry.gd`; wall-strip depth remains16. The strip-size
study does not constrain the available raised face or establish mounting on it.
Its recorded renderer hash is historical. Recheck current host geometry and
render ordering before installation; retain the earlier evidence unchanged.
