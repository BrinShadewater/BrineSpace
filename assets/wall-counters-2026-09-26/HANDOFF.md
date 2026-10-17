# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: counters designed to sit flush with walls

## Objective and acceptance
Four new wall-counter candidates complete: drawer counter, long cabinet counter, utility sink counter and wood-top counter. Owner visual review pending.

## Accepted decisions and constraints
Match the current visual bible and accepted science cabinet style/camera reference. Neutral matte materials, restrained detail, straight rear edges, no rear fittings projecting beyond the worktop. Preserve existing artwork.

## Current state
masters/ holds four original generated PNGs; game-size/ holds proportionally calibrated transparent exports. production.json contains exact prompts and built-in image_gen method. sources.json preserves source provenance. build_exports.py reproduces exports and review boards; manifest.json contains hashes, dimensions and proposed display widths.

## Verification
Reviewed native light and dark sheets: all four show straight horizontal rear edges and complete silhouettes; sink faucet stays within the countertop footprint. Painted finishes and visible-top perspective are coherent with the reference family. Four RGBA exports have alpha range 0–255 and four-pixel outer transparent margins. Proposed density is 0.34 world units per source pixel.

These are individual wall-abutting candidates, not a verified seamless modular kit: front heights and worktop depths vary. No wall, floor or cast shadow is baked in. Wall contact requires aligning the visible rear edge rather than the padded PNG canvas. No runtime placement, collision or crew-height check performed; no registry or owner layouts changed.

## Next action
Owner review of review-light.png and review-dark.png. For integration, test rear-edge contact against actual room walls at proposed scale, then record placement anchors.
