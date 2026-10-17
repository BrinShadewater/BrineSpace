# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: servers, communications and stocked shelves

## Objective and acceptance
Six generic props complete: server cabinet, low server pedestal, communications console, wall communications panel, supply shelving and personal-item shelving. Owner review pending.

## Accepted decisions and constraints
Current accepted science-cabinet reference provides style/camera. Matte painted industrial materials, neutral palette, sparse muted screen graphics, overhead/cutaway view and readable detail. Preserve prior assets.

## Current state
masters/ and game-size/ contain six transparent PNGs each. production.json records exact built-in image_gen prompts and reference; sources.json records original generated paths. build_exports.py reproduces calibrated exports and review sheets; manifest.json records dimensions, hashes and proposed display widths.

## Verification
Six RGBA exports have alpha range 0–255 and transparent margins. Native light/dark review complete: intact silhouettes, visible tops, consistent straight-on facing, subdued screens and separated shelf items. Material finish broadly matches accepted art. Tall server is intentionally taller than the low pedestal; wall panel is intentionally shallow. Density convention remains 0.34 world units per library pixel, with individual proposed sizes. Live fit and wall-panel mounting untested; no runtime or owner layout changes.

## Next action
Follow-up audit complete: AUDIT.md, audit-checks.json and native audit-light/dark.png comparisons record consistent declared density and broadly matching style/perspective. Tall-server scuffs are optional polish; wall-panel mounting perspective remains a live-room check. No artwork changed.

Owner review of review-light.png/review-dark.png, followed by world-scale and mounting checks if integrated.
