# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Less shiny plants

## Objective and acceptance
Owner requested a slightly less shiny finish on plant props. Ten revised plant candidates produced; owner review pending.

## Accepted decisions and constraints
Soften leaf highlights and bright planter rims while retaining painted shading, colors, plant identities and calibrated scale. Preserve original artwork.

## Current state
masters/ and game-size/ contain ten revised plants, including the earlier common standing plant and all three tall plants. Built-in image_gen edits; exact prompts in production.json and input/output mapping in sources.json. manifest.json records hashes, dimensions and prior suggested display widths. Earlier calibrated pack remains preserved; use these ten exports as its plant replacements.

## Verification
Ten transparent RGBA exports reviewed at calibrated size on light/dark backgrounds. Leaf highlights are softer; pots retain diffuse material variation with reduced bright rims. Existing canvas sizes and suggested display widths retained. New visible bounds fit proportionally inside previous visible sizes using premultiplied-alpha LANCZOS and alpha>=16 bounds with four source-pixel padding. No runtime integration performed.

## Next action
Owner reviews matte finish. Use these plant replacements for future integration with the calibrated pack.
