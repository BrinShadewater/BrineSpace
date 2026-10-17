# Common props handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: neutral common prop expansion

## Objective and acceptance
Create reusable props covering crates, barrels, couches, chairs, bookcases, standing plants, containers, table/chair assemblies, lockers and workstations in the current asset-bible style.

## Accepted decisions and constraints
Owner requested no department color themes: neutral steel, charcoal, warm wood and fabric with small generic accents. Current September 26 bible governs. Existing art and owner layouts preserved. Built-in image_gen used; no Higgsfield.

## Current state
Ten selected transparent PNGs in masters/. Original ten generations plus six revisions preserved in raw/. Container and table/chairs use revised facing/camera; others retain original versions because revisions offered no clear improvement. production.json contains exact generation and revision prompts and source paths. manifest.json records selected dimensions, alpha and SHA-256. review-size/ contains aspect-preserving comparison thumbnails, not assigned world-scale exports. review-light.jpg and review-dark.jpg show all ten.

## Verification
All ten masters decode as RGBA with zero-alpha background pixels. Agent visually reviewed full generation previews and composited comparison sheets on light/dark backgrounds: neutral palette, complete visible supports, open furniture gaps, no visible exterior haze at comparison size. The raw viewer exposed RGB data behind zero alpha; apparent haze initially prompted unnecessary repair attempts. Composited alpha is the relevant evidence. PNG paths are covered by existing Git LFS attributes. No code or live registrations changed, so no gameplay tests run. Owner acceptance and actual crew-relative scale, footprints and runtime placement remain unverified. Table assembly retains deeper legs than the locked couch exemplar; review in context before registration.

## Next action
Owner visual review of this candidate pack. If selected for integration, assign crew-relative sizes, floor contacts and interaction footprints, register without changing owner layouts, then verify native gameplay. This pack does not supersede the locked art references.
