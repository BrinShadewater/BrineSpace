# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: opposite-wall corner counters

## Objective and acceptance
Three matching northeast-corner variants complete: utility, reading and refreshments. Owner review pending.

## Accepted decisions and constraints
Interpret other wall as opposite upper corner: horizontal north run, vertical east return, open lower-left inner corner. Preserve corrected cabinet proportions and room-neutral finish; existing northwest variants retained.

## Current state
masters/ and game-size/ contain three transparent PNGs. production.json records exact built-in image_gen edit prompts and references; sources.json records generated originals. Reproducible exporter, manifest and light/dark boards included.

## Verification
Native light/dark review confirms right-hand returns, straight outer top/right edges, matching materials and recognizable accessories. Full RGBA range with transparent margins. Same proportional 345x285 visible-size budget and 0.34 world units per source pixel. clearance-checks.json confirms positive bounding-box gaps against the previous conservative entry lanes at a proposed northeast placement ending at x=182, starting y=-186. Static calculation only; no live mounting or navigation verification. Accessory tops must not be used as wall anchors. No runtime or owner layout changes.

## Next action
Owner review and eventual actual-room anchor/crew checks. These are new opposite-wall variants, not replacements for northwest versions.
