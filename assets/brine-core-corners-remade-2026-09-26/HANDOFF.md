# Project handoff

Updated: 2026-09-26 · BrineSpace · BRINE Core corner remakes

## Objective and acceptance
Remake the BRINE Core room's two corner pieces using the current matte painted prop direction.

## Accepted decisions and constraints
NW life-support and NE analysis/oxygenation identities were established from rooms/full-wall-v1/registrations/brine-corner-service-nw.json and brine-corner-analysis-ne.json and the existing room card. Preserve pearl-white construction, restrained teal, original facing and functional bays. Current bible overrides older skill camera guidance.

## Current state
Two new masters and transparent exports, produced with built-in image_gen. Exact prompts and references in production.json; sources in sources.json; hashes and proportional export dimensions in manifest.json. Original assets, registrations, operating-screen coordinates and owner layouts remain unchanged. Source art serves as subject/layout reference; locked sp-science-extra3-3 is the style reference.

## Verification
Both exports visually reviewed on light and dark backgrounds at native export size. Recognizable equipment arrangement and orthogonal wall-contact runs retained; source white exterior/inner void replaced with transparency. Cabinet fascia and component shading remain shallow, with some cylinder highlights: this is a conservative visual remake, not a new cabinet geometry design. Both exports have alpha range 0–255. Proportional premultiplied-alpha resizing, maximum content box 376 by 350 pixels plus padding. Size cap is approximately based on registered base width 128 world units at the preceding 0.34 convention; actual final placement scale is not established by it.

## Next action
Follow-up audit in ART_AUDIT.md identifies warm/dark color drift, about 5.5% unequal visible pixel density at owner q0 scale, a longer NE return and insufficient conservative north-approach margins. Read audit-results.json before revising geometry; these candidates are not ready for replacement. Audit did not modify artwork or owner layouts.

Owner review. These are candidate artwork, not installed replacements. Existing live registration pieces, screen rectangles and collision geometry reference the old images and must be regenerated for any integration, then tested with actual crew and door approaches. The old default layouts also apply per-piece scale multipliers, so do not claim the generic corner clearance check covers these pieces.
