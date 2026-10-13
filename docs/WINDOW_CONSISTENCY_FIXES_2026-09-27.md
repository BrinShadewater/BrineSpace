# Window consistency fixes

Updated: 2026-09-27 · Project: BrineSpace · Task: ocean-window consistency pass

## Objective and acceptance
Owner authorized fixes from the pixel-density, colour and style audit. Bring window detail and materials closer to room walls; maintain the approved darker greens and smaller, centered mounts. Owner visual review remains pending.

## Accepted decisions and constraints
North riser walls only, with no doorway or exterior hatch. Preserve room/material assignments, 56-unit center mount, side mounts lowered seven units and the prior reduced doors. No geometry or gameplay changes in this pass. Original masters preserved byte-for-byte.

## Current state
- `rooms/whole-room/ocean_windows.gd` loads calibrated textures with the original logical aspects and mount coordinates.
- `tools/build_window_render_assets.gd` (+ paired UID) exports all 14 at approximately five texels per representative display unit, close to measured wall sources (4.92–5.59). Cubic reduction, alpha-edge repair and four-pixel transparent padding; runtime nearest filtering retained. Different corridor spans can still vary effective density.
- Seven built-in imagegen edits in `assets/ocean-windows-v3/refined/`: three matte dark-green frames, duller brass, more readable small porthole, subdued blue/octagonal ocean exposure. Prompts, raw output locations and registrations retained. Generative edits can shift small painted details; logical silhouettes and mount dimensions are preserved.
- `calibrated/` contains 14 runtime PNGs and catalog; total uncompressed RGBA storage 2,982,276 bytes. Original `sources/` stays intact; `before-consistency/` saves prior room captures and runtime source.
- Gallery builder and native review updated for calibrated registrations. Gallery at http://127.0.0.1:8897/index.html?consistency=fixed includes current sources, 56 native views and before/current comparisons.

## Verification
Offline export passed; source hashes confirm all 14 original masters unchanged. All 14 registrations, transparency, source coverage, aspect fits and doorway/hatch exclusions pass. Native Godot review: 56 captures, zero failures across five rooms and three corridor shapes/four orientations/three corridor finishes. Representative native room and corridor captures visually inspected. Verification JSON and full logs live beside the gallery.

Both exporter and native review assert a scratch APPDATA directory. Native engine exit was zero; wrapper exit was one because the independently running game changed real `last_session.json` during the review. No owner files restored or overwritten by this work. This is a static visual check, not a motion/shimmer test. Packaged exports and baked cards have not been rebuilt.

## Next action
Owner review of the updated gallery. If accepted, include calibrated artwork in the next maintained release export and card bake; do not treat these editor captures as packaged-game acceptance.
