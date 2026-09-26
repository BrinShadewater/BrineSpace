# Reactor console operating feedback

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Restore a restrained operating cue on the bought Reactor console using the existing
library renderer. This is console feedback, not a replacement for fan/rotor animation
or completion of the broader animation and art-polish goal.

## Accepted decisions and constraints
No source raster edits, Higgsfield, owner-layout changes, library mark changes,
new rendering system or release export. Preserve existing screen/casing details.

## Current state
Only npp2-107 in rooms/tileset-library/props.json gains operating_screens
[[200,701,26,12]] and muted green operating_screen_color #73aa87cc.
Coordinates are absolute in reactor-hall/tile-B-03.png. The current registered
renderer already maps these through source pivot, scale and mirror transforms.
The trace is gated by room.operating and driven by room.machine_clock.
Added tests/test_reactor_console_feedback.gd and UID to room-art with explicit
native lane (auto-classification incorrectly treated its headless guard as safe).
All other registration records match the backup; no source images changed.

## Verification
Native four-view test passes: active clocks change pixels only inside the monitor;
off-state clocks produce identical images; repeated held clock produces identical
images. Screen samples visually inspected. This is held-clock evidence, not a new
UI-pause integration test. Full registry validator: 10,507 props, zero problems.
Test runner list resolves native lane correctly. Evidence and registry backup:
output/reactor-operating-feedback-2026-09-21. Geometry is unchanged, so earlier
Reactor route evidence is not replaced by this pixel test.

## Next action
Continue other animation and room reviews. Reactor and cooling body sprites remain
static. Existing Windows/Mac test packages predate this registration, the newer
room layouts and navigation cancellation fix; batch the next release checkpoint.
