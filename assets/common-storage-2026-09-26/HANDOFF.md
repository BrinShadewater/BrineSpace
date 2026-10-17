# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Additional generic storage

## Objective and acceptance
Six additional cabinets/shelves/storage props matching existing painted style, camera and size-relative pixel density. Owner visual review pending.

## Accepted decisions and constraints
Neutral generic matte materials, broad readable details, overhead/cutaway reference perspective. Preserve reference family and owner layouts. Artwork generation only.

## Current state
masters/ and game-size/: low two-door cabinet, three-drawer unit, open shelving, six-cubby rack, supply chest and wood bookshelf. Built-in image_gen used with accepted sp-science-extra3-3 and sp-recreation-extra3-5 masters as style/camera references. Exact prompts in production.json, source mapping in sources.json, hashes and export dimensions in manifest.json.

## Verification
Six RGBA exports checked for transparent exterior and visually reviewed on light/dark sheets at 1:1 library pixels beside unchanged native references. Broad tops, restrained surface texture, complete supports and readable compartments. Drawer fronts are subdued blue-gray. Proportional premultiplied-alpha LANCZOS export; visible bounds alpha>=16 with four source-pixel padding, final four-pixel margins. Visible budgets range from 115x150 for drawers to 245x155 for bookshelf. Suggested display widths follow existing 0.34 world units per library pixel. These are calibrated proposals, not runtime placement verification.

## Next action
Owner reviews. Integrate game-size files with recorded display widths only if requested; verify crew scale and access in room.
