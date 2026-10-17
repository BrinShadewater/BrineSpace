# Project handoff

Updated: 2026-09-26 · BrineSpace · Tube material match

## Objective and acceptance
Update BRINE's tube to match the corrected corner consoles and show it in the same room preview.

## Accepted decisions and constraints
Preserve the animated character, chamber silhouette and placement, pearl-white/teal identity and separate glass/front-rim layers. No owner layouts or production room scripts changed.

## Current state
source-atlas.png is a built-in imagegen edit of the original overhead source, using the corrected corner review sheet as material reference. Full prompt and reference roles in production.json. The full atlas is retained to preserve fixed source coordinates; only the chamber polygons are sampled by this preview. Do not deploy the atlas as a complete room background.

tools/preview_brine_corners.gd now overrides room.life_texture in memory, with a 1254x1254 assertion. The existing outline, body texture, body movement, glass, bubbles, nameplate and front-occlusion passes remain in use. --old-tube bypasses the override. Existing isolated launcher is reused. Original corner-only capture remains in its original folder; new combined capture is room-preview.png here.

## Verification
Full source and native room screenshot visually reviewed. Pearl-white panels now have calmer shading and fewer bright scratches. Tube remains recognisable with the same apparent size and support-ring arrangement. Native capture completed without logged script errors and owner save fingerprint unchanged (session-f99d55642d6248079e8354d412dd5e81). BRINE is visible inside the foreground glass; the original nameplate draws on the collar. This is a visual preview, not a new walking/collision or complete animation regression test. Existing chamber footprint and placement were not changed.

## Next action
Owner review of the combined tube/corner preview. Production installation remains pending. Source artwork remains intact. Exact generated-source provenance is recorded in sources.json; SHA256 values in manifest.json.
