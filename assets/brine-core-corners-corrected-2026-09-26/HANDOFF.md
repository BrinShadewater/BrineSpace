# Project handoff

Updated: 2026-09-26 · BrineSpace · Core corner corrections

## Objective and acceptance
Correct the remade core corners' color, hard highlights, inconsistent density and tight doorway envelopes. Preserve originals and owner layouts.

## Accepted decisions and constraints
Pearl-white housings, subdued teal modules, NW/NE facing and exterior wall contact. These are candidate assets with explicit proposed placement; old screen coordinates and registrations cannot be reused unchanged.

## Current state
Two imagegen-edited masters and transparent exports. Exact prompts in production.json; provenance in sources.json; hashes, dimensions and proposed content origins in manifest.json. build_exports.py resizes proportionally with premultiplied alpha at shared 0.34 world units/pixel. Content placement excludes 4px transparent padding on each edge.

## Verification
Both reviewed at native export size on light/dark backgrounds. Masked pale RGB medians improved to NW 220/215/209 and NE 216/211/205 from 208/200/192 and 192/186/174. Original medians were 225/221/215 and 223/218/212: slight warmth remains. Borders softened; some cylinder highlights remain. No exact colorimetric or complete camera match claimed.

Content world sizes NW 137.70x124.44 and NE 135.66x127.84. Proposed anchors preserve saved q0 outer west x=-188.6473, east x=186.1587, top y=-192; NE begins x=50.4987. North 72-unit lane clearances 14.95/14.50 leave 4.95/4.50 beyond a 10-unit buffer. Side clearances 31.56/28.16 leave 21.56/18.16 beyond the same buffer. Conservative full bounding envelopes pass; old collision fractions are not needed for this static result. This includes modest overall size reduction, not merely shortening individual modules.

RGBA, proportional size and static clearance assertions passed. These apply only to proposed placements; actual owner layouts remain untouched. Native walking, crew usability, depth sorting and operating-screen registration are unverified.

## Next action
Owner visual review, then isolated integration preview with new registrations, screen rectangles and collision regions before production replacement. CURRENT_STATUS.md could not be updated because its current bytes are not valid UTF-8; left unchanged to avoid interfering with concurrent edits.

Native preview: tools/preview_brine_corners.gd and .ps1 render the corrected corners in the actual core room with chamber, south bench and standing crew. room-preview.png visually reviewed; capture run completed without script errors and owner save fingerprints unchanged. North/return use separate draw depths. Live walking and screen overlays remain unverified. Interactive preview opened.
