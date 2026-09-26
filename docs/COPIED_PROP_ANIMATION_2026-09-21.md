# Copied prop animation repair

Updated September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Resolve the retained/direct render discrepancy without changing the owner's
Mining Drone Bay layout or weakening pixel checks.

## Current state
The mismatching pixel maps to cell (21,17), Mining Drone Bay, and the copied
mining_tether prop. Drawing already replaced the copy instance ID with copy_source,
but is_animated_prop received the copy ID and returned false. The retained copy
therefore stopped redrawing its clock-driven display.
scripts/room_content_canvas.gd now resolves copy_source in a shallow dictionary
copy before animation classification. Instance identity, layout coordinates,
artwork, state keys and custom draw dispatch remain unchanged. No owner file or
source raster was edited.

## Verification
Native regression tests/test_copied_prop_animation.gd (paired UID, indexed native)
uses a real mining tether source with a synthetic copy ID. Before: 12 failures
across animation counts and pixels. After: zero failures; four views, on/off states,
12 advancing frames each, exact retained/direct pixel equality.
The full tests/test_content_cache_parity.gd now passes: 49 rooms, 44 views, four
rotations, state/camera changes, live crew/drone movement and completed construction.
All 31 current capture pairs were archived and independently compared: maximum
RGB difference zero, stronger than the unchanged test threshold of 8. Process exit
0 and no engine/script errors. Static-content reuse and live-animation assertions
both pass. Evidence: output/copied-prop-animation-2026-09-21/.
The abbreviated diagnosis probe is under output/retained-pixel-trace-2026-09-21;
its different warmup exposes more stale pixels and is not the full regression gate.

## Constraints and next action
Preserved all owner layouts, library marks and art. No commit, export or publication.
The ordinary bought-prop retention optimization remains installed. No overall FPS
claim is made. Continue broader motion/room acceptance and measured performance;
current Windows/Mac exports predate these fixes.
