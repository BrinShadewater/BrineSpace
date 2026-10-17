# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: binders, books and globe counters

## Objective and acceptance
Three dressed counter variations complete; owner review pending: binder storage, books/open reading material, and tabletop globe with atlas and rolled chart.

## Accepted decisions and constraints
Preserve the earlier wood and drawer counter designs, matte painted materials, overhead/cutaway perspective and wall-abutting rear edges. Sparse accessories and clear worktop areas. Originals preserved.

## Current state
masters/ contains three built-in image_gen edits; game-size/ contains calibrated transparent PNGs. production.json records exact prompts and edit references; sources.json records generated originals. build_exports.py reproduces exports and review sheets. manifest.json records dimensions, hashes and proposed display widths.

## Verification
All three RGBA exports have alpha range 0–255 and transparent margins. Native light/dark review complete: counter structures retained closely, accessory footprints on worktops, readable restrained detail and matte materials. Export width is 245 library pixels plus padding, using 0.34 world units per pixel. Accessories extend upward visually; future wall alignment must use the counter rear edge, not combined image bounds. Live room fit remains unverified. No runtime or layout changes.

## Next action
Owner review of review-light.png/review-dark.png; placement checks when integrating.
