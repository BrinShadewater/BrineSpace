# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: additional common props

## Objective and acceptance
Create more reusable common props matching the current art bible, reference perspective and calibrated density. Six candidates complete; owner visual review pending.

## Accepted decisions and constraints
Neutral matte materials, restrained accents and detail, overhead/cutaway facing. Preserve prior artwork. Use accepted science cabinet as style/camera reference. Do not infer live scale acceptance from native export size.

## Current state
Six new assets: tool chest, battery charging rack, cleaning caddy, personal-effects cubbies, compact refrigerator and equipment trolley. Masters and transparent game-size exports are saved here. production.json records exact prompts and built-in image_gen method; sources.json records original generated paths. build_exports.py reproduces size-only exports and review boards. manifest.json records hashes and proposed display widths.

## Verification
Six RGBA exports have alpha range 0–255, proportional resizing and four-pixel transparent canvas margins. Native light/dark sheets visually reviewed: complete silhouettes, restrained materials and coherent overhead/cutaway family. Density convention is 0.34 world units per library pixel. No runtime integration, placement, collision or crew-scale test performed.

## Next action
Owner review of review-light.png/review-dark.png. Retain original masters; use game-size exports for future placement checks. Prior audit recommendations remain separate and unchanged.
