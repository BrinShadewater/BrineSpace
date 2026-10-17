# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: dressed wall-counter variations

## Objective and acceptance
Two new variations complete: refreshments on the wood counter, maintenance items on the drawer counter. Owner review pending.

## Accepted decisions and constraints
Preserve the existing counter designs and wall-abutting rear edges; use sparse matte accessories, neutral materials and the established perspective. Keep originals untouched.

## Current state
masters/ and game-size/ contain two transparent assets. production.json records exact built-in image_gen edit prompts and source references; sources.json records generated files. Reproducible build_exports.py and manifest.json capture proportional exports, hashes and proposed widths. Light/dark native review sheets included.

## Verification
Both exports visually reviewed on light/dark backgrounds: cabinet designs retained closely, items rest on worktops, counter width remains 245 library pixels and useful clear surface remains. RGBA alpha ranges 0–255 with transparent margins. Export density convention remains 0.34 world units per pixel. The drink dispenser rises visually above the rear edge but its base sits on the worktop; align placement to the counter rear edge, not the top of the combined silhouette. No live placement or collision verification; no runtime changes.

## Next action
Owner visual review, then wall-placement checks if integrated. Masters preserved separately from empty-counter originals.
