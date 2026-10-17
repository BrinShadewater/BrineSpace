# Project handoff

Updated: 2026-09-26 · BrineSpace · Metal corner counter variants

## Objective and acceptance
Create metal variations of the current corner counters with different objects on top.

## Accepted decisions and constraints
Preserve square wall alignment, left/right orientation, substantial cabinetry and existing export limits. Use muted steel and charcoal, diffuse painted materials, restrained accents and futuristic underwater equipment. Originals remain unchanged.

## Current state
Six variants: west communications, east sample handling, west maintenance, east refreshments, west records and east dive gear. Built-in image_gen created each asset from the corresponding refined utility counter reference. Exact prompts and references are in production.json; generated provenance in sources.json. Masters and transparent game-size exports are saved here, with SHA256 manifest and reproducible export/check scripts.

## Verification
Reviewed all six at native export size on light and dark backgrounds: clear object silhouettes, consistent cabinet perspective and subdued materials. All six RGBA/size/static entry-envelope checks passed. Maximum padded canvas 353 by 293 pixels; proposed scale 0.34 world units per source pixel. Minimum conservative north-entry gap 8.78 world units. No live-room placement, collision or character occlusion test was performed for this pack.

## Next action
Subsequent comparative audit is recorded in ART_AUDIT.md: family consistency is good, but continuous bright rims, uniform outlines, stone-like light tops and shallow inner-return depth merit targeted refinement. Export height drift is about 2.5%; world-scale acceptance remains unverified. No images changed during the audit.

Owner visual review. These are saved art candidates; production registration and actual room placement are not changed. On integration, use separate north and return draw depths as in the existing corner preview.
