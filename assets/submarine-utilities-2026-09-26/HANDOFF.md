# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Unique submarine-base utility props

## Objective and acceptance
Owner requested supply/wooden crates, fire suppression, water cooler, HVAC and other futuristic submarine-base props. Eight candidates completed; visual acceptance pending.

## Accepted decisions and constraints
Current painted style, overhead/cutaway view, neutral matte materials with restrained functional accents, size-relative pixel density. Artwork only.

## Current state
masters/ and game-size/ contain supply-crate stack, wooden crate, fire-suppression station, closed water dispenser, HVAC unit, air scrubber, emergency cabinet and maintenance cart. Built-in image_gen with accepted sp-science-extra3-3 master reference. Exact prompts and original file mapping in production.json/sources.json; dimensions, alpha, source/export hashes and suggested display widths in manifest.json.

## Verification
Eight RGBA exports checked for transparent exterior and reviewed at native library pixel scale on light/dark backgrounds beside accepted reference exports. Readable large fittings, complete wheels/supports, broad top surfaces. Export uses premultiplied-alpha LANCZOS, alpha>=16 bounds with four source-pixel padding and four final pixels of margin. Suggested display widths use established 0.34 world units per library pixel; size budgets range from 90x140 for dispenser through 190x140 for HVAC. No integration, functional simulation, collision or crew interaction checks implied. Fire suppression is a fictional visual prop, not an engineered system specification.

## Next action
Owner reviews artwork; use calibrated exports and recorded display widths for any later requested integration.
